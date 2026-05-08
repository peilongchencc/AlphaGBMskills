"""A股单只股票综合分析 - 技术面+资金面+风险评分.

功能:
    1. 技术面评估：均线系统/RSI/MACD/KDJ/布林带（基于日线自行计算）
    2. 资金面评估：量价关系/量比
    3. 趋势评估：多周期涨跌幅/波动率
    4. 综合风险评分（0-10）和投资建议

注意: 基本面数据（PE/PB/ROE）需要 Tushare 更高积分权限，
      当前版本聚焦于技术面分析。
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.config import pro, STOCK_POOL, MA_PERIODS, rate_limited_call


def fetch_daily_data(ts_code: str) -> pd.DataFrame:
    """获取日线行情数据.

    Args:
        ts_code: Tushare 股票代码

    Returns:
        按日期升序排列的 DataFrame
    """
    df = rate_limited_call(pro.daily, ts_code=ts_code)
    if df is None or df.empty:
        return pd.DataFrame()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df = df.sort_values("trade_date").reset_index(drop=True)
    return df


def calc_rsi(prices: pd.Series, period: int = 12) -> float:
    """计算 RSI 指标.

    Args:
        prices: 收盘价序列
        period: RSI 周期

    Returns:
        最新 RSI 值
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50.0


def calc_macd(prices: pd.Series) -> dict:
    """计算 MACD 指标.

    Args:
        prices: 收盘价序列

    Returns:
        包含 dif, dea, signal 的字典
    """
    ema12 = prices.ewm(span=12).mean()
    ema26 = prices.ewm(span=26).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9).mean()

    signal = "中性"
    if len(dif) >= 2:
        if dif.iloc[-1] > dea.iloc[-1] and dif.iloc[-2] <= dea.iloc[-2]:
            signal = "金叉"
        elif dif.iloc[-1] < dea.iloc[-1] and dif.iloc[-2] >= dea.iloc[-2]:
            signal = "死叉"
        elif dif.iloc[-1] > dea.iloc[-1]:
            signal = "多头"
        else:
            signal = "空头"

    return {"dif": dif.iloc[-1], "dea": dea.iloc[-1], "signal": signal}


def calc_kdj(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 9) -> dict:
    """计算 KDJ 指标.

    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        n: 计算周期

    Returns:
        包含 k, d, j 的字典
    """
    lowest = low.rolling(n).min()
    highest = high.rolling(n).max()
    rsv = (close - lowest) / (highest - lowest) * 100
    rsv = rsv.fillna(50)

    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d

    return {"k": k.iloc[-1], "d": d.iloc[-1], "j": j.iloc[-1]}


def calc_bollinger(prices: pd.Series, period: int = 20) -> dict:
    """计算布林带.

    Args:
        prices: 收盘价序列
        period: 计算周期

    Returns:
        包含 upper, middle, lower, position 的字典
    """
    middle = prices.rolling(period).mean().iloc[-1]
    std = prices.rolling(period).std().iloc[-1]
    upper = middle + 2 * std
    lower = middle - 2 * std
    current = prices.iloc[-1]

    if current > upper:
        position = "上轨之上"
    elif current < lower:
        position = "下轨之下"
    elif current > middle:
        position = "中轨之上"
    else:
        position = "中轨之下"

    return {"upper": upper, "middle": middle, "lower": lower, "position": position}


def score_technical(df: pd.DataFrame) -> tuple[float, list[str]]:
    """技术指标评分.

    Args:
        df: 日线数据 DataFrame

    Returns:
        (分数, 评分细节列表) 的元组
    """
    score = 0.0
    details = []
    prices = df["close"]

    # RSI(12)
    rsi = calc_rsi(prices, 12)
    if rsi > 80:
        score += 1.5
        details.append(f"RSI(12)={rsi:.1f} > 80，严重超买 +1.5")
    elif rsi > 70:
        score += 1
        details.append(f"RSI(12)={rsi:.1f} > 70，超买 +1")
    elif rsi < 20:
        score += 1.5
        details.append(f"RSI(12)={rsi:.1f} < 20，严重超卖 +1.5")
    elif rsi < 30:
        score += 1
        details.append(f"RSI(12)={rsi:.1f} < 30，超卖 +1")
    else:
        details.append(f"RSI(12)={rsi:.1f}，正常区间")

    # MACD
    macd = calc_macd(prices)
    if macd["signal"] == "死叉":
        score += 1
        details.append(f"MACD 死叉（DIF={macd['dif']:.3f}）+1")
    elif macd["signal"] == "金叉":
        details.append(f"MACD 金叉（DIF={macd['dif']:.3f}）")
    else:
        details.append(f"MACD {macd['signal']}运行（DIF={macd['dif']:.3f}）")

    # KDJ
    if len(df) >= 9:
        kdj = calc_kdj(df["high"], df["low"], prices)
        if kdj["j"] > 100:
            score += 1
            details.append(f"KDJ-J={kdj['j']:.1f} > 100，超买区 +1")
        elif kdj["j"] < 0:
            score += 1
            details.append(f"KDJ-J={kdj['j']:.1f} < 0，超卖区 +1")
        else:
            details.append(f"KDJ-J={kdj['j']:.1f}，正常")

    # 布林带
    if len(prices) >= 20:
        boll = calc_bollinger(prices)
        if boll["position"] == "上轨之上":
            score += 1
            details.append(f"股价 > 布林上轨({boll['upper']:.2f})，超强/超买 +1")
        elif boll["position"] == "下轨之下":
            score += 0.5
            details.append(f"股价 < 布林下轨({boll['lower']:.2f})，超跌 +0.5")
        else:
            details.append(f"布林带{boll['position']}，正常")

    return score, details


def score_trend(df: pd.DataFrame) -> tuple[float, list[str]]:
    """趋势与均线系统评分.

    Args:
        df: 日线数据 DataFrame

    Returns:
        (分数, 评分细节列表) 的元组
    """
    score = 0.0
    details = []
    prices = df["close"]
    current = prices.iloc[-1]

    ma_values = {}
    for period in MA_PERIODS:
        if len(prices) >= period:
            ma_values[f"MA{period}"] = prices.rolling(period).mean().iloc[-1]

    # 股价 vs MA250（年线）
    if "MA250" in ma_values:
        ma250 = ma_values["MA250"]
        if current < ma250:
            score += 1.5
            details.append(f"股价({current:.2f}) < 年线MA250({ma250:.2f})，长期趋势偏空 +1.5")
        else:
            pct_above = (current - ma250) / ma250
            details.append(f"股价在年线之上 {pct_above:.1%}，长期趋势向上")

    # 均线多空排列
    if len(ma_values) >= 4:
        ma_list = [(k, v) for k, v in sorted(ma_values.items(), key=lambda x: int(x[0][2:]))]
        short_above_long = all(ma_list[i][1] >= ma_list[i+1][1] for i in range(len(ma_list)-1))
        short_below_long = all(ma_list[i][1] <= ma_list[i+1][1] for i in range(len(ma_list)-1))
        if short_above_long:
            details.append("均线多头排列，趋势健康")
        elif short_below_long:
            score += 1
            details.append("均线空头排列 +1")
        else:
            details.append("均线交织，趋势不明")

    # 近期涨跌幅
    if len(prices) >= 60:
        ret_20d = (current - prices.iloc[-20]) / prices.iloc[-20]
        ret_60d = (current - prices.iloc[-60]) / prices.iloc[-60]
        details.append(f"近20日涨跌: {ret_20d:.1%}，近60日涨跌: {ret_60d:.1%}")

        if ret_20d > 0.3:
            score += 1
            details.append("20日涨幅 > 30%，短期过热 +1")
        elif ret_20d < -0.2:
            score += 0.5
            details.append("20日跌幅 > 20%，急跌 +0.5")

    return score, details


def score_volume(df: pd.DataFrame) -> tuple[float, list[str]]:
    """量能与资金面评分.

    Args:
        df: 日线数据 DataFrame

    Returns:
        (分数, 评分细节列表) 的元组
    """
    score = 0.0
    details = []

    if len(df) < 20:
        details.append("数据不足，跳过量能分析")
        return score, details

    recent_5 = df.tail(5)
    recent_20 = df.tail(20)
    vol_5_avg = recent_5["vol"].mean()
    vol_20_avg = recent_20["vol"].mean()

    vol_ratio = vol_5_avg / vol_20_avg if vol_20_avg > 0 else 1.0
    details.append(f"5日均量/20日均量 = {vol_ratio:.2f}")

    price_up = recent_5["close"].iloc[-1] > recent_5["close"].iloc[0]
    vol_shrink = vol_5_avg < vol_20_avg * 0.7

    if price_up and vol_shrink:
        score += 1
        details.append("价升量缩，量价背离 +1")
    elif not price_up and vol_ratio > 1.5:
        score += 1
        details.append("价跌放量，恐慌抛售 +1")
    else:
        details.append("量价配合正常")

    if vol_ratio > 3:
        score += 1
        details.append(f"近5日量能是20日均量的 {vol_ratio:.1f} 倍，异常放量 +1")

    return score, details


def get_risk_level(score: float) -> str:
    """根据评分返回风险等级和建议.

    Args:
        score: 综合风险评分

    Returns:
        风险等级描述字符串
    """
    if score <= 2:
        return "低风险 - 技术面健康，可考虑建仓"
    elif score <= 4:
        return "中低风险 - 整体偏强，正常持有"
    elif score <= 6:
        return "中等风险 - 存在隐忧，谨慎操作"
    elif score <= 8:
        return "高风险 - 多项指标预警，建议减仓观望"
    else:
        return "极高风险 - 技术面全面恶化，建议远离"


def analyze_stock(ts_code: str, name: str) -> None:
    """对单只股票执行综合分析.

    Args:
        ts_code: Tushare 股票代码
        name: 股票中文名称
    """
    logger.info(f"正在分析: {name}({ts_code})")
    df = fetch_daily_data(ts_code)

    if df.empty:
        logger.warning(f"跳过 {name}，无数据")
        return

    current_price = df["close"].iloc[-1]
    latest_date = df["trade_date"].iloc[-1].strftime("%Y-%m-%d")

    print(f"\n{'='*55}")
    print(f" {name}({ts_code}) 综合分析报告")
    print(f"{'='*55}")
    print(f" 最新收盘价: {current_price:.2f}  |  数据日期: {latest_date}")

    total_score = 0.0

    # 技术面
    tech_score, tech_details = score_technical(df)
    total_score += tech_score
    print(f"\n--- 技术指标评估（得分: {tech_score:.1f}）---")
    for d in tech_details:
        print(f"  * {d}")

    # 趋势
    trend_score, trend_details = score_trend(df)
    total_score += trend_score
    print(f"\n--- 趋势与均线评估（得分: {trend_score:.1f}）---")
    for d in trend_details:
        print(f"  * {d}")

    # 量能
    vol_score, vol_details = score_volume(df)
    total_score += vol_score
    print(f"\n--- 量能评估（得分: {vol_score:.1f}）---")
    for d in vol_details:
        print(f"  * {d}")

    # 综合
    total_score = max(0, min(10, total_score))
    risk_level = get_risk_level(total_score)

    print(f"\n{'─'*55}")
    print(f" 综合风险评分: {total_score:.1f} / 10")
    print(f" 风险等级: {risk_level}")
    print(f"{'─'*55}")
    print(f" (注: 基本面数据需 Tushare 更高积分，当前以技术面为主)")


def main():
    """主入口：遍历股票池执行分析."""
    logger.info("A股综合分析启动")
    for ts_code, name in STOCK_POOL.items():
        analyze_stock(ts_code, name)
    logger.info("分析完成")


if __name__ == "__main__":
    main()
