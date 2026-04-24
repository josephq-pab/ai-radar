# FRONTEND_STRUCTURAL_DATA_ATTRIBUTE_SPEC_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE5-2（STAGE258）
- **日期**：2026-04-24
- **前提**：PHASE4_BASELINE_FREEZE_NOTE + PHASE5-1 COMPONENT_BOUNDARY_RULES

---

## 一、data-* 属性规范总览

### 1.1 属性分类

| 属性 | 类别 | 作用域 | 稳定性 |
|------|------|--------|--------|
| `data-template` | 页面级 | 页面根容器 | 永久标识 |
| `data-role` | 页面级 | 页面根容器 | 永久标识 |
| `data-block` | Block级 | 各Block容器 | 永久标识 |
| `data-support-page` | 页面级 | 支援页根容器 | 支援页必备 |
| `data-stop-type` | 页面级 | 页面根容器 | 永久标识 |
| `data-component-candidate` | Block级 | 各Block容器 | 可演进 |
| `data-disclosure-level` | Block级 | 各Block容器 | 可演进 |
| `data-phase` | 页面级 | 页面根容器 | 版本追踪 |

---

## 二、data-template

**定义**：页面所属模板类型

**出现位置**：页面根容器 `<body>` 或其直接子容器

**取值**：

| 取值 | 含义 |
|------|------|
| `T-HOME` | 首页模板 |
| `T-MAINCHAIN` | 主链路页模板 |
| `T-DECISION` | 决策页模板 |
| `T-PLAYBOOK` | 执行页模板 |
| `T-EVIDENCE` | 证据页模板 |
| `T-BRIEF` | 快报页模板 |
| `T-SUPPORT` | 支援页模板 |

**写法**：
```html
<body data-template="T-HOME" data-role="entry" data-stop-type="stop">
```

---

## 三、data-role

**定义**：页面在运营体系中的角色

**取值**：

| 取值 | 含义 |
|------|------|
| `entry` | 任务触发入口 |
| `main-chain` | 主链路运营 |
| `decision` | 决策支持 |
| `playbook` | 执行流程 |
| `evidence` | 证据核查 |
| `brief` | 快查快报 |
| `route` | 路径导航 |
| `glossary` | 术语查询 |
| `registry` | 真源登记 |
| `config` | 配置快照 |

---

## 四、data-block

**定义**：Block 在共性 Block 体系中的类型

**出现位置**：各 Block 的包裹容器

**取值**：

| 取值 | 含义 | 出现条件 |
|------|------|---------|
| `first-screen` | 首屏判定区 | 全部页面 |
| `meta` | Page Meta | 全部页面 |
| `action` | 当前动作/路径区 | 主链路/决策/快报 |
| `stop-condition` | 停止条件区 | 主链路/决策/支援 |
| `support-location` | 支援页定位区 | 仅支援页 |
| `evidence` | 必要依据区 | 证据/决策页 |
| `footer-nav` | Footer 导航 | 全部页面 |
| `governance-fold` | 治理折叠区 | 全部页面 |

**写法**：
```html
<div data-block="first-screen" data-component-candidate="FirstScreenJudge">
```

---

## 五、data-support-page

**定义**：标识当前页为支援页

**出现位置**：仅支援页（routes/glossary/registry/config-status）

**取值**：`true`

**写法**：
```html
<div data-template="T-SUPPORT" data-role="glossary" data-support-page="true" data-stop-type="return">
```

---

## 六、data-stop-type

**定义**：页面停止条件类型

**取值**：

| 取值 | 含义 |
|------|------|
| `stop` | 主链路停止（即可停止）|
| `return` | 支援页返回（即可返回）|

---

## 七、data-component-candidate

**定义**：标识该 Block 为组件候选

**出现位置**：各 Block 容器

**取值**：

| 取值 | 对应 Block |
|------|-----------|
| `FirstScreenJudge` | first-screen |
| `FooterNav` | footer-nav |
| `GovernanceFold` | governance-fold |
| `PageMeta` | meta |
| `StopConditionBadge` | stop-condition |
| `SupportLocationBanner` | support-location |
| `EvidenceCard` | evidence（仅 evidence 页）|
| `DecisionConclusion` | action（仅 decision 页）|

**写法**：
```html
<div data-block="governance-fold" data-component-candidate="GovernanceFold">
```

---

## 八、data-disclosure-level

**定义**：Block 的信息层级（L0~L5）

**取值**：L0 / L1 / L2 / L3 / L4 / L5

**含义**：
- L0：页面入口级（首屏判定区、Page Meta）
- L1：主结论（页面最核心结论）
- L2：主动作/路径
- L3：必要依据
- L4：参考细节
- L5：背景补充/治理说明

**写法**：
```html
<div data-block="governance-fold" data-disclosure-level="L5">
```

---

## 九、data-phase

**定义**：页面当前治理阶段版本

**取值**：`P4-6`

**写法**：
```html
<body data-phase="P4-6">
```

---

## 十、属性书写规范

### 10.1 顺序规范

建议书写顺序：`data-template` → `data-role` → `data-support-page` → `data-stop-type` → `data-phase`

### 10.2 禁止事项

- ❌ 不得在 L1/L2 区块上标注 `data-disclosure-level="L5"`
- ❌ 不得在支援页上标注 `data-support-page="false"`
- ❌ 不得在主链路页上标注 `data-stop-type="return"`
- ❌ 不得混用模板代码（如 `T-HOME1`、`T-Decision`）
