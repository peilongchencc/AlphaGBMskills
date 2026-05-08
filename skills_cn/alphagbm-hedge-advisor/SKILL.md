---
name: alphagbm-hedge-advisor
description: |
  针对现有股票仓位的情景驱动对冲推荐。输入股票代码 + 成本价 + 持仓目的，
  自动识别持仓场景（接刀/抄底布局/浮盈保护/正常持仓），并从当前期权链获取真实
  行权价和权利金，给出具体的 Long Put、Collar 或减仓建议。
  触发关键词："对冲我的 AAPL"、"保护 NVDA 浮盈"、"MSFT Collar 策略"、
  "TSLA Long Put"、"如何对冲 COIN 接刀风险"、"降低 BABA 风险"、
  "锁定 META 收益"、"下行保护"、"组合对冲"、"仓位保险"。
globs:
  - "mock-data/hedge-advisor/**"
---

# AlphaGBM 对冲顾问

「我在 $140 买入 AAPL，现在涨到 $180 了，我怎么保护浮盈？」

照字面意思回答这个问题。给定股票代码 + 成本价 + 持仓目的，
将持仓分类到四个场景之一，并从实时期权链解析出具体的对冲方案，
行权价和成本已经算好了。

## 场景说明

| 场景 | 触发条件 | 推荐对冲 |
|------|----------|----------|
| **接刀下落（Falling Knife）** | 30日高点以来回撤 ≥ 15% 且浮盈 ≤ +5% | Long Put 5% 虚值，75天到期，100%覆盖，预算约5% |
| **抄底布局（Bottom Fishing）** | 浮盈在 ±8% 以内且目的是 just_bought 或 long_term | Long Put 5% 虚值，90天到期，50-75%覆盖，预算约3% |
| **浮盈保护（Gain Protection）** | 浮盈 ≥ 15% | Collar 95/110（零成本或净收益）+ 减仓作为备选 |
| **正常持仓（Normal Hold）** | 以上场景均不触发 | 仅仓位规则，无紧急对冲 |

## 返回内容

对于每个推荐方案，Skill 从实时期权链解析**真实行权价和价格**：

- **Long Put**：行权价、DTE、`cost_per_share`、`cost_per_contract`、`cost_pct_of_spot`、Delta、IV
- **Collar**：`long_put_strike`、`short_call_strike`、`put_cost`、`call_credit`、
  `net_cost_per_share`（负值表示你收到权利金）、盈亏平衡分析
- **减仓/仓位规则**：仅静态规则说明

还返回 `position_rules[]` 数组（单票 ≤20%、板块 ≤30-35%、现金储备10-15%等），
用于正常持仓场景。

## 使用方法

**输入：**
- `ticker`（必填）
- `cost_basis`（必填，浮点数 — 平均入场价）
- `purpose`（可选，默认 `long_term`）— 取值：`long_term / short_term /
  pre_earnings / just_bought`

**输出：**
- 场景标签 + 原因（中英文）
- 当前价格、成本价、未实现盈亏%、近期回撤%
- `recommendations[]` — 每项含类型、优先级、标题、逻辑说明，以及含真实定价的 `resolved` 块
- `position_rules[]` — 始终适用的仓位管理规则

**示例问法：**
- `AAPL 成本 $140，现价 $180，怎么对冲` → 浮盈保护 → Collar 95/110 报价
- `我刚在抄底时买了 NVDA $110，要对冲吗？` → 接刀或抄底布局 → Long Put 5% 虚值 60-90 DTE
- `怎么保护我的 TSLA 仓位` → 根据盈亏判断是浮盈保护还是抄底布局
- `MSFT 成本 340 现价 410 怎么 Collar` → 完整 Collar 定价

## 模拟数据

模拟响应在 `mock-data/hedge-advisor/` — 涵盖四种场景的示例。

## API 端点

```
GET /api/options/hedge-advisor?ticker={SYMBOL}&cost_basis={PRICE}&purpose={PURPOSE}
```

查询参数：
- `ticker`（必填）
- `cost_basis`（必填，浮点数 > 0）
- `purpose`（默认 `long_term`）— 取值：`long_term / short_term / pre_earnings / just_bought`

响应示例：

```json
{
  "success": true,
  "ticker": "AAPL",
  "current_price": 180.0,
  "cost_basis": 140.0,
  "unrealized_pnl_pct": 28.57,
  "recent_drawdown_pct": 3.1,
  "purpose": "long_term",
  "scenario": {
    "scenario": "gain_protection",
    "label_zh": "浮盈怕坐电梯",
    "label_en": "Gain Protection",
    "reason_zh": "已浮盈 28.6%，需要保护已实现收益。",
    "reason_en": "Up 28.6% on cost — protect unrealized gains.",
    "unrealized_pnl_pct": 28.57
  },
  "recommendations": [
    {
      "type": "collar",
      "priority": 1,
      "title_zh": "Collar 95/110 锁定收益",
      "title_en": "Collar 95/110 lock-in",
      "resolved": {
        "long_put_strike": 170.0,
        "short_call_strike": 200.0,
        "put_cost": 2.15,
        "call_credit": 2.45,
        "net_cost_per_share": -0.30,
        "net_cost_per_contract": -30,
        "is_credit": true,
        "dte": 62
      }
    }
  ],
  "position_rules": [
    {"rule_zh": "单票仓位 ≤ 20%", "rule_en": "Single ticker ≤20%"}
  ]
}
```

定价：每次1次期权分析额度；每（股票，成本价，持仓目的）组合5分钟缓存。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 超出预设方案的自定义对冲多腿策略构建器 |
| [alphagbm-greeks](../alphagbm-greeks/) | 对冲仓位的希腊字母 |
| [alphagbm-pnl-simulator](../alphagbm-pnl-simulator/) | 在不同未来价格下压力测试对冲效果 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
