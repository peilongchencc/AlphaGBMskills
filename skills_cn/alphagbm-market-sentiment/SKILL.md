---
name: alphagbm-market-sentiment
description: |
  全市场情绪仪表盘，涵盖 VIX、Put/Call 比率、恐惧贪婪指数、市场广度和板块轮动分析。
  将当前市场状态分类为风险偏好（risk-on）、避险（risk-off）或中性（neutral）。
  触发关键词："市场情绪"、"市场是否恐惧"、"VIX 分析"、"put call ratio"、
  "市场广度"、"恐惧贪婪"、"风险偏好还是避险"、"涨跌比"、
  "新高新低"、"板块轮动"、"市场状态"。
globs:
  - "mock-data/market-sentiment/**"
---

# AlphaGBM 市场情绪仪表盘

将全市场情绪指标汇总成单一仪表盘，对当前市场状态进行分类，以指导交易策略。

## 功能说明

| 指标 | 说明 |
|------|------|
| VIX 水平 + 百分位 | 当前 VIX 值及其在过去一年的排名（如85百分位 = 恐慌偏高）|
| Put/Call 比率 | 股票和指数期权的 P/C 比率，高值表示恐慌，低值表示自满 |
| 恐惧贪婪指数 | 综合多项情绪输入的0-100复合得分 |
| 市场广度 | 涨跌比和新高/新低数量，衡量行情参与度 |
| 板块轮动阶段 | 领涨/落后板块映射到经济周期 |
| 状态分类 | 综合判断：风险偏好 / 避险 / 中性，带置信度 |

## 使用方法

**输入：** 市场情绪查询（无需指定股票，或指定 VIX/SPX 进行聚焦分析）。

**输出：**
- 包含所有指标当前读数的情绪仪表盘
- 历史背景：每个指标在过去1年的位置
- 当前状态分类（风险偏好 / 避险 / 中性）+ 置信度
- 板块轮动图：早周期 / 中周期 / 晚周期 / 衰退定位
- 可操作解读：当前情绪对期权交易意味着什么

**示例问法：**
- `市场情绪` — 包含所有指标的完整仪表盘
- `市场现在恐惧吗` — 快速恐惧/贪婪评估
- `VIX 分析` — VIX 水平、期限结构和百分位深度解析
- `put call ratio` — 股票和指数 P/C 比率及历史背景
- `市场广度` — 涨跌比、新高/新低、参与度分析
- `板块轮动` — 哪些板块领涨以及当前周期阶段

## 模拟数据

模拟数据文件位于 `mock-data/market-sentiment/`，包括：
- `sentiment-dashboard.json` — 包含所有指标的完整仪表盘快照
- `vix-history.json` — VIX 时间序列及百分位排名
- `sector-rotation.json` — 板块表现和周期分类

## API 端点

```
GET /api/analytics/market-sentiment
```

查询参数：
- `indicators`（字符串，默认 "all"）— 逗号分隔列表："vix"、"pcr"、"fear_greed"、"breadth"、"rotation"
- `lookback_days`（整数，默认 252）— 百分位计算的历史周期

响应字段：`vix`、`put_call_ratio`、`fear_greed_index`、`breadth`、`sector_rotation`、`regime`、`regime_confidence`

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | 受市场状态影响的单股分析 |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | 贡献情绪信号的异常期权流 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
