# ROUND_RECAP_2026-04-08.md — 试点轮次小结

> 轮次编号：ROUND-02
> 执行日期：2026-04-08
> 运营编辑者：AI雷达站 agent
> 触发原因：例外执行（用户指令。触发条件不满足：距 ROUND-01 仅约1天，无 raw 新增。命中例外条件：用户明确要求推进）
> **重要说明**：本轮为机制验证轮，数据未刷新（79 raw / 29 usable / 5 queue 与 ROUND-01 完全相同），本轮重点验证现有机制在"数据未刷新"条件下的运行是否顺畅。

---

## 本轮状态概览

| 检查项 | 完成情况 | 备注 |
|--------|---------|------|
| build / queue 生成 | ✅ | 2026-04-08 已完成，数字与 ROUND-01 相同 |
| tracker upsert | ⚠️ 无新增变化 | 本轮 queue 条目与 ROUND-01 完全相同，tracker 状态未变 |
| tracker merge | ✅ | merge 正常，tracker 状态正确合入 |
| pilot-tracking-ledger.csv 导出 | ✅ | 2026-04-08 已导出 |
| 人工 review | ⚠️ 本轮未执行 | queue 条目与上轮相同，无新状态需确认 |

---

## 本轮数据变化

| 指标 | ROUND-01 | ROUND-02 | 变化 |
|------|----------|----------|------|
| raw 总记录数 | 79 | 79 | 0（数据未刷新）|
| usable 池记录数 | 29 | 29 | 0（数据未刷新）|
| review queue 条数 | 5 | 5 | 0（数据未刷新）|
| tracker 记录总数 | 5 | 5 | 0 |

**结论**：数据未刷新，本轮 queue 条目与 ROUND-01 完全一致。

---

## 本轮 queue 条目对比

| itemId | 来源 | articleTitle（摘要）| 与 ROUND-01 相比 |
|--------|------|-------------------|----------------|
| analyst-72873eb4 | 薛洪言 | 这些公司，都有护城河（收藏）| ✅ 完全相同 |
| analyst-21789d40 | 薛洪言 | 要熬出头了！6月，大胆买入这两个板块 | ✅ 完全相同 |
| analyst-ba70f502 | 周茂华 | 大额存单利率下降却仍是"香饽饽"... | ✅ 完全相同 |
| analyst-9e4b367f | 薛洪言 | 8月，新一轮牛市起点！ | ✅ 完全相同 |
| analyst-a535dc4d | 薛洪言 | 春节前，就别指望了 | ✅ 完全相同 |

**结论**：queue 条目与 ROUND-01 完全相同，无新增条目，无变化。

---

## 本轮 tracker 状态

| itemId | 来源 | reviewStatus | trackingStatus | 备注 |
|--------|------|-------------|---------------|------|
| analyst-72873eb4 | 薛洪言 | confirmed | follow_up | 状态保持 |
| analyst-21789d40 | 薛洪言 | confirmed | follow_up | 状态保持 |
| analyst-ba70f502 | 周茂华 | confirmed | candidate | 状态保持 |
| analyst-9e4b367f | 薛洪言 | confirmed | follow_up | 状态保持 |
| analyst-a535dc4d | 薛洪言 | confirmed | closed | 状态保持 |

**结论**：5/5 条全部保持 ROUND-01 状态，无新增 confirmed/rejected/follow_up/closed 操作。

---

## 本轮新发现

- 本轮数据未刷新，79 raw / 29 usable / 5 queue 与 ROUND-01 完全相同
- queue 条目完全一致，tracker 状态无需更新
- 本轮 merge 机制验证通过：build 重跑后 queue 的 pending 状态正确被 tracker 的 confirmed 状态覆盖

---

## 来源复核触发检查

| 触发条件 | 是否触发 | 判断依据 |
|---------|---------|---------|
| 满4~6周 | ❌ 否 | 距上次复核：约1天 |
| usable 大幅变化（±3） | ❌ 否 | 29 → 29，变化0 |
| 首次出现 raw | ❌ 否 | 各来源 raw 数量与 ROUND-01 一致 |
| queue 贡献明显变化 | ❌ 否 | 薛洪言 4/5 → 薛洪言 4/5，无变化 |
| 长期0 usable 来源状态改变 | ❌ 否 | 顾慧君/王锟仍为0 |

**结论**：✅ 未触发来源复核

---

## OPEN_ISSUES 更新

| 编号 | 问题描述 | 是否新增 | 当前状态 |
|------|---------|---------|---------|
| OI-03 | 来源先验权重过重（薛洪言截断其他来源）| ❌ 已有 | 开放中，薛洪言 4/5 占比持续（OI-03 持续恶化风险，但本轮无新数据无法确认） |
| OI-04 | confirmLevel 为规则映射，非人工验证 | ❌ 已有 | 开放中，本轮无 review 操作，无法验证 |

---

## 下轮关注点

- 关注新数据何时到来（下次触发依赖 raw 新增 ≥5 条 或 距上次满14天）
- 薛洪言 4/5 占比是否在新数据到来后有所改善（OI-03 持续观察）
- 若新数据到来，需重新执行完整 review 操作
- 来源复核仍建议按原计划约4周后（2026-05-07前后）执行

---

## 备注

- 本轮执行为机制验证，非数据更新轮
- pipeline 命令：build_analyst_opinions.py + generate_review_queue.py 直接运行（run-pipeline.py 存在路径问题，需后续记录）
- merge 机制验证通过：tracker 状态在 build 重跑后仍正确保留
- 本轮 ledger 状态与 ROUND-01 完全相同，无新增变化
