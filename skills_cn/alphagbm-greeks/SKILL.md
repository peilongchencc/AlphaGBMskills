---
name: alphagbm-greeks
description: >
  任意期权合约或多腿组合的希腊字母仪表盘。涵盖一阶希腊字母（Delta、Gamma、Theta、
  Vega、Rho）和二阶希腊字母（Charm、Vanna、Volga）。返回单合约和组合层面的希腊字母
  以及情景热力图。适用场景：检查期权敏感性、管理仓位风险、分析时间衰减、
  分析Gamma敞口、对冲组合。
  触发关键词："AAPL 220 Call 的希腊字母"、"仓位希腊字母"、"Theta 衰减分析"、
  "NVDA Gamma 敞口"、"我的仓位 Delta"、"SPY 跨式 Vega 风险"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM 希腊字母

## 前置条件

- **API Key**：设置环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx...`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。

## 功能说明

为任意单一期权合约或多腿组合提供完整的**希腊字母仪表盘**。计算一阶和二阶敏感性，
并生成情景热力图，展示随价格和 IV 变化时希腊字母如何演变。

### 覆盖的希腊字母

| 希腊字母 | 阶数 | 衡量内容 |
|----------|------|----------|
| **Delta** | 一阶 | 价格敏感性，标的每涨 $1 期权价格变动多少 |
| **Gamma** | 一阶 | Delta 敏感性，Delta 变化的速度（加速度）|
| **Theta** | 一阶 | 时间衰减，期权每天损耗多少价值 |
| **Vega** | 一阶 | IV 敏感性，IV 每变动1% 期权价格变动多少 |
| **Rho** | 一阶 | 利率敏感性，利率每变动1% 期权价格变动多少 |
| **Charm** | 二阶 | Delta 衰减，Delta 随时间的变化速度（Delta-Theta交叉）|
| **Vanna** | 二阶 | Delta-波动率交叉，Delta 随 IV 变化的速度 |
| **Volga** | 二阶 | Vega 凸性，Vega 随 IV 变化的速度 |

### 组合层面分析

对于多腿组合，汇总所有腿的希腊字母并展示：
- **净希腊字母**：组合的总 Delta、Gamma、Theta、Vega
- **单位资金的希腊字母**：按保证金要求或净借方归一化
- **风险集中度**：哪条腿对每个希腊字母贡献最大

## API 端点

### 希腊字母计算器

根据基本参数计算单一期权的希腊字母：

```
POST /api/options/tools/greeks
Content-Type: application/json

{
  "spot": 150,
  "strike": 155,
  "expiry_days": 30,
  "iv": 0.25,
  "option_type": "call"
}
```

参数：
- **spot**（必填）：标的当前价格
- **strike**（必填）：期权行权价
- **expiry_days**（必填）：到期天数
- **iv**（必填）：隐含波动率（小数，如0.25表示25%）
- **option_type**（必填）：`"call"` 或 `"put"`

### 隐含波动率计算器

根据市场价格反推 IV：

```
POST /api/options/tools/implied-volatility
Content-Type: application/json

{
  "market_price": 4.50,
  "spot": 150,
  "strike": 155,
  "expiry_days": 30,
  "option_type": "call"
}
```

参数：
- **market_price**（必填）：期权当前市场价格
- **spot**（必填）：标的当前价格
- **strike**（必填）：期权行权价
- **expiry_days**（必填）：到期天数
- **option_type**（必填）：`"call"` 或 `"put"`

## 使用方法

### 输入
- **必填**：股票 + 行权价 + 到期日 + 类型（单合约），或仓位定义（腿的列表）
- **可选**：标的价格覆盖、IV 覆盖、日期覆盖（前瞻性分析）

### 输出结构

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "position": [
    {
      "leg": "AAPL 2026-04-18 220C",
      "quantity": 1,
      "greeks": {
        "delta": 0.52,
        "gamma": 0.035,
        "theta": -0.18,
        "vega": 0.32,
        "rho": 0.08,
        "charm": -0.003,
        "vanna": 0.012,
        "volga": 0.005
      }
    }
  ],
  "net_greeks": {
    "delta": 0.52,
    "gamma": 0.035,
    "theta": -0.18,
    "vega": 0.32,
    "rho": 0.08
  },
  "heatmap": {
    "price_axis": [200, 205, 210, 215, 220, 225, 230, 235],
    "iv_axis": [20, 25, 30, 35, 40],
    "delta_grid": ["..."],
    "pnl_grid": "..."
  },
  "insights": [
    "净多 Delta（0.52）— 股价上涨时盈利",
    "Theta 为 -0.18，每合约每天时间价值损耗约 $18",
    "Gamma 为 0.035，股价每移动 $1，Delta 变化约 3.5"
  ]
}
```

### 示例问法

| 用户提问 | 处理结果 |
|----------|----------|
| "AAPL 220 Call 的希腊字母" | 单合约完整希腊字母 + 情景热力图 |
| "仓位希腊字母" | 之前定义的多腿仓位的汇总希腊字母 |
| "NVDA Theta 衰减分析" | Theta 随时间变化图（临近到期时加速）|
| "NVDA Gamma 敞口" | 跨行权价的 Gamma，突出 Gamma 风险区 |
| "我的铁鹰 Delta" | 全部4条腿的净 Delta + 逐腿分解 |
| "IV 飙升时 Vega 如何变化？" | Volga 分析，Vega 的二阶敏感性 |

### 模拟数据

无 API Key 时可用演示股票：AAPL、NVDA、SPY、TSLA、META。希腊字母基于 `mock-data/` 中的真实期权链快照计算。

### 相关 Skills
- **alphagbm-options-score** — 希腊字母均衡是合约质量的评分因子
- **alphagbm-pnl-simulator** — 可视化希腊字母如何转化为实际盈亏
- **alphagbm-options-strategy** — 查看推荐策略的净希腊字母
- **alphagbm-vol-surface** — 了解驱动 Vega 和 Vanna 的 IV 输入

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
