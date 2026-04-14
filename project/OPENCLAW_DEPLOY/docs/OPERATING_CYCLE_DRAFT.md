# OPERATING_CYCLE_DRAFT.md — Phase 3 周期运行草案

> 文档版本：v1.1（本次更新：reviewStatus / trackingStatus 字段定义及最小流转规则）
> 版本历史：
> - v1.0（2026-04-07）：初建
> - v1.1（2026-04-07）：reviewStatus / trackingStatus 定义（M4b 最小闭环演示所需字段）

---

## 周期管理目标

让系统具备**可定义、可执行、可追踪**的周期性运行能力，不依赖人工实时监控。

---

## 日度机制

**当前阶段**：暂不启用自动日度运行。

| 字段 | 内容 |
|------|------|
| 周期名称 | 日度检查 |
| 主要目标 | 确认系统可用性 |
| 主要输入 | — |
| 主要输出 | — |
| 人工参与点 | 无（被动触发告警） |
| review 点 | — |
| 状态更新要求 | — |

---

## 周度机制（核心周期）

| 字段 | 内容 |
|------|------|
| 周期名称 | 周度抓取与 review |
| 主要目标 | 保持数据 freshness，支持周报引用 |
| 主要输入 | analyst_sources.json；fetch_analyst_articles.py |
| 主要输出 | analyst_opinions_raw.json（新增记录）；fetch-run-log.json |
| 人工参与点 | review confirmable items（P1/P2 分类） |
| review 点 | 每周一09:00 执行抓取；review 结果当天内确认 |
| 状态更新要求 | raw JSON 覆盖追加；review 状态写入 analyst_opinions.json |

**运行命令**（写入 RUNBOOK.md）：
```bash
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本
OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY \
/tmp/py39env/bin/python fetch_analyst_articles.py --dimension 对公存款
```

**失败处理规则**：
- 单个来源失败：记录到 fetch-run-log.json，继续其他来源，不中断全流程
- 全局失败（>50% 来源失败）：输出告警，人工介入检查
- 超时处理：单 URL 超时 30s 跳过，不重试

---

## 月度机制

| 字段 | 内容 |
|------|------|
| 周期名称 | 月度数据 review 与归档 |
| 主要目标 | 归档月度数据，评估来源有效性，更新 analyst_sources.json |
| 主要输入 | 月度 fetch-run-log.json；月度 analyst_opinions_raw.json |
| 主要输出 | analyst_review_notes.md（月度 review 结论）；无效来源列表 |
| 人工参与点 | P1-2 review（来源有效性）；数据新鲜度确认 |
| review 点 | 每月最后一周执行 |
| 状态更新要求 | analyst_sources.json 更新（如有来源变更） |

---

## 事项状态流转

| 状态 | 说明 | 触发动作 |
|------|------|---------|
| 待确认 | raw 层新抓入，等待 review | 新抓取完成 |
| 已确认 | review 通过，标记为 confirmable | 运营编辑者确认 |
| 跟进中 | 确认后需要进一步验证或等待数据 | 人工标记 |
| 已关闭 | 已被报告引用或确认过期 | 人工关闭 |
| 暂缓 | 因时效/数据问题暂停跟进 | 人工标记 |
| 失效 | 被 reject 或确认无法使用 | 人工 reject |

---

## reviewStatus / trackingStatus 字段定义（M4b 最小闭环演示）

> 本节定义 analyst-review-queue.json 中用于演示 M4b 流程的状态字段。
> **注意**：重新运行 build_analyst_opinions.py 会将所有记录重置为初始状态（pending/candidate），不具备持久化能力。持久化机制不在 Phase 3 MVP 范围内。

### reviewStatus（确认操作状态）

| 取值 | 含义 | 初始值 |
|------|------|--------|
| pending | 等待人工 review | ✅ 默认 |
| confirmed | 运营编辑者已确认，可引用 | — |
| rejected | 运营编辑者已驳回，标注原因 | — |

### trackingStatus（跟进状态）

| 取值 | 含义 | 初始值 |
|------|------|--------|
| pending | 非 tracking 候选，初始为 pending | ✅ 默认（trackingCandidate=False 时） |
| candidate | 进入 tracking 候选列表 | ✅ 默认（trackingCandidate=True 时） |
| follow_up | 确认后进入跟进 | — |
| closed | 跟进完成或已引用 | — |

---

## 周期性 review 规则

- **每周一**：执行抓取 → 更新 raw JSON → 运营 review
- **每月最后一周**：来源有效性 review → 数据归档 → 状态同步
- **每 sprint 末**（约2周）：变更控制清单 review → 文档一致性检查

---

## 当前阶段暂不纳入的复杂机制

| 机制 | 原因 |
|------|------|
| 自动告警（邮件/群消息） | MVP 阶段无需实时告警 |
| 多维度并行抓取 | 当前只有对公存款一个维度 |
| 动态来源发现（AI自动扩展） | 需要人工审核边界 |
| 版本对比和 diff 视图 | 超出 MVP 范围 |
| 自动分级（P1/P2 自动判断） | 需历史样本积累 |
