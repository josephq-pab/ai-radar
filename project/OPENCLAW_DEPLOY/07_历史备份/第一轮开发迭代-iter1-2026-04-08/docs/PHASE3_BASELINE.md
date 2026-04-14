# PHASE3_BASELINE.md — Phase 3 基线冻结说明

> 文档版本：v1.0（初建）
> 建立日期：2026-04-07
> 对应阶段：Phase 3 — 试点运营化 / MVP 闭环
> 依据：PHASE3_CLOSURE_REPORT.md v1.0

---

## 一、基线目的

本文档定义 Phase 3 的交付物基线，用于：

1. **明确边界**：冻结本阶段已通过结论，防止后续变更回写篡改
2. **变更参照**：后续 P1 变更需对比本文档，判断是否回写到 Phase 3 产物
3. **交接依据**：新参与者可通过本文档快速理解 Phase 3 实际交付了什么

---

## 二、当前文档基线版本

| 文档 | 版本 | 建立日期 | 用途 |
|------|------|---------|------|
| PHASE3_STATUS.md | v1.3 | 2026-04-07 | 阶段状态实时参考 |
| PHASE3_TASK_PACKAGE.md | v1.3 | 2026-04-07 | P0/P1/P2 任务边界与验收口径 |
| PHASE3_CLOSURE_REPORT.md | v1.0 | 2026-04-07 | 阶段完成情况正式记录 |
| CHANGE_CONTROL.md | v1.1 | 2026-04-07 | 变更控制硬化规则 |
| DECISION_LOG.md | v1.3 | 2026-04-07 | 7项关键决策记录（D-01~D-07） |
| REVIEW_LOG.md | v1.2 | 2026-04-07 | 15轮 review 记录（R-01~R-15） |
| OPEN_ISSUES.md | v1.1 | 2026-04-07 | 4个非阻断型问题 + 2个外部依赖 |
| ROLE_VIEW_DRAFT.md | — | 2026-04-07 | 角色视图（v几无标注，按日期认定） |
| CONTENT_STRUCTURE_DRAFT.md | — | 2026-04-07 | 内容结构（v几无标注，按日期认定） |
| OPERATING_CYCLE_DRAFT.md | — | 2026-04-07 | 运营周期（v几无标注，按日期认定） |
| SOURCE_GOVERNANCE_DRAFT.md | v0.9 | 2026-04-07 | **候选初稿，非正式版本** |

**无版本标注的文档**（按日期认定）：
- ROLE_VIEW_DRAFT.md、CONTENT_STRUCTURE_DRAFT.md、OPERATING_CYCLE_DRAFT.md 均未在文档内标注版本号。
- 后续更新时应统一标注版本号（建议 v1.0 与本基线对齐）。

---

## 三、当前脚本/产物基线

### 3.1 关键脚本（已验证可运行）

| 脚本 | 路径 | 验证状态 |
|------|------|---------|
| fetch_analyst_articles.py | 05_工具脚本/ | ✅ 可运行，输出 79条 raw |
| build_analyst_opinions.py | 05_工具脚本/ | ✅ 可运行，输出 29条 usable + 5条 report-ready |
| smoke_test.py | 05_工具脚本/ | ✅ 38/38 PASS |
| rebuild_go_live_gate.py | 05_工具脚本/ | ✅ 可运行 |
| run-pipeline.sh | /tmp/run-pipeline.sh | ✅ 入口脚本 |

### 3.2 关键数据产物（基线版本）

| 产物 | 路径 | 条目数 | 备注 |
|------|------|-------|------|
| analyst_opinions_raw.json | 04_数据与规则/processed/ | 79条 | 基线：2026-04-07 抓取结果 |
| analyst_opinions.json | 04_数据与规则/processed/ | 29条 | VALID×25 + DEGRADED×4 |
| analyst-review-queue.json | 04_数据与规则/processed/ | 5条 | 含 reviewStatus + trackingStatus + confirmLevel |
| analyst_sources.json | 04_数据与规则/ | 13个来源 | 苏商银行替代微信公号方案后来源列表 |

### 3.3 基线产物快照日期

所有基线产物均为 **2026-04-07** 的快照。
后续抓取运行会更新这些文件，但：
- analyst_sources.json 更新需同步更新 SOURCE_GOVERNANCE_DRAFT（如有分类变更）
- analyst-review-queue.json 的 reviewStatus/trackingStatus 每次 build 重置（已知边界）

---

## 四、当前演示基线

### 4.1 M4a 演示基线（结果可展示）

**演示内容**：前端页面展示最新抓取结果
- URL：http://47.112.211.98:8787/index.html
- 数据范围：analyst_opinions_raw.json（79条）经 build 后输出
- 数据新鲜度：2026-04-07（当日抓取）

**演示边界**：
- 利率数据仅标注至 2025-12（Gate A 未解除）
- 页面不展示 reviewStatus/trackingStatus（M4a 只验证结果可见性）

### 4.2 M4b 演示基线（流程可演示）

**演示链路**：
```
原始观点进入 → 分层输出 → review queue → confirmLevel → 最小状态流转 → REVIEW_LOG 留痕
```

**演示步骤**（5步）：
1. 展示 analyst_opinions_raw.json（79条 raw 层）
2. 展示 analyst-review-queue.json（5条，含 reviewStatus=pending / trackingStatus=candidate）
3. 选择 analyst-72873eb4（薛洪言），修改 reviewStatus=confirmed / trackingStatus=follow_up
4. 重读 analyst-review-queue.json，确认状态已变化
5. 恢复初始状态（reset 为 pending），演示结束

**演示边界**：
- 状态修改在 JSON 文件层面，不涉及数据库
- 重新运行 build 后所有状态重置（不得声称"持久化"）
- 演示路径：M4b 演示路径为 M4a + P0-2 完成后可验证

---

## 五、基线冻结范围

以下内容在 Phase 3 基线中已**明确**，后续变更不得回写篡改：

### 5.1 不得回写的结论

| # | 已冻结结论 | 依据 |
|---|----------|------|
| 1 | M1~M4b 全部通过 | PHASE3_CLOSURE_REPORT.md / PHASE3_STATUS.md |
| 2 | P0-1/P0-2/P0-3 全部完成 | PHASE3_TASK_PACKAGE.md |
| 3 | analyst-review-queue.json 含 reviewStatus + trackingStatus | REVIEW_LOG R-15 |
| 4 | 重新 build 会重置所有 reviewStatus=pending | DECISION_LOG D-07 |
| 5 | Gate A 为外部依赖，系统层无解 | DECISION_LOG D-04 / OPEN_ISSUES ED-01 |
| 6 | SOURCE_GOVERNANCE_DRAFT 为候选初稿 v0.9，非正式版本 | SOURCE_GOVERNANCE_DRAFT 文档标注 |
| 7 | 79条 raw → 29条 usable → 5条 report-ready 筛选链路 | PHASE3_CLOSURE_REPORT.md / CONTENT_STRUCTURE_DRAFT |
| 8 | confirmLevel P1/P2/P3 为规则映射，非人工验证 | OPEN_ISSUES OI-04 |
| 9 | CHANGE_CONTROL 有硬化规则（变更先记录才能进任务包） | CHANGE_CONTROL v1.1 C-03 |

### 5.2 可以正常变更的范围（P1 范围）

| # | P1 正常变更范围 | 变更后操作 |
|---|--------------|----------|
| 1 | P1-1 建立追踪表（fetch-run-log.json） | 同步更新 RUNBOOK.md |
| 2 | P1-2 来源有效性 review 完成 | 更新 SOURCE_GOVERNANCE_DRAFT 为 v1.0 |
| 3 | P1-3 confirmLevel 规则文档化 | 新建 CONFIRMABILITY_RULES.md |
| 4 | OI-03 评分优化 | 更新 build_analyst_opinions.py 评分逻辑 |
| 5 | OI-04 人工分级对比机制 | 更新 analyst-review-queue.json 生成逻辑 |

### 5.3 不得单独修改的 Phase 3 文档

以下文档如需修改，需经过 CHANGE_CONTROL 流程（记录 → 结论 → 才可进入任务包）：

- CHANGE_CONTROL.md（硬化规则约束）
- DECISION_LOG.md（D-01~D-07 已固化）
- REVIEW_LOG.md（历史记录不得删除，只能追加）
- PHASE3_CLOSURE_REPORT.md（本文件，冻结版）

---

## 六、后续变更原则

### 6.1 P1 变更与 Phase 3 基线关系

1. **不得回写篡改**：P1 变更不得修改 Phase 3 已通过的结论（如"P0-3 已完成"）
2. **不得删除留痕**：REVIEW_LOG / DECISION_LOG 历史记录只可追加，不可删除
3. **版本递进**：P1 对 Phase 3 文档的更新应递进版本号（如 v1.3 → v1.4）
4. **变更记录**：任何对基线文档的修改应记录到 CHANGE_CONTROL"新增建议变更记录"节

### 6.2 文档版本号规范

建议统一规范：
- Phase 3 文档版本号：v1.x（当前最高 v1.3）
- P1 新建文档：v1.0 起（如 P1-3 新建的 CONFIRMABILITY_RULES.md）
- PILOT_DEMO_SCRIPT.md：v1.0（本轮新建）
- P1_CANDIDATES.md：v1.0（本轮新建）

---

## 七、基线冻结检查清单

以下项目在进入 P1 前应确认仍然成立：

- [ ] 8787 前端仍然可访问
- [ ] analyst_opinions_raw.json 非空（79条 或更多）
- [ ] analyst-review-queue.json 含 reviewStatus + trackingStatus
- [ ] smoke_test.py 仍然 38/38 PASS
- [ ] PHASE3_CLOSURE_REPORT.md 描述与实际产物一致
- [ ] Gate A 仍未解除（ED-01 持续）
- [ ] SOURCE_GOVERNANCE_DRAFT 仍为 v0.9（未误标为正式版）

---

**基线编制人**：AI雷达站 agent
**基线冻结日期**：2026-04-07
**下次复查时机**：进入 P1-1 前
