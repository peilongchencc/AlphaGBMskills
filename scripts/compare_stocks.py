"""A股多股横向对比 - 多维度量化对比与排名.

功能:
    1. 趋势对比：近20日/60日涨跌幅/MA20偏离度
    2. 技术指标对比：RSI/MACD/KDJ 状态
    3. 波动率与夏普比率对比
    4. 量能对比
    5. 综合排名输出

注意: 基本面数据（PE/PB/ROE）需要 Tushare 更高积分权限，
      当前版本聚焦于行情与技术面对比。
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.config import pro, STOCK_POOL, rate_limited_call
from scripts.stock_analysis import calc_rsi, calc_macd, calc_kdj


def fetch_compare_data(ts_code: str) -> dict:
    """获取单只股票的对比所需数据.

    Args:
        ts_code: Tushare 股票代码

    Returns:
        包含各维度指标的字典
    """
    result = {"ts_code": ts_code, "name": STOCK_POOL.get(ts_code, ts_code)}

    daily = rate_limited_call(pro.daily, ts_code=ts_code)
    if daily is None or daily.empty:
        return result

    daily["trade_date"] = pd.to_datetime(daily["trade_date"])
    daily = daily.sort_values("trade_date").reset_index(drop=True)
    prices = daily["close"]

    result["latest_price"] = prices.iloc[-1]

    # 技术指标
    if len(prices) >= 26:
        result["rsi_12"] = calc_rsi(prices, 12)
        macd = calc_macd(prices)
        result["macd_dif"] = macd["dif"]
        result["macd_signal"] = macd["signal"]

    if len(daily) >= 9:
        kdj = calc_kdj(daily["high"], daily["low"], prices)
        result["kdj_j"] = kdj["j"]

    # 涨跌幅
    if len(prices) >= 20:
        result["return_20d"] = (prices.iloc[-1] - prices.iloc[-20]) / prices.iloc[-20]
    if len(prices) >= 60:
        result["return_60d"] = (prices.iloc[-1] - prices.iloc[-60]) / prices.iloc[-60]

    # MA20 偏离度
    if len(prices) >= 20:
        ma20 = prices.rolling(20).mean().iloc[-1]
        result["ma20_deviation"] = (prices.iloc[-1] - ma20) / ma20

    # 年化波动率
    daily_returns = prices.pct_change().dropna()
    if len(daily_returns) >= 60:
        result["volatility"] = daily_returns.tail(250).std() * np.sqrt(252)

    # 夏普比率（无风险利率按2%算）
    if len(daily_returns) >= 250:
        annual_return = prices.iloc[-1] / prices.iloc[-250] - 1
        vol = daily_returns.tail(250).std() * np.sqrt(252)
        result["sharpe"] = (annual_return - 0.02) / vol if vol > 0 else 0

    # 量比
    if len(daily) >= 20:
        vol_5 = daily["vol"].tail(5).mean()
        vol_20 = daily["vol"].tail(20).mean()
        result["vol_ratio"] = vol_5 / vol_20 if vol_20 > 0 else 1.0

    return result


def rank_metric(data_list: list[dict], key: str, ascending: bool = True) -> list[int]:
    """对某个指标进行排名.

    Args:
        data_list: 股票数据列表
        key: 排名指标名
        ascending: True 表示越小越好

    Returns:
        排名列表（1为最优）
    """
    values = [(i, d.get(key)) for i, d in enumerate(data_list)]
    valid = [(i, v) for i, v in values if v is not None]

    if not valid:
        return [len(data_list)] * len(data_list)

    valid.sort(key=lambda x: x[1], reverse=not ascending)
    ranks = [len(data_list)] * len(data_list)
    for rank, (idx, _) in enumerate(valid, 1):
        ranks[idx] = rank

    return ranks


def rank_rsi_health(data_list: list[dict]) -> list[int]:
    """RSI 健康度排名（越接近50越健康）.

    Args:
        data_list: 股票数据列表

    Returns:
        排名列表
    """
    deviations = []
    for d in data_list:
        rsi = d.get("rsi_12")
        deviations.append(abs(rsi - 50) if rsi is not None else 50)

    indexed = sorted(enumerate(deviations), key=lambda x: x[1])
    ranks = [0] * len(data_list)
    for rank, (idx, _) in enumerate(indexed, 1):
        ranks[idx] = rank
    return ranks


def print_comparison(data_list: list[dict]) -> None:
    """打印对比结果.

    Args:
        data_list: 各股票数据列表
    """
    names = [d["name"] for d in data_list]
    max_name_len = max(len(n) for n in names)

    print(f"\n{'='*60}")
    print(f" A股多股横向对比")
    print(f" 对比标的: {' vs '.join(names)}")
    print(f"{'='*60}")

    # 趋势对比
    print(f"\n--- 趋势对比 ---")
    print(f"{'股票':<{max_name_len+2}} {'20日涨跌':>10} {'60日涨跌':>10} {'MA20偏离':>10}")
    print("-" * (max_name_len + 36))
    for d in data_list:
        r20 = f"{d['return_20d']:.1%}" if d.get("return_20d") is not None else "N/A"
        r60 = f"{d['return_60d']:.1%}" if d.get("return_60d") is not None else "N/A"
        ma = f"{d['ma20_deviation']:.1%}" if d.get("ma20_deviation") is not None else "N/A"
        print(f"{d['name']:<{max_name_len+2}} {r20:>10} {r60:>10} {ma:>10}")

    # 技术指标对比
    print(f"\n--- 技术指标对比 ---")
    print(f"{'股票':<{max_name_len+2}} {'RSI(12)':>8} {'KDJ-J':>8} {'MACD状态':>10}")
    print("-" * (max_name_len + 32))
    for d in data_list:
        rsi = f"{d['rsi_12']:.1f}" if d.get("rsi_12") is not None else "N/A"
        kdj = f"{d['kdj_j']:.1f}" if d.get("kdj_j") is not None else "N/A"
        macd_s = d.get("macd_signal", "N/A")
        print(f"{d['name']:<{max_name_len+2}} {rsi:>8} {kdj:>8} {macd_s:>10}")

    # 风险收益对比
    print(f"\n--- 风险收益对比 ---")
    print(f"{'股票':<{max_name_len+2}} {'年化波动率':>10} {'夏普比率':>8} {'量比(5/20)':>10}")
    print("-" * (max_name_len + 34))
    for d in data_list:
        vol = f"{d['volatility']:.1%}" if d.get("volatility") is not None else "N/A"
        sharpe = f"{d['sharpe']:.2f}" if d.get("sharpe") is not None else "N/A"
        vr = f"{d['vol_ratio']:.2f}" if d.get("vol_ratio") is not None else "N/A"
        print(f"{d['name']:<{max_name_len+2}} {vol:>10} {sharpe:>8} {vr:>10}")

    # 综合排名
    n = len(data_list)
    ret_ranks = rank_metric(data_list, "return_60d", ascending=False)
    vol_ranks = rank_metric(data_list, "volatility", ascending=True)
    sharpe_ranks = rank_metric(data_list, "sharpe", ascending=False)
    rsi_ranks = rank_rsi_health(data_list)

    weights = {"return": 0.30, "volatility": 0.20, "sharpe": 0.30, "rsi_health": 0.20}

    composite_scores = []
    for i in range(n):
        score = (
            (n - ret_ranks[i] + 1) * weights["return"]
            + (n - vol_ranks[i] + 1) * weights["volatility"]
            + (n - sharpe_ranks[i] + 1) * weights["sharpe"]
            + (n - rsi_ranks[i] + 1) * weights["rsi_health"]
        )
        composite_scores.append(score)

    max_possible = n * 1.0
    normalized = [s / max_possible * 10 for s in composite_scores]
    ranked_indices = sorted(range(n), key=lambda i: normalized[i], reverse=True)

    print(f"\n--- 综合排名 ---")
    print(f"{'排名':>4} {'股票':<{max_name_len+2}} {'综合得分':>8}")
    print("-" * (max_name_len + 18))
    for rank, idx in enumerate(ranked_indices, 1):
        print(f"{rank:>4} {data_list[idx]['name']:<{max_name_len+2}} {normalized[idx]:>8.1f}")

    print(f"\n{'─'*60}")
    best = data_list[ranked_indices[0]]
    print(f" 当前综合最优: {best['name']}（综合得分 {normalized[ranked_indices[0]]:.1f}/10）")
    print(f" 评分权重: 60日收益30% + 夏普比率30% + 波动率20% + RSI健康度20%")
    print(f"{'─'*60}")


def main():
    """主入口：获取数据并输出对比结果."""
    logger.info("A股多股横向对比启动")

    data_list = []
    for ts_code in STOCK_POOL:
        logger.info(f"获取数据: {STOCK_POOL[ts_code]}({ts_code})")
        data = fetch_compare_data(ts_code)
        data_list.append(data)

    if len(data_list) < 2:
        logger.error("有效数据不足2只股票，无法对比")
        return

    print_comparison(data_list)
    logger.info("对比分析完成")


if __name__ == "__main__":
    main()
