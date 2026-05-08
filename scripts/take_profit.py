"""A股止盈策略分析 - 过山车率计算与策略回测.

功能:
    1. 计算过山车率（Rollercoaster Rate）
    2. 回测三种止盈策略：固定止盈、移动止盈、分批止盈
    3. 输出年化收益率、最大回撤、夏普比率等指标
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.config import pro, STOCK_POOL, BACKTEST_START, BACKTEST_END, rate_limited_call


def fetch_daily_data(ts_code: str, start: str, end: str) -> pd.DataFrame:
    """获取日线行情数据.

    Args:
        ts_code: Tushare 股票代码，如 '600519.SH'
        start: 开始日期，格式 YYYYMMDD
        end: 结束日期，格式 YYYYMMDD

    Returns:
        按日期升序排列的 DataFrame，包含 trade_date, close, high, low 等列
    """
    df = rate_limited_call(pro.daily, ts_code=ts_code, start_date=start, end_date=end)
    if df is None or df.empty:
        logger.error(f"未获取到 {ts_code} 的行情数据")
        return pd.DataFrame()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df = df.sort_values("trade_date").reset_index(drop=True)
    return df


def calc_rollercoaster_rate(
    df: pd.DataFrame, profit_threshold: float = 0.5, drawdown_threshold: float = 0.5
) -> dict:
    """计算过山车率.

    每月第一个交易日入场，浮盈达到 profit_threshold 后，
    如果从峰值回撤超过 drawdown_threshold（利润层面），则计为一次过山车。

    Args:
        df: 日线数据 DataFrame
        profit_threshold: 触发监控的浮盈阈值（默认 50%）
        drawdown_threshold: 利润回撤阈值（默认 50%，即利润腰斩）

    Returns:
        包含 entries, rollercoasters, rate, details 的字典
    """
    df = df.copy()
    df["year_month"] = df["trade_date"].dt.to_period("M")

    monthly_first = df.groupby("year_month").first().reset_index()
    entries = []

    for _, row in monthly_first.iterrows():
        entry_date = row["trade_date"]
        entry_price = row["close"]
        future = df[df["trade_date"] > entry_date].copy()

        if future.empty:
            continue

        peak = entry_price
        hit_threshold = False
        is_rollercoaster = False
        peak_profit = 0.0

        for _, future_row in future.iterrows():
            current_price = future_row["close"]
            peak = max(peak, current_price)
            current_profit = (peak - entry_price) / entry_price

            if current_profit >= profit_threshold:
                hit_threshold = True
                peak_profit = max(peak_profit, current_profit)

            if hit_threshold:
                actual_profit = (current_price - entry_price) / entry_price
                profit_drawdown = (peak_profit - actual_profit) / peak_profit if peak_profit > 0 else 0
                if profit_drawdown >= drawdown_threshold:
                    is_rollercoaster = True
                    break

        entries.append({
            "entry_date": entry_date,
            "entry_price": entry_price,
            "hit_threshold": hit_threshold,
            "is_rollercoaster": is_rollercoaster,
        })

    total = len([e for e in entries if e["hit_threshold"]])
    rollercoasters = len([e for e in entries if e["is_rollercoaster"]])
    rate = rollercoasters / total if total > 0 else 0.0

    return {
        "entries": len(entries),
        "qualified_entries": total,
        "rollercoasters": rollercoasters,
        "rate": rate,
        "details": entries,
    }


def backtest_buy_and_hold(df: pd.DataFrame) -> dict:
    """买入持有策略基准.

    Args:
        df: 日线数据 DataFrame

    Returns:
        包含年化收益率、最大回撤、夏普比率的字典
    """
    prices = df["close"].values
    total_return = (prices[-1] - prices[0]) / prices[0]
    days = (df["trade_date"].iloc[-1] - df["trade_date"].iloc[0]).days
    annual_return = (1 + total_return) ** (365 / days) - 1

    cummax = np.maximum.accumulate(prices)
    drawdowns = (prices - cummax) / cummax
    max_drawdown = drawdowns.min()

    daily_returns = pd.Series(prices).pct_change().dropna()
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() > 0 else 0

    return {
        "strategy": "持有不动",
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
        "win_rate": None,
    }


def backtest_fixed_take_profit(df: pd.DataFrame, target_pct: float = 0.2) -> dict:
    """固定止盈策略回测.

    每月第一个交易日买入，涨到 target_pct 时卖出，否则持有到下次入场前一天。

    Args:
        df: 日线数据 DataFrame
        target_pct: 止盈目标百分比

    Returns:
        策略回测结果字典
    """
    df = df.copy()
    df["year_month"] = df["trade_date"].dt.to_period("M")
    monthly_first = df.groupby("year_month").first().reset_index()

    trades = []
    for i, row in monthly_first.iterrows():
        entry_date = row["trade_date"]
        entry_price = row["close"]

        if i + 1 < len(monthly_first):
            next_entry = monthly_first.iloc[i + 1]["trade_date"]
            window = df[(df["trade_date"] >= entry_date) & (df["trade_date"] < next_entry)]
        else:
            window = df[df["trade_date"] >= entry_date]

        exit_price = entry_price
        for _, day in window.iterrows():
            if (day["close"] - entry_price) / entry_price >= target_pct:
                exit_price = entry_price * (1 + target_pct)
                break
            exit_price = day["close"]

        ret = (exit_price - entry_price) / entry_price
        trades.append(ret)

    return _calc_strategy_metrics(f"固定止盈{int(target_pct*100)}%", trades)


def backtest_trailing_stop(df: pd.DataFrame, trail_pct: float = 0.15) -> dict:
    """移动止盈策略回测.

    每月第一个交易日买入，浮盈达到 trail_pct 后开始跟踪，
    从最高点回撤超过 trail_pct 时卖出。

    Args:
        df: 日线数据 DataFrame
        trail_pct: 移动止盈回撤阈值

    Returns:
        策略回测结果字典
    """
    df = df.copy()
    df["year_month"] = df["trade_date"].dt.to_period("M")
    monthly_first = df.groupby("year_month").first().reset_index()

    trades = []
    for i, row in monthly_first.iterrows():
        entry_date = row["trade_date"]
        entry_price = row["close"]

        if i + 1 < len(monthly_first):
            next_entry = monthly_first.iloc[i + 1]["trade_date"]
            window = df[(df["trade_date"] >= entry_date) & (df["trade_date"] < next_entry)]
        else:
            window = df[df["trade_date"] >= entry_date]

        peak = entry_price
        trailing_active = False
        exit_price = window.iloc[-1]["close"] if not window.empty else entry_price

        for _, day in window.iterrows():
            current = day["close"]
            peak = max(peak, current)

            if (peak - entry_price) / entry_price >= trail_pct:
                trailing_active = True

            if trailing_active and (peak - current) / peak >= trail_pct:
                exit_price = current
                break

        ret = (exit_price - entry_price) / entry_price
        trades.append(ret)

    return _calc_strategy_metrics(f"移动止盈{int(trail_pct*100)}%", trades)


def backtest_batch_take_profit(
    df: pd.DataFrame, levels: list[float] | None = None
) -> dict:
    """分批止盈策略回测.

    每月第一个交易日买入，按不同盈利档位分批卖出（各卖 1/N）。

    Args:
        df: 日线数据 DataFrame
        levels: 分批止盈档位列表，默认 [0.2, 0.35, 0.5]

    Returns:
        策略回测结果字典
    """
    if levels is None:
        levels = [0.20, 0.35, 0.50]

    df = df.copy()
    df["year_month"] = df["trade_date"].dt.to_period("M")
    monthly_first = df.groupby("year_month").first().reset_index()
    portion = 1.0 / len(levels)

    trades = []
    for i, row in monthly_first.iterrows():
        entry_date = row["trade_date"]
        entry_price = row["close"]

        if i + 1 < len(monthly_first):
            next_entry = monthly_first.iloc[i + 1]["trade_date"]
            window = df[(df["trade_date"] >= entry_date) & (df["trade_date"] < next_entry)]
        else:
            window = df[df["trade_date"] >= entry_date]

        sold_levels = set()
        weighted_return = 0.0
        remaining = 1.0

        for _, day in window.iterrows():
            current_return = (day["close"] - entry_price) / entry_price
            for level in levels:
                if level not in sold_levels and current_return >= level:
                    weighted_return += portion * level
                    remaining -= portion
                    sold_levels.add(level)

        final_return = (window.iloc[-1]["close"] - entry_price) / entry_price if not window.empty else 0
        weighted_return += remaining * final_return
        trades.append(weighted_return)

    return _calc_strategy_metrics("分批止盈", trades)


def _calc_strategy_metrics(name: str, trades: list[float]) -> dict:
    """根据交易收益序列计算策略指标.

    Args:
        name: 策略名称
        trades: 每笔交易的收益率列表

    Returns:
        包含策略名称、年化收益率、最大回撤、夏普比率、胜率的字典
    """
    if not trades:
        return {"strategy": name, "annual_return": 0, "max_drawdown": 0, "sharpe_ratio": 0, "win_rate": 0}

    trades_arr = np.array(trades)
    avg_monthly = trades_arr.mean()
    annual_return = (1 + avg_monthly) ** 12 - 1

    cumulative = np.cumprod(1 + trades_arr)
    cummax = np.maximum.accumulate(cumulative)
    drawdowns = (cumulative - cummax) / cummax
    max_drawdown = drawdowns.min()

    sharpe = (trades_arr.mean() / trades_arr.std()) * np.sqrt(12) if trades_arr.std() > 0 else 0
    win_rate = np.sum(trades_arr > 0) / len(trades_arr)

    return {
        "strategy": name,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
        "win_rate": win_rate,
    }


def run_analysis(ts_code: str, name: str) -> None:
    """对单只股票运行完整的止盈策略分析.

    Args:
        ts_code: Tushare 股票代码
        name: 股票中文名称
    """
    logger.info(f"正在分析: {name}({ts_code})")
    df = fetch_daily_data(ts_code, BACKTEST_START, BACKTEST_END)
    if df.empty:
        logger.warning(f"跳过 {name}，无数据")
        return

    print(f"\n{'='*50}")
    print(f" {name}({ts_code}) 止盈策略分析")
    print(f"{'='*50}")

    # 过山车率
    rc = calc_rollercoaster_rate(df, profit_threshold=0.3, drawdown_threshold=0.5)
    print(f"\n--- 过山车率分析（浮盈30%后利润回撤50%）---")
    print(f"  分析区间: {BACKTEST_START[:4]}-{BACKTEST_START[4:6]}-{BACKTEST_START[6:]} ~ "
          f"{BACKTEST_END[:4]}-{BACKTEST_END[4:6]}-{BACKTEST_END[6:]}")
    print(f"  入场次数: {rc['entries']}")
    print(f"  达标入场: {rc['qualified_entries']}")
    print(f"  过山车次数: {rc['rollercoasters']}")
    print(f"  过山车率: {rc['rate']:.1%}")

    # 策略回测
    results = [
        backtest_buy_and_hold(df),
        backtest_fixed_take_profit(df, target_pct=0.20),
        backtest_trailing_stop(df, trail_pct=0.15),
        backtest_batch_take_profit(df),
    ]

    print(f"\n--- 策略回测对比 ---")
    print(f"{'策略':<14} {'年化收益':>8} {'最大回撤':>8} {'夏普比率':>8} {'胜率':>6}")
    print("-" * 50)
    for r in results:
        wr = f"{r['win_rate']:.1%}" if r["win_rate"] is not None else "N/A"
        print(
            f"{r['strategy']:<12} {r['annual_return']:>8.1%} "
            f"{r['max_drawdown']:>8.1%} {r['sharpe_ratio']:>8.2f} {wr:>6}"
        )


def main():
    """主入口：遍历股票池执行止盈分析."""
    logger.info("A股止盈策略分析启动")
    for ts_code, name in STOCK_POOL.items():
        run_analysis(ts_code, name)
    logger.info("分析完成")


if __name__ == "__main__":
    main()
