# OPS_CHANGE_IMPACT_MATRIX_V1.md — 变更影响矩阵

> 文档版本：v1.0（P3-41）
> 创建时间：2026-04-21
> 对应阶段：Phase 3 — 试点运营化 / P3-41 全站治理底座、可维护性矩阵与防漂移维护手册功能包第一期
> 目的：明确"如果改X，必须同步哪些对象"，让每次改动不漏同步

---

## 一、变更影响矩阵总览

使用说明：
- 必同步 = 必须检查并可能需要修改
- 建议检查 = 大概率需要修改
- 可选检查 = 低概率需要修改
- 不受影响 = 该对象与此项改动无关

---

## 二、状态主线改动

**改动场景**：修改"对公 AI 雷达站 · V7 基线冻结 · 十页入口可用"这句主线口号

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| radar-home.html | 必同步 | 首页横幅+footer |
| ops-brief.html | 建议检查 | 状态快照引用句 |
| single-chain-ops.html | 建议检查 | 当前停点描述 |
| ops-decision.html | 可选检查 | 边界条件描述 |
| ops-evidence.html | 可选检查 | 证据页引用 |
| ops-playbook.html | 可选检查 | 执行前置描述 |
| ops-glossary.html | 可选检查 | 术语引用 |
| ops-registry.html | 可选检查 | 元信息描述 |
| ops-routes.html | 可选检查 | 路径索引引用 |
| config-status.html | 建议检查 | 配置快照引用 |
| STAGE2_SINGLE_CHAIN_STATUS.md | 必同步 | 真源层必须同步 |
| OPS_COPY_BASELINE.md | 必同步 | 全站标准句库必须同步 |

---

## 三、生命周期定义改动

**改动场景**：修改七阶段（W/L/A/P/E/R/S）定义、流转规则、禁止自动流转边界

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| radar-home.html | 必同步 | 生命周期总览模块 |
| single-chain-ops.html | 必同步 | 状态流转模块 |
| ops-routes.html | 必同步 | 生命周期路径 |
| ops-decision.html | 建议检查 | A/E阶段边界条件 |
| ops-brief.html | 建议检查 | 快报生命周期段 |
| ops-playbook.html | 建议检查 | 执行前置P阶段 |
| STAGE2_SINGLE_CHAIN_STATUS.md | 必同步 | 真源层 |
| OPS_LIFECYCLE_MAP_V1.md | 必同步 | 生命周期包 |
| OPS_CASEBOOK_V1.md | 建议检查 | 场景样例 |
| OPS_BOUNDARY_CASES_V1.md | 建议检查 | 边界对照 |
| OPS_TRAINING_PACK_V1.md | 建议检查 | 训练包示例 |
| OPS_MISUSE_GUARDRAILS_V1.md | 建议检查 | 误用防护 |

---

## 四、升级规则改动

**改动场景**：修改升级条件、升级判断标准、升级路径

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| single-chain-ops.html | 必同步 | 升级判断模块 |
| ops-decision.html | 必同步 | 决策辅助条件 |
| ops-brief.html | 建议检查 | 快报升级标记 |
| ops-evidence.html | 可选检查 | 升级依据说明 |
| STAGE2_SINGLE_CHAIN_STATUS.md | 必同步 | 真源层 |
| OPS_ESCALATION_PACK_V1.md | 必同步 | 升级规则包 |
| OPS_CORE_LOOP_V1.md | 建议检查 | 核心环路 |
| OPS_CASEBOOK_V1.md | 建议检查 | 升级场景样例 |
| OPS_TRAINING_PACK_V1.md | 建议检查 | 训练包 |
| OPS_MISUSE_GUARDRAILS_V1.md | 建议检查 | 误用防护 |

---

## 五、回复回写规则改动

**改动场景**：修改"暂不推进/补材料/同意准备/否决"的回写路径与停点

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| single-chain-ops.html | 必同步 | 回复吸收态模块 |
| ops-decision.html | 建议检查 | 决策回复处理 |
| ops-brief.html | 建议检查 | 快报状态更新 |
| STAGE2_SINGLE_CHAIN_STATUS.md | 必同步 | 真源层 |
| OPS_DECISION_REPLY_V1.md | 必同步 | 回复回写包 |
| OPS_MISUSE_GUARDRAILS_V1.md | 必同步 | 误用防护（补材料≠否决等）|
| OPS_DRILL_PACK_V1.md | 建议检查 | 演练题 |
| OPS_CASEBOOK_V1.md | 建议检查 | 回复场景样例 |

---

## 六、第二链路状态改动

**改动场景**：第二链路从冻结→有条件解冻→完全解冻

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| radar-home.html | 必同步 | 第二链路状态横幅 |
| single-chain-ops.html | 必同步 | 第二链路说明 |
| config-status.html | 必同步 | 第二链路配置说明 |
| ops-evidence.html | 建议检查 | 来源说明 |
| ops-registry.html | 建议检查 | 来源登记说明 |
| STAGE2_SINGLE_CHAIN_STATUS.md | 必同步 | 真源层 |
| OPS_TRAINING_PACK_V1.md | 必同步 | 训练包（来源候选≠解冻）|
| OPS_MISUSE_GUARDRAILS_V1.md | 必同步 | 误用防护（来源候选≠解冻）|
| OPS_DRILL_PACK_V1.md | 建议检查 | 演练题（来源候选场景）|

---

## 七、训练/误用/演练内容改动

**改动场景**：修改训练路径、误用场景、演练题

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| OPS_TRAINING_PACK_V1.md | 必同步 | 训练包 |
| OPS_MISUSE_GUARDRAILS_V1.md | 必同步 | 误用防护 |
| OPS_DRILL_PACK_V1.md | 必同步 | 演练题 |
| radar-home.html | 建议检查 | 训练入口模块 |
| ops-brief.html | 建议检查 | 快报训练提示 |
| single-chain-ops.html | 建议检查 | 运营训练提示 |
| ops-decision.html | 建议检查 | 决策训练提示 |
| ops-evidence.html | 建议检查 | 证据训练提示 |
| ops-playbook.html | 建议检查 | 执行训练提示 |
| ops-glossary.html | 建议检查 | 术语训练提示 |
| ops-registry.html | 建议检查 | 登记训练提示 |
| ops-routes.html | 建议检查 | 路径训练提示 |
| config-status.html | 建议检查 | 配置训练提示 |

---

## 八、典型场景/边界对照改动

**改动场景**：新增/修改典型场景判例或边界对照

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| OPS_CASEBOOK_V1.md | 必同步 | 典型场景包 |
| OPS_BOUNDARY_CASES_V1.md | 必同步 | 边界对照包 |
| radar-home.html | 建议检查 | 典型场景速查模块 |
| single-chain-ops.html | 建议检查 | 场景判例模块 |
| ops-brief.html | 建议检查 | 高频误判对照 |
| ops-decision.html | 建议检查 | 边界场景模块 |
| ops-routes.html | 建议检查 | 场景路径模块 |

---

## 九、口径/文案统一性改动

**改动场景**：修改全站标准句库（canonical sentences）

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| OPS_COPY_BASELINE_V1.md | 必同步 | 标准句库 |
| 全站10个HTML页面 | 必同步 | footer + 状态横幅 |
| OPS_TRAINING_PACK_V1.md | 建议检查 | 训练引用句 |
| OPS_MISUSE_GUARDRAILS_V1.md | 建议检查 | 误用引用句 |
| OPS_DRILL_PACK_V1.md | 建议检查 | 演练引用句 |

---

## 十、跟踪文档改动

**改动场景**：修改 STAGE2 / CHANGE_CONTROL / REVIEW_LOG / FEEDBACK_TRACKING

| 对象 | 影响等级 | 同步要求 |
|------|---------|---------|
| STAGE2_SINGLE_CHAIN_STATUS.md | - | 真源层，单独维护 |
| CHANGE_CONTROL.md | 必同步 | ops-registry.html（真源映射）|
| REVIEW_LOG.md | 建议检查 | ops-registry.html（真源映射）|
| FEEDBACK_TRACKING_STATUS.md | 建议检查 | radar-home.html（状态横幅）|

---

## 十一、改动后验收检查清单

每次改动完成后，按以下清单逐项确认：

- [ ] 状态主线句是否在全站保持一致
- [ ] 涉及改动的页面 footer 是否同步更新
- [ ] STAGE2 是否已更新（如涉及）
- [ ] CHANGE_CONTROL 是否已追加（如涉及）
- [ ] REVIEW_LOG 是否已更新（如涉及）
- [ ] 训练包/误用防护/演练题是否需要同步（如涉及）
- [ ] OPS_GOVERNANCE_MAP 是否需要更新（如涉及新治理层级）
- [ ] 改动是否影响了其他页面的交叉引用
- [ ] 改动是否引入了新的不一致（用 OPS_COPY_BASELINE 核对）
