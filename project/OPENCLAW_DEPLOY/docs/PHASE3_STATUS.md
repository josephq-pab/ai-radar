# PHASE3_STATUS.md — 对公 AI 雷达站 Phase 3 阶段状态

> 文档版本：v1.7（本次更新：P1-3 试点运行 SOP 实施完成）
> 版本历史：
> - v1.0（2026-04-07）：按模板初建
> - v1.1（2026-04-07）：M4拆分为M4a（结果可展示）/M4b（流程可演示），M4a/M4b/M3状态重新标定
> - v1.2（2026-04-07）：P0-2 实施完成，输出分层固化（路径统一 + confirmLevel落地）
> - v1.3（2026-04-07）：P0-3 实施完成，M4b 演示通过（reviewStatus+trackingStatus落地）

---

## 当前阶段

Phase 3 — 试点运营化 / MVP 闭环

---

## 上阶段结论

| 阶段 | 结论 | 完成日期 |
|------|------|---------|
| Phase 2 基线收敛 | ✅ 完成 | 2026-04-03 |
| Phase 2.1 B Gate 语义收口 | ✅ 完成 | 2026-04-03 |

---

## Gate A 状态

**状态**：BLOCKED（持续）

**原因**：外部条件未满足——2026-03 贷款利率 Excel 文件未到位。系统层无解，依赖数据供给方。

**影响**：
- 前端利率数据只能标注至 2025-12
- 报告引用需注明数据截止月份
- 不得声称"截至 2026-03"

**临时处理**：文档标注法，不作为 Phase 3 主线任务。

---

## 本阶段目标

让系统具备**可管理、可确认、可跟进、可复盘、可按周期运行、可演示**的最小闭环。

**具体可验收标志**：
- 分析师抓取可按周期运行
- 输出分层清晰（raw → reviewed → report-ready）
- 确认项分级明确
- 文档与实际状态一致

---

## 本阶段不做事项

1. Gate A 数据修复（外部依赖，系统层无解）
2. 重型后台建设
3. 复杂权限体系
4. 新模块扩展（除非明确属于 MVP 最小闭环所必需）
5. 界面精致化（优先级低于结构治理）
6. 未列入任务包的任何功能新增

---

## 本阶段五项核心推进点

| 推进点 | 说明 |
|--------|------|
| 输出分层 | raw → reviewed → report-ready 三层定义与固化 |
| 确认项分级 | confirmable / referenceable / reportable 规则文档化 |
| 周期管理 | 日/周/月运行机制定义 |
| 角色视图 | 不同角色看什么、做什么的最小边界 |
| 数据源轻管理 | 来源分类、启用/停用规则 |

---

## 本阶段里程碑

| 里程碑 | 定义 | 验收方式 | 状态 | 完成日期 |
|--------|------|---------|------|---------|
| M1 | 运行入口稳定 | 8787 可访问，run-pipeline.sh 路径正确 | ✅ | 2026-04-07 |
| M2 | 分析师抓取可周期运行 | fetch_analyst_articles.py 无报错，输出非空 | ✅ | 2026-04-07 |
| M3 | 文档与状态对齐 | 10 份核心文档与实际状态一致 | ✅ | 2026-04-07 |
| M4a | 试点结果可展示 | 页面可访问 + 数据非空 + freshness 可确认 | ✅ | 2026-04-07 |
| M4b | 试点流程可演示 | reviewStatus+trackingStatus 字段落地，演示一次状态变更并确认生效 | ✅ | 2026-04-07 |
| M5 | 首轮 review 通过 | REVIEW_LOG 有实质性记录，无重大偏差 | ⏳ | — |

**M4 拆分说明**：
- M4a（结果可展示）：验证数据能采集、能呈现。对应 P0-1 前端验证，当前 8787 已恢复可访问，但尚未人工确认数据可读性。
- M4b（流程可演示）：验证运营编辑者能对数据进行 confirm/reject/跟进操作。需 P0-2（输出分层固化）+ P1-1（追踪表）完成后方可验证。

---

## 当前风险与约束

| 风险/约束 | 程度 | 应对 |
|-----------|------|------|
| Gate A 数据持续缺位 | 高 | 文档标注，暂挂处理 |
| 顾慧君/王锟来源文章年代偏旧 | 中 | P1-2 review 时处理 |
| 文档与实际状态可能漂移 | 中 | M3 验证时同步检查 |
| 变更控制依赖人工自觉遵守 | 低 | 每轮 review 前自检 |

---

## 当前完成情况

| 文档 | 路径 | 状态 |
|------|------|------|
| PHASE3_STATUS | docs/PHASE3_STATUS.md | ✅ 本文档 |
| PHASE3_TASK_PACKAGE | docs/PHASE3_TASK_PACKAGE.md | ✅ 已按模板重建 |
| CHANGE_CONTROL | docs/CHANGE_CONTROL.md | ✅ 已按模板重建 |
| DECISION_LOG | docs/DECISION_LOG.md | ✅ 完成 |
| OPEN_ISSUES | docs/OPEN_ISSUES.md | ✅ 完成 |
| REVIEW_LOG | docs/REVIEW_LOG.md | ✅ 完成 |
| ROLE_VIEW_DRAFT | docs/ROLE_VIEW_DRAFT.md | ✅ 完成 |
| CONTENT_STRUCTURE_DRAFT | docs/CONTENT_STRUCTURE_DRAFT.md | ✅ 完成 |
| OPERATING_CYCLE_DRAFT | docs/OPERATING_CYCLE_DRAFT.md | ✅ 完成 |
| SOURCE_GOVERNANCE_DRAFT | docs/SOURCE_GOVERNANCE_DRAFT.md | ✅ 完成 |

---

## 下一检查点

**当前状态**：
- M1 ✅ / M2 ✅ / M3 ✅ / M4a ✅ / M4b ✅ / M5 ⏳
- P1-1 ✅（review 状态持久化独立台账，2026-04-07 实施验证通过）
- P1-1b ✅（CSV轻量追踪表 pilot-tracking-ledger.csv，2026-04-07 实施验证通过）
- P1-2 ✅（来源有效性review矩阵与笔记，2026-04-07 实施验证通过）
- P1-3 ✅（试点运行SOP与首轮小结，2026-04-07 实施验证通过）

**进入 P1-3 前置条件**：P1-2 已有结论文档，confirmLevel 规则文档化（P1-3）可在 P1-2 结论基础上推进

**本轮（P1-2 实施）产出确认**：
- docs/analyst_review_matrix.md：13个来源证据矩阵（数值可追溯）
- docs/analyst_review_notes.md：每来源一段，含结论/证据/边界/配置建议
- 结论分布：keep=2/observe=3/pending-check=8/downgrade=0
- analyst_sources.json 未被修改（配置建议是人工参考，非自动生效）
- 顾慧君/王锟正确归因为 min_year 过滤，非来源质量差
- 付一夫正确归因为 top-k 截断，非来源质量差

**P1-2 遗留边界说明**：
- analyst_sources.json 未被自动修改（待人工决策）
- SOURCE_GOVERNANCE_DRAFT 仍为 v0.9 候选初稿
- 6个来源0 raw记录待人工核实

**P1-3 遗留边界说明**：
- CONFIRMABILITY_RULES.md 降级为后续待办（需2~3轮数据积累才有意义）
- 当前不做自动 cron/调度提醒
- 来源复核频率：每4~6周或触发条件满足时（温彬/曾刚/朱太辉/孙扬/杜娟/董希淼）

**当前 Phase 3 P0 任务全部完成**：
- P0-1 ✅ / P0-2 ✅ / P0-3 ✅

---

## 最近一次更新时间

2026-04-07（v1.7：P1-3 试点运行 SOP 实施完成，ROUND-01 首轮跑通，PILOT_RUN_SOP + ROUND_RECAP_TEMPLATE + SOURCE_REVIEW_CHECKLIST 验证通过）
