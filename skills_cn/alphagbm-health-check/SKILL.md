---
name: alphagbm-health-check
description: >
  用户研究知识库的每周诊断报告 — 标记过期档案（几周未更新）、论据偏离
  （AI 检测到原始前提不再成立）和孤立页面（无论据的档案、缺少档案的主题中的股票）。
  返回0-100整体健康评分及具体行动建议。
  适用场景：审计知识库状态、触发新鲜报告、查看需要关注的内容。
  触发关键词："体检我的研究库"、"哪些过期了"、"有没有偏离"、"生成报告"、
  "研究库体检"、"过期档案"、"论据偏离"、"孤立主题"。
---

# AlphaGBM 知识库健康体检

定期审计用户研究工作区 — 过期档案、偏离论据、孤立页面 — 输出0-100综合评分
和具体改进建议。

## 适用场景

- 用户询问知识库中有什么问题 / 过期内容
- 用户想手动触发新鲜健康报告
- 用户询问过期档案、论据偏离或孤立条目
- 用户提到「健康体检」/ 「体检」/ 「audit」/ 「health check」/ 「什么需要更新」

## 前置条件

- **API Key**：环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx…`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。
- **生成的套餐要求**：`POST /health/generate` 为 **Pro 专属**。免费/Plus 用户收到 403，含 `upgrade_required: true`。
  免费/Plus 用户仍可通过 `GET /health` 读取最新的每周自动生成报告。

## API 端点

所有端点均需要 `Authorization: Bearer $ALPHAGBM_API_KEY`。

### 1. 获取最新健康报告

```
GET /api/research/health
```

**存在报告时的响应：**
```json
{
  "success": true,
  "has_report": true,
  "report_date": "2026-04-13",
  "overall_score": 78,
  "stale_profiles": [
    {"ticker": "AAPL", "days_since_update": 21}
  ],
  "thesis_drift": [
    {"ticker": "NVDA", "drift_reason": "营收增长从写论据时的25%降至12%"}
  ],
  "orphan_pages": [
    {"ticker": "XYZ", "issue": "档案30天后仍无论据"}
  ],
  "recommendations": [
    {"action": "refresh", "ticker": "AAPL", "reason": "已过期21天"},
    {"action": "review_thesis", "ticker": "NVDA", "reason": "增长已减速"},
    {"action": "archive", "ticker": "XYZ", "reason": "孤立超过30天"}
  ],
  "created_at": "2026-04-13T02:00:00Z"
}
```

**尚无报告时的响应：**
```json
{
  "success": true,
  "has_report": false
}
```

### 2. 生成新鲜报告（Pro 专属）

```
POST /api/research/health/generate
```

立即对用户的档案 + 论据 + 主题启动完整审计。返回与 `GET` 相同格式的新报告。

**套餐限制响应（403）：**
```json
{
  "success": false,
  "error": "Health check generation is a Pro feature.",
  "upgrade_required": true
}
```

免费/Plus 用户仍可获得每周自动生成的报告（通过 `GET` 读取），只是不能按需触发。

## 响应结构 — 报告

```
{
  id, report_date,
  stale_profiles,          // [{ticker, days_since_update}]
  thesis_drift,            // [{ticker, drift_reason}]
  orphan_pages,            // [{ticker, issue}]
  overall_score,           // 0-100
  recommendations,         // [{action, ticker, reason}]
  created_at
}
```

## 评分区间解读

| 分数 | 等级 | 含义 |
|------|------|------|
| 90-100 | 优秀（Excellent）| 无紧急问题 |
| 75-89  | 良好（Good）| 轻微过期 |
| 60-74  | 一般（Fair）| 几个档案需刷新，部分偏离 |
| 40-59  | 较差（Poor）| 明显偏离/孤立问题 |
| 0-39   | 危险（Critical）| 知识库大部分已过期 |

## 推荐操作类型

- `refresh` — 调用 `POST /api/research/profiles/<ticker>/refresh`
- `review_thesis` — 浮出论据 + 最新基本面；由用户决定编辑或关闭
- `archive` — `DELETE /api/research/profiles/<ticker>` 或删除孤立条目
- `create_thesis` — 档案存在但无论据；提示用户写一条

执行这些操作的 Skills：`alphagbm-company-profile`、`alphagbm-investment-thesis`。

## 典型工作流

```
1. 用户："我的研究库状态怎么样？"
   → GET /api/research/health
   → 如果 has_report=false："还没有报告 — 首次自动审计在<日期>运行。
      Pro 用户现在可以触发。"
   → 如果 has_report=true：展示评分 + 前3个建议

2. 用户（Pro）："现在运行一次新鲜的健康体检"
   → POST /api/research/health/generate
   → 展示新报告

3. 用户（免费/Plus）："运行健康体检"
   → POST /api/research/health/generate 返回 403
   → 回退：通过 GET 展示上次每周自动报告，建议升级

4. 用户："帮我修复那些过期的"
   → 对每个 action=refresh 的建议：
     POST /api/research/profiles/<ticker>/refresh
   → 重新检查：GET /api/research/health → 展示更新后评分
```

## 输出格式建议

展示健康报告时：
1. **首先展示综合评分** + 等级（颜色：绿色 ≥ 75，黄色 60-74，红色 < 60）
2. **前3个建议** — 最可操作的优先（刷新 > 审查 > 归档）
3. **按类别分组** — "3个过期档案 · 1个偏离论据 · 2个孤立条目" 作为芯片行
4. **每只股票可操作** — 理由与一键操作配对
5. **报告日期突出** — "截至 2026-04-13"，让用户知道新鲜度
6. **尚无报告** — 解释每周节奏，为 Pro 用户提供按需触发选项

## 相关 Skills

- **alphagbm-company-profile** — 对标记的过期档案执行刷新
- **alphagbm-investment-thesis** — 审查/关闭偏离的论据
- **alphagbm-theme-research** — 处理主题内的孤立条目

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
