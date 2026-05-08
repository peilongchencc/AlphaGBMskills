---
name: alphagbm-polymarket
description: |
  整合预测市场数据（Polymarket）与期权分析，浮出事件概率与期权隐含概率之间的
  定价差异信号。
  触发关键词："Polymarket 信号"、"预测市场 vs 期权"、"事件概率"、
  "降息概率"、"选举赔率 vs 期权"、"Polymarket 套利"、
  "隐含概率不匹配"、"预测市场数据"、"事件驱动期权"。
globs:
  - "mock-data/polymarket/**"
---

# AlphaGBM Polymarket 整合

连接预测市场与期权市场 — 当 Polymarket 显示降息概率 70% 但期权仅隐含 55% 时，
这就是一个可能存在交易价值的定价差。

## 功能说明

| 概念 | 说明 |
|------|------|
| 事件概率 | 预测市场对特定事件（如降息、选举结果）的共识概率 |
| 期权隐含概率 | 从期权价格和偏斜推导出的期权市场定价概率 |
| 概率差值 | 预测市场与期权隐含概率之间的差值，差值大说明可能存在定价错误 |
| 套利信号 | 当差值超过阈值时，可能存在可交易机会 |
| 事件相关性 | 二元事件与特定期权仓位的映射强度 |
| 历史准确率 | 预测市场 vs 期权在预测类似历史事件中的准确度记录 |

## 使用方法

**输入：** 事件类型或关于预测市场 vs 期权定价的查询。

**输出：**
- 事件概率对比表：Polymarket 概率 vs 期权隐含概率
- 概率差值及方向（哪个市场对事件更看涨/看跌）
- 按置信度和差值大小排序的定价错误信号
- 利用定价错误的建议期权交易
- 类似历史事件的历史准确率对比

**示例问法：**
- `Polymarket 信号` — 扫描当前最大概率不匹配
- `预测市场 vs 期权降息概率` — 对比联储降息概率
- `选举事件概率` — 选举结果概率 vs 期权仓位
- `降息概率` — 预测市场和期权各自对下次美联储会议的暗示
- `Polymarket 套利` — 可操作的定价错误机会

## 模拟数据

模拟数据文件位于 `mock-data/polymarket/`，包括：
- `rate-cut-comparison.json` — 美联储降息概率：Polymarket vs 期权隐含
- `event-scan.json` — 活跃预测市场中的顶级定价差信号
- `historical-accuracy.json` — 各市场类型历史事件预测准确率

## API 端点

```
GET /api/analytics/polymarket/signals
GET /api/analytics/polymarket/event/{event_id}
```

查询参数：
- `event_type`（字符串）— 过滤："fed"（美联储）、"election"（选举）、"earnings"（财报）、"macro"（宏观）、"all"（全部）
- `min_spread`（浮点数，默认0.10）— 最低概率差值（10%）
- `include_trades`（布尔，默认 true）— 包含建议期权交易

响应字段：`events[]`、`polymarket_prob`、`options_implied_prob`、`spread`、`confidence`、`suggested_trades[]`、`historical_accuracy`

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | 解读事件概率的宏观情绪背景 |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 可利用定价差信号的策略推荐 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
