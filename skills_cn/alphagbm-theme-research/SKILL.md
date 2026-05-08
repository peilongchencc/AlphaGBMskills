---
name: alphagbm-theme-research
description: >
  将相关股票按投资主题分组 — AI 基础设施、港股高息、新能源供应链、生物科技催化剂 —
  并配有主题级别的 AI 摘要和新闻关键词监控。每个主题是一个命名的股票篮子加上系统
  为你监控的关键词。适用场景：创建主题篮子、查看主题聚合视图、添加/删除股票、
  监控某个话题的新闻。
  触发关键词："创建一个 AI 基建主题"、"显示我的主题"、"把 MSFT 加入 AI 主题"、
  "港股高息最近有什么动态"、"主题研究"、"AI基建"、"港股高息"、"投资主题"。
---

# AlphaGBM 主题研究

将相关股票整理成命名的投资主题，配有 AI 生成摘要和新闻关键词监控列表。
每个主题是一个轻量级篮子，可在概念层面追踪。

## 适用场景

- 用户想按主题组织股票（AI 基建、港股高息、新能源供应链、生物科技…）
- 用户想查看特定主题的持仓 + 最新摘要
- 用户想向主题添加或删除股票
- 用户想让系统监控某个话题的新闻
- 用户提到「主题」/ 「theme」/ 「basket」/ 「篮子」/ 「板块」

## 前置条件

- **API Key**：环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx…`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。
- **套餐限额**：免费档位对主题有上限。通过仪表盘端点检查 `limits.max_themes`。

## API 端点

所有端点均需要 `Authorization: Bearer $ALPHAGBM_API_KEY`。

### 1. 列出主题

```
GET /api/research/themes
```

**响应：**
```json
{
  "success": true,
  "themes": [
    {
      "id": 7,
      "theme_name": "AI 基础设施",
      "description": "AI 资本开支周期的铲子和镐",
      "tickers": ["NVDA", "AVGO", "MSFT", "ORCL"],
      "news_keywords": ["AI capex", "数据中心", "hyperscaler"],
      "theme_summary": "4家超大规模云厂商资本开支指引上调…",
      "last_updated_at": "2026-04-13T09:00:00Z"
    }
  ]
}
```

### 2. 获取主题详情（聚合数据）

```
GET /api/research/themes/<THEME_ID>
```

返回主题 + 跨股票的聚合数据（平均价格变化、顶级异动股、关键词匹配的近期新闻）。
未找到或不属于当前用户时返回 404。

### 3. 创建主题

```
POST /api/research/themes
Content-Type: application/json

{
  "theme_name": "AI 基础设施",
  "description": "AI 资本开支的铲子和镐",
  "tickers": ["NVDA", "AVGO", "MSFT"],
  "news_keywords": ["AI capex", "数据中心"]
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `theme_name` | string | 是 | 显示名称，用于去重 |
| `description` | string | 否 | 简短说明 |
| `tickers` | 字符串数组 | 否 | 初始股票；之后可编辑 |
| `news_keywords` | 字符串数组 | 否 | 监控新闻匹配的关键词 |

### 4. 更新主题（按 id）

```
PUT /api/research/themes/<THEME_ID>
Content-Type: application/json

{"tickers": ["NVDA", "AVGO", "MSFT", "ORCL"], "news_keywords": [...]}
```

部分更新。创建时的任意字段均可修改。

### 5. 删除主题（按 id）

```
DELETE /api/research/themes/<THEME_ID>
```

硬删除。不影响底层公司档案。

## 响应结构 — 主题

```
{
  id, theme_name, description,
  tickers,                  // 股票代码字符串数组
  news_keywords,            // 用于新闻匹配的关键词数组
  theme_summary,            // AI 生成叙事（Markdown）
  last_updated_at, created_at
}
```

主题详情端点（`GET /themes/<id>`）还包含聚合字段，如顶级异动股和近期匹配新闻。

## 典型工作流

```
1. 用户："创建一个 AI 基建主题，包含 NVDA、AVGO、MSFT"
   → POST /api/research/themes
     {"theme_name": "AI 基础设施", "tickers": ["NVDA","AVGO","MSFT"],
      "news_keywords": ["AI capex", "数据中心"]}
   → 确认主题已创建；提示它会开始积累摘要和新闻

2. 用户："我有哪些主题？"
   → GET /api/research/themes
   → 表格：主题 · 股票数量 · 最后更新 · 摘要摘录

3. 用户："把 ORCL 加入我的 AI 主题"
   → GET /api/research/themes（找到 id）
   → PUT /api/research/themes/<id> {"tickers": [... + "ORCL"]}

4. 用户："我的港股高息主题最近有什么动态？"
   → GET /api/research/themes/<id>
   → 以 theme_summary 开头 + 聚合异动 + 匹配新闻
```

## 输出格式建议

展示主题时：
1. **列表视图** — 主题名 · 股票数量 · "X天前更新" · 一句话摘要
2. **详情视图** — 以 `theme_summary`（AI 叙事）开头，然后是股票涨跌网格，再是近期匹配新闻
3. **关键词卫生** — 如果用户创建主题时没有 `news_keywords`，提示："要让我监控哪些新闻关键词吗？例如'AI capex'、'hyperscaler'"
4. **股票重叠** — 创建新主题时，检查股票是否已存在于其他主题；可以重叠（股票可在多个主题中），但值得一提

## 相关 Skills

- **alphagbm-company-profile** — 主题引用档案；添加无档案股票仍可运作，但没有档案数据
- **alphagbm-health-check** — 标记主题中不再有档案的孤立股票
- **alphagbm-compare** — 主题内股票的横向对比

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
