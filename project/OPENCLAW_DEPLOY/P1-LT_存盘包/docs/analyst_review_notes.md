# analyst_review_notes.md — 来源有效性 Review 结论文档

> 文档版本：v1.0（初建）
> 建立日期：2026-04-07
> 对应阶段：P1-2 实施
> 样本说明：本轮数据为单轮抓取结果（2026-04-07），结论为**试行版/阶段性建议**，建议在2~3轮试点数据后复核

---

## 结论口径说明

本文档为来源有效性 review 结论文档。结论分为五类：

| 结论枚举 | 含义 | 配置动作 |
|---------|------|---------|
| keep | 当前有效，维持 active | 建议保持 active |
| observe | 继续观察，有待更多数据 | 建议继续观察，暂不调整 |
| pending-check | 需人工核实后才能判断 | 建议人工确认后再考虑配置变更 |
| downgrade-candidate | 建议降级 | 建议人工确认后再考虑降级 |
| quarantine-candidate | 建议观察或暂停 | 建议人工确认后再暂停 |

**重要**：所有"配置建议"均为**人工决策参考**，不是自动生效。analyst_sources.json 不在本轮自动修改。

---

## 来源结论

---

### 来源 1：薛洪言

- **sourceId**：analyst-deposit-002
- **当前结论**：**keep**
- **关键证据**：
  - usable = 15/15（100%）
  - referenceable = 12/15（80%）
  - enterReport = 4（全部5条 top-5 中占4条）
  - latestYear = 2025（最新）
- **风险点**：
  - top-5 中占比过高（4/5），导致其他来源被截断（OI-03）
  - 结论不因本 review 而改变；OI-03 评分权重优化是独立问题
- **配置建议**：**建议保持 active**
- **是否为最终结论**：❌ 否，本结论基于单轮数据，建议2~3轮后复核

---

### 来源 2：周茂华

- **sourceId**：analyst-deposit-005
- **当前结论**：**keep**
- **关键证据**：
  - usable = 2/2（100%）
  - referenceable = 2/2（100%）
  - enterReport = 1（review_queue 中1条）
  - latestYear = 2026
- **风险点**：
  - 数据量偏少（仅2条），当前周期代表性有限
- **配置建议**：**建议保持 active**，每轮观察数据量变化
- **是否为最终结论**：❌ 否，本结论基于单轮数据，建议2~3轮后复核

---

### 来源 3：连平

- **sourceId**：analyst-deposit-004
- **当前结论**：**observe**
- **关键证据**：
  - usable = 2/2（100%），referenceable = 2/2（100%）
  - 综合分 0.86（本轮最高之一），但未进入 top-5（被薛洪言截断，OI-03问题）
  - latestYear = 2026
- **降级原因**：无（本来源质量正常）
- **为何不直接 keep**：数据量少（2条），当前样本不确定性强
- **配置建议**：**建议继续观察**，保持 active
- **是否为最终结论**：❌ 否，本结论基于单轮数据，建议2~3轮后复核

---

### 来源 4：娄飞鹏

- **sourceId**：analyst-deposit-003
- **当前结论**：**observe**
- **关键证据**：
  - usable = 1/1（100%），referenceable = 1/1（100%）
  - 数据量极少（仅1条 ops）
  - latestYear = 2026
- **风险点**：
  - 数据量过少，无法判断稳定性
- **配置建议**：**建议继续观察**，保持 active
- **是否为最终结论**：❌ 否，本结论基于单轮数据，建议2~3轮后复核

---

### 来源 5：付一夫

- **sourceId**：analyst-deposit-007
- **当前结论**：**observe**
- **关键证据**：
  - usable = 9/9（100%），referenceable = 8/9（89%），VALID = 8
  - raw 全为 2023-2024 年文章（新鲜）
  - enterReport = 0（被薛洪言截断，非来源质量问题）
- **为何 0 enterReport**：
  - 原因：top-k=5 排序截断（薛洪言4条 + 周茂华1条），付一夫的高分文章未能入选
  - 不是来源质量差，而是 OI-03 来源权重过重导致的排序问题
  - **不得将此来源标记为低效来源**
- **配置建议**：**建议继续观察**，保持 active，关注后续周期是否积累更多 enterReport
- **是否为最终结论**：❌ 否，本结论基于单轮数据，建议2~3轮后复核

---

### 来源 6：顾慧君

- **sourceId**：analyst-deposit-006
- **当前结论**：**pending-check**
- **关键证据**：
  - rawTotal = 20，但 opsTotal = 0（全被 min_year=2024 过滤）
  - latestYear = 2022（全部在2024年前）
  - analyst_sources.json notes 记录：profile 页有20篇以上文章
- **0 usable 原因**：**min_year=2024 规则过滤**，不是来源质量差
- **待核实项**：
  1. profile 页（https://sif.suning.com/author/detail/8009）是否有 2024 年后新文章？
  2. 若有新文章但未被抓取，是抓取逻辑问题还是网站更新问题？
  3. 若确认无2024年后文章，实际停更时间有多长？
- **配置建议**：**建议人工确认来源实际情况**，再考虑 inactive 或降级为参考源
- **是否为最终结论**：❌ 否，当前为待核实状态

---

### 来源 7：王锟

- **sourceId**：analyst-deposit-008
- **当前结论**：**pending-check**
- **关键证据**：
  - rawTotal = 13，但 opsTotal = 0（全被 min_year=2024 过滤）
  - latestYear = 2019（全部在2024年前）
  - analyst_sources.json notes 记录：profile 页有13篇文章
- **0 usable 原因**：**min_year=2024 规则过滤**，不是来源质量差
- **待核实项**：
  1. profile 页（https://sif.suning.com/author/detail/8022）是否有 2024 年后新文章？
  2. 若确认无2024年后文章，实际停更时间已超5年
- **配置建议**：**建议人工确认来源实际情况**，若确认长期无更新，建议降级为参考源或 inactive
- **是否为最终结论**：❌ 否，当前为待核实状态

---

### 来源 8~13（待核实来源组）

以下6个来源本轮 rawTotal = 0，在抓取层未触达：

| sourceId | 姓名 | 待核实项 |
|---------|------|---------|
| analyst-deposit-001 | 董希淼 | active=False（已在 analyst_sources.json 中标注），无需操作 |
| analyst-loan-001 | 温彬 | 抓取0条，需确认：平台壁垒 / URL变更 / 实际无更新 |
| analyst-loan-002 | 曾刚 | 同上 |
| analyst-overall-001 | 朱太辉 | 同上 |
| analyst-overall-002 | 孙扬 | 同上 |
| analyst-overall-003 | 杜娟 | 同上 |

**配置建议**：**建议优先核实温彬/曾刚/朱太辉/孙扬/杜娟的实际URL可访问性**，确认为平台壁垒还是来源本身问题

---

## 与 analyst_sources.json 的关系

- **不自动修改**：analyst_sources.json 在本轮不自动修改
- **配置建议仅作参考**：本文档的配置建议是人工决策参考，不是自动生效
- **若未来执行配置变更**：需单独进入下一轮实施与 review

---

## 与 SOURCE_GOVERNANCE_DRAFT 的关系

- SOURCE_GOVERNANCE_DRAFT 仍是候选初稿（v0.9）
- 本轮产物（analyst_review_matrix.md + analyst_review_notes.md）为其后续升级提供证据基础
- **不把 v0.9 候选初稿直接说成正式版**
- 若要升级为正式版，需在本文档结论基础上，经人工确认后再更新

---

## 本轮结论执行边界

- ✅ 已有：analyst_review_matrix.md（证据矩阵）
- ✅ 已有：analyst_review_notes.md（结论文档）
- ❌ 未执行：analyst_sources.json 自动修改（本轮不做）
- ❌ 未执行：SOURCE_GOVERNANCE_DRAFT v0.9 升版（本轮不做）
- ❌ 未执行：多轮趋势分析（本轮不做）
