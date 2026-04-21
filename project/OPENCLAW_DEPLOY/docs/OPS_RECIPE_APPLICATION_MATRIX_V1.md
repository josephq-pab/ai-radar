# OPS_RECIPE_APPLICATION_MATRIX_V1.md — 配方应用矩阵

> 文档版本：v1.0（P3-45）
> 创建时间：2026-04-21
> 对应阶段：Phase 3 — P3-45 全站黄金路径、失败路径与维护配方样本库功能包第一期
> 目的：建立"改动对象 → 应该用哪个配方 → 回归深度是什么 → 是否需要白天"的快速映射表

---

## 一、配方应用矩阵

### 1.1 按页面/模块查找配方

| 页面 | 模块 ID | 模块名称 | 风险等级 | 适用配方 | 回归深度 | 夜间 |
|------|--------|---------|---------|---------|---------|------|
| radar-home | home-M01 | V7冻结banner | 🔴 No-touch | R-01 | FC-7+白天 | ❌ |
| radar-home | home-M02 | 第二链路冻结banner | 🔴 No-touch | R-04 | FC-7+白天 | ❌ |
| radar-home | home-M03 | 七阶段生命周期定义 | 🔴 No-touch | R-03 | FC-7+白天 | ❌ |
| radar-home | home-M04 | 三连澄清句（冻结≠没做等） | 🔴 No-touch | R-02 | FC-7+白天 | ❌ |
| radar-home | home-M05 | 不允许自动流转句 | 🔴 No-touch | R-01 | FC-7+白天 | ❌ |
| radar-home | home-M06 | 高频误判澄清 | 🟡 Controlled | R-02 | FC-3~7 | ❌ |
| radar-home | home-M07 | 相似场景边界 | 🟡 Controlled | R-11 | QC-3 | ✅ |
| radar-home | home-M08 | 第二链路说明 | 🟡 Controlled | R-04 | FC-7+白天 | ❌ |
| radar-home | home-M09 | 升级说明5字段 | 🟡 Controlled | R-05 | FC-3~7 | ⚠️ |
| radar-home | home-M10 | 训练提示 | 🟢 Safe | R-09 | QC-1 | ✅ |
| radar-home | home-M18 | 值班路径说明 | 🟢 Safe | R-10 | QC-1~2 | ✅ |
| ops-brief | brief-M01 | V7冻结banner | 🔴 No-touch | R-01 | FC-7+白天 | ❌ |
| ops-brief | brief-M03 | 使用时机说明 | 🟢 Safe | R-09 | QC-1 | ✅ |
| ops-brief | brief-M07 | 第二链路说明 | 🟡 Controlled | R-04 | FC-7+白天 | ❌ |
| ops-brief | brief-M09 | 升级最小5字段 | 🟡 Controlled | R-05 | FC-3~7 | ⚠️ |
| single-chain-ops | ops-M02 | 不允许自动流转句 | 🔴 No-touch | R-01 | FC-7+白天 | ❌ |
| single-chain-ops | ops-M04 | 次轮触发规则摘要 | 🔴 No-touch | R-03 | FC-7+白天 | ❌ |
| single-chain-ops | ops-M06 | 升级说明5字段 | 🟡 Controlled | R-05 | FC-3~7 | ⚠️ |
| single-chain-ops | ops-M07 | 先分类再停 | 🟡 Controlled | R-05 | FC-3~7 | ⚠️ |
| ops-decision | decision-M01 | 第二链路未解冻句 | 🔴 No-touch | R-04 | FC-7+白天 | ❌ |
| ops-decision | decision-M04 | 准备态≠RUN-next已开启 | 🔴 No-touch | R-02 | FC-7+白天 | ❌ |
| ops-decision | decision-M07 | 升级说明5字段 | 🟡 Controlled | R-05 | FC-3~7 | ⚠️ |
| ops-evidence | evidence-M01 | 证据≠判断依据 | 🔴 No-touch | R-02 | FC-7+白天 | ❌ |
| ops-evidence | evidence-M02 | 来源候选≠解冻 | 🔴 No-touch | R-02 | FC-7+白天 | ❌ |
| ops-playbook | playbook-M01 | 执行页角色边界句 | 🟢 Safe | R-09 | QC-1 | ✅ |
| ops-playbook | playbook-M02 | 何时需要看执行页 | 🟡 Controlled | R-11 | QC-3 | ✅ |
| ops-glossary | glossary-M01~M07 | W/L/A/P/E/R/S 七阶段定义 | 🔴 No-touch | R-15 | FC-7+白天 | ❌ |
| ops-glossary | glossary-M08 | 术语簇分组说明 | 🟢 Safe | R-09 | QC-1 | ✅ |
| ops-registry | registry-M04 | 十页真源归属总表 | 🔴 No-touch | R-12 | FC-7+白天 | ❌ |
| ops-registry | registry-M07 | 冲突解决规则 | 🔴 No-touch | R-12 | FC-7+白天 | ❌ |
| ops-registry | registry-M14~M17 | 真源归属四节 | 🟡 Controlled | R-12 | FC-7 | ❌ |
| ops-routes | routes-M08 | 升级/回写说明 | 🟡 Controlled | R-05 | FC-3~7 | ⚠️ |
| config-status | config-M04 | 配置快照说明 | 🟢 Safe | R-14 | QC-1 | ✅ |
| config-status | config-M05 | 状态快照字段 | 🟡 Controlled | R-14 | QC-1~2 | ✅ |

---

## 二、按改动类型查找配方

| 改动类型 | 典型对象 | 适用配方 | 风险等级 | 回归要求 | 夜间 |
|---------|---------|---------|---------|---------|------|
| 改 V7 冻结状态句 | home-M01/brief-M01 banner | R-01 | 🔴 | FC-7+白天 | ❌ |
| 改第二链路冻结句 | home-M02/brief-M08/decision-M01 | R-04 | 🔴 | FC-7+白天 | ❌ |
| 改高频误判澄清句 | home-M04(三连)/decision-M04 | R-02 | 🔴 | FC-7+白天 | ❌ |
| 改不允许自动流转句 | home-M05/ops-M02 | R-01 | 🔴 | FC-7+白天 | ❌ |
| 改七阶段定义句 | glossary-M01~M07 | R-15 | 🔴 | FC-7+白天 | ❌ |
| 改升级最小5字段 | brief-M09/ops-M06/decision-M07 | R-05 | 🟡 | FC-3~7 | ⚠️ |
| 改先分类再停 | ops-M07 | R-05 | 🟡 | FC-3~7 | ⚠️ |
| 改次轮触发规则 | ops-M04 | R-03 | 🔴 | FC-7+白天 | ❌ |
| 改 B 类值班结果才升级 | ops-M05 | R-05 | 🟡 | FC-3~7 | ⚠️ |
| 改本页面内 S1 句 | 各页局部 S1 句 | R-06 | 🟡 | QC-1~2 | ✅ |
| 改 S2/S3 句 | 局部段落措辞 | R-07 | 🟢 | QC-1 | ✅ |
| 改模块标题 | 各页模块标题 | R-08 | 🟢 | QC-1~2 | ✅ |
| 改训练提示句 | 各页 P3-40 训练提示 | R-09 | 🟢 | QC-1 | ✅ |
| 改路径引导句 | routes-M02/M09 | R-10 | 🟢 | QC-1~2 | ✅ |
| 改边界对照说明 | 各页边界对照/误判澄清 | R-11 | 🟡 | QC-3 | ✅ |
| 改 evidence 说明句 | evidence-M05 | R-13 | 🟡 | QC-1~2 | ✅ |
| 改配置快照描述 | config-M04/M05 | R-14 | 🟢 | QC-1 | ✅ |
| 改 registry 归属句 | registry-M04/M07 | R-12 | 🟡 | FC-7+白天 | ❌ |
| 改 glossary 术语定义 | glossary-M01~M07 | R-15 | 🔴 | FC-7+白天 | ❌ |
| cleanup 近重复压缩 | 值班路径/误判澄清/典型场景 | R-16 | 🟡 | QC-3 | ⚠️ |

---

## 三、按 S0/S1 句 ID 查找配方

| S0/S1 句 ID | 句内容摘要 | 适用配方 | 涉及页面数 | 夜间 |
|------------|---------|---------|-----------|------|
| S-CORE-001 | V7基线冻结/第二链路冻结 | R-01 | ≥5 | ❌ |
| S-CORE-002 | 等待触发/等待态默认起点 | R-01 | ≥3 | ❌ |
| S-CORE-003 | 冻结≠没做 | R-02 | ≥5 | ❌ |
| S-LC-001 | W/L/A/P/E/R/S七阶段定义 | R-15 | ≥5 | ❌ |
| S-LC-002 | 不允许自动流转 | R-01 | ≥3 | ❌ |
| S-LC-003 | 准备≠RUN-next已开启 | R-02 | ≥3 | ❌ |
| S-LC-004 | 评估≠升级 | R-02 | ≥3 | ❌ |
| S-JD-001 | 轻微信号≠评估项 | R-02 | ≥3 | ❌ |
| S-JD-002 | 边界不清≠直接升级 | R-02 | ≥3 | ❌ |
| S-JD-003 | 先分类再停 | R-05 | ≥3 | ⚠️ |
| S-JD-004 | B类值班结果才升级 | R-05 | ≥3 | ⚠️ |
| S-SH-001 | 第二链路未解冻前不推进 | R-04 | ≥3 | ❌ |
| S-SH-002 | 来源候选≠解冻 | R-02 | ≥3 | ❌ |
| S-SH-003 | 来源候选必须经过评估 | R-02 | ≥3 | ❌ |
| S-ES-001 | 升级最小5字段 | R-05 | ≥4 | ⚠️ |
| S-ES-002 | 次轮触发规则摘要 | R-03 | ≥3 | ❌ |
| S-MC-001 | 证据≠判断依据 | R-02 | ≥2 | ❌ |
| S-MC-014 | 补材料≠否决 | R-02 | ≥2 | ❌ |

---

## 四、快速决策树：遇到改动请求，下一步是什么？

```
遇到改动请求：

Step 1：这个改动涉及哪个模块/句子？
  → 定位到模块 ID

Step 2：该模块属于哪个风险区？
  → 查上表第一部分（按页面/模块）
  → 确认风险等级：🔴/🟡/🟢

Step 3：应该用哪个配方？
  → 配方编号 = R-01 ~ R-16

Step 4：回归深度是多少？
  → FC-7+白天（🔴）
  → FC-3~7 或 QC-3（🟡）
  → QC-1~2（🟢）

Step 5：可以夜间执行吗？
  → ❌ 禁止夜间（🔴 No-touch）
  → ⚠️ 不建议夜间（🟡 Controlled ≥3页联动）
  → ✅ 可夜间（🟢 Safe / 🟡 Controlled ≤2页）
```

---

## 五、配方复用：哪些页面可共享同一配方

| 配方 | 可复用页面 | 不可复用页面 | 原因 |
|------|-----------|------------|------|
| R-01（改 S0 横幅句） | radar-home / ops-brief / single-chain-ops / ops-evidence / ops-decision | — | 同一句的多个镜像 |
| R-02（改 S0 误判澄清） | radar-home / ops-decision / ops-evidence / ops-brief | — | 同一澄清句的多个镜像 |
| R-03（改生命周期句） | ops-glossary / radar-home / single-chain-ops | — | W/L/A/P/E/R/S 全站统一 |
| R-04（改第二链路句） | ops-brief / single-chain-ops / ops-decision | — | 同一第二链路句的多个镜像 |
| R-05（改升级 S1 句） | ops-brief / single-chain-ops / ops-decision / ops-routes | — | 同一升级句的多个镜像 |
| R-09（改训练提示） | 十页各自独立 | 无 | 各页训练提示独立设计 |
| R-10（改路径引导） | ops-routes / radar-home | — | 路径引导跨页引用 |
| R-11（改边界对照） | radar-home / ops-decision / ops-evidence | — | 边界对照跨页引用 |

---

*文档版本：v1.0（P3-45）*
*最后更新：2026-04-21*
*下次维护检查：遇到任何改动请求，先查本矩阵定位配方编号*
