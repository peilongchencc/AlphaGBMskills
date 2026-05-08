---
name: alphagbm-compare
description: |
  2-5 只股票或期权在 GBM 五维评分、期权指标、技术面和估值上的并列对比。
  识别每个维度的胜者。
  触发关键词："对比 AAPL 和 MSFT"、"NVDA 还是 AMD"、"TSLA 还是 META 期权哪个便宜"、
  "科技股对比"、"并列对比"、"谁更好"、"期权对比"、"IV 最低的"、"最有价值的股票"。
globs:
  - "mock-data/compare/**"
---

# AlphaGBM 对比

2-5 只股票或期权在 AlphaGBM 所有维度上的并列对比，帮你找出最优机会。

## 功能说明

| 维度 | 对比内容 |
|------|----------|
| GBM 五维评分 | 每只股票的动量、价值、质量、波动率、情绪评分 |
| 期权指标 | 每只股票的 IV Rank、IV 百分位、VRP、偏斜、期限结构 |
| 技术面 | RSI、MACD、均线、支撑/阻力位 |
| 估值 | P/E、P/S、EV/EBITDA、PEG 比率 — 谁更便宜？|
| 各维度冠军 | 每个维度最优标的高亮显示 |
| 综合推荐 | 所有维度加权综合排名 |

## 使用方法

**输入：** 2-5 个股票代码及对比查询。

**输出：**
- 所有维度并列对比表格
- 每个维度冠军高亮（绿色标识）
- 综合推荐及合成评分
- 关键差异化因素：胜者的优势在哪里
- 交易建议：如果只选一只，选哪个以及原因

**示例问法：**
- `对比 AAPL 和 MSFT` — 全维度正面交锋
- `NVDA 还是 AMD` — 哪只半导体更值得交易？
- `TSLA 和 META 期权哪个更便宜` — 期权成本对比
- `AAPL MSFT GOOGL AMZN META 科技股对比` — 完整板块对比
- `AAPL 和 MSFT 的 30日平值期权对比` — 特定期权合约对比

## 模拟数据

模拟数据文件位于 `mock-data/compare/`，包括：
- `aapl-vs-msft.json` — AAPL vs MSFT 完整对比输出
- `tech-five-way.json` — 五大科技股五向对比
- `options-cost-compare.json` — 期权特定指标对比

## API 端点

```
GET /api/analytics/compare
```

查询参数：
- `symbols`（字符串，必填）— 逗号分隔的股票代码（2-5只），如 `"AAPL,MSFT,GOOGL"`
- `dimensions`（字符串，默认 "all"）— 逗号分隔："pillars"、"options"、"technicals"、"valuations"
- `options_expiry`（字符串）— 期权对比的目标到期日（如 "30d"、"60d"）

响应字段：`tickers[]`、`comparison_table`、`category_winners`、`overall_ranking[]`、`recommendation`

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | 对比后对特定股票做深度分析 |
| [alphagbm-options-score](../alphagbm-options-score/) | 纳入对比的期权评分数据来源 |
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | 期权指标对比中使用的 IV Rank 数据 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
