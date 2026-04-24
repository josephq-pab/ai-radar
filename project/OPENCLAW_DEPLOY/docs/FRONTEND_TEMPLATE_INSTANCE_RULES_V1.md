# FRONTEND_TEMPLATE_INSTANCE_RULES_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE5-2（STAGE258）
- **日期**：2026-04-24
- **前提**：PHASE4_BASELINE_FREEZE_NOTE + PHASE5-1 TEMPLATE_SYSTEM

---

## 一、模板实例化原则

PHASE5-1 将十页归类为5类模板。PHASE5-2 的任务是：将"人能看懂的模板分类"变成"页面自身带稳定结构标识"。

**模板实例化定义**：将模板归属从注释层推进为页面自身可机器识别的结构标识，使后续组件抽象和页面维护有稳定锚点。

---

## 二、页面级模板标识规则

### 2.1 必须存在于页面根节点

每个页面必须在 `<html>` 后的首个语义容器上标注 `data-template` 属性。

**标准位置**：`<!-- PHASE5-1 TEMPLATE: T-xxx -->` 注释的紧邻父容器，或 `<body>` 标签本身。

**标准写法**：
```html
<!-- PHASE5-2 INSTANCE: T-HOME -->
<!-- COMPONENT-CANDIDATE: FirstScreenJudge --> <!-- COMPONENT-CANDIDATE: FooterNav --> <!-- COMPONENT-CANDIDATE: GovernanceFold -->
```

### 2.2 七类模板实例

| 模板代码 | 页面 | data-template 取值 |
|---------|------|-----------------|
| T-HOME | radar-home.html | `T-HOME` |
| T-MAINCHAIN | single-chain-ops.html | `T-MAINCHAIN` |
| T-DECISION | ops-decision.html | `T-DECISION` |
| T-PLAYBOOK | ops-playbook.html | `T-PLAYBOOK` |
| T-EVIDENCE | ops-evidence.html | `T-EVIDENCE` |
| T-BRIEF | ops-brief.html | `T-BRIEF` |
| T-SUPPORT | ops-routes/glossary/registry/config-status | `T-SUPPORT` |

### 2.3 支援页附加标识

支援页（glossary/registry/config-status/routes）除 `data-template="T-SUPPORT"` 外，还需：

```html
data-support-page="true"
data-stop-type="return"
```

主链路/决策类页面使用 `data-stop-type="stop"`。

---

## 三、Block 级标识规则

### 3.1 Block 标识原则

每个共性 Block 必须在包裹元素上标注 `data-block` 属性，标识该 Block 的类型。

### 3.2 标准 Block 代码

| Block 类型 | data-block 取值 | 层级 | 出现条件 |
|-----------|---------------|------|---------|
| 首屏判定区 | `first-screen` | L0 | 全部页面必备 |
| Page Meta | `meta` | L0 | 全部页面必备 |
| 当前动作区 | `action` | L2 | 主链路/决策/快报 |
| 停止条件区 | `stop-condition` | L2 | 主链路/决策/支援 |
| 支援页定位区 | `support-location` | L2 | 仅支援页 |
| 必要依据区 | `evidence` | L3 | 证据/决策页 |
| Footer Navigation | `footer-nav` | L4 | 全部页面 |
| 治理折叠区 | `governance-fold` | L5 | 全部页面 |

### 3.3 标注格式

```html
<!-- 首屏判定区 -->
<div data-block="first-screen" data-component-candidate="FirstScreenJudge">
  ...
</div>

<!-- 治理折叠区 -->
<details data-block="governance-fold" data-component-candidate="GovernanceFold">
  ...
</details>
```

---

## 四、角色标识规则

### 4.1 页面角色

每个页面必须有 `data-role` 属性，表明页面在运营体系中的角色：

| data-role | 含义 | 适用页面 |
|----------|------|---------|
| `entry` | 任务触发入口 | radar-home |
| `main-chain` | 主链路运营 | single-chain-ops |
| `decision` | 决策支持 | ops-decision |
| `playbook` | 执行流程 | ops-playbook |
| `evidence` | 证据核查 | ops-evidence |
| `brief` | 快查快报 | ops-brief |
| `route` | 路径导航 | ops-routes |
| `glossary` | 术语查询 | ops-glossary |
| `registry` | 真源登记 | ops-registry |
| `config` | 配置快照 | config-status |

### 4.2 停止类型

| data-stop-type | 含义 | 适用页面 |
|---------------|------|---------|
| `stop` | 主链路停止（即可停止）| 主链路/决策/快报/证据/配置 |
| `return` | 支援页返回（即可返回）| 支援页（routes/glossary/registry）|

---

## 五、支援页标识附加要求

支援页（T-SUPPORT）额外需要：

1. `data-support-page="true"` 在页面根容器
2. `data-stop-type="return"` 在页面根容器
3. 支援定位 Block（`data-block="support-location"`）必须存在于页面中，不得删除

---

## 六、标识稳定性规则

以下属性为页面结构基础标识，**不得随意删除或改名**：

- `data-template`
- `data-role`
- `data-block`
- `data-support-page`（支援页必备）
- `data-stop-type`

后续任何页面修改，必须保留这些标识。如需修改，必须先更新本文档和组件边界规则。
