---
name: alphagbm-macro-view
description: >
  追踪真正影响你组合的宏观变量 — VIX、US10Y、DXY、黄金、石油等 —
  并自动计算对用户持仓的影响。每个追踪指标返回当前数值、变化幅度和
  关联用户档案的 AI 影响分析。适用场景：添加宏观指标、查看当前宏观仪表盘、
  询问 VIX 如何影响组合。
  触发关键词："追踪 VIX"、"当前10年期国债"、"美元现在怎样"、
  "把黄金加入宏观监控"、"删除 US10Y"、"宏观指标"、"美债利率"、
  "美元指数"、"VIX 恐慌指数"。
---

# AlphaGBM 宏观视角

在用户知识库中追踪关键宏观指标 — VIX、US10Y、DXY、黄金、石油、BTC 等。
每个指标配有关联用户实际持仓的自动计算影响分析。

## 适用场景

- 用户想开始追踪宏观变量（VIX、国债收益率、美元、黄金…）
- 用户询问当前宏观仪表盘 / 快照
- 用户询问宏观变化如何影响其组合
- 用户想停止追踪某个指标
- 用户提到「宏观」/ 「VIX」/ 「美债」/ 「美元」/ 「macro」/ 「yield」

## 前置条件

- **API Key**：环境变量 `ALPHAGBM_API_KEY`（格式 `agbm_xxxx…`）。
- **Base URL**：默认 `https://alphagbm.zeabur.app`。可通过环境变量 `ALPHAGBM_BASE_URL` 覆盖。
- **无需档案前提** — 宏观追踪与公司档案列表无关。

## API 端点

所有端点均需要 `Authorization: Bearer $ALPHAGBM_API_KEY`。

### 1. 列出已追踪指标（同时返回支持的指标目录）

```
GET /api/research/macro
```

**响应：**
```json
{
  "success": true,
  "indicators": [
    {
      "indicator_key": "VIX",
      "display_name": "CBOE Volatility Index",
      "current_value": 18.2,
      "previous_value": 16.8,
      "change_pct": 8.3,
      "impact_analysis": "VIX 上升，不确定性增加。您的 NVDA 和 TSLA 仓位是高 Beta 股票；可以考虑…",
      "last_updated_at": "2026-04-13T10:15:00Z"
    }
  ],
  "supported": {
    "VIX":   {"name": "CBOE Volatility Index", "category": "volatility"},
    "US10Y": {"name": "US 10-Year Treasury",   "category": "yields"},
    "DXY":   {"name": "US Dollar Index",        "category": "currency"},
    "GOLD":  {"name": "Gold Spot",              "category": "commodity"}
  }
}
```

`supported` 字段是有效 `indicator_key` 的目录。当用户询问「我可以追踪什么」时，用它展示选项。

### 2. 添加指标

```
POST /api/research/macro
Content-Type: application/json

{"indicator_key": "VIX"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `indicator_key` | string | 是 | 必须在 `supported` 目录中 |

**不支持的指标键 400 响应：**
```json
{
  "success": false,
  "error": "Unsupported indicator. Supported: ['VIX', 'US10Y', 'DXY', ...]"
}
```

### 3. 删除指标

```
DELETE /api/research/macro/<INDICATOR_KEY>
```

使用指标键（`VIX`，而非 id）。未追踪时返回 404。

## 响应结构 — 指标

```
{
  id, indicator_key,
  display_name,              // 人类可读名称
  current_value,             // 最新读数
  previous_value,            // 用于计算变化幅度
  change_pct,                // 变化百分比
  impact_analysis,           // AI 生成，参考用户持仓
  last_updated_at
}
```

## 常用指标键

| 键 | 含义 | 重要原因 |
|----|------|----------|
| `VIX` | CBOE 恐慌指数 | 风险情绪，期权定价 |
| `US10Y` | 美国10年期国债收益率 | 折现率，债股轮动 |
| `US2Y` | 美国2年期国债 | 加息预期 |
| `DXY` | 美元指数 | 新兴市场/大宗商品/跨国企业盈利 |
| `GOLD` | 现货黄金 | 对冲，实际收益率反向指标 |
| `OIL` | WTI 原油 | 通胀/能源板块 |
| `BTC` | 比特币 | 风险偏好，加密相关股票 |
| `HKD` | 港元流动性 | 港股市场流动性信号 |

始终先调用 `GET /api/research/macro` 获取最新 `supported` 目录 — 指标键可能会新增或停用。

## 典型工作流

```
1. 用户："追踪 VIX 和10年期美债"
   → POST /api/research/macro {"indicator_key": "VIX"}
   → POST /api/research/macro {"indicator_key": "US10Y"}
   → 确认两者已添加，显示当前数值

2. 用户："宏观面现在怎样？"
   → GET /api/research/macro
   → 展示每个指标：数值、变化、对持仓的影响

3. 用户："停止追踪 DXY"
   → DELETE /api/research/macro/DXY

4. 用户："VIX 偏高对我的仓位有什么影响？"
   → GET /api/research/macro → 读取 VIX 的 impact_analysis 字段
   → impact_analysis 已预先计算并关联用户的具体持仓
```

## 输出格式建议

展示宏观指标时：
1. **多指标用表格**：键 · 数值 · 变化% · 一行影响说明
2. **变化方向高亮**，用箭头/颜色（VIX/收益率上升 ↑ 红色等）
3. 用户问「X 如何影响我的组合」时，**优先展示 impact_analysis**，已预先计算关联持仓
4. **数据陈旧** — 如 `last_updated_at` > 1天，注明「数据可能陈旧」
5. 用户问「我能追踪什么」时，展示按类别分组的 `supported` 目录

## 相关 Skills

- **alphagbm-company-profile** — 宏观影响分析参考用户档案
- **alphagbm-market-sentiment** — 更广泛的跨资产情绪读取
- **alphagbm-iv-rank** — 期权专属波动率背景

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
