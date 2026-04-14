# PHASE3_TASK_PACKAGE.md — Phase 3 任务包

> 文档版本：v1.7（本次更新：P1-3 试点运行 SOP 实施完成）
> 版本历史：
> - v1.0（2026-04-07）：按模板初建
> - v1.1（2026-04-07）：P1-2重写（明确review→确认→留痕→形成规则）；M4验收口径更新
> - v1.2（2026-04-07）：P0-2 实施完成（路径统一 + confirmLevel注入 + SKIP_OLD过滤修复）
> - v1.3（2026-04-07）：P0-3 实施完成（reviewStatus+trackingStatus落地 + M4b演示）

---

## 任务包说明

本文档定义 Phase 3 所有任务的边界、优先级、依赖关系和验收口径。

**优先级定义**：
- P0：MVP 闭环必需，当前 sprint 必须完成
- P1：有助于提升可用性，可稍后
- P2：记录在案，本阶段不推进

**变更机制**：所有任务新增/修改必须经 CHANGE_CONTROL 记录，不得直接在任务包中扩展。

---

## P0 任务

---

### 任务 P0-1

- **编号**：P0-1
- **任务名称**：前端页面试点运行验证
- **对应推进点**：输出分层、周期管理
- **任务目的**：验证前端页面可正常展示最近一次抓取结果
- **解决的问题**：8787 端口服务曾中断，需确认恢复后页面可访问
- **输入**：03_前端页面/index.html；最近一次 analyst_opinions_raw.json
- **输出**：前端页面可访问且数据可读
- **依赖**：M1（运行入口稳定）✅ 已完成
- **是否阻断试点**：✅ 是
- **验收方式**：人工访问 http://47.112.211.98:8787/index.html，确认页面加载正常、有数据展示
- **当前状态**：✅ 已完成（M1 的一部分）
- **备注**：2026-04-07 已修复并验证 8787 可访问

---

### 任务 P0-2

- **编号**：P0-2
- **任务名称**：分析师观点输出分层固化
- **对应推进点**：输出分层
- **任务目的**：明确 raw / reviewed / report-ready 三层定义、字段和转化逻辑
- **解决的问题**：
  1. analyst_opinions_raw.json（79条）与 analyst_opinions.json（7条）路径不一致（build读data/，fetch写04_数据与规则/）
  2. 三层输出结构未固化
  3. confirmLevel（P1/P2/P3）未落地
  4. SKIP_OLD记录（50条2024年前旧文）混入DEGRADED统计
- **输入**：analyst_opinions_raw.json（79条）
- **输出**：
  - analyst_opinions.json（reviewed层，29条可用：VALID×25/DEGRADED×4）
  - analyst-review-queue.json（report-ready层，5条：P1×4/P2×1，confirmLevel已注入）
  - 四层结构与实际产物映射完成
- **依赖**：P0-1 完成
- **是否阻断试点**：✅ 是
- **验收方式**：
  1. build_analyst_opinions.py 路径统一到 04_数据与规则/processed/
  2. analyst_opinions.json 字段完整（qualityTier/isReferenceable/relevanceScore等）
  3. analyst-review-queue.json 每条有 confirmLevel（P1/P2/P3）
  4. usableCount=29（VALID+DEGRADED，不含SKIP_OLD）
- **当前状态**：✅ 实施完成（2026-04-07）
- **本次修正内容**：
  - PROCESSED/SOURCES_CONFIG/OUTPUT 三处路径统一到 04_数据与规则/（DECISION_LOG D-06）
  - SKIP_OLD 过滤修复（50条2024年前旧文正确剔除，不进入scored）
  - confirmLevel 注入（P1：VALID+综合分≥0.75；P2：VALID+综合分≥0.60或DEGRADED+综合分≥0.50；其余P3）
- **遗留（需后续sprint处理，不阻断当前MVP）**：
  - 来源多样性未纳入评分，导致连平（0.86分）被薛洪言（0.90分）文章挤压
  - confirmLevel为规则映射，非人工分级（人工分级需P1-1追踪表建立后补充）

---

### 任务 P0-3

- **编号**：P0-3
- **任务名称**：周期运行脚本固化
- **对应推进点**：周期管理
- **任务目的**：将分析师抓取固化为一键可执行脚本，明确运行频率和失败处理
- **解决的问题**：抓取依赖人工触发，缺少周期化运行机制；M4b 演示缺少状态字段
- **输入**：fetch_analyst_articles.py；analyst_sources.json
- **输出**：
  - 一条可执行的周期运行命令（写入 RUNBOOK.md）
  - 运行频率定义（建议：每周一执行）
  - 失败处理规则（重试次数/跳过机制）
  - 数据过期定义（多久之前的数据视为过期）
  - analyst-review-queue.json 含 reviewStatus + trackingStatus 字段（M4b 演示用）
- **依赖**：P0-2 完成
- **是否阻断试点**：✅ 是
- **验收方式**（M4b 精确验收）：
  1. analyst-review-queue.json 存在且每条有 reviewStatus（默认pending）和 trackingStatus（默认candidate/pending）
  2. 演示一次状态变更：修改一条 reviewStatus=confirmed，重读 JSON 确认变化
  3. 上述演示记录入 REVIEW_LOG
- **当前状态**：✅ 已完成（2026-04-07，M4b 演示通过）
- **本次实施内容**：
  - build_analyst_opinions.py review_items 增加 reviewStatus（默认pending）和 trackingStatus（默认candidate/pending，trackingCandidate=False时为pending）
  - analyst-review-queue.json 重新生成，含两个新字段
  - M4b 演示：analyst-72873eb4 状态变更 confirmed/follow_up，重读确认
  - OPERATING_CYCLE_DRAFT v1.1 补充 reviewStatus/trackingStatus 定义和流转规则
  - D-07 记录状态重置边界说明
- **遗留边界说明**（D-07 已记录）：
  - 重新运行 build 会将所有状态重置为 pending/candidate，不具备持久化能力
  - 持久化机制不在 Phase 3 MVP 范围内

---

## P1 任务

---

### 任务 P1-1

- **编号**：P1-1
- **任务名称**：review 状态持久化 / 独立台账
- **对应推进点**：确认项分级、周期管理
- **任务目的**：让 reviewStatus / trackingStatus 在重新 build 后不丢失
- **解决的问题**：analyst-review-queue.json 被 build 全量覆盖后，手动修改的 confirmed/follow_up 状态丢失（D-07 边界）
- **输入**：analyst-review-queue.json（build 纯输出）
- **输出**：
  - reports/review-tracker.json（独立状态台账）
  - 05_工具脚本/review-tracker.py（upsert + merge 工具）
- **依赖**：P0-3 完成
- **是否阻断试点**：⚠️ 是（体验断点，试点会立即暴露）
- **验收方式**：
  1. review-tracker.json 建立，upsert 可写
  2. merge 可输出 queue + tracker 合并状态
  3. build 重跑后 tracker 内容不丢失
  4. merge 后 confirmed/follow_up 状态仍存在
  5. itemId 跨 build 稳定性已验证（D-08）
- **当前状态**：✅ 已完成（2026-04-07，实施验证通过）
- **本次实施内容**：
  - 新增 reports/review-tracker.json（独立状态台账）
  - 新增 05_工具脚本/review-tracker.py（upsert + merge）
  - itemId 跨 build 稳定性验证通过（两次连续 build，itemId 完全一致）
  - merge 落点选方案A（独立 merge 脚本，不嵌入 build）
  - 验收场景通过：build → upsert → 再 build → merge 后 confirmed/follow_up 仍存在
- **遗留边界说明**：
  - review-tracker.json 需要人工维护 upsert（无 UI 按钮）
  - fetch-run-log（P1-1b原设计）尚未实施，属于独立待办项

---

### 任务 P1-1b

- **编号**：P1-1b
- **任务名称**：CSV 轻量追踪表
- **对应推进点**：确认项分级、周期管理
- **任务目的**：把 review queue + tracker 的状态沉淀成可导入 Excel/飞书表格的轻量追踪表
- **解决的问题**：当前 review 结果只能通过 JSON 查看，非技术人员不易读；试点需要可沟通的表格形态台账
- **输入**：analyst-review-queue.json + review-tracker.json
- **输出**：
  - reports/pilot-tracking-ledger.csv
  - review-tracker.py export 子命令
- **依赖**：P1-1 完成
- **是否阻断试点**：⚠️ 部分影响（台账形态，非阻断）
- **验收方式**：
  1. pilot-tracking-ledger.csv 存在且可被 Excel/飞书表格直接打开
  2. 字段：itemId / analystName / articleTitle / confirmLevel / reviewStatus / trackingStatus / updatedAt / note / source
  3. 无 owner/nextAction/deadline/priority 等任务系统字段
  4. build 重跑后重新导出，tracker 状态不丢失
  5. CSV 为 UTF-8-sig 编码（Excel 兼容）
- **当前状态**：✅ 已完成（2026-04-07，实施验证通过）
- **本次实施内容**：
  - 新增 review-tracker.py export 子命令
  - pilot-tracking-ledger.csv 生成（9字段，UTF-8-sig BOM，逗号分隔）
  - 字段不含任何任务系统字段
  - 验收场景通过：build → upsert → 再 build → export 后 confirmed/follow_up 仍存在
- **遗留边界说明**：
  - CSV 依赖人工 upsert + export，不是自动同步
  - 建议每月归档一次历史 CSV 版本

---

### 任务 P1-2

- **编号**：P1-2
- **任务名称**：分析师来源有效性 review
- **对应推进点**：输出分层、数据源轻管理
- **任务目的**：对来源进行 review → 确认分类 → 留痕 → 形成最终轻治理规则，不是"完成分类"而是"确认分类的过程本身"
- **解决的问题**：SOURCE_GOVERNANCE_DRAFT 中的分类是"候选初稿"，需要通过 P1-2 review 过程确认为正式分类
- **输入**：analyst_sources.json；analyst_opinions_raw.json；analyst_opinions.json；SOURCE_GOVERNANCE_DRAFT（候选分类）
- **输出**：
  - docs/analyst_review_matrix.md（证据矩阵，所有来源一行，数值可追溯）
  - docs/analyst_review_notes.md（review 结论文档，每来源一段，含结论/证据/边界/配置建议）
- **依赖**：有实际抓取数据；SOURCE_GOVERNANCE_DRAFT 候选分类作为输入参考
- **是否阻断试点**：❌ 否
- **验收方式**：
  1. analyst_review_matrix.md 存在，数值可追溯至 analyst_opinions.json
  2. analyst_review_notes.md 存在，每来源有明确结论（keep/observe/pending-check/downgrade-candidate）
  3. 结论与证据一致，无越界表述（无"已修改"/"正式生效"等）
  4. analyst_sources.json 未被自动修改
  5. 样本轮次边界已在文档中标注（单轮数据，试行版建议）
- **当前状态**：✅ 已完成（2026-04-07，实施验证通过）
- **本次实施内容**：
  - 新增 docs/analyst_review_matrix.md（证据矩阵，13个来源，数值可追溯）
  - 新增 docs/analyst_review_notes.md（结论文档，keep=2/observe=3/pending-check=7/无downgrade）
  - 顾慧君/王锟：pending-check，正确归因 min_year=2024 过滤，非来源质量差
  - 付一夫：observe，正确归因 top-k 截断，非来源质量差
  - analyst_sources.json 未被修改（配置建议是人工参考，非自动生效）
  - 样本边界已标注：本轮单轮数据，试行版建议，建议2~3轮后复核
- **遗留边界说明**：
  - analyst_sources.json 未被自动修改（待人工决策）
  - SOURCE_GOVERNANCE_DRAFT 仍为 v0.9 候选初稿（待后续升版）
  - 6个来源0 raw记录待人工核实

---

### 任务 P1-3

- **编号**：P1-3
- **任务名称**：最小试点运行 SOP / 周期机制 / 复核节奏
- **对应推进点**：确认项分级
- **任务目的**：将当前 MVP 能力组织为可执行、可复盘、可持续运行的小规模试点 SOP
- **解决的问题**：MVP 从"能演示"升级为"能按周/轮次稳定运行"，有章可循
- **输入**：analyst-review-queue.json；review-tracker.py；pilot-tracking-ledger.csv
- **输出**：
  - docs/PILOT_RUN_SOP.md（v1.0，人工操作手册）
  - docs/ROUND_RECAP_TEMPLATE.md（v1.0，每轮小结模板）
  - docs/SOURCE_REVIEW_CHECKLIST.md（v1.0，来源复核触发条件）
  - reports/ROUND_RECAP/ROUND_RECAP_2026-04-07.md（首轮小结）
- **依赖**：analyst-review-queue 可用；tracker 可 upsert；pilot-tracking-ledger.csv 可导出
- **是否阻断试点**：❌ 否
- **验收方式**：
  1. PILOT_RUN_SOP.md 存在且每步可执行
  2. ROUND_RECAP_TEMPLATE.md 存在且已填写示例
  3. 首个完整轮次（ROUND-01）已跑通
  4. 周期触发条件已在 SOP 中明确
  5. 无 cron/UI/数据库/任务系统
- **当前状态**：✅ 已完成（2026-04-07，实施验证通过）
- **本次实施内容**：
  - 新增 docs/PILOT_RUN_SOP.md（v1.0）
  - 新增 docs/ROUND_RECAP_TEMPLATE.md（v1.0）
  - 新增 docs/SOURCE_REVIEW_CHECKLIST.md（v1.0）
  - 首个完整轮次 ROUND-01 已跑通（5条 confirmed 状态）
  - 周期触发条件：双周 OR raw 新增≥5条（含例外口径）
  - 角色：单角色（运营编辑者）
- **P1-3 原规划说明**：
  - 原 P1-3 规划为"confirmLevel 规则文档化（CONFIRMABILITY_RULES.md）"
  - 该方向需基于2~3轮历史数据才有意义，已降级为"后续数据积累后推进"
  - 当前 P1-3 实施为试点运行 SOP，两者可共存，本轮只做前者
- **遗留边界说明**：
  - CONFIRMABILITY_RULES.md 待后续（有2~3轮数据后）再推进
  - 当前不做自动 cron/调度提醒
  - 来源复核频率：每4~6周或触发条件满足时

---

## P2 任务（本阶段不推进）

| 编号 | 任务名称 | 对应推进点 | 不推进原因 |
|------|---------|-----------|-----------|
| P2-1 | 微信公号抓取方案继续研究 | 数据源轻管理 | 平台壁垒不可解；苏商银行可替代 |
| P2-2 | 角色视图梳理 | 角色视图 | 无多角色需求苗头，为未来扩展保留 |

---

## 不纳入本阶段的事项

以下事项不在任务包范围内，详见 CHANGE_CONTROL.md：

- Gate A 数据修复（外部依赖）
- 重型后台建设
- 复杂权限体系
- 新模块扩展
- 界面精致化
- 微信公号主动推进

---

## 依赖与阻断关系

```
P0-1（已完成）
    ↓
P0-2（已完成）
    ↓
P0-3（已完成 ✅）
    ↓
P1-1b（✅ 已完成：CSV轻量追踪表，2026-04-07）
P1-2（✅ 已完成：来源有效性review矩阵与笔记，2026-04-07）
P1-3（✅ 已完成：试点运行SOP与首轮小结，2026-04-07）
```

---

## 验收口径

**试点运行验收标准（M4 里程碑）**：

- M4a（结果可展示）：前端页面可访问（8787）✅ / 分析师抓取可成功运行 / analyst_opinions_raw.json 非空 / 数据 freshness 可确认
- M4b（流程可演示）：M4a 通过 + P0-2 完成 + P1-1 review状态持久化实施后，可演示一次完整 review 流程（确认/驳回/状态变化）

**M4a/M4b 当前状态**：
- M4a：✅ 通过（页面可访问 + 数据非空 + freshness 可确认）
- M4b：✅ 通过（reviewStatus+trackingStatus落地 + 状态变更演示成功）

**非阻断但需记录的问题**：

- 顾慧君/王锟来源 0 篇（SOURCE_GOVERNANCE_DRAFT 中标注为候选初稿，待 P1-2 确认）
- Gate A 持续 BLOCKED（已记录在 OPEN_ISSUES.md）
