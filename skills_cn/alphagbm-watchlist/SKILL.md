---
name: alphagbm-watchlist
description: |
  监控一组股票的关键变化：价格、IV Rank、异常活动、财报日期和评分变化。
  支持自定义自选列表和默认「热门期权」列表。
  触发关键词："把 AAPL 加入自选"、"我的自选股"、"关注 NVDA TSLA META"、
  "自选股预警"、"从自选删除 SPY"、"热门期权"、
  "我的自选股有什么"、"自选股摘要"、"每日自选股"。
globs:
  - "mock-data/watchlist/**"
---

# AlphaGBM 自选股

监控你关注的股票，追踪有意义的变化 — 价格异动、IV 变化、异常活动、
即将到来的财报和评分变化 — 全部集中在一个仪表盘中。

## 功能说明

| 功能 | 说明 |
|------|------|
| 自定义自选列表 | 创建和管理个人股票追踪列表 |
| 热门期权列表 | 系统精选的期权活动最活跃股票默认列表 |
| 价格预警 | 标记显著价格异动（跳空涨/跌、突破、跌破）|
| IV Rank 变化 | 高亮 IV Rank 穿越关键阈值的股票（如升破80或降至20以下）|
| 异常活动 | 浮出自选股中的异常期权资金流 |
| 财报临近 | 当自选股7天内有财报时发出提醒 |
| 优先级排序 | 通知按重要程度排序，最重要的先看 |

## 使用方法

**输入：** 自选股管理指令或查询。

**输出：**
- 自选股仪表盘：每只股票的当前价格、日涨跌、IV Rank、下次财报日期
- 预警标志：上次检查以来的变化（价格突破、IV 飙升、异常资金流等）
- 每日摘要：所有自选股的按优先级排序通知
- 快速操作：基于自选股预警的建议交易

**示例问法：**
- `把 AAPL 加入自选` — 添加股票到自选列表
- `我的自选股` — 查看完整自选股仪表盘
- `关注 NVDA TSLA META` — 批量添加多只股票
- `自选股预警` — 仅显示有活跃预警的股票
- `从自选删除 SPY` — 移除一只股票
- `热门期权` — 查看精选高活跃度期权列表

## 模拟数据

模拟数据文件位于 `mock-data/watchlist/`，包括：
- `user-watchlist.json` — 包含10只股票的示例用户自选股
- `watchlist-alerts.json` — 自选股触发的预警
- `hot-options.json` — 热门期权精选列表

## API 端点

```
GET    /api/user/watchlist
POST   /api/user/watchlist
DELETE /api/user/watchlist/{symbol}
GET    /api/user/watchlist/alerts
GET    /api/analytics/hot-options
```

POST 请求体：`{ "symbol": "AAPL" }` 或 `{ "symbols": ["NVDA", "TSLA", "META"] }`

响应字段：`watchlist[]`、`alerts[]`、`daily_summary`、`hot_options[]`

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | 对自选股中任意一只做深度分析 |
| [alphagbm-alert](../alphagbm-alert/) | 对自选股设置特定预警条件 |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | 触发自选股通知的异常资金流数据 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
