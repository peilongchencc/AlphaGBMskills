---
name: alphagbm-take-profit
description: |
  通过「过山车率」指标量化股票是否适合长期持有或需要分批止盈，
  在每只股票约10年日线历史数据上运行15种退出策略并返回各自的中位数结果。
  首次查询新股票约需30秒并全局缓存；后续查询即时返回。
  触发关键词："TQQQ 适合长期持有吗"、"NVDA 止盈策略"、"AAPL 能一直持有吗"、
  "TSLA 过山车率"、"COIN 卖出策略"、"什么时候卖 NVDA"、"QQQ 止盈计划"、
  "我的股票退出策略"、"杠杆 ETF 持有分析"。
globs:
  - "mock-data/take-profit/**"
---

# AlphaGBM 止盈策略实验室

机械化回答任意股票的一个问题：**这只股票可以一直持有，还是需要主动止盈？**
大多数散户亏损来自糟糕的退出，而非糟糕的入场。这个 Skill 用10年日线数据量化退出决策。

## 核心指标：过山车率

「过山车事件」发生在：某次入场的纸面盈利超过 +50% 后，又从那个峰值回撤超过50%，
才退出。示例：100入场，涨到190，又跌回90 — 你没亏钱，但那90点的峰值盈利你「摸到了」
又归零了，这段旅程相当残忍。

过山车率在不同资产间相差**高达97个百分点**：
- 宽基 ETF（SPY、VTI）：0% — 可以永远持有
- 蓝筹股（AAPL、MSFT）：0% — 可以永远持有
- 板块 ETF（SOXX、XLK）：0% — 可以永远持有
- 大型成长股（META、AMZN）：~47% — 推荐分批止盈
- 港股科技（腾讯、阿里）：~49% — 推荐分批止盈
- 高弹性成长（NVDA、TSLA、AMD）：~85% — 必须分批止盈
- 加密相关（COIN、MSTR）：~90% — 必须分批止盈
- **杠杆 ETF（TQQQ、SOXL）：~97% — 结构上无法持有**

**能否持有是工具本身的特性，不是心态问题。**

## 策略体系（共15种）

- **A 系列**（触发时全部卖出）：A_+50%、A_+100%、A_+200%
- **B 系列**（分批卖出）：B_50/100/200（默认）、B_30/60/100、B2_20/40/80、B3_40/80/150、
  B5 后加权、B6 前加权
- **C_10x**（信仰持有）
- **D**（-20% / -30% 移动止损）— **在每只被测股票上都跑输持有策略**
- **E**（永不卖出 / 长期持有）
- **F**（+50% 激活后追高点回撤）
- **G**（历史波动率感知：根据入场日波动率选择 A_+100% 或 A_+200%）

## 使用方法

**输入：**
- `ticker`（必填）— 任意美股 / 港股 / A 股、ETF 或杠杆 ETF

**输出：**
- **特征概括**：`color`（绿/琥珀/红）+ `special_flag`（杠杆 ETF 用 `no_hold`，
  主动卖出跑赢持有时用 `reverse_alpha`）
- **核心数字**：`rollercoaster_rate`、`max_drawdown`、`hold_cagr`
- **`strategy_results`**：15种策略，每种含 `{cagr, rc, mdd}` 中位数
- **数据溯源**：`sample_size`（通常约120个入场点）、`period`、`computed_at`

调用方需要：
1. 展示核心特征概括
2. 根据用户性格 + 仓位大小推荐策略（前端逻辑）
3. 按 `entry × 1.5 / 2.0 / 3.0` 等生成具体的 GTC 限价卖单

## 示例问法

- `TQQQ 适合长期持有吗` → no_hold 标志 + 过山车率97% → 分批止盈
- `NVDA 止盈策略` → 高成长特征，B_50/100/200 默认推荐
- `AAPL 能一直持有吗` → 蓝筹特征，过山车率0%，推荐持有
- `COIN 什么时候应该卖` → 加密特征，强制分批止盈
- `SPY 过山车率是多少` → 0%，长期持有最优
- `MSFT 止盈策略回测` → 全15种策略对比

## 模拟数据

模拟数据在 `mock-data/take-profit/` — TQQQ（no_hold）、AAPL（持有最优）和 PYPL（reverse_alpha）的示例响应。

## API 端点

```
POST /api/stock/take-profit-analyze
Content-Type: application/json
```

请求体：

```json
{"ticker": "TQQQ"}
```

也可查询缓存库（不消耗额度）：

```
GET /api/stock/take-profit-library
```

返回已缓存股票列表及其核心数字，方便 Agent 判断哪些查询即时、哪些是首次计算。

响应示例：

```json
{
  "success": true,
  "ticker": "TQQQ",
  "color": "red",
  "special_flag": "no_hold",
  "rollercoaster_rate": 97,
  "max_drawdown": -82,
  "hold_cagr": 37.0,
  "strategy_results": {
    "A_50": {"cagr": 6.0, "rc": 21, "mdd": -32},
    "A_100": {"cagr": 11.5, "rc": 44, "mdd": -50},
    "A_200": {"cagr": 17.6, "rc": 64, "mdd": -62},
    "B_50_100_200": {"cagr": 12.0, "rc": 36, "mdd": -42},
    "B6_front": {"cagr": 11.0, "rc": 29, "mdd": -37},
    "E_hold": {"cagr": 37.0, "rc": 97, "mdd": -82}
  },
  "sample_size": 120,
  "period": {"start": "2014-04-20", "end": "2026-04-20"},
  "computed_at": "2026-04-24T08:00:00"
}
```

定价：首次计算消耗1次股票分析额度；**全局数据库缓存30天** — 一旦计算完成，
所有用户都能即时读取（进程内5分钟缓存命中同样免费）。
首次计算约需30秒（10年日线 × 15种策略 × 约120个入场点 = 约1800次模拟）。
后续读取 < 100 毫秒。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | 深度基本面 + 动量分析，补充退出决策 |
| [alphagbm-watchlist](../alphagbm-watchlist/) | 跨组合的批量查询 |
| [alphagbm-hedge-advisor](../alphagbm-hedge-advisor/) | 对「高过山车率」仓位进行期权对冲 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
