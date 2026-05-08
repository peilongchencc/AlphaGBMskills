---
name: alphagbm-iv-rank
description: >
  IV Rank 和 IV 百分位分析，显示当前隐含波动率相对252日历史的位置。
  返回 IV Rank（0-100）、IV 百分位（0-100）、IV 历史数据以及基于 IV 区间的交易信号。
  适用场景：决定是买还是卖权利金、判断 IV 高低、把握波动率交易时机、筛选 IV 极端值。
  触发关键词："AAPL IV Rank"、"NVDA IV 高吗"、"SPY IV 百分位"、"TSLA 历史 IV"、
  "META 期权是否便宜"、"IV Rank 扫描"、"适合卖权利金吗"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM IV Rank

## 前置条件

- **API Key**：设置环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx...`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。

## 功能说明

计算任意股票的 **IV Rank** 和 **IV 百分位**，将当前隐含波动率置于历史背景中。
回答核心问题：*"当前 IV 是高还是低，我该怎么做？"*

### 核心指标

| 指标 | 计算公式 | 含义 |
|------|----------|------|
| **IV Rank** | (当前IV - 52周低点) / (52周高点 - 52周低点) × 100 | IV 在年度区间的位置。0 = 最低点，100 = 最高点 |
| **IV 百分位** | 过去一年中 IV 低于今天的天数比例 | 过去多少比例的时间 IV 比现在便宜。80 = 80% 的时间 IV 更低 |
| **当前 IV** | 30日平值隐含波动率 | 市场当前对年化波动幅度的预期 |
| **52周高点** | 过去252个交易日的最高30日IV | IV 峰值，通常发生在大跌或重要事件期间 |
| **52周低点** | 过去252个交易日的最低30日IV | IV 谷底，通常出现在平静、缓涨的市场中 |
| **HV/IV 比率** | 历史波动率 / 隐含波动率 | >1 意味着实际波动超过隐含（IV 可能便宜）|

### IV 区间与交易信号

| IV Rank | 区间 | 含义 | 建议操作 |
|---------|------|------|----------|
| **80-100** | 极高 | IV 接近年度峰值，期权很贵 | 卖权利金：Short Strangle / Iron Condor / 信用价差 |
| **60-80** | 偏高 | IV 偏高，期权价格高于平均 | 偏向卖方，选择性操作；Covered Call 机会 |
| **40-60** | 中等 | IV 居中，不贵也不便宜 | 策略中性，根据方向观点决定 |
| **20-40** | 偏低 | IV 偏低，期权便宜 | 偏向买方；Debit Spread / Long Straddle |
| **0-20** | 极低 | IV 接近年度谷底，期权非常便宜 | 买权利金：Long Straddle / Debit Spread / 日历价差（卖远月）|

## API 端点

### IV 快照（即时，无额度消耗）

```
GET /api/options/snapshot/<SYMBOL>
```

返回：平值IV、IV Rank、30日历史波动率、VRP、VRP 等级。此端点免费，不计入分析额度。

### 波动率风险溢价（VRP）

```
VRP = 隐含波动率 - 历史波动率
```

VRP 衡量市场"预期"（IV）与实际"发生"（HV）之间的差距，是判断买卖权利金的关键信号。

| VRP 等级 | 数值 | 卖方 | 买方 |
|----------|------|------|------|
| very_high（极高）| ≥15% | 非常有利 | 不利 |
| high（偏高）| 5-15% | 有利 | 略不利 |
| normal（正常）| ±5% | 中性 | 中性 |
| low（偏低）| -15% 到 -5% | 不利 | 有利 |
| very_low（极低）| <-15% | 非常不利 | 非常有利 |

## 使用方法

### 输入
- **必填**：股票代码
- **可选**：回溯周期（默认252天）、IV 度量（30日平值、60日或自定义）

### 输出结构

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "iv_current": 28.5,
  "iv_rank": 42,
  "iv_percentile": 55,
  "iv_52w_high": 48.2,
  "iv_52w_low": 18.8,
  "iv_52w_mean": 30.1,
  "hv_30d": 25.2,
  "hv_iv_ratio": 0.88,
  "zone": "moderate",
  "signal": "没有强 IV 优势。根据方向性判断选择策略。",
  "iv_history": {
    "dates": ["2025-04-01", "2025-04-02", "..."],
    "iv_values": [32.1, 31.8, "..."],
    "hv_values": [28.5, 28.3, "..."]
  },
  "notable_events": [
    {"date": "2026-01-28", "iv": 48.2, "event": "财报飙升"},
    {"date": "2025-08-05", "iv": 44.1, "event": "市场大跌"}
  ]
}
```

### 示例问法

| 用户提问 | 处理结果 |
|----------|----------|
| "AAPL IV Rank" | IV Rank、百分位、区间分类和交易信号 |
| "NVDA IV 高吗？" | IV Rank + 区间分类 + 与52周区间对比 |
| "SPY IV 百分位" | 百分位及历史背景 |
| "TSLA 历史 IV" | 252日完整IV历史（含历史波动率叠加）|
| "META 期权是否便宜？" | IV Rank + HV/IV 比率 + 买/卖建议 |
| "QQQ 适合卖权利金吗？" | 基于 IV Rank 的回答及建议策略 |

### 模拟数据

无 API Key 时可用演示股票：AAPL、NVDA、SPY、TSLA、META。IV 历史数据使用 `mock-data/` 中的真实252天数据。

### 相关 Skills
- **alphagbm-vol-surface** — 跨行权价和到期日的完整3D IV 图
- **alphagbm-vol-smile** — 特定到期日的 IV 偏斜
- **alphagbm-options-strategy** — IV 区间决定是买还是卖权利金
- **alphagbm-options-score** — IV 吸引力是评分的关键因子

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
