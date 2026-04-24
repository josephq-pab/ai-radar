# FRONTEND_PRIORITY_COMPONENT_PILOT_RULES_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE5-2（STAGE258）
- **日期**：2026-04-24
- **前提**：PHASE5-1 COMPONENT_BOUNDARY_RULES + PHASE5-2 STRUCTURAL_DATA_ATTRIBUTE_SPEC

---

## 一、试点目标

在支援页（ops-glossary / ops-registry / config-status / ops-routes）上试点四个高优先级组件的结构抽象，验证：
1. 组件边界抽取不影响页面渲染
2. 治理语法（首屏四问/支援化表达/停止条件）保持完整
3. 页面角色定位无回弹

**本轮只做结构验证，不做实际组件替换代码**。

---

## 二、四个高优先级组件

| 组件 | 对应 Block | 试点优先级 |
|------|-----------|----------|
| `FirstScreenJudge` | first-screen | P1 |
| `GovernanceFold` | governance-fold | P1 |
| `PageMeta` | meta | P2 |
| `FooterNav` | footer-nav | P2 |

---

## 三、试点语义边界（必须保持不变）

### 3.1 FirstScreenJudge 语义边界

**必须保留**：
- 四问措辞（"现在有没有事 / 值不值得继续读 / 当前最重要的结论是什么 / 下一眼该看哪里"）
- 首屏判定区高亮边框样式
- 支援页的"查到即回"表达

**禁止改变**：
- 四问的文案不得改写
- 首屏判定区不得降级为 L3/L4
- 支援化表达不得移除

### 3.2 GovernanceFold 语义边界

**必须保留**：
- `<details>` 折叠结构
- 标准标题 `🔽 P4-6 治理折叠区（...）`
- P3-41/42/43/44 内容完整性

**禁止改变**：
- details 的默认折叠状态不得改为默认展开
- 折叠标题格式不得改变

### 3.3 PageMeta 语义边界

**必须保留**：
- 版本号 `P4-6 · v1.0`
- 页面角色描述
- 快照属性标识

### 3.4 FooterNav 语义边界

**必须保留**：
- 导航链接数量（七页版 vs 十页版）
- 链接目标地址
- 支援页 FooterNav 可省略

---

## 四、试点成功标准

### 4.1 验证检查项

| 检查项 | 验证方式 |
|--------|---------|
| 页面可正常打开 | 浏览器渲染无报错 |
| 首屏四问可见 | 页面加载后不需要滚动即可看到 |
| 支援化表达可见 | 支援页的"即可返回"表达在首屏可见 |
| details 可正常展开/收起 | 点击折叠标题可切换状态 |
| Footer 导航链接正确 | 七个/十个链接均指向正确页面 |

### 4.2 回退条件

如出现以下任一情况，立即回退到 PHASE5-1 状态：
- 页面渲染异常
- 首屏四问不可见或被遮挡
- 支援化表达被移除
- details 折叠功能失效
- 导航链接断裂

---

## 五、试点页面顺序

### 第一批（最低风险）

1. **ops-glossary.html** — 支援页，结构最简单
2. **ops-registry.html** — 支援页，结构简单
3. **config-status.html** — 支援页，结构简单

### 第二批（低风险）

4. **ops-routes.html** — 支援页，结构中等

### 不在本轮试点的页面

- single-chain-ops.html / ops-decision.html / ops-evidence.html / ops-playbook.html
- 原因：主链路页语义复杂，试点失败影响大，留在 PHASE5-3 处理

---

## 六、组件结构验证写法

试点页面在结构上标注组件候选，但不实际重构。标注格式：

```html
<!-- ================================================ -->
<!-- COMPONENT PILOT: FirstScreenJudge (PHASE5-2) -->
<!-- 语义边界：四问 + 支援化表达不得改变 -->
<!-- ================================================ -->
<div data-block="first-screen"
     data-component-candidate="FirstScreenJudge"
     data-disclosure-level="L0"
     data-pilot="true">

<!-- ================================================ -->
<!-- COMPONENT PILOT: GovernanceFold (PHASE5-2) -->
<!-- 语义边界：details + 标准标题 + P3 内容完整 -->
<!-- ================================================ -->
<details data-block="governance-fold"
        data-component-candidate="GovernanceFold"
        data-disclosure-level="L5"
        data-pilot="true">
```

**注意**：`data-pilot="true"` 表示这是试点标注，实际组件替换将在 PHASE5-3 执行。
