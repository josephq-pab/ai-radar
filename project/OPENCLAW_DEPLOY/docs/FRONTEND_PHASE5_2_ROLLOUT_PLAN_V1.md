# FRONTEND_PHASE5_2_ROLLOUT_PLAN_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE5-2（STAGE258）
- **日期**：2026-04-24
- **前提**：PHASE5-1 + PHASE5-2 前三份文档

---

## 一、本轮落地顺序

本轮分三个批次执行：

### 第一批（属性落地，十页统一）：先做十页共性属性

| 顺序 | 页面 | 模板 | 主要工作 |
|------|------|------|---------|
| 1 | radar-home.html | T-HOME | data-template/role/stop-type + block属性 |
| 2 | single-chain-ops.html | T-MAINCHAIN | data-template/role/stop-type + block属性 |
| 3 | ops-decision.html | T-DECISION | data-template/role/stop-type + block属性 |
| 4 | ops-playbook.html | T-PLAYBOOK | data-template/role/stop-type + block属性 |
| 5 | ops-evidence.html | T-EVIDENCE | data-template/role/stop-type + block属性 |
| 6 | ops-brief.html | T-BRIEF | data-template/role/stop-type + block属性 |
| 7 | ops-routes.html | T-SUPPORT | data-template/role/stop-type + support标识 + block属性 |
| 8 | ops-glossary.html | T-SUPPORT | data-template/role/stop-type + support标识 + block属性 |
| 9 | ops-registry.html | T-SUPPORT | data-template/role/stop-type + support标识 + block属性 |
| 10 | config-status.html | T-SUPPORT | data-template/role/stop-type + support标识 + block属性 |

**第一批目标**：十页均具备 `data-template` + `data-role` + `data-block` 属性，共性 Block 均有 `data-component-candidate` 标注。

---

### 第二批（组件试点，支援页低风险）

| 顺序 | 页面 | 试点组件 | 试点目标 |
|------|------|---------|---------|
| 11 | ops-glossary.html | FirstScreenJudge + GovernanceFold | 结构验证 |
| 12 | ops-registry.html | FirstScreenJudge + GovernanceFold | 结构验证 |
| 13 | config-status.html | FirstScreenJudge + GovernanceFold | 结构验证 |
| 14 | ops-routes.html | FirstScreenJudge + GovernanceFold | 结构验证 |

**第二批目标**：四个支援页完成 `data-pilot="true"` 标注，组件边界验证通过。

---

### 第三批（主链路页，仅属性落地）

| 顺序 | 页面 | 状态 |
|------|------|------|
| 15 | single-chain-ops.html | data-block 全部属性完成 |
| 16 | ops-decision.html | data-block 全部属性完成 |
| 17 | ops-evidence.html | data-block 全部属性完成 |
| 18 | ops-playbook.html | data-block 全部属性完成 |

**第三批目标**：主链路页完成结构属性，但不进行组件试点（风险控制）。

---

## 二、执行约束

### 2.1 每页执行后必须验证

- 页面在浏览器中可正常渲染
- 首屏四问可见
- 支援化表达（支援页）可见
- details 折叠功能正常
- 导航链接完整

### 2.2 禁止事项

- ❌ 不得在同一次修改中同时改动多个页面（防止批量失败）
- ❌ 不得在属性落地时改变任何文案内容
- ❌ 不得在试点时添加/删除任何 Block 内容
- ❌ 不得修改 L1/L2 区块的样式类

---

## 三、风险控制

| 风险 | 缓解措施 |
|------|---------|
| 属性冲突（data-block 多处）| 标注最近父容器，不重复标注子块 |
| 支援化表达被覆盖 | 严格审查 data-block="support-location" 存在性 |
| 主链路页试点风险 | 留在 PHASE5-3，不在本轮试点 |
| 批量失败 | 每次只修改一页，验证后进入下一页 |

---

## 四、PHASE5-3 建议方向

**明确建议进入 PHASE5-3**，方向：

1. **实际组件替换（支援页）**：将 ops-glossary / ops-registry / config-status / ops-routes 的四个高优先级组件从标注层推进到实际替换层
2. **主链路页试点**：在 single-chain-ops 上试点 FirstScreenJudge + GovernanceFold
3. **组件接口建立**：为四个高优先级组件建立标准 HTML 模板片段

**PHASE5-3 入口条件**：
- 十页 data-template / data-role / data-block 属性完整 ✅
- 四个支援页 data-pilot 标注完成 ✅
- PHASE5-2 四份文档已归档 ✅
