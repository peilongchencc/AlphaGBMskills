---
name: alphagbm-bps-backtest
description: |
  约8年日线数据的完整前进式牛市价差（Bull Put Spread）回测。在同一请求中同时运行
  「有信号版（FearScore ≥ 60 入场）」和「无信号对照组」，以便量化恐慌入场规则是否
  真正为该股票带来 Alpha。返回权益曲线、4个 KPI
  （年化收益 / 胜率 / 最大回撤 / 夏普比率）、交易明细和通俗解读。
  触发关键词："QQQ 回测 BPS"、"牛市价差回测"、"FearScore 在 SPY 有没有效"、
  "BPS 用什么 DTE"、"最优 BPS Delta"、"BPS 策略回测"、"信用价差回测"、
  "空头 Put 价差回测"。
globs:
  - "mock-data/bps-backtest/**"
---

# AlphaGBM BPS 回测

对任意股票，在2018年至今进行牛市价差（Short Put + 更低行权价 Long Put）的机械策略
回测，每次调用运行两遍：

1. **有信号版** — 仅在单股 FearScore ≥ 你设定的阈值时入场
2. **无信号版（对照组）** — 每周一无条件入场

并排对比展示信号是否真正起作用，还是花了1次额度换来噪音。

## 参数说明

除 `ticker` 外均为可选：

| 参数 | 默认值 | 范围 | 含义 |
|------|--------|------|------|
| `ticker` | 必填 | 美股/港股/A股 | 标的 |
| `dte_target` | 14 | 7–45 | 入场时的到期天数 |
| `short_delta` | 0.25 | 0.15–0.35 | Short Put 腿的绝对 Delta |
| `spread_width` | 5.0 | 2–10 | 价差宽度（美元）|
| `take_profit_pct` | 0.50 | 0.20–0.80 | 实现最大盈利的该比例时平仓 |
| `fear_threshold` | 60 | 40–80 | FearScore ≥ X 触发入场信号 |
| `start_date` | 2018-01-01 | YYYY-MM-DD | 回测开始日期 |
| `end_date` | 2026-04-20 | YYYY-MM-DD | 回测结束日期 |
| `include_control` | true | bool | 是否同时运行无信号对照组 |

## 返回内容

每遍（`with_signal` 和 `no_signal`）：
- `total_trades`、`win_rate_pct`、`annual_return_pct`、`sharpe`、`max_drawdown_pct`、
  `roc_pct`、`avg_holding_days`、`avg_pnl_per_trade`、`total_pnl`、`final_capital`
- `exit_reasons` — 按类型统计：`take_profit / stop_loss / expiry_otm / expiry_itm / close_early`
- `trades[]` — 完整交易明细（入/出场日期、行权价、权利金、盈亏、原因）
- `equity_curve[]` — 每日累计资金曲线
- `pnl_histogram` — 盈亏分布的分桶统计

还有：
- `summary` — 中英文一段式解读，对比有信号 vs 无信号，当回撤或胜率存在问题时附 ⚠️ 警告

## 方法论说明

- 用20日历史波动率（HV20）替代 BS 定价中的 IV。
  历史期权链 IV 大规模采购成本过高，HV20 是合理替代，但在事件期间会低估 IV。
  实盘通常优于回测正是因为这个原因。
- FearScore 由与实盘版相同的6个指标重建，但仅从廉价历史价格和成交量数据计算。
- 入场过滤：`max_positions`（3个）和 `min_entry_spacing_days`（3天）以及
  `risk_per_trade` 上限（资金的0.5%）。

## 使用方法

**示例问法：**
- `QQQ 回测 BPS` — 默认参数，有信号 vs 无信号对比
- `FearScore 在 SPY 有没有效` — 同一调用，读取对比摘要
- `IWM 牛市价差回测 DTE 21 Delta 0.30` — 自定义参数
- `QQQ 什么 DTE 最适合 BPS` — 用不同 DTE 跑几遍对比
- `NVDA 上 FearScore 阈值 70 vs 60 对比` — 用不同阈值跑两次

## 模拟数据

模拟数据在 `mock-data/bps-backtest/` — QQQ 的有信号和无信号示例。

## API 端点

```
POST /api/options/bps-backtest
Content-Type: application/json
```

请求体：

```json
{
  "ticker": "QQQ",
  "dte_target": 14,
  "short_delta": 0.25,
  "spread_width": 5.0,
  "take_profit_pct": 0.50,
  "fear_threshold": 60,
  "start_date": "2018-01-01",
  "end_date": "2026-04-20",
  "include_control": true
}
```

响应：

```json
{
  "success": true,
  "ticker": "QQQ",
  "period": {"start": "2018-01-01", "end": "2026-04-20"},
  "with_signal": {
    "total_trades": 28, "win_rate_pct": 100, "annual_return_pct": 10.8,
    "sharpe": 16.3, "max_drawdown_pct": 0.0, "trades": [...], "equity_curve": [...],
    "pnl_histogram": {...}, "exit_reasons": {"take_profit": 20, "expiry_otm": 8}
  },
  "no_signal": {
    "total_trades": 185, "win_rate_pct": 82, "annual_return_pct": 3.5,
    "sharpe": 2.1, "max_drawdown_pct": -8.2
  },
  "summary": {
    "zh": "QQQ · 2018-2026 · 使用 FearScore ≥ 60 触发 BPS 入场，共交易 28 笔，年化 +10.8%，胜率 100%，最大回撤 0.0%。同参数无信号对照组年化 +3.5%、胜率 82%；信号版本高出无信号组 7.3 个百分点。",
    "en": "QQQ · 2018-2026 · BPS entry on FearScore ≥ 60 over 28 trades: annualized +10.8%, win rate 100%, max drawdown 0.0%. No-signal control: annualized +3.5%, win rate 82%. Signal outperforms by 7.3 pp."
  }
}
```

定价：1次期权分析额度；每参数哈希30分钟缓存（缓存命中免费）。新哈希预计需要5-10秒计算。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-fear-score](../alphagbm-fear-score/) | 正在回测的入场信号实盘版 |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 确定参数后构建具体 BPS |
| [alphagbm-pnl-simulator](../alphagbm-pnl-simulator/) | 在不同未来价格下前向模拟特定 BPS |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
