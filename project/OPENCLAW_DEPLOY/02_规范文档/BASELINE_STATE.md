# Phase 2 基线 — 现状对齐文档

> 版本：v2-baseline | 日期：2026-04-02 | 状态：dry-run/fast-check 已验证

---

## 一、当前系统状态

### 1.1 Gate 状态（`rebuild_go_live_gate.py --check` 输出）

```
A_gate: BLOCKED
  deposit_observedAt: 2026-03-31（阈值: >=2026-03-01）✅
  loan_observedAt: 2026-03-31（阈值: >=2026-03-01）✅
  rate_observedAt: 2025-12-01（阈值: >=2026-03-01）❌ ← 唯一阻断项

B_gate: CLEARED ✅（Phase 2.1 收口）
  garbledCount: 0 ✅
  usableCount: 4（VALID+DEGRADED）✅
  referenceableCount: 2（VALID 级别，薛洪言、连平）✅
  reportableCount: 3（薛洪言、连平、周茂华）✅
  isReliableForReport: True ✅

C_gate: CLEARED ✅
  gateBlockers: 0
  postApprovalFollowups: 15（不阻断reportPrep）
  closed: 2
```

**说明**：
- A gate 阻断：仅 `rate_observedAt` 落后（2025-12-01），需导入 2026-03 月贷款利率数据
- B gate 已 cleared：Layer 3 提取 + VALID 语义门控 + quarantine 配置驱动 + 周报引用规则全部落地
- C gate 清零：所有 pending 项均已给出决策

### 1.2 主链路 smoke test（`--fast`）结果

```
✅ 59 项 PASS | ⚠️ 0 项 WARN | ❌ 0 项 FAIL
```

**通过项摘要**：
- `tracking-items.json`：`total=17`，所有 trackingStatus 合规，无重复 id
- `weekly-report-draft.md`：9572 字符，必含 8 个章节，第九节一致性通过
- `report-tracking 链路`：第九+十节内容真实，无兜底模式残留
- `bundle(app-data.js)`：17 items，trackingStatusSummary 与 JSON 一致，新鲜度 0s 差距
- 偏好/模板/规则：全部 17 个文件结构完整

---

## 二、单一真相源对账

### 2.1 Gate 数据流（Phase 2 约定）

```
[源]                    [生成脚本]              [产物]
─────────────────────────────────────────────────────────────
reviews/review-log.jsonl → build_review_status.py → reports/review-status.json
                                            ↓
                              build_tracking_items.py → reports/tracking-items.json
                                            ↓
                    rebuild_go_live_gate.py ──────────────────→ reports/go-live-gate.json
                         (A/B/C gate 唯一生成入口)              ↓
                                                           reports/run-summary.json
                                                          (gateType 单向同步)
                                            ↓
                              generate_weekly_report.py → reports/weekly-report-draft.md
                                            ↓
                              build_web_bundle.py → apps/web/data/app-data.js
```

**禁止路径**（Phase 2 起）：
- ❌ `run-pipeline.py` 的 `generate_run_summary()` 独立计算 `readinessLevels`
- ❌ `sync_after_review.py` 调用 `rebuild_c_gate.py` 而非 `rebuild_go_live_gate.py`
- ❌ 其他脚本直接写入 `go-live-gate.json`

### 2.2 关键文件契约

| 文件 | 消费者 | 更新频率 | 维护入口 |
|------|--------|----------|----------|
| `go-live-gate.json` | sync_after_review, run-summary, 前端 | 每次 review/tracking 变更后 | `rebuild_go_live_gate.py` |
| `run-summary.json` | human readable, cron health check | 每次 pipeline/sync 执行后 | `run-pipeline.py`, `sync_after_review.py` |
| `tracking-items.json` | 周报第九+十节, bundle, gate C | 每次 review/tracking 变更后 | `build_tracking_items.py` |

---

## 三、Analyst 质量语义现状

### 3.1 当前数据

```
原始记录: 5 条
质量分层: VALID=0 | DEGRADED=5 | GARBLED=0 | PLACEHOLDER=0
usableCount:     5（VALID+DEGRADED，内容可读）
referenceableCount: 0（VALID 级别）
reportableCount: 0（无记录满足进入周报阈值）
isReliableForReport: False（因 reportableCount=0）
B_gate: blocked/marginal
```

### 3.2 Phase 2 字段语义

| 字段 | 当前值 | 含义 |
|------|--------|------|
| `isUsable` | 5条为True | 内容可读（非乱码非占位）|
| `isReferenceable` | 0条为True | VALID级别，值得引用 |
| `isReportable` | 0条为True | 已进入周报 |
| `usableCount` | 5 | VALID+DEGRADED |
| `referenceableCount` | 0 | 仅VALID |
| `reportableCount` | 0 | 已进周报 |
| `isReliableForReport` | False | GARBLED==0 AND usable>=3 AND reportable>=1 |

### 3.3 B gate 清除路径

当前阻断项：**reportableCount=0**（无记录进入周报）

解除方案：
```bash
# 方案A: 运行 batch_verify_analyst 补充高质量来源
python3 scripts/batch_verify_analyst.py --status
python3 scripts/batch_verify_analyst.py  # 默认批次大小=2

# 方案B: 直接跑 fetch（可能引入乱码）
python3 scripts/fetch_analyst_articles.py
python3 scripts/build_analyst_opinions.py
```

---

## 四、CLI 对齐状态

### 4.1 run-pipeline.py 标志（已验证）

```
--full          完整刷新（含数据解析+analyst+周报+bundle+smoke）
--parse-only    仅数据解析
--report-only   仅周报重生成
--rebuild-only  仅周报+tracking+bundle（不跑解析） ← 常用！
--track-only    仅 tracking 重建
--smoke-only    仅 smoke test
```

### 4.2 文档对齐

| 文档 | 状态 |
|------|------|
| `docs/trial-runbook.md` | ✅ 已更新 `--mode full` → `--full` |
| `ops/cron.example` | ✅ 已更新 |
| `scripts/schedule-example.sh` | ✅ 已更新为相对路径 |
| `docs/SOP_EXECUTION.md` | ✅ 已补充路径说明 |

### 4.3 调度入口

```bash
# 日常刷新（工作日 08:00）
python3 scripts/run-pipeline.py --rebuild-only

# 周报刷新（每周五 08:00）
python3 scripts/run-pipeline.py --full

# review/tracking 变更后同步
python3 scripts/sync_after_review.py --confirm
```

---

## 五、路径架构（Phase 2）

```
ai-radar-station/
├── scripts/
│   ├── paths.py              ← 统一路径配置（Phase 2 新增）
│   ├── rebuild_go_live_gate.py  ← Gate 单一真相源
│   ├── sync_after_review.py     ← 同步链路主入口
│   ├── build_analyst_opinions.py ← Analyst 质量计算
│   └── ...
├── reports/
│   ├── go-live-gate.json       ← Gate 唯一写入点
│   ├── run-summary.json         ← 消费 gateSnapshot
│   └── ...
└── docs/
    ├── PHASE2_CHANGES.md        ← 本次变更说明
    └── BASELINE_STATE.md        ← 本文档
```
