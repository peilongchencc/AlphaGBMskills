---
name: alphagbm-duan-analysis
description: |
  段永平风格卖方策略分析：在「愿意买入价格」卖 Put、Covered Call 收益增强，
  以及基于当前 VIX 的「极度恐慌抄底」背景读取。输出三块紧凑的分析卡片，
  源自让段永平在中国散户投资中闻名的那套框架（只卖期权不买，租金收集逻辑，
  永久持有优质公司）。
  触发关键词："段永平风格 AAPL"、"卖 Put NVDA 愿意在 120 入"、
  "TSLA Covered Call 收益"、"AAPL 现在应该卖 Put 吗"、"MSFT 卖方策略"、
  "段式分析"、"权利金收集布局"、"民族主义卖方手册"。
globs:
  - "mock-data/duan-analysis/**"
---

# AlphaGBM 段永平分析

对单只股票即时输出段氏框架。三块聚焦输出：

1. **卖 Put** — 如果你「愿意在 $X 买入」，卖一张 $X 行权价的 Put 实际收多少权利金，
   被行权后成本价是多少？
2. **Covered Call** — 如果你持有100股，卖约 5% 虚值的 Call（25-50 DTE）能收多少收益？
   被行权的话总回报是多少？
3. **极度恐慌抄底背景** — 当前 VIX 在说什么？我们是否到了段永平说的
   「极度恐慌 = 极度机会」那档（VIX ≥ 35），还是继续等待？

每个面板都针对段永平框架量身打造：只卖不买、收租逻辑、永久持有优质公司，
将 VIX 极端飙升视为机会而非威胁。

## 为什么这是一个独立 Skill

通用的 `alphagbm-options-strategy` 可以计算任意价差，但段永平风格
有三个非常具体的操作和非常具体的哲学。这个 Skill 将那套哲学包装进单次调用，
配有符合中国散户实际说话方式的中文原生文案。

## 使用方法

**输入：**
- `ticker`（必填）
- `buy_price`（可选）— 你「很乐意在这个价格买入」的水位；
  省略时默认为当前价 × 0.95

**输出（每个面板在无合适合约时可为 null）：**

- `sell_put`: `{strike, premium, annualized_yield_pct, if_assigned_cost_basis, delta, dte}`
- `covered_call`: `{strike, premium, annualized_yield_pct, upside_cap_pct,
  total_return_if_called_pct, dte}`
- `panic_buy`: `{vix, level, signal (bool), action_zh, action_en}`
  - `level` 取值：`normal / caution / extreme_fear`
  - `signal = true` 当 VIX ≥ 35（段永平买入档位）

以及元数据：`ticker, stock_price, expiry_date, dte, timestamp`

## 示例问法

- `段永平风格 AAPL` — 苹果的三块面板
- `卖 Put NVDA 愿意在 110 入` — 目标 $110 入场的卖 Put 分析
- `TSLA Covered Call 收益` — 当前价格下的 CC 分析
- `VIX 到段永平买入线了吗` — 单独看极度恐慌面板（也可用 `alphagbm-vix-status`）
- `在 180 卖 AAPL Put 合适吗` — 特定行权价的卖 Put 分析

## 模拟数据

模拟数据在 `mock-data/duan-analysis/` — AAPL 买入价180的示例。

## API 端点

```
GET /api/options/duan-analysis?ticker={SYMBOL}&buy_price={PRICE}
```

查询参数：
- `ticker`（必填）
- `buy_price`（可选，浮点数）— 卖 Put 的首选入场行权价；默认为当前价 × 0.95

响应示例：

```json
{
  "success": true,
  "ticker": "AAPL",
  "stock_price": 185.4,
  "expiry_date": "2026-06-20",
  "dte": 41,
  "sell_put": {
    "strike": 180.0,
    "premium": 2.45,
    "annualized_yield_pct": 12.1,
    "implied_vol": 0.24,
    "delta": -0.28,
    "open_interest": 4821,
    "volume": 312,
    "if_assigned_cost_basis": 177.55,
    "dte": 41
  },
  "covered_call": {
    "strike": 195.0,
    "premium": 2.10,
    "annualized_yield_pct": 10.1,
    "implied_vol": 0.22,
    "delta": 0.32,
    "open_interest": 3200,
    "volume": 198,
    "upside_cap_pct": 5.18,
    "total_return_if_called_pct": 6.31,
    "dte": 41
  },
  "panic_buy": {
    "vix": 18.7,
    "level": "normal",
    "signal": false,
    "action_zh": "VIX 18.7 偏平静。段永平风格下此水位更适合卖 Put 等跌到心理价位，而不是主动抄底。",
    "action_en": "VIX 18.7 is calm. Duan-style strategy prefers Sell-Put \"waiting\" over proactive buying at this level."
  },
  "timestamp": "2026-04-24T08:00:00"
}
```

定价：每次1次期权分析额度；每（股票，买入价）组合5分钟缓存。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-vix-status](../alphagbm-vix-status/) | 单独 VIX 档位读取（极度恐慌面板使用相同分类）|
| [alphagbm-options-score](../alphagbm-options-score/) | 更广泛的多因子期权评分（非段氏专用）|
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 自定义多腿策略 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
