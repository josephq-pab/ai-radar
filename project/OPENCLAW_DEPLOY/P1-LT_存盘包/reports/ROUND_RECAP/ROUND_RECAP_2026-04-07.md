# ROUND_RECAP_2026-04-07.md — 试点轮次小结

> 轮次编号：ROUND-01
> 执行日期：2026-04-07
> 运营编辑者：AI雷达站 agent
> 触发原因：试点启动（首轮建立 baseline，今日已运行 build）

---

## 本轮状态概览

| 检查项 | 完成情况 | 备注 |
|--------|---------|------|
| build / queue 生成 | ✅ | 2026-04-07 21:39 已完成 |
| tracker upsert | ✅ | 5/5 items 全部 reviewed |
| pilot-tracking-ledger.csv 导出 | ✅ | 已生成 |
| 人工 review | ✅ | 5条全部确认 |

---

## 本轮数据变化

| 指标 | 上一轮（参考） | 本轮（ROUND-01）| 变化 |
|------|--------------|----------------|------|
| raw 总记录数 | —（无历史） | 79 | 首轮建立 |
| usable 池记录数 | — | 29 | 首轮建立 |
| review queue 条数 | — | 5 | 首轮建立 |
| tracker 记录总数 | — | 5 | 首轮建立 |

---

## 本轮状态变化摘要

| itemId | 来源 | reviewStatus | trackingStatus | 备注 |
|--------|------|-------------|---------------|------|
| analyst-72873eb4 | 薛洪言 | confirmed | follow_up | 护城河观点，对公存款维度高度相关 |
| analyst-21789d40 | 薛洪言 | confirmed | follow_up | 存款利率下行观点，确认有效 |
| analyst-9e4b367f | 薛洪言 | confirmed | follow_up | 银行股观点，相关性高 |
| analyst-ba70f502 | 周茂华 | confirmed | candidate | 观点有效，继续观察是否进入周报 |
| analyst-a535dc4d | 薛洪言 | confirmed | closed | P2级，维度匹配度一般，已关闭 |

**结论**：本轮 5/5 条全部 confirmed，无 rejected。薛洪言主导特征明显（4/5条）。

---

## 本轮新发现

- 薛洪言在 top-5 中占 4/5 条（OI-03 来源权重问题，非来源质量问题）
- 周茂华 enterReport=1，usable=2，质量良好
- 连平/付一夫均未进入 top-5（被截断，非质量问题）
- 本轮无 rejected items

---

## 来源复核触发检查

| 触发条件 | 是否触发 | 判断依据 |
|---------|---------|---------|
| 满4~6周 | ❌ 否 | 首轮，距下次复核约4周（2026-05-07）|
| usable 大幅变化（±3） | ❌ 否 | 首轮，无历史对比 |
| 首次出现 raw | ❌ 否 | 各来源 raw 数量与上次一致 |
| queue 贡献明显变化 | ❌ 否 | 首轮 |
| 长期0 usable 来源状态改变 | ❌ 否 | 顾慧君/王锟仍为0 |

**结论**：✅ 未触发来源复核

---

## OPEN_ISSUES 更新

| 编号 | 问题描述 | 是否新增 | 当前状态 |
|------|---------|---------|---------|
| OI-03 | 来源先验权重过重（薛洪言截断其他来源）| ❌ 已有 | 开放中，持续观察 |
| OI-04 | confirmLevel 为规则映射，非人工验证 | ❌ 已有 | 开放中 |

---

## 下轮关注点

- 关注薛洪言的4/5占比是否持续（OI-03 观察）
- 下轮 build 后关注连平/付一夫是否能进入 enterReport
- 关注周茂华的 candidate item 是否最终进入 report
- 距下次来源复核：约4周（建议2026-05-07前后）

---

## 备注

- 本轮为试点启动 baseline建立，tracker 已初始化 5条 confirmed 状态
- SOP（PILOT_RUN_SOP.md）已建立，ROUND_RECAP_TEMPLATE.md 已建立，SOURCE_REVIEW_CHECKLIST.md 已建立
- 下轮触发条件：满14天（2026-04-21）或 raw 新增≥5条
