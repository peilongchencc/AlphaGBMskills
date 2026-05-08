---
name: alphagbm-unusual-activity
description: |
  检测异常期权活动和聪明钱信号。监控成交量/持仓量比飙升、大宗交易、
  异常行权价/到期日组合和净权利金流向。
  触发关键词："异常期权活动"、"AAPL 聪明钱"、"NVDA 大宗交易"、
  "谁在买 TSLA Put"、"期权资金流"、"大宗交易"、"扫单"、
  "异常成交量"、"暗池活动"、"巨鲸交易"。
globs:
  - "mock-data/unusual-activity/**"
---

# AlphaGBM 异常期权活动

检测异常期权活动并分类聪明钱信号，帮助你跟踪机构资金动向。

## 功能说明

| 概念 | 说明 |
|------|------|
| 成交量/持仓量比 | 今日成交量远超持仓量，说明有新仓位建立 |
| 大宗交易（Block）| 单笔大额交易（通常100+合约），以同一价格成交 |
| 扫单（Sweep）| 跨多个交易所快速扫单，表示资金非常着急 |
| 权利金流向 | Call vs Put 的净美元流入，反映方向性押注 |
| 情绪分类 | 看涨扫单 / 看跌大宗 / 对冲 / 财报押注 |
| 历史准确率 | 过去类似异常活动正确预测方向的概率 |

## 使用方法

**输入：** 股票代码或全市场扫描请求。

**输出：**
- 异常活动列表：时间戳、行权价、到期日、类型（Call/Put）、成交量、持仓量、权利金、交易分类
- 每笔交易的情绪分类（看涨扫单、看跌大宗、对冲、财报押注）
- 净权利金流向（Call vs Put 美元金额）
- 历史准确率：类似信号过去出现后标的走向正确的比率
- 汇总聪明钱评分

**示例问法：**
- `异常期权活动` — 今日全市场最异常交易扫描
- `AAPL 聪明钱` — 苹果的机构资金流信号
- `NVDA 大宗交易` — 英伟达的大宗和扫单订单
- `谁在买 TSLA Put` — 特斯拉的看跌资金流分析
- `SPY 期权资金流` — 标普500 ETF 净权利金流向

## 模拟数据

模拟数据文件位于 `mock-data/unusual-activity/`，包括：
- `aapl-unusual-trades.json` — AAPL 最近的异常交易
- `market-wide-scan.json` — 全市场前20个异常活动信号
- `flow-summary.json` — 按板块汇总的权利金流向

## API 端点

```
GET /api/options/unusual-activity/{symbol}
GET /api/options/unusual-activity/scan
```

查询参数：
- `min_premium`（整数，默认100000）— 最低交易权利金（美元）
- `min_vol_oi_ratio`（浮点数，默认3.0）— 最低成交量/持仓量比
- `trade_type`（字符串）— 过滤：`"sweep"`、`"block"`、`"all"`
- `sentiment`（字符串）— 过滤：`"bullish"`、`"bearish"`、`"all"`

响应字段：`trades[]`、`net_premium_flow`、`sentiment_summary`、`smart_money_score`、`historical_accuracy`

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-options-score](../alphagbm-options-score/) | 异常活动纳入整体期权评分 |
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | 解读资金流信号的市场背景 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
