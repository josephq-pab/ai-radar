# PILOT_DEMO_SCRIPT.md — 试点展示口径与最小演示脚本

> 文档版本：v1.0（初建）
> 建立日期：2026-04-07
> 对应阶段：Phase 3 — 试点运营化 / MVP 闭环
> 依据：PHASE3_CLOSURE_REPORT.md / PHASE3_BASELINE.md

---

## 一、演示目标

向内部干系人演示 AI雷达站 MVP 的**最小可用闭环**，证明：

1. 系统可以采集分析师观点（抓取层）
2. 观点可以经过分层处理（raw → usable → report-ready）
3. 运营编辑者可以对观点进行确认/驳回/跟进（review 层）
4. 每条记录的状态变化可追溯（review queue 状态字段）
5. 整个流程有文档记录（review log）

**本演示不证明**：
- 系统已具备完整运营能力
- 状态可以持久保存（重新 build 后会重置）
- 评分规则已完善（OI-03 存在）
- 来源分类已正式确定（SOURCE_GOVERNANCE DRAFT v0.9 是候选初稿）

---

## 二、演示对象

| 对象 | 关注点 | 演示重点 |
|------|-------|---------|
| 业务决策层 | 系统能做什么，边界在哪里 | 全链路演示 + 明确边界说明 |
| 运营执行层 | 如何使用系统 | review queue 操作演示 |
| 技术评估层 | 架构是否可扩展 | 分层结构 + 状态字段设计 |

---

## 三、演示前提

在开始演示前，必须确认以下条件已满足：

| # | 前提条件 | 确认方式 |
|---|---------|---------|
| 1 | 8787 前端可访问 | 浏览器打开 http://47.112.211.98:8787/index.html |
| 2 | analyst_opinions_raw.json 非空 | 确认 04_数据与规则/processed/analyst_opinions_raw.json 存在且有数据 |
| 3 | analyst-review-queue.json 含状态字段 | 确认 reviewStatus + trackingStatus 字段存在 |
| 4 | 最近一次 build 未超过 24 小时 | 检查文件修改时间，确认数据 freshness |
| 5 | review queue 处于初始状态（pending） | 确认 analyst-72873eb4 的 reviewStatus=candidate（若已被修改，需先 reset）|

**演示前检查清单**：
- [ ] 8787 可访问
- [ ] analyst-review-queue.json 已 reset 到初始状态（pending/candidate）
- [ ] 准备好修改用的文本编辑器或脚本
- [ ] REVIEW_LOG R-15 打印件或屏幕投影准备

---

## 四、演示步骤（5步）

### Step 1：展示抓取结果（raw 层）

**操作**：打开 analyst_opinions_raw.json（路径：04_数据与规则/processed/）

**展示内容**：
- 共 79 条原始抓取记录
- 每条含：title / author / published_date / source / url / qualityTier / relevanceScore

**说清**：
> "这是原始抓取层，共79条记录，来自6个可抓取来源（薛洪言、苏商银行研究院等）。其中50条因发表于2024年前被标记为 SKIP_OLD，不进入后续评分。"

**不能说**：
- "这些数据是完整最新的"（实际有50条被过滤）
- "所有来源都可以抓取"（微信公号平台壁垒不可解）

---

### Step 2：展示分层输出（usable 层 + report-ready 层）

**操作**：展示 analyst_opinions.json（29条）和 analyst-review-queue.json（5条）

**展示内容**：
- analyst_opinions.json：29条 usable 记录（VALID×25 + DEGRADED×4）
- analyst-review-queue.json：5条 report-ready 记录，每条含 confirmLevel（P1/P2/P3）

**说清**：
> "经过评分过滤后，79条→29条 usable。其中 relevanceScore ≥ 0.4 的有29条。再经过 top-k=5 排序，选出综合评分最高的5条进入 report-ready 层。每条有 confirmLevel：P1是最高优先级进入周报，P2是参考，P3是低优先级。"

**不能说**：
- "这5条是唯一相关的内容"（实际29条 relevance≥0.4，5条是 top-k 截断结果）
- "confirmLevel 是人工审核过的"（OI-04：当前 confirmLevel 是规则映射，非人工验证）

---

### Step 3：展示 review queue 的初始状态

**操作**：展示 analyst-review-queue.json，重点展示 analyst-72873eb4

**展示内容**：
- 5条记录的 reviewStatus=pending，trackingStatus=candidate
- analyst-72873eb4（薛洪言，护城河）：reviewStatus=pending / trackingStatus=candidate

**说清**：
> "这是 review queue，所有 report-ready 记录初始状态都是 pending/candidate。运营编辑者需要对每条进行确认（confirmed）或驳回（rejected），并设置跟进状态（follow_up/closed）。"

---

### Step 4：演示一次状态变更

**操作**：
1. 修改 analyst-72873eb4 的 reviewStatus → "confirmed"，trackingStatus → "follow_up"
2. 保存文件
3. 重新读取 analyst-review-queue.json，确认字段已变化

**展示内容**：
- 修改前：reviewStatus=pending / trackingStatus=candidate
- 修改后：reviewStatus=confirmed / trackingStatus=follow_up

**说清**：
> "运营编辑者确认薛洪言这篇文章可以作为周报输入，将状态改为 confirmed+follow_up。修改后重读 JSON，状态已更新。"

**重要边界说明（必须说清）**：
> "注意：这个状态修改是在 JSON 文件层面操作的。重新运行 build_analyst_opinions.py 后，所有 reviewStatus 会重置为 pending，trackingStatus 重置为 candidate。状态持久化能力不在 Phase 3 MVP 范围内，将在 P1-1 建立追踪表后解决。"

**不能说**：
- "状态会被永久保存"（实际会重置）
- "这是一个完整的运营后台"（当前是 MVP，最小可演示闭环）

---

### Step 5：展示 REVIEW_LOG 留痕

**操作**：展示 REVIEW_LOG.md R-15 条目

**展示内容**：
- R-15 记录了 M4b 演示全过程（时间、修改记录、重读确认）
- 包含修改前后的状态快照

**说清**：
> "所有 review 操作都会记录在 REVIEW_LOG 中，包含时间、操作人（当前为 AI雷达站 agent）、修改前后状态。这为未来复盘和审计提供了依据。"

---

## 五、每一步的风险点与应对

| Step | 潜在风险 | 应对 |
|------|---------|------|
| Step 1 | 演示中被问"为什么有这么多被过滤" | 说明 SKIP_OLD 过滤规则（2024年前旧文） |
| Step 2 | 演示中被问"为什么选这5条" | 说明 top-k=5 排序逻辑；连平排名第6 被截断是 OI-03，已记录 |
| Step 2 | 被问 confirmLevel 准不准 | 诚实说明 OI-04（当前是规则映射，P1-1 后引入人工对比） |
| Step 4 | 被问"状态保存了吗" | 主动说明重置边界（D-07），不回避 |
| Step 4 | 修改后 JSON 没变化 | 检查文件路径是否正确；确认 build 未在修改后自动运行 |

---

## 六、常见问答口径

### Q1：这个系统和直接看文章有什么区别？

> "核心区别是分层和确认机制。原始文章进来后，经过 relevanceScore 评分 + top-k 排序 + confirmLevel 分级，运营编辑者可以对每条进行确认/驳回/跟进，最终形成有管理痕迹的周报输入。不是搜索，是管理。"

### Q2：状态修改后关闭系统，再打开还有吗？

> "当前 Phase 3 MVP 中，JSON 文件修改后重启系统状态仍然保留（文件系统层面持久）。但重新运行 build_analyst_opinions.py 后，所有 reviewStatus/trackingStatus 会重置为初始值。P1-1 会建立独立的状态存储机制解决这个问题。"

### Q3：为什么连平的文章没有进入 top-5？

> "连平的综合分是0.865，排名第6，与第5名（0.880）差0.015。top-k=5 排序受来源先验权重影响（OI-03 已记录），薛洪言的来源权重较高导致其低相关性文章仍排在连平之前。这是评分规则的已知问题，P1-1 sprint 会优化。"

### Q4：Gate A 阻断是什么？

> "Gate A 是贷款利率数据的外部依赖。2026-03 的贷款利率 Excel 文件尚未到位，前端利率数据只能显示到 2025-12。这是外部因素，系统层无解，已在文档中明确标注。"

### Q5：为什么只有 6 个来源，另一个去哪了？

> "微信公众号方案因平台反爬壁垒不可解（ED-02）。已用苏商银行研究院替代，4个分析师 profile 来源可正常抓取。总计13个来源，6个当前有数据，其余待 P1-2 review 后处理。"

---

## 七、演示边界声明（演示前必须说明）

在演示开始前，**必须主动声明**以下边界，不得在演示结束后被对方发现时再解释：

1. **数据新鲜度**：当前数据为 2026-04-07 快照，非实时数据
2. **状态重置**：review queue 状态在重新 build 后会重置，不支持高频换手
3. **评分验证**：confirmLevel 为规则映射，非人工验证；OI-03 存在，top-5 可能不是最优解
4. **来源状态**：SOURCE_GOVERNANCE_DRAFT 为候选初稿，来源分类尚未正式 review
5. **Gate A**：贷款利率数据只能显示到 2025-12（2026-03 数据未到位）

---

## 八、演示后建议动作

| 动作 | 目的 | 责任方 |
|------|------|--------|
| 将 analyst-review-queue.json 手动备份 | 防止下次 build 前丢失当前 review 状态 | 运营编辑者 |
| 记录演示日期和参与者 | 为 P1-1 追踪表建立提供输入 | AI雷达站 agent |
| 确认是否需要 P1-1 优先推进 | 干系人明确状态持久化需求后 | 用户决策 |

---

**脚本编制人**：AI雷达站 agent
**建立日期**：2026-04-07
**适用阶段**：Phase 3 试点展示
**有效期至**：P1-1 追踪表建立前（状态持久化问题解决后，本脚本需更新）
