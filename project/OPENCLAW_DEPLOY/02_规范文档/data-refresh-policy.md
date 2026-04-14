# 数据更新治理规则

## 概述

本文档定义 ai-radar-station 各类数据的更新责任、节奏和过旧判断标准。

---

## 一、关键数据分类与更新规则

### 1. deposit_benchmark.json (存款对标数据)

| 属性 | 说明 |
|------|------|
| **生产来源** | 手工导入 Excel: `股份行人行口径贷款对标数据260228.xlsx` / `2026年2月同业对标数据_更新格式_余额和年日均.xlsx` |
| **推荐更新频率** | **月度** (每月初更新上月数据) |
| **触发方式** | 人工导入新文件 + 重新运行 `parse_initial_data.py` |
| **过旧阈值** | observedAt 超过 45 天 |
| **过旧提示** | run-summary.dataFreshness.stale = true |
| **责任人** | 业务分析师 / 数据管理员 |

### 2. loan_benchmark.json (贷款对标数据)

| 属性 | 说明 |
|------|------|
| **生产来源** | 手工导入 Excel: `股份行人行口径贷款对标数据260228.xlsx` |
| **推荐更新频率** | **月度** |
| **触发方式** | 人工导入新文件 + 重新运行 |
| **过旧阈值** | observedAt 超过 45 天 |
| **过旧提示** | run-summary.dataFreshness.stale = true |
| **责任人** | 业务分析师 / 数据管理员 |

### 3. loan_rate.json (利率数据)

| 属性 | 说明 |
|------|------|
| **生产来源** | 手工导入 Excel: `贷款利率-2602.xlsx` |
| **推荐更新频率** | **月度** |
| **触发方式** | 人工导入新文件 + 重新运行 |
| **过旧阈值** | observedAt 超过 45 天 |
| **过旧提示** | run-summary.dataFreshness.stale = true |
| **责任人** | 业务分析师 / 数据管理员 |

### 4. analyst_opinions.json (分析师观点)

| 属性 | 说明 |
|------|------|
| **生产来源** | 自动抓取: `fetch_analyst_articles.py` |
| **推荐更新频率** | **每日** (工作日) 或 **每周** |
| **触发方式** | 系统自动 (full 运行时) |
| **过旧阈值** | fetchedAt 超过 7 天 |
| **过旧提示** | fetch-health.json 中标注 |
| **责任人** | 系统 + 人工监控 |

### 5. review-queue.json (审核队列)

| 属性 | 说明 |
|------|------|
| **生产来源** | 系统生成: `generate_review_queue.py` |
| **推荐更新频率** | **每次运行** |
| **触发方式** | 系统 (full / rebuild) |
| **过旧阈值** | 不适用 (每次重建) |
| **责任人** | 系统 |

### 6. tracking-items.json (跟踪事项)

| 属性 | 说明 |
|------|------|
| **生产来源** | 系统生成: `build_tracking_items.py` |
| **推荐更新频率** | **每次运行** |
| **触发方式** | 系统 (full / rebuild) |
| **过旧阈值** | 不适用 (每次重建) |
| **责任人** | 系统 + 业务确认状态 |

### 7. weekly-report-draft.md (周报草稿)

| 属性 | 说明 |
|------|------|
| **生产来源** | 系统生成: `generate_weekly_report.py` |
| **推荐更新频率** | **每周** (周五) |
| **触发方式** | 系统 (full 运行) |
| **过旧阈值** | 生成时间超过 7 天 |
| **责任人** | 系统 + 邱非定稿 |

---

## 二、数据新鲜度判断标准

### 判断逻辑

```python
# 过旧阈值
STALE_THRESHOLD = {
    'benchmark': 45,  # 天
    'analyst': 7,     # 天
    'report': 7,      # 天
}

# 判断函数
def is_stale(observed_at: str, data_type: str) -> bool:
    from datetime import datetime
    obs_date = datetime.fromisoformat(observed_at[:10])
    age_days = (datetime.now() - obs_date).days
    threshold = STALE_THRESHOLD.get(data_type, 30)
    return age_days > threshold
```

### 新鲜度等级

| 等级 | 条件 | 说明 |
|------|------|------|
| **新鲜** | age ≤ 7 天 | 数据为近期，可直接使用 |
| **正常** | 7 < age ≤ 30 天 | 数据可接受，但需注意时效 |
| **偏旧** | 30 < age ≤ 45 天 | 建议更新，使用时需说明 |
| **过旧** | age > 45 天 | 不建议直接使用，需更新或明确说明 |

---

## 三、运行摘要中的新鲜度暴露

### run-summary.json 结构

```json
{
  "dataFreshness": {
    "raw_file_mtimes": {
      "存款对标.xlsx": "2026-03-28"
    },
    "observedAt": {
      "deposit_benchmark.json": "2026-02-28",
      "loan_benchmark.json": "2026-02-28",
      "loan_rate.json": "2026-02-01"
    },
    "stale": false,
    "stale_reason": null,
    "assessment": {
      "benchmark_age_days": 31,
      "benchmark_level": "偏旧",
      "analyst_age_days": 1,
      "analyst_level": "新鲜"
    }
  }
}
```

### 使用解释示例

运行摘要中将包含如下说明：

```
📊 数据新鲜度评估：
- benchmark 数据：observedAt = 2026-02-28，距今 31 天 (偏旧)
- analyst 观点：fetchedAt = 2026-03-31，距今 1 天 (新鲜)
- 结论：核心对标数据基于 2026-02 snapshot，analyst 观点已更新
```

---

## 四、更新触发机制

### 日常刷新 (Daily)

- 触发: cron / launchd 工作日 08:00
- 执行: rebuild-only
- 更新: analyst 观点 + tracking 状态 + web bundle
- 不更新: benchmark / rate (需人工导入)

### 周报刷新 (Weekly)

- 触发: cron 每周五 08:00
- 执行: full
- 更新: 全部（包括 analyst 观点重新抓取）
- 不更新: benchmark / rate (需人工导入)

### 手动更新

当有新的月度数据文件时：

1. 将新文件放入 `data/raw/`
2. 更新 `config/source_files.json` 中的文件名
3. 运行 `python3 scripts/run-pipeline.py --mode full`

---

## 五、责任边界

| 角色 | 职责 |
|------|------|
| **业务分析师** | 月度数据导入、数据质量确认 |
| **邱非** | 周报定稿、tracking 状态确认 |
| **系统** | 日常自动运行、异常告警 |
| **Sylvia** | 运行监控、问题记录、状态同步 |
