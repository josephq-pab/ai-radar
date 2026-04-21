# OPS_MODULE_DEPENDENCY_MAP_V1.md — 全站模块级依赖关系图

> 文档版本：v1.0（P3-42）
> 创建时间：2026-04-21
> 对应阶段：Phase 3 — P3-42 全站模块级 inventory、依赖关系、重复治理与模块维护底图功能包第一期
> 目的：建立模块级依赖关系图，回答"改这个模块，哪些模块/文档会受影响"

---

## 一、核心概念

**上游真源（Primary Source）：** 模块内容的最原始来源文档
**下游展示（Downstream Display）：** 依赖本模块内容的展示层页面/模块
**关联文档（Related Docs）：** 与本模块内容相关的文档，但非上下游直接关系

**真源层级（优先级从高到低）：**
```
STAGE2 > analyst_sources.json > V7基线 > 各HTML页面 > 各文档包
```

---

## 二、模块 → 上游真源（我依赖谁）

### 2.1 首页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| home-M01 | 页头横幅 | STAGE2 | — | — |
| home-M02 | 统一状态横幅 | STAGE2 | — | OPS_COPY_BASELINE_V1.md |
| home-M03 | 页面元信息块 | STAGE2 | — | OPS_GOVERNANCE_MAP_V1.md |
| home-M04 | 非运行按钮提示 | STAGE2 | — | OPS_MISUSE_GUARDRAILS_V1.md |
| home-M05 | 状态卡片组 | STAGE2 | — | — |
| home-M06 | 入口卡片组 | STAGE2 | — | — |
| home-M07 | 页面分层与优先级看板 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |
| home-M08 | 核心三页默认闭环路径 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |
| home-M09 | 能力与边界看板 | STAGE2 | — | OPS_CAPABILITY_BOARD_V1.md |
| home-M10 | 按时间阅读最短路径 | STAGE2 | — | OPS_READING_MODES_V1.md |
| home-M11 | RUN-01最近关键结论 | STAGE2 | — | STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md |
| home-M12 | 自上次以来变化 | STAGE2 | — | CHANGE_CONTROL.md |
| home-M13 | 信息新鲜度与有效窗口 | STAGE2 | — | OPS_FRESHNESS_RULES_V1.md |
| home-M14 | 当前剩余未决事项 | STAGE2 | — | OPS_OPEN_ITEMS_V1.md |
| home-M15 | 下一步动作 | STAGE2 | — | OPS_CORE_LOOP_V1.md |
| home-M16 | 默认停点与不再深查规则 | STAGE2 | — | OPS_STOP_RULES_V1.md |
| home-M17 | 新输入响应分流 | STAGE2 | — | OPS_INPUT_RESPONSE_V1.md |
| home-M18 | 四步最小巡检路径 | STAGE2 | — | OPS_DAILY_ROUTINE_V1.md |
| home-M19 | 值班结果输出模板 | STAGE2 | — | OPS_SHIFT_OUTPUT_V1.md |
| home-M20 | 何时升级为拍板请求 | STAGE2 | — | OPS_ESCALATION_PACK_V1.md |
| home-M21 | 拍板回复处理 | STAGE2 | — | OPS_DECISION_REPLY_V1.md |
| home-M22 | 生命周期总览 | STAGE2 | — | OPS_LIFECYCLE_MAP_V1.md |
| home-M23 | 典型场景一眼判断 | STAGE2 | — | OPS_CASEBOOK_V1.md |
| home-M24 | 相似场景边界对照 | STAGE2 | — | OPS_BOUNDARY_CASES_V1.md |
| home-M25 | 使用者训练入口 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |

**首页依赖结论：** 所有25个模块均以 STAGE2 为主要真源，无例外。

---

### 2.2 快报页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| brief-M01~M04 | 页头/元信息/最小必看/看完后 | STAGE2 | single-chain-ops | — |
| brief-M05 | 统一状态横幅 | STAGE2 | — | OPS_COPY_BASELINE_V1.md |
| brief-M06 | 一句话状态 | STAGE2 | single-chain-ops | — |
| brief-M07 | 已完成关键成果 | STAGE2 | STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md | — |
| brief-M08 | 能力与边界看板 | STAGE2 | — | OPS_CAPABILITY_BOARD_V1.md |
| brief-M09~M14 | 时间阅读/异常/有效/未决/回访/停摆 | STAGE2 | — | — |
| brief-M15 | 下一步触发条件 | STAGE2 | — | STAGE2_SINGLE_CHAIN_TRIGGER_RULES_V1.md |
| brief-M16~M20 | 误解/阅读顺序/对外口径/误判/训练 | STAGE2 | — | OPS_MISUSE_GUARDRAILS_V1.md |

**快报依赖结论：** 主要依赖 STAGE2，部分依赖 single-chain-ops。

---

### 2.3 运营页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| ops-M04 | RUN-01运行结果 | STAGE2 | STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md | — |
| ops-M05 | RUN-01最终结论 | STAGE2 | STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md | — |
| ops-M06 | 次轮触发规则摘要 | STAGE2 | STAGE2_SINGLE_CHAIN_TRIGGER_RULES_V1.md | — |
| ops-M07 | 现在不能做什么 | STAGE2 | — | OPS_EXCEPTION_RULES_V1.md |
| ops-M08 | 运营状态新鲜度 | STAGE2 | — | OPS_FRESHNESS_RULES_V1.md |
| ops-M09~M13 | 停点/下一步/关联/新输入 | STAGE2 | — | OPS_CORE_LOOP_V1.md |
| ops-M14~M17 | 值班结果/模板/升级/拍板 | STAGE2 | — | OPS_SHIFT_OUTPUT_V1.md |
| ops-M18 | 状态流转与停点 | STAGE2 | — | OPS_LIFECYCLE_MAP_V1.md |
| ops-M19~M20 | 典型场景/相似场景 | STAGE2 | — | OPS_CASEBOOK_V1.md |
| ops-M21 | 运营页训练提示 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |
| ops-M22 | 治理维护提示 | STAGE2 | — | OPS_GOVERNANCE_MAP_V1.md |
| ops-M23 | 核心判断区 | STAGE2 | — | — |
| ops-M24 | 证据链连接 | STAGE2 | — | — |

**运营页依赖结论：** 核心判断类模块均以 STAGE2 为真源，产出类模块以 STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md 为真源。

---

### 2.4 证据页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| evidence-M03~M07 | 证据链/冻结原因/历史/冻结理由 | STAGE2 | SINGLE_CHAIN_EVIDENCE_PACK_V1.md | — |
| evidence-M08 | 证据页训练提示 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |
| evidence-M10 | 证据有效性说明 | STAGE2 | — | OPS_MISUSE_GUARDRAILS_V1.md |

**证据页依赖结论：** 所有模块均以 STAGE2 为真源，证据链内容补充 SINGLE_CHAIN_EVIDENCE_PACK_V1.md。

---

### 2.5 决策页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| decision-M05~M07 | 场景判断/条件/触发三问 | STAGE2 | — | OPS_CASEBOOK_V1.md |
| decision-M08 | 八步执行参考 | STAGE2 | — | SINGLE_CHAIN_OPS_PACK_V1.md |
| decision-M09 | 场景快速索引 | STAGE2 | — | OPS_CASEBOOK_V1.md |
| decision-M10~M11 | 边界对照/异常规则 | STAGE2 | — | OPS_BOUNDARY_CASES_V1.md |
| decision-M12~M22 | 何时/条件/评估/升级/回复 | STAGE2 | — | OPS_ESCALATION_PACK_V1.md |
| decision-M23 | 决策页训练提示 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |

**决策页依赖结论：** 核心判断模块以 STAGE2 为真源，场景参考模块以 OPS_CASEBOOK_V1.md 和 OPS_BOUNDARY_CASES_V1.md 为真源。

---

### 2.6 执行页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| playbook-M05~M06 | 八步执行总览/详细说明 | STAGE2 | SINGLE_CHAIN_OPS_PACK_V1.md | — |
| playbook-M07 | 停点清单 | STAGE2 | — | OPS_STOP_RULES_V1.md |
| playbook-M08 | 产出物规格说明 | STAGE2 | — | SINGLE_CHAIN_OPS_PACK_V1.md |
| playbook-M09 | 执行后回环路径 | STAGE2 | — | OPS_RETURN_LOOP_V1.md |
| playbook-M10 | 异常停点说明 | STAGE2 | — | OPS_EXCEPTION_RULES_V1.md |

**执行页依赖结论：** 执行步骤类模块以 STAGE2 和 SINGLE_CHAIN_OPS_PACK_V1.md 为真源。

---

### 2.7 术语页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| glossary-M03~M05 | 术语/生命周期/状态术语定义 | STAGE2 | OPS_COPY_BASELINE_V1.md | — |
| glossary-M06 | 术语页训练提示 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |

**术语页依赖结论：** 所有模块均以 STAGE2 和 OPS_COPY_BASELINE_V1.md 为真源。

---

### 2.8 真源登记页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| registry-M03 | 版本与真源说明 | STAGE2 | CHANGE_CONTROL.md | — |
| registry-M04 | 十页真源归属 | STAGE2 | — | OPS_GOVERNANCE_MAP_V1.md |
| registry-M05~M07 | 页面层级/优先级/冲突规则 | STAGE2 | — | OPS_GOVERNANCE_MAP_V1.md |
| registry-M08~M18 | 各类真源映射 | STAGE2 | 各专项文档 | — |
| registry-M19~M20 | 训练提示/治理维护 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |

**真源登记页依赖结论：** 全站所有真源最终都指向 STAGE2，本页是映射层，不是真源层。

---

### 2.9 路径页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| routes-M03~M04 | 十页角色/四大角色必看 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |
| routes-M05~M12 | 场景路径/闭环/深化/角色 | STAGE2 | — | OPS_CORE_LOOP_V1.md |
| routes-M13~M16 | 值班路径/输出/升级/回写 | STAGE2 | — | OPS_DAILY_ROUTINE_V1.md |
| routes-M17~M19 | 生命周期/典型场景/相似场景 | STAGE2 | — | OPS_LIFECYCLE_MAP_V1.md |

**路径页依赖结论：** 所有模块均以 STAGE2 为真源。

---

### 2.10 配置页模块依赖关系

| 模块ID | 模块名 | 主要真源 | 次要真源 | 关联文档 |
|--------|--------|---------|---------|---------|
| config-M05~M09 | 基线/来源/Gate/运行参数/规则 | analyst_sources.json | STAGE2 | — |
| config-M04/M11/M13 | 训练提示/边界说明 | STAGE2 | — | OPS_TRAINING_PACK_V1.md |

**配置页依赖结论：** 配置快照类模块以 analyst_sources.json 为真源（只读），训练提示类以 STAGE2 为真源。

---

## 三、高依赖模块清单（Multi-Source Modules）

以下模块同时依赖多个真源，维护时必须同时检查所有真源：

| 模块ID | 模块名 | 依赖真源数 | 具体真源 |
|--------|--------|-----------|---------|
| ops-M04 | RUN-01运行结果 | 2 | STAGE2 + STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md |
| ops-M05 | RUN-01最终结论 | 2 | STAGE2 + STAGE2_SINGLE_CHAIN_RUN_CLOSE_01.md |
| ops-M06 | 次轮触发规则摘要 | 2 | STAGE2 + STAGE2_SINGLE_CHAIN_TRIGGER_RULES_V1.md |
| brief-M06 | 一句话状态 | 2 | STAGE2 + single-chain-ops |
| playbook-M05 | 八步执行总览 | 2 | STAGE2 + SINGLE_CHAIN_OPS_PACK_V1.md |
| playbook-M06 | 各步骤详细说明 | 2 | STAGE2 + SINGLE_CHAIN_OPS_PACK_V1.md |
| playbook-M08 | 产出物规格说明 | 2 | STAGE2 + SINGLE_CHAIN_OPS_PACK_V1.md |
| evidence-M03~M07 | 证据链/冻结/历史 | 2 | STAGE2 + SINGLE_CHAIN_EVIDENCE_PACK_V1.md |
| config-M05~M09 | 所有配置快照 | 2 | analyst_sources.json + STAGE2 |
| glossary-M03~M05 | 所有术语定义 | 2 | STAGE2 + OPS_COPY_BASELINE_V1.md |

**维护高依赖模块时的强制步骤：**
1. 先查所有依赖真源是否有一致性
2. 如真源间有冲突，以 STAGE2 为准
3. 同步修改后验证所有依赖模块的一致性

---

## 四、模块 → 下游展示（谁依赖我）

### 4.1 高影响力模块（下游展示最多）

| 模块ID | 模块名 | 下游展示数量 | 下游展示列表 |
|--------|--------|------------|------------|
| home-M02 | 统一状态横幅 | 10 | 全站所有页面都有状态横幅副本 |
| home-M22 | 生命周期总览 | 4 | brief/ops/decision/routes |
| home-M09 | 能力与边界看板 | 3 | home/brief/ops |
| ops-M06 | 触发规则摘要 | 3 | ops/brief/decision |
| ops-M05 | RUN-01最终结论 | 2 | ops/home |
| brief-M06 | 一句话状态 | 2 | brief/home |
| playbook-M05 | 八步执行总览 | 2 | playbook/decision |
| registry-M04 | 十页真源归属 | 2 | registry/routes |

**高影响力模块改动影响范围：**
- home-M02 改动 → 需同步检查全站10个页面状态横幅
- home-M22 改动 → 需同步检查 brief/ops/decision/routes 四页生命周期模块
- ops-M06 改动 → 需同步检查 ops/brief/decision 三页触发规则

---

## 五、模块依赖强度矩阵

| 模块类型 | 对 STAGE2 依赖 | 对其他文档依赖 | 典型模块 |
|---------|--------------|--------------|---------|
| 状态总览类 | 极高 | 低 | home-M02/05/06 |
| 判断模块类 | 极高 | 中 | ops-M05/06, decision-M05 |
| 路径引导类 | 极高 | 低 | home-M08/10/18, routes-M04 |
| 训练提示类 | 高 | 中 | home-M25, decision-M23 |
| 证据说明类 | 中 | 高 | ops-M04, evidence-M03~M07 |
| 真源映射类 | 极高 | 中 | registry-M04~M18 |
| 场景判例类 | 中 | 高 | ops-M19/20, decision-M05/22 |
| 留痕/升级/回复类 | 高 | 低 | home-M19/20/21 |
| 治理维护类 | 高 | 低 | 各页元信息块 |

---

## 六、跨页依赖热点（Cross-Page Dependencies）

以下模块存在跨页重复表达，维护时需特别小心：

### 热点1：状态横幅（home-M02 镜像到所有页）
- 镜像到：brief-M05, ops-M02, evidence-M01, decision-M02, playbook-M02, glossary-M01, routes-M01, config-M02
- **维护注意：** 改 home-M02 时必须同步全站状态横幅

### 热点2：生命周期总览（home-M22 镜像到多页）
- 镜像到：brief（隐式），ops-M18, decision（无），routes-M17
- **维护注意：** 改 home-M22 时需同步 ops/decision/routes

### 热点3：触发规则摘要（ops-M06 镜像到 brief/decision）
- 镜像到：brief-M15, decision-M05（部分）
- **维护注意：** 改 ops-M06 时需同步 brief/decision

### 热点4：场景判断总表（decision-M05 独立但被引用）
- 被引用：ops-M19, routes-M18
- **维护注意：** 改 decision-M05 时需同步 ops/routes

---

## 七、依赖关系异常识别

以下模块的依赖关系存在潜在风险，维护时需特别关注：

| 异常类型 | 模块ID | 模块名 | 风险描述 |
|---------|--------|--------|---------|
| 真源漂移 | home-M09 | 能力与边界看板 | 看板内容随P3编号变化，但真源标注不精确 |
| 多层镜像 | home-M02 | 状态横幅 | 10个镜像副本，任一改动都可能遗漏同步 |
| 文档缺失 | ops-M23 | 核心判断区 | 标注为"无关联文档"，但内容实际上依赖多个文档 |
| 映射不清 | registry-M04 | 十页真源归属 | 映射关系复杂，但维护记录不完整 |

---

## 八、维护时的依赖检查步骤

### 改任何模块前的强制检查清单：

**Step 1：识别上游真源**
```
查本清单"模块 → 上游真源"章节
确认模块的 Primary Source 和 Secondary Source
```

**Step 2：检查真源间一致性**
```
如果模块有多于1个真源（如ops-M04），先验证所有真源是否一致
如有冲突，以 STAGE2 为准
```

**Step 3：识别下游展示**
```
查本清单"模块 → 下游展示"章节
列出所有会受影响的下游模块/页面
```

**Step 4：同步修改**
```
按依赖方向依次修改：真源层 → 展示层
不要跳步
```

**Step 5：验证一致性**
```
对照 OPS_TRACEABILITY_MATRIX_V1.md 验证
确认修改后的模块内容与真源一致
```

---

*文档版本：v1.0（P3-42）*
*最后更新：2026-04-21*
*下次维护检查：任何模块真源关系发生变化时*
