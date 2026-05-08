"""A股量化分析 - 全局配置模块."""

import os
import time
from pathlib import Path

from dotenv import load_dotenv
import tushare as ts

# 加载环境变量
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")
if not TUSHARE_TOKEN:
    raise EnvironmentError("未找到 TUSHARE_TOKEN，请在 .env 文件中配置")

# 初始化 Tushare Pro API
ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

# 测试标的配置
STOCK_POOL = {
    "600519.SH": "贵州茅台",
    "300750.SZ": "宁德时代",
    "000001.SZ": "平安银行",
}

# 回测默认参数
BACKTEST_START = "20200101"
BACKTEST_END = "20250501"

# 技术指标参数
MA_PERIODS = [5, 10, 20, 60, 120, 250]
RSI_PERIOD = 14

# Tushare 频率限制：2次/秒，保守使用 0.6s 间隔
API_CALL_INTERVAL = 0.6

_last_call_time = 0.0


def rate_limited_call(func, **kwargs):
    """带频率限制的 Tushare API 调用封装.

    Args:
        func: Tushare pro_api 的方法（如 pro.daily）
        **kwargs: 传递给 API 的参数

    Returns:
        API 返回的 DataFrame
    """
    global _last_call_time
    elapsed = time.time() - _last_call_time
    if elapsed < API_CALL_INTERVAL:
        time.sleep(API_CALL_INTERVAL - elapsed)
    _last_call_time = time.time()
    return func(**kwargs)
