# CONTENT_STRUCTURE_DRAFT.md — Phase 3 内容结构草案

> 文档版本：v1.1（本次更新：四层产物映射，基于 P0-2 实施结果）
> 版本历史：
> - v1.0（2026-04-07）：初建，定义三层结构和 P1/P2/P3 标准
> - v1.1（2026-04-07）：四层产物映射落地（P0-2 实施完成后的实际对应关系）

---

## 输出分层原则

1. **raw 层**：原始抓取结果，不做质量判断，保留全部字段
2. **reviewed 层**：经过 confirmable 过滤和 review 标记的中间层
3. **report-ready 层**：可直接引入报告的高优先级观点

---

## 首页默认展示内容（第一层）

**关键结论层**

- 数据 freshness 标注（"数据截至 XXX 年 XX 月"）
- 本轮抓取汇总：总条数 / 成功 / 跳过 / 失败
- 高优先级确认项（P1）摘要（≤3条）
- 分析师来源列表（活跃度标注）

---

## 折叠内容（第二层）

**高优先级确认层**

- 所有 P1 确认项：标题 / 作者 / 发布时间 / 摘要 / 判断依据
- 所有 P2 确认项：标题 / 作者 / 发布时间 / 摘要

---

## 确认项分级规则

### P1 — 高优先级确认项

**定义**：有明确数据/事件支撑，分析师背景可信，逻辑清晰，可直接引用。

**判断标准（须同时满足）**：
- 有具体数据或事件引用（数字 / 百分比 / 机构名称 / 时间）
- 作者有明确机构背景（研究所/银行/高校）
- 与当前维度（对公存款/贷款）直接相关
- 发布于近 3 个月内

**默认展示策略**：首页默认展示，上下文完整

---

### P2 — 中优先级确认项

**定义**：观点有价值但引用支撑不够强，或时效性略弱。

**判断标准（满足以下任一）**：
- 有逻辑推断但缺乏具体数据
- 作者机构背景一般
- 与当前维度间接相关
- 发布于 3~6 个月前

**默认展示策略**：折叠展示，需要时展开

---

### P3 — 参考项

**定义**：信息来源单一、推断性质强或时效性已过。

**判断标准（满足以下任一）**：
- 无具体数据支撑
- 无明确作者机构
- 与当前维度关联弱
- 发布于 6 个月前

**默认展示策略**：默认折叠，仅在有明确需求时调取

---

## 跟进行动呈现规则

- 每条 P1/P2 确认项，附"跟进状态"标签
- 状态流转：待确认 → 已确认 → 跟进中 → 已关闭 / 暂缓

---

## 证据底稿呈现规则

- analyst_opinions_raw.json（raw 层）作为证据底稿
- 运营编辑者有权限查阅
- 报告阅读者默认不直接访问，仅通过 reviewed 层引用

---

## 三层 JSON 字段对照

| 字段 | raw 层 | reviewed 层 | report-ready 层 |
|------|--------|------------|----------------|
| articleTitle | ✅ | ✅ | ✅ |
| analystName | ✅ | ✅ | ✅ |
| publishedAt | ✅ | ✅ | ✅ |
| sourceUrl | ✅ | ✅ | ✅ |
| content | ✅ | ✅（摘要） | ✅（摘要） |
| summary | — | ✅ | ✅ |
| keyViewpoints | ✅ | ✅ | ✅ |
| evidenceSnippets | ✅ | ✅ | ✅ |
| confirmStatus | — | ✅ | ✅ |
| confirmLevel | — | —（仅report-ready层） | ✅ P1/P2/P3 |
| reviewDecision | — | ✅ | ✅ |
| lastReviewedAt | — | ✅ | ✅ |

---

## 四层结构实际产物映射（P0-2 实施后）

> 以下为 P0-2 实施后的实际对应关系，基于 analyst_opinions_raw.json（79条）实际运行结果。

| 层级 | 定义 | 对应实际产物 | 当前状态 |
|------|------|------------|---------|
| 第一层（关键结论层） | 首页默认展示，数据freshness标注 | analyst_opinions.json 的 summary + analyst-review-queue.json 的 reportable 条目摘要 | ✅ 落地（5条进入周报，freshness=2026-03-31） |
| 第二层（高优先级确认层） | P1/P2 确认项，默认展开 | analyst-review-queue.json 的 items（含 confirmLevel） | ✅ 落地（当前 4 P1 + 1 P2） |
| 第三层（跟进行动层） | tracking 候选，有具体跟进事项 | analyst-review-queue.json 的 trackingCandidate=true 条目 | ✅ 最小可行（当前 5 条均为 tracking=True） |
| 第四层（证据/底稿层） | 原始记录，运营编辑者可查阅 | analyst_opinions_raw.json（79条原始记录） | ✅ 落地（50条SKIP_OLD+29条usable） |

**当前 confirmLevel 规则（P0-2 MVP 最小版）**：
- P1：VALID + 综合分 ≥ 0.75
- P2：VALID + 综合分 ≥ 0.60，或 DEGRADED + 综合分 ≥ 0.50
- P3：其余（当前无 P3 进入周报）

**已知不足（记录于 OPEN_ISSUES）**：
- confirmLevel 为规则映射，非人工分级
- 来源多样性未纳入评分，导致部分优质来源（连平）文章被挤压
- tracking 仅为候选标记，无独立跟追表（P1-1 任务待建立）

---

## 当前阶段暂不支持的呈现方式

| 方式 | 原因 |
|------|------|
| 在线实时确认操作界面 | review 流程尚未系统化（需 P1-1 追踪表建立后） |
| 多级确认项（>3级） | P1/P2/P3 分级已足够，过于复杂不利于判断 |
| 自动分级 | 需人工 review 积累足够样本后才能训练规则 |
| 版本对比视图 | 超出 MVP 范围 |

---

## 三层 JSON 字段对照

| 字段 | raw 层 | reviewed 层 | report-ready 层 |
|------|--------|------------|----------------|
| articleTitle | ✅ | ✅ | ✅ |
| analystName | ✅ | ✅ | ✅ |
| publishedAt | ✅ | ✅ | ✅ |
| sourceUrl | ✅ | ✅ | ✅ |
| content | ✅ | ✅（摘要） | ✅（摘要） |
| summary | — | ✅ | ✅ |
| keyViewpoints | ✅ | ✅ | ✅ |
| evidenceSnippets | ✅ | ✅ | ✅ |
| confirmStatus | — | ✅ | ✅ |
| confirmLevel | — | P1/P2/P3 | P1 |
| reviewDecision | — | ✅ | ✅ |
| lastReviewedAt | — | ✅ | ✅ |
