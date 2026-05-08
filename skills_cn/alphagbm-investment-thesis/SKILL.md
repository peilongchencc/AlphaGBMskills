---
name: alphagbm-investment-thesis
description: >
  记录并追踪每个仓位的「为什么买」和「什么时候卖」。
  每条论据附属于一个公司档案：买入理由以散文形式记录，卖出条件作为结构化触发器
  （价格下跌、PE 超限、论据失效）。系统自动监控条件，一旦触发则将论据状态翻转
  为「已触发」。适用场景：记录买入逻辑、设置退出触发条件、查看活跃论据、
  查看哪些已触发。
  触发关键词："为 NVDA 写一个论据"、"我为什么买的 AAPL"、"为 TSLA 设置止损逻辑"、
  "哪些论据被触发了"、"更新我的论据"、"投资论据"、"卖出条件"、
  "买入理由"、"论据被打破"。
---

# AlphaGBM 投资论据

将「我买这只因为…」转化为有追踪、有监控的记录。每条论据将散文形式的买入理由
与结构化卖出条件配对，使系统能自动检测推理何时不再成立。

## 适用场景

- 用户想记录*为什么*买入某只股票
- 用户想设置退出触发器（价格、PE、基本面失效）
- 用户询问哪些论据仍然有效 vs 已被触发
- 用户想更新 / 完善现有论据
- 用户提到「论据」/ 「买入理由」/ 「卖出条件」/ 「thesis」/ 「exit trigger」

## 前置条件

- **API Key**：环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx…`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。
- **需要档案**：论据必须附属于已存在的公司档案。如果用户尚未为该股票创建档案，
  先调用 `POST /api/research/profiles`（参见 `alphagbm-company-profile`）。

## API 端点

所有端点均需要 `Authorization: Bearer $ALPHAGBM_API_KEY`。

### 1. 列出论据

```
GET /api/research/theses?status=active
```

| 查询参数 | 取值 | 说明 |
|----------|------|------|
| `status` | `active` / `triggered` / `closed` | 可选过滤 |

**响应：**
```json
{
  "success": true,
  "theses": [
    {"id": 12, "ticker": "NVDA", "buy_thesis": "...", "status": "active"}
  ]
}
```

### 2. 按股票获取论据

```
GET /api/research/theses/<TICKER>
```

返回股票的*活跃*论据。不存在时返回 404。

### 3. 创建论据

```
POST /api/research/theses
Content-Type: application/json

{
  "ticker": "NVDA",
  "buy_thesis": "AI 资本开支周期；数据中心 GPU 护城河；FCF > $600亿。",
  "sell_conditions": [
    {"type": "price_drop_pct",  "value": 20},
    {"type": "pe_above",        "value": 60},
    {"type": "growth_below",    "value": 15},
    {"type": "thesis_breach",   "value": "云服务资本开支指引下调超20%"}
  ]
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ticker` | string | 是 | 必须匹配已存在的档案 |
| `buy_thesis` | string | 是 | 自由文本，建议2-4句话 |
| `sell_conditions` | array | 否 | 结构化触发器（见下方类型）|

**常见 `sell_conditions` 类型：**
- `price_drop_pct` — 从买入/峰值下跌的百分比
- `pe_above` / `pb_above` — 估值上限
- `growth_below` — 营收/盈利增长下限
- `thesis_breach` — 自由文本定性触发器（需手动监控）

### 4. 更新论据（按 id）

```
PUT /api/research/theses/<THESIS_ID>
Content-Type: application/json

{"buy_thesis": "更新后的文字", "sell_conditions": [...], "status": "closed"}
```

支持部分更新。注意：**使用 `thesis_id`（整数）**，而非股票代码 — 需先通过列表或获取接口读取 id。

### 5. 删除论据（按 id）

```
DELETE /api/research/theses/<THESIS_ID>
```

硬删除。同样使用数字 id。

## 响应结构 — 完整论据

```
{
  id, ticker,
  buy_thesis,                     // 散文
  sell_conditions,                // [{type, value}]
  status,                         // "active" | "triggered" | "closed"
  thesis_score,                   // AI 置信度 0-100（如已评分）
  ai_feedback,                    // AI 对论据的评审（Markdown）
  triggered_at, trigger_detail,   // 状态翻转时填充
  created_at, updated_at
}
```

## 状态流转

```
active ──（卖出条件触发）──▶ triggered
   │                              │
   └──────（用户关闭）──▶ closed ◀──┘
```

当 `status = "triggered"` 时，`trigger_detail` 显示是哪个条件触发了。
把这个展示给用户 — 这正是整个系统的意义所在。

## 典型工作流

```
1. 用户："我要买 NVDA，因为 AI 资本开支还在加速"
   → （确保档案存在，参见 alphagbm-company-profile）
   → POST /api/research/theses，附 buy_thesis + sell_conditions
   → 确认："已保存。监控中：价格下跌 > 20%，PE > 60，增长 < 15%。"

2. 用户："我的活跃论据有哪些？"
   → GET /api/research/theses?status=active
   → 表格：股票 · 一行论据 · 条件 · 评分

3. 用户："有没有论据被触发？"
   → GET /api/research/theses?status=triggered
   → 预警列表，含 trigger_detail 说明触发原因

4. 用户："更新我的 NVDA 论据，PE 退出线从60改到70"
   → GET /api/research/theses/NVDA 找到 id
   → PUT /api/research/theses/<id>，修改 sell_conditions
```

## 输出格式建议

向用户展示论据时，重点突出：
1. **股票 + 状态**（颜色/标识：活跃=绿色，触发=红色，关闭=灰色）
2. **买入论据** — 原文前2句
3. **卖出条件** — 以项目符号列出，人类可读形式（"股价下跌20%时退出"）
4. **如已触发** — 哪个触发器触发了，首先展示这个
5. **AI 评审/评分** — 如有，以引用块形式展示
6. **时间** — "3周前写，2天前查阅"

## 相关 Skills

- **alphagbm-company-profile** — 前置条件，论据附属于档案
- **alphagbm-health-check** — 浮出可能偏离原始前提的论据
- **alphagbm-stock-analysis** — 运行新鲜分析来验证论据

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
