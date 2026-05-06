<div align="center">

# AlphaGBM Skills

**用真实数据看透期权定价——而非凭空猜测。**

*26 个 AI Skills，覆盖期权与研究智能 · 基于真实市场数据 · 受 10,000+ 交易者信赖*

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Skills](https://img.shields.io/badge/skills-26-green.svg)](#skills-overview) [![Users](https://img.shields.io/badge/users-10K%2B-orange.svg)](https://alphagbm.com)

[官网](https://alphagbm.com) · [文档](#skills-overview) · [快速开始](#quick-start) · [贡献指南](CONTRIBUTING.md)

</div>

---

## 30 秒演示

```bash
git clone https://github.com/AlphaGBM/skills.git .claude/skills/alphagbm
```

然后问你的 AI：*"使用 AlphaGBM 分析 AAPL 期权"* —— 无需 API Key，内置数据即刻生效。

## 什么是 AlphaGBM？

AlphaGBM 是面向交易者和 AI 智能体的**真实数据期权与研究智能层**。每一个数字都来自真实市场数据——IV、希腊值、VRP、偏斜、流量，以及可追踪的研究工作区——而非 LLM 幻觉。

这 26 个 Skills 将 AlphaGBM 的能力带入你的 AI 工作流：Claude Code、Cursor、Windsurf，或任何支持 Skills 的智能体。

### 为什么选择 AlphaGBM？

| | LLM 角色扮演工具 | 通用金融 API | **AlphaGBM** |
|--|-------------------|---------------------|-------------|
| 数据来源 | LLM 生成 | 延迟/基础 | **实时期权数据** |
| 可验证性 | "85% 置信度" | 部分可验证 | **每个数字都有来源** |
| 期权深度 | 无 | 基础链 | **IV/HV/VRP/希腊值/偏斜/曲面** |
| 评分体系 | 主观 | 无 | **量化评分（期权 0-100，股票 1-10）** |
| 分析模型 | 无 | 无 | **G = B + M（收益 = 基本面 + 动量）** |
| 实战验证 | 否 | 不一 | **10K 用户，3 个月实盘交易** |
| 覆盖市场 | 仅美股 | 不一 | **美股 + 港股 + A 股 + 大宗商品** |

## 快速开始

### 作为 Claude Code Skills 安装

```bash
# 克隆到你的项目
git clone https://github.com/AlphaGBM/skills.git .claude/skills/alphagbm

# 或作为子模块添加
git submodule add https://github.com/AlphaGBM/skills.git .claude/skills/alphagbm
```

### 为 Cursor 安装

```bash
git clone https://github.com/AlphaGBM/skills.git .cursor/skills/alphagbm
```

### 安装 CLI

```bash
# 克隆并安装
git clone https://github.com/AlphaGBM/skills.git
cd skills/cli
pip install -e .

# 设置你的 API Key
alphagbm config set-key agbm_xxxxxxxxxxxxxxxx

# 开始分析
alphagbm stock analyze AAPL
alphagbm options score NVDA
```

完整 CLI 文档见 [cli/README.md](cli/README.md)。

### 立即试用（无需 API Key）

所有 Skills 均内置 AAPL、NVDA、SPY、TSLA 和 META 的演示数据。直接问你的 AI：

> "使用 AlphaGBM 分析 AAPL 股票"
> "对 NVDA 期权评分"
> "显示 TSLA 的波动率曲面"
> "META 最佳看涨策略是什么？"

### 接入实时数据

```bash
# 设置 API Key 以获取实时数据
export ALPHAGBM_API_KEY=agbm_xxxxxxxxxxxxxxxx
export ALPHAGBM_BASE_URL=https://alphagbm.zeabur.app  # 可选，此为默认值

# 在 https://alphagbm.com/api-keys 获取免费 Key
```

### 检查 API 健康状态

```bash
curl https://alphagbm.zeabur.app/api/health
```

返回 API 状态、可用数据字段、数据源健康状况和市场覆盖范围——无需认证。适合 AI 智能体在调用前验证可用性。

### 配额

| 套餐 | 股票分析 | 期权分析 | 快速报价 / 快照 |
|------|---------|---------|----------------|
| 免费 | 2次/天 | 1次/天 | 无限制 |
| Plus | 1,000次/月 | 1,000次/月 | 无限制 |
| Pro | 5,000次/月 | 5,000次/月 | 无限制 |

## Skills 概览

### 核心分析（7 个 Skills）

| Skill | 功能说明 | 示例查询 |
|------|---------|---------|
| [**股票分析**](skills/alphagbm-stock-analysis/) | G=B+M 模型：基本面、动量、EV、风险评分、AI 报告 | "分析 AAPL" |
| [**期权评分**](skills/alphagbm-options-score/) | 4 种策略（卖 Put/Call、买 Put/Call）0-100 评分 | "最佳 NVDA 看涨期权" |
| [**期权策略**](skills/alphagbm-options-strategy/) | 含 15+ 模板的策略构建器与扫描器 | "TSLA 看涨策略" |
| [**波动率曲面**](skills/alphagbm-vol-surface/) | 跨行权价与到期日的三维隐含波动率 | "AAPL IV 贵吗？" |
| [**波动率微笑**](skills/alphagbm-vol-smile/) | 单一到期日的偏斜分析 | "NVDA 认沽偏斜" |
| [**希腊值**](skills/alphagbm-greeks/) | 希腊值计算器 + 隐含波动率求解器 | "AAPL 220C 的希腊值" |
| [**盈亏模拟器**](skills/alphagbm-pnl-simulator/) | 任意持仓的假设情景分析 | "模拟我的铁鹰策略" |

### 数据智能（6 个 Skills）

| Skill | 功能说明 | 示例查询 |
|------|---------|---------|
| [**IV 排名**](skills/alphagbm-iv-rank/) | 与 252 天历史对比的 IV 百分位 | "TSLA IV 高吗？" |
| [**财报 IV 面板**](skills/alphagbm-earnings-crush/) | 崩塌历史 + 隐含波动 + IV 排名标签 + 定价铁鹰组合 | "META 财报铁鹰策略" |
| [**异常活动**](skills/alphagbm-unusual-activity/) | 聪明钱 / 大宗期权流检测 | "今日异常期权流" |
| [**市场情绪**](skills/alphagbm-market-sentiment/) | VIX、认沽/认购比、恐贪指数仪表盘 | "当前市场情绪" |
| [**VIX 状态**](skills/alphagbm-vix-status/) ✨ | 5 档恐慌温度计：平静 / 正常 / 卖方甜蜜点 / 谨慎 / 极度恐慌 | "现在适合做 BPS 吗？" |
| [**恐慌评分**](skills/alphagbm-fear-score/) ✨ | 个股 6 指标恐慌综合评分；≥60 为 BPS 入场信号 | "QQQ 恐慌评分"、"NVDA 是否超卖" |

### 工作流工具（4 个 Skills）

| Skill | 功能说明 | 示例查询 |
|------|---------|---------|
| [**对比**](skills/alphagbm-compare/) | 股票与期权并排比较 | "AAPL vs MSFT" |
| [**自选列表**](skills/alphagbm-watchlist/) | 监控股票关键变化 | "将 NVDA 加入自选" |
| [**提醒**](skills/alphagbm-alert/) | 设置 IV、价格或活动提醒 | "TSLA IV > 80 时提醒我" |
| [**Polymarket**](skills/alphagbm-polymarket/) | 预测市场与期权定价对比 | "降息概率 vs 期权" |

### 风险与投资组合纪律（4 个 Skills）✨

基于真实数据量化退出、对冲和仓位管理决策——而非主观判断。

| Skill | 功能说明 | 示例查询 |
|------|---------|---------|
| [**对冲顾问**](skills/alphagbm-hedge-advisor/) ✨ | 针对现有持仓的情景驱动对冲（刀锋下行 / 抄底 / 锁定收益）；返回定价后的长期认沽 / 领口 / 减仓方案 | "对冲我的 AAPL，成本 140，现价 180" |
| [**BPS 回测**](skills/alphagbm-bps-backtest/) ✨ | 一次调用即可完成牛市认沽价差的滚动回测，含信号 vs 无信号对照组 | "回测 QQQ BPS——恐慌评分有效吗？" |
| [**止盈实验室**](skills/alphagbm-take-profit/) ✨ | 任意股票 15 种退出策略回测；通过新颖的"过山车率"指标自动判断是否可持有或需分批退出 | "TQQQ 适合长期持有吗？" |
| [**段永平分析**](skills/alphagbm-duan-analysis/) ✨ | 三板斧卖方操作手册（在愿意买入的价格卖认沽 / 持保看涨期权收益 / VIX 档位恐慌买入背景） | "AAPL 段式分析" |

### 知识库——研究大脑（5 个 Skills）

构建个人化、可监控的研究工作区。档案自动刷新，投资逻辑触发点自动核查，系统每周自我审计。

| Skill | 功能说明 | 示例查询 |
|------|---------|---------|
| [**公司档案**](skills/alphagbm-company-profile/) | 自动构建研究文件：基本面、PE/PB 区间、风险信号、事件雷达 | "将 NVDA 加入我的知识库" |
| [**投资逻辑**](skills/alphagbm-investment-thesis/) | 买入理由 + 结构化卖出触发点，自动监控 | "我为什么买了 AAPL？" |
| [**宏观视角**](skills/alphagbm-macro-view/) | 追踪 VIX / 美债 10 年 / 美元指数 / 黄金，带组合影响分析 | "追踪 VIX 和美债 10 年" |
| [**主题研究**](skills/alphagbm-theme-research/) | 将股票按主题分组（AI 基础设施、港股红利等）+ 新闻关键词监控 | "创建 AI 基础设施主题" |
| [**健康检查**](skills/alphagbm-health-check/) | 每周审计：过期档案、逻辑漂移、孤立页面 → 0-100 分 | "审计我的研究大脑" |

### 延伸阅读

- **[Investment Masters](https://github.com/AlphaGBM/investment-masters)** -- 10 位大师方法论（巴菲特、达利欧、索罗斯、马克斯……）+ 13F 追踪

## 架构

```
你 / 你的 AI 智能体
    |  （自然语言）
+------------------------------------------------------+
|              AlphaGBM Skills（本仓库）                |
|                                                       |
|  股票    期权   波动率    策略     希腊值   ...         |
|  分析    评分   曲面     构建器   仪表盘               |
+-------------------------+-----------------------------+
                          |
               +----------+----------+
               v                     v
           模拟数据              AlphaGBM API
        （内置，免费）        （alphagbm.zeabur.app）
                              实时市场数据
                              IV/HV/VRP/希腊值/偏斜
```

### Skills 如何联动

Skills 并非孤立——它们相互引用，形成完整工作流：

```
股票分析 --> 期权评分 --> 期权策略 --> 盈亏模拟器
    |            |            |
    v            v            v
  对比       波动率曲面      希腊值
             波动率微笑
             IV 排名 --> 财报 IV 面板

市场情绪 --> 异常活动 --> 提醒
                         自选列表

Polymarket --> 市场情绪 --> 期权策略
```

## 数据覆盖

| 市场 | 股票 | 期权 | 数据点 |
|------|------|------|--------|
| 美股 | 200+ | 完整链 | IV/HV/VRP/希腊值/偏斜/曲面 |
| 港股 | 35+ | 完整链 | IV/HV/VRP/希腊值 |
| A 股 | 20+ ETF | 完整链 | IV/HV/VRP/希腊值 |
| 大宗商品 | 金/银/铜/铝 | 期货期权 | IV/希腊值/交割风险 |

## 真实数据，而非猜测

AlphaGBM 中的每个数字都是**可验证的**：

| 指标 | 数值 | 计算方式 |
|------|------|---------|
| **IV** | 32.5% | 基于实际买卖价的 Black-Scholes |
| **IV 排名** | 58 | 当前 IV vs. 252 个交易日历史 |
| **VRP** | +4.0% | `隐含波动率 - 历史波动率`——衡量期权溢价程度 |
| **期权评分** | 80/100 | 加权：权利金收益率 + 支撑/阻力 + 安全边际 + 趋势 + 胜率 + 流动性 + 时间衰减 |
| **股票评分** | 7.0/10 | `G = B + M`——基本面（PE、PEG、增长、利润率）+ 动量（VIX、技术面、流量） |
| **风险** | 4/10 | 加总：估值 +2、增长 +2、流动性 +2、市场 +1.5、技术面 +1 |
| **EV** | +5.2% | `50% × 1周 + 30% × 1月 + 20% × 3月` 期望值 |

这不是*"基于我的训练数据"*或*"我以 85% 的置信度估计"*。

这是基于市场数据的数学运算。

## 示例工作流

> **你**："分析 AAPL，然后找出最佳期权策略"

智能体自动串联 Skills：

```
1. GET  /api/stock/quick-quote/AAPL          → $261.40 (-0.8%)
2. POST /api/stock/analyze-sync              → G=B+M 评分 7.0/10，EV +5.2%，买入
   {"ticker": "AAPL", "style": "balanced"}     风险 4/10，目标价 $275，止损 $239

3. GET  /api/options/snapshot/AAPL           → IV 32.5%，IV 排名 58，VRP +4.0%
4. POST /api/options/chain-sync              → 卖 Put 评分：80, 78, 75...
   {"symbol": "AAPL", "expiry_date": "..."}    买 Call 评分：76, 74, 72...

5. POST /api/options/tools/strategy/build    → 牛市看涨价差 265/280
   {"template_id": "bull_call_spread"}         最大收益 $1085，最大亏损 $415

6. POST /api/options/tools/simulate          → 盈亏平衡点 $269.15，胜率 44.5%
   {"symbol": "AAPL", "legs": [...]}
```

> **你**："那个 IV 贵吗？"

```
7. GET  /api/options/snapshot/AAPL           → IV 排名 58（中等）
8. GET  /api/options/tools/vol-surface/AAPL  → 平值 IV 处于正向期限结构，26 天后财报
```

所有数据均来自真实 API 调用，全部可验证。

## 路线图

- [x] 26 个 Skills 含模拟数据
- [x] 支持 Claude Code 与 Cursor
- [x] CLI 工具（`pip install -e ./cli`）
- [ ] 实时 WebSocket 数据推送
- [ ] 社区策略共享
- [ ] 更多市场（欧股、日股、韩股期权）

## 贡献指南

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎：

- Bug 报告与功能请求
- Skills 改进与新 Skills 提案
- 翻译（当前支持中英文）
- 更多股票的模拟数据

## 许可证

MIT——详见 [LICENSE](LICENSE)。

## 链接

- [alphagbm.com](https://alphagbm.com) -- 含实时数据的完整平台
- [API 文档](https://alphagbm.com/docs)
- [Discord 社区](https://discord.gg/alphagbm)
- [Twitter/X](https://x.com/alphagbm)

---

<div align="center">

**由 [AlphaGBM](https://alphagbm.com) 团队打造，受全球 10,000+ 交易者信赖。**

*真实数据。真实信号。真实优势。*

</div>
