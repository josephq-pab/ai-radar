# 对公 AI 雷达站 — 评估规则（EVAL_RULES）

> 本文件定义 pipeline 运行成功标准、数据完整性要求、A/B Gate 判断口径、前端和报告最低要求。
> 建立时间：2026-04-07

---

## 一、运行成功标准

Pipeline 完整链路（`run-pipeline.py --full`）成功必须同时满足：

1. **smoke test 全部通过**（38/38 PASS，无 FAIL 项）
2. **主链路 JSON 生成**：`deposit_benchmark.json`、`loan_benchmark.json`、`loan_rate.json` 均存在且非空
3. **review-queue.json 生成**：包含 review 条目
4. **tracking-items.json 生成**：包含跟踪事项
5. **weekly-report-draft.md 生成**：第一节"核心结论摘要"非空
6. **app-data.js 生成**：包含完整的 `window.APP_DATA` 注入

满足以上全部 → `browseReadiness: ✅` / `internalDiscussionReadiness: ✅`

---

## 二、数据完整性检查

### 2.1 中间层 JSON 完整性

| 文件 | 必须包含字段 | 验证方法 |
|------|-------------|---------|
| `deposit_benchmark.json` | `data[].bank`, `data[].balance`, `data[].monthly_change`, `data[].ytd_change`, `observedAt` | 检查字段非空 |
| `loan_benchmark.json` | `data[].bank`, `data[].balance`, `observedAt` | 同上 |
| `loan_rate.json` | `data[].bank`, `data[].current_rate`, `observedAt` | 同上 |
| `review-queue.json` | 非空数组，每项有 `id`、`summary`、`priority` | 长度 ≥ 1 |
| `tracking-items.json` | 非空数组，每项有 `id`、`status`、`priority` | 长度 ≥ 1 |
| `review-status.json` | 每条有 `status`（accepted/rejected/pending） | — |

### 2.2 数据新鲜度要求

| 数据类型 | 最低新鲜度 | 当前状态（2026-04-07） |
|----------|-----------|----------------------|
| 贷款利率 | ≥ 2026-03-01 | ❌ 2025-12-01（阻断项） |
| 存款对标 | ≥ 2026-03-01 | ✅ 2026-03 |
| 贷款对标 | ≥ 2026-03-01 | ✅ 2026-03 |
| 分析师观点 | 任意 | ✅ 有效 6 条 |

### 2.3 数据月份标注规则

前端和周报引用的利率数据必须携带月份标注：
- 格式：`利率数据（2026-02）` / `利率数据（截至 2026-02）`
- 月份取自 `loan_rate.json` 的 `observedAt` 字段
- **禁止**在月份未确认的情况下标注为"最新"

---

## 三、A Gate 判断口径

### A Gate 定义
原始数据是否已更新到目标月份。

### A Gate 通过条件
```
loan_rate.json observedAt ≥ 2026-03-01
```

### A Gate 阻断影响
- 阻断阶段：数据解析（parse）完成后即可判断
- 阻断范围：不影响 B/C Gate 运行，但影响报告引用
- 绕行方式：在周报和前端中明确标注数据月份（2026-02），注明"待更新"

### 当前状态
**❌ BLOCKED** — `observedAt = 2025-12-01`，目标 ≥ 2026-03-01

---

## 四、B Gate 判断口径

### B Gate 定义
Review 队列质量：是否具备进入人工 review 的可用性。

### B Gate 通过条件
- `usable + referenceable + reportable` 总数 ≥ 1
- 无乱码、无空 placeholder、无明显数据错误

### B Gate 分类标准

| 分类 | 定义 | 当前数量 |
|------|------|---------|
| `usable` | 可直接引用到报告 | 4 |
| `referenceable` | 需补充说明后可引用 | 2 |
| `reportable` | 已通过 review 可输出 | 3 |

### 当前状态
**✅ CLEARED** — usable=4, referenceable=2, reportable=3

---

## 五、C Gate 判断口径

### C Gate 定义
Review 闭环完整性：所有 review 条目是否已给出明确处置结论。

### C Gate 通过条件
- `blocker` 数量 = 0
- 所有条目的 `status` ∈ {accepted, rejected, closed}

### 当前状态
**✅ CLEARED** — 0 blockers，15 followups

---

## 六、前端可展示的最低要求

| 要求 | 标准 |
|------|------|
| 页面可访问 | `http://localhost:8787` 可打开 |
| Bundle 可用 | `app-data.js` 存在且大小 > 50KB |
| 数据展示 | deposit / loan / rate 三个模块均有数据 |
| 数据月份 | 每个数据点必须标注月份 |
| 无 JS 错误 | 浏览器控制台无 Error 级别报错 |

**当前状态：** ✅ 满足最低要求（8787 端口正常）

---

## 七、报告可输出的最低要求

| 要求 | 标准 |
|------|------|
| 第一节存在 | "核心结论摘要"有实质性内容（非模板占位） |
| 同业数据完整 | 至少包含 4 家重点股份行数据 |
| 利率数据标注月份 | 利率数字后必须跟月份标注 |
| 跟踪事项状态 | tracking-items 有明确状态（非全部 pending） |
| 无数据矛盾 | 周报与中间层 JSON 数据一致 |

**当前状态：** ⚠️ 满足（利率数据标注为 2026-02，需注明待更新）

---

## 八、数据文件路径规范

所有中间层 JSON 必须在以下路径范围内：

```
OPENCLAW_DEPLOY_BASE/
├── 04_数据与规则/
│   └── processed/
│       ├── deposit_benchmark.json
│       ├── loan_benchmark.json
│       └── loan_rate.json
├── 06_进展状态/
│   ├── review-queue.json
│   ├── review-status.json
│   ├── tracking-items.json
│   └── weekly-report-draft.md
└── 03_前端页面/
    └── app-data.js
```

**禁止**将中间产物写入 `workspace/`、`workspace-digital-employee/` 等其他目录。
