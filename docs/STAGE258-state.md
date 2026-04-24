# STAGE258 — PHASE5-2 断点文件

**创建时间**：2026-04-24 17:51
**更新时间**：2026-04-24 18:05
**阶段**：PHASE5-2 模板实例化标识、结构属性落地与高优先级组件试点

## 子阶段清单

- [x] 创建 FRONTEND_TEMPLATE_INSTANCE_RULES_V1.md
- [x] 创建 FRONTEND_STRUCTURAL_DATA_ATTRIBUTE_SPEC_V1.md
- [x] 创建 FRONTEND_PRIORITY_COMPONENT_PILOT_RULES_V1.md
- [x] 创建 FRONTEND_PHASE5_2_ROLLOUT_PLAN_V1.md
- [x] 十页 body data-* 属性落地（data-template/role/stop-type/phase）
- [x] 十页 Block 注释标注（meta/first-screen/governance-fold/footer-nav）
- [x] 支援页 data-pilot="true" 标注（glossary/registry/config-status/routes）
- [x] 跟踪文档同步（CC-105 / FEEDBACK STAGE258 / R-118）
- [x] Git commit + push

## 十页 data-template 映射

| 页面 | data-template | data-role | data-support-page | data-stop-type |
|------|-------------|---------|------------------|---------------|
| radar-home | T-HOME | entry | - | stop |
| single-chain-ops | T-MAINCHAIN | main-chain | - | stop |
| ops-decision | T-DECISION | decision | - | stop |
| ops-playbook | T-PLAYBOOK | playbook | - | stop |
| ops-evidence | T-EVIDENCE | evidence | - | stop |
| ops-brief | T-BRIEF | brief | - | stop |
| ops-routes | T-SUPPORT | route | true | return |
| ops-glossary | T-SUPPORT | glossary | true | return |
| ops-registry | T-SUPPORT | registry | true | return |
| config-status | T-SUPPORT | config | true | return |

## 组件试点页面

glossary / registry / config-status / routes — data-pilot="true" 已标注

## 当前状态
**已完成。未自动进入下一轮。**
