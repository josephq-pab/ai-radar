# CROSS_ROUND_CHECKLIST.md — 跨轮复盘触发检查清单

> 文档版本：v1.0（初建）
> 建立日期：2026-04-08
> 对应阶段：P1-4 多轮试点复盘机制
> 用途：帮助运营编辑者判断本轮哪些情况只需记 ROUND_RECAP，哪些需要触发跨轮关注，哪些需要升级 OPEN_ISSUES。

---

## 一、只记 ROUND_RECAP（不做跨轮动作）

以下情况**不需要**更新 ROUND_COMPARISON 的特殊标记，也**不需要**进入 OPEN_ISSUES，只在 ROUND_RECAP"本轮新发现"节记录：

- 某来源单轮 usable 数量 ±1~2 条的正常波动
- confirmLevel 分布略有变化但无系统性偏离
- queue 中顺序的正常轮换
- 某来源 enterReport 从 0 变 1 或从 1 变 0 的单次波动
- 触发检查已执行但无实质变化（见 PILOT_RUN_SOP 触发例外）

---

## 二、需要跨轮关注标记（记入 ROUND_RECAP + 更新 ROUND_COMPARISON 对应列）

以下情况在 ROUND_RECAP 中标注"⚠️ 跨轮关注"，并更新 ROUND_COMPARISON 对应格子：

| 触发条件 | 在 ROUND_COMPARISON 中标注 |
|---------|--------------------------|
| rejected 首次出现 | rejectedCount 列标注"⚠️ 首次" |
| 薛洪言 top-5 占比超过 4/5（如变为 5/5） | topSourceShare 列标注"⚠️ 占比上升" |
| usable 变化超过 ±5 条（相对上轮） | usableCount 列标注"⚠️ 跳变" |
| 某来源连续 2 轮 queue 贡献为 0 但 raw > 0 | 记入 ROUND_RECAP 本轮新发现 |
| 首次触发来源复核 | 来源复核记录，标注"首次触发" |

---

## 三、需要升级进入 OPEN_ISSUES（ROUND_RECAP 标注 + OPEN_ISSUES 更新）

以下情况**必须**在 ROUND_RECAP 标注"🚨 建议升级"，并在当轮或下轮更新 OPEN_ISSUES.md：

| 触发条件 | 升级理由 | 记入 OPEN_ISSUES 的编号 |
|---------|---------|----------------------|
| rejected 首次出现且非误操作 | 重要信号，跨轮追踪 | 新增 OI-0X |
| 某来源 raw 数量大幅下降（>50%相对历史均值） | 疑似抓取逻辑异常 | 新增 OI-0X |
| review 判断与 confirmLevel 系统性偏离（>30%条目被反方向处理） | confirmLevel 规则问题（关联 OI-04） | 更新 OI-04 描述 |
| 任何影响试点正常推进的异常 | — | 新增 OI-0X |
| 新增 OI 后同步更新 ROUND_COMPARISON 的 openIssuesStatus 列 | — | — |

---

## 四、何时做小复盘（正式跨轮复盘）

以下条件满足**任一**时，应在 ROUND_RECAP 中标注"🔴 建议小复盘"，并在当轮或下轮结束后做最小复盘（见 PILOT_RETRO，非当前必须）：

- **条件1**：连续 3 轮无 rejected 条目（说明 review 判断过于宽松，缺乏过滤）
- **条件2**：OI 连续 3 轮无变化（说明自行缓解概率低）
- **条件3**：薛洪言 top-5 占比连续 3 轮超过 80%
- **条件4**：usable 池连续 2 轮下降或上升超过 ±10 条

> 注：当前只跑 2~3 轮试点，上述条件在前 3 轮内通常不会触发。小复盘是 3 轮后的机制，当前不强制执行。

---

## 五、何时更新 ROUND_COMPARISON

| 时点 | 动作 |
|------|------|
| 每轮结束后 | 追加新一行，填写本轮数字 |
| 来源复核触发后 | 在 openIssuesStatus 列注明"来源复核已执行" |
| 新增或关闭 OI 后 | 更新 openIssuesStatus 列 |
| 发现需跨轮关注的数字跳变 | 在对应格子加 ⚠️ 标注 |

---

## 六、当前不做

- ❌ 不做系统性 confirmLevel vs 人工判断偏差统计（OI-04 未解决，基准不存在）
- ❌ 不做趋势图 / dashboard
- ❌ 不做自动告警
- ❌ 不做跨轮原因分析（原因分析在 ROUND_RECAP"本轮新发现"节）
