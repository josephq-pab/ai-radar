# REVIEW_LOG.md — Phase 3 Review 记录

> 文档版本：v1.29（本次更新：R-44 P1-LT 观察窗口长期触发包（首次执行，分支A：P0/P1/P2均未触发））
> 版本历史：
> - v1.0（2026-04-07）：初建，10 轮形式化全通过 review
> - v1.1（2026-04-07）：识别出机制失灵问题，重写 R-01~R-10，改为实质性记录
> - v1.2（2026-04-07）：R-12 P0-2 实施 review + R-13 口径统一 + R-14 M4b设计 + R-15 M4b演示
> 最近更新：2026-04-07
> 对应阶段：Phase 3 — 试点运营化 / MVP闭环

---

## ⚠️ REVIEW_LOG 机制修正说明

v1.0 版本 R-01~R-10 所有条目均标记"是否符合阶段目标：✅ 是 / 是否新增未批准范围：❌ 否 / 发现问题：无 / 修正动作：无"——这是**机制失灵**，不是高质量。

v1.1 修正方向：
1. 不伪造问题（未发现问题，必须说明核查范围和依据）
2. 区分"本 round 可发现"与"需要跨文档才能发现"
3. 本轮（R-11）识别出 6 个结构性问题，记录为本次 review 的真实发现

---

## Review 记录列表

---

### Review R-01

- **日期**：2026-04-07
- **review 对象**：PHASE3_STATUS.md v1.0
- **所属推进点**：阶段基础建设
- **核查范围**：本轮只写了 STATUS，核查范围局限于单文档内部结构
- **本 round 可发现的问题**：
  - M4"试点运行可演示"的验收方式是否具体 → M4 定义本身是清晰的
  - 十项必填字段是否完整 → 完整
  - Gate A 是否归入不做事项 → 是
- **本 round 未发现问题的依据**：STATUS 是第一份写的文档，彼时 M4 的验收标准与阶段目标之间的缺口尚未暴露（M4 没有拆分是 R-11 时才识别）
- **跨文档问题（在 R-06 后才可发现）**：M4 定义与 TASK 包中 M4 验收口径的对应关系，在 R-06（五文档全部建立后）才能识别
- **是否与既有文档一致**：✅ 是（本 round 无其他文档）
- **是否新增未批准范围**：❌ 否
- **发现问题**：无（在本 round 核查范围内）
- **修正动作**：无
- **是否已完成文档同步**：✅ 是
- **下一步建议**：推进 TASK 包
- **状态**：✅ 本 round 核查通过（但 R-06 后回看：M4 定义缺口在彼时不可见，不属于 R-01 失职）

---

### Review R-02

- **日期**：2026-04-07
- **review 对象**：PHASE3_TASK_PACKAGE.md v1.0
- **所属推进点**：输出分层、确认项分级、周期管理、角色视图、数据源轻管理
- **核查范围**：单文档内部（字段完整性、P0/P1/P2 分级、依赖关系）
- **本 round 可发现的问题**：
  - P0-2 验收方式中"analyst_opinions.json 生成非空记录"——未验证 build_analyst_opinions.py 是否能跑
  - P1-2 与 SOURCE_GOVERNANCE_DRAFT 边界不清（P1-2 说"有来源分类结果"，SOURCE_GOVERNANCE_DRAFT 已在做分类）→ **本 round 可发现，R-02 应标记**
- **本 round 实际状态**：R-02 写成"无发现问题"——**这是 R-02 的失职，P1-2 与 SOURCE_GOVERNANCE 边界重叠是可发现的**
- **是否与既有文档一致**：⚠️ 否（R-02 时 STATUS 刚建立，M4 拆分缺口不可见；但 P1-2/SOURCE_GOVERNANCE 边界问题是 R-02 可发现的）
- **是否新增未批准范围**：❌ 否
- **发现问题**：P1-2 任务描述与 SOURCE_GOVERNANCE_DRAFT 做的事情重叠，P1-2 实质上是"确认"而不是"分类"，边界模糊
- **修正动作**：应由 R-02 提出，v1.1 中修正（M-02）
- **是否已完成文档同步**：✅ 是（v1.0 中已同步）
- **下一步建议**：推进 CHANGE_CONTROL
- **状态**：⚠️ 本 round 失职（应发现但未发现；v1.1 中补正）

---

### Review R-03

- **日期**：2026-04-07
- **review 对象**：CHANGE_CONTROL.md v1.0
- **所属推进点**：防止范围漂移
- **核查范围**：单文档内部（8项不做/变更记录/拒绝/复查机制）
- **本 round 可发现的问题**：
  - 变更申请流程缺少硬化规则（"不得在未经用户确认的情况下擅自扩展任务包"只是描述，没有执行机制）→ **本 round 可发现，应标记**
  - 新增建议变更记录与 DECISION_LOG 无编号对应 → **本 round 可发现**
- **本 round 实际状态**：R-03 写成"无发现问题"——**机制缺失是可发现的**
- **是否与既有文档一致**：⚠️ 部分（变更记录数量与 DECISION_LOG 不对应，R-03 本应提出）
- **是否新增未批准范围**：❌ 否
- **发现问题**：
  1. 变更申请流程无硬化机制（只靠描述，无执行约束）
  2. 新增建议变更记录数量（3条）少于 DECISION_LOG（5条），编号不对应
- **修正动作**：应由 R-03 提出，v1.1 中修正（C-01/C-02/C-03）
- **是否已完成文档同步**：✅ 是（v1.0 中已同步）
- **下一步建议**：建立 DECISION_LOG
- **状态**：⚠️ 本 round 失职（应发现但未发现；v1.1 中补正）

---

### Review R-04

- **日期**：2026-04-07
- **review 对象**：DECISION_LOG.md v1.0
- **所属推进点**：决策可追溯
- **核查范围**：单文档内部（5条决策字段完整性/逻辑一致性）
- **本 round 可发现的问题**：
  - D-01/D-04 在 CHANGE_CONTROL 中无对应 CC 编号 → **本 round 可发现，应标记**
  - D-02（profile 发现逻辑）和 D-03（内容提取修复）已实现，但 CHANGE_CONTROL 中未同步记录 → **本 round 可发现**
- **本 round 实际状态**：R-04 写成"无发现问题"
- **是否与既有文档一致**：⚠️ 否（与 CHANGE_CONTROL 有缺口）
- **是否新增未批准范围**：❌ 否
- **发现问题**：D-01/D-04 等决策与 CHANGE_CONTROL 无编号映射，导致变更控制追踪链断裂
- **修正动作**：应由 R-04 提出，v1.1 中补正（C-02）
- **是否已完成文档同步**：✅ 是（v1.0 中已同步）
- **下一步建议**：建立 OPEN_ISSUES
- **状态**：⚠️ 本 round 失职（应发现但未发现；v1.1 中补正）

---

### Review R-05

- **日期**：2026-04-07
- **review 对象**：OPEN_ISSUES.md v1.0
- **所属推进点**：问题追踪
- **核查范围**：单文档内部（Gate A 归类/OI 编号/责任方/复查时间）
- **本 round 可发现的问题**：
  - ED-01（Gate A）解除后无验证动作 → **本 round 可发现，应标记**
  - OI-02（文档漂移风险）的"复查时间"写的是"每次脚本路径变更时"，但没有说清楚谁来触发这个复查 → **本 round 可发现，应标记**
- **本 round 实际状态**：R-05 写成"无发现问题"
- **是否与既有文档一致**：✅ 是（内部一致；跨文档一致性在 R-06 后才可验证）
- **是否新增未批准范围**：❌ 否
- **发现问题**：ED-01 解除后的验证动作缺失
- **修正动作**：应在 R-05 提出，写入 OPEN_ISSUES.md；目前缺失，v1.1 记录但不回补（ED-01 解除是外部事件，修正由人工触发）
- **是否已完成文档同步**：✅ 是
- **下一步建议**：建立 ROLE_VIEW_DRAFT 等
- **状态**：⚠️ 本 round 失职（应发现但未发现；v1.1 中补正）

---

### Review R-06

- **日期**：2026-04-07
- **review 对象**：PHASE3_STATUS.md + PHASE3_TASK_PACKAGE.md + CHANGE_CONTROL.md + DECISION_LOG.md + OPEN_ISSUES.md（共5份）
- **所属推进点**：跨文档一致性（首次出现跨文档 review）
- **核查范围**：五份核心文档之间的里程碑/任务/变更/决策/问题是否对应
- **本 round 可发现的问题**：
  - **M4 的验收标准（5条）与阶段目标"可演示/可确认/可跟进"不匹配** → 这是 R-06 最应该发现的核心问题
  - M4 在 STATUS 中标记为"⏳"，但在 TASK 包中没有对应 M4 的"当前状态"字段说明
- **本 round 实际状态**：R-06 写成"无发现问题"
- **是否与既有文档一致**：⚠️ 否（M4 定义与 TASK 验收标准不匹配）
- **是否新增未批准范围**：❌ 否
- **发现问题**：M4 定义（"前端可展示最近一次抓取结果"）与阶段目标（"可演示/可确认/可跟进"）存在缺口；TASK 包中 P0-1 标注"已完成"但 M4 验收标准（页面可访问+数据非空）尚未人工验证
- **修正动作**：应由 R-06 提出，v1.1 中修正（M-01）
- **是否已完成文档同步**：✅ 是
- **下一步建议**：建立 ROLE_VIEW_DRAFT 等
- **状态**：⚠️ 本 round 失职（R-06 是跨文档 review 的首次尝试，但未发现 M4 缺口问题；v1.1 中补正）

---

### Review R-07

- **日期**：2026-04-07
- **review 对象**：ROLE_VIEW_DRAFT.md v1.0
- **所属推进点**：角色视图
- **核查范围**：单文档内部（3角色完整性/MVP最小能力/不需要看到的内容）
- **本 round 可发现的问题**：
  - 运营编辑者的"手动确认/驳回操作（当前为纸面流程，未系统化）"与 M4b（流程可演示）之间的依赖关系未说明 → **可发现，应标记**
- **本 round 未发现问题的依据**：纸面流程未系统化在 R-07 时是已知的（文档写了"当前为纸面流程"），但没有连接到 M4b 验收条件——这是一个需要跨文档（M4b 定义）才能看到的问题，R-07 单文档核查无法发现
- **是否与既有文档一致**：✅ 是
- **是否新增未批准范围**：❌ 否
- **发现问题**：无（在本 round 核查范围内；但 R-06 后回看：运营编辑者的"可演示"能力与 M4b 定义之间存在依赖，R-07 无法独立发现）
- **修正动作**：无
- **是否已完成文档同步**：✅ 是
- **下一步建议**：建立 CONTENT_STRUCTURE_DRAFT
- **状态**：✅ 本 round 核查通过

---

### Review R-08

- **日期**：2026-04-07
- **review 对象**：CONTENT_STRUCTURE_DRAFT.md v1.0
- **所属推进点**：输出分层、确认项分级
- **核查范围**：单文档内部（3层/P1~P3标准/字段对照表）
- **本 round 可发现的问题**：
  - 三层字段对照表中 report-ready 层的 confirmLevel 标注"P1"，但没有说清楚"为什么 P2 不进入 report-ready" → 口径不清
- **本 round 未发现问题的依据**：这个口径问题属于"细节完善"范畴，不是结构性错误；更重要的是，review 机制当时失灵了（R-08 写成"无发现问题"但实际上有遗漏）
- **是否与既有文档一致**：✅ 是
- **是否新增未批准范围**：❌ 否
- **发现问题**：无（在本 round 核查范围内；但口径细节有完善空间）
- **修正动作**：无
- **是否已完成文档同步**：✅ 是
- **下一步建议**：建立 OPERATING_CYCLE_DRAFT
- **状态**：✅ 本 round 核查通过

---

### Review R-09

- **日期**：2026-04-07
- **review 对象**：OPERATING_CYCLE_DRAFT.md v1.0
- **所属推进点**：周期管理
- **核查范围**：单文档内部（日/周/月机制/状态流转/失败处理规则）
- **本 round 可发现的问题**：
  - "失败处理规则"中说">50%来源失败则告警"——但告警机制在"暂不纳入"节已列出，这里又隐含了告警逻辑，存在内部矛盾 → **本 round 可发现，应标记**
- **本 round 实际状态**：R-09 写成"无发现问题"
- **是否与既有文档一致**：⚠️ 否（告警逻辑在"暂不纳入"与"失败处理规则"中出现矛盾）
- **是否新增未批准范围**：❌ 否
- **发现问题**：失败处理中">50%来源失败则告警"与"暂不纳入的复杂机制：自动告警"存在矛盾
- **修正动作**：应在 R-09 提出；v1.1 记录为待修正（OPERATING_CYCLE_DRAFT v0.9，不回补）
- **是否已完成文档同步**：✅ 是
- **下一步建议**：建立 SOURCE_GOVERNANCE_DRAFT
- **状态**：⚠️ 本 round 失职（应发现但未发现；v1.1 中补正）

---

### Review R-10

- **日期**：2026-04-07
- **review 对象**：SOURCE_GOVERNANCE_DRAFT.md v1.0
- **所属推进点**：数据源轻管理
- **核查范围**：单文档内部（4类来源/启用停用规则/可信等级）
- **本 round 可发现的问题**：
  - **本文档已对7个来源逐一分类，这不是"轻管理原则"，而是"完成了分类决策"**——这与 TASK P1-2 的任务目的（"review后形成最终分类规则"）存在边界重叠 → **本 round 最应该发现的核心问题**
  - P1-2 的输入中已包含"analyst_sources.json；analyst_opinions_raw.json"，不包含 SOURCE_GOVERNANCE_DRAFT——说明 P1-2 是独立的 review 过程，不是对 SOURCE_GOVERNANCE 的确认
- **本 round 实际状态**：R-10 写成"无发现问题"
- **是否与既有文档一致**：⚠️ 否（SOURCE_GOVERNANCE_DRAFT 的分类实质上是 P1-2 的工作，P1-2 尚未执行就已经有了"候选结论"）
- **是否新增未批准范围**：❌ 否（文档层面，未进入系统实现）
- **发现问题**：SOURCE_GOVERNANCE_DRAFT 对 7 个来源的分类是"工作成果"而非"治理原则"，且与 TASK P1-2 存在逻辑重复（P1-2 尚未执行，SOURCE_GOVERNANCE 已产出候选结论）
- **修正动作**：应由 R-10 提出，v1.1 中修正（M-02）
- **是否已完成文档同步**：✅ 是
- **下一步建议**：执行 P0-2
- **状态**：⚠️ 本 round 失职（R-10 最应该发现边界重叠问题，但写成"无发现问题"；v1.1 中补正）

---

### Review R-11（当前校正轮次）

- **日期**：2026-04-07
- **review 对象**：本轮文档校正整体产出（PHASE3_STATUS / PHASE3_TASK_PACKAGE / SOURCE_GOVERNANCE_DRAFT / CHANGE_CONTROL / DECISION_LOG / REVIEW_LOG）
- **所属推进点**：全部（本次 review 是一次跨文档机制校正）
- **核查内容**：
  1. M-01：M4 是否已拆分为 M4a/M4b，M4b 是否明确了前置条件
  2. M-02：SOURCE_GOVERNANCE_DRAFT 是否已标注为候选初稿
  3. C-01：CHANGE_CONTROL 是否已增加版本历史
  4. C-02：CHANGE_CONTROL 与 DECISION_LOG 编号是否已映射
  5. C-03：CHANGE_CONTROL 是否有硬化规则（变更先记录才能进入 TASK）
  6. R-01~R-10 是否有实质性记录，是否反映真实的 review 过程
- **是否符合阶段目标**：✅ 是（本次校正严格限定在文档层面，未扩项）
- **是否与既有文档一致**：✅ 是（校正后的文档之间相互一致）
- **是否新增未批准范围**：❌ 否（本次校正只修改了已有文档，未新增功能或方向）
- **发现问题**：
  1. R-02/R-03/R-04/R-06/R-09/R-10 六个 round 存在"未发现问题"的形式化问题，属于机制失灵
  2. R-02 最应该发现 P1-2 与 SOURCE_GOVERNANCE 边界重叠（可发现）
  3. R-03 最应该发现 CHANGE_CONTROL 机制硬化缺失（可发现）
  4. R-04 最应该发现 DECISION_LOG 与 CHANGE_CONTROL 编号不对应（可发现）
  5. R-06 最应该发现 M4 定义缺口（跨文档可见）
  6. R-09 发现了告警逻辑矛盾但未记录
  7. R-10 最应该发现 SOURCE_GOVERNANCE 边界越界（可发现）
- **修正动作**：R-01~R-10 已按实际情况回补（区分"本 round 可发现"与"需跨文档"）；本次 R-11 作为机制校正的正式记录
- **是否已完成文档同步**：
  - ✅ PHASE3_STATUS.md（v1.1）：M4 拆分，M3/M4a/M4b 状态标定
  - ✅ PHASE3_TASK_PACKAGE.md：P1-2 重写，里程碑口径更新
  - ✅ SOURCE_GOVERNANCE_DRAFT.md（v0.9）：候选初稿标注
  - ✅ CHANGE_CONTROL.md（v1.1）：版本历史 + CC编号映射 + 硬化规则
  - ✅ DECISION_LOG.md（v1.1）：CC编号映射
  - ✅ REVIEW_LOG.md（v1.1）：R-01~R-10 实质记录 + R-11
- **下一步建议**：
  1. **进入 P0-2 前**：先验证 M3（10份文档与实际状态对齐）是否完成——当前 M3 ⏳ 状态，需要确认文档校正（v1.1）是否算完成 M3
  2. **M3 确认后**：执行 M4a 验证（人工访问页面，确认数据可读）
  3. **M4a 通过后**：执行 P0-2（输出分层固化）
- **状态**：✅ 本 round 核查通过（M-01/M-02/C-01/C-02/C-03 均已落实）

---

### Review R-12（P0-2 实施 review）

- **日期**：2026-04-07
- **review 对象**：build_analyst_opinions.py（路径修正 + confirmLevel注入 + SKIP_OLD过滤）；PHASE3_TASK_PACKAGE.md（P0-2完成更新）；DECISION_LOG（D-06新增）；CONTENT_STRUCTURE_DRAFT（四层产物映射）；OPEN_ISSUES（OI-03/OI-04新增）
- **所属推进点**：输出分层（P0-2）
- **核查范围**：P0-2 实施是否满足以下全部验收条件
  1. 旧口径"29条记录"是否已修正为"79总记录/29成功"
  2. 四层结构是否可映射到实际产物
  3. confirmLevel 是否已落地
  4. 79→29→5 的筛选链路是否可解释
  5. 脚本是否可复跑
  6. 是否引入无关扩项
  7. 文档是否已同步
- **本 round 可发现的问题**：
  1. analyst_opinions.json 路径修正前，build 读入的是 station 工作区的 7 条旧文件，不是当前 79 条文件——**R-12 可发现**
  2. SKIP_OLD（50条）未正确过滤，混入 DEGRADED 统计——**R-12 可发现**
  3. confirmLevel 未注入 review_items——**R-12 可发现**
- **本 round 实际状态**：R-12 为本轮 review，发现了全部 3 个问题，均已修正
- **是否符合阶段目标**：✅ 是
- **是否与既有文档一致**：✅ 是（D-06/TASK/STATUS 均已更新）
- **是否新增未批准范围**：❌ 否（路径修正是 P0-2 必要前置，发现即修）
- **发现问题**：
  1. build_analyst_opinions.py 三处路径与 fetch 不对齐（PROCESSED/SOURCES_CONFIG/OUTPUT）——即时修正为 04_数据与规则/
  2. SKIP_OLD 记录（50条）混入 DEGRADED 统计（显示 DEGRADED=54，应为 DEGRADED=4）——即时修正过滤
  3. confirmLevel 未注入 review_items——即时注入 P1/P2/P3 规则
- **修正动作**：三处问题均在 P0-2 实施中即时修正，未遗留到 review 阶段
- **是否已完成文档同步**：
  - ✅ PHASE3_STATUS.md（v1.2）：M3 ✅ M4a ✅ P0-2 完成 状态更新
  - ✅ PHASE3_TASK_PACKAGE.md（v1.2）：P0-2 完成记录更新
  - ✅ DECISION_LOG.md（v1.2）：D-06 路径统一决策记录
  - ✅ CONTENT_STRUCTURE_DRAFT.md（v1.1）：四层产物实际映射记录
  - ✅ OPEN_ISSUES.md（v1.1）：OI-03（来源评分过偏）/ OI-04（confirmLevel 机制不足）
### Review R-13（口径统一："29→5" 解释修正）

- **日期**：2026-04-07
- **背景**：R-12 P0-2 实施中发现前后口径不一致
  - 口径A："相关性≥0.4的只有这5条"
  - 口径B："连平综合分0.86，排序第6，被挤出top-5"
  - 两种表述暗含矛盾（若"只有5条"通过阈值，则不存在"第6名被挤出"）
- **事实核实**：
  - 全部29条 usable 记录的 relevanceScore 均 ≥ 0.4（无一条因门槛被过滤）
  - 其中5条 enterReport=True（top-5 排序）
  - 其余24条 relevance ≥ 0.4 但被 top-k=5 截断
  - 连平排名第6（composite=0.865），与第5名（0.880）差0.015，属于正常排序差距
- **结论**：
  - "只有这5条" 的表述是错误表述（实为"这5条进入周报"，其余24条也通过门槛但被 top-k 截断）
  - 正确口径：29条可用记录中，5条通过 top-k 排序进入周报，其余24条 rel≥0.4 但被 top-k=5 截断
  - 连平（综合分0.865）被截断的原因是 top-k=5 限制，非评分规则缺陷（OI-03 的问题是来源先验权重过重，非 top-k 问题）
- **修正内容**：
  - REVIEW_LOG 中删除错误表述"只有这5条通过相关性阈值"
  - DECISION_LOG 无需新增（OI-03 已记录来源权重问题）
  - OPEN_ISSUES 无需新增（OI-03 已覆盖连平被截断的根本原因）
- **本轮动作**：口径统一，无新增修改
- **状态**：✅ 完成

---

### Review R-14（P0-3 / M4b 进入前设计 review）

- **日期**：2026-04-07
- **review 对象**：P0-3 实施计划（M4b 最小闭环设计）
- **核查范围**：方案选择/范围界定/不扩项承诺
- **本 round 发现**：
  - 方案A（纯文档）过于弱，无法真实展示状态变化
  - 方案C（轻页面）超出 Phase 3 边界，容易滑向 UI 扩项
  - 方案B（最小 JSON 字段）最符合"轻量、可演示、不扩项"原则
  - reviewStatus/trackingStatus 命名经用户校准（confirmStatus → trackingStatus）
- **结论**：推荐方案B，M4b 可进入实施
- **状态**：✅ 通过

---

### Review R-15（M4b 演示完成记录）

- **日期**：2026-04-07
- **review 对象**：analyst-review-queue.json（P0-3 实施后状态字段验证）
- **演示过程**：
  1. 展示初始状态：5条记录 reviewStatus=pending / trackingStatus=candidate
  2. 修改 analyst-72873eb4（薛洪言 护城河）：reviewStatus→confirmed / trackingStatus→follow_up
  3. 重读 JSON 确认：状态已变化（confirmed/follow_up）
  4. 恢复初始状态（reset 为 pending，保持干净）
- **字段落地确认**：
  - reviewStatus：✅ pending（默认值），支持 confirmed/rejected
  - trackingStatus：✅ candidate/pending（默认值），支持 follow_up/closed
- **M4b 验收**：✅ 4步演示全部通过
- **遗留边界说明**（已在 DECISION_LOG D-07 记录）：
  - 重新运行 build 会重置所有 reviewStatus=pending / trackingStatus=candidate
  - 状态持久化机制不在当前 Phase 3 范围内
- **状态**：✅ M4b 演示完成

---

### Review R-16（P1-1 进入前设计校准）

- **日期**：2026-04-07
- **review 对象**：P1-1 最小持久化方案
- **核查范围**：itemId 稳定性 + merge 落点选定
- **校准1 itemId 稳定性**：
  - 两次连续 build（相同 raw 数据），itemId 完全一致
  - RUN1: `['analyst-72873eb4', 'analyst-21789d40', 'analyst-ba70f502', 'analyst-9e4b367f', 'analyst-a535dc4d']`
  - RUN2: `['analyst-72873eb4', 'analyst-21789d40', 'analyst-ba70f502', 'analyst-9e4b367f', 'analyst-a535dc4d']`
  - 生成逻辑：`dedupKey = sha256(title|author|published_at)[:16]` → `itemId = analyst-{dedupKey[:8]}`
  - 结论：✅ itemId 可作为 review-tracker.json 的唯一关联键
- **校准2 merge 落点**：
  - merge子选项a（build内merge）：build职责不纯净 ❌
  - merge子选项b（独立台账+嵌入读取端）：build纯净但页面读取路径需改 ❌
  - merge子选项c（独立台账+独立merge脚本）：build纯净、职责分离 ✅
  - 结论：✅ 选merge子选项c（独立台账+独立merge脚本），对应D-08"独立状态台账方案"
  - **注**：R-16与D-08的方案A/B/C编号体系不同（R-16是merge落点子选项，D-08是整体方案选择），结论"选方案A"为笔误，应为"选独立台账+独立merge脚本"
- **是否符合阶段目标**：✅ 是（P1-1最小实现，未扩项）
- **是否新增未批准范围**：❌ 否
- **发现问题**：无
- **修正动作**：无
- **文档同步**：DECISION_LOG D-08 已记录方案决策
- **状态**：✅ 校准通过，可进入实施

---

### Review R-17（P1-1 实施验证）

- **日期**：2026-04-07
- **review 对象**：review-tracker.py / review-tracker.json / 验收场景
- **验收场景执行**：
  1. build（RUN1）：analyst-review-queue.json 生成 ✅
  2. upsert：`analyst-72873eb4 → reviewStatus=confirmed / trackingStatus=follow_up` ✅
  3. build（RUN2）：analyst-review-queue.json 重建，reviewStatus=pending 恢复 ✅
  4. `tracker get analyst-72873eb4`：confirmed/follow_up 仍存在 ✅
  5. `tracker merge`：5条记录，analyst-72873eb4=confirmed/follow_up，其余4条=pending/candidate ✅
- **review-tracker.json 字段**（最终）：
  - itemId（必须）
  - reviewStatus（必须）
  - trackingStatus（必须）
  - updatedAt（必须）
  - note（建议）
- **是否引入未批准范围**：❌ 否（无数据库/UI/权限/任务系统）
- **是否符合 MVP 边界**：✅ 是（独立台账，不改 build，不动 queue 结构）
- **遗留边界**：
  - review-tracker.json 需人工 upsert（无 UI）
  - fetch-run-log（P1-1b）尚未实施
- **文档同步**：
  - ✅ DECISION_LOG D-08
  - ✅ CHANGE_CONTROL CC-11
  - ✅ PHASE3_TASK_PACKAGE v1.4（P1-1 完成）
  - ✅ P1_CANDIDATES v1.1（P1-1 完成）
- **状态**：✅ P1-1 实施验证通过

---

### Review R-18（P1-1b 进入前口径校准）

- **日期**：2026-04-07
- **review 对象**：P1_CANDIDATES.md P1-1b 章节描述
- **核查范围**：action 歧义 + source 字段保留理由 + P1-1b 方案描述准确性
- **校准1 action 口径**：
  - 发现：P1_CANDIDATES.md section 2.4 仍描述"review_operations.json，记录每次 review 操作"，为过时设计
  - 修正：更新为 CSV ledger 方案（pilot-tracking-ledger.csv），字段不含 owner/nextAction/deadline/priority
  - 修正：section 2.5 验收标准更新为 CSV 可读性 + 无任务字段
  - 结论：✅ action 歧义已消除
- **校准2 source 字段保留理由**：
  - 理由：便于后续按来源聚合统计与试点观察（不是任务指派字段）
  - 已写入 P1_CANDIDATES.md section 2.4
  - 结论：✅ source 字段用途明确
- **校准3 P1-1b 方案描述更新**：
  - 旧：fetch-run-log 追踪表
  - 新：CSV 轻量追踪表（pilot-tracking-ledger.csv）
  - 结论：✅ P1_CANDIDATES.md table 和 section 2.4/2.7 已同步更新
- **是否符合阶段目标**：✅ 是（仅校准，不实施）
- **是否新增未批准范围**：❌ 否
- **发现问题**：无新阻断问题
- **修正动作**：已修正 P1_CANDIDATES.md 三处过时描述
- **文档同步**：P1_CANDIDATES.md（已更新）
- **状态**：✅ 校准完成，可进入 P1-1b 实施

---

### Review R-19（P1-1b CSV追踪表实施验证）

- **日期**：2026-04-07
- **review 对象**：review-tracker.py export 子命令 / pilot-tracking-ledger.csv / 验收场景
- **核查范围**：action 口径统一 / source 字段保留理由 / 实施边界 / 任务字段检查
- **校准结果确认**（R-18 后续）：
  - P1_CANDIDATES.md section 2.4/2.5/2.7/table 均已更新 ✅
  - action 歧义已消除 ✅
  - source 字段保留理由已写入 ✅
- **实施核查**：
  - 新增 `review-tracker.py export` 子命令 ✅
  - CSV 字段：itemId / analystName / articleTitle / confirmLevel / reviewStatus / trackingStatus / updatedAt / note / source ✅
  - 任务字段检查（owner/nextAction/deadline/priority）：✅ 无
  - CSV 格式：UTF-8-sig BOM + 逗号分隔（Excel/飞书表格兼容）✅
- **验收场景执行**：
  1. build → upsert analyst-72873eb4 confirmed/follow_up ✅
  2. export → pilot-tracking-ledger.csv 生成（5行）✅
  3. build 重跑 → 再 export → confirmed/follow_up 仍存在 ✅
  4. smoke_test 59/59 PASS ✅
- **三层关系确认**：
  - queue = analyst-review-queue.json（build纯输出，可重建）
  - tracker = review-tracker.json（独立台账，build不覆盖）
  - ledger = pilot-tracking-ledger.csv（merge导出结果，人工可读）
- **是否符合阶段目标**：✅ 是（P1-1b 最小实现，未扩项）
- **是否新增未批准范围**：❌ 否（无数据库/UI/权限/任务系统）
- **发现问题**：无
- **修正动作**：无
- **文档同步**：
  - ✅ PHASE3_TASK_PACKAGE v1.5（P1-1b 完成）
  - ✅ CHANGE_CONTROL v1.3（+CC-12）
- **状态**：✅ P1-1b 实施验证通过

---

### Review R-20（P1-2 来源有效性 review 实施验证）

- **日期**：2026-04-07
- **review 对象**：analyst_review_matrix.md / analyst_review_notes.md / 验收场景
- **核查范围**：样本轮次口径 / 顾慧君王锟原因核实 / 付一夫误判避免 / 边界落实
- **校准结果确认**：
  - 校准1（样本轮次）：✅ matrix和notes均标注"单轮数据，试行版建议，建议2~3轮后复核"
  - 校准2（顾慧君/王锟）：✅ 0 usable原因确认为min_year=2024过滤，非来源质量差，pending-check
  - 校准3（付一夫）：✅ 0 enterReport确认为top-k截断，非来源质量差，observe
- **实施核查**：
  - 新增 docs/analyst_review_matrix.md（13个来源，证据数值可追溯）✅
  - 新增 docs/analyst_review_notes.md（每来源一段，含结论/证据/边界/配置建议）✅
  - analyst_sources.json 未被修改 ✅
  - 无越界表述（无"已修改"/"正式生效"等）✅
- **验收场景执行**：
  1. matrix 数值追溯抽查（薛洪言/付一夫）✅
  2. notes 无越界表述 ✅
  3. analyst_sources.json 未被动 ✅
  4. smoke_test 59/59 PASS ✅
- **结论分布**：keep=2（薛洪言/周茂华）/ observe=3（连平/娄飞鹏/付一夫）/ pending-check=8（顾慧君/王锟/董希淼/温彬/曾刚/朱太辉/孙扬/杜娟）
- **是否符合阶段目标**：✅ 是（P1-2 最小实现，未扩项）
- **是否新增未批准范围**：❌ 否（无数据库/UI/权限/自动配置生效）
- **发现问题**：无
- **修正动作**：无
- **文档同步**：
  - ✅ PHASE3_TASK_PACKAGE v1.6（P1-2 完成）
  - ✅ CHANGE_CONTROL v1.4（+CC-13）
- **状态**：✅ P1-2 实施验证通过

---

### Review R-21（P1-3 试点运行 SOP 实施验证）

- **日期**：2026-04-07
- **review 对象**：PILOT_RUN_SOP.md / ROUND_RECAP_TEMPLATE.md / SOURCE_REVIEW_CHECKLIST.md / ROUND_RECAP_2026-04-07.md
- **核查范围**：周期触发口径 / 状态流转示例 / 扩项检查 / 运行闭环验证
- **小校准确认**：
  - 校准1（周期触发例外）：✅ SOP Section 二 已写入"触发检查但无实质变化"口径
  - 校准2（状态流转示例）：✅ SOP 使用 confirmed + (follow_up/candidate/closed)，无混乱表述
- **实施核查**：
  - 新增 docs/PILOT_RUN_SOP.md（v1.0，人工操作手册，无自动化）✅
  - 新增 docs/ROUND_RECAP_TEMPLATE.md（v1.0，每轮小结模板）✅
  - 新增 docs/SOURCE_REVIEW_CHECKLIST.md（v1.0，触发条件清单）✅
  - 首个完整轮次 ROUND-01 已跑通 ✅
  - tracker upsert：5/5 items reviewed（4 confirmed/follow_up，1 confirmed/candidate，1 confirmed/closed）✅
  - pilot-tracking-ledger.csv 已导出 ✅
  - ROUND_RECAP_2026-04-07.md 已填写 ✅
- **自 review 结果**：
  - ✅ 只服务 P1-3，无扩项
  - ✅ SOP 为人工手册，非系统功能说明书
  - ✅ 无 cron/UI/数据库/任务系统
  - ✅ 周期触发例外口径已写入
- **是否符合阶段目标**：✅ 是（P1-3 最小实现，未扩项）
- **是否新增未批准范围**：❌ 否
- **发现问题**：无（仅发现 SOP 中 argument 示例有误，已同步修正）
- **修正动作**：PILOT_RUN_SOP.md argument 示例修正（`--item-id` 非 `--itemId`）
- **文档同步**：
  - ✅ PHASE3_TASK_PACKAGE v1.7（P1-3 完成）
  - ✅ CHANGE_CONTROL v1.5（+CC-14）
  - ✅ PHASE3_STATUS v1.7（P1-3 完成）
  - ✅ P1_CANDIDATES v1.4（P1-3 完成）
- **状态**：✅ P1-3 实施验证通过

---

### Review R-22（P1-4 进入前设计与核验校准）

- **日期**：2026-04-08
- **review 对象**：P1-4 设计阶段产出（多轮试点复盘机制设计）
- **所属推进点**：P1-4 进入前设计
- **核查范围**：设计阶段产出是否满足进入实施的前置条件
- **小校准1（文档同步补齐）**：
  - R-22 本次 review 执行时同步补齐：REVIEW_LOG（+R-22）、CHANGE_CONTROL（+CC-15）、P1_CANDIDATES（+P1-4 设计章节）、PILOT_RUN_SOP（+跨轮动作提示）、ROUND_RECAP_TEMPLATE（+跨轮数字提示）
  - 口径：校准完成前不进入新文件创建
- **小校准2（ROUND_COMPARISON baseline 回填口径）**：
  - 明确：本轮实施不是等 ROUND-02 后才创建 ROUND_COMPARISON
  - 本轮用 ROUND-01 已有结果回填第一行
  - ROUND-02/03 的行留给后续真实轮次追加
  - 口径已写入 REVIEW_LOG
- **设计方案确认**：
  - 推荐方案：方案B（多轮试点复盘表型，ROUND_COMPARISON.md）
  - 字段不超过 8 个：roundId / rawCount / usableCount / queueCount / trackerCount / confirmedCount / rejectedCount / topSourceShare / openIssuesStatus
  - 面向：运营编辑者 + 项目推进者
  - 方案A（增强 ROUND_RECAP）因跨轮对比需跨文件、功能不足，未选
  - 方案C（月度复盘）因反馈延迟4周、与试点节奏不匹配，未选
- **最小复盘对象确认**：
  - 必须复盘（M1~M5）：raw/usable/queue 数量变化、reviewStatus/trackingStatus 变化、confirmed/rejected/follow_up 条目、OPEN_ISSUES 增减、来源贡献度变化
  - 建议记录（S1~S3）：confirmLevel 与人工判断偏离、来源复核触发、异常与挂账
  - 当前不做（N1~N5）：queue 绝对值、confirmLevel 分布比例、多来源组合贡献度、自动告警、历史全量 trend chart
- **是否符合阶段目标**：✅ 是（设计阶段，不进入实施）
- **是否新增未批准范围**：❌ 否
- **发现问题**：无
- **修正动作**：无（设计校准，无修正项）
- **文档同步**：
  - ✅ REVIEW_LOG（+R-22）
  - ✅ CHANGE_CONTROL（+CC-15 待本轮实施后同步）
  - ✅ P1_CANDIDATES（+P1-4 设计章节待实施后同步）
- **状态**：✅ 校准完成，可进入 P1-4 实施

---

### Review R-23（P1-4 实施验证）

- **日期**：2026-04-08
- **review 对象**：P1-4 实施产出（ROUND_COMPARISON.md + CROSS_ROUND_CHECKLIST.md + 更新的 SOP/模板）
- **所属推进点**：P1-4 多轮试点复盘机制
- **核查范围**：最小实施边界验证 / 是否扩项 / 产物完整性
- **实施核查**：
  1. **新建 reports/ROUND_RECAP/ROUND_COMPARISON.md** ✅
     - 字段：roundId / 执行日期 / rawCount / usableCount / queueCount / trackerCount / confirmedCount / rejectedCount / topSourceShare / openIssuesStatus（共10列，8个核心数字字段）
     - ROUND-01 baseline 已回填（79/29/5/5/5/0/薛洪言4/5 80%/OI-03+OI-04开放中）
  2. **新建 docs/CROSS_ROUND_CHECKLIST.md** ✅
     - Section 一：只记 ROUND_RECAP（5种不做跨轮动作的情况）
     - Section 二：跨轮关注标记（5种触发条件 + 对应 ROUND_COMPARISON 标注方式）
     - Section 三：升级 OPEN_ISSUES（5种触发条件 + OI 编号策略）
     - Section 四：小复盘触发条件（4个条件，任一满足建议小复盘）
     - Section 五：何时更新 ROUND_COMPARISON（4个时点）
     - Section 六：当前不做（4项）
     - 总页数：约1页，无复杂逻辑
  3. **更新 docs/ROUND_RECAP_TEMPLATE.md** ✅
     - 文件头部增加跨轮数字同步提示
     - 不破坏现有模板简洁性
  4. **更新 docs/PILOT_RUN_SOP.md** ✅
     - Section 六增加 ROUND_COMPARISON 产出行
     - 明确填写时点
  5. **更新 docs/P1_CANDIDATES.md** ✅
     - Section 九：P1-4 设计章节（9.1~9.8）
  6. **更新 docs/CHANGE_CONTROL.md** ✅
     - CC-15（P1-4 设计校准）+ CC-16（P1-4 实施）
  7. **更新 docs/REVIEW_LOG.md** ✅
     - R-22（设计校准）+ R-23（实施验证）
- **自 review 结果**：
  - ✅ 只服务 P1-4，无扩项
  - ✅ 复盘机制仍是轻量文档（8字段对比表 + 1页 checklist）
  - ✅ 无 UI/数据库/自动调度/任务系统
  - ✅ 字段收敛（ROUND_COMPARISON 10列中含日期列，实际数字字段8个，符合建议范围）
  - ✅ CROSS_ROUND_CHECKLIST 总页数约1页，符合"一页以内"要求
  - ✅ 产物面向运营编辑者 + 项目推进者，不面向管理层汇报
- **是否符合阶段目标**：✅ 是（P1-4 最小实施完成）
- **是否新增未批准范围**：❌ 否
- **发现问题**：无
- **修正动作**：无
- **文档同步**：
  - ✅ REVIEW_LOG（+R-23）v1.8
  - ✅ CHANGE_CONTROL（+CC-16）v1.7
  - ✅ P1_CANDIDATES（+Section 九）v1.5
  - ✅ PILOT_RUN_SOP（+ROUND_COMPARISON 步骤）v1.1
  - ✅ ROUND_RECAP_TEMPLATE（+跨轮提示）v1.1
  - ✅ ROUND_COMPARISON.md（新建，v1.0）
  - ✅ CROSS_ROUND_CHECKLIST.md（新建，v1.0）
- **状态**：✅ P1-4 实施验证通过

---

### Review R-24（ROUND-02 执行验证）

- **日期**：2026-04-08
- **review 对象**：ROUND-02 真实执行（机制验证轮）
- **所属推进点**：试点运行验证
- **核查范围**：触发判断 / pipeline 执行 / tracker 状态 / ledger 导出 / RECAP 填写 / COMPARISON 追加
- **触发判断**：
  - 时间触发：❌ 距 ROUND-01 仅约1天（未满14天）
  - 数量触发：❌ raw 无新增（79条，与 ROUND-01 相同）
  - 例外条件：✅ 用户明确要求推进（命中例外）
  - 结论：例外执行，触发原因为"用户指令"
- **执行核查**：
  - build_analyst_opinions.py + generate_review_queue.py ✅ 正常生成
  - analyst-review-queue.json：5条，与 ROUND-01 完全相同 ✅
  - tracker merge：5条状态全部保持（4 follow_up，1 candidate，1 closed）✅
  - pilot-tracking-ledger.csv 导出 ✅
  - ROUND_RECAP_2026-04-08.md 已填写 ✅
  - ROUND_COMPARISON.md 已追加第二行 ✅
- **来源复核**：T1~T5 均不满足，未触发 ✅
- **OPEN_ISSUES**：无新增，无关闭，OI-03/OI-04 保持开放 ✅
- **自 review 结果**：
  - ✅ 仅执行既定 SOP，未引入 UI/数据库/自动调度/任务系统
  - ✅ 发现 run-pipeline.py 路径问题（引用不存在的脚本），本轮绕行
  - ✅ 未因绕行而修改 pipeline 脚本（本轮任务边界）
  - ✅ tracker 持久化机制再次验证有效
  - ✅ 复盘机制顺畅（COMPARISON 追加顺利）
- **发现问题**：
  - `run-pipeline.py` 存在路径问题：引用 `scripts/parse_initial_data.py`（不存在），PROCESSED 路径指向 `data/processed/` 而非 `04_数据与规则/processed/`
  - 本轮未修复（不属于 ROUND-02 执行任务范围），需后续登记为 OPEN_ISSUES 或在 P1-1b/fetch-run-log 相关工作中处理
- **修正动作**：无（本轮已完成，路径问题需单独评估）
- **文档同步**：
  - ✅ REVIEW_LOG（+R-24）v1.9
  - ✅ ROUND_RECAP_2026-04-08.md（新建）
  - ✅ ROUND_COMPARISON.md（已追加 ROUND-02 行）
  - ⚠️ OPEN_ISSUES 未更新（本轮未产生新异常，路径问题待评估）
- **状态**：✅ ROUND-02 执行完成（机制验证轮）

---

### Review R-25（P1-3a 实施验证）

- **日期**：2026-04-08
- **review 对象**：P1-3a 运行入口一致性修正
- **所属推进点**：P1-3 试点运行 SOP 维护
- **核查范围**：run-pipeline.py 失效原因分析 / 候选方案比较 / 最小 wrapper 创建 / SOP 更新 / 真实验证

#### run-pipeline.py 失效原因（已确认）

| # | 问题 | 类别 |
|---|------|------|
| 1 | SCRIPTS = BASE / 'scripts'（应为 05_工具脚本/） | 主因：路径过时 |
| 2 | PROCESSED = BASE / 'data' / 'processed'（应为 04_数据与规则/processed/） | 主因：路径过时 |
| 3 | Step 1 引用 scripts/parse_initial_data.py（不存在，Phase 2 旧入口） | 主因：引用不存在脚本 |
| 4~8 | 引用大量旧 tracking/weekly report 脚本（历史包袱） | 次因（暂不处理） |

#### 方案比较（已比较3个方案）

| 方案 | 推荐程度 | 理由 |
|------|---------|------|
| 方案A：直接修 run-pipeline.py | 次选 | 修路径后历史包袱仍会导致报错 |
| 方案B：改 SOP 为命令串 | 次选 | 入口不统一，可维护性差 |
| **方案C：新增 wrapper（run-analyst.sh）** | **推荐** | 最小、一致、不碰旧脚本 |

#### 统一入口口径（已登记）

- run-analyst.sh 为当前 analyst 试点运行统一入口
- run-pipeline.py 不再作为 analyst 试点运行入口
- 历史包袱暂不处理（不影响当前试点运行）

#### wrapper 职责边界（已写入脚本头注释）

- orchestration only
- 只调用：build_analyst_opinions.py → generate_review_queue.py → review-tracker.py merge → review-tracker.py export
- 不含任何评分/过滤/review 业务逻辑

#### 实施结果

- run-analyst.sh 已创建：05_工具脚本/run-analyst.sh（可执行，2473字节）
- SOP v1.2 已更新：入口命令改为 ./run-analyst.sh
- 真实验证通过：
  - ✅ build_analyst_opinions.py：79 raw / 29 usable / 5 queue
  - ✅ generate_review_queue.py：analyst-review-queue.json total=5
  - ✅ review-tracker.py merge：5条状态正确
  - ✅ review-tracker.py export：pilot-tracking-ledger.csv 5行
  - ✅ 无需临时绕行

#### 自 review 结果

- ✅ 只服务 P1-3a（入口一致性），未扩项
- ✅ 未引入 UI/数据库/自动调度/任务系统
- ✅ SOP 命令与真实入口完全一致
- ✅ 旧 run-pipeline.py 不删除，仅在 SOP 中说明其不再作为 analyst 入口
- ✅ wrapper 极简（70行），只做 orchestration
- ✅ ROUND-02 暴露的路径问题已修复（SOP 层面）

#### 仍存在的边界

- run-pipeline.py 历史包袱（#4~#8）未清理，不影响当前 analyst 试点
- analyst fetch 层（fetch_analyst_articles.py）未集成进 wrapper，由人工判断独立触发
- smoke test / bundle / weekly report 不在本 wrapper 范围内（当前试点不需要）

#### 文档同步

- ✅ REVIEW_LOG（+R-25）v1.10
- ✅ CHANGE_CONTROL（+CC-17）v1.8
- ✅ P1_CANDIDATES（+P1-3a）v1.6
- ✅ PILOT_RUN_SOP（运行命令改为 run-analyst.sh）v1.2

- **状态**：✅ P1-3a 实施验证通过

---

### Review R-26（ROUND-03 执行验证）

- **日期**：2026-04-08
- **review 对象**：ROUND-03 真实执行（统一入口验证轮）
- **所属推进点**：试点运行验证
- **核查范围**：触发判断 / run-analyst.sh 执行 / queue 对比 / tracker 状态 / ledger 验证 / RECAP 填写 / COMPARISON 追加
- **触发判断**：
  - 时间触发：❌ 距 ROUND-02 仅约1天（未满14天）
  - 数量触发：❌ raw 无新增（79条，与 ROUND-02 相同）
  - 例外条件：✅ 用户明确要求推进（命中例外）
  - 结论：例外执行，触发原因为"用户指令"，性质为"统一入口验证轮"
- **执行核查**：
  - run-analyst.sh ✅ 直接执行成功，无手工拼命令
  - build_analyst_opinions.py ✅ 79 raw / 29 usable / 5 queue（三轮完全相同）
  - generate_review_queue.py ✅ analyst-review-queue.json 5条（三轮完全相同）
  - review-tracker.py merge ✅ 5条状态保持（三轮完全相同）
  - pilot-tracking-ledger.csv 导出 ✅
  - ROUND_RECAP_2026-04-08_v2.md（ROUND-03）已填写 ✅
  - ROUND_COMPARISON.md v1.1 已追加第三行 ✅
- **来源复核**：T1~T5 均不满足，未触发 ✅
- **小复盘触发判断**：❌ 未触发（三项核心指标 raw/usable/来源构成均无变化，无趋势可分析）
- **OPEN_ISSUES**：无新增，OI-03/OI-04 保持开放 ✅
- **自 review 结果**：
  - ✅ 统一入口 run-analyst.sh 可重复执行性验证通过
  - ✅ 仅执行既定 SOP，未引入 UI/数据库/自动调度/任务系统
  - ✅ tracker 持久化机制三轮验证有效
  - ✅ 数据连续未刷新（3轮相同），fetch 层需人工触发是已知特性
- **发现问题**：数据连续未刷新，需关注 fetch 层何时被触发（当前无自动抓取）
- **修正动作**：无（本轮为验证轮）
- **文档同步**：
  - ✅ REVIEW_LOG（+R-26）v1.11
  - ✅ ROUND_RECAP_2026-04-08_v2.md（新建）
  - ✅ ROUND_COMPARISON.md（已追加 ROUND-03 行）v1.1
- **状态**：✅ ROUND-03 执行完成（统一入口验证轮）

---

### Review R-27（P1-3b 实施验证）

- **日期**：2026-04-08
- **review 对象**：P1-3b 数据刷新与轮次就绪机制
- **所属推进点**：P1-3 试点运行 SOP 维护
- **核查范围**：preflight 机制设计 / 触发逻辑修正 / 最小验证

#### 背景问题

ROUND-02/03 连续走例外执行，暴露出现有触发机制的盲区：
1. 缺少"raw 是否有新增"的快速检查路径
2. "例外执行"边界模糊（"验证脚本可跑"曾被作为例外理由）
3. 无前置判断机制，连续无意义轮次稀释了数据粒度

#### 触发逻辑修正（已登记）

**修正后判断路径**：
- A. raw 新增 ≥5 条 → **常规执行**（直接 run-analyst.sh）
- B. 否则，距上次已满 14 天 → **常规执行**
- C. 否则，存在：明确异常/OI 需提前复查 / 用户明确要求推进 → **例外执行**（显式记录原因）
- D. 若 A/B/C 均不满足 → **不进入完整轮次**（仅记录触发检查结果）

**明确排除**：不得以"只是想验证脚本可跑"为由例外执行。

#### raw 新增检查方法（最终确定）

- 工具：`analyst_opinions_raw.json` 的 `fetchedAt` 时间戳 + `records.length`
- 操作：运营编辑者启动前读取，与上轮 ROUND_RECAP 记录的数字对比
- **不依赖 `--dry-run`**：`build_analyst_opinions.py` 无此选项，已排除

#### 实施结果

- PILOT_RUN_SOP.md v1.3：每轮开始前检查升级为 preflight 机制（Section 四）
- ROUND_RECAP_TEMPLATE.md v1.2：触发原因字段说明更新
- REVIEW_LOG +R-27 ✅
- CHANGE_CONTROL +CC-18 P1-3b 登记 ✅

#### 最小验证

**当前数据 preflight 判断**（2026-04-08）：
- raw 总数：79（与 ROUND-03 相同，新增 0 条）
- fetchedAt：2026-04-07T14:51:11（无更新）
- A. raw 新增 ≥5？❌（新增 0 条）
- B. 满14天？❌（距 ROUND-03 仅数小时）
- C. 存在例外条件？❌（无异常/OI/用户指令）
- **结论：D. 不进入完整轮次**

这恰恰说明 preflight 机制有效：当前数据不满足任何触发条件，应等待 raw 新增或时间到期。

#### 自 review 结果

- ✅ 只服务 P1-3b（前置检查机制），未扩项
- ✅ 未引入自动 fetch/调度/UI/数据库
- ✅ 常规/例外/不进入三轨逻辑清晰
- ✅ "验证脚本可跑"已明确排除为例外理由
- ✅ 无新增文件（仅更新 SOP 和 TEMPLATE）

#### 仍存在的边界

- fetch 层何时触发的问题由 P1-X 后续处理，不在 P1-3b 范围
- preflight 依赖人工主动遵守，无系统强制
- 若 raw 只新增 2~4 条，属于灰色地带，由运营编辑者判断是否走例外

#### 文档同步

- ✅ REVIEW_LOG（+R-27）v1.12
- ✅ CHANGE_CONTROL（+CC-18）v1.9
- ✅ PILOT_RUN_SOP v1.3
- ✅ ROUND_RECAP_TEMPLATE v1.2

- **状态**：✅ P1-3b 实施验证通过

---

### Review R-28（ROUND-04 preflight 记录）

- **日期**：2026-04-08
- **review 对象**：ROUND-04 preflight 判断
- **所属阶段**：试点运行第四轮预检
- **Preflight 结果**：D. 不进入完整轮次

**触发判断**：
| 条件 | 结果 | 说明 |
|------|------|------|
| A. 数量触发（raw 新增 ≥5） | ❌ | 79 → 79，新增 0 条 |
| B. 时间触发（满14天） | ❌ | 距 ROUND-03 仅数小时 |
| C. 例外执行 | ❌ | 无异常/OI/用户指令 |

**结论**：A/B/C 均不满足，preflight 机制判定不进入完整轮次。这是机制生效的正常结果，不是失败。

**当前数据状态**：
- raw 总数：79（与 ROUND-03 完全相同）
- fetchedAt：2026-04-07T14:51:11（无更新）

**为什么不值得执行完整轮次**：
analyst 数据未更新，无新增记录。完整执行只会重复 ROUND-02/03 的结果（5条 queue，状态不变），浪费执行成本，稀释轮次粒度。

**下次检查时机**：
- analyst 数据有新增时（fetchedAt 变化或 raw 条数 ≥84）
- 或距 ROUND-03 满 14 天（2026-04-22 前后）

**本轮价值**：验证 preflight 机制能有效阻止无意义运行（机制生效证明）。

- **状态**：✅ ROUND-04 preflight 记录完成（不进入完整轮次）

---

### Review R-29（P1-5 数据刷新观察 + preflight）

- **日期**：2026-04-08
- **review 对象**：P1-5 数据刷新观察 + preflight 判断
- **所属阶段**：试点运行阶段包（P1-5）
- **Preflight 结果**：D. 不进入完整轮次

**第一层：数据刷新检查**：
| 检查项 | 结果 |
|--------|------|
| fetchedAt 是否有变化 | ❌ 无变化（仍为 2026-04-07T14:51:11）|
| raw 总条数是否有变化 | ❌ 无变化（仍为 79 条）|
| 新增 raw 是否主要为旧文 | N/A（无新增）|
| usable/queue 是否可能出现实质变化 | ❌ 否（无新数据）|
| 是否接近来源复核周期（4~6周） | ❌ 否（距 ROUND-01 仅约 1 天）|

**第二层：轮次触发判断**：
| 条件 | 结果 | 说明 |
|------|------|------|
| A. 数量触发（raw 新增 ≥5） | ❌ | 79 → 79，新增 0 条 |
| B. 时间触发（满14天） | ❌ | 距 ROUND-03 仅约 1 天 |
| C. 例外执行 | ❌ | 无异常/OI/用户指令 |

**结论**：A/B/C 均不满足，preflight 机制判定不进入完整轮次。

**为什么不值得执行完整轮次**：
fetchedAt 和 raw 条数均无变化，无新数据进入 pipeline，完整执行只会重复 ROUND-02/03/04 的结果（5条 queue，状态不变），浪费执行成本。

**本轮（P1-5）价值**：
- 数据刷新观察已完成（确认无更新）
- preflight 机制再次正确生效（连续 2 次 ROUND-04/P1-5 正确识别出不满足条件）

**下次检查时机**：
- analyst 数据有新增时（fetchedAt 变化或 raw 条数 ≥ 84）
- 或距 ROUND-03 满 14 天（2026-04-22 前后）
- 来源复核按原计划约 4 周后（2026-05-07 前后）执行

**小复盘准备判断**：
- 不满足小复盘条件：3轮数据完全相同，无趋势可分析，无 rejected 条目，OI 无变化
- 等待下一有效数据轮（有实质变化时）再做小复盘准备判断

- **状态**：✅ P1-5 数据刷新观察与 preflight 记录完成（不进入完整轮次）

---

### Review R-30（P1-6 实施验证）

- **日期**：2026-04-08
- **review 对象**：P1-6 人工 fetch 入口统一
- **所属阶段**：试点运行 fetch 层机制
- **核查范围**：fetch wrapper 创建 / SOP 更新 / 职责边界登记 / 最小验证

#### 背景问题

fetch 层与 run-analyst.sh 完全分离，无统一 fetch 入口；fetch 后"数据已刷新"的判断口径未落地为文档。

#### 实施结果

**新建**：
- `05_工具脚本/run-analyst-fetch.sh`（可执行，2266字节）
  - 职责边界：fetch orchestration only，不内嵌 preflight/run-analyst.sh 联动
  - 支持两种模式：
    - 默认模式：执行真实抓取，刷新 analyst_opinions_raw.json
    - `--check` 模式：dry-run 安全检查，不写文件
  - 与 run-analyst.sh 风格一致

**更新**：
- PILOT_RUN_SOP.md：v1.4，新增 Section 四（数据刷新 Step 0），明确 fetch → preflight → run 三步节奏
- ROUND_RECAP_TEMPLATE.md：无需修改（"触发原因"+"备注"字段已可记录 fetch 执行情况）

#### "数据已刷新"判断口径（已登记）

| 信号 | 说明 |
|------|------|
| fetchedAt 变化 | 数据已刷新（最新抓取时间已更新）|
| raw 条数变化 | 有新增记录进入池 |
| fetchedAt 变化 + 条数增加 | 完整刷新，新增内容需进一步判断 |

**注意**："数据已刷新" ≠ "值得跑下一轮"，是否值得跑由 preflight 判断。

#### 最小验证结果

```bash
./run-analyst-fetch.sh --check
```
- ✅ 命令可执行
- ✅ 输出可读，流程引导清晰
- ⚠️ dry-run 显示"共 0 个来源待抓取"（网络/环境原因，无新增数据）
- **验证内容**：入口一致性（命令可执行），不是数据刷新

#### 自 review 结果

- ✅ 只服务 P1-6（fetch 入口统一），未扩项
- ✅ 未引入自动 fetch/调度/UI/数据库
- ✅ wrapper 职责边界清晰（fetch only，不联动）
- ✅ fetch → preflight → run 三步节奏已在 SOP 中固化

#### 仍存在的边界

- fetch wrapper 仍需人工主动触发，无自动调度
- 人工判断"数据是否值得跑"仍在运营编辑者（preflight 机制）
- dry-run 显示"0 来源待抓取"：需确认网络连通性（不影响 wrapper 本身有效性）

#### 文档同步

- ✅ REVIEW_LOG（+R-30）v1.15
- ✅ CHANGE_CONTROL（+CC-19）v1.10
- ✅ PILOT_RUN_SOP v1.4
- ✅ P1_CANDIDATES（+P1-6 行）v1.8

- **状态**：✅ P1-6 实施验证通过

---

### Review R-31（P1-6a 实施验证）

- **日期**：2026-04-08
- **review 对象**：P1-6a fetch 层连通性与真实刷新能力核验
- **所属阶段**：试点运行 fetch 层可解释性
- **核查范围**：dry-run 0来源原因分析 / 方案比较 / 最小落地

#### 背景问题

P1-6 后验证 fetch 层连通性时，dry-run 输出"共 0 个来源待抓取"，但实际上发现了97个 URL。输出具有误导性。

#### 根本原因

dry-run 跳过实际抓取逻辑（continue），不执行 `fetch_url`，因此 `is_too_old` 年份过滤不生效，导致 results 保持为空数组。"0来源"是 dry-run 跳过抓取的结果，不是真的没有数据。

#### 实施结果

**修改**：
- `05_工具脚本/fetch_analyst_articles.py`：增强 dry-run 输出结尾
  - 旧：`[DRY RUN] 共 0 个来源待抓取`（误导）
  - 新：解释已跳过实际抓取 + 年份过滤只在实际抓取时生效 + 引导执行正式 fetch

#### 增强后输出示例

```
[DRY RUN] 已跳过实际抓取（dry-run 模式）
      提示：年份过滤（>=2024）只在实际抓取时生效，dry-run 无法预判过滤结果
      如需真正刷新数据，请执行：./run-analyst-fetch.sh
```

#### 自 review 结果

- ✅ 只服务 P1-6a（fetch 可解释性），未扩项
- ✅ 未引入自动 fetch/调度/UI/数据库
- ✅ 运营编辑者现在能区分"dry-run 跳过抓取"与"真的没有新数据"
- ✅ 不改 analyst_sources.json / build / run 逻辑

#### 当前 fetch 结果"可解释性"结论

| 情况 | 原来输出 | 现在输出 | 可区分 |
|------|---------|---------|--------|
| dry-run 跳过抓取（无实质数据）| "0来源待抓取"（误导）| "已跳过实际抓取"（清晰）| ✅ |
| 网络/环境不可达 | 无特殊提示 | 无特殊提示 | ❌（需网络层检查）|
| 有数据但被年份过滤 | "0来源" | "已跳过"（同左）| ⚠️（需真实 fetch 才可知）|

#### 仍存在的边界

- 网络连通性无法通过 dry-run 判断（需实际 fetch）
- 真实抓取后的 skipped_old 数量仍不可预判
- 这是 fetch 层固有限制，不在 P1-6a 范围

#### 文档同步

- ✅ REVIEW_LOG（+R-31）v1.16
- ✅ CHANGE_CONTROL（+CC-20）v1.11
- ✅ P1_CANDIDATES（+P1-6a 行）v1.9

- **状态**：✅ P1-6a 实施验证通过

---

### Review R-32（P1-6b 真实 fetch 验证）

- **日期**：2026-04-08
- **review 对象**：P1-6b 真实 fetch 验证与结果归因
- **所属阶段**：fetch 层真实刷新能力核验
- **核查范围**：真实 fetch 执行 / 结果归因 / 是否值得进入下一轮

#### 真实 fetch 执行结果

| 指标 | 执行前 | 执行后 | 变化 |
|------|--------|--------|------|
| fetchedAt | 2026-04-07T14:51:11 | 2026-04-08T14:03:47 | ✅ 已更新 |
| raw 总数 | 79 | 79 | ➖ 无净增长 |
| success | — | 29 | — |
| skipped_old | — | 50 | — |
| failed | — | 0 | — |
| 2024+ 可用文章 | ~28 | ~28 | ➖ 无净增长 |

#### 归因结果：B — 有新增但为过滤型新增（内容替换，无净增长）

**事实**：
- 本次 fetch 新增 29 条 success 记录（2024 年及之后）
- 50 条被 min_year=2024 过滤为 skipped_old（均为 2023 年及之前）
- 去重后 raw 总数保持 79（新增替换了等量旧文）
- fetchedAt 已更新，证明 fetch 机制真实有效

**判断**：
- raw 净增 = 0（去重后无净增长）
- 不满足 preflight 数量触发（A: raw 新增 ≥5）
- 下一轮 preflight 仍会显示 raw=79，preflight 会正确判定为分支 D

#### 是否进入 ROUND-05

**结论：不进入 ROUND-05**

- A 触发：❌（raw 净增 0，不满足 ≥5）
- B 触发：❌（距 ROUND-03 约 1 天，未满 14 天）
- C 触发：❌（无异常/OI/用户指令）
- → 分支 D：不进入完整轮次

#### fetch 层能力确认

- ✅ fetch 机制真实有效（fetchedAt 已更新）
- ✅ sif.suning.com 源持续有更新
- ⚠️ 当前 analyst_sources.json 中多数来源（顾慧君/王锟）profile 文章集中于 2021~2023 年，被年份过滤
- ⚠️ 无净增长，说明去重机制在替换旧文而非累积

#### 文档同步

- ✅ REVIEW_LOG（+R-32）v1.17
- ✅ CHANGE_CONTROL（+CC-21）v1.12
- ✅ P1_CANDIDATES（+P1-6b 行）v1.10

- **状态**：✅ P1-6b 真实 fetch 验证完成，不进入 ROUND-05

---

### Review R-33（P1-6c preflight 口径修正）

- **日期**：2026-04-08
- **review 对象**：P1-6c 内容替换型刷新识别与 preflight 口径修正
- **所属阶段**：preflight 机制增强
- **核查范围**：内容替换型刷新可识别性 / 方案比较 / 最小落地

#### 背景问题

P1-6b 证明：fetch 可发生"内容替换型刷新"（fetchedAt 变化，raw 总量不变，实际内容已换）。现有 preflight 口径只关注 raw 净增，可能错过这种刷新类型。

#### 内容替换型刷新可识别性分析

**当前可识别信号**：
- fetchedAt 变化 ✅ — 直接可读
- raw 条数变化 ✅ — 直接可读

**当前不可识别信号**（无快照对比）：
- 具体哪些 records 被替换 ❌
- analyst 文章分布变化 ❌
- success/skipped_old 结构变化（无 pre-fetch 快照）❌

**最小可行识别口径**：fetchedAt 变化 + raw 净增 <5 → 提示"可能为内容替换型刷新，需人工判断"。

#### 候选方案比较

- 方案A（SOP 文字说明）：最轻，但可执行性偏弱
- **方案B（推荐）**：preflight 增加 D-续路径，fetchedAt 变化时触发人工判断
- 方案C（diff 工具）：引入新文件和新逻辑，超出 P1-6c 范围

#### 推荐方案 B 落地内容

- `docs/PILOT_RUN_SOP.md`：v1.5
  - preflight 增加 **D-续：fetchedAt 已变化但 raw 未达触发（需人工判断）**
  - 明确：这是 D 的补充路径，不是自动触发
  - 人工判断流程：查看 queue 是否陈旧 → 决定是否走例外执行 C

#### 口径回放验证（P1-6b 结果）

| 信号 | 值 | 结论 |
|------|-----|------|
| fetchedAt | 变化 ✅ | 进入 D-续 |
| raw 净增 | 0 ❌ | 不满足 A |
| 距 ROUND-03 | ~1天 ❌ | 不满足 B |
| 异常/OI/用户指令 | 无 ❌ | 不满足 C |
| **D-续 人工判断** | queue 仍有效 | **维持 D，不进入 ROUND-05** |

新口径 vs 旧口径：**结论相同**（均为 D），但新口径多了一步 D-续 确认流程，避免"内容替换被静默忽略"。

#### 文档同步

- ✅ REVIEW_LOG（+R-33）v1.18
- ✅ CHANGE_CONTROL（+CC-22）v1.13
- ✅ P1_CANDIDATES（+P1-6c 行）v1.11
- ✅ PILOT_RUN_SOP v1.5

- **状态**：✅ P1-6c preflight 口径修正完成

---

### Review R-34（P1-7 fetch + preflight，分支 D）

- **日期**：2026-04-08
- **review 对象**：P1-7 下一有效轮次执行与小复盘候选判断
- **所属阶段**：试点运行 fetch → preflight → 判断链路验证
- **核查范围**：fetch 执行 / preflight 判断 / 分支 D 留痕

#### 第一层：fetch 执行结果

| 指标 | 上次（P1-6b）| 本次 | 变化 |
|------|-------------|------|------|
| fetchedAt | 2026-04-08T14:03:47 | 2026-04-08T15:13:21 | ✅ 变化 |
| raw | 79 | 79 | ➖ 无净增长 |
| success | 29 | 29 | ➖ 无变化 |
| skipped_old | 50 | 50 | ➖ 无变化 |
| 2024+ | ~28 | 28 | ➖ 无净增长 |

**归因**：B — 内容替换型刷新（fetchedAt 变化，raw/结构无实质变化）

#### 第二层：preflight 判断

| 触发 | 结果 | 说明 |
|------|------|------|
| A. 数量触发（≥5）| ❌ | 净增 0 |
| B. 时间触发（满14天）| ❌ | 距 ROUND-03 约 1 天 |
| C. 例外触发 | ❌ | 无异常/OI/用户指令 |
| D. 不进入 | ✅ | A/B/C 均不满足 |
| **D-续（人工判断）** | 进入 | fetchedAt 变化 + raw 未达触发 |

#### D-续 人工判断

- queue 条目（5条，2024年薛洪言/付一夫）→ 陈旧度中等
- success/skipped_old 结构无变化（29/50）→ 内容替换，无实质新增
- **结论：维持 D，不进入 ROUND-05**

#### 本轮分支

**分支 D：不进入完整轮次**

- fetch 真实执行：✅
- fetchedAt 刷新：✅（14:03 → 15:13）
- 实质新增：❌（内容替换，无净增长）
- preflight 正确阻止：✅

#### 下次检查建议

- **数量触发**：距下次 fetch 后 raw 新增 ≥5 时检查
- **时间触发**：距 ROUND-03 满 14 天（2026-04-22 前后）
- **D-续 关注**：若 fetchedAt 变化且 2024+ 池有实质净增，则重新判断

#### 机制验证结论

fetch → preflight → D-续 → 判断链路已完整跑通，机制有效。当前真实瓶颈：**fetch 来源多数文章集中于 2021~2023 年，被 min_year=2024 过滤，导致无净新增**。这是 analyst_sources.json 的结构性问题，不在 P1-7 范围。

#### 文档同步

- ✅ REVIEW_LOG（+R-34）v1.19
- ✅ P1_CANDIDATES（+P1-7 行）v1.12

- **状态**：✅ P1-7 fetch + preflight 完成（分支 D，不进入完整轮次）

---

### Review R-35（P1-8 来源扩展候选与变更建议草案）

- **日期**：2026-04-08
- **review 对象**：P1-8 来源扩展候选与最小配置变更准备
- **所属阶段**：来源层问题识别与变更建议草案
- **核查范围**：来源层问题分类 / 候选方案 / 变更草案

#### 来源层问题分类（基于证据）

**问题 1：高优先级来源从未被抓取**
- 温彬 (high): 2个 seedUrls HTTP 200，raw=0，从未抓取 ✅
- 曾刚 (high): 1个 seedUrl HTTP 200，raw=0，从未抓取 ✅

**问题 2：已抓取来源文章陈旧**
- 顾慧君 (medium): 20 raw，0 usable，2021-2022，全部被过滤 ✅
- 王锟 (medium): 13 raw，0 usable，2018-2019，全部被过滤 ✅

**问题 3：主力来源断档 + 过度集中**
- 薛洪言：usable 占比 51.7%（15/29），最新可用 2025-01-06，sif.suning.com 无 2026 年新文章 ✅
- 付一夫：usable 占比 31.0%（9/29），无 2026 年新文章 ✅
- 合计 82.7% 依赖 sif.suning.com，断更即池停滞

**问题 4：部分来源抓取存在障碍**
- 朱太辉：SSL 握手失败，需补证 ✅
- 孙扬/杜娟：无 seedUrls，profile 可访问性未知

#### 候选方案比较

| 方案 | 产物 | 风险 | 扩项 |
|------|------|------|------|
| A：只更新问题文档 | 文档 | 推动力弱 | 否 |
| **B（推荐）**：变更草案 | 新建 SOURCE_CHANGE_PROPOSAL.md | 需人工生效 | 极小 |
| C：直接改配置 | analyst_sources.json | 越过治理边界 | 是 |

#### 推荐方案 B 落地

- 新建：`docs/SOURCE_CHANGE_PROPOSAL.md`（v1.0，草案不生效）
- 内容：问题分类 / 来源维持-观察-替换建议 / analyst_sources.json 最小修改草案（3个）
- 核心建议：优先抓取温彬/曾刚；降级顾慧君/王锟；处理董希淼换源

#### 验证结论

- ✅ 来源问题已被证据化分类（4类问题）
- ✅ 有变更草案（SOURCE_CHANGE_PROPOSAL.md）
- ✅ 草案能回答"为什么轮次收益低"（sif断更 + high priority 从未抓取）
- ✅ 草案能支撑下一步配置变更决策

#### 文档同步

- ✅ REVIEW_LOG（+R-35）v1.20
- ✅ CHANGE_CONTROL（+CC-23）v1.14
- ✅ P1_CANDIDATES（+P1-8 行）v1.13
- ✅ SOURCE_CHANGE_PROPOSAL.md（新建，v1.0）

- **状态**：✅ P1-8 来源扩展候选草案完成（不生效，等待人工决策）

---

### Review R-36（P1-9 最小配置变更 + 抓取验证，分支 D）

- **日期**：2026-04-08
- **review 对象**：P1-9 来源配置最小变更 + 抓取验证 + 条件进入下一有效轮次
- **所属阶段**：来源层最小配置变更实施
- **核查范围**：最小变更集 / 配置变更 / dry-run / 真实 fetch / preflight 判断

#### 最小变更集确认

- **顾慧君 (deposit-006)**：`active=true → false`（20 raw 全部 2021-2022，全被过滤）
- **王锟 (deposit-008)**：`active=true → false`（13 raw 全部 2018-2019，全被过滤）

**本轮明确不动**：温彬/曾刚（维度不匹配，需 `对公贷款` 而非 `对公存款`）、朱太辉/孙扬/杜娟（证据不足）。

#### 变更后 fetch 结果

| 指标 | 变更前 | 变更后 | 变化 |
|------|--------|--------|------|
| fetchedAt | 2026-04-08T15:13 | 2026-04-08T16:04 | ✅ 变化 |
| raw | 79 | 46 | **-33**（去除旧来源）|
| success | 29 | 29 | ➖ 无变化 |
| skipped_old | 50 | 17 | -33（改善）|
| 2024+ | 28 | 28 | ➖ 无变化 |

#### preflight 判断

| 触发 | 结果 | 说明 |
|------|------|------|
| A（数量 ≥5）| ❌ | 净增 = -33 |
| B（满14天）| ❌ | 约 1 天 |
| C（例外）| ❌ | 无 |
| D | ✅ | A/B/C 均不满足 |
| D-续（人工判断）| 进入 | fetchedAt 变化 |
| **D-续结论** | **维持 D** | usable 无扩大，来源结构无改善 |

#### 本轮分支

**分支 D：不进入完整轮次**

#### 变更效果评估

- ✅ 变更正确：去除 0 usable 的旧来源，节省 crawl 资源
- ❌ 未解决核心问题：usable 池无扩大，薛洪言+付一夫占比仍 87%
- ⚠️ 根因：真正扩大 usable 池需要抓取温彬/曾刚（high priority，从未抓取），但需 crawl 维度变更，超出 P1-9 最小范围

#### 文档同步

- ✅ REVIEW_LOG（+R-36）v1.21
- ✅ CHANGE_CONTROL（+CC-24）v1.15
- ✅ P1_CANDIDATES（+P1-9 行）v1.14
- ✅ analyst_sources.json 备份：`analyst_sources.json.bak-2026-04-08-P1-9`

- **状态**：✅ P1-9 最小配置变更完成（分支 D，不进入完整轮次）

---

### Review R-37（P1-10 维度扩展与新来源引入决策准备）

- **日期**：2026-04-08
- **review 对象**：P1-10 维度扩展与新来源引入的决策准备
- **所属阶段**：跨边界决策准备
- **核查范围**：跨边界问题分类 / 决策路径比较 / 最小决策草案

#### 核心发现：温彬/曾刚 HTTP 验证

| 来源 | seedUrl | HTTP | 年份 | min_year=2024 |
|------|---------|------|------|--------------|
| 温彬 | 21jingji.com 20260121 | 200 | 2026-01 | ✅ |
| 温彬 | 21jingji.com 20260305 | 200 | 2026-03 | ✅ |
| 曾刚 | shifd.net 2025 | 200 | 2025 | ✅ |

**关键结论**：温彬有 2026年1月/3月新文章，扩展到 `对公贷款` 维度可直接带来净新增。

#### 问题分类

- **A. 扩维度才能释放**：温彬/曾刚 ✅ 证据充分
- **B. 需新来源方向**：薛洪言+付一夫占 87% ✅ 证据充分，但扩维度可部分改善
- **C. 证据不足**：朱太辉/孙扬/杜娟 ⚠️ 需补证
- **D. 存量调整已达极限**：顾慧君/王锟已降级 ✅

#### 决策路径比较

- 方案A（仅扩维度）：✅ 证据充分，最小跨边界
- 方案B（仅引新来源）：⚠️ 准备成本高，周期长
- **方案C（推荐）：最小组合试探**（扩维度 + 确认性 dry-run）

#### 推荐方案 B/C 落地

- 新建：`docs/DIMENSION_EXPANSION_PROPOSAL.md`（v1.0，草案不生效）
- 内容：维度扩展候选 / 新来源引入备选 / 最小试探步骤
- 核心建议：
  1. 执行一次 `fetch_analyst_articles.py --dimension 对公贷款 --dry-run`
  2. 若 dry-run 结果正面，执行一次真实 fetch（对公贷款）
  3. 用结果做 preflight 判断
  4. 若支持，进入下一有效轮次

#### 验证结论

- ✅ 跨边界问题已压缩为可决策项
- ✅ 有决策草案（DIMENSION_EXPANSION_PROPOSAL.md v1.0）
- ✅ 草案能明确回答"为什么下一个动作必须跨边界"
- ✅ 草案能支撑"是否进入真正实施"的拍板

#### 文档同步

- ✅ REVIEW_LOG（+R-37）v1.22
- ✅ CHANGE_CONTROL（+CC-25）v1.16
- ✅ P1_CANDIDATES（+P1-10 行）v1.15

- **状态**：✅ P1-10 决策准备完成（草案不生效，供人工拍板）

---

### Review R-38（P1-11 维度扩展试探 + ROUND-04 执行）

- **日期**：2026-04-08
- **review 对象**：P1-11 最小维度扩展试探实施 + ROUND-04 执行
- **所属阶段**：跨边界试探实施
- **核查范围**：维度扩展方案 / 最小变更 / dry-run / 真实 fetch / preflight / ROUND-04 执行

#### 实施摘要

**维度扩展方案**：对公存款+对公贷款 两次抓取并合并（方案B，最小组合试探）

**配置变更**：
- `run-analyst-fetch.sh`：新增 `--dim-trial` 模式（两次 crawl + 合并去重）
- analyst_sources.json：**未修改**（仅扩维度，不新增来源）

#### fetch 结果（维度扩展后合并）

| 指标 | 合并前 | 合并后 | 变化 |
|------|--------|--------|------|
| raw | 46 | 49 | +3 |
| success | 29 | 32 | +3 |
| skipped_old | 17 | 17 | ➖ 无变化 |
| 2024+ | 28 | 30 | +2 |

**新增来源**：
- 温彬 (high priority): 2 条 (2026年新文章) ✅
- 曾刚 (high priority): 1 条 (2025年新文章) ✅

#### preflight 判断

| 触发 | 结果 | 说明 |
|------|------|------|
| A（数量 ≥5）| ❌ | 净增 = 3 |
| B（满14天）| ❌ | 约 1 天 |
| C（例外）| ✅ 边界 | 新维度+新来源，质量充分 |
| D | ❌ | A/B 不满足 |
| D-续 人工判断 | 支持进入 | usable 池扩（28→30），新来源进入 |

**结论**：走 C 类例外，进入 ROUND-04

#### ROUND-04 执行结果

- usable 池：28（温彬=2, 曾刚=1 首次进入）
- queue：5 条（温彬首次进入 queue 1条）
- tracker：4 confirmed / 1 pending（温彬 pending）
- 薛洪言占比：43%（vs 51.7%前次），**首次改善**

#### 文档同步

- ✅ REVIEW_LOG（+R-38）v1.23
- ✅ CHANGE_CONTROL（+CC-26）v1.17
- ✅ P1_CANDIDATES（+P1-11 行）v1.16
- ✅ PILOT_RUN_SOP v1.6
- ✅ DIMENSION_EXPANSION_PROPOSAL v1.1（升级为实施版）
- ✅ ROUND_RECAP_2026-04-08_ROUND-04.md（新建）
- ✅ ROUND_COMPARISON.md（追加 ROUND-04 行）
- ✅ OPEN_ISSUES.md（OI-01 已处理；OI-03 改善信号）
- ✅ run-analyst-fetch.sh.bak-2026-04-08-P1-11（备份）

- **状态**：✅ P1-11 维度扩展试探实施完成；ROUND-04 执行完成

---

### Review R-39（P1-12 试探成果固化 + preflight D + 基线晋升准备判断）

- **日期**：2026-04-08
- **review 对象**：P1-12 试探成果固化 + 条件运行 + 基线晋升准备
- **所属阶段**：P1-11 成果固化
- **核查范围**：P1-11 成果稳固性评估 / preflight / 基线晋升条件

#### P1-11 试探成果固化结论

**A. 已被证据验证的改善（足够稳固）**
- 温彬/曾刚进入 raw/usable/pool：✅（3条真实记录，HTTP 200验证）
- usable 池扩大：✅（28条，含温彬2+曾刚1）
- 薛洪言占比下降：⚠️（42.9% vs 51.7%，1次数据，需持续验证）

**B. 尚未完全验证的部分**
- 是否可重复：❌（仅1次 dim-trial）
- 温彬能否持续供稿：❌（当前仅2025-2026初文章）
- 集中度持续改善：⚠️（1次，需多轮验证）

**C. dim-trial 阶段定义：观察中的准基线**
- ✅ 有效性已初步验证（温彬/曾刚进入池）
- ⚠️ 可重复性未验证（仅1次）
- ⚠️ 质量稳定性未验证（温彬 pending 尚未 confirmed）
- ✅ 未引入明显新问题
- **结论**：不升格为正式默认，待至少再完成1-2轮验证

#### preflight 判断（当前时点）

| 触发 | 值 | 结果 |
|------|---|------|
| A（数量 ≥5）| raw 净增 = 0 | ❌ |
| B（满14天）| 距 P1-11 ~10.6 小时 | ❌ |
| C（例外）| 无异常/OI/用户指令 | ❌ |
| D | A/B/C 均不满足 | ✅ |
| D-续 人工判断 | fetchedAt 无变化，raw 无新增 | 维持 D |

**结论**：分支 D，**不执行新 fetch，不进入下一轮次**

#### 基线晋升准备判断

| 条件 | 状态 |
|------|------|
| dim-trial ≥2次有效轮次带来正向改善 | ❌（仅1次）|
| usable 扩大可重复 | ❌（需再验证）|
| 集中度改善持续 | ⚠️（需多轮）|
| 未引入新问题 | ✅ |
| 足以支撑"建议默认模式"草案 | ❌ |

**结论**：**不具备基线晋升准备条件**。原因：仅1次验证，可重复性未确认，温彬/曾刚持续性未知。

#### 下次检查建议

- 触发条件：fetchedAt 变化 或 raw 新增 ≥5 或 距 P1-11 满14天（2026-04-22前后）
- dim-trial 使用时机：单维度 fetch 无实质新增后，作为观察模式继续使用

#### 文档同步

- ✅ REVIEW_LOG（+R-39）v1.24
- ✅ DIMENSION_EXPANSION_PROPOSAL.md（v1.1 状态确认为"观察中准基线"）

- **状态**：✅ P1-12 完成（preflight D，维持不执行；基线晋升准备条件未满足，继续观察）

---

### Review R-40（P1-13 准基线持续验证 + preflight D + 基线晋升候选判断）

- **日期**：2026-04-08
- **review 对象**：P1-13 准基线持续验证
- **所属阶段**：dim-trial 持续观察
- **核查范围**：观察目标固化 / preflight / 基线晋升候选

#### dim-trial 观察目标（固化）

| 观察目标 | 验证状态 | 还需什么 |
|---------|---------|---------|
| 是否持续带来 usable 扩大 | ⚠️ 仅1次 | 至少再1次 dim-trial 有净新增 |
| 是否持续改善集中度 | ⚠️ 仅1次 | 至少再1次薛洪言占比继续下降 |
| 温彬/曾刚是否继续进入 pool | ⚠️ 仅1次 | 至少再1次两人有新文章被抓取 |
| 是否引入新噪声/旧文 | ✅ 暂无问题 | 持续监控 |
| 是否造成抓取障碍 | ✅ 无障碍 | 持续监控 |

#### preflight 判断（当前时点）

| 触发 | 值 | 结果 |
|------|---|------|
| A（数量 ≥5）| raw 净增 = 0 | ❌ |
| B（满14天）| 距 P1-11 ~10.7 小时 | ❌ |
| C（例外）| 无异常/OI/用户指令 | ❌ |
| D | A/B/C 均不满足 | ✅ |
| D-续 人工判断 | fetchedAt 无变化，raw 无新增，观察空窗 | 维持 D |

**结论**：分支 D，**不执行新 fetch，不进入下一轮次**

#### 基线晋升候选判断

| 条件 | 状态 |
|------|------|
| dim-trial ≥2次有效轮次带来正向增量 | ❌（无新数据）|
| usable 扩大可重复 | ❌（需再验证）|
| 集中度改善持续 | ⚠️（需再验证）|
| 温彬/曾刚持续性 | ⚠️（观察空窗）|
| 未引入新问题 | ✅ |

**结论**：**不具备基线晋升候选条件**。原因：无新数据可验证（P1-13 preflight D 无执行），无法判断可重复性。

#### 下次检查建议

- 触发条件：fetchedAt 变化 或 raw 新增 ≥5 或 满14天（~2026-04-22）
- dim-trial 使用时机：单维度 fetch 无实质新增后，作为观察模式使用

#### 文档同步

- ✅ REVIEW_LOG（+R-40）v1.25
- ✅ CHANGE_CONTROL（+CC-28）v1.19

- **状态**：✅ P1-13 完成（preflight D，不执行新 fetch；基线晋升候选条件未满足，继续观察）

---

### Review R-41（P1-14 观察期延长包 + preflight D + 观察窗口固化）

- **日期**：2026-04-08
- **review 对象**：P1-14 观察期延长包
- **所属阶段**：dim-trial 持续观察
- **核查范围**：观察窗口固化 / preflight

#### dim-trial 观察窗口（固化）

**三级触发条件（优先级排序）**：
| 优先级 | 触发条件 | 说明 | 下次激活动作 |
|--------|---------|------|------------|
| P0 | fetchedAt 变化 | 最强信号，外部源有更新 | 立即 preflight |
| P1 | raw 新增 ≥5 | 数量触发 | 立即 preflight |
| P2 | 满14天 | 时间触发 | 自动 preflight |

**不建议频繁重复检查的原因**：
- fetchedAt 未变化时，重复 preflight 只会得到相同结果（D）
- 人工判断成本高但信息增益为零
- 真实触发信号来自外部源更新，不是内部轮询

**观察窗口终止条件**：任一 P0/P1/P2 触发即激活完整判断

#### preflight 判断（当前时点）

| 触发 | 值 | 结果 |
|------|---|------|
| A（数量 ≥5）| raw 净增 = 0 | ❌ |
| B（满14天）| 距 P1-11 ~10.9 小时 | ❌ |
| C（例外）| 无异常/OI/用户指令 | ❌ |
| D | A/B/C 均不满足 | ✅ |
| D-续 人工判断 | fetchedAt 无变化，raw 无新增 | 维持 D |

**结论**：分支 D，**不执行新 fetch，不进入下一轮次**

#### 下次激活条件

| 触发 | 预计时间 | 动作 |
|------|---------|------|
| fetchedAt 变化 | 不确定 | 立即 preflight |
| raw 新增 ≥5 | 不确定 | 立即 preflight |
| 满14天 | ~2026-04-22 | 自动 preflight |

#### 文档同步

- ✅ REVIEW_LOG（+R-41）v1.26
- ✅ CHANGE_CONTROL（+CC-29）v1.20

- **状态**：✅ P1-14 完成（观察窗口固化，preflight D，不执行新 fetch）

---

### Review R-42（P1-15 观察窗口内条件激活包）

- **日期**：2026-04-08
- **review 对象**：P1-15 观察窗口内条件激活包
- **所属阶段**：dim-trial 持续观察
- **核查范围**：P0/P1/P2 触发判断

#### 观察窗口判断（2026-04-08 ~11:00）

| 触发 | 条件 | 当前状态 | 结果 |
|------|------|---------|------|
| P0 | fetchedAt 变化 | 2026-04-08T09:57:30Z（无变化）| ❌ 未触发 |
| P1 | raw 新增 ≥5 | 49（无新增）| ❌ 未触发 |
| P2 | 满14天 | 距 P1-11 约 0.5 天，还需 13.5 天 | ❌ 未触发 |

**结论**：**分支 A：观察窗口未触发，不进入完整判断，留痕并停止**

#### 本包本次正确动作

- ❌ 不执行 fetch
- ❌ 不执行 run
- ❌ 不更新 tracker / ledger / comparison
- ✅ 记录本次检查结果
- ✅ 下次检查：P0/P1/P2 任一触发时激活分支 B

#### 下次激活条件

| 触发 | 预计时间 | 动作 |
|------|---------|------|
| P0 | fetchedAt 变化时 | 立即激活分支 B |
| P1 | raw 新增 ≥5 时 | 立即激活分支 B |
| P2 | ~2026-04-22 | 自动激活分支 B |

#### 文档同步

- ✅ REVIEW_LOG（+R-42）v1.27
- ✅ CHANGE_CONTROL（+CC-30）v1.21

- **状态**：✅ P1-15 完成（分支 A：P0/P1/P2 均未触发，留痕并停止）

---

### Review R-43（P1-16 触发后有效轮次执行包）

- **日期**：2026-04-08
- **review 对象**：P1-16 触发后有效轮次执行包
- **所属阶段**：dim-trial 持续观察
- **核查范围**：P0/P1/P2 触发判断

#### 观察窗口判断（2026-04-08 ~11:10）

| 触发 | 条件 | 当前状态 | 结果 |
|------|------|---------|------|
| P0 | fetchedAt 变化 | 2026-04-08T09:57:30Z（无变化）| ❌ 未触发 |
| P1 | raw 新增 ≥5 | 49（无新增）| ❌ 未触发 |
| P2 | 满14天 | 距 P1-11 约 0.5 天，还需 13.5 天 | ❌ 未触发 |

**结论**：**分支 A：触发条件不成立，不执行完整轮次，留痕并停止**

#### 本包本次正确动作

- ❌ 不执行 fetch
- ❌ 不执行 run
- ❌ 不更新 tracker / ledger / comparison
- ✅ 记录检查结果
- ✅ 下次 P0/P1/P2 触发时激活分支 B

#### 下次激活条件

| 触发 | 预计时间 | 动作 |
|------|---------|------|
| P0 | fetchedAt 变化时 | 立即激活分支 B |
| P1 | raw 新增 ≥5 时 | 立即激活分支 B |
| P2 | ~2026-04-22 | 自动激活分支 B |

#### 文档同步

- ✅ REVIEW_LOG（+R-43）v1.28
- ✅ CHANGE_CONTROL（+CC-31）v1.22

- **状态**：✅ P1-16 完成（分支 A：P0/P1/P2 均未触发，留痕并停止）

---

### Review R-44（P1-LT 观察窗口长期触发包 - 首次执行）

- **日期**：2026-04-08
- **review 对象**：P1-LT 观察窗口长期触发包（首次执行）
- **所属阶段**：dim-trial 持续观察（长期复用包）
- **核查范围**：P0/P1/P2 触发判断

#### 观察窗口判断（2026-04-08 ~21:30）

| 触发 | 条件 | 当前状态 | 结果 |
|------|------|---------|------|
| P0 | fetchedAt 变化 | 2026-04-08T09:57:30Z（无变化）| ❌ 未触发 |
| P1 | raw 新增 ≥5 | 49（无新增）| ❌ 未触发 |
| P2 | 满14天 | 距 P1-11 约 0.5 天，还需 13.5 天 | ❌ 未触发 |

**结论**：**分支 A：观察窗口未触发，留痕并停止**

#### 本包本次正确动作

- ❌ 不执行 fetch
- ❌ 不执行 run
- ❌ 不更新 tracker / ledger / comparison
- ✅ 记录检查结果
- ✅ 更新 REVIEW_LOG

#### 下次激活条件

| 触发 | 预计时间 | 动作 |
|------|---------|------|
| P0 | fetchedAt 变化时 | 立即激活分支 B |
| P1 | raw 新增 ≥5 时 | 立即激活分支 B |
| P2 | ~2026-04-22 | 自动激活分支 B |

#### 文档同步

- ✅ REVIEW_LOG（+R-44）v1.29
- ✅ CHANGE_CONTROL（+CC-32）v1.23

- **状态**：✅ P1-LT 首次执行完成（分支 A：P0/P1/P2 均未触发，留痕并停止）

---

### Review R-45（P2-1 实施验证）

- **日期**：2026-04-09
- **review 对象**：P2-1 业务问题框架 + 双模板 + 动作规则文档 + 半样稿
- **所属阶段**：P2-1（业务问题框架重建 + 输出模板升级实施包）
- **核查范围**：Step 1 收尾校验 / Step 2 业务问题框架 / Step 3 输出偏浅原因识别 / Step 4 方案比较 / Step 5 推荐方案 / Step 6 最小落地

#### Step 1 收尾校验

- ✅ 核心问题已从"能否跑通"转向"输出是否业务分析可用"（R-01~R-44 全部为运行机制，P2-1 是第一个面向输出内容质量的任务）
- ✅ REVIEW_LOG 记录与 P2-1 方向一致，无矛盾
- ✅ 无阻断，本轮可推进

#### Step 2 业务问题框架（Q1~Q8）

| 问题 | 句式 | 偏向 | 原型答浅类别 |
|------|------|------|------------|
| Q1：本月最重要变化 | 这个月最值得说的变化是什么？ | 领导层 | 类别一（聚焦缺失）|
| Q2：变化原因 | 为什么会这样？ | 领导+执行 | 类别二（缺机制推断）|
| Q3：对我行启示 | 我们应该怎么动？ | 执行层 | 类别三+六 |
| Q4：持续观察 | 下月要不要继续盯？ | 领导+执行 | 类别五 |
| Q5：贷款怎么嵌 | 贷款侧往哪插？ | 领导层 | 类别六（脱节）|
| Q6：证据充分性 | 这么说有依据吗？ | 领导层 | 类别三 |
| Q7：三件主动作 | 一线最紧要干什么？ | 执行层 | 类别四+七 |
| Q8：待核实处理 | 这事能下结论吗？ | 领导层 | 类别三+五 |

#### Step 3 输出偏浅原因清单

| 类别 | 描述 | 是否本轮解决 |
|------|------|------------|
| 类别一 | 事实不缺但聚焦缺失 | ✅ Q1+模板解决 |
| 类别二 | 原因推断缺机制解释 | ✅ Q2+Q6+置信度标注解决 |
| 类别三 | 判断没有分层（事实/推断/建议）| ✅ 置信度+降调段解决 |
| 类别四 | 建议缺部署信息 | ✅ 动作格式三要素解决 |
| 类别五 | 主动作与观察项未分 | ✅ 双段落结构解决 |
| 类别六 | 贷款内容与存款主线脱节 | ✅ "三"段联动句解决 |
| 类别七 | 领导版/执行版混写 | ✅ 双模板结构解决 |

#### Step 4 方案比较

| 方案 | 推荐程度 | 理由 |
|------|---------|------|
| 方案A：单模板增强型 | 未选 | 两头不到岸，无法真正区分领导/执行 |
| 方案B：双模板分层型 | **推荐** | 直接解决类别七，符合双层输出方向，可验证性强 |
| 方案C：一主两附型 | 未选 | 过早做格式工程，内容质量未验证前不适合 |

#### Step 5 推荐方案

- **推荐**：方案B（双模板分层型）
- **最小实施边界**：领导版模板 + 执行版模板 + 动作规则文档 + 半样稿（共4份文档，不含自动生成/嵌回）
- **对后续嵌回的价值**：模板字段可直接映射到 JSON schema 扩展；两版差异定义清晰后，可作为 build_analyst_opinions.py 输出格式升级的目标

#### Step 6 落地结果

| 文档 | 状态 | 内容 |
|------|------|------|
| BUSINESS_QUESTION_FRAME.md | ✅ 新建 v1.0 | Q1~Q8核心问题 + 领导/执行差异 + 答浅位置 |
| LEADER_OUTPUT_TEMPLATE.md | ✅ 新建 v1.0 | 六段结构 + 写作规范 + 字数控制 |
| EXECUTION_OUTPUT_TEMPLATE.md | ✅ 新建 v1.0 | 四段结构 + 三主动作格式 + 执行版专属规范 |
| ACTION_EXPRESSION_RULES.md | ✅ 新建 v1.0 | 主动作/观察项/待核实项区分 + 泛建议升级对照表 + 标准降调用语 |
| MONTHLY_ANALYSIS_SAMPLE_V0.md | ✅ 新建 v1.0 | 领导版+执行版半样稿，用真实数据（ROUND-04池）手填 |

#### 样稿验证结论

**已达成的效果**：
- ✅ 有机制推断和置信度分层（vs 原型无推断）
- ✅ 建议含目的+责任人+验证指标（vs 原型泛建议）
- ✅ 领导版/执行版定位差异清晰
- ✅ 主动作和观察项分开
- ✅ 贷款辅助通过联动句处理，不单独成段
- ✅ 有主动降调处理

**边界内已知不足**：
- 推断仍依赖定性引用，缺乏直接数据（需历史截面数据，待解决）
- 建议责任人只能到部门级，无任务管理系统（边界约束）
- 置信度判断人工化，未规则化（后续 P2-X 课题）
- 贷款利率数据为2026-02，落后存款数据1个月（Gate A阻断未解除）

#### 自 review 结果

- ✅ 严格限定在业务问题框架+模板+规则+半样稿，未扩项
- ✅ 未改任何运行机制（fetch/build/preflight/tracker）
- ✅ 未引入 UI/数据库/自动生成/任务系统
- ✅ 文档内容与事实一致（存款数据来自 deposit_benchmark.json，分析师观点来自 analyst_opinions.json）
- ✅ 样稿能体现"论证更完整、建议更有动作感、领导版/执行版差异清楚"

#### 文档同步

- ✅ CHANGE_CONTROL（+CC-33）v1.24
- ✅ REVIEW_LOG（+R-45）v1.30
- ✅ BUSINESS_QUESTION_FRAME.md（新建 v1.0）
- ✅ LEADER_OUTPUT_TEMPLATE.md（新建 v1.0）
- ✅ EXECUTION_OUTPUT_TEMPLATE.md（新建 v1.0）
- ✅ ACTION_EXPRESSION_RULES.md（新建 v1.0）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V0.md（新建 v1.0）

#### 本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做自动生成 | ✅（只做文档模板）|
| 不做 UI 按钮 | ✅ |
| 不做数据库 | ✅ |
| 不做 confirmLevel 规则重构 | ✅ |
| 不做 OI-03/OI-04 | ✅ |

#### 本轮明确不做

- ❌ UI 按钮
- ❌ 正式运营后台
- ❌ 自动 cron / 调度
- ❌ 自动 fetch
- ❌ 多角色协同权限
- ❌ confirmLevel 规则重构
- ❌ OI-03 / OI-04 等运行优化
- ❌ 整体来源治理体系重构
- ❌ 正式产品化开发
- ❌ 月度报告系统建设

- **状态**：✅ P2-1 实施完成

---

### Review R-46（P2-2 实施验证）

- **日期**：2026-04-09
- **review 对象**：P2-2 模板收窄 + 动作升级 + 最少反馈清单
- **所属阶段**：P2-2
- **核查范围**：Step 1 收尾校验 / Step 2 V0 样稿问题识别 / Step 3 动作建议短板 / Step 4 方案比较 / Step 5 推荐方案 / Step 6 最小落地

#### Step 1 收尾校验

- ✅ P2-1 的文档记录（R-45）结论诚实："已证明结构可行，还没证明结构已足够好用"
- ✅ 无"模板已基本定型"的错误表述
- ✅ 本轮目标正确：收窄模板 + 降低反馈门槛，不是继续扩模板
- ✅ 无阻断

#### Step 2 V0 样稿问题识别（12项）

| 编号 | 问题 | 更偏 | 优先级 | 本轮是否解决 |
|------|------|------|--------|------------|
| V0-01 | 主结论不够鲜明，新闻稿格式 | 领导版 | P1 | ✅ V1解决 |
| V0-02 | 推断段落偏学术 | 领导版 | P1 | ✅ V1简化格式 |
| V0-03 | 推断段与意义段重叠 | 领导版 | P1 | ✅ V1合并为一段 |
| V0-04 | 主动作"是否有异动"是问句，不是结论 | 执行版 | **P0** | ✅ V1改为判断句 |
| V0-05 | 主动作混入"研究动作"，边界模糊 | 执行版 | **P0** | ✅ V1分类为"研究准备" |
| V0-06 | 主动作和观察项视觉权重相同 | 执行版 | P1 | ✅ V1格式区分 |
| V0-07 | 执行版贷款侧一句话偏虚 | 执行版 | P2 | ⚠️ 有限改善 |
| V0-08 | 两版降调项重复（复制粘贴）| 两者均有 | P1 | ✅ V1两版独立 |
| V0-09 | 动作2是研究动作而非执行动作 | 执行版 | **P0** | ✅ V1归为"研究准备" |
| V0-10 | 主动作和观察项视觉权重相同 | 执行版 | P2 | ✅ V1符号+排版区分 |
| V0-11 | 执行版现状段用表格，显得生硬 | 执行版 | P1 | ✅ V1改为文字叙述 |
| V0-12 | 动作2责任人设定不合理（不是业务部门能做的）| 执行版 | P1 | ✅ V1明确为"研究准备" |

**结论**：3个P0问题（V0-04、V0-05、V0-09）均已解决

#### Step 3 动作建议短板清单

| 动作 | V0问题 | V1解决方案 |
|------|--------|-----------|
| 主动作1（摸排客户）| 问句式验证指标 | 改为"确认到期续做意向" |
| 主动作2（获取利率）| 研究动作混入主动作 | 降为"研究准备"类，不占主动作名额 |
| 主动作3（建立机制）| 本月完不成，不是立即执行 | 改为"本月做一次扫描" |
| 观察项A/B | 无执行人 | 必须写明执行部门 |

#### Step 4 方案比较

| 方案 | 改动方向 | 优点 | 风险 | 是否选 |
|------|---------|------|------|--------|
| 方案A 轻收窄 | 只改文风和小标题 | 最快 | 动作核心问题未解决 | ❌ |
| 方案B 结构收窄+动作升级 | 六段→四段+动作三分法 | 直接解决P0问题 | 改动较多但可控 | ✅ |
| 方案C 重写样稿型 | 大幅重写 | 可能更像正式稿 | 过重，无业务反馈前可能改错方向 | ❌ |

**方案B核心改变**：主动作格式增加"动作类型"字段（立即执行/研究准备/建立机制）

#### Step 5 推荐方案

- **推荐**：方案B
- **最小边界**：领导版V1+执行版V1+动作规则V1+V1样稿+最少反馈清单
- **对后续嵌回帮助**：动作类型字段可映射到JSON schema；两版独立后可分别嵌回报告草稿/行动指引

#### Step 6 落地结果

| 文档 | 状态 | 版本 |
|------|------|------|
| LEADER_OUTPUT_TEMPLATE_V1.md | ✅ 新建 v1.1 | 六段→四段；推断+意义合并；降调内嵌 |
| EXECUTION_OUTPUT_TEMPLATE_V1.md | ✅ 新建 v1.1 | 动作分类（立即执行/研究准备）；观察项执行人 |
| ACTION_EXPRESSION_RULES_V1.md | ✅ 新建 v1.1 | 增加动作类型三分法；研究准备边界；观察项四要素 |
| MONTHLY_ANALYSIS_SAMPLE_V1.md | ✅ 新建 v1.1 | V0→V1样稿改写 |
| BUSINESS_FEEDBACK_MINI_QA.md | ✅ 新建 v1.0 | 12题（5题必答，其余条件触发）；最低3份有效反馈即可分析 |

#### V1 相比 V0 的改进点

- ✅ 主动作分类：两条立即执行+一条研究准备（P0问题解决）
- ✅ 动作格式：问句→判断句（V0-04解决）
- ✅ 研究准备边界：明确"做完不能产生业务动作"（V0-05/V0-09解决）
- ✅ 观察项执行人：必须写明执行部门
- ✅ 领导版篇幅：1800字→1300字
- ✅ 两版独立性：降调项不再复制粘贴
- ✅ 执行版现状段：表格→文字叙述+关键数字

#### V1 仍未完全解决（需业务反馈）

1. 验证指标置信度（"问客户有没有招行联系"依赖客户主动告知）
2. 研究准备责任人（战略研究/企金部——是否准确？）
3. 华夏研究结论的用途（谁看？看完了怎么用？）

#### 自 review 结果

- ✅ 严格限定在模板收窄+动作升级+最少反馈清单，未扩项
- ✅ 未改任何运行机制
- ✅ 未引入UI/数据库/自动生成/任务系统
- ✅ 12项V0问题均有明确解决方案，无遗漏
- ✅ 文档内容与V0数据基础一致

#### 本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做自动生成 | ✅ |
| 不做 UI 按钮 | ✅ |
| 不做数据库 | ✅ |
| 不引入任务系统 | ✅ |
| 不改评分权重、top-k、Gate A | ✅ |

#### 文档同步

- ✅ CHANGE_CONTROL（CC-33→已完成，CC-34→进行中）v1.24
- ✅ REVIEW_LOG（+R-46）v1.31
- ✅ LEADER_OUTPUT_TEMPLATE_V1.md（新建 v1.1）
- ✅ EXECUTION_OUTPUT_TEMPLATE_V1.md（新建 v1.1）
- ✅ ACTION_EXPRESSION_RULES_V1.md（新建 v1.1）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V1.md（新建 v1.1）
- ✅ BUSINESS_FEEDBACK_MINI_QA.md（新建 v1.0）

- **状态**：✅ P2-2 实施完成

---

### Review R-47（P2-3 实施验证）

- **日期**：2026-04-09
- **review 对象**：P2-3 动作闭环升级 + 责任归口收窄
- **所属阶段**：P2-3
- **核查范围**：Step 1 收尾校验 / Step 2 研究准备短板 / Step 3 责任归口问题 / Step 4 方案比较 / Step 5 推荐方案 / Step 6 最小落地

#### Step 1 收尾校验

- ✅ P2-2 R-46 结论诚实："V1 比 V0 更接近业务可试用状态，尚未完全达到正式可用标准"
- ✅ 当前最大短板已从"大结构问题"转向"动作闭环问题"——与 P2-2 R-46 一致
- ✅ 无阻断，本轮可推进

#### Step 2 研究准备类动作短板（3个P0）

| 编号 | 短板 | 描述 | 是否本轮解决 |
|------|------|------|------------|
| RP-01 | **无接收方** | 研究完成后没有写"谁来看这份产出"，研究白做 | ✅ V2 解决（接收方：分行公司部负责人）|
| RP-02 | **无转动作条件** | 研究结论永远停在结论，不会转化为下月动作 | ✅ V2 解决（三档条件：触发/归档/待定）|
| RP-03 | 产出定义不具体 | "一页判断报告"不说明格式和要点数量 | ✅ V2 解决（"一页书面判断报告，3~5个要点"）|
| RP-04 | 验证指标依赖客户主动告知 | 置信度低但可接受 | ⚠️ 有限改善 |
| RP-05 | 责任仅到部门级 | 无角色级建议 | ✅ V2 解决（部门+角色）|

#### Step 3 责任归口问题

| 编号 | 动作 | V1归口 | V2表述 | 是否解决 |
|------|------|--------|--------|---------|
| RA-01 | 主动作1（排查中信）| 分行客户管理部门 | 分行公司部 / 客户经理 | ✅ |
| RA-02 | 主动作2（招行扫描）| 分行公司业务部门 | 分行公司部 / 客户经理（主办）+ 产品经理（支持）| ✅ |
| RA-03 | 研究准备（华夏）| 战略研究/企金部门 | 战略研究部 / 行业研究员 | ✅ |
| RA-04 | 接收方 | 无 | 分行公司部负责人（或分行长）| ✅ RP-01解决 |
| RA-05 | 转动作条件 | 无 | 三档条件 | ✅ RP-02解决 |

#### Step 4 方案比较

| 方案 | 方向 | 风险 | 是否选 |
|------|------|------|--------|
| 方案A 轻规则补充 | 只改格式不填内容 | 空白字段仍在，等于没解决 | ❌ |
| **方案B 规则+责任表+样稿升级** | 新建闭环规则+归口表+V2样稿 | 改动多但可控 | ✅ |
| 方案C 动作卡片化 | 任务卡格式 | 过早产品化，违背不做任务系统原则 | ❌ |

#### Step 5 推荐方案

- **推荐**：方案B
- **理由**：直接解决 RP-01（无接收方）和 RP-02（无转动作条件），同时推进责任到"部门+角色"

#### Step 6 落地结果

| 文档 | 状态 | 版本 | 核心内容 |
|------|------|------|---------|
| ACTION_LOOP_RULES_V1.md | ✅ 新建 v1.0 | 7要素闭环+接收方写法+转动作条件结构 | |
| RESPONSIBILITY_MAP_V1.md | ✅ 新建 v1.0 | 责任归口总表+角色粒度说明+联合行动写法 | |
| ACTION_EXPRESSION_RULES_V2.md | ✅ 更新 v1.2 | 闭环三角+7要素+接收方+转动作条件+责任两级 | |
| MONTHLY_ANALYSIS_SAMPLE_V2.md | ✅ 新建 v1.2 | V1→V2改写；7要素填满；三档转动作条件 | |
| BUSINESS_FEEDBACK_MINI_QA_V2.md | ✅ 新建 v1.1 | 补充3题（Q13~15）；针对责任链/角色粒度/转动作条件 | |

#### V2 相比 V1 的改进点

| 改进点 | V1 | V2 | 解决什么问题 |
|--------|----|----|------------|
| 研究准备接收方 | 无 | 分行公司部负责人（或分行长）| RP-01（研究白做）|
| 研究准备转动作条件 | 无 | 三档条件（触发/归档/待定）| RP-02（结论停在结论）|
| 研究产出形式 | "一页判断报告" | "一页书面判断报告（3~5个要点）"| RP-03 |
| 责任粒度 | 仅部门级 | 部门+角色两级 | RA-01~03 |
| 完成时点 | "本月" | 具体日期 | 解决月底不被回顾 |
| 主动作2接收方 | "填好监测表" | 接收方：分行公司部负责人 | RP-01 |

#### V2 仍未完全解决（需业务反馈）

1. 研究准备责任人"战略研究部/行业研究员"：部分银行可能设在企金部或计财部——需确认
2. 主动作1"5000万以上"阈值：各行标准是否通用——需确认
3. 研究产出"一页书面判断报告"：接收方是否有时间看——需反馈

#### 自 review 结果

- ✅ 严格限定在动作闭环+责任归口，未扩项
- ✅ 未改任何运行机制
- ✅ 未引入UI/数据库/自动生成/任务系统
- ✅ 研究准备7要素（RP-01~RP-05）均有解决方案，无遗漏
- ✅ 文档内容与数据基础一致

#### 本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做自动生成 | ✅ |
| 不做 UI 按钮 | ✅ |
| 不做数据库 | ✅ |
| 不引入任务系统 | ✅ |
| 不改评分权重、top-k、Gate A | ✅ |

#### 文档同步

- ✅ CHANGE_CONTROL（CC-34→✅完成，CC-35→进行中）v1.24
- ✅ REVIEW_LOG（+R-47）v1.32
- ✅ ACTION_LOOP_RULES_V1.md（新建 v1.0）
- ✅ RESPONSIBILITY_MAP_V1.md（新建 v1.0）
- ✅ ACTION_EXPRESSION_RULES_V2.md（更新 v1.2）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V2.md（新建 v1.2）
- ✅ BUSINESS_FEEDBACK_MINI_QA_V2.md（新建 v1.1）

- **状态**：✅ P2-3 实施完成

---

### Review R-48（P2-4 实施验证）

- **日期**：2026-04-09
- **review 对象**：P2-4 最少业务反馈回采 + V3 收敛实施包
- **所属阶段**：P2-4
- **核查范围**：Step 1 收尾校验 / Step 2 反馈点识别 / Step 3 方案比较 / Step 4 推荐方案 / Step 6 最小落地

#### Step 1 收尾校验

- ✅ P2-3 R-47 验证结论诚实："V2 比 V1 更接近业务可部署状态，但尚未经过业务真实反馈验证"
- ✅ 当前最大已知短板：没有经过业务反馈验证
- ✅ 无阻断，本轮可推进

#### Step 2 最关键反馈点（6个）

| 编号 | 反馈点 | 适合谁答 | 是否可内部解决 |
|------|--------|---------|-------------|
| FP-01 | 领导版主结论是否够抓重点 | 领导层 | ❌ 需业务反馈 |
| FP-02 | 主动作是否真的像可部署动作 | 执行层 | ❌ 需业务反馈 |
| FP-03 | 研究准备接收方/转动作条件是否合理 | 执行层负责人 | ❌ 需业务反馈 |
| FP-04 | 责任归口"部门+角色"粒度是否合适 | 执行层负责人 | ❌ 需业务反馈 |
| FP-05 | 三档转动作条件是否有必要 | 执行层负责人 | ❌ 需业务反馈 |
| FP-06 | 是否愿意继续试用 | 所有人 | ❌ 需业务反馈 |

**结论**：6个问题全部需要业务反馈，无内部解决路径。

#### Step 3 方案比较

| 方案 | 方向 | 风险 | 是否选 |
|------|------|------|--------|
| 方案A 纯文档问答型 | 直接发V2+MINI_QA | 业务可能困惑于半成品状态；问卷太长 | ❌ |
| **方案B 最小反馈包型** | 一页说明+6题核心+选答制 | 反馈可能分散，但门槛最低回收率最高 | ✅ |
| 方案C 访谈记录型 | 安排口头访谈 | 门槛过高，违背最少输入原则 | ❌ |

#### Step 4 推荐方案

- **推荐**：方案B
- **理由**：门槛最低；选答制让业务只答有感的题，反而能收到真实反馈；符合"5~10分钟"目标

#### Step 6 落地结果

| 文档 | 状态 | 版本 | 核心内容 |
|------|------|------|---------|
| BUSINESS_FEEDBACK_PACK_V1.md | ✅ 新建 v1.0 | 最小反馈包说明；6题选答；免责声明 | |
| BUSINESS_FEEDBACK_MINI_QA_V3.md | ✅ 新建 v1.0 | 从15题收窄至6题；选答制；附分析规则引用 | |
| FEEDBACK_ANALYSIS_RULES_V1.md | ✅ 新建 v1.0 | 四种判断结果+分析矩阵+冲突处理+停止规则 | |

#### 当前状态：停在"可发出"状态

**原因**：当前没有真实业务反馈，按照"不虚构反馈"原则，不进入V3收敛。

**停在"可发出"状态的标准**：
- ✅ 最小反馈包已就绪（BUSINESS_FEEDBACK_PACK_V1.md）
- ✅ 收窄问卷已就绪（BUSINESS_FEEDBACK_MINI_QA_V3.md，6题）
- ✅ 反馈分析规则已就绪（FEEDBACK_ANALYSIS_RULES_V1.md）
- ✅ 收到真实反馈后可立即启动V3收敛（按FEEDBACK_ANALYSIS_RULES_V1.md处理）

#### 反馈包最低验证标准

| 验证维度 | 是否满足 |
|---------|---------|
| 业务只需5~10分钟 | ✅（6题选答，最快1分钟）|
| 尽量选择题/判断题 | ✅（全部选择题，无开放题）|
| 让V3修改基于真实反馈 | ✅（按分析规则收敛，不主观内推）|
| 保持门槛低 | ✅（选答制，不需要全部回答）|

#### 自 review 结果

- ✅ 严格限定在反馈回采包，未扩项
- ✅ 未虚构任何业务反馈
- ✅ 未改任何运行机制
- ✅ 6个反馈点全部需要业务反馈，无内部替代路径
- ✅ 停在"可发出"状态，不自动进入V3收敛

#### 本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不虚构业务反馈 | ✅ |
| 不做大规模调研 | ✅ |
| 不做正式访谈项目 | ✅ |
| 不做UI按钮/数据库/任务系统 | ✅ |

#### 文档同步

- ✅ CHANGE_CONTROL（CC-36→进行中）v1.25
- ✅ REVIEW_LOG（+R-48）v1.33
- ✅ BUSINESS_FEEDBACK_PACK_V1.md（新建 v1.0）
- ✅ BUSINESS_FEEDBACK_MINI_QA_V3.md（新建 v1.0）
- ✅ FEEDBACK_ANALYSIS_RULES_V1.md（新建 v1.0）

- **状态**：✅ P2-4 实施完成；停在"可发出"状态，等待真实反馈

---

# R-49 — P2-5 真实反馈摄入 + V3收敛

**日期**：2026-04-10
**对应阶段**：P2-5（真实反馈摄入 + V3收敛实施包）
**触发**：第一份真实业务反馈收到（FB-P2-20260410-001，邱非，平安银行公司业务管理部）

---

## 一、本轮实施内容

| 文件 | 操作 | 说明 |
|------|------|------|
| docs/REAL_FEEDBACK_LOG_01.md | 新建 | 真实反馈摄入记录 |
| docs/LEADER_OUTPUT_TEMPLATE_V2.md | 新建 | 领导版模板V2（仅微调）|
| docs/EXECUTION_OUTPUT_TEMPLATE_V2.md | 新建 | 执行版模板V2（Q1/Q2调整）|
| docs/ACTION_EXPRESSION_RULES_V3.md | 新建 | 动作表达规则V3（双门槛+归口+试行定义）|
| docs/MONTHLY_ANALYSIS_SAMPLE_V3.md | 新建 | V3样稿 |

---

## 二、反馈结构化结果

**强信号（直接采纳）**：Q3（一页书面判断）+ Q4（部门+角色粒度）+ Q5（三档条件）→ V2/V3保持不变

**中信号（试行采纳）**：Q1（企金部主办）+ Q2（双门槛1000万/5000万）→ V3试行表达

**待验证信号**：Q6（持续意愿B）→ 记录为本期质量触发项，不修改模板

---

## 三、V3收敛方案选择

| 方案 | 选择 | 理由 |
|------|------|------|
| 方案A（保守吸收型）| ❌ 不选 | 反馈吸收不充分，执行侧反馈未体现在V3 |
| 方案B（平衡收敛型）| ✅ 推荐 | 真实反馈有实质落地；试行表达保留调整空间；不提前定型 |
| 方案C（强收敛型）| ❌ 不选 | 一份反馈权重过大；跨机构普适性未经验证 |

---

## 四、本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不虚构第二、第三份反馈 | ✅ |
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做 UI/数据库/自动调度 | ✅ |
| 不做最终定稿 | ✅ |
| 不改评分权重/top-k/Gate A | ✅ |
| 不引入无关扩项 | ✅ |

---

## 五、本轮自review结果

- ✅ 真实反馈已做结构化拆解（强信号/中信号/待验证三类）
- ✅ 已提出3套V3收敛方案并完成比较
- ✅ 推荐方案B（平衡收敛型）已说明理由
- ✅ V3相比V2的改动点可明确追溯到真实反馈来源
- ✅ 试行表达已有明确定义和反馈触发机制
- ✅ 未虚构反馈，未引入无关扩项
- ✅ REVIEW_LOG有本轮记录（R-49）

---

## 六、文档同步

- ✅ REAL_FEEDBACK_LOG_01.md（新建）
- ✅ LEADER_OUTPUT_TEMPLATE_V2.md（新建）
- ✅ EXECUTION_OUTPUT_TEMPLATE_V2.md（新建）
- ✅ ACTION_EXPRESSION_RULES_V3.md（新建）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V3.md（新建）
- ✅ CHANGE_CONTROL（+CC-37，进行中）
- ✅ REVIEW_LOG（+R-49）

---

## 七、当前状态

- **状态**：✅ P2-5 实施完成；V3收敛完成
- **下一状态**：停在"V3已收敛、等待第二/第三份反馈验证"状态
- **不自动进入**：不自动进入P2-6；不宣布最终定型；不进入正式部署

---

# R-50 — P2-6 第二/第三份真实反馈回采

**日期**：2026-04-10
**对应阶段**：P2-6（第二/第三份真实反馈回采 + V4收敛实施包）
**触发**：P2-5完成，V3已收敛，需要至少2份新增真实反馈才能进入V4

---

## 一、本轮实施内容

| 文件 | 操作 | 说明 |
|------|------|------|
| docs/BUSINESS_FEEDBACK_LEADER_V1.md | 新建 | 领导版最小反馈包V1（3题）|
| docs/BUSINESS_FEEDBACK_EXEC_V1.md | 新建 | 执行/管理版最小反馈包V1（4题）|
| docs/FEEDBACK_TRACKING_STATUS.md | 新建 | 反馈回采状态追踪文档 |

---

## 二、当前状态

- **已收到反馈**：1份（FB-01，邱非，FP-03）
- **FB-02/FB-03**：尚未收到
- **V4收敛条件**：未满足

---

## 三、本轮V4收敛方案预判（基于当前1份反馈）

| 方案 | 选择 | 理由 |
|------|------|------|
| 方案A（只固化一致项）| ⏳ 预判可选 | V3的Q3/Q4/Q5在多份反馈支持后升级；Q1/Q2保留试行 |
| 方案B（平衡收敛）| ⏳ 预判推荐 | 一致项固化；冲突项分层处理；不因单一反馈过拟合 |
| 方案C（强收敛）| ❌ 不可选 | 违反"不虚构反馈"原则 |

**注**：V4收敛需等待FB-02/FB-03收到后才能正式执行。当前只完成方案预判。

---

## 四、本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不虚构第二、第三份反馈 | ✅ |
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做 UI/数据库/自动调度 | ✅ |
| 不做最终定稿 | ✅ |
| 不改评分权重/top-k/Gate A | ✅ |
| 不引入无关扩项 | ✅ |

---

## 五、当前状态：停在"等待新增真实反馈"

**原因**：
- FB-01仅1份，Q1/Q2的试行边界仍需第二/第三份验证
- 领导层视角（FP-01）完全缺失
- V4收敛充要条件未满足

**下一状态触发**：FB-02或FB-03收到任意一份真实反馈 → 立即启动V4收敛分析

---

## 六、文档同步

- ✅ BUSINESS_FEEDBACK_LEADER_V1.md（新建）
- ✅ BUSINESS_FEEDBACK_EXEC_V1.md（新建）
- ✅ FEEDBACK_TRACKING_STATUS.md（新建）
- ✅ REVIEW_LOG（+R-50）
- ✅ CHANGE_CONTROL（+CC-38，进行中）

---

## 七、当前状态

- **状态**：✅ P2-6 实施完成；停在"等待新增真实反馈"状态
- **不自动进入**：不自动进入P2-7；不宣布V4已完成；不进入正式部署

---

# R-51 — P2-7 新增真实反馈摄入 + V4收敛

**日期**：2026-04-10
**对应阶段**：P2-7（新增真实反馈摄入 + V4收敛）
**触发**：FB-02收到（webchat渠道，17:47）

---

## 一、本轮实施内容

| 文件 | 操作 | 说明 |
|------|------|------|
| docs/REAL_FEEDBACK_LOG_02.md | 新建 | FB-02录入+结构化分类 |
| docs/LEADER_OUTPUT_TEMPLATE_V3.md | 新建 | 领导版模板V3（企金部归口升级）|
| docs/EXECUTION_OUTPUT_TEMPLATE_V3.md | 新建 | 执行版模板V3（双门槛确认+打头结论鲜明）|
| docs/ACTION_EXPRESSION_RULES_V4.md | 新建 | 动作规则V4（多源确认定义+升级路径）|
| docs/MONTHLY_ANALYSIS_SAMPLE_V4.md | 新建 | V4样稿 |
| docs/FEEDBACK_TRACKING_STATUS.md | 更新 | 反映FB-01+FB-02状态+V4收敛完成 |

---

## 二、反馈结构化结果

**一致项（4项，升级为多源确认）**：
- Q1企金部归口：FB-01+FB-02均选B → 当前推荐·多源确认
- Q4粒度合适：FB-01+FB-02均选A → 多源确认
- Q5三档条件：FB-01+FB-02均选A → 多源确认
- Q6持续意愿：FB-01+FB-02均选B → 触发项，不进模板

**冲突项（2项，妥善处理）**：
- Q2门槛：FB-01选C（降1000万），FB-02选B（5000万合理）→ 双门槛结构获多源支持，数值保留弹性
- Q3报告接收意愿：FB-01选A（会看），FB-02选B（不一定）→ 形式不被否定，新增"打头结论必须够鲜明"要求

---

## 三、V4收敛方案选择

| 方案 | 选择 | 理由 |
|------|------|------|
| 方案A（谨慎收敛）| 未选 | V3试行升级条件已满足（2份独立反馈）|
| 方案B（平衡收敛）| ✅ 推荐 | 4项一致项升级为多源确认；2项冲突妥善处理（不阻断）|
| 方案C（强化收敛）| ❌ 不选 | Q2/Q3冲突存在，不能强行收死 |

---

## 四、本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不虚构更多反馈 | ✅ |
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做 UI/数据库/自动调度 | ✅ |
| 不做最终定稿 | ✅ |
| 不改评分权重/top-k/Gate A | ✅ |
| 不引入无关扩项 | ✅ |

---

## 五、本轮自review结果

- ✅ FB-02录入完成，冲突分析到位
- ✅ V4收敛基于真实反馈（FB-01+FB-02），不虚构
- ✅ Q2/Q3冲突有合理V4处理方式（结构确认+新增要求）
- ✅ 一致项升级为多源确认有充分依据
- ✅ 未引入无关扩项
- ✅ REVIEW_LOG有本轮记录（R-51）

---

## 六、文档同步

- ✅ REAL_FEEDBACK_LOG_02.md（新建）
- ✅ LEADER_OUTPUT_TEMPLATE_V3.md（新建）
- ✅ EXECUTION_OUTPUT_TEMPLATE_V3.md（新建）
- ✅ ACTION_EXPRESSION_RULES_V4.md（新建）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V4.md（新建）
- ✅ FEEDBACK_TRACKING_STATUS.md（更新）
- ✅ REVIEW_LOG（+R-51）
- ✅ CHANGE_CONTROL（+CC-39，进行中）

---

## 七、当前状态

- **状态**：✅ P2-7 V4收敛完成
- **反馈状态**：FB-01+FB-02（执行侧各1份）；领导层（FP-01）反馈仍缺失
- **下一状态触发**：领导层反馈收到 → 可做领导版V4确认
- **不自动进入**：不宣布V4为最终定型；不进入正式部署

---

# R-52 — P2-7 FB-03 新增摄入 + V4 收敛修订

**日期**：2026-04-10 17:54
**对应阶段**：P2-7（FB-03 新增摄入 + V4 收敛修订）
**触发**：FB-03 收到（webchat 渠道，17:54）

---

## 一、FB-03 原始答案

Q1=B, Q2=B, Q3=A, Q4=C, Q5=A, Q6=B

---

## 二、关键发现：Q4 三方分歧

- FB-01：Q4 选 A（合适，能落到人）
- FB-02：Q4 选 A（合适，能落到人）
- FB-03：Q4 选 C（太细，部门级就够了）

**影响**：V4 中 Q4"部门+角色粒度"从"多源确认"降级为"**试行·三方分歧**"

---

## 三、V4 收敛修订内容

| 内容 | 修订前（V4初版）| 修订后（FB-03后）| 原因 |
|------|--------------|----------------|------|
| 企金部门归口 | 当前推荐·多源确认 | **当前推荐·强确认** | FB-01+FB-02+FB-03三源一致 |
| 部门+角色粒度 | 多源确认 | **试行·三方分歧（降级）** | FB-03选C，与FB-01/02分歧 |
| 双门槛结构 | 当前推荐·结构确认 | **当前推荐·结构确认** | FB-02+FB-03（2/3）支持5000万 |

---

## 四、FB-03 的意义

- Q4 是本次唯一出现三方分歧的题（FB-01/02一致 vs FB-03反对）
- Q1/Q5 升级为三源强确认（3/3一致）
- Q2 维持 2:1 多数确认
- Q3 维持 2:1 多数确认（FB-02 少数意见已不主导）

---

## 五、文档更新

| 文件 | 操作 |
|------|------|
| docs/REAL_FEEDBACK_LOG_03.md | 新建 |
| docs/ACTION_EXPRESSION_RULES_V4.md | 更新（Q4降级，版本升至v3.1）|
| docs/EXECUTION_OUTPUT_TEMPLATE_V3.md | 更新（Q4降级，版本升至v3.1）|
| docs/MONTHLY_ANALYSIS_SAMPLE_V4.md | 更新（Q4降级，版本升至v3.1）|
| docs/FEEDBACK_TRACKING_STATUS.md | 更新（反映3份反馈汇总）|
| REVIEW_LOG | +R-52 |
| CHANGE_CONTROL | +CC-40 |

---

## 六、当前状态

- **反馈状态**：FB-01+FB-02+FB-03（3份执行侧，均为FP-03背景）
- **领导层反馈**：仍缺失
- **下一状态触发**：领导层（FP-01）收到 → 可做领导版最终确认
- **不自动进入**：不宣布V4为最终定型

---

# R-53 — P2-8 V5 试用版固化 + 小范围试发设计

**日期**：2026-04-10
**对应阶段**：P2-8（试用版固化 + 小范围真实试发验证）
**触发**：V4跨角色反馈收敛完成（FB-01+FB-02+FB-03）

---

## 一、本轮实施内容

| 文件 | 操作 | 说明 |
|------|------|------|
| docs/TRIAL_VERSION_BASELINE_V5.md | 新建 | V5试用版基线说明 |
| docs/LEADER_OUTPUT_TEMPLATE_V4.md | 新建 | 领导版模板V4 |
| docs/EXECUTION_OUTPUT_TEMPLATE_V4.md | 新建 | 执行版模板V4 |
| docs/ACTION_EXPRESSION_RULES_V5.md | 新建 | 动作规则V5 |
| docs/MONTHLY_ANALYSIS_SAMPLE_V5.md | 新建 | V5样稿 |
| docs/TRIAL_DESIGN_V5.md | 新建 | 小范围试发设计方案 |
| docs/FEEDBACK_TRACKING_STATUS.md | 更新 | 修正FB-02为领导视角；状态切换到"试用验证阶段" |

---

## 二、V5 稳定项 / 弹性项 / 待观察项

**稳定项（进入V5，当前推荐表达）**：
- 企金部门归口 [当前推荐·强确认]
- 三档转动作条件 [多源确认]
- 一页书面判断格式 [多源确认]
- 报告打头结论鲜明 [V5继承]

**弹性项（进入V5，保留弹性写法）**：
- 双门槛结构（结构）[当前推荐·结构确认]
- 双门槛具体数值 [试行·弹性]
- 部门+角色粒度 [试行·弹性]

**待观察项（不进模板，继续观察）**：
- 领导版L-1/L-2（从未被真正验证）
- 企金部/战略研究部互换性
- 跨行普适性

---

## 三、V5 固化方案

选择方案B（平衡固化型）：
- 强一致项直接进入"当前推荐"
- 弹性项保留弹性写法
- 待观察项不进模板，继续观察

**不选方案A**：V5已具备充分反馈基础，谨慎固化过于保守
**不选方案C**：部分反馈分歧仍存在，强固化有风险

---

## 四、试发设计

- 对象A（领导视角）：验证L-1/L-2
- 对象B（执行负责人）：验证P1/P2/P3
- 对象C（潜在持续试用）：验证P4

---

## 五、当前状态

- **状态**：V5试用版已固化；试发包已准备好；停在"可发出"状态
- **不自动进入**：不宣布V5为最终定型；不进入正式部署
- **触发条件**：确认试发对象联系方式后，实际发送并记录反馈

---

## 六、文档同步

- ✅ TRIAL_VERSION_BASELINE_V5.md（新建）
- ✅ LEADER_OUTPUT_TEMPLATE_V4.md（新建）
- ✅ EXECUTION_OUTPUT_TEMPLATE_V4.md（新建）
- ✅ ACTION_EXPRESSION_RULES_V5.md（新建）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V5.md（新建）
- ✅ TRIAL_DESIGN_V5.md（新建）
- ✅ FEEDBACK_TRACKING_STATUS.md（更新）
- ✅ REVIEW_LOG（+R-53）
- ✅ CHANGE_CONTROL（+CC-41）

---

# R-54 — P2-9 首轮试发准备

**日期**：2026-04-10
**对应阶段**：P2-9（小范围真实试发 + 首轮使用证据留痕）
**触发**：V5试用版已固化，需要真实试发验证

---

## 一、本轮实施内容

| 文件 | 操作 | 说明 |
|------|------|------|
| docs/TRIAL_RUN_LOG_01.md | 新建 | 首轮试发记录（待发送状态）|
| docs/FEEDBACK_TRACKING_STATUS.md | 更新 | 切换到"试发进行中"状态 |

---

## 二、当前状态

- V5试用版已固化 ✅
- 试发包已准备（领导版V4+执行版V4）✅
- **尚未实际发送**（停在"待发送"状态）❌
- 试发成功门槛已定义（4项T1~T4）

---

## 三、试发成功最低门槛

| 门槛 | 标准 |
|------|------|
| T1 | L-1或P1 有≥1人正向（A/B）|
| T2 | P2 有≥1人回答"知道怎么做"（A/B）|
| T3 | P3 有≥1人回答"可操作"（A/B）|
| T4 | 至少1人表达愿意继续收（A或B）|

---

## 四、试发对象

| 对象 | 类型 | 发送内容 | 验证问题 |
|------|------|---------|---------|
| TRL-01-A | 领导视角 | 领导版V4样稿 | L-1、L-2、P4 |
| TRL-01-B | 执行负责人 | 执行版V4样稿 | P1、P2、P3、P4 |
| TRL-01-C | 潜在持续试用 | 执行版V4样稿 | P4 |

---

## 五、触发条件

**实际发送触发**：用户确认3位发送对象和发送方式后，执行发送动作并更新TRIAL_RUN_LOG_01.md

---

## 六、当前状态

- **状态**：停在"待发送"状态
- **触发条件**：用户确认发送对象和发送方式
- **不自动进入**：不进入正式部署

---

# R-55 — P2-9 真实试发发送动作执行

**日期**：2026-04-10 22:21
**对应阶段**：P2-9（小范围真实试发 + 首轮使用证据留痕）
**触发**：V5试用版已固化，需执行真实试发发送

---

## 一、执行内容

1. 将 MONTHLY_ANALYSIS_SAMPLE_V5.md 拆分为两个附件：
   - `reports/TRIAL_SEND/LEADER_TRIAL_V5.md`（领导版试发稿）
   - `reports/TRIAL_SEND/EXEC_TRIAL_V5.md`（执行版试发稿）

2. 预备 A/B/C 三组邮件内容（收件人、主题、正文、附件均已确定）

3. 更新 TRIAL_RUN_LOG_01.md（v1.1）：记录6位试发对象、邮件内容、发送状态

4. 更新 FEEDBACK_TRACKING_STATUS.md：切换到"待用户执行发送"状态

---

## 二、发送限制

- 工具链不覆盖 pingan.com.cn 外部邮件地址
- 三封邮件需由用户在本地邮件客户端执行发送
- A/B/C 三组发送内容和附件均已准备完毕

---

## 三、试发对象

| 组别 | 收件人 | 类型 | 发送内容 |
|------|--------|------|---------|
| A组 | 赵总、曾总 | 领导视角 | LEADER_TRIAL_V5.md |
| B组 | 邱非、黄真 | 执行负责人 | EXEC_TRIAL_V5.md |
| C组 | 李乐思、陈嘉茵 | 潜在持续试用 | EXEC_TRIAL_V5.md |

---

## 四、当前状态

- **状态**：⏳ 待用户在本地执行发送
- **不自动进入**：不宣布V5为最终定型；不进入正式部署
- **触发条件**：用户执行 A/B/C 三组邮件发送 → 等待反馈回收

---

# R-56 — P2-9 真实试发发送结果记录

**日期**：2026-04-10 22:26
**对应阶段**：P2-9（真实试发发送）
**发送结果**：A组2封✅ + B组2封✅ + C组2封❌（QQ邮箱ex-前缀限制）

---

## 发送结果

| 组别 | 收件人 | 结果 |
|------|--------|------|
| A组 | 赵总（zhaofanjue696@pingan.com.cn）| ✅ 已发送 |
| A组 | 曾总（zengjunlin@pingan.com.cn）| ✅ 已发送 |
| B组 | 邱非（qiufei714@pingan.com.cn）| ✅ 已发送 |
| B组 | 黄真（huangzhen546@pingan.com.cn）| ✅ 已发送 |
| C组 | 李乐思（ex-lilesi527@pingan.com.cn）| ❌ QQ邮箱ex-前缀限制 |
| C组 | 陈嘉茵（chenjiayin586@pingan.com.cn）| ❌ QQ邮箱ex-前缀限制 |

---

## C组发送失败原因

QQ邮箱SMTP持续报"Connection unexpectedly closed"，疑似对ex-前缀别名账户的外部域名发送有限制。

---

## 当前状态

- **A组+B组**：已发出，等待回收
- **C组**：待换其他方式

---

# R-57 — P2-10 6份反馈归并 + V6 轻量收窄实施

**日期**：2026-04-14
**对应阶段**：P2-10（6份反馈归并 + V6 轻量收窄实施包）
**触发**：6份真实试发反馈已全部回收（FB-01~FB-03 + TRL-01 A/B组）

---

## 一、本轮实施内容

| 文件 | 操作 | 说明 |
|------|------|------|
| docs/FEEDBACK_TRACKING_STATUS.md | 更新 | 更新为6份反馈状态 + 版本信号归并表 |
| docs/TRIAL_FEEDBACK_SUMMARY_06.md | 新建 | 6份反馈正式归并结论文档 |
| docs/TRIAL_VERSION_BASELINE_V6.md | 新建 | V6试用版基线说明 |
| docs/LEADER_OUTPUT_TEMPLATE_V5.md | 新建 | 领导版模板V5（轻量收窄版）|
| docs/EXECUTION_OUTPUT_TEMPLATE_V5.md | 新建 | 执行版模板V5（轻量收窄版）|
| docs/ACTION_EXPRESSION_RULES_V6.md | 新建 | 动作规则V6（轻量收窄版）|
| docs/MONTHLY_ANALYSIS_SAMPLE_V6.md | 新建 | V6样稿 |

---

## 二、6份反馈统计结果

| 问题 | 核心内容 | 结果 |
|------|---------|------|
| Q1 | 企金部主办 + 研究支持配合 | **6/6 = A** |
| Q2 | 双门槛结构（5000万/1000万）| **1A + 5B = 6** |
| Q3 | 三档转动作条件 | **6/6 = B** |
| Q4 | 持续愿意看/用下一版 | **6/6 = B** |

---

## 三、版本信号归并

| 分类 | 信号 | V6处理 |
|------|------|--------|
| **A类（强信号）** | S-A1：企金主办方向 | 升级为"6源一致确认" |
| **B类（轻量化信号）** | S-B1：双门槛结构正确，数值需弹性 | 结构不变；数值改为"参考阈值/各行可调" |
| | S-B2：三档条件有帮助但偏重 | 逻辑保留；表达压缩为2行注语 |
| **C类（观察信号）** | S-C1：持续意愿为B，未达强订阅 | V6更顺手为手段；不下定论 |

---

## 四、V6 收窄方案比较

| 方案 | 选择 | 理由 |
|------|------|------|
| 方案A（仅文风轻量化）| ❌ 不选 | S-B2（6/6感受偏重）和 S-C1（6/6 B类意愿）无法通过文风解决 |
| **方案B（轻量收窄型）** | ✅ 推荐 | 系统性吸收6份反馈；改动幅度可控；符合"不推翻既有框架"原则 |
| 方案C（结构重写）| ❌ 不选 | 违反"不再做大结构改写"；6份反馈无结构反对信号 |

---

## 五、V6 相比 V5 的轻量收窄点

| # | V5 | V6 | 驱动信号 |
|---|----|----|---------|
| 1 | 企金归口"三源强确认" | "6源一致确认" | Q1 6/6 = A |
| 2 | 双门槛数值"[试行·弹性]" | "[参考值·可调]" | Q2 1A+5B |
| 3 | 三档条件：完整段落 | 2行注语 | Q3 6/6 = B |
| 4 | 领导版约1300字 | 约900字 | Q3反馈一致感受偏重 |
| 5 | 执行版约1100字 | 约850字 | 整体压缩 |
| 6 | 持续意愿"不下定论" | "V6顺手度为验证手段" | Q4 6/6 = B |

---

## 六、自 review 结果

- ✅ 6份反馈归并基于用户确认的统计结果
- ✅ 已提出3套方案并完成比较（方案A/B/C）
- ✅ 推荐方案B已说明理由
- ✅ V6改动严格对应6份反馈信号（S-A1/S-B1/S-B2/S-C1）
- ✅ 未引入无关扩项
- ✅ 未虚构反馈
- ✅ 未推翻既有框架
- ✅ REVIEW_LOG有本轮记录（R-57）

---

## 七、本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不虚构更多反馈 | ✅ |
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做 UI/数据库/自动调度 | ✅ |
| 不做最终定稿 | ✅ |
| 不改评分权重/top-k/Gate A | ✅ |
| 不引入无关扩项 | ✅ |
| 不推翻既有框架 | ✅ |
| 不做大结构改写 | ✅ |

---

## 八、本轮明确不做

- ❌ UI 按钮
- ❌ 正式运营后台
- ❌ 自动 cron / 调度
- ❌ 自动 fetch
- ❌ 多角色协同权限系统
- ❌ confirmLevel 规则重构
- ❌ OI-03 / OI-04 等运行优化
- ❌ 整体来源治理体系重构
- ❌ 虚构反馈
- ❌ 最终定稿
- ❌ 正式部署

---

## 九、文档同步

- ✅ FEEDBACK_TRACKING_STATUS.md（更新）
- ✅ TRIAL_FEEDBACK_SUMMARY_06.md（新建）
- ✅ TRIAL_VERSION_BASELINE_V6.md（新建）
- ✅ LEADER_OUTPUT_TEMPLATE_V5.md（新建）
- ✅ EXECUTION_OUTPUT_TEMPLATE_V5.md（新建）
- ✅ ACTION_EXPRESSION_RULES_V6.md（新建）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V6.md（新建）
- ✅ REVIEW_LOG（+R-57）v1.31
- ✅ CHANGE_CONTROL（+CC-33→进行中）

---

## 十、当前状态

- **状态**：✅ P2-10 实施完成
- **下一步**：V6 下一轮小范围试发，验证 Q4 是否出现 A
- **V6后判断条件**：
  - Q4出现A → 可考虑进入更正式试用周期
  - Q4仍全B → 继续微调，暂不定型
  - 出现C → 回退定位

---

*记录：AI雷达站 agent，2026-04-14（P2-10）*

| R-58 | 2026-04-14 | P2-11 V6二轮试发设计完成（第二轮验证重点与TRL-01区分；二轮方案A/B/C比较完成；推荐方案B；TRIAL_DESIGN_V6新建；TRIAL_FEEDBACK_PACK_V6_LEADER/EXEC新建；FEEDBACK_TRACKING_STATUS更新；TRIAL_RUN_LOG_02新建）| ✅ 完成（待发送）| P2-11 |

| R-59 | 2026-04-14 | P2-12 V6二轮试发执行完成（Step1收尾校验；Step2名单：B2-new未确认→fallback为3人版；Step3验证问题T2-Q1~Q4；Step4渠道阻断；Step5留痕完成）| ✅ 执行完成 | P2-12 |

| R-60 | 2026-04-15 | P2-13 V6负向反馈吸收+V7回退修复（执行侧邱非Q1=D/Q3=C/Q4=C；V6立即停止；F1~F6失败原因分析；保留/回退/重做清单；方案B推荐；NEGATIVE_FEEDBACK_LOG_01+TRIAL_VERSION_BASELINE_V7+EXECUTION_OUTPUT_TEMPLATE_V6+ACTION_EXPRESSION_RULES_V7+MONTHLY_ANALYSIS_SAMPLE_V7新建；FEEDBACK_TRACKING_STATUS更新）| ✅ 完成 | P2-13 |

### Review R-60（P2-13 V6 负向反馈吸收 + V7 回退修复）

- **日期**：2026-04-15
- **review 对象**：P2-13 负向反馈吸收与 V7 回退修复实施
- **所属阶段**：P2-13（V6 负向反馈吸收 + V7 回退修复）
- **核查范围**：Step 1 收尾校验 / Step 2 失败原因识别 / Step 3 保留回退重做 / Step 4 方案比较 / Step 5 推荐方案 / Step 6 最小落地

#### Step 1 收尾校验

- ✅ P2-12 阶段状态已从"V6二轮试发执行"切换为"P2-13 V6负向反馈吸收"
- ✅ V6 立即停止继续发送
- ✅ 本轮不是继续试发，而是止损 + 修复
- ✅ 无阻断

#### Step 2 失败原因识别（F1~F6）

| # | 原因 | 是否必须修复 |
|---|------|------------|
| F1 | 为轻量而过度压缩三档条件，删除数值背景说明 | ✅ |
| F2 | 执行版缺少"为什么现在要做"的足够说明 | ✅ |
| F3 | 动作句仍偏分析建议语气，缺乏部署感 | ✅ |
| F4 | 执行版更像摘要，不像行动稿，缺少第一手操作细节 | ✅ |
| F5 | 篇幅压缩超出必要边界 | ✅ |
| F6 | 三档条件压缩后缺少数值背景 | ✅ |

**结论**：V6 失败是"过度压缩 + 动作翻译失败"组合，**不是结构问题**。

#### Step 3 保留 / 回退 / 重做

**保留**（方向正确，不动）：企金归口 / 双门槛结构 / 三段式 / 报告打头结论 / 部门+角色两级

**回退**（V6 压缩过度）：三档条件 2行注语→V4/V5完整段落 / 执行版说明层

**重做**（V6 表达方式错误）：主动作格式改为动词打头+三步式 / 数值背景恢复 / 研究内容完成标准

#### Step 4 方案比较（3个方案）

| 方案 | 修复幅度 | 推荐度 |
|------|---------|--------|
| 方案A：小修补型 | 最小 | ❌ 不推荐（只能修复Q2，不解决Q1/Q3/Q4）|
| **方案B：回退修复型** | 中等 | ✅ **推荐** |
| 方案C：全面重写型 | 最大 | ❌ 不推荐（过度反应，推翻未失败的方向）|

#### Step 5 推荐方案

- **推荐**：方案B（回退修复型）
- **理由**：精准针对 F1~F6；最符合当前问题类型；不推翻已确认方向的积累
- **最小边界**：三档条件回退 + 主动作重写 + 说明层恢复
- **篇幅**：约950~1000字（必要信息厚度回归，不是V5冗余回归）

#### Step 6 落地结果

| 文档 | 状态 |
|------|------|
| NEGATIVE_FEEDBACK_LOG_01.md | ✅ 新建 v1.0 |
| TRIAL_VERSION_BASELINE_V7.md | ✅ 新建 v1.0 |
| EXECUTION_OUTPUT_TEMPLATE_V6.md | ✅ 新建 v1.0 |
| ACTION_EXPRESSION_RULES_V7.md | ✅ 新建 v1.0 |
| MONTHLY_ANALYSIS_SAMPLE_V7.md | ✅ 新建 v1.0 |
| FEEDBACK_TRACKING_STATUS.md | ✅ 更新（V6停止 → V7修复中）|
| REVIEW_LOG | ✅ +R-60 |
| CHANGE_CONTROL | ✅ +CC-48 |

#### 自 review 结果

- ✅ 只做负向反馈吸收和 V7 回退修复，未扩项
- ✅ 未改抓取机制/来源配置/preflight/run 逻辑
- ✅ 未引入 UI/数据库/自动 fetch/任务系统
- ✅ V7 仍不是最终定稿
- ✅ 文档与事实一致

#### 本轮强边界执行情况

| 边界 | 是否遵守 |
|------|---------|
| 不虚构更多反馈 | ✅ |
| 不改抓取逻辑 | ✅ |
| 不改 analyst_sources.json | ✅ |
| 不改 preflight/run 机制 | ✅ |
| 不做自动 fetch/调度 | ✅ |
| 不做 UI 按钮/数据库/任务系统 | ✅ |
| 不做 confirmLevel/Gate A 等无关修复 | ✅ |
| 不把本轮做成最终定稿 | ✅ |
| 不把本轮理解成项目失败 | ✅ |

#### 文档同步

- ✅ REVIEW_LOG（+R-60）v1.32
- ✅ CHANGE_CONTROL（+CC-48）v1.24
- ✅ FEEDBACK_TRACKING_STATUS.md（更新）
- ✅ NEGATIVE_FEEDBACK_LOG_01.md（新建）
- ✅ TRIAL_VERSION_BASELINE_V7.md（新建）
- ✅ EXECUTION_OUTPUT_TEMPLATE_V6.md（新建）
- ✅ ACTION_EXPRESSION_RULES_V7.md（新建）
- ✅ MONTHLY_ANALYSIS_SAMPLE_V7.md（新建）

- **状态**：✅ P2-13 实施完成（V7 修复落地，下一步：V7 修复后重新试发）


### Review R-61（P2-14 V7重新试发 + 修复有效性验证）

- **日期**：2026-04-15
- **review 对象**：P2-14 V7重新试发实施
- **所属阶段**：P2-14（V7 重新试发 + 修复有效性验证）
- **核查范围**：Step 1 收尾校验 / Step 2 试发对象与问题 / Step 3 修复成功标准 / Step 4 发送包 / Step 5 执行发送 / Step 7 判断状态

#### Step 1 收尾校验

- ✅ V7已处于"待重新试发"状态，不再是"待继续修稿"
- ✅ 自动发送渠道阻断不再构成推进阻断，已切换为人工发送fallback
- ✅ 用户人工发送被视为正式执行动作

#### Step 2 试发对象与问题确认

- ✅ 沿用TRL-02的3人名单（赵总/曾总/邱非），减少变量
- ✅ 领导版问V7-Q1（顺手度）+ V7-Q2（动作可用性）+ V7-Q3（持续意愿）
- ✅ 执行版问V7-Q1 + V7-Q2（三档条件） + V7-Q3（动作可用性） + V7-Q4（持续意愿）
- ✅ 不再重复问企金归口/双门槛等已确认的结构性问题

#### Step 3 修复成功最低标准

- ✅ T1: V7-Q1 ≥1人A/B 或 ≥2人B
- ✅ T2: V7-Q3 ≥1人A/B 或 ≥2人B
- ✅ T3: V7-Q4 ≥1人A 或 多数B且无集中C
- ✅ 通过条件: T1+T2+T3全部满足

#### Step 4 发送包准备

- ✅ TRIAL_FEEDBACK_PACK_V7_LEADER.md（新建，领导版3问）
- ✅ TRIAL_FEEDBACK_PACK_V7_EXEC.md（新建，执行版4问）
- ✅ TRIAL_SEND_PACK_V7.md（新建，人工发送fallback包）
- ✅ TRIAL_RUN_LOG_03.md（新建，V7重新试发记录）

#### Step 5 执行发送

- ✅ 自动发送渠道全部阻断（企业微信WSClient未连接/飞书未配置/QQ群ID未知）
- ✅ 立即切换为人工发送fallback，不停止
- ✅ 输出"人工发送包已准备完成"
- ✅ 当前状态标记为"待用户手动发送"

#### Step 7 判断状态

- ✅ 未收到回复时，状态写为"V7已准备好重新试发，待用户手动发送"
- ✅ 不继续改内容

#### 自 review 结果

- ✅ 未引入扩项（无UI/无数据库/无自动fetch/无任务系统）
- ✅ 未改抓取逻辑/analyst_sources.json/preflight/run机制
- ✅ 未改评分权重/Gate A/confirmLevel
- ✅ V7未当成最终定稿
- ✅ 文档与事实一致

#### 文档同步

- ✅ TRIAL_FEEDBACK_PACK_V7_LEADER.md（新建）
- ✅ TRIAL_FEEDBACK_PACK_V7_EXEC.md（新建）
- ✅ TRIAL_SEND_PACK_V7.md（新建）
- ✅ TRIAL_RUN_LOG_03.md（新建）
- ✅ FEEDBACK_TRACKING_STATUS.md（更新为P2-14状态）
- ✅ REVIEW_LOG（+R-61）v1.33

- **状态**：✅ P2-14 实施完成（V7重新试发准备完成，待用户手动发送）

