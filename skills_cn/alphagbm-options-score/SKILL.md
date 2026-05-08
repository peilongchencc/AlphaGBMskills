---
name: alphagbm-options-score
description: >
  使用 AlphaGBM 多因子评分模型（流动性、IV 吸引力、希腊字母均衡、风险/收益）
  对任意股票的期权合约进行评分和排名。返回标注最优合约的期权链评分。
  适用场景：评估选哪个期权交易、寻找最佳行权价/到期日、按质量排名期权。
  触发关键词："AAPL 期权评分"、"NVDA 最佳期权"、"TSLA 应该买哪个 Call"、
  "SPY 期权链"、"META Put 排名"。
globs:
  - "mock-data/*.json"
---

# AlphaGBM 期权评分

## 前置条件

- **API Key**：设置环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx...`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。

## 功能说明

使用跨4种策略类型的**多因子模型**对期权链中的每个合约评分，
让你即刻知道哪些合约具有最佳风险/收益特征。

### 策略评分模型

#### 卖 Put 权重

| 因子 | 权重 | 说明 |
|------|------|------|
| premium_yield（权利金收益率）| 20% | 权利金的年化回报 |
| support_strength（支撑强度）| 20% | 与关键支撑位的接近程度 |
| safety_margin（安全边际）| 15% | ATR 调整后的虚值缓冲 |
| trend_alignment（趋势匹配）| 15% | 下跌趋势=100，上涨趋势=30 |
| probability_profit（盈利概率）| 15% | 到期时虚值的 BS 概率 |
| liquidity（流动性）| 10% | 成交量 + 持仓量 + 买卖价差 |
| time_decay（时间价值）| 5% | 20-45 DTE 最优 |

#### 卖 Call 权重

| 因子 | 权重 |
|------|------|
| premium_yield | 20% |
| resistance_strength（阻力强度）| 20% |
| trend_alignment | 15% |
| upside_buffer（上行缓冲）| 15% |
| liquidity | 10% |
| is_covered（是否有持仓覆盖）| 10% |
| time_decay | 5% |
| overvaluation（高估程度）| 5% |

#### 买 Call 权重

| 因子 | 权重 |
|------|------|
| bullish_momentum（看涨动量）| 25% |
| breakout_potential（突破潜力）| 20% |
| value_efficiency（性价比）| 20% |
| volatility_timing（波动率时机）| 15% |
| liquidity | 10% |
| time_optimization（时间优化）| 10% |

#### 买 Put 权重

| 因子 | 权重 |
|------|------|
| bearish_momentum（看跌动量）| 25% |
| support_break（支撑突破）| 20% |
| value_efficiency | 20% |
| volatility_expansion（波动率扩张）| 15% |
| liquidity | 10% |
| time_value（时间价值）| 10% |

### 分数区间

- **80-100**：顶级机会
- **60-79**：良好交易候选
- **40-59**：一般，谨慎操作
- **0-39**：较差，避免（除非对冲需要）

### 风险收益特征

| 风格 | 典型胜率 | 典型回报 |
|------|----------|----------|
| steady_income（稳定收入）| 65-80% | 每月 1-5% |
| balanced（均衡）| 40-55% | 50-200% |
| high_risk_high_reward（高风险高回报）| 20-40% | 2-10倍 |
| hedge（对冲）| 30-50% | 0-1倍 |

## API 端点

### 获取到期日列表

```
GET /api/options/expirations/<SYMBOL>
```

### 期权链分析 — 同步

```
POST /api/options/chain-sync
Content-Type: application/json

{"symbol": "AAPL", "expiry_date": "2026-04-17"}
```

添加 `?compact=true` 获取精简响应。

响应包含4种策略（卖Put、卖Call、买Call、买Put）中每种的：
- 按评分降序排列的前10个推荐（0-100分）
- 评分分解：权利金收益率、支撑/阻力强度、安全边际、趋势匹配、盈利概率、流动性、时间价值
- ATR 安全信息（safety_ratio、atr_multiples、is_safe）
- 风险收益特征：风格、风险等级、胜率
- 趋势分析：方向、强度、匹配分数

### 期权链分析 — 异步

```
POST /api/options/chain-async
Content-Type: application/json

{"symbol": "TSLA", "expiry_date": "2026-04-17"}
```

返回 `{"task_id": "uuid"}`。轮询：`GET /api/tasks/<task_id>`。

### 单期权增强分析 — 同步

```
POST /api/options/enhanced-sync
Content-Type: application/json

{"symbol": "AAPL", "option_identifier": "AAPL260417C00190000"}
```

### 单期权增强分析 — 异步

```
POST /api/options/enhanced-async
Content-Type: application/json

{"symbol": "AAPL", "option_identifier": "AAPL260417C00190000"}
```

### 反向评分

根据已知参数对特定合约评分：

```
POST /api/options/reverse-score
Content-Type: application/json

{"symbol": "AAPL", "option_type": "CALL", "strike": 190, "expiry_date": "2026-02-16", "option_price": 2.50, "implied_volatility": 28}
```

### 批量期权链分析

```
POST /api/options/chain/batch
Content-Type: application/json

{"symbols": ["AAPL", "NVDA"], "expiries": ["2026-04-17", "2026-05-15"]}
```

每次请求最多 3 只股票 × 2 个到期日。

### IV 快照（即时，无额度消耗）

```
GET /api/options/snapshot/<SYMBOL>
```

返回：平值IV、IV Rank、30日历史波动率、VRP、VRP等级。

### 每日推荐（无需认证）

```
GET /api/options/recommendations?count=5
```

## 典型工作流

1. **获取到期日**：`GET /api/options/expirations/AAPL`
2. **IV 快速检查**：`GET /api/options/snapshot/AAPL`（免费，无额度）
3. **运行链分析**：`POST /api/options/chain-sync`（股票 + 到期日）
4. **深入特定合约**：`POST /api/options/enhanced-sync`（期权标识符）
5. **跨标的对比**：`POST /api/options/chain/batch`（多股票分析）

## 额度

- **免费**：每天 1 次期权分析
- **Plus**：每月 1,000 次
- **Pro**：每月 5,000 次
- 快照和推荐端点免费

## 输出格式建议

- 评分0-100，按评分降序排列展示前几名。
- 始终展示评分分解因子，让用户理解合约高分的原因。
- 对于卖方策略，突出显示 ATR 安全信息（is_safe 标志）。
- 包含风险收益风格标签（稳定收入、均衡等）以便快速定位。

### 示例问法

| 用户提问 | 处理结果 |
|----------|----------|
| "AAPL 期权评分" | 完整链评分，突出显示前几名 |
| "NVDA 最好的 Call" | 过滤为 Call，按评分降序 |
| "TSLA 下周五的 Put" | 按到期日 + 类型过滤 |
| "SPY 哪个期权风险收益最好？" | 按 risk_reward 因子排序 |

### 模拟数据

无 API Key 时可用演示股票：AAPL、NVDA、SPY、TSLA、META。使用 `mock-data/` 中的真实期权链快照。

### 相关 Skills
- **alphagbm-stock-analysis** — 先分析标的股票
- **alphagbm-options-strategy** — 用高评分合约构建多腿策略
- **alphagbm-greeks** — 深入分析特定合约的希腊字母
- **alphagbm-vol-surface** — 查看 IV 跨行权价是否偏贵或便宜

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
