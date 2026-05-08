---
name: alphagbm-pnl-simulator
description: >
  任意单腿或多腿期权仓位的盈亏模拟引擎。生成到期盈亏图、随时间的盈亏曲线、
  假设情景（价格、IV、时间）、盈亏平衡分析和概率分布。
  适用场景：测试交易想法、可视化风险/收益、运行假设情景、检查盈亏平衡点、
  压力测试仓位。
  触发关键词："模拟 AAPL 牛市 Call 价差盈亏"、"如果 NVDA 跌 10% 怎样"、
  "盈亏图"、"测试我的铁鹰"、"盈亏平衡分析"、"压力测试我的仓位"、
  "到期时会怎样"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM 盈亏模拟器

## 前置条件

- **API Key**：设置环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx...`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。

## 功能说明

在多个维度上模拟任意期权仓位的**盈亏**，包括标的价格、隐含波动率和到期时间。
生成盈亏图、盈亏平衡分析和概率加权结果分布。

### 四种核心策略背景

| 策略 | 理想趋势 | 最大盈利 | 最大亏损 |
|------|----------|----------|----------|
| **卖 Put** | 中性 / 看涨 | 收到权利金 | 行权价 - 权利金 |
| **卖 Call** | 中性 / 看跌 | 收到权利金 | 无限（裸空）|
| **买 Call** | 看涨 | 无限 | 支付的权利金 |
| **买 Put** | 看跌 | 行权价 - 权利金 | 支付的权利金 |

### 模拟能力

| 能力 | 说明 |
|------|------|
| **到期盈亏** | 经典盈亏图，到期时盈亏 vs 标的价格 |
| **随时间盈亏** | 仓位价值从现在到到期日的演变（时间序列曲线）|
| **假设情景：价格** | 标的价格按固定金额或百分比变化，查看对盈亏的影响 |
| **假设情景：IV** | 隐含波动率变化，查看 IV 崩塌或飙升如何影响仓位 |
| **假设情景：时间** | 快进到特定日期，查看 Theta 衰减影响 |
| **概率分布** | 蒙特卡洛模拟盈亏结果及盈利概率 |
| **盈亏平衡分析** | 精确盈亏平衡点及到期前随时间变化的盈亏平衡 |

### 支持的仓位类型
- 单腿（Long Call、Long Put、Short Call、Short Put）
- 双腿价差（垂直价差、日历价差、对角价差）
- 三腿组合（蝴蝶价差、比例价差）
- 四腿组合（铁鹰、铁蝶、双对角）
- 任意多腿自定义仓位

## API 端点

### 盈亏模拟器

```
POST /api/options/tools/simulate
Content-Type: application/json

{
  "symbol": "AAPL",
  "spot": 150.0,
  "legs": [
    {"action": "buy", "option_type": "call", "strike": 145, "expiry_days": 30, "iv": 0.26},
    {"action": "sell", "option_type": "call", "strike": 150, "expiry_days": 30, "iv": 0.25}
  ]
}
```

参数：
- **symbol**（必填）：股票代码
- **spot**（必填）：标的当前价格
- **legs**（必填）：期权腿数组，每条腿包含：
  - **action**：`"buy"` 或 `"sell"`
  - **option_type**：`"call"` 或 `"put"`
  - **strike**：行权价
  - **expiry_days**：到期天数
  - **iv**：隐含波动率（小数，如0.26表示26%）

## 使用方法

### 输入
- **必填**：仓位定义（含行权价、到期日、类型、数量、入场价的腿）
- **可选**：情景参数（价格区间、IV 变化、目标日期）、蒙特卡洛路径数量

### 输出结构

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "position": {
    "strategy": "Bull Call Spread",
    "legs": [
      {"action": "buy", "type": "call", "strike": 215, "expiry": "2026-04-18", "price": 7.20, "qty": 1},
      {"action": "sell", "type": "call", "strike": 225, "expiry": "2026-04-18", "price": 3.40, "qty": 1}
    ],
    "net_debit": 380
  },
  "pnl_at_expiry": {
    "price_axis": [195, 200, 205, 210, 215, 218.8, 220, 225, 230, 235],
    "pnl_axis":   [-380, -380, -380, -380, -380, 0, 120, 620, 620, 620]
  },
  "pnl_over_time": {
    "dates": ["2026-03-29", "2026-04-04", "2026-04-11", "2026-04-18"],
    "curves": {
      "at_210": [-180, -220, -290, -380],
      "at_218": [50, 30, 10, -20],
      "at_225": [320, 400, 510, 620]
    }
  },
  "breakevens": [218.80],
  "max_profit": 620,
  "max_loss": 380,
  "risk_reward_ratio": 1.63,
  "probability_of_profit": 0.56,
  "expected_value": 42.50,
  "scenarios": {
    "price_down_10pct": {"pnl": -380, "pnl_pct": -100},
    "price_up_10pct": {"pnl": 620, "pnl_pct": 163},
    "iv_crush_50pct": {"pnl": -85, "note": "IV 下降对 Long Spread 略有负面影响"},
    "iv_spike_50pct": {"pnl": 120, "note": "IV 上升对 Long Spread 略有正面影响"}
  }
}
```

### 示例问法

| 用户提问 | 处理结果 |
|----------|----------|
| "模拟 AAPL 牛市 Call 价差盈亏" | 到期完整盈亏图 + 随时间曲线 |
| "如果 NVDA 跌 10% 怎样？" | 当前仓位的价格情景分析 |
| "盈亏图" | 任意已定义仓位的到期盈亏图 |
| "测试我的铁鹰" | 含盈亏平衡、最大盈亏、盈利概率的完整模拟 |
| "分析我的价差盈亏平衡" | 精确盈亏平衡点 + 随时间变化的盈亏平衡 |
| "压力测试：IV 翻倍会怎样？" | IV 冲击情景及盈亏影响 |
| "我的跨式蒙特卡洛" | 10,000路径模拟及结果分布 |

### 模拟数据

无 API Key 时可用演示股票：AAPL、NVDA、SPY、TSLA、META。模拟使用校准自 `mock-data/` 快照的真实定价模型。

### 相关 Skills
- **alphagbm-options-strategy** — 先获取策略推荐，再在此模拟
- **alphagbm-greeks** — 了解驱动盈亏变化的希腊字母
- **alphagbm-iv-rank** — 判断 IV 情景是否合理
- **alphagbm-vol-surface** — 校准模拟用的完整 IV 图

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
