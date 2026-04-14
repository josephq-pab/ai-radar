# 数据时间语义说明

## 概述

本文档明确区分各类时间字段的含义，避免混用和误解。

---

## 时间字段定义

| 字段 | 含义 | 用途 |
|------|------|------|
| **observedAt** | 业务数据观察日期 | 表示该数据反映了哪个时间点的业务状态 |
| **fetchedAt** | 数据抓取时间 | 外部数据被获取的时间（如 analyst 文章发布时间） |
| **builtAt** | 构建时间 | 数据被处理/生成的时间 |
| **file mtime** | 文件修改时间 | 文件系统层面的最后修改时间 |
| **run time** | 运行时间 | 本次运行脚本的实际执行时间 |

---

## 当前数据时间状态

### deposit_benchmark.json (存款对标)

| 字段 | 值 |
|------|-----|
| observedAt | 2026-02-28 |
| builtAt | 2026-03-30 (见 mtime) |
| 说明 | 反映 2026 年 2 月底的存款业务数据 |

### loan_benchmark.json (贷款对标)

| 字段 | 值 |
|------|-----|
| observedAt | 2026-02-28 |
| builtAt | 2026-03-30 |
| 说明 | 反映 2026 年 2 月底的贷款业务数据 |

### loan_rate.json (利率数据)

| 字段 | 值 |
|------|-----|
| observedAt | 2025-12-01 / 2026-02-01 |
| builtAt | 2026-03-30 |
| 说明 | **存在口径不一致问题**: 部分记录为 2025-12，部分为 2026-02，与 deposit/loan 的 2026-02-28 不一致 |

---

## 时间口径不一致问题

### 问题描述

- **deposit/loan**: observedAt = 2026-02-28 (月末口径)
- **loan_rate**: observedAt 包含 2025-12-01 和 2026-02-01 (非月末口径)

### 影响

- 业务理解时可能产生混淆
- 周报展示时需要注意区分

### 当前处理方式

1. **展示层不做强行统一** — 保留原始 observedAt
2. **在摘要中说明差异** — run-summary.json 和 change-summary.md 已体现
3. **后续优化方向**: 
   - 如果 loan_rate 源数据可补齐月末口径，则统一
   - 如果无法补齐，则在文档中明确说明差异来源

---

## 如何判断数据新旧

### 1. 查看 run-summary.json

```bash
python3 -c "
import json
s = json.load(open('reports/run-summary.json'))
fresh = s.get('dataFreshness', {})
print(f'原始文件时间: {fresh.get(\"raw_file_mtimes\")}')
print(f'observedAt: {fresh.get(\"observedAt\")}')
print(f'是否过期: {fresh.get(\"stale\")}')
print(f'原因: {fresh.get(\"stale_reason\")}')
"
```

### 2. 查看 change-summary.json

```bash
python3 -c "
import json
c = json.load(open('reports/change-summary.json'))
print(f'变化文件: {c.get(\"changedFiles\")}')
print(f'结论: {c.get(\"conclusion\")}')
"
```

### 3. 典型判断逻辑

| 场景 | 判断 |
|------|------|
| observedAt ≤ 当前日期 - 30 天 | 数据较旧，建议更新 |
| change-summary 长期无变化 | 可能需要手动刷新数据 |
| stale: true | 数据已过期，不建议直接使用 |

---

## 运行记录示例

```
原始文件 mtime: 2026-03-28 (最近 2 天)
observedAt: 2026-02-28 (数据实际观察点)
结论: 数据基于 2026-02 月度 snapshot，raw 文件较新
```
