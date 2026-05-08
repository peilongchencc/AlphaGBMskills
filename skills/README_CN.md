# AlphaGBM Skills 中文说明

> 本文档是 `skills/` 目录下所有 Skill 的中文速查手册，帮助你快速了解每个 Skill 的用途和触发时机。

---

## 目录

| Skill 名称 | 一句话功能 |
|---|---|
| [alphagbm-vix-status](#1-alphagbm-vix-status) | VIX 恐慌指数 + 五档分类 + 卖方策略建议 |
| [alphagbm-market-sentiment](#2-alphagbm-market-sentiment) | 全市场情绪仪表盘（VIX / PCR / 市场广度 / 板块轮动）|
| [alphagbm-stock-analysis](#3-alphagbm-stock-analysis) | 单股五维深度分析（基本面 / 技术 / 情绪 / 资金流 / 估值）|
| [alphagbm-options-score](#4-alphagbm-options-score) | 对期权合约逐一打分，找出最优行权价 / 到期日 |
| [alphagbm-options-strategy](#5-alphagbm-options-strategy) | 根据市场观点推荐最适合的多腿期权策略 |
| [alphagbm-fear-score](#6-alphagbm-fear-score) | 每只股票的恐慌指数（0-100），≥60 触发 BPS 入场信号 |
| [alphagbm-iv-rank](#7-alphagbm-iv-rank) | IV Rank / IV 百分位，判断隐含波动率是贵还是便宜 |
| [alphagbm-vol-surface](#8-alphagbm-vol-surface) | 3D 波动率曲面（行权价 × 到期日），识别定价异常 |
| [alphagbm-vol-smile](#9-alphagbm-vol-smile) | 单个到期日的波动率微笑 / 偏斜分析 |
| [alphagbm-greeks](#10-alphagbm-greeks) | 希腊字母仪表盘（一阶 + 二阶），支持多腿组合 |
| [alphagbm-pnl-simulator](#11-alphagbm-pnl-simulator) | 期权仓位盈亏模拟器（到期图 / 时间衰减 / 假设情景）|
| [alphagbm-bps-backtest](#12-alphagbm-bps-backtest) | 牛市价差（BPS）策略回测，信号版 vs 无信号对照组 |
| [alphagbm-earnings-crush](#13-alphagbm-earnings-crush) | 财报前后 IV Crush 分析 + 铁鹰策略报价 |
| [alphagbm-duan-analysis](#14-alphagbm-duan-analysis) | 段永平风格卖方分析（卖 Put / Covered Call / 极度恐慌抄底）|
| [alphagbm-hedge-advisor](#15-alphagbm-hedge-advisor) | 持仓对冲顾问（自动识别场景，给出 Long Put / Collar 报价）|
| [alphagbm-take-profit](#16-alphagbm-take-profit) | 量化止盈策略实验室（过山车率 + 15 种退出策略回测）|
| [alphagbm-unusual-activity](#17-alphagbm-unusual-activity) | 异常期权活动监测（大宗交易 / 扫单 / 净权利金流向）|
| [alphagbm-watchlist](#18-alphagbm-watchlist) | 自选股看板（价格异动 / IV 变化 / 异常活动 / 财报预警）|
| [alphagbm-alert](#19-alphagbm-alert) | 设置价格 / IV / 异常活动等智能提醒 |
| [alphagbm-compare](#20-alphagbm-compare) | 2-5 只股票或期权多维横向对比，找出最优标的 |
| [alphagbm-macro-view](#21-alphagbm-macro-view) | 宏观指标追踪（VIX / 美债 / 美元 / 黄金 / 油价…）|
| [alphagbm-polymarket](#22-alphagbm-polymarket) | 预测市场（Polymarket）概率 vs 期权隐含概率套利信号 |
| [alphagbm-company-profile](#23-alphagbm-company-profile) | 建立并管理公司研究档案（PE/PB 历史区间 / 财务红旗）|
| [alphagbm-investment-thesis](#24-alphagbm-investment-thesis) | 记录「买入理由 + 卖出条件」，系统自动监控触发 |
| [alphagbm-theme-research](#25-alphagbm-theme-research) | 投资主题篮子管理（AI基建 / 港股高息 / 新能源…）|
| [alphagbm-health-check](#26-alphagbm-health-check) | 研究知识库健康诊断（过期档案 / 论据偏离 / 孤立主题）|

---

## 详细说明

---

### 1. alphagbm-vix-status

**功能：** 把 VIX 单一数字翻译成五档策略区间，告诉你现在适不适合卖权利金。

| 档位 | VIX 区间 | 颜色 | 卖方建议 |
|---|---|---|---|
| Calm 平静 | < 15 | 🔵 蓝 | 权利金太薄，**便宜买保护**（Long Put）|
| Normal 正常 | 15-20 | 🟢 绿 | 日常卖 Put / BPS 例行操作 |
| 卖方甜蜜区 | 20-25 | 🟡 黄 | BPS 权利金变肥，**积极开仓** |
| Caution 谨慎 | 25-35 | 🟠 橙 | 可做但**减半仓位**，VIX 爆炸风险 |
| Extreme Fear 极度恐慌 | ≥ 35 | 🔴 红 | 散户卖方最容易被埋，**只买股不卖期权** |

**还会返回：** 1年均值、百分位、每档占比分布。

**典型问法：**
- "VIX 现在多少" / "现在适合卖 BPS 吗" / "市场恐慌指数怎么样"

**API：** `GET /api/options/vix-status`（免费，5分钟缓存）

---

### 2. alphagbm-market-sentiment

**功能：** 全市场情绪仪表盘，综合多个指标给出当前是「风险偏好」还是「避险」模式。

**包含指标：**
- VIX 水平 + 百分位
- Put/Call Ratio（看跌/看涨比率）
- 恐惧贪婪指数（0-100）
- 市场广度（涨跌比、新高/新低数量）
- 板块轮动阶段（经济周期定位）

**输出：** 整体判定为 risk-on（风险偏好）/ risk-off（避险）/ neutral（中性）+ 置信度。

**典型问法：**
- "现在市场情绪怎么样" / "市场是贪婪还是恐惧" / "哪个板块在领涨"

**API：** `GET /api/analytics/market-sentiment`

---

### 3. alphagbm-stock-analysis

**功能：** 基于 AlphaGBM 五维模型（G = B + M）对单只股票做深度分析，给出评级 + 目标价 + 止损价 + 风险评分。

**核心模型：**
- **B（基本面）：** PE/PEG、增长率、利润率、ROE、自由现金流
- **M（动量）：** VIX、技术指标、资金流、宏观背景

**输出亮点：**
- 推荐（STRONG_BUY / BUY / HOLD / AVOID / STRONG_AVOID）
- 目标价（5种估值方法加权）
- ATR 止损价（动态调整）
- 期望值模型（EV）：加权1周+1月+3月胜率

**典型问法：**
- "分析一下 NVDA" / "AAPL 现在值不值得买" / "TSLA 的风险评分"

**API：** `POST /api/stock/analyze-sync`（同步），`POST /api/stock/analyze-async`（异步）

**免费额度：** 每天 2 次；Plus 1000次/月；Pro 5000次/月

---

### 4. alphagbm-options-score

**功能：** 对期权链中每一个合约打分（0-100），按四种策略分别给出最优推荐合约。

**四种策略评分因子：**
- **卖 Put：** 权利金收益率(20%) + 支撑强度(20%) + 安全边际(15%) + 趋势匹配(15%) + 盈利概率(15%) + 流动性(10%) + 时间价值(5%)
- **卖 Call / 买 Call / 买 Put：** 各有对应权重体系

**分数区间含义：**
- 80-100：顶级机会
- 60-79：良好候选
- 40-59：一般，谨慎操作
- 0-39：差，避免（除非对冲需要）

**典型问法：**
- "AAPL 期权怎么打分" / "NVDA 最好的 Call 是哪个" / "帮我找 SPY 最佳性价比期权"

**API：** `POST /api/options/chain-sync`，`GET /api/options/snapshot/<SYMBOL>`（免费快照）

---

### 5. alphagbm-options-strategy

**功能：** 根据你对市场的方向判断（看涨/看跌/中性/波动），推荐最合适的多腿期权策略，自动选择最优行权价和到期日。

**支持 15+ 策略模板：**
- 看涨：牛市价差、Bull Put Spread、Long Call、Covered Call...
- 看跌：Bear Put Spread、Long Put...
- 中性：铁鹰、铁蝶、Short Straddle...
- 波动：Long Straddle、Long Strangle...
- 收入：Covered Call、CSP（现金担保卖 Put）、Collar...

**典型问法：**
- "AAPL 有什么期权策略" / "TSLA 财报怎么玩" / "SPY 铁鹰策略" / "NVDA 看涨策略"

**API：** `GET /api/options/tools/strategy/templates`，`POST /api/options/tools/strategy/build`

---

### 6. alphagbm-fear-score

**功能：** 对每只股票计算一个恐慌指数（0-100），由6个信号加权合成。**≥ 60 触发 BPS（牛市价差）入场信号。**

**6个信号权重：**
| 指标 | 权重 |
|---|---|
| VIX 水平 | 20% |
| IV Rank（最重要）| 25% |
| RSI-14 超卖程度 | 15% |
| 成交量异常 | 15% |
| Put/Call 比率 | 15% |
| 连续下跌天数 | 10% |

**实测效果：** 146 笔 BPS 交易数据中，FearScore ≥ 60 入场年化收益约 10.8%，无信号入场约 3.5%，**约 3 倍 Alpha 提升**。

**典型问法：**
- "QQQ 的恐慌指数是多少" / "NVDA 超卖了吗" / "现在是卖 Put 的好时机吗"

**API：** `GET /api/options/fear-score?ticker={SYMBOL}`（1次期权分析额度，5分钟缓存）

---

### 7. alphagbm-iv-rank

**功能：** 计算 IV Rank 和 IV 百分位，告诉你当前隐含波动率相对历史是高还是低，以及应该买权利金还是卖权利金。

**核心指标：**
- **IV Rank**：(当前IV - 52周低点) / (52周高点 - 52周低点) × 100
- **IV 百分位**：过去252天中IV低于今天的比例
- **VRP（波动率风险溢价）**：隐含波动率 - 历史波动率，正值有利于卖方

**信号解读：**
| IV Rank | 区间 | 含义 | 建议 |
|---|---|---|---|
| 80-100 | 极高 | 期权很贵 | 卖权利金（Short Strangle / Iron Condor）|
| 60-80 | 偏高 | 期权偏贵 | 偏向卖方，Covered Call 机会 |
| 40-60 | 中等 | 不贵不便宜 | 看方向决定 |
| 20-40 | 偏低 | 期权便宜 | 偏向买方，Debit Spread |
| 0-20 | 极低 | 期权很便宜 | 买权利金（Long Straddle / Calendar）|

**典型问法：**
- "AAPL IV Rank 是多少" / "NVDA 隐含波动率贵不贵" / "现在 SPY 适合卖 Put 吗"

**API：** `GET /api/options/snapshot/<SYMBOL>`（免费，无额度消耗）

---

### 8. alphagbm-vol-surface

**功能：** 构建3D波动率曲面（行权价 × 到期日 × IV），找出定价偏离点（潜在错误定价机会）。

**核心输出：**
- **曲面网格：** 每个（行权价，到期日）坐标的IV值
- **ATM 期限结构：** 平值期权跨不同到期日的IV变化
- **各到期日偏斜：** Put/Call IV 差值
- **形态分类：** 正价差 / 反价差 / 平坦 / 事件驱动

**曲面形态含义：**
- **正价差（Contango）**：近月IV < 远月IV → 正常市场，近期无恐慌
- **反价差（Backwardation）**：近月IV > 远月IV → 近期有重要事件（财报/FDA等）
- **陡峭偏斜：** 市场在给 Put 定极端风险溢价，对冲需求强

**典型问法：**
- "AAPL 波动率曲面" / "NVDA IV 贵不贵" / "SPY 期限结构"

**API：** `GET /api/options/tools/vol-surface/<SYMBOL>`

---

### 9. alphagbm-vol-smile

**功能：** 单个到期日的波动率微笑/偏斜分析，揭示市场对方向性风险和尾部风险的定价。

**核心指标：**
- **微笑曲线：** 每个行权价对应的IV
- **25-Delta 偏斜：** IV(25d put) - IV(25d call)，标准方向偏斜度量
- **Risk Reversal：** 25d Call 与 25d Put 的价格差，可直接交易
- **形态分类：** 正常 / 平坦 / 反向 / 双翼 / 斜歪

**形态含义：**
| 形态 | 含义 | 交易思路 |
|---|---|---|
| Normal（正常）| OTM Put IV > OTM Call IV | 标准对冲需求，卖 Put Spread |
| Flat（平坦）| 两边 IV 接近 | 低恐慌，中性策略（铁鹰）|
| Reverse（反向）| OTM Call IV > OTM Put IV | 上行投机 / 轧空风险，卖 Call Spread |
| Winged（双翼）| 两边 OTM IV 都高 | 预期大幅波动，卖跨式 |

**典型问法：**
- "AAPL 波动率微笑" / "NVDA 偏斜分析" / "TSLA Put 偏斜贵不贵"

**API：** `GET /api/options/tools/vol-smile/<SYMBOL>?expiry=YYYY-MM-DD`

---

### 10. alphagbm-greeks

**功能：** 单一期权合约或多腿组合的希腊字母仪表盘，支持一阶（Delta/Gamma/Theta/Vega/Rho）和二阶（Charm/Vanna/Volga）。

**希腊字母速查：**
| 希腊字母 | 阶数 | 含义 |
|---|---|---|
| Delta | 一阶 | 标的每涨 $1，期权价格变动多少 |
| Gamma | 一阶 | Delta 变化的速度（加速度）|
| Theta | 一阶 | 每天时间价值损耗多少 |
| Vega | 一阶 | IV 每变动 1%，期权价格变动多少 |
| Rho | 一阶 | 利率变动对期权价格的影响 |
| Charm | 二阶 | Delta 随时间的衰减速度 |
| Vanna | 二阶 | Delta 随 IV 变化的速度 |
| Volga | 二阶 | Vega 随 IV 变化的速度（Vega 的凸性）|

**多腿组合：** 汇总所有腿的净希腊字母，显示各腿贡献占比，并输出价格/IV 热力图。

**典型问法：**
- "AAPL 220 Call 的希腊字母" / "我的铁鹰净 Delta 是多少" / "Theta 衰减分析"

**API：** `POST /api/options/tools/greeks`，`POST /api/options/tools/implied-volatility`

---

### 11. alphagbm-pnl-simulator

**功能：** 期权仓位盈亏模拟器，支持单腿到四腿任意组合，生成到期盈亏图、时间价值衰减曲线、假设情景分析、盈亏平衡点、蒙特卡洛分布。

**模拟维度：**
- **到期盈亏图：** 标的价格 vs 到期盈亏
- **随时间盈亏：** 不同日期下的仓位价值变化曲线
- **价格假设：** 标的涨跌 X% 后的盈亏
- **IV 假设：** IV 压缩 / IV 飙升后的影响
- **时间假设：** 快进到某个日期
- **蒙特卡洛：** 1万路径模拟，输出盈利概率

**典型问法：**
- "模拟 AAPL 牛市价差的盈亏" / "如果 NVDA 跌 10% 怎么样" / "测试我的铁鹰策略" / "财报后 IV 崩塌会怎样"

**API：** `POST /api/options/tools/simulate`

---

### 12. alphagbm-bps-backtest

**功能：** 牛市价差（Bull Put Spread）策略回测，2018年至今，同时运行「有 FearScore 信号」版本和「无信号对照组」，让你量化信号是否真的产生 Alpha。

**可调参数：**
| 参数 | 默认值 | 说明 |
|---|---|---|
| 到期日目标（DTE）| 14天 | 7-45天可调 |
| Short Put Delta | 0.25 | 0.15-0.35 |
| 价差宽度 | $5 | $2-$10 |
| 止盈比例 | 50% | 达到最大盈利的50%时平仓 |
| 恐慌阈值 | 60 | FearScore ≥ X 才入场 |

**回测结果（QQQ示例）：**
- 有信号：28笔交易，年化 +10.8%，胜率 100%，最大回撤 0%
- 无信号：185笔交易，年化 +3.5%，胜率 82%，最大回撤 -8.2%

**典型问法：**
- "帮我回测 QQQ 的 BPS 策略" / "FearScore 在 SPY 上有没有用" / "什么 DTE 最适合 BPS"

**API：** `POST /api/options/bps-backtest`（1次期权分析额度，30分钟缓存）

---

### 13. alphagbm-earnings-crush

**功能：** 财报季一站式 IV 分析：历史 IV 崩塌幅度 + 隐含波动预期 + IV Rank 策略推荐 + 现成的铁鹰策略报价。

**核心概念：**
- **IV Crush（IV 崩塌）：** 财报公布后，IV 急剧下降的现象
- **隐含波动 ±X%：** 期权市场对财报涨跌幅的定价
- **策略推荐逻辑：**
  - IV Rank > 70 → 卖 IV（铁鹰 / Iron Condor）
  - IV Rank < 30 → 方向性策略（Long Call/Put）
  - 30-70 → 等待

**输出：**
- 最近8个季度：财报前IV / 财报后IV / 崩塌幅度 / 实际涨跌 / 跨式盈亏
- 铁鹰报价：4个行权价 + 信用 + 最大盈亏 + 盈亏平衡区间

**典型问法：**
- "AAPL 财报 IV 崩塌历史" / "NVDA 财报前后 IV 怎么走" / "META 财报能玩铁鹰吗"

**API：** `GET /api/options/earnings-crush/{symbol}`（1次额度，5分钟缓存）

---

### 14. alphagbm-duan-analysis

**功能：** 段永平风格卖方策略分析，专为喜欢「收租」而非投机的投资者设计。一次调用返回三块分析板：

1. **卖 Put 板：** 在你「愿意买入价格」卖 Put，收多少权利金，被行权后成本价是多少
2. **Covered Call 板：** 持有100股时，卖 ~5% 虚值 Call，收益率和潜在上限
3. **极度恐慌抄底板：** 当前 VIX 是否到了段永平说的「极度恐慌 = 极度机会」区间（VIX ≥ 35）

**使用方式：**
- 输入：`ticker`（必填）+ `buy_price`（可选，你愿意买入的价格，默认为当前价×0.95）

**典型问法：**
- "段永平风格分析 AAPL" / "卖 NVDA Put 愿意 110 元入" / "TSLA Covered Call 收益率" / "现在 VIX 到段永平抄底线了吗"

**API：** `GET /api/options/duan-analysis?ticker={SYMBOL}&buy_price={PRICE}`（1次额度，5分钟缓存）

---

### 15. alphagbm-hedge-advisor

**功能：** 基于你的持仓成本价，自动识别场景类型，给出带真实期权报价的对冲方案。

**四种场景自动识别：**
| 场景 | 触发条件 | 推荐对冲方式 |
|---|---|---|
| 接刀下落（Falling Knife）| 近期回撤 ≥ 15% 且浮盈 ≤ 5% | Long Put 5% 虚值，75天到期，100%覆盖 |
| 抄底布局（Bottom Fishing）| 浮亏/盈在 ±8% 内，刚买入 | Long Put 5% 虚值，90天到期，50-75%覆盖 |
| 保护浮盈（Gain Protection）| 浮盈 ≥ 15% | Collar（95/110）零成本或净收益 |
| 正常持仓（Normal Hold）| 以上条件均未触发 | 仓位规则建议 |

**输出：** 真实行权价 + 权利金费用 + Collar 净成本（可能为负数，即你收钱）+ 仓位管理规则。

**典型问法：**
- "帮我对冲 AAPL，成本 140 现在 180" / "刚买了 NVDA 110，要不要加保护" / "MSFT 成本 340 现在 410 怎么 Collar"

**API：** `GET /api/options/hedge-advisor?ticker={}&cost_basis={}&purpose={}`（1次额度，5分钟缓存）

---

### 16. alphagbm-take-profit

**功能：** 量化回答「这只股票能长期持有还是必须主动止盈」，核心指标是「过山车率」。

**过山车率定义：** 入场后浮盈超过 +50%，然后从最高点回撤超过 50% 才离场的概率。

**不同资产的典型过山车率：**
| 资产类型 | 过山车率 | 建议 |
|---|---|---|
| 宽基 ETF（SPY / VTI）| 0% | 长期持有即可 |
| 蓝筹（AAPL / MSFT）| 0% | 长期持有即可 |
| 大型成长股（META / AMZN）| ~47% | 建议分批止盈 |
| 高弹性成长（NVDA / TSLA）| ~85% | 必须分批止盈 |
| 加密相关（COIN / MSTR）| ~90% | 强制分批止盈 |
| 杠杆 ETF（TQQQ / SOXL）| ~97% | 结构上无法持有，必须止盈 |

**15种策略对比：** A家族（全部卖出）、B家族（分批卖出）、C（10倍梦想持有）、D（移动止损）、E（永不卖出）等。

**典型问法：**
- "TQQQ 能长期持有吗" / "NVDA 怎么止盈" / "AAPL 能一直拿吗" / "QQQ 的过山车率"

**API：** `POST /api/stock/take-profit-analyze`（首次计算约30秒；全局缓存30天，缓存命中不扣额度）

---

### 17. alphagbm-unusual-activity

**功能：** 监测异常期权活动，追踪「聪明钱」的机构资金动向。

**监测内容：**
| 概念 | 说明 |
|---|---|
| 成交量/持仓量比 | 今日成交远超持仓量，说明有新仓位建立 |
| 大宗交易（Block）| 单笔 100+ 合约的大额交易 |
| 扫单（Sweep）| 跨多个交易所快速扫单，表示资金非常着急 |
| 净权利金流向 | Call vs Put 的净美元流入，反映方向性押注 |
| 情绪分类 | 看涨扫单 / 看跌大宗 / 对冲 / 财报押注 |

**输出：** 每笔异常交易的时间、行权价、到期日、类型（Call/Put）、成交量、权利金、情绪分类；以及历史上类似信号后股价方向的准确率。

**典型问法：**
- "异常期权活动扫描" / "AAPL 聪明钱在干嘛" / "谁在买 TSLA Put" / "SPY 期权资金流"

**API：** `GET /api/options/unusual-activity/{symbol}`，`GET /api/options/unusual-activity/scan`

---

### 18. alphagbm-watchlist

**功能：** 自选股监控看板，追踪价格异动、IV 变化、异常活动、财报日期等。

**功能特点：**
- 自定义自选列表，批量添加多只股票
- 「热门期权」精选列表（系统默认推荐）
- 价格预警（跳空上涨/下跌、突破/跌破）
- IV Rank 穿越关键阈值预警（如 IV Rank 升破80）
- 异常活动浮出
- 财报临近提醒（7天内）
- 按重要程度排序的通知

**典型问法：**
- "把 AAPL 加入自选" / "我的自选股" / "有什么预警" / "删除 SPY" / "热门期权"

**API：** `GET/POST /api/user/watchlist`，`DELETE /api/user/watchlist/{symbol}`，`GET /api/analytics/hot-options`

---

### 19. alphagbm-alert

**功能：** 设置智能提醒，触发时附带完整上下文，让你可以立即行动。

**提醒类型：**
| 类型 | 说明 |
|---|---|
| IV Rank 阈值 | IV Rank 穿越指定水平时触发（如 >80 或 <20）|
| 价格水平 | 价格突破支撑/阻力或自定义价格时触发 |
| 异常活动 | 检测到异常期权流时触发 |
| 财报临近 | 财报前 N 天触发 |
| VRP 信号变化 | VRP（波动率风险溢价）翻转时触发 |
| 一次性 vs 循环 | 一次性触发后自动删除；循环提醒持续监控 |

**典型问法：**
- "AAPL IV Rank 超过 80 提醒我" / "NVDA 跌破 850 通知我" / "TSLA 财报前7天提醒" / "查看我的提醒列表"

**API：** `GET/POST /api/user/alerts`，`PUT/DELETE /api/user/alerts/{alert_id}`

---

### 20. alphagbm-compare

**功能：** 2-5 只股票或期权的全维度横向对比，识别每个维度的最优标的。

**对比维度：**
| 维度 | 对比内容 |
|---|---|
| GBM 五维评分 | 动量/价值/质量/波动率/情绪 各维度分数 |
| 期权指标 | IV Rank、IV百分位、VRP、偏斜、期限结构 |
| 技术面 | RSI、MACD、均线、支撑/阻力 |
| 估值 | P/E、P/S、EV/EBITDA、PEG 谁更便宜 |
| 各维度冠军 | 每个维度最优标的高亮显示 |
| 综合推荐 | 加权综合排名 + 核心差异分析 |

**典型问法：**
- "对比 AAPL 和 MSFT" / "NVDA 还是 AMD" / "TSLA 和 META 期权哪个更便宜" / "五只大型科技股对比"

**API：** `GET /api/analytics/compare?symbols=AAPL,MSFT,GOOGL`

---

### 21. alphagbm-macro-view

**功能：** 追踪影响你持仓的宏观变量，每个指标都附带 AI 生成的「对我的持仓具体有什么影响」分析。

**支持的宏观指标：**
| 指标代码 | 含义 | 为什么重要 |
|---|---|---|
| VIX | CBOE 恐慌指数 | 风险情绪，期权定价 |
| US10Y | 美国10年期国债收益率 | 折现率，股债轮动 |
| US2Y | 2年期美债 | 加息预期 |
| DXY | 美元指数 | 新兴市场/大宗商品/跨国企业盈利 |
| GOLD | 现货黄金 | 对冲，实际利率反向指标 |
| OIL | WTI 原油 | 通胀/能源板块 |
| BTC | 比特币 | 风险偏好，加密相关股票 |
| HKD | 港元流动性 | 港股市场流动性信号 |

**典型问法：**
- "追踪 VIX 和10年期美债" / "宏观面现在怎么样" / "高 VIX 对我的持仓有什么影响" / "停止追踪 DXY"

**API：** `GET /api/research/macro`，`POST /api/research/macro`，`DELETE /api/research/macro/<KEY>`

---

### 22. alphagbm-polymarket

**功能：** 将预测市场（Polymarket）概率与期权隐含概率对比，找出定价差异带来的套利信号。

**核心逻辑：**
- Polymarket 显示降息概率 70%，但期权只隐含 55% → 存在 15% 的概率差，可能是交易机会
- 自动扫描当前概率差最大的事件
- 给出利用这种定价差的具体期权策略

**事件类型：** 美联储会议 / 选举 / 财报 / 宏观事件等

**典型问法：**
- "扫描 Polymarket 套利信号" / "预测市场和期权对降息的概率判断有没有差异" / "选举赔率 vs 期权定价"

**API：** `GET /api/analytics/polymarket/signals`，`GET /api/analytics/polymarket/event/{event_id}`

---

### 23. alphagbm-company-profile

**功能：** 在个人研究知识库中建立并维护公司研究档案，自动拉取基本面、PE/PB 历史区间（8年）、财务红旗和近期事件。

**档案包含：**
- 当前股价、PE 比率、PB 比率
- PE/PB 历史区间（8年数据，含当前百分位：「PE 32，处于8年历史的85%位置 → 贵」）
- 财务红旗（高危/中危/低危分级）
- 近期事件雷达（公告/新闻/重大变化）
- AI 生成档案摘要
- 关联的投资论据（如已创建）

**套餐限额：** 免费版 1 个，Plus 10个，Pro 50个

**典型问法：**
- "把 NVDA 加入我的研究知识库" / "显示我的 AAPL 档案" / "刷新我的 TSLA 档案" / "我关注了哪些公司"

**API：** `GET/POST /api/research/profiles`，`POST /api/research/profiles/<TICKER>/refresh`，`GET /api/research/profiles/<TICKER>/band`

---

### 24. alphagbm-investment-thesis

**功能：** 记录并追踪每个仓位的「为什么买」和「什么时候卖」，系统自动监控卖出条件是否触发。

**核心机制：**
- **买入论据（buy_thesis）：** 自由文本，记录你的投资逻辑
- **卖出条件（sell_conditions）：** 结构化触发器，如：
  - 从买入价下跌超过 20%
  - PE > 60
  - 营收增长低于 15%
  - 定性触发：「云服务资本开支指引下调超20%」
- 当任一条件触发，系统将论据状态翻转为 `triggered`，并记录触发原因

**状态流转：** `active` → （触发条件）→ `triggered` → （用户关闭）→ `closed`

**典型问法：**
- "帮 NVDA 写一个买入论据" / "我的 AAPL 是因为什么买的" / "有哪些论据被打破了" / "更新 NVDA 的 PE 止盈线从60改到70"

**API：** `GET/POST /api/research/theses`，`GET /api/research/theses/<TICKER>`，`PUT/DELETE /api/research/theses/<ID>`

---

### 25. alphagbm-theme-research

**功能：** 将相关股票按投资主题分组管理，每个主题配有 AI 生成的主题摘要和新闻关键词监控。

**主题示例：**
- AI 基础设施（NVDA / AVGO / MSFT / ORCL）
- 港股高息股
- 新能源供应链
- 生物科技催化剂

**功能特点：**
- 创建命名主题篮子，批量添加/删除股票
- 系统监控设定关键词（如「AI 资本开支」「数据中心」）的相关新闻
- 主题级别的 AI 叙事摘要和聚合涨跌数据

**典型问法：**
- "创建一个 AI 基建主题，包含 NVDA AVGO MSFT" / "我有哪些主题" / "把 ORCL 加到 AI 主题" / "港股高息主题最近有什么动态"

**API：** `GET/POST /api/research/themes`，`PUT/DELETE /api/research/themes/<ID>`

---

### 26. alphagbm-health-check

**功能：** 对整个研究知识库做健康诊断，给出0-100综合评分，并列出具体需要处理的问题。

**诊断内容：**
| 问题类型 | 说明 |
|---|---|
| 过期档案（Stale）| 几周没有更新的公司档案 |
| 论据偏离（Thesis Drift）| AI 检测到原始买入逻辑已不成立（如增长从25%跌到12%）|
| 孤立页面（Orphan）| 有档案但无论据；或主题中有档案找不到的股票 |

**评分区间：**
| 分数 | 等级 | 含义 |
|---|---|---|
| 90-100 | 优秀 | 无需操作 |
| 75-89 | 良好 | 轻微过期 |
| 60-74 | 一般 | 几个档案需刷新 |
| 40-59 | 较差 | 明显偏离/孤立问题 |
| 0-39 | 危险 | 知识库基本过期 |

**权限说明：** 免费/Plus 用户每周自动生成一次报告（GET 读取）；Pro 用户可随时手动触发（POST 生成）。

**典型问法：**
- "帮我检查一下研究库" / "哪些档案过期了" / "有没有论据被打破" / "研究库状态怎么样"

**API：** `GET /api/research/health`（读取最新报告），`POST /api/research/health/generate`（Pro 专属，立即生成）

---

## 技能关联图

```
市场背景层
├── alphagbm-vix-status          VIX 五档分类
├── alphagbm-market-sentiment    全市场情绪仪表盘
└── alphagbm-macro-view          宏观指标追踪

股票分析层
├── alphagbm-stock-analysis      单股深度分析
├── alphagbm-compare             多股横向对比
└── alphagbm-take-profit         量化止盈策略

期权分析层
├── alphagbm-iv-rank             IV Rank / 百分位
├── alphagbm-vol-surface         3D 波动率曲面
├── alphagbm-vol-smile           单到期日微笑/偏斜
├── alphagbm-options-score       期权合约评分
├── alphagbm-options-strategy    多腿策略推荐
├── alphagbm-greeks              希腊字母分析
├── alphagbm-pnl-simulator       盈亏模拟器
├── alphagbm-earnings-crush      财报 IV Crush
└── alphagbm-bps-backtest        BPS 回测

信号层
├── alphagbm-fear-score          每股恐慌指数（BPS 入场信号）
├── alphagbm-unusual-activity    异常期权活动
└── alphagbm-polymarket          预测市场套利信号

策略层
├── alphagbm-duan-analysis       段永平卖方风格
└── alphagbm-hedge-advisor       持仓对冲顾问

研究管理层
├── alphagbm-watchlist           自选股看板
├── alphagbm-alert               智能提醒
├── alphagbm-company-profile     公司研究档案
├── alphagbm-investment-thesis   投资论据追踪
├── alphagbm-theme-research      投资主题篮子
└── alphagbm-health-check        知识库健康诊断
```

---

*本文档由 AI 自动翻译整理，基于 [AlphaGBM](https://alphagbm.com) Skills 原始英文文档。*
