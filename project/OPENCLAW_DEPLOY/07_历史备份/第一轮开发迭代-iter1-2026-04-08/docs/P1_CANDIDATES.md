# P1_CANDIDATES.md — P1 候选任务清单与优先级建议

> 文档版本：v1.9（本次更新：增加 P1-6a dry-run 可解释性增强章节）
> 建立日期：2026-04-07
> 对应阶段：P1-1/P1-1b/P1-2/P1-3/P1-4 全部完成
> 依据：PHASE3_CLOSURE_REPORT.md / PHASE3_BASELINE.md / PHASE3_TASK_PACKAGE.md v1.4 / DECISION_LOG D-08

---

## 一、P1 候选任务总览

| 编号 | 任务名称 | 优先级 | 是否影响试点 | 是否阻断 P1 后续 | 建议 | 状态 |
|------|---------|-------|------------|----------------|------|------|
| P1-1 | review 状态持久化（独立台账） | **P0** | 体验断点 | 是 | **已完成** | ✅ 已完成 |
| P1-1b | CSV轻量追踪表（pilot-tracking-ledger.csv） | P1 | 不影响 | 否 | 已完成 | ✅ 已完成 |
| P1-2 | 分析师来源有效性review | P1 | 不影响 | 否 | 已完成 | ✅ 已完成 |
| P1-3 | 最小试点运行SOP/周期机制/复核节奏 | P1 | 不影响 | 否 | 已完成 | ✅ 已完成 |
| P1-4 | 多轮试点复盘机制（ROUND_COMPARISON） | P1 | 不影响 | 否 | 已完成 | ✅ 已完成 |
| P1-3a | 运行入口一致性修正（run-analyst.sh wrapper） | P1 | 阻断 | 是 | **已完成** | ✅ 已完成 |
| P1-3b | 数据刷新与轮次就绪机制（preflight） | P1 | 阻断 | 是 | **已完成** | ✅ 已完成 |
| P1-6 | 人工 fetch 入口统一（run-analyst-fetch.sh） | P1 | 阻断 | 是 | **已完成** | ✅ 已完成 |
| P1-6a | fetch 层 dry-run 可解释性增强 | P1 | 阻断 | 是 | **已完成** | ✅ 已完成 |
| OI-03 | 来源先验权重优化 | P2 | 部分影响 | 否 | 并行处理 | ⏳ 开放中 |
| OPERATING_CYCLE 告警矛盾修正 | 失败处理规则内部矛盾 | P3 | 不影响 | 否 | 低优先级 | ⏳ 待执行 |

---

## 二、P1-1：review 状态持久化（独立台账）

**对应 Phase 3 任务**：PHASE3_TASK_PACKAGE.md P1-1（v1.4 更新）

### 2.1 解决什么问题

当前 review queue 的 reviewStatus/trackingStatus 修改在 JSON 文件层面：
- 运营编辑者修改后状态生效
- **重新运行 build_analyst_opinions.py 后，所有状态重置为 pending/candidate**（D-07 边界）
- 无历史运行日志，无法追溯"什么时候跑过、跑了多少、成功率多少"

### 2.2 影响分析

| 影响维度 | 说明 |
|---------|------|
| 试点体验 | 运营编辑者第一次遇到状态重置，会立即失去信任 |
| 数据完整性 | review 结果无持久化，试点结束后无法复盘 |

### 2.3 是否阻断下一阶段

**是**。状态重置是当前 MVP 最明显的体验断点，P1-2/P1-3 的结果如果无法持久化，也无法发挥价值。

### 2.4 建议实现方式

- **CSV 轻量追踪表**（pilot-tracking-ledger.csv）：基于 review-tracker.py merge 结果导出为 CSV
- **导出字段**：itemId / analystName / articleTitle / confirmLevel / reviewStatus / trackingStatus / updatedAt / note / source
- **source 字段保留理由**：便于后续按来源聚合统计与试点观察（不是任务指派字段）
- **不得改动 Phase 3 基线**：analyst-review-queue.json 的结构不变，review-tracker.json 不变

### 2.5 验收标准

- pilot-tracking-ledger.csv 存在且包含所有 review queue 记录的状态快照
- review-tracker.py merge 输出可正确映射到 CSV 字段
- CSV 可被 Excel / 飞书表格直接打开
- 无 owner / nextAction / deadline / priority 等任务系统字段
- PHASE3_BASELINE.md 同步更新（声明 P1-1b 完成后试点台账能力建立）

### 2.6 优先级理由

P1-1 是当前 MVP 唯一会在真实使用时立即暴露的断点（状态重置），必须第一优先解决。

### 2.7 P1-1 实施结果（2026-04-07）

**实际完成内容**（review 状态持久化，非 fetch-run-log）：
- ✅ 新增 reports/review-tracker.json（独立状态台账）
- ✅ 新增 05_工具脚本/review-tracker.py（upsert + merge）
- ✅ itemId 跨 build 稳定性验证通过
- ✅ merge 落点选方案A（独立 merge 脚本，不嵌入 build）
- ✅ 验收场景通过（build → upsert → 再 build → merge 后 confirmed/follow_up 仍存在）

**P1-1b 实施结果（CSV 轻量追踪表）**：正在实施，待完成。

---

## 三、P1-2：分析师来源有效性 review

**对应 Phase 3 任务**：PHASE3_TASK_PACKAGE.md P1-2

### 3.1 解决什么问题

SOURCE_GOVERNANCE_DRAFT v0.9 是候选初稿，对7个来源的分类尚未经过 review 确认为正式版本。顾慧君/王锟来源0篇（2024年前旧文），这两个来源对当前维度贡献为 0，但分类尚未正式确认。

### 3.2 影响分析

| 影响维度 | 说明 |
|---------|------|
| 来源治理 | 候选初稿不能作为正式治理依据 |
| 试点可信度 | 运营编辑者可能会质疑来源分类的权威性 |
| ED-01 | 无关（Gate A 是外部依赖） |

### 3.3 是否阻断下一阶段

**否**。但 P1-2 完成后可将 SOURCE_GOVERNANCE_DRAFT 从 v0.9 升级为 v1.0（正式版），是来源治理的必要里程碑。

### 3.4 建议实现方式

- 用当前已有的 79 条数据快速进行一次来源 review（不是等新数据）
- analyst_review_notes.md：记录每条来源的 review 结论（保留/降级/移除）
- 更新 SOURCE_GOVERNANCE_DRAFT 为 v1.0（标注"经 P1-2 review 确认"）
- 同步更新 analyst_sources.json（如有变更）

### 3.5 验收标准

- analyst_review_notes.md 存在且每条来源有明确结论
- SOURCE_GOVERNANCE_DRAFT 标注 v1.0（经 P1-2 review 确认）
- analyst_sources.json 对应更新（如有）

### 3.6 优先级理由

P1-2 不阻断试点，可在 P1-1 之后并行推进，或在试点准备期间同步进行。

---

## 四、P1-3：试点运行 SOP / 周期机制 / 复核节奏

> **注（2026-04-07）**：原 P1-3 规划为"确认项分级规则文档化（CONFIRMABILITY_RULES.md）"。该方向需基于2~3轮历史数据才有意义，已降级为后续待办。当前 P1-3 实施为试点运行 SOP，两者可共存，本文档仅记录已完成的新 P1-3。

**对应 Phase 3 任务**：PHASE3_TASK_PACKAGE.md P1-3（已完成）

### 4.1 解决什么问题

MVP 从"能演示"升级为"能按周/轮次稳定运行"，有章可循。当前已有能力（tracker / ledger / queue）需要一套最小运行 SOP 才能真正落地。

### 4.2 影响分析

| 影响维度 | 说明 |
|---------|------|
| 试点运营 | 有 SOP 可执行，避免"知道能跑但不知道怎么跑" |
| 知识沉淀 | 最小小结模板统一归档格式 |
| 来源复核 | 触发条件清单避免漏检或过度检查 |

### 4.3 是否阻断下一阶段

**否**。但 P1-3 完成后，试点运行有 SOP 可依。

### 4.4 建议实现方式

- 新建 PILOT_RUN_SOP.md（人工操作手册）
- 新建 ROUND_RECAP_TEMPLATE.md（每轮小结模板）
- 新建 SOURCE_REVIEW_CHECKLIST.md（来源复核触发条件）
- 触发条件：双周 OR raw 新增≥5条

### 4.5 验收标准

- PILOT_RUN_SOP.md 存在且每步可执行
- ROUND_RECAP_TEMPLATE.md 存在且已填写示例
- 首个完整轮次 ROUND-01 已跑通
- 无 cron/UI/数据库/任务系统
- 与 OPERATING_CYCLE_DRAFT 的状态流转描述不矛盾

### 4.6 优先级理由

P1-3 是知识沉淀类任务，对试点的直接影响较小，建议在 P1-1 运行1~2轮后再推进（有实际数据可参考）。

---

## 五、OI-03：来源先验权重优化（来源优先级调整）

**类型**：非阻断型改进

### 5.1 解决什么问题

相关性评分中来源维度的先验权重过重（score_relevance 中 dim_priority 对薛洪言 base=0.6，对其他分析师 base=0.4），导致周茂华、连平等高相关性文章被薛洪言低相关性文章挤压出 top-5。

**实测案例**：连平（综合分0.865）排名第6，与第5名（0.880）差0.015，被 top-k=5 截断。

### 5.2 影响分析

| 影响维度 | 说明 |
|---------|------|
| 周报覆盖度 | 高相关性文章可能因来源权重被挤出 top-5 |
| 试点可信度 | 运营编辑者可能质疑"为什么某篇文章没进来" |

### 5.3 是否阻断下一阶段

**否**。但优化后 top-5 准确度提升，对试点期间的周报质量有帮助。

### 5.4 建议处理方式

- 在 P1-1 追踪表建立后，用实际运行数据评估 OI-03 的真实影响程度
- 如果试点期间发现明显不合理案例，优先手动干预（P1-1 后的 review_operations.json 可追溯）
- 系统性优化在有2~3轮实际数据后进行

---

## 六、OPERATING_CYCLE_DRAFT 告警逻辑矛盾修正

**类型**：低优先级遗留修正

### 6.1 问题描述

"失败处理规则"中说">50%来源失败则告警"，但"暂不纳入"节已列出"自动告警"属于暂不纳入，两者存在内部矛盾。

### 6.2 影响分析

| 影响维度 | 说明 |
|---------|------|
| 文档一致性 | 对内会造成理解混乱 |
| 试点运营 | 运营编辑者查阅文档时可能困惑 |

### 6.3 建议处理

- 不作为 P1 主线任务
- 在试点运行2~3轮后，确认是否需要告警机制再决定是否修正
- 当前可将"失败处理规则"中的告警表述降级为"建议手动检查"而非"自动告警"

---

## 七、优先级汇总与排序理由

### 7.1 执行顺序建议

```
第一优先：P1-1（状态持久化）
    ↓
第二优先：P1-2（来源有效性 review）  [可与 P1-1 并行]
    ↓
第三优先：P1-3（confirmLevel 规则文档化）  [P1-1 运行1~2轮后]
    ↓
并行处理：OI-03（权重优化）  [P1-1 有数据后再评估]
    ↓
低优先级：OPERATING_CYCLE 告警矛盾修正  [试点2~3轮后再决定]
```

### 7.2 P1-1 必须第一优先的理由

1. **体验断点明确**：重新 build 后状态重置，会在第一次真实使用时立即暴露，严重损害可信度
2. **下游依赖**：P1-2/P1-3 的结果如果无法持久化，也无法发挥价值
3. **试点直接相关**：运营编辑者会直接感受到"改完状态没了"的挫败感
4. **验证快**：P1-1 的验收标准简单（看日志文件是否存在且非空），可以在1个 sprint 内完成

---

## 八、本文档与 Phase 3 基线文档的关系

| Phase 3 基线文档 | 对 P1 的约束 |
|----------------|------------|
| PHASE3_BASELINE.md | P1 变更不得回写篡改 Phase 3 已通过结论 |
| PHASE3_CLOSURE_REPORT.md | P1-1/P1-2/P1-3 的描述不得与 Closure Report 矛盾 |
| CHANGE_CONTROL.md | P1 新增任务必须先记录到 CHANGE_CONTROL"新增建议变更记录"节 |
| DECISION_LOG D-07 | P1-1 不得改变"重新 build 会重置 reviewStatus"的已知边界，而是通过独立存储解决 |

---

## 九、P1-4：多轮试点复盘机制

> **对应 Phase 3 任务**：P1-4（多轮试点复盘机制设计与核验，2026-04-08 完成设计校准）

### 9.1 解决什么问题

当前试点运行已有 ROUND_RECAP（当轮小结），但缺乏跨轮对比机制。ROUND-01 之后，无法判断：数量趋势、状态变化、薛洪言占比是否持续、OI 是否收敛。P1-4 建立最小复盘机制，使 2~3 轮试点能沉淀出可比较的成果。

### 9.2 推荐方案：多轮试点复盘表型（ROUND_COMPARISON.md）

| 维度 | 结论 |
|------|------|
| 方案A（增强 ROUND_RECAP） | 未选：跨轮对比需跨文件，功能不足 |
| 方案B（跨轮对比表） | **推荐**：汇总一处，趋势可见，字段少，填写成本低 |
| 方案C（月度复盘） | 未选：反馈延迟4周，与试点节奏不匹配 |

### 9.3 实施范围

- 新建 `reports/ROUND_RECAP/ROUND_COMPARISON.md`（跨轮数字对比表）
- 更新 `docs/ROUND_RECAP_TEMPLATE.md`（增加跨轮数字提示）
- 更新 `docs/PILOT_RUN_SOP.md`（增加每轮填写 ROUND_COMPARISON 的步骤）
- 视需要新建 `docs/CROSS_ROUND_CHECKLIST.md`（跨轮触发清单）

### 9.4 最小复盘对象

**必须复盘（M1~M5）**：raw/usable/queue 数量变化；reviewStatus/trackingStatus 变化；confirmed/rejected/follow_up 条目；OPEN_ISSUES 增减；来源贡献度变化（薛洪言 top-5 占比）

**建议记录（S1~S3）**：confirmLevel 与人工判断偏离；来源复核触发；异常与挂账

**当前不做（N1~N5）**：queue 绝对值统计；confirmLevel 分布比例；多来源组合贡献度；自动告警；历史全量 trend chart

### 9.5 ROUND_COMPARISON 字段设计（8字段）

roundId / rawCount / usableCount / queueCount / trackerCount / confirmedCount / rejectedCount / topSourceShare（薛洪言 top-5 占比）/ openIssuesStatus

### 9.6 跨轮触发与升级路径

| 触发条件 | 动作 |
|---------|------|
| rejected 首次出现 | 进入 OPEN_ISSUES |
| 薛洪言占比从 4/5 变为 5/5 | ROUND_RECAP 标注关注 |
| OI 连续3轮无变化 | 触发小复盘讨论 |
| usable 变化 ±5 条以上 | ROUND_RECAP 标注追查 |

### 9.7 当前不做事项

- ❌ dashboard / 可视化
- ❌ 自动 cron / 调度
- ❌ PILOT_RETRO_TEMPLATE（2~3轮不需要）
- ❌ CONFIRMABILITY_RULES（已降级为后续待办）
- ❌ 任何系统实现（数据库/服务端/UI）

### 9.8 验收标准

- ROUND_COMPARISON.md 已生成，ROUND-01 baseline 已回填
- ROUND_RECAP_TEMPLATE.md 已更新
- PILOT_RUN_SOP.md 已更新
- REVIEW_LOG 有本轮记录
- 未引入 UI/数据库/自动调度等无关扩项

---

**文档编制人**：AI雷达站 agent
**建立日期**：2026-04-07
**最后更新**：2026-04-08（P1-4 设计校准完成）

---

## 十、P1-3a：运行入口一致性修正

**对应 Phase 3 任务**：P1-3 试点运行 SOP 维护（运行入口一致性）

**问题背景**：
ROUND-02 执行时发现 SOP 中写明的 `run-pipeline.py --full` 在当前环境下不能直接执行。原因：run-pipeline.py 内部路径（SCRIPTS/PROCESSED）和引用脚本（parse_initial_data.py）均为 Phase 2 旧结构，与当前 05_工具脚本/ 和 04_数据与规则/ 目录不对应。

**推荐方案**：方案C——新增最小统一入口包装脚本（run-analyst.sh）

**P1-3a 实施结果**：
- 新建 `05_工具脚本/run-analyst.sh`：analyst 试点运行统一入口
- PILOT_RUN_SOP.md v1.2：入口命令已更新为 `./run-analyst.sh`
- 真实验证通过：4步全部成功，无需临时绕行
- run-pipeline.py 不删除，SOP 中注明其不再作为 analyst 试点入口

**P1-3a 验收标准**：
- [x] 统一入口口径已写入 REVIEW_LOG
- [x] wrapper 职责边界已写入脚本头注释
- [x] run-analyst.sh 已生成（可执行）
- [x] SOP 入口命令已更新
- [x] 真实验证通过（build + queue + merge + export 全流程）
- [x] REVIEW_LOG 有本轮记录
- [x] 未引入 UI/数据库/自动调度等无关扩项

**最后更新**：2026-04-08（P1-3a 实施完成）

---

## 十一、P1-3b：数据刷新与轮次就绪机制

**对应 Phase 3 任务**：P1-3 试点运行 SOP 维护（轮次就绪机制）

**问题背景**：
ROUND-02/03 连续走例外执行，暴露出现有触发机制的盲区：启动前没有"值不值得跑"的前置检查，"例外执行"边界模糊，导致连续无意义轮次稀释了数据粒度。

**P1-3b 实施结果**：
- PILOT_RUN_SOP.md v1.3：每轮开始前检查升级为 preflight 机制（四步骤判断路径）
- 触发逻辑修正：常规/例外/不进入三轨清晰
- "验证脚本可跑"已明确排除为例外理由
- raw 新增检查方法确定：读取 `analyst_opinions_raw.json` 的 `fetchedAt` + 条数对比

**触发判断路径**（已写入 SOP）：
- A. raw 新增 ≥5 条 → 常规执行
- B. 满14天 → 常规执行
- C. 存在：异常/OI提前复查/用户指令 → 例外执行（显式记录）
- D. A/B/C 均不满足 → 不进入完整轮次（仅记录）

**P1-3b 验收标准**：
- [x] 常规/例外/不进入三轨逻辑已写入 SOP
- [x] preflight 检查方法已确定（无 dry-run 依赖）
- [x] "验证脚本可跑"已排除
- [x] REVIEW_LOG 有本轮记录（R-27）
- [x] CHANGE_CONTROL +CC-18 已登记

**最后更新**：2026-04-08（P1-3b 实施完成）

---

## 十二、P1-6：人工 fetch 入口统一

**对应 Phase 3 任务**：P1-6 人工 fetch 入口统一

**问题背景**：
fetch 层与 run-analyst.sh 完全分离，无统一 fetch 入口；fetch 后"数据已刷新"的判断口径未落地为文档。运营编辑者需要记忆脚本路径与参数。

**P1-6 实施结果**：
- 新建 `05_工具脚本/run-analyst-fetch.sh`（可执行，2266字节）
  - fetch orchestration only，不内嵌 preflight/run-analyst.sh 联动
  - 支持默认模式（真实抓取）和 `--check` 模式（dry-run 安全检查）
- PILOT_RUN_SOP.md：v1.4，新增 Section 四（数据刷新 Step 0），明确 fetch → preflight → run 三步节奏

**"数据已刷新"判断口径**（已写入 SOP）：
- 最低信号：fetchedAt 变化 OR raw 条数变化
- "数据已刷新" ≠ "值得跑下一轮"，是否值得跑由 preflight 判断

**fetch → preflight → run 三步节奏**：
1. `./run-analyst-fetch.sh` — 刷新数据（或 `--check` 安全检查）
2. 读取 fetchedAt + 条数变化 — preflight 判断
3. `./run-analyst.sh` — 若 preflight 通过则执行完整轮次

**P1-6 验收标准**：
- [x] run-analyst-fetch.sh 已创建（fetch orchestration only）
- [x] SOP 已接入 fetch → preflight → run 三步节奏
- [x] "数据已刷新"判断口径已写入 SOP
- [x] 最小验证通过（--check 模式可执行）
- [x] REVIEW_LOG 有本轮记录（R-30）
- [x] CHANGE_CONTROL +CC-19 已登记

**最后更新**：2026-04-08（P1-6 实施完成）

---

## 十三、P1-6a：fetch 层 dry-run 可解释性增强

**对应 Phase 3 任务**：P1-6a fetch 层连通性与真实刷新能力核验

**问题背景**：
run-analyst-fetch.sh --check 执行后，dry-run 输出"共 0 个来源待抓取"，但实际上从 profile 发现了 97 个 URL。输出具有误导性，导致运营编辑者无法判断"是真的没有新数据"还是"抓取被跳过"。

**根本原因**：
dry-run 跳过实际抓取逻辑（continue），不执行 `fetch_url`，因此 `is_too_old` 年份过滤不生效，导致 results 保持为空数组。"0来源"是 dry-run 跳过抓取的结果，不是真的没有数据。

**P1-6a 实施结果**：
- `05_工具脚本/fetch_analyst_articles.py`：增强 dry-run 输出结尾
  - 旧：`[DRY RUN] 共 0 个来源待抓取`（误导）
  - 新：解释已跳过实际抓取 + 年份过滤只在实际抓取时生效 + 引导执行正式 fetch

**当前 fetch 结果"可解释性"状态**：
- dry-run 跳过抓取（无实质数据）：✅ 可区分（"已跳过实际抓取"）
- 网络/环境不可达：❌ 无特殊提示（需网络层检查）
- 有数据但被年份过滤：⚠️ 需真实 fetch 才可知（固有限制，不在 P1-6a 范围）

**P1-6a 验收标准**：
- [x] dry-run 输出已增强（从"0来源"变为"已跳过实际抓取"）
- [x] 年份过滤限制已在输出中说明
- [x] 引导运营编辑者执行正式 fetch
- [x] REVIEW_LOG 有本轮记录（R-31）
- [x] CHANGE_CONTROL +CC-20 已登记

**最后更新**：2026-04-08（P1-6a 实施完成）
