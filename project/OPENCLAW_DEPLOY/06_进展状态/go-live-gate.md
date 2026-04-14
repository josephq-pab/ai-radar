# 对公 AI 雷达站｜试运行准入门槛清单

**版本**: go-live-gate-v1
**生成时间**: 2026-04-01
**用途**: 明确 reportPrepReadiness 提升到 ready 的准入门槛

---

## 一、准入门槛分层

系统 readiness 分三层，各自对应不同准入门槛：

| readiness | 含义 | 达到 ready 的门槛 |
|-----------|------|-----------------|
| `browseReadiness` | 系统可正常浏览 | smoke test 全 PASS + bundle 新鲜 |
| `internalDiscussionReadiness` | 可用于内部讨论复盘 | 数据新鲜 + analyst 基本可信 |
| `reportPrepReadiness` | 可用于正式汇报前准备 | 三类门槛全部满足 |

---

## 二、三类门槛定义

### 门槛 A：数据新鲜度

| 检查项 | 门槛值 | 当前值 | 状态 |
|--------|--------|--------|------|
| deposit observedAt | ≥ 2026-03 | 2026-02-28 | ❌ 缺 2026-03 数据 |
| loan observedAt | ≥ 2026-03 | 2026-02-28 | ❌ 缺 2026-03 数据 |
| rate observedAt | ≥ 2026-03 | 2026-02-01 | ❌ 缺 2026-03 数据 |
| dataFreshness.blocked | false | true（阻塞中）| ❌ |

**数据门槛满足条件**：A-1、A-2、A-3 全部 ≥ 2026-03-01

---

### 门槛 B：Analyst 输入质量

| 检查项 | 门槛值 | 当前值 | 状态 |
|--------|--------|--------|------|
| analyst 层 verdict | ≠ degraded | degraded | ❌ |
| analyst 层 isReliableForReport | true | false | ❌ |
| analyst 层 referenceableCount | ≥ 5 | 3 | ⚠️ 不足 |
| analyst 层 garbledCount | 0 | 4 | ❌ |
| analyst 层 emptyOrPlaceholderCount | 0 | 2 | ❌ |

**Analyst 门槛满足条件**：verdict ≠ degraded 且 referenceableCount ≥ 3 且 garbledCount = 0

当前状态下分析师门槛仍为 degraded（乱码未修复），fetch 源头编码问题需先修。

---

### 门槛 C：Pending 决策完成度

| 检查项 | 门槛值 | 当前值 | 状态 |
|--------|--------|--------|------|
| 静默 pending（未进入 review 流程）| 0 | 2 | ❌ |
| pending 总量中 trackingStatus=待研判 | < 3 | 2 | ⚠️ 边缘 |
| pending 中 waiting-for-business-decision 未闭环 | 0 | 1 | ❌ |

**Pending 门槛满足条件**：
- 静默 pending 全部处理完毕（reject 或正式进入 review）
- 无未闭环的 waiting-for-business-decision

---

## 三、当前 reportPrepReadiness = limited 的具体阻塞项

| 阻塞类型 | 具体项 | 属于哪个门槛 | 是否硬阻断 |
|---------|--------|-------------|--------|
| 2026-03 数据未到位 | deposit/loan/rate observedAt 均 < 2026-03 | A 数据新鲜度 | ✅ 硬阻断 |
| analyst 层乱码 | 4 条 GARBLED，2 条 PLACEHOLDER | B 输入质量 | ✅ 阻断 reportPrep |
| 2 项静默 pending | 1dbd4051cc58 + 581527c09784 | C Pending 完成度 | ⚠️ 软阻断 |

---

## 四、readiness 提升路径图

```
当前状态：
browseReadiness     = ready  ✅
internalDiscussionReadiness = limited ⚠️（数据+analyst 双重阻塞）
reportPrepReadiness = limited ⚠️（数据+analyst+pending 三重阻塞）

提升路径：
Step 1: 收到 2026-03 数据 → import_monthly_data.py --confirm
          → 数据新鲜度门槛 A 解除 → internalDiscussionReadiness 可升 ready

Step 2: 修复 analyst fetch 编码 → 乱码条目减少
          → analyst verdict → degraded
          → analyst isReliableForReport → true

Step 3: 处理 2 项静默 pending（reject 或 approve）
          → pending 门槛 C 解除

三者同时满足 → reportPrepReadiness 可升 ready
```

---

## 五、准入门槛检查命令

```bash
# 查看当前 readiness
cat reports/run-summary.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for k, v in d['readinessLevels'].items():
    print(f'{k}: {v[\"level\"]} — {v[\"verdictText\"]}')
"

# 查看 analyst 层质量
cat data/processed/analyst_opinions.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
s = d['summary']
print(f'verdict: {s.get(\"verdict\")} | valid: {s[\"qualityTiers\"].get(\"VALID\",0)} | garbled: {s[\"qualityTiers\"].get(\"GARBLED\",0)} | placeholder: {s[\"qualityTiers\"].get(\"PLACEHOLDER\",0)}')
"

# 查看 pending 状态
cat reports/tracking-items.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
s = d['trackingStatusSummary']
t = d.get('total', 0)
pending = s.get('待研判', 0) + s.get('跟踪中', 0)
print(f'pending: {pending}/{t}')
"
```

---

**当前阻塞**：A+B+C 三重门槛均未满足，reportPrepReadiness = limited 状态合理。
