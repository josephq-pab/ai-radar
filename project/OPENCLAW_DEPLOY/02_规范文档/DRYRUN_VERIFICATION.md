# Phase 2 基线 — Dry-run / Fast-check 验证报告

> 验证时间：2026-04-02 09:59 CST | 验证人：Sylvia

---

## 一、验证环境

```bash
python3 scripts/paths.py
# BASE = /Users/josephq/.openclaw/workspace/projects/ai-radar-station
# 所有路径 ✅ 解析正常
```

---

## 二、语法校验

```bash
python3 -m py_compile scripts/paths.py scripts/smoke_test.py \
  scripts/sync_after_review.py scripts/rebuild_go_live_gate.py \
  scripts/build_analyst_opinions.py
# 结果：All syntax OK ✅
```

---

## 三、sync_after_review.py dry-run

```
模式: DRY-RUN（演练）

步骤计划：
  1. build_review_status.py         ✅
  2. build_tracking_items.py        ✅
  3. rebuild_go_live_gate.py        ✅（Phase 2: 已替换 rebuild_c_gate.py）
  4. generate_weekly_report.py      ✅
  5. build_web_bundle.py            ✅

演练输出：✅ 演练完成，未写入任何文件
```

**验证结论**：步骤序列正确，`rebuild_go_live_gate.py` 已接入（替换 Phase 1 的 `rebuild_c_gate.py`）。

---

## 四、rebuild_go_live_gate.py --check

```
A_gate: BLOCKED（预期，数据新鲜度问题，非本次变更引入）
  deposit: 2026-02-28 < 2026-03-01 ❌
  loan:    2026-02-28 < 2026-03-01 ❌
  rate:    2025-12-01 < 2026-03-01 ❌

B_gate: MARGINAL（Phase 2 语义已生效 ✅）
  garbledCount=0      ✅ cleared
  usableCount=5       ✅ cleared（>=3）
  reportableCount=0   ❌ blocked（<1）
  isReliableForReport=False ❌ blocked（因reportable=0）
  差距: reportableCount=0
  清除标准: garbledCount=0 AND usableCount>=3 AND reportableCount>=1 ✅

C_gate: CLEARED ✅
  gateBlockers: 0
  postApprovalFollowups: 15
  closed: 2

一致性检查:
  WARN: B_analystQuality: go-live-gate=blocked，但 run-summary 未列入
  （预期，run-summary 待 sync_after_review 同步）
```

**Phase 2 B gate 语义验证**：
- ✅ `usableCount=5`（VALID+DEGRADED，内容可读）
- ✅ `referenceableCount=0`（VALID 级别，仅 0 条）
- ✅ `reportableCount=0`（无记录进周报）
- ✅ `isReliableForReport=False`（因 reportable=0）
- ✅ 清除标准显示 `garbledCount=0 AND usableCount>=3 AND reportableCount>=1`

---

## 五、smoke_test.py --fast

```
模式: 快速校验（主链路一致性）

汇总: ✅ 59 | ⚠️ 0 | ❌ 0

全部通过 ✅
```

**覆盖范围**：
- `tracking-items.json`：17 items，trackingStatus 全部合规
- `weekly-report-draft.md`：9572 字符，8 个必含章节，第九节一致性通过
- `report-tracking 链路`：第九+十节内容真实，无兜底残留
- `bundle(app-data.js)`：trackingItems=17，trackingStatusSummary 一致，新鲜度 0s
- 偏好/模板/规则：17 个文件结构完整

---

## 六、build_analyst_opinions.py

```
原始记录: 5 条
去重后: 5 条
质量分层: VALID=0 | DEGRADED=5 | GARBLED=0 | PLACEHOLDER=0

Phase 2 字段验证:
  usableCount=5          ✅ DEGRADED=5 → isUsable=True
  referenceableCount=0   ✅ DEGRADED NOT referenceable
  reportableCount=0      ✅ 无记录进周报
  isReliableForReport=False ✅ (garbled=0 AND usable>=3 AND reportable>=1)
  B_gate: blocked/marginal ✅
```

**关键验证**：
- Phase 1 会将 DEGRADED 的 `isReferenceable=True`，导致 `referenceableCount=5` 错误清除 B gate
- Phase 2 DEGRADED 的 `isReferenceable=False`，`referenceableCount=0` 正确反映

---

## 七、路径解析验证

```bash
python3 scripts/paths.py
# ✅ BASE       = /Users/josephq/.openclaw/workspace/projects/ai-radar-station
# ✅ SCRIPTS    = .../scripts  ✅
# ✅ DATA       = .../data      ✅
# ✅ PROCESSED  = .../data/processed  ✅
# ✅ REPORTS    = .../reports   ✅
# ✅ REVIEWS    = .../reviews   ✅
# ✅ WEB_DATA   = .../apps/web/data  ✅
```

---

## 八、文档对齐验证

| 文档 | 验证点 | 状态 |
|------|--------|------|
| `docs/trial-runbook.md` | 无 `--mode full` 错误引用 | ✅ |
| `ops/cron.example` | CLI 标志为 `--full`/`--rebuild-only` | ✅ |
| `scripts/schedule-example.sh` | 无硬编码绝对路径 | ✅ |
| `docs/SOP_EXECUTION.md` | 有路径说明注释 | ✅ |

---

## 九、总体结论

| 验证项 | 结果 |
|--------|------|
| Python 语法 | ✅ 全部通过 |
| 路径解析 | ✅ 全部正确 |
| sync_after_review dry-run | ✅ 步骤序列正确 |
| rebuild_go_live_gate --check | ✅ A/B/C gate 逻辑正确 |
| smoke_test --fast | ✅ 59/59 通过 |
| Analyst 质量语义 | ✅ Phase 2 语义生效 |
| 文档对齐 | ✅ 全部修正 |

**结论**：Phase 2 基线基础设施验证通过，可进入下一阶段。
