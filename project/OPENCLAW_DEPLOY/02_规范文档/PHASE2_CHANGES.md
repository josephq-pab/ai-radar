# Phase 2 基线收敛 — 变更说明

> 版本：v2-baseline | 日期：2026-04-02 | 状态：已验证通过

---

## 一、变更概览

本次变更不扩新业务模块，聚焦基础设施收敛，共涉及 6 个脚本 + 4 个文档：

| 任务 | 范围 | 变更类型 |
|------|------|----------|
| T2 路径配置化 | 所有脚本 | 基础设施 |
| T3 Gate 单一真相源 | rebuild_go_live_gate.py | 基础设施 |
| T4 同步链路接入 | sync_after_review.py | 基础设施 |
| T5 Analyst 质量语义 | build_analyst_opinions.py + rebuild_go_live_gate.py | 语义重构 |
| T6 文档与调度漂移 | 4 个文档 + schedule-example.sh | 文档修复 |
| T7 硬编码清理 | smoke_test.py | 清理 |

---

## 二、详细变更

### T2：路径配置化 — `scripts/paths.py`（新增）

**问题**：所有脚本各自硬编码 `BASE = Path('/Users/josephq/.openclaw/workspace/projects/ai-radar-station')`，无法复现。

**变更**：
- 新增 `scripts/paths.py`，作为项目路径的单一配置源
- 所有脚本统一 `from paths import BASE, SCRIPTS, REPORTS, ...`
- 支持从 `paths.py` 所在目录自动推算项目根（`BASE = __file__` → scripts → 项目根）
- 兼容回退：若 `paths.py` 未部署，自动降级为相对路径

**已更新脚本**（共 7 个）：
`paths.py`(新增) · `rebuild_go_live_gate.py` · `sync_after_review.py` · `smoke_test.py`

---

### T3：Gate 单一真相源 — `scripts/rebuild_go_live_gate.py`

**问题**：`run-pipeline.py` 的 `generate_run_summary()` 独立计算 `readinessLevels`/`gateType`，与 `rebuild_go_live_gate.py` 产生数据分歧。

**变更**：
- `rebuild_go_live_gate.py` 成为 A/B/C gate 的唯一生成入口
- 新增 `sync_run_summary()` 将 gate 结果单向同步至 `run-summary.json`（单向同步，禁止反向写入）
- B gate 清除标准更新为 Phase 2 语义（见 T5）
- `check_consistency()` 校验 `go-live-gate.json` 与 `run-summary.json` 一致性

**数据流**：
```
rebuild_go_live_gate.py（唯一入口）
    ├── A gate → go-live-gate.json[gates.A_dataFreshness]
    ├── B gate → go-live-gate.json[gates.B_analystQuality]
    ├── C gate → go-live-gate.json[gates.C_pendingCompletion]
    └── gateType → go-live-gate.json[readinessLevels.reportPrepReadiness.gateType]
                        ↓ 单向同步（不反向写入）
                   run-summary.json[readinessLevels]
```

---

### T4：同步链路接入 — `scripts/sync_after_review.py`

**问题**：`sync_after_review.py` 第3步调用 `rebuild_c_gate.py`（仅C gate），A/B gate 未被纳入同步链路。

**变更**：
- 第3步替换为 `rebuild_go_live_gate.py`（覆盖 A/B/C 全量 gate）
- `build_review_status.py` → `build_tracking_items.py` → `rebuild_go_live_gate.py` → `generate_weekly_report.py` → `build_web_bundle.py` → fast-check
- `fast-check` 不再独立计算 gate，改为直接读取 `go-live-gate.json`
- `run-summary` 更新增加 `gateSnapshot` 字段（来自 `go-live-gate.json`）
- fast-check 新增 `go-live-gate.json` 文件存在性和新鲜度校验

**Step 对照**：
| 步骤 | Phase 1 | Phase 2 |
|------|---------|---------|
| 3 | `rebuild_c_gate.py`（仅C） | `rebuild_go_live_gate.py`（A+B+C）|
| 6 | fast-check（独立计算gate）| fast-check（读go-live-gate.json）|

---

### T5：Analyst 质量语义重构 — `scripts/build_analyst_opinions.py`

**问题**：`DEGRADED` 记录同时设置 `isReferenceable=True`，导致：
1. `referenceableCount` 包含 DEGRADED，与"可引用"语义冲突
2. B gate 中 `referenceableCount>=3` 被 DEGRADED 满足，但 `isReliableForReport` 仍为 True，两者逻辑打架

**Phase 2 语义约定**（字段级）：

| 字段 | 含义 | GARBLED | PLACEHOLDER | DEGRADED | VALID |
|------|------|---------|-------------|----------|-------|
| `isUsable` | 内容可读，非乱码非占位 | ❌ | ❌ | ✅ | ✅ |
| `isReferenceable` | 值得引用（仅VALID） | ❌ | ❌ | ❌ | ✅ |
| `isReportable` | 已进入周报 | ❌ | ❌ | ❌ | ✅（满足阈值）|

**Summary 层字段**：

| 字段 | Phase 1 | Phase 2 |
|------|---------|---------|
| `referenceableCount` | VALID + DEGRADED（含糊）| 仅 VALID |
| `usableCount` | — | VALID + DEGRADED（新增）|
| `reportableCount` | — | 已进入周报（新增）|
| `isReliableForReport` | `GARBLED==0 AND referenceable>=3` | `GARBLED==0 AND usable>=3 AND reportable>=1` |

**B gate 清除标准变更**：
- Phase 1：`garbledCount==0 AND referenceableCount>=3 AND isReliableForReport==true`
- Phase 2：`garbledCount==0 AND usableCount>=3 AND reportableCount>=1`

**影响范围**：
- `build_analyst_opinions.py`：修改 `classify_analyst_record()` 和 summary 统计逻辑
- `rebuild_go_live_gate.py`：B gate 读取新字段，使用新阈值

---

### T6：文档与调度漂移修复

#### 6.1 `docs/trial-runbook.md`
- ❌ 错误：`python3 scripts/run-pipeline.py --mode full`
- ✅ 正确：`python3 scripts/run-pipeline.py --full`
- 新增：sync_after_review.py 使用说明

#### 6.2 `ops/cron.example`
- ❌ 错误：`--mode full`、`./scripts/schedule-example.sh daily`
- ✅ 正确：`--full`（独立标志）、`python3 scripts/run-pipeline.py --rebuild-only`
- 新增：CLI 标志说明注释

#### 6.3 `scripts/schedule-example.sh`
- ❌ 错误：硬编码 `PROJECT_DIR="/Users/josephq/..."`
- ✅ 正确：从脚本自身位置动态推算（`dirname "$0"`）
- 修复：`check_health()` 兼容无 `exitCode` 字段的旧版 run-summary.json
- 修复：mode 分支 `smoke` 使用 `smoke_test.py --fast` 而非内联脚本

#### 6.4 `docs/SOP_EXECUTION.md`
- 新增 Phase 2 路径说明注释

---

### T7：硬编码清理 — `scripts/smoke_test.py`

**问题**：`run_pending_aging()` 中存在：
```python
WAITING_FOR_DATA = {'1dbd4051cc58'}
WAITING_FOR_BUSINESS = {'581527c09784'}
```
这两个 ID 早已不存在于系统，集合为失效硬编码。

**变更**：
- 删除 `WAITING_FOR_DATA`、`WAITING_FOR_BUSINESS` 两个硬编码集合
- 分类逻辑改为从 `review-log.jsonl` 实时读取 decision 动态推导：
  - `decision in ('', 'pending')` → `needs-review`
  - `decision in ('approve','modify')` + `trackingStatus='跟踪中'` → `waiting-for-business-decision`
  - `decision in ('approve','modify')` + `trackingStatus='已上报'` → `waiting-for-data`
- `smoke_test.py` BASE 路径改为 `from paths import ...`（兼容回退）

---

## 三、约束遵守情况

| 约束 | 状态 |
|------|------|
| 不引入数据库/API/UI框架大改 | ✅ 未动 |
| 不改历史 review-log.jsonl，只允许追加 | ✅ 未动 |
| 不在缺少 2026-03 原始数据时跑 `import_monthly_data.py --confirm` | ✅ 未动 |
| 不直接跑全量 `fetch_analyst_articles.py`，保留 batch_verify_analyst 机制 | ✅ 未动 |

---

## 四、向后兼容性说明

- `analyst_opinions.json` 仍保留 `referenceableCount` 字段（值为仅 VALID 的数量），兼容旧消费者
- `go-live-gate.json` 新增 `bGateClearCriteria` 字符串字段，说明当前清除标准
- `smoke_test.py` 的 `validate_analyst_opinions()` 仍检查 `qualityTier` 字段，兼容 Phase 1 数据

---

## 五、Phase 2.1 增量变更（2026-04-03）

> 本次变更聚焦 B gate 语义收口和周报引用规则，**不扩新业务模块，不改 Phase 2 基线语义**。

| 任务 | 范围 | 性质 |
|------|------|------|
| P2.1-A 字段兼容层修复 | build_analyst_opinions.py | bugfix |
| P2.1-B Layer 3 提取 | build_analyst_opinions.py | 新增 |
| P2.1-C VALID 语义门控 | build_analyst_opinions.py | 语义修正 |
| P2.1-D quarantine 配置驱动 | build_analyst_opinions.py | 架构优化 |
| P2.1-E 周报引用规则 | generate_weekly_report.py | 规则补全 |

### P2.1-A：字段兼容层修复

**问题**：`setdefault()` 只处理字段不存在，不处理字段存在但为空字符串，导致 fallback 逻辑失效。

**变更**：
```python
# Before
record.setdefault('articleTitle', record.get('title', ''))
# After
record['articleTitle'] = record.get('articleTitle') or record.get('title', '')
record['analystName'] = record.get('analystName') or record.get('sourceName', '')
record['sourceUrl'] = record.get('sourceUrl') or record.get('url', '')
record['publishedAt'] = record.get('publishedAt') or record.get('fetchedAt', '')
```

### P2.1-B：Layer 3 内容提取

**问题**：`content` 非空但 `keyViewpoints`/`evidenceSnippets` 全为空 → `actionabilityScore=0` → 无记录进周报。

**变更**：新增 `extract_viewpoints_and_snippets(record)` 函数，在评分之前执行：
- 触发条件：content≥200字 + viewpoints=[] + snippets=[] + 内容质量预检通过（非浏览器错误页，非2023年前旧文）
- viewpoints：显式分析师引语（`XXX表示/指出/认为...`）≥25字，或预判类长句≥40字；排除新闻套话
- snippets：含 `%/亿元/增长` 等数字关键词≥25字；排除标题重复句

**Before/After（薛洪言、连平）**：
- viewpoints: 0→2，snippets: 0→3，rel: 0.2→0.85，act: 0.0→0.6，qualityTier: DEGRADED→VALID

### P2.1-C：VALID 语义门控（`_post_extraction_quality_gate`）

**问题**：VALID 仅检查标题长度≥10字，不验证正文是否有分析师观点；记者转写稿标题长也会被判为 VALID。

**变更**：Layer 3 提取完成后，`classify_analyst_record()` 之后追加 `_post_extraction_quality_gate()`：
- VALID 文章若 viewpoints=0 且 snippets 中无明确分析师引语 → 降级 DEGRADED
- `_is_analyst_evidence()`：判断 snippet 是否为分析师正式引语（排除"银行工作人员表示"等记者转写）
- 降级后仍可进入周报（isReportable 由 decide_enter_report 决定），但 isReferenceable=False

**周茂华案例**：
- 记者转写稿（银行员工表示...）→ 标题长判 VALID → Layer 3 无 viewpoints → 降级 DEGRADED → isReferenceable=False → 周报写入"市场信息"而非"分析师观点" ✅

### P2.1-D：quarantine 配置驱动

**问题**：`QUARANTINED_SOURCES = frozenset(['analyst-deposit-001'])` 硬编码在代码中。

**变更**：
- 删除硬编码 `QUARANTINED_SOURCES`
- 新增 `_load_inactive_source_ids()`：运行时读取 `config/analyst_sources.json` 中 `active: false` 的 source ID
- 过滤在去重循环之前执行
- `analyst_sources.json` 中 `analyst-deposit-001` 标记 `active: false` + `_quarantine` 字段

**单一真相源**：`config/analyst_sources.json`（唯一） > `build_analyst_opinions.py`（运行时读配置）

### P2.1-E：周报引用规则（`isReferenceable` 分叉写入）

**问题**：所有 `enterReport=True` 记录统一冠以"分析师姓名"写入，DEGRADED 记者转写内容被误标为"分析师观点"。

**变更**（`generate_weekly_report.py`）：
| 条件 | 写法 |
|------|------|
| `isReferenceable=True`（VALID） | `#### 薛洪言（研究员）` + `核心观点：` + 归因给分析师 |
| `isReferenceable=False`（DEGRADED） | `#### 文章标题片段` + `市场信息：` + 注"不可直接引用为分析师观点" |

---

## 六、Phase 2.1 约束遵守

| 约束 | 状态 |
|------|------|
| 不为清 B gate 放松 VALID 语义 | ✅ 周茂华降级为 DEGRADED，isReferenceable=False |
| quarantine 不硬编码 | ✅ 配置驱动，从 analyst_sources.json 读取 |
| 周报不写无归因分析师句 | ✅ DEGRADED 写"市场信息"，不冠分析师名 |
| 不继续横向扩 B 层功能 | ✅ 本次收口，未扩新模块 |
