---
name: alphagbm-alert
description: |
  设置价格、IV 或活动类智能提醒，触发时附带完整上下文通知。
  提醒类型包括：IV Rank 阈值穿越、价格支撑/阻力突破、异常活动检测、
  财报临近和 VRP 信号变化。
  触发关键词："AAPL IV Rank 超过 80 提醒我"、"NVDA 跌破 850 通知我"、
  "TSLA 财报提醒"、"VRP 预警"、"设置价格提醒"、
  "IV 飙升时提醒我"、"异常活动通知"、"我的提醒"、"删除提醒"。
globs:
  - "mock-data/alert/**"
---

# AlphaGBM 提醒

基于价格、IV Rank、异常活动、财报时机和 VRP 信号设置智能提醒，
每次触发都附带完整背景信息，让你能立即行动。

## 功能说明

| 提醒类型 | 说明 |
|----------|------|
| IV Rank 阈值 | IV Rank 穿越指定水平时触发（如 IV Rank > 80）|
| 价格水平 | 价格突破支撑、阻力或自定义价格时触发 |
| 异常活动 | 检测到指定股票的异常期权资金流时触发 |
| 财报临近 | 股票财报前 N 天触发 |
| VRP 信号变化 | 波动率风险溢价翻转时触发（如从负转正）|
| 一次性 vs 循环 | 一次性提醒触发后自动删除；循环提醒重置并持续监控 |

## 使用方法

**输入：** 指定股票代码、条件和阈值的提醒配置指令。

**输出：**
- 提醒配置确认，含监控内容摘要
- 触发时：附带完整上下文的提醒通知（触发内容、当前数值、建议操作）
- 提醒管理：列出活跃提醒、编辑条件、删除提醒

**示例问法：**
- `AAPL IV Rank 超过 80 提醒我` — IV Rank 阈值提醒
- `NVDA 跌破 850 通知我` — 价格水平提醒
- `TSLA 财报提醒` — TSLA 财报前7天提醒
- `AAPL VRP 预警` — AAPL VRP 信号变化时通知
- `设置 SPY 550 价格提醒` — 简单价格目标提醒
- `我的提醒` — 列出所有活跃提醒
- `删除提醒 3` — 删除指定提醒

## 模拟数据

模拟数据文件位于 `mock-data/alert/`，包括：
- `active-alerts.json` — 已配置提醒的示例列表
- `triggered-alerts.json` — 最近触发的提醒及上下文
- `alert-config-response.json` — 提醒创建确认示例

## API 端点

```
GET    /api/user/alerts
POST   /api/user/alerts
PUT    /api/user/alerts/{alert_id}
DELETE /api/user/alerts/{alert_id}
GET    /api/user/alerts/triggered
```

POST 请求体：
```json
{
  "symbol": "AAPL",
  "type": "iv_rank_above",
  "threshold": 80,
  "recurring": true
}
```

响应字段：`alert_id`、`status`、`condition_summary`、`triggered_alerts[]`、`context`

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-watchlist](../alphagbm-watchlist/) | 自选股是设置提醒的天然候选 |
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | 驱动 IV 阈值提醒的 IV Rank 数据 |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | 驱动活动提醒的异常资金流检测 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
