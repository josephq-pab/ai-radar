# PHASE3_CLOSURE_REPORT.md — Phase 3 完成报告

> 文档版本：v1.0（初建）
> 建立日期：2026-04-07
> 对应阶段：Phase 3 — 试点运营化 / MVP 闭环
> 编写依据：PHASE3_STATUS.md v1.3 / PHASE3_TASK_PACKAGE.md v1.3 / REVIEW_LOG.md v1.2 / DECISION_LOG.md v1.3 / CHANGE_CONTROL.md v1.1

---

## 一、阶段目标回顾

Phase 3 的原始目标：

> 让系统具备**可管理、可确认、可跟进、可复盘、可按周期运行、可演示**的最小闭环。

五项核心推进点：
1. 输出分层（raw → reviewed → report-ready）
2. 确认项分级（confirmable / referenceable / reportable）
3. 周期管理（日/周/月运行机制）
4. 角色视图（不同角色看什么、做什么的最小边界）
5. 数据源轻管理（来源分类、启用/停用规则）

---

## 二、阶段完成情况

### 2.1 P0 任务（全部 ✅）

| 任务 | 名称 | 结论 | 完成日期 |
|------|------|------|---------|
| P0-1 | 前端页面试点运行验证 | ✅ 完成 | 2026-04-07 |
| P0-2 | 分析师观点输出分层固化 | ✅ 完成 | 2026-04-07 |
| P0-3 | 周期运行脚本固化 | ✅ 完成 | 2026-04-07 |

### 2.2 里程碑（全部 ✅）

| 里程碑 | 定义 | 验收方式 | 结论 | 完成日期 |
|--------|------|---------|------|---------|
| M1 | 运行入口稳定 | 8787 可访问，run-pipeline.sh 路径正确 | ✅ | 2026-04-07 |
| M2 | 分析师抓取可周期运行 | fetch_analyst_articles.py 无报错，输出非空 | ✅ | 2026-04-07 |
| M3 | 文档与状态对齐 | 10 份核心文档与实际状态一致 | ✅ | 2026-04-07 |
| M4a | 试点结果可展示 | 页面可访问 + 数据非空 + freshness 可确认 | ✅ | 2026-04-07 |
| M4b | 试点流程可演示 | reviewStatus+trackingStatus 字段落地，演示一次状态变更 | ✅ | 2026-04-07 |

**里程碑通过口径**：M1~M4b 全部通过 M3 验证（M3 确认文档与状态一致）。

### 2.3 P1 任务（本阶段不要求完成）

| 任务 | 名称 | 状态 |
|------|------|------|
| P1-1 | 试点运行状态追踪表 | ⏳ 待执行 |
| P1-2 | 分析师来源有效性 review | ⏳ 待执行 |
| P1-3 | 确认项分级规则文档化 | ⏳ 待执行 |

---

## 三、已完成能力清单

以下能力经 M4a/M4b 验证，属实：

### 3.1 数据采集层
- 分析师文章抓取可成功运行（6/7 来源成功，1 个来源平台壁垒）
- 数据写入 04_数据与规则/processed/，路径统一
- 抓取记录含 title / author / published_date / source / url / qualityTier / relevanceScore / isReferenceable

### 3.2 分层输出层
- **raw 层**：analyst_opinions_raw.json（79条，抓取原始结果）
- **usable 层**：analyst_opinions.json（29条 = VALID×25 + DEGRADED×4，过滤 SKIP_OLD）
- **report-ready 层**：analyst-review-queue.json（5条，含 confirmLevel P1/P2/P3）
- **四层结构**：raw → scored → usable → report-ready，每层转化逻辑可解释

### 3.3 状态字段层
- analyst-review-queue.json 含 reviewStatus（pending/confirmed/rejected）
- analyst-review-queue.json 含 trackingStatus（candidate/pending/follow_up/closed）
- reviewStatus / trackingStatus 支持人工修改并可重读确认

### 3.4 文档与治理层
- 10 份核心文档与实际代码/产物状态一致（M3 验证通过）
- CHANGE_CONTROL 有硬化规则（变更先记录才能进入任务包）
- DECISION_LOG 记录了 D-01~D-07 共 7 项关键决策
- REVIEW_LOG 记录了 R-01~R-15 共 15 轮 review（含 6 轮机制失灵的自检校正）

---

## 四、关键证据

| 证据 | 位置 | 验证方式 |
|------|------|---------|
| 8787 前端可访问 | http://47.112.211.98:8787/index.html | 人工访问 |
| analyst_opinions_raw.json 非空 | 04_数据与规则/processed/ | 文件存在，79条 |
| analyst-review-queue.json 有状态字段 | 04_数据与规则/processed/ | reviewStatus+trackingStatus 存在 |
| M4b 演示记录 | REVIEW_LOG R-15 | 状态变更+重读确认 |
| smoke_test 通过 | 05_工具脚本/smoke_test.py | 38/38 PASS |
| 路径统一修正记录 | DECISION_LOG D-06 | 3处路径已修正 |
| SKIP_OLD 过滤修复 | build_analyst_opinions.py | 50条2024年前旧文正确剔除 |
| confirmLevel 注入 | build_analyst_opinions.py | P1×4/P2×1 |

---

## 五、当前 MVP 能力边界

### 5.1 当前能支持的
- 人工触发一次抓取，产生 raw / usable / report-ready 三层输出
- 前端页面展示最新一次抓取结果（8787）
- reviewStatus / trackingStatus 字段在内存中修改并重读确认（M4b 演示通过）
- 周报口径可给出（"29条 usable，其中5条 top-k 进入周报"）
- 运营编辑者可看到 review queue 并知道下一步操作

### 5.2 当前不能支持的（已知边界，不属于 Phase 3 缺陷）
- **状态持久化**：重新运行 build 后，所有 reviewStatus 重置为 pending，trackingStatus 重置为 candidate/pending
- **自动周期运行**：当前依赖人工触发，无 cron 化
- **微信公号抓取**：平台壁垒不可解
- **Gate A 数据**：2026-03 贷款利率数据未到位
- **历史运行日志**：无独立日志文件（P1-1 待建）
- **来源有效性 review**：SOURCE_GOVERNANCE_DRAFT 为候选初稿，非正式版本

---

## 六、遗留问题清单

### 6.1 外部依赖（系统层无解）
| 编号 | 问题 | 影响 |
|------|------|------|
| ED-01 | Gate A — 2026-03 贷款利率 Excel 未到位 | 利率数据只能标注至 2025-12 |
| ED-02 | wechatsogou pip 安装超时 | 微信公号抓取方案不可推进 |

### 6.2 非阻断型内部问题
| 编号 | 问题 | 影响 | 建议处理时机 |
|------|------|------|------------|
| OI-01 | 顾慧君/王锟来源 0 篇（2024年前旧文） | 两个新来源对当前维度贡献为 0 | P1-2 review |
| OI-03 | 来源先验权重过重，连平等被挤出 top-5 | 周报覆盖度可能不足 | P1-1 评分优化 sprint |
| OI-04 | confirmLevel 为规则映射，非人工验证 | P1/P2 分级可能存在系统性偏差 | P1-1 追踪表建立后 |

### 6.3 已知遗留边界（不得误写为"已解决"）
- reviewStatus/trackingStatus 在重新 build 后会**被重置**，不是持久化状态
- analyst_opinions.json 的筛选顺序依赖来源先验权重（OI-03），存在评分偏颇
- confirmLevel 的 P1/P2/P3 阈值（0.75/0.60）无人工验证（OI-04）
- SOURCE_GOVERNANCE_DRAFT v0.9 是候选初稿，不是正式版本

---

## 七、是否建议进入试点

**建议：可以进入小范围试点准备，但必须明确以下口径**。

### 7.1 可支持的试点行为
- 用真实数据向内部干系人演示完整流程（抓取→分层→review queue→confirmLevel→状态变更）
- 用 M4b 演示证明"运营编辑者可以确认/驳回/跟进"的能力存在
- 积累2~3轮运行数据，为 P1-1 追踪表提供输入

### 7.2 不得对外声称的
- "系统已具备完整运营能力"——当前是 MVP 最小闭环
- "状态会持久保存"——重新 build 后会重置
- "评分规则已完善"——OI-03 存在，不适合对外表述为"规则经过验证"
- "来源分类是正式的"——SOURCE_GOVERNANCE DRAFT v0.9 是候选初稿

### 7.3 试点期间注意事项
- 每次重新 build 前，review queue 状态需手动导出留存（或接受重置）
- 建议在试点期间记录每次运行的 review queue JSON，作为人工备份
- Gate A 数据未到位期间，利率相关内容应注明数据截止月份

---

## 八、对 P1 的建议

### 8.1 建议 P1-1 优先的原因
- P1-1（状态持久化/追踪表）是当前 MVP 最明显的体验断点
- 重新 build 后状态重置的问题，会在第一次真实使用时立即暴露，严重损害体验可信度
- P1-1 建好后，P1-2/P1-3 的结果才有地方沉淀

### 8.2 P1-1 成功后可解锁的
- review queue 状态不因 build 重置
- 历史运行记录可查询（fetch-run-log）
- confirmLevel 阈值可与实际人工判断对比（支持 OI-04 修正）

### 8.3 试点期间同步可推进的（不阻断）
- P1-2（来源有效性 review）：用当前已有数据（79条）进行一次快速 review，不依赖新抓取
- P1-3（confirmLevel 规则文档化）：在 P1-1 追踪表运行1~2轮后，基于实际数据补充

---

## 九、本报告与其他 Phase 3 文档的关系

| 文档 | 与本报告的关系 |
|------|-------------|
| PHASE3_STATUS.md | 提供里程碑和当前状态的实时参考 |
| PHASE3_TASK_PACKAGE.md | 提供任务边界和验收口径 |
| PHASE3_BASELINE.md（本轮新建） | 冻结本阶段交付物基线，后续变更不得回写篡改 |
| PILOT_DEMO_SCRIPT.md（本轮新建） | 提供试点展示口径和演示步骤 |
| P1_CANDIDATES.md（本轮新建） | 提供 P1 任务优先级建议 |
| REVIEW_LOG.md | 提供 15 轮 review 的完整记录 |
| DECISION_LOG.md | 提供 7 项关键决策的上下文 |
| CHANGE_CONTROL.md | 提供 10 项边界决策和硬化规则 |
| OPEN_ISSUES.md | 提供 4 个非阻断型问题和 2 个外部依赖的详细描述 |

---

**报告编制人**：AI雷达站 agent
**报告日期**：2026-04-07
**Phase 3 状态**：✅ 收口完成，可进入试点准备
