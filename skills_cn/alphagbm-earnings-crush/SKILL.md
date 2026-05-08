---
name: alphagbm-earnings-crush
description: |
  完整财报季 IV 分析：历史崩塌幅度、隐含波动预期、IV Rank 策略标签，以及现成的
  铁鹰策略报价，一次调用全搞定。
  触发关键词："AAPL 财报 IV 崩塌"、"NVDA 财报前 IV"、"MSFT 隐含波动"、
  "META 铁鹰"、"AAPL 财报 IV Rank"、"TSLA 财报怎么玩"、"是否适合在 AMZN 财报前
  做空 IV"、"财报后 IV 下跌"、"财报前跨式"、"财报前策略"。
globs:
  - "mock-data/earnings-crush/**"
---

# AlphaGBM 财报 IV 面板

财报周所需的一切：历史 IV Crush + 前瞻隐含波动预期 + IV Rank 策略推荐
+ 以隐含波动为中心的现成铁鹰报价，一次 API 调用完成。

## 功能说明

| 概念 | 说明 |
|------|------|
| IV Crush | 财报公布后隐含波动率急剧下降的现象 |
| 平均崩塌幅度 | 过去8个季度财报前峰值到财报后低谷的平均IV下降幅度 |
| **隐含波动 ±X%** | 期权定价的财报涨跌幅，由平值IV × √(DTE/365) 推导 |
| **IV Rank** | 当前平值IV相对2年历史的20日HV百分位，驱动策略推荐 |
| **策略推荐** | IV Rank > 70 → 做空IV（铁鹰）；< 30 → 方向性（Long Call/Put）；30-70 → 等待 |
| **铁鹰报价** | 现成4腿价差，Short 行权价在 ±1× 隐含波动处，含具体权利金/最大盈亏/最大亏损/盈亏平衡 |
| 历史对比 | 过去8个财报的隐含波动与实际波动对比 |

## 使用方法

**输入：** 有近期或历史财报的股票代码。

**输出：**
- 距下次财报天数（如已安排）
- 当前股价 + 平值IV + IV Rank
- **隐含波动 ±X% 和 ±$Y** — 财报季最常引用的数字
- **推荐标签**（🔥 做空IV / 等待 / 方向性），含中英文说明
- **铁鹰报价** — 4个行权价 + 权利金 + 最大盈利 + 最大亏损 + 盈亏平衡区间（Pro 档位）
- 过去8个季度：财报前IV / 财报后IV / 崩塌幅度 / 实际涨跌 / 跨式盈亏
- 平均崩塌幅度和跨式胜率

**示例问法：**
- `AAPL 财报 IV 崩塌历史` — 完整崩塌历史 + 下次财报隐含波动
- `NVDA 隐含波动` — 期权对下次财报的定价
- `META 铁鹰` — 现成做空权利金策略
- `MSFT 财报 IV Rank` — 策略标签 + 推荐
- `TSLA 财报前适合做空 IV 吗` — 推荐 + 铁鹰报价
- `AMZN 过去8个季度跨式盈亏` — 历史做空权利金胜率

## 模拟数据

模拟数据文件在 `mock-data/earnings-crush/`：
- `aapl-crush-history.json` — AAPL 8个季度的崩塌历史 + 隐含波动 + 铁鹰
- `nvda-crush-history.json` — NVDA 同上
- `crush-summary.json` — 多股票汇总崩塌统计

## API 端点

```
GET /api/options/earnings-crush/{symbol}
```

查询参数：
- `quarters`（整数，默认8）— 分析的历史财报季数
- `include_straddle_pnl`（布尔，默认 true）— 包含跨式盈亏模拟
- `include_iron_condor`（布尔，默认 true）— 包含铁鹰报价（UI 的 Pro 档位）

响应字段（核心数字）：
- `next_earnings`、`days_to_earnings`、`current_atm_iv`、`current_stock_price`
- `implied_move_pct` — 如5.1表示市场定价 ±5.1% 波动
- `iv_rank_pct` — 0-100百分位；驱动 `recommendation.level`
- `recommendation` — `{level: 'high'|'mid'|'low'|'unknown', iv_rank_pct, recommendation_zh, recommendation_en}`
- `iron_condor` — `{short_call, long_call, short_put, long_put, credit, max_profit, max_loss, breakeven_up, breakeven_down, wing_width_pct}`
- `crush_history[]`、`avg_crush_pct`、`avg_actual_move_pct`、`straddle_win_rate`
- `quarters_analyzed`、`timestamp`

定价：1次期权分析额度；相同股票/参数5分钟内缓存命中免费。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | 当前 IV 百分位，财报前 IV 是否已经偏高？|
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 考虑财报时机的策略推荐 |
| [alphagbm-vol-surface](../alphagbm-vol-surface/) | 财报到期日附近的期限结构扭折 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
