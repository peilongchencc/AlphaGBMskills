---
name: alphagbm-vol-smile
description: >
  单个到期日的2D波动率微笑和偏斜分析，将IV映射到各行权价，揭示Put偏斜、Call偏斜
  和微笑形态。返回微笑曲线数据、偏斜指标（25-Delta偏斜、风险逆转）和形态分类。
  适用场景：分析Put/Call偏斜、判断Put是否偏贵、理解期权定价中的方向性恐慌、
  寻找偏斜交易机会。
  触发关键词："AAPL 波动率微笑"、"NVDA 偏斜分析"、"TSLA Put 偏斜"、
  "SPY 微笑陡吗"、"META 波动率偏斜"、"GOOGL 微笑形态"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM 波动率微笑

## 前置条件

- **API Key**：设置环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx...`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。

## 功能说明

分析单个到期日的**波动率微笑**（或偏斜）— 以行权价为横轴绘制的隐含波动率曲线。
揭示市场如何对尾部风险、方向性恐慌和期权链上的供需失衡进行定价。

### 核心输出

| 输出 | 说明 |
|------|------|
| **微笑曲线** | 所选到期日每个行权价对应的 IV，原始微笑数据 |
| **25-Delta 偏斜** | IV(25d Put) - IV(25d Call)，方向偏斜的标准度量 |
| **风险逆转（Risk Reversal）** | 25d Call 减 25d Put 的价格差，可直接交易的偏斜表达 |
| **微笑形态** | 分类：正常 / 平坦 / 反向 / 双翼 / 斜歪（Smirk）|
| **偏斜百分位** | 当前偏斜在252日历史中的位置，偏斜异常陡峭还是平坦？|

### 微笑形态与交易含义

| 形态 | 说明 | 市场含义 | 交易思路 |
|------|------|----------|----------|
| **正常（Normal）** | OTM Put IV > OTM Call IV | 标准对冲需求，Put 偏贵 | 卖 Put 价差，买 Call 价差 |
| **平坦（Flat）** | 各行权价 IV 大致相同 | 恐慌低，仓位均衡 | 中性策略（铁鹰）|
| **反向（Reverse）** | OTM Call IV > OTM Put IV | 上行投机或轧空风险 | 若 Call 定价过高则卖 Call 价差 |
| **双翼（Winged）** | OTM Put 和 Call 均偏高 | 预期大幅波动，方向不明 | 若 IV 偏高则卖跨式/宽跨式 |
| **斜歪（Smirk）** | 一侧明显更陡 | 方向性恐慌集中在一侧 | 若偏斜极端则交易陡峭一侧 |

## API 端点

### 波动率微笑

```
GET /api/options/tools/vol-smile/<SYMBOL>?expiry=2026-04-17
```

查询参数：
- **expiry**（可选）：到期日，格式 `YYYY-MM-DD`。省略时默认取最近月度到期日。

返回指定到期日的微笑曲线（行权价、IV、Delta）、偏斜指标、形态分类和偏斜百分位。

## 使用方法

### 输入
- **必填**：股票代码
- **可选**：到期日（默认最近月度）、虚实程度范围

### 输出结构

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "expiry": "2026-04-18",
  "dte": 20,
  "smile": {
    "strikes": [190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240],
    "ivs":    [42.1, 39.5, 36.8, 34.0, 31.5, 29.2, 27.5, 28.8, 30.5, 32.8, 35.2],
    "deltas": [-0.10, -0.15, -0.22, -0.30, -0.40, -0.48, 0.52, 0.42, 0.32, 0.22, 0.14]
  },
  "skew_metrics": {
    "skew_25d": -8.3,
    "risk_reversal_25d": -2.45,
    "skew_10d": -14.6,
    "atm_iv": 28.3
  },
  "shape": "normal",
  "skew_percentile": 72,
  "interpretation": "Put 偏斜处于中等偏陡水平（72百分位）。OTM Put 比等距 Call 高约8个波动点，属于标准对冲需求略有抬升。"
}
```

### 示例问法

| 用户提问 | 处理结果 |
|----------|----------|
| "AAPL 波动率微笑" | 最近月度到期日的微笑曲线 + 偏斜指标 |
| "NVDA 偏斜分析" | 完整微笑 + 偏斜百分位 vs 历史 |
| "TSLA Put 偏斜" | 聚焦 Put 侧 IV、25d 偏斜、偏斜百分位 |
| "SPY 微笑陡吗？" | 当前25d偏斜与252日区间对比 |
| "GOOGL 4月到期微笑形态" | 指定到期日的形态分类 |

### 模拟数据

无 API Key 时可用演示股票：AAPL、NVDA、SPY、TSLA、META。微笑数据使用 `mock-data/` 中的真实IV快照。

### 相关 Skills
- **alphagbm-vol-surface** — 查看所有到期日的完整3D曲面
- **alphagbm-iv-rank** — 整体 IV 相对历史是高还是低？
- **alphagbm-options-strategy** — 陡峭偏斜建议特定价差策略
- **alphagbm-options-score** — 利用偏斜洞察寻找高评分合约

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
