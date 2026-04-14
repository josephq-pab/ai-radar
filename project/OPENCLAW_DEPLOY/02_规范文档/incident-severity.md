# 异常优先级定义

## 概述

本文档定义试运行期间的异常分级机制，用于判断"问题严重不严重"，避免全靠人工经验判断。

---

## 异常等级定义

### P0: 阻断级别

**定义**: 试运行无法继续，必须立即处理。

**判断标准**:
- `run-summary.json` 中 `success: false` 或 `exitCode != 0`
- `smokeTestResult.FAIL > 0`
- 核心数据文件 (`deposit_benchmark.json`, `loan_benchmark.json`, `loan_rate.json`) 任一缺失或损坏

**处理方式**:
1. 立即停止使用系统
2. 检查运行日志定位问题
3. 修复后重新运行

**示例**:
```
❌ 核心数据文件缺失: deposit_benchmark.json
❌ smoke test FAIL: 3 项
❌ 运行 exitCode: 1
```

---

### P1: 警告级别

**定义**: 不阻断试运行，但会影响数据可信度或业务理解，需要尽快处理。

**判断标准**:
- `smokeTestResult.WARN > 0`
- analyst fetch 失败率 > 50%
- `reviewQueueFallbackCount` > 总数的 30%
- 数据新鲜度显示 `stale: true`
- tracking 状态分布异常（如 90% 以上为"待研判"）

**处理方式**:
1. 记录问题到 `reports/trial-issue-log.md`
2. 尽快排查原因
3. 使用时注意风险，可正常浏览但需注意数据可能不完整

**示例**:
```
⚠️ analyst fetch: 4/9 失败 (失败率 44%)
⚠️ 数据已过期 30+ 天，建议更新
⚠️ review queue 兜底比例: 35% (6/17)
```

---

### P2: 观察级别

**定义**: 非阻断观察项，可后续优化。

**判断标准**:
- loan_rate 的 observedAt 与 deposit/loan 时间口径不一致
- dedup 策略存在理论风险但未触发
- analyst 观点数量少于预期
- 页面加载性能问题

**处理方式**:
1. 记录到问题台账
2. 后续版本优化
3. 不影响当前使用

**示例**:
```
ℹ️ loan_rate 时间口径为月初，deposit/loan 为月末
ℹ️ dedup 存在理论风险: 若新版本出现在后面可能丢失
ℹ️ analyst 观点仅 5 条，可后续扩充
```

---

## 当前已知问题归类

| 问题 | 级别 | 影响范围 | 当前状态 |
|------|------|----------|----------|
| analyst fetch 4/9 失败 | P1 | analyst 观点 | open |
| snapshot 数据非实时 | P1 | 核心数据新鲜度 | open |
| observedAt 口径不一致 | P2 | loan_rate 时间解释 | open |
| loan dedup 策略风险 | P2 | 贷款数据完整性 | monitoring |
| review queue 兜底 | P2 | 建议质量 | monitoring |
| weekly report 未完全承接 tracking | P2 | 周报完整性 | open |

---

## 如何使用

1. 运行后查看 `reports/run-summary.json`
2. 检查 `verdict` 和 `warnings` 字段
3. 对照本表判断异常级别
4. 依据处理方式响应

```bash
# 快速判断健康度
python3 -c "
import json
s = json.load(open('reports/run-summary.json'))
verdict = s.get('verdict', 'unknown')
warnings = s.get('warnings', [])
print(f'健康度: {verdict}')
for w in warnings: print(f'  - {w}')
"
```

---

## 升级路径

- **P2 → P1**: 当观察项开始影响核心功能时
- **P1 → P0**: 当 P1 问题导致运行失败或数据完全不可用时
- **P0 / P1 → resolved**: 问题修复并验证通过后
