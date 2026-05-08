---
name: alphagbm-stock-analysis
description: >
  基于 AlphaGBM 五维框架（基本面、技术面、情绪、资金流、估值）并结合真实市场数据
  的 AI 股票分析。返回1-10综合评分及可操作信号。适用场景：分析任意股票代码、评估买卖
  决策、对比股票基本面、评估风险水平。
  触发关键词："分析 AAPL"、"NVDA 怎么看"、"TSLA 值得买吗"、"META 股票分析"、
  "SPY 是否高估"、"GOOGL 风险评估"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM 股票分析

通过 AlphaGBM API 分析股票，采用 G = B + M（收益 = 基本面 + 动量）模型，
综合基本面分析、市场情绪、期望值模型、ATR 止损、板块轮动和 AI 报告。

## 适用场景

- 用户要求分析某只股票（美股 / 港股 / A 股）
- 用户询问股价、目标价、风险评分或 EV 推荐
- 用户提到 AlphaGBM 或想要综合股票分析

## 前置条件

- **API Key**：存储在环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx…`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。
- 如果用户没有 API Key，请引导其在 <https://alphagbm.com> 注册，并在 `/api-keys` 创建密钥。

## API 端点

所有端点均需要 `Authorization: Bearer $ALPHAGBM_API_KEY`。

### 1. 快速行情（即时，无额度消耗）

```
GET /api/stock/quick-quote/<TICKER>
```

返回：价格、涨跌幅、PE、远期PE、52周区间、板块、市值。

### 2. 完整股票分析 — 同步（阻塞10-30秒）

```
POST /api/stock/analyze-sync
Content-Type: application/json

{"ticker": "AAPL", "style": "balanced"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ticker` | string | 是 | 股票代码（如 `AAPL`、`0700.HK`、`600519.SS`）|
| `style` | string | 否 | `quality`（默认）、`value`、`growth`、`momentum`、`balanced` |

添加 `?compact=true` 获取对 AI 友好的精简响应（约500 token）。

**响应包含：**
- `data` — 价格、PE、PEG、增长率、利润率、目标价、止损价、市场情绪(0-10)、EV 模型、板块分析、资金分析
- `risk` — 评分(0-10)、风险等级、建议仓位%、风险标志
- `report` — AI 生成的叙事报告（Markdown，约2000字符）

### 3. 完整股票分析 — 异步（适用于 Web 前端）

```
POST /api/stock/analyze-async
Content-Type: application/json

{"ticker": "TSLA", "style": "growth"}
```

返回 `{"task_id": "uuid"}`。轮询任务状态：

```
GET /api/tasks/<task_id>
```

### 4. 股票搜索（无需认证）

```
GET /api/stock/search?q=AAPL&limit=8
```

模糊搜索，支持美股（`AAPL`）、港股（`700`、`0700.HK`）、A股（`600519`）。

### 5. 分析历史记录

```
GET /api/stock/history?page=1&per_page=10&ticker=AAPL
```

### 6. 股票摘要（用于期权页面联动）

```
GET /api/stock/summary/<TICKER>
```

返回精简分析。每只股票第一次分析免费。

## 分析模型说明

### G = B + M

| 维度 | 组成要素 | 权重 |
|------|----------|------|
| **B（基本面）** | PE/PEG、增长率、利润率、ROE、自由现金流 | 基本面估值 |
| **M（动量）** | VIX、技术指标、资金流、宏观 | 市场情绪 0-10 |

### 风险评分（0-10，累加制）

| 因子 | 触发条件 | 加分 |
|------|----------|------|
| 估值 | PE > 60 | +2.0 |
| 增长 | 增长率 < -10% | +2.0 |
| 流动性 | 成交量低于阈值 | +2.0 |
| 市场 | VIX > 30 | +1.5 |
| 技术面 | 股价 < 200日均线 | +1.0 |

风险 0-2 → 最大仓位 20%；风险 8-10 → 不要买入。

### 期望值（EV）模型

```
EV = (上涨概率 × 上涨幅度) + (下跌概率 × 下跌幅度)
加权 = 50% × 1周 + 30% × 1月 + 20% × 3月
```

| EV | 推荐 |
|----|------|
| > +8% | STRONG_BUY（强烈买入）|
| +3% ~ +8% | BUY（买入）|
| -3% ~ +3% | HOLD（持有）|
| < -8% | STRONG_AVOID（强烈回避）|

### 目标价 — 5种方法，行业加权

PE 估值 · PEG 估值 · 增长折现 · DCF · 技术分析。
风险调整：高风险 → -15%，中等风险 → -8%。

### ATR 止损

```
止损价 = 当前价 - ATR(14) × 乘数(1.5-4.0)
```
乘数根据 Beta 和 VIX 调整。硬性底线：-15%。

## 典型工作流

```
1. 快速查看 → GET /api/stock/quick-quote/NVDA
2. 如果感兴趣 → POST /api/stock/analyze-sync {"ticker":"NVDA","style":"growth"}
3. 展示：推荐评级、目标价、风险评分、EV、AI 报告
```

## 额度

- 免费用户：每天 2 次股票分析
- Plus：每月 1000 次；Pro：每月 5000 次
- 快速行情免费

## 输出格式建议

向用户展示结果时，重点突出：
1. **推荐评级**（STRONG_BUY / BUY / HOLD / AVOID / STRONG_AVOID）+ 置信度
2. **目标价** vs 当前价 → 上涨空间
3. **风险评分** + 等级 + 主要风险标志
4. **止损价** + 计算方法
5. **EV 分数** + 加权 EV%
6. **AI 报告**关键摘录（前2-3段）

## 模拟数据

未配置 API Key 时，使用内置市场数据快照 `mock-data/`。支持演示股票：AAPL、NVDA、SPY、TSLA、META。

## 相关 Skills

- **alphagbm-options-score** — 股票分析完成后，评估期权机会
- **alphagbm-compare** — 多只股票横向对比
- **alphagbm-market-sentiment** — 分析的宏观市场背景

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
