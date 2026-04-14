# 对公AI雷达站 Phase 2 基线收敛 — 结项报告

> 项目：对公AI雷达站 Phase 2 基线收敛
> 时间：2026-04-02
> 执行：Sylvia
> 状态：**已完成（已验证）**

---

## 一、任务目标回顾

将"对公AI雷达站"从可在原作者环境运行的一阶段MVP，收敛为可移交、可复现、可扩展的二阶段基线版本。

本轮优先级：

| 优先级 | 任务 | 类型 |
|--------|------|------|
| P1 | 路径基础设施：移除所有脚本绝对路径 | 基础设施 |
| P2 | Gate单一真相源：A/B/C gate统一由一处生成 | 基础设施 |
| P3 | 同步链路接入：rebuild_go_live_gate.py接入sync_after_review | 基础设施 |
| P4 | Analyst质量语义：拆分usable/referenceable/reportable，消除DEGRADED冲突 | 语义重构 |
| P5 | 文档与调度修正：SOP/trial-runbook/cron.example/schedule对齐CLI | 文档修复 |
| P6 | 清理smoke_test.py中失效的硬编码ID集合 | 清理 |

---

## 二、交付物清单

### 2.1 新增文件

| 文件 | 说明 |
|------|------|
| `scripts/paths.py` | 统一路径配置模块，项目内所有脚本的路径来源 |
| `docs/PHASE2_CHANGES.md` | 变更说明文档 |
| `docs/BASELINE_STATE.md` | 现状对齐文档 |
| `docs/OPEN_ISSUES.md` | 未决事项清单 |
| `docs/DRYRUN_VERIFICATION.md` | Dry-run/Fast-check 验证报告 |

### 2.2 修改文件

| 文件 | 变更摘要 |
|------|----------|
| `scripts/rebuild_go_live_gate.py` | 接入paths.py；B gate改用Phase 2质量语义；assess_c_gate路径修正 |
| `scripts/sync_after_review.py` | 第3步改用rebuild_go_live_gate.py（覆盖A+B+C）；fast-check改读go-live-gate.json；run-summary增加gateSnapshot |
| `scripts/build_analyst_opinions.py` | classify_analyst_record()重构；新增usableCount/reportableCount；isReliableForReport逻辑修正 |
| `scripts/smoke_test.py` | 删除WAITING_FOR_DATA/WAITING_FOR_BUSINESS硬编码；分类改为动态review-log推导；BASE路径改用paths.py |
| `scripts/schedule-example.sh` | 硬编码路径改为dirname动态推算；CLI标志修正；check_health兼容旧版run-summary |
| `docs/trial-runbook.md` | `--mode full`→`--full`；新增sync_after_review使用说明 |
| `docs/SOP_EXECUTION.md` | 补充Phase 2路径说明 |
| `ops/cron.example` | CLI标志修正；新增标志说明注释 |

---

## 三、核心变更详解

### 3.1 路径配置化（paths.py）

所有脚本统一从`paths.py`导入路径，消除了散落在13个脚本中的硬编码绝对路径：

```python
# Before
BASE = Path('/Users/josephq/.openclaw/workspace/projects/ai-radar-station')

# After
from paths import BASE, SCRIPTS, REPORTS, PROCESSED, ...
```

自举机制：从`__file__`所在目录向上两级推导项目根目录，无需任何环境变量或硬编码。

### 3.2 Gate单一真相源

```
A/B/C gate + readinessLevels + gateType + blockers + goLiveCriteria
统一由 rebuild_go_live_gate.py 生成，禁止其他脚本独立计算。

rebuild_go_live_gate.py（唯一入口）
    ├── 写入 go-live-gate.json（全部gate数据）
    └── 单向同步 gateType → run-summary.json
```

同步链路`sync_after_review.py`第3步已从`rebuild_c_gate.py`（仅C）升级为`rebuild_go_live_gate.py`（A+B+C全量）。

### 3.3 Analyst质量语义重构

| 字段 | Phase 1 | Phase 2 |
|------|---------|---------|
| DEGRADED.isReferenceable | `True`（矛盾） | `False` |
| usableCount | — | `VALID + DEGRADED`（新增）|
| reportableCount | — | `已进入周报`（新增）|
| isReliableForReport | `GARBLED==0 AND refCount>=3` | `GARBLED==0 AND usable>=3 AND reportable>=1` |

B gate清除标准：Phase 1会被DEGRADED欺骗清除，Phase 2必须内容真实进周报才能清除。

### 3.4 文档与调度对齐

| 漂移点 | Phase 1 | Phase 2 |
|--------|---------|---------|
| run-pipeline.py CLI | `--mode full`（错误）| `--full` |
| schedule-example.sh | 硬编码绝对路径 | dirname动态推算 |
| cron.example | `./scripts/schedule-example.sh daily` | `python3 scripts/run-pipeline.py --rebuild-only` |
| trial-runbook.md | 无sync_after_review说明 | 新增同步链路使用说明 |

---

## 四、验证结果

### 4.1 语法校验
```
py_compile: paths.py + smoke_test.py + sync_after_review.py + rebuild_go_live_gate.py + build_analyst_opinions.py
结果：All syntax OK
```

### 4.2 sync_after_review.py dry-run
```
步骤序列：build_review_status → build_tracking_items → rebuild_go_live_gate → generate_weekly_report → build_web_bundle
演练完成，未写入任何文件 ✅
```

### 4.3 rebuild_go_live_gate.py --check
```
A_gate:  BLOCKED（数据新鲜度，非本次变更引入）
B_gate:  MARGINAL（Phase 2语义生效 ✅）
  - garbledCount=0    cleared
  - usableCount=5     cleared（>=3）
  - reportableCount=0 blocked（<1）
C_gate:  CLEARED ✅
  - gateBlockers: 0
  - postApprovalFollowups: 15
一致性检查：1条WARN（run-summary待sync同步）
```

### 4.4 smoke_test.py --fast
```
✅ 59 项 PASS | ⚠️ 0 项 WARN | ❌ 0 项 FAIL
```

覆盖范围：tracking-items、weekly-report第九+十节一致性、report-tracking链路真实性、bundle一致性（17 items）、偏好/模板/规则文件（17个）。

### 4.5 build_analyst_opinions.py
```
质量分层：VALID=0 | DEGRADED=5 | GARBLED=0 | PLACEHOLDER=0
usableCount=5 ✅ | referenceableCount=0（Phase 2关键修复）| reportableCount=0
B_gate: blocked/marginal（预期，因无可进周报记录）
```

**关键验证**：Phase 1会将DEGRADED的isReferenceable=True，导致referenceableCount=5（错误），Phase 2正确计为0。

---

## 五、约束遵守情况

| 约束 | 状态 |
|------|------|
| 不引入数据库/API/UI框架大改 | ✅ 未动 |
| 不改历史review-log.jsonl，只允许追加 | ✅ 未动 |
| 不在缺少2026-03原始数据时跑import_monthly_data.py --confirm | ✅ 未动 |
| 不直接跑全量fetch_analyst_articles.py，保留batch_verify_analyst | ✅ 保留 |

---

## 六、未决事项

### P0（阻断正式汇报）

| 事项 | 说明 | 解决方案 |
|------|------|----------|
| O-1：A gate数据新鲜度 | observedAt均为2026-02，需更新至2026-03 | 取得原始数据后执行import_monthly_data.py --confirm |
| O-2：B gate reportableCount=0 | analyst记录全为DEGRADED，需batch_verify补充高质量来源 | python3 scripts/batch_verify_analyst.py |

### P1（影响可信度）

| 事项 | 说明 | 优先级 |
|------|------|--------|
| O-3：run-summary与go-live-gate一致性警告 | sync_after_review --confirm后消除 | 尽快处理 |
| O-4：smoke_test.py的check_baseline()未被调用 | 独立函数，main()未接入 | 次优先 |

---

## 七、基线质量评估

| 维度 | Phase 1 | Phase 2 |
|------|---------|---------|
| 可复现性 | ❌ 硬编码路径，散布13个脚本 | ✅ paths.py单一配置源 |
| Gate一致性 | ❌ 多处独立计算，分歧风险 | ✅ 单一真相源，单向同步 |
| 同步链路完整性 | ❌ sync只处理C gate | ✅ sync处理A+B+C全量 |
| Analyst质量语义 | ❌ DEGRADED与isReliableForReport冲突 | ✅ 四层语义清晰，无歧义 |
| 硬编码残留 | ❌ 失效ID集合残留于smoke_test | ✅ 动态推导，无硬编码 |
| 文档CLI一致性 | ❌ `--mode full`等漂移 | ✅ 全部对齐 |

**整体评估**：Phase 2基线达到可移交标准。基础设施收敛完成，语义清晰，文档与代码一致。P0未决项为数据依赖问题，不影响基线质量。

---

## 九、Phase 2.1 增量结项（2026-04-03）

> 执行：Sylvia | 状态：**已完成（已验证）**

### 9.1 任务目标

收口 B gate 语义和周报引用规则，不扩新模块。

### 9.2 完成项

| 任务 | 交付物 | 验证 |
|------|--------|------|
| P2.1-A 字段兼容层修复 | `articleTitle`/`analystName`/`sourceUrl`/`publishedAt` 支持空字符串回退 | 运行无 KeyError |
| P2.1-B Layer 3 提取 | `extract_viewpoints_and_snippets()` 从薛洪言/连平正文提取 viewpoints+snippets | rel 0.2→0.85，act 0.0→0.6 |
| P2.1-C VALID 语义门控 | `_post_extraction_quality_gate()` 将记者转写稿降级 DEGRADED | 周茂华 isReferenceable=False ✅ |
| P2.1-D quarantine 配置驱动 | `_load_inactive_source_ids()` 读 `analyst_sources.json`，删除硬编码 |董希淼 quarantine ✅，garbledCount=0 |
| P2.1-E 周报引用规则 | `isReferenceable` 分叉写入 | 周茂华写"市场信息" ✅ |

### 9.3 B gate 最终状态（2026-04-03）

```
garbledCount: 0 ✅
usableCount: 4（VALID 2 + DEGRADED 2）✅
referenceableCount: 2（VALID：薛洪言、连平）✅
reportableCount: 3（薛洪言、连平、周茂华）✅
isReliableForReport: True ✅
B gate: CLEARED ✅
```

### 9.4 周报引用示例（周茂华）

**Before**：标题冠以"周茂华"，数据写"关键数据"，读者误以为是周茂华分析
**After**：`#### 大额存单利率下降却仍是"香饽饽"...` + `市场信息：` + `注：不可直接引用为分析师观点` ✅

### 9.5 全链路验证

```
smoke_test --fast: 59/59 PASS ✅
smoke_test --baseline: 全部通过，无回归 ✅
rebuild_go_live_gate --check: B CLEARED / C CLEARED / A BLOCKED ✅
一致性检查: OK ✅
```

### 9.6 当前唯一阻断项

**A gate（rate 数据缺口）**：`loan_rate.json` observedAt = 2025-12-01，目标 ≥ 2026-03-01。
需导入 2026-03 月贷款利率原始 Excel 后执行 `import_monthly_data.py --confirm`。

### 9.7 Phase 2.1 结论

B gate 语义已收口，quarantine 机制配置化，周报引用规则清晰。Phase 2.1 达到结项标准。

---

## 八、后续建议

1. **立即**：执行batch_verify_analyst.py提升B gate至cleared状态
2. **数据就绪后**：执行import_monthly_data.py --confirm清除A gate阻断
3. **确认数据后**：执行sync_after_review.py --confirm完成首次全量同步
4. **下阶段**：考虑将run-pipeline.py的readiness_levels计算也统一到go-live-gate.json读取模式
