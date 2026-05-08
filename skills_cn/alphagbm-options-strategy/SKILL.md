---
name: alphagbm-options-strategy
description: >
  根据市场观点（看涨、看跌、中性、波动）推荐最优多腿期权策略，支持15+策略模板，
  包括价差、铁鹰、跨式和收入策略。返回完整盈亏特征、盈亏平衡点和盈利概率。
  适用场景：选择期权策略、围绕财报规划交易、构建多腿仓位、对比策略备选。
  触发关键词："AAPL 期权策略"、"NVDA 看涨策略"、"TSLA 财报最佳玩法"、
  "SPY 铁鹰"、"META 熊市 Put 价差"、"GOOGL 收入策略"、"QQQ 中性策略"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM 期权策略

## 前置条件

- **API Key**：设置环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx...`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。

## 功能说明

给定**市场观点**和**股票代码**，推荐按风险/收益特征排名的最优多腿期权策略。
使用 AlphaGBM 评分引擎自动选择最优行权价和到期日。

### 四种核心策略与趋势匹配

| 策略 | 理想趋势 | 最大盈利 | 最大亏损 |
|------|----------|----------|----------|
| **卖 Put** | 中性 / 看涨 | 收到权利金 | 行权价 - 权利金（被行权风险）|
| **卖 Call** | 中性 / 看跌 | 收到权利金 | 无限（裸空）|
| **买 Call** | 看涨 | 无限 | 支付的权利金 |
| **买 Put** | 看跌 | 行权价 - 权利金 | 支付的权利金 |

**趋势匹配评分**：评分模型奖励与主导趋势匹配的合约。对于卖 Put，下跌趋势得100分
（反直觉：在弱势时卖 Put 可获得更高权利金），上涨趋势得30分。
对于买 Call，看涨动量权重25%。

### 支持的策略模板（15+）

| 类别 | 策略 |
|------|------|
| **看涨** | 牛市 Call 价差、牛市 Put 价差（BPS）、Long Call、Covered Call、合成多头 |
| **看跌** | 熊市 Put 价差、熊市 Call 价差、Long Put、合成空头 |
| **中性** | 铁鹰（Iron Condor）、铁蝶（Iron Butterfly）、Short Straddle、Short Strangle、日历价差 |
| **波动** | Long Straddle、Long Strangle、蝴蝶价差、反向铁鹰 |
| **收入** | Covered Call、现金担保卖 Put（CSP）、Collar、Jade Lizard |

### 风险收益特征

| 风格 | 典型胜率 | 典型回报 |
|------|----------|----------|
| steady_income（稳定收入）| 65-80% | 每月 1-5% |
| balanced（均衡）| 40-55% | 50-200% |
| high_risk_high_reward（高风险高回报）| 20-40% | 2-10倍 |
| hedge（对冲）| 30-50% | 0-1倍 |

### 策略选择逻辑

1. 将用户的**市场观点**匹配到候选策略
2. 根据 **IV 环境**过滤（高 IV 适合卖权利金；低 IV 适合买权利金）
3. 使用**风险/收益**、**盈利概率**和**资金效率**对每个候选评分
4. 排序并返回前3个推荐，附完整详情

## API 端点

### 策略模板

列出所有可用策略模板：

```
GET /api/options/tools/strategy/templates
```

### 策略构建器

根据模板和特定参数构建策略：

```
POST /api/options/tools/strategy/build
Content-Type: application/json

{
  "mode": "template",
  "template_id": "bull_call_spread",
  "spot": 150.0,
  "expiry_days": 30,
  "strikes": [140, 145, 150, 155, 160]
}
```

### 期权扫描器

按条件跨标的扫描策略：

```
POST /api/options/tools/scan
Content-Type: application/json

{
  "strategies": ["covered_call", "cash_secured_put"],
  "tickers": ["AAPL", "NVDA"],
  "min_yield_pct": 1.0
}
```

## 使用方法

### 输入
- **必填**：股票代码 + 市场观点（看涨 / 看跌 / 中性 / 波动）
- **可选**：最大资金、目标到期日、风险承受度（保守 / 稳健 / 激进）

### 输出结构

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "market_view": "bullish",
  "iv_environment": "moderate",
  "recommendations": [
    {
      "strategy": "Bull Call Spread",
      "rank": 1,
      "score": 8.5,
      "legs": [
        {"action": "buy", "type": "call", "strike": 215, "expiry": "2026-04-18", "price": 7.20},
        {"action": "sell", "type": "call", "strike": 225, "expiry": "2026-04-18", "price": 3.40}
      ],
      "max_profit": 620,
      "max_loss": 380,
      "breakeven": [218.80],
      "probability_of_profit": 0.58,
      "risk_reward_ratio": 1.63,
      "net_debit": 380,
      "greeks": {
        "delta": 0.32,
        "gamma": 0.012,
        "theta": -0.08,
        "vega": 0.14
      },
      "rationale": "中等看涨敞口，风险有上限。IV 合理，借方价差优于裸买 Call。"
    }
  ]
}
```

### 示例问法

| 用户提问 | 处理结果 |
|----------|----------|
| "AAPL 期权策略" | 从股票分析推断观点，返回前3个策略 |
| "NVDA 看涨策略" | 过滤到看涨策略，按评分排序 |
| "TSLA 财报最佳玩法" | 选择波动率策略（跨式、宽跨式）应对事件 |
| "SPY 铁鹰" | 以最优行权价构建铁鹰并返回完整特征 |
| "GOOGL 收入策略" | 过滤到 Covered Call、CSP、Collar |
| "META 保守看跌策略" | 参数收紧的 Bear Put Spread 或 Collar |

### 模拟数据

无 API Key 时可用演示股票：AAPL、NVDA、SPY、TSLA、META。策略推荐使用 `mock-data/` 中的真实链数据。

### 相关 Skills
- **alphagbm-options-score** — 对每条腿使用的合约评分
- **alphagbm-pnl-simulator** — 随时间模拟任意推荐策略的盈亏
- **alphagbm-greeks** — 深入分析所选策略的仓位希腊字母
- **alphagbm-iv-rank** — 确认 IV 环境是否有利于买或卖权利金

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
