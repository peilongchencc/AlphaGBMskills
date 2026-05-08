---
name: alphagbm-company-profile
description: >
  在 AlphaGBM 上构建和维护公司研究档案 — 从基本面、PE/PB 历史区间、财务红旗
  和事件雷达自动生成。每个档案是一条用户+股票记录，系统按计划刷新。
  适用场景：创建需追踪公司的监控列表、拉取已保存的研究文件、刷新档案市场数据、
  查看 PE/PB 历史区间。
  触发关键词："把 AAPL 加入我的知识库"、"显示我的 NVDA 档案"、
  "刷新我的 TSLA 档案"、"列出我追踪的公司"、"META PE 历史区间"、
  "我的研究大脑里有什么"、"创建公司档案"、"我的投研档案"。
---

# AlphaGBM 公司档案

在用户私有知识库中构建和管理公司研究档案。每个档案记录基本面（PE/PB）、
8年估值区间、财务红旗和近期事件，按计划自动刷新。

## 适用场景

- 用户想在个人研究空间追踪一家公司
- 用户询问列出 / 查看 / 删除已保存的公司
- 用户询问某只股票的 PE 或 PB 历史区间
- 用户想刷新陈旧的档案
- 用户提到「知识库」/ 「投研档案」/ 「research brain」/ 「knowledge base」

## 前置条件

- **API Key**：存储在环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx…`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。
- 如果用户没有密钥，引导其在 <https://alphagbm.com> 注册，并在 `/api-keys` 创建。
- **套餐限额**：免费版 = 1 个档案；Plus = 10 个；Pro = 50 个。超出上限时创建端点返回 403，含 `upgrade_required: true`。

## API 端点

所有端点均需要 `Authorization: Bearer $ALPHAGBM_API_KEY`。

### 1. 列出档案

```
GET /api/research/profiles?page=1&per_page=20
```

**响应：**
```json
{
  "success": true,
  "profiles": [{"ticker": "AAPL", "company_name": "...", "current_price": 261.0}],
  "total": 3,
  "page": 1,
  "per_page": 20
}
```

### 2. 获取档案详情（含已有论据）

```
GET /api/research/profiles/<TICKER>
```

返回完整档案 + 嵌入的 `thesis` 字段（无论据时为 null）。
股票不在用户知识库中时返回 404。

### 3. 创建档案

```
POST /api/research/profiles
Content-Type: application/json

{"ticker": "AAPL"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ticker` | string | 是 | 股票代码（美股/港股/A股），大小写不敏感 |

**行为：** 通过数据提供商拉取基本面，计算红旗和事件雷达，持久化档案。
如果该用户+股票的档案已存在，则在原地更新（幂等操作）。

**套餐限制响应（403）：**
```json
{
  "success": false,
  "error": "Profile limit reached. Upgrade to Plus for 10 profiles.",
  "current": 1,
  "max": 1,
  "upgrade_required": true
}
```

### 4. 删除（归档）档案

```
DELETE /api/research/profiles/<TICKER>
```

软删除，将 `status` 翻转为 `archived`。未找到时返回 404。

### 5. 刷新档案数据

```
POST /api/research/profiles/<TICKER>/refresh
```

拉取最新市场数据，重新计算红旗和事件。当用户说「刷新我的档案」或
`last_updated_at` 陈旧（> 7天）时使用。

### 6. PE/PB 历史区间数据（缓存24小时）

```
GET /api/research/profiles/<TICKER>/band
```

返回8年 PE/PB 历史数据，用于构建区间图表。**可以在股票不在用户知识库的情况下调用**，
它是只读的市场数据端点。

**响应：**
```json
{
  "success": true,
  "ticker": "AAPL",
  "pe_history": [{"date": "2017-04", "pe": 16.2}],
  "pb_history": [...],
  "current_pe_percentile": 0.82,
  "current_pb_percentile": 0.75
}
```

## 响应结构 — 完整档案

```
{
  id, ticker, company_name, market,          // market = US | HK | CN
  current_price, pe_ratio, pb_ratio,
  pe_band_data,                              // 8年历史，与 /band 端点格式相同
  financial_red_flags,                       // [{rule_id, severity: "high|med|low", message}]
  event_radar,                               // [{event_type, timestamp, headline}]
  ai_profile_summary,                        // Markdown，约500字符
  status,                                    // "active" | "archived"
  last_viewed_at, last_updated_at, created_at
}
```

## 典型工作流

```
1. 用户："把 NVDA 加入我的研究库"
   → POST /api/research/profiles {"ticker": "NVDA"}
   → 展示："已添加 NVDA。当前 PE 45，2个红旗，PE 处于8年区间的85百分位。"

2. 用户："我的知识库里有什么？"
   → GET /api/research/profiles
   → 展示表格：股票 · 公司 · PE · 最后更新 · 红旗数量

3. 用户："给我看我的 AAPL 档案"
   → GET /api/research/profiles/AAPL
   → 展示：摘要、PE/PB 历史区间、红旗列表、事件雷达、关联论据（如有）

4. 用户："刷新我的 TSLA 档案"
   → POST /api/research/profiles/TSLA/refresh
```

## 套餐限额

| 套餐 | 最大档案数 |
|------|-----------|
| 免费 | 1 |
| Plus | 10 |
| Pro  | 50 |

当创建请求触及上限时，API 返回 `upgrade_required: true`。
向用户展示时附上升级链接 `/pricing`。

## 输出格式建议

展示档案时，重点突出：
1. **股票代码 + 公司名** 及市场标志（US / HK / CN）
2. **当前价格 + PE / PB** 加百分位背景（"PE 32，8年区间的85百分位 → 偏贵"）
3. **红旗** — 按严重程度分组，展示前3条
4. **事件雷达** — 最近3-5个事件（含日期）
5. **关联论据** — 如有，一行买入理由 + 退出触发条件摘要
6. **数据陈旧** — 如 `last_updated_at` > 7天，建议刷新

## 相关 Skills

- **alphagbm-investment-thesis** — 为档案附加买入论据 + 退出触发条件
- **alphagbm-health-check** — 检测工作区中陈旧/偏离的档案
- **alphagbm-stock-analysis** — 一次性深度分析（不持久化到知识库）
- **alphagbm-theme-research** — 将档案按主题分组（AI基建、港股高息等）

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
