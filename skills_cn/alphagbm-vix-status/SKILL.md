---
name: alphagbm-vix-status
description: |
  当前 VIX 水平 + 五档恐慌温度计分类 + 期权卖方策略建议。
  将单一 VIX 数字转化为可操作的交易指导（平静 / 正常 / 卖方甜蜜区 / 谨慎 / 极度恐慌）。
  包含当前 VIX 相对1年历史的百分位，以及过去一年市场在每个档位停留的天数比例。
  触发关键词："VIX 是多少"、"VIX 水平"、"市场平静吗"、"市场恐慌指数"、
  "现在适合卖权利金吗"、"VIX 档位"、"VIX 策略"、"波动率环境"、
  "恐慌指数"、"要不要买保护"、"适合做 BPS 吗"。
globs:
  - "mock-data/vix-status/**"
---

# AlphaGBM VIX 状态

将 VIX 单一数字映射到期权卖方实际使用的五档策略区间。
在进行任何单股分析之前，先用这个指标了解整体市场背景。

## 功能说明

将原始 VIX 值映射到以下五个策略区间：

| 档位 | VIX 区间 | 颜色 | 卖方建议 |
|------|----------|------|----------|
| 平静（Calm）| < 15 | 🔵 蓝 | 权利金偏薄，**便宜买保护**（Long Put）|
| 正常（Normal）| 15–20 | 🟢 绿 | 日常卖 Put / BPS 例行操作 |
| 卖方甜蜜区（Sweet Spot）| 20–25 | 🟡 黄 | BPS 权利金变肥，**积极开仓** |
| 谨慎（Caution）| 25–35 | 🟠 橙 | 可做但**减半仓位**，VIX 爆炸风险 |
| 极度恐慌（Extreme Fear）| ≥ 35 | 🔴 红 | 散户卖方最容易被埋，**只买股不卖期权** |

同时返回：
- `mean_1y` — 1年均值 VIX，用于对比
- `percentile_1y` — 今日 VIX 在过去一年分布中的位置
- `distribution_1y_pct` — 过去一年在五个档位各停留的比例

## 使用方法

**输入：** 无参数，市场级别指标。

**输出：**
- `vix` — 当前收盘 VIX
- `level` — 取值：`calm / normal / sweet_spot / caution / extreme_fear`
- `color` — 取值：`blue / green / yellow / orange / red`
- `label` — 中英文短名（如 `卖方甜蜜区 / Seller Sweet Spot`）
- `strategy_hint` — 中英文可操作建议段落
- `percentile_1y`、`mean_1y`
- `distribution_1y_pct` — 过去一年在每档的占比

**示例问法：**
- `VIX 现在多少` — 当前水平 + 档位 + 策略建议
- `现在适合做 BPS 吗` — 检查 VIX 是否在"甜蜜区"（20–25）
- `今天适合卖权利金吗` — 卖方视角的档位分类
- `市场恐慌指数` — 带上下文解读的 VIX
- `今年有多少时间 VIX 在极度恐慌区` — 1年分布统计

## 模拟数据

模拟数据在 `mock-data/vix-status/` 目录，包含五个档位的示例响应。

## API 端点

```
GET /api/options/vix-status
```

无参数。返回示例：

```json
{
  "success": true,
  "vix": 22.5,
  "mean_1y": 18.3,
  "percentile_1y": 68.5,
  "level": "sweet_spot",
  "color": "yellow",
  "label": {"zh": "卖方甜蜜区", "en": "Seller Sweet Spot"},
  "strategy_hint": {"zh": "BPS 权利金变肥，积极开仓", "en": "BPS premiums get juicy — actively open positions"},
  "distribution_1y_pct": {"calm": 12.5, "normal": 45.2, "sweet_spot": 28.7, "caution": 11.3, "extreme_fear": 2.3},
  "timestamp": "2026-04-24T08:00:00"
}
```

定价：免费（不消耗额度）。服务端5分钟缓存。

## 相关 Skills

| Skill | 关联说明 |
|-------|----------|
| [alphagbm-fear-score](../alphagbm-fear-score/) | 单股恐慌指数，VIX 是其6个输入之一 |
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | 更宏观的情绪仪表盘（VIX + 市场广度 + 板块轮动）|
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | 策略构建时应参考 VIX 档位 |

---

*由 [AlphaGBM](https://alphagbm.com) 提供支持 — 面向交易者和 AI 智能体的真实数据期权与研究平台。10K+ 用户。*
