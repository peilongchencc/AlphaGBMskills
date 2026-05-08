---
name: alphagbm-fear-score
description: |
  单股恐慌指数（0-100），对六个真实信号加权：VIX、IV Rank、RSI-14、
  期权成交量异常、Put/Call 比率和连续下跌天数。评分 ≥ 60 触发牛市价差（BPS）入场信号。
  基于 FearDesk 方法论，在信号触发入场的 BPS 交易中年化 ROC 约 10.8%，
  无信号约 3.5%，约 3 倍 Alpha 提升。
  触发关键词："QQQ 恐慌指数"、"NVDA 超卖了吗"、"SPY 恐慌指数"、"TSLA BPS 信号"、
  "现在是恐慌时刻吗"、"BPS 入场时机"、"什么时候卖 Put"、"AAPL 恐慌了吗"、
  "逆向入场信号"、"超卖读数"、"VIX 加 RSI"。
globs:
  - "mock-data/fear-score/**"
---

# AlphaGBM 恐慌评分（FearScore）

单股加权综合恐慌指标。一次 API 调用重现 FearDesk 框架：六个独立恐慌信号，
各自评分0-100，再按固定权重合并为一个数字。**评分 ≥ 60 是牛市价差（BPS）历史入场触发线。**

## 评分权重

| 指标 | 权重 | 来源 |
|------|------|------|
| VIX 水平 | 20% | 全市场恐慌底线 |
| **IV Rank**（最重要）| 25% | 单股期权权利金贵/贱程度 |
| RSI-14 | 15% | 超卖强度 |
| 成交量异常 | 15% | 期权或正股成交量相对5日均值的放大倍数 |
| Put/Call 比率 | 15% | 看跌仓位倾斜程度 |
| 连续下跌天数 | 10% | 抛售持续性 |

每个指标都有自己的0-100子评分，极端读数贡献最多。
缺失输入回退到中性值（在 `components.*.fallback` 中标记），端点不会因数据缺失而报错。

## 为什么需要这个指标

大多数恐慌指标要么只看 VIX（忽略单股差异），要么不透明（"情绪指数：72"）。
这个指标精确拆解了评分的驱动因素，让你决定是否信任它。

**回测证据：** 在146笔实盘牛市价差交易中，FearScore ≥ 60 入场年化 ROC 约 10.8%，
无条件入场约 3.5% — 单一过滤器带来约 **3 倍 Alpha**。
可将此作为任何卖权利金策略的市场择时层。

## 使用方法

**输入：** 股票代码。

**输出：**
- `fear_score` — 加权总分 0-100
- `signal` — 布尔值，当 `fear_score ≥ threshold`（默认60）时为 true
- `threshold` — 当前触发阈值
- `confidence` — 0-1，使用真实（非回退）数据的指标比例
- `components.{vix,iv_rank,rsi,volume_anomaly,pc_ratio,consecutive_down}`：
  - `value` — 原始输入值
  - `score` — 单指标0-100评分
  - `weight` — 贡献权重
  - `fallback` — 是否使用中性默认值

**示例问法：**
- `QQQ 恐慌指数` — QQQ 六个指标的完整分析
- `NVDA 现在超卖了吗` — RSI + FearScore 综合
- `SPY BPS 信号` — 检查是否触发入场阈值
- `什么时候卖 AAPL Put` — 通过 FearScore ≥ 60 规则择时
- `TSLA 今天有多恐慌` — 带组成分析的单股恐慌指数
- `为什么 QQQ 恐慌指数低` — 逐指标解释

## 模拟数据

模拟数据在 `mock-data/fear-score/` — 包含中性 / 偏高 / 信号触发三种示例响应。

## API 端点

```
GET /api/options/fear-score?ticker={SYMBOL}
```

查询参数：
- `ticker`（必填）— 股票代码（支持美股 / 港股 / A 股白名单标的）

响应示例：

```json
{
  "success": true,
  "ticker": "QQQ",
  "fear_score": 68.2,
  "signal": true,
  "threshold": 60,
  "confidence": 1.0,
  "components": {
    "vix": {"value": 28.4, "score": 82, "weight": 0.20, "fallback": false},
    "iv_rank": {"value": 78, "score": 78, "weight": 0.25, "fallback": false},
    "rsi": {"value": 24.1, "score": 88, "weight": 0.15, "fallback": false},
    "volume_anomaly": {"value": 2.3, "score": 72, "weight": 0.15, "fallback": false},
    "pc_ratio": {"value": 1.6, "score": 80, "weight": 0.15, "fallback": false},
    "consecutive_down": {"value": 3, "score": 60, "weight": 0.10, "fallback": false}
  },
  "timestamp": "2026-04-24T08:00:00"
}
```

定价：1次期权分析额度；单股5分钟缓存（缓存命中免费）。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-vix-status](../alphagbm-vix-status/) | 市场整体 VIX 输入 |
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | IV Rank（综合评分的25%）单独查询 |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 应参考 ≥60 信号的 BPS/卖 Put 策略 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
