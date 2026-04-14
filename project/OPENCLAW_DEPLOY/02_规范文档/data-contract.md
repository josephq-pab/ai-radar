# 对公 AI 雷达站 — 数据契约

**版本**: v1.0  
**更新时间**: 2026-03-30

---

## 1. deposit_benchmark.json

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataset | string | 是 | 固定值: `deposit_benchmark` |
| observedAt | string | 是 | 日期 (YYYY-MM-DD) |
| bank | string | 是 | 银行名称 |
| metricGroup | string | 是 | 指标组 (如"本外币存款") |
| metricCode | string | 是 | 指标代码 (如`balance_total`) |
| currentValue | float | 是 | 当前余额 (万元) |
| monthChange | float | 否 | 月环比变动 |
| yearChange | float | 否 | 年同比变动 |

**生产者**: `parse_initial_data.py`  
**消费者**: `generate_weekly_report.py`, `build_web_bundle.py`

---

## 2. loan_benchmark.json

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataset | string | 是 | 固定值: `loan_benchmark` |
| observedAt | string | 是 | 日期 |
| bank | string | 是 | 银行名称 |
| metricGroup | string | 是 | 指标组 |
| metricCode | string | 是 | 指标代码 |
| currentValue | float | 是 | 当前余额 |

**生产者**: `parse_initial_data.py` (含 dedup)  
**去重策略**: 保留第一条 (bank, metricGroup, observedAt)

---

## 3. loan_rate.json

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataset | string | 是 | `loan_rate` |
| observedAt | string | 是 | 日期 |
| bank | string | 是 | 银行名称 |
| monthlyRate | float | 是 | 月度加权平均利率 |

---

## 4. review-queue.json

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 (stable hash 或硬编码) |
| category | string | 是 | 分类 |
| text | string | 是 | 内容文本 |
| source | string | 是 | 来源文件 |

**生产者**: `generate_review_queue.py`  
**去重兜底**: 存在硬编码 fallback 数组

---

## 5. tracking-items.json

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 与 review-queue 对应 |
| layer | string | 是 | 层级 (如"待人工确认事项") |
| trackingStatus | string | 是 | 状态 (待研判/跟踪中/已上报/已行动/已关闭) |
| text | string | 是 | 事项内容 |
| latestProgress | string | 否 | 最新进展 |
| nextAction | string | 否 | 下一步动作 |

**生产者**: `build_tracking_items.py`  
**状态来源**: `generate_weekly_report.py` 第九/十节

---

## 6. analyst_opinions.json

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| analystName | string | 是 | 分析师姓名 |
| articleTitle | string | 是 | 文章标题 |
| sourceUrl | string | 是 | 来源 URL |
| publishedAt | string | 是 | 发布时间 |
| relevanceScore | float | 是 | 相关度 (0-1) |

**生产者**: `fetch_analyst_articles.py` + `build_analyst_opinions.py`  
**编码修复**: `build_analyst_opinions.py` 的 `_repair_mojibake()`

---

## 迁移核心字段

以下字段在迁移到 API/DB 时必须保留：

- `deposit_benchmark`: bank + metricGroup + currentValue + observedAt
- `loan_benchmark`: bank + metricGroup + metricCode + currentValue + observedAt
- `review-queue`: id + category + text + source
- `tracking-items`: id + trackingStatus + latestProgress + nextAction
