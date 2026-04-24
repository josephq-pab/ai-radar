# FRONTEND_PHASE4_BASELINE_FREEZE_NOTE_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE4_CLOSURE_AUDIT（STAGE256）
- **日期**：2026-04-24
- **目的**：记录当前十页已冻结的 Phase 4 基线，明确 Phase 5 组件化与稳定化的输入前提

---

## 一、Phase 4 基线冻结声明

### 1.1 冻结范围

以下内容视为已冻结，Phase 5 继承时不得随意回退：

**十页 HTML 文件**（`03_前端页面/`）：
- radar-home.html
- single-chain-ops.html
- ops-decision.html
- ops-brief.html
- ops-evidence.html
- ops-playbook.html
- ops-routes.html
- ops-glossary.html
- ops-registry.html
- config-status.html

**十二份治理文档**（`docs/`）：

| 文档 | 版本 | 用途 |
|------|------|------|
| FRONTEND_ACTION_CLOSURE_RULES_V1.md | V1 | 页面动作闭环语法 |
| FRONTEND_STOP_CONDITION_RULES_V1.md | V1 | 停止条件规范 |
| FRONTEND_MINIMAL_COMPLETION_UNIT_RULES_V1.md | V1 | 最小完成单元定义 |
| FRONTEND_PAGE_EXIT_CRITERIA_PLAN_V1.md | V1 | 离开输出标准 |
| FRONTEND_FIRST_SCREEN_DECISION_RULES_V1.md | V1 | 首屏判定语法 |
| FRONTEND_SIGNAL_PRIORITY_RULES_V1.md | V1 | 信号优先级规范 |
| FRONTEND_SCAN_ORDER_RULES_V1.md | V1 | 扫描顺序规范 |
| FRONTEND_ATTENTION_DENSITY_PLAN_V1.md | V1 | 注意力密度方案 |
| FRONTEND_DISCLOSURE_STRATEGY_RULES_V1.md | V1 | 信息露出策略 |
| FRONTEND_INFORMATION_LAYERING_RULES_V1.md | V1 | 五层信息层级 |
| FRONTEND_DEFAULT_EXPANSION_RULES_V1.md | V1 | 默认展开规则 |
| FRONTEND_DETAIL_FOLDING_PLAN_V1.md | V1 | 细节折叠计划 |

---

## 二、已冻结的结构要素

### 2.1 首屏四问标准

```
1. 现在有没有事
2. 值不值得继续读
3. 当前最重要的结论是什么
4. 下一眼该看哪里
```

Phase 5 任何重设计必须保留此四问结构。

### 2.2 五层信息层级体系

```
L1：主结论（默认展开，不可折叠）
L2：主动作/路径（默认展开，不可折叠）
L3：必要依据（条件展开，按需查看）
L4：参考细节（默认折叠，consult 模式可见）
L5：背景补充/治理说明（强制折叠至 details）
```

Phase 5 不得破坏此层级顺序。

### 2.3 P4-6 details 折叠区标准标题

```
🔽 P4-6 治理折叠区（模块说明、句子规范、维护索引 — 维护人员按需展开）
```

### 2.4 版本标识标准

- meta 版本：`P4-6 · v1.0`
- footer 阶段名：`P4-6 · 信息压缩、默认展开策略与细节折叠治理功能包第一期`

---

## 三、已冻结的页面角色定位

| 页面 | 角色定位 | 冻结状态 |
|------|---------|---------|
| radar-home | 首页/任务触发入口 | ✅ 冻结 |
| single-chain-ops | 主链路运营页 | ✅ 冻结 |
| ops-decision | 决策支持页 | ✅ 冻结 |
| ops-brief | 快查快报页 | ✅ 冻结 |
| ops-evidence | 证据核查页 | ✅ 冻结 |
| ops-playbook | 执行流程页 | ✅ 冻结 |
| ops-routes | 支援页（角色路径） | ✅ 冻结 |
| ops-glossary | 支援页（术语） | ✅ 冻结 |
| ops-registry | 支援页（真源登记） | ✅ 冻结 |
| config-status | 配置快照页 | ✅ 冻结 |

**支援页约束**：glossary / registry / routes 不得中心化，不得承载延伸任务，必须维持"查到即回"。

---

## 四、已冻结的停止条件语法

### 4.1 主链路/决策类页面

**标准**：`[已完成动作] → [结论] → 即可停止`

### 4.2 支援页

**标准**：`查到[对象] → [确认动作] → 即可返回`

---

## 五、Phase 5 继承前提

Phase 5（组件化与稳定化）必须满足以下输入条件：

| 输入项 | Phase 5 要求 |
|--------|------------|
| 首屏四问 | 任何重设计不得移除四问结构 |
| 五层信息层级 | 任何组件化不得破坏层级优先级 |
| 支援页定位 | glossary/registry/routes 不得变成独立中心 |
| 停止条件语法 | 任何重构不得移除"即可停止/即可返回" |
| details 折叠区 | 治理说明必须保留折叠机制 |
| 版本标识 | P4-6 基线版本不得回退 |

---

## 六、Phase 4 变更日志（供 Phase 5 参考）

| 日期 | 阶段 | 变更内容 |
|------|------|---------|
| 2026-04-22 | P4-1 | 页面层级重整 + 导航分层 |
| 2026-04-22 | P4-2 | 首屏体验统一 + 骨架一致性 |
| 2026-04-22 | P4-3 | 跨页上下文连续性治理 |
| 2026-04-22 | P4-4 | 页面动作闭环、停止条件、最小完成单元 |
| 2026-04-23 | P4-5 | 首屏判定、关键信号前置、扫描效率 |
| 2026-04-23 | P4-6 | 信息压缩、默认展开、细节折叠 |
| 2026-04-24 | STAGE256 | 一致性清边 + 收尾审计 + 轻微漂移修正 |

---

## 七、冻结确认

| 检查项 | 状态 |
|--------|------|
| 十页版本统一为 P4-6 | ✅ |
| 十二份治理文档已归档 | ✅ |
| 首屏四问标准统一 | ✅ |
| 五层信息层级统一 | ✅ |
| 支援页支援定位稳定 | ✅ |
| details 折叠标题标准统一 | ✅ |
| 停止条件语法统一 | ✅ |
| 一致性漂移已修正（3处）| ✅ |
| 跟踪文档已同步 | ✅ |

**冻结日期**：2026-04-24
**冻结人**：AI雷达站 agent（STAGE256 PHASE4_CLOSURE_AUDIT）
