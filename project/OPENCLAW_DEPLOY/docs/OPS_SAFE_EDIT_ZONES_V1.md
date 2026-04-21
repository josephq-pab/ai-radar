# OPS_SAFE_EDIT_ZONES_V1.md — 安全修改区划分

> 文档版本：v1.0（P3-44）
> 创建时间：2026-04-21
> 对应阶段：Phase 3 — P3-44 假设变更演练、回归剧本与安全修改区功能包第一期
> 目的：建立 Safe Zone / Controlled Zone / No-touch Zone 三区划分，明确各区定义、典型内容、修改约束和回归要求

---

## 一、三区划分总览

| 区域 | 颜色标识 | 风险等级 | 改动要求 | 回归要求 |
|------|---------|---------|---------|---------|
| Safe Zone | 🟢 | 低风险 | 可局部改动，按需执行 | Quick Check 即可 |
| Controlled Zone | 🟡 | 中风险 | 需先查依赖图，按剧本执行 | Quick Check → Full Check |
| No-touch Zone | 🔴 | 高风险 | 当前阶段不建议动，按剧本评估 | Full Check + 白天人工确认 |

---

## 二、Safe Zone（低风险可局部改动）

### 2.1 定义

**Safe Zone 内容特征：**
- 不参与核心判断逻辑
- 不被其他模块引用为依据
- 改动后不影响用户的决策或判断
- 通常是独立的训练提示、路径引导说明、样式配置

**Safe Zone 改动前提：**
- 改动后上下文通顺
- 不与相邻句产生语义冲突
- 不改变页面核心定位

### 2.2 Safe Zone 典型内容

| 页面 | Safe Zone 内容 | 说明 |
|------|-------------|------|
| radar-home | home-M10（训练提示） | 训练型句子，不参与判断 |
| radar-home | home-M18（值班路径说明） | 路径引导，不参与判断 |
| ops-brief | brief-M03（使用时机说明） | 训练型句子，不参与判断 |
| ops-playbook | playbook-M01（执行页角色边界句） | 角色边界，不参与判断 |
| ops-playbook | playbook-M02（何时需要/不需要看执行页） | 训练型句子 |
| ops-glossary | glossary-M08（术语簇分组说明） | 索引型句子 |
| ops-routes | routes-M09（路径推荐逻辑说明） | 路径引导，不参与判断 |
| config-status | config-M04（配置快照说明） | 配置说明，不参与判断 |

### 2.3 Safe Zone 允许的改动

| 允许的改动类型 | 示例 |
|---------------|------|
| 模块标题文字微调（不影响含义） | "当前运营总览" → "当前运营状态总览" |
| 路径引导句文字优化（不改方向） | "先去 A 再去 B" → "建议先去 A，再去 B" |
| 训练提示句措辞优化（不改逻辑） | "请注意" → "需要注意" |
| 样式标签文字微调 | 颜色标签名称调整（不改变功能） |

### 2.4 Safe Zone 禁止的改动

| 禁止的改动类型 | 示例 |
|---------------|------|
| 任何判断句的文字替换 | "等待态(W)是默认起点" → "等待态(W)是主起点" |
| 任何 S0/S1 句的措辞改动 | "V7 基线冻结" → "V7 已锁定" |
| 改变页面角色边界含义 | "执行页不是默认入口" → "执行页是可选入口" |
| 引入新的功能描述 | "可以在此页面操作配置" |

### 2.5 Safe Zone 最低回归要求

```
Quick Check（QC-1 ~ QC-3）：
  [ ] 改动页面自查（加载正常、上下文通顺）
  [ ] 最近邻引用检查（≤2 个相关页）
  [ ] 版本标注更新（如需）
```

---

## 三、Controlled Zone（受控修改区）

### 3.1 定义

**Controlled Zone 内容特征：**
- 可能被其他模块引用
- 参与训练/误判澄清，但不直接参与核心判断
- 改动后需要同步相关引用
- 改动时需要先查依赖图

**Controlled Zone 改动前提：**
- 先查 OPS_MODULE_DEPENDENCY_MAP
- 确认涉及页面数量（≥3 升级为 No-touch）
- 有明确的改动理由和预期影响
- 准备好同步所有相关引用

### 3.2 Controlled Zone 典型内容

| 页面 | Controlled Zone 内容 | 风险来源 |
|------|-------------------|---------|
| radar-home | home-M09（升级说明） | 影响 single-chain-ops / ops-routes |
| radar-home | home-M06（高频误判澄清） | 被 ops-brief / ops-evidence 引用 |
| ops-brief | brief-M09（升级最小5字段） | 影响 decision / routes |
| ops-brief | brief-M07（第二链路冻结说明） | 影响 evidence / ops |
| single-chain-ops | ops-M06（升级说明） | 影响 radar-home / decision / routes |
| single-chain-ops | ops-M05（值班结果模板） | 影响 radar-home / routes |
| ops-decision | decision-M02（场景进入条件） | 影响 playbook / evidence |
| ops-decision | decision-M07（升级说明） | 影响 ops / radar-home |
| ops-evidence | evidence-M05（冻结理由说明） | 影响 ops / brief |
| ops-routes | routes-M08（升级/回写说明） | 影响 radar-home / ops |
| ops-registry | registry-M07（冲突解决规则） | 被多页引用为裁判依据 |

### 3.3 Controlled Zone 允许的改动

| 允许的改动类型 | 示例 |
|---------------|------|
| S2/S3 句的文字优化 | "可用分析师 3 条" → "可用分析师 3 条（曾刚）" |
| 局部段落内容补充（不超长） | 在说明后追加一句解释 |
| 升级说明措辞微调（同步全站） | 统一升级 5 字段措辞 |
| 误判澄清句顺序调整 | 调整澄清句顺序（不改变含义） |

### 3.4 Controlled Zone 禁止的改动

| 禁止的改动类型 | 示例 |
|---------------|------|
| 改变 S0 句的含义 | "升级说明最小5字段" → "升级说明2字段" |
| 删减高频误判澄清句 | 删除"冻结≠没做" |
| 改动触发条件/进入条件逻辑 | "正常触发：月度窗口到达" → "月度窗口到达即触发" |
| 单独改一个页面的镜像，不同步其他 | 改了 brief-M09 但不更新 decision-M07 |

### 3.5 Controlled Zone 最低回归要求

```
Quick Check → Full Check（按需升级）：
  [ ] 改前：查 OPS_MODULE_DEPENDENCY_MAP，确认影响范围
  [ ] 改前：确认涉及页面数量（≥3 升级为 No-touch）
  [ ] 改后：QC-1 + QC-2
  [ ] 改后：全站镜像同步检查
  [ ] 改后：S1 句同步（如涉及）
```

---

## 四、No-touch Zone（高风险不可轻动区）

### 4.1 定义

**No-touch Zone 内容特征：**
- 全站硬约束句（S0）
- 核心判断依据，被多个模块引用
- 涉及 V7 基线/第二链路/RUN-next 冻结
- 生命周期核心定义
- P0 模块

**No-touch Zone 改动前提：**
- 理论上当前阶段不建议动
- 如确需改动，必须满足：
  1. 有明确且无法回避的改动理由
  2. 完成 Full Check 全套回归
  3. 建议在白天执行（不是夜间）
  4. 需要人工确认（不只是工具执行）
  5. 改动后有完整回归验证

### 4.2 No-touch Zone 典型内容

| 页面 | No-touch Zone 内容 | 为什么不能动 |
|------|------------------|------------|
| radar-home | home-M01（状态横幅：V7冻结/第二链路冻结/等待触发） | S0 硬约束句，全站标准 |
| radar-home | home-M03（七阶段生命周期定义） | S0 生命周期体系根基 |
| radar-home | home-M04（三连澄清句：冻结≠没做/阻断≠放弃/不做≠忘了做） | S0 高频误判澄清 |
| ops-brief | brief-M01（V7基线冻结/第二链路冻结banner） | S0 主状态句 |
| ops-brief | brief-M08（第二链路冻结结构性说明） | S0 第二链路冻结句 |
| single-chain-ops | ops-M09（结论A：RUN-01最终结论句） | P0 结论性陈述 |
| single-chain-ops | ops-M02（不允许自动流转句） | S0 流转约束句 |
| single-chain-ops | ops-M04（次轮触发规则摘要） | P0 高依赖模块 |
| ops-decision | decision-M01（第二链路未解冻前不推进） | S0 第二链路句 |
| ops-decision | decision-M04（准备态≠RUN-next已开启） | S0 高频误判澄清 |
| ops-evidence | evidence-M01（证据≠判断依据） | S-MC-014，S0 硬约束 |
| ops-evidence | evidence-M02（来源候选≠解冻） | S-MC-006，S0 高频澄清 |
| ops-glossary | glossary-M01~M07（W/L/A/P/E/R/S七阶段定义） | S0 生命周期标准句 |
| ops-registry | registry-M04（十页真源归属总表） | S0 真源裁判依据 |
| ops-registry | registry-M07（冲突解决规则） | S0 真源冲突裁判句 |
| 所有页面 | 各页 footer（V7冻结/第二链路冻结状态句） | S0 主状态句传播 |

### 4.3 No-touch Zone 改动决策流程

```
遇到 No-touch Zone 改动请求时：

Step 1：这个改动真的必要吗？
  → 如果不动会怎样？如果不动能接受，先不动
  → 如果必须动，继续 Step 2

Step 2：这个改动属于 S0 句还是 P0 模块？
  → 查 OPS_SENTENCE_REGISTRY_V1.md 确认
  → 确认是 No-touch Zone

Step 3：白天还是夜间执行？
  → 建议白天（有足够时间做完整回归）

Step 4：执行 Full Check（FC-1 ~ FC-7）
  → 不得跳过任何步骤

Step 5：人工验收
  → 必须有人在改动后实际打开页面确认

Step 6：更新相关治理文档
  → 记录本次改动（时间/原因/改动内容/影响面）
```

### 4.4 No-touch Zone 最低回归要求

```
Full Check（FC-1 ~ FC-7 全套）+ 白天人工确认：
  [ ] FC-1：改动类型和风险等级已确认
  [ ] FC-2：真源层已检查
  [ ] FC-3：OPS_MODULE_DEPENDENCY_MAP 已查
  [ ] FC-4：全站镜像副本已同步
  [ ] FC-5：S0/S1 句所有位置已确认
  [ ] FC-6：P3 版本标注已更新
  [ ] FC-7：人工验收通过
  [ ] 额外：白天执行（非夜间）
  [ ] 额外：有人实际打开页面确认
```

---

## 五、三区内容速查表

### 5.1 按页面速查

| 页面 | Safe Zone | Controlled Zone | No-touch Zone |
|------|----------|----------------|---------------|
| radar-home | M10/M18 | M09/M06 | M01/M03/M04/M05 |
| ops-brief | M03 | M07/M09 | M01/M08 |
| single-chain-ops | M15 | M05/M06 | M02/M04/M09 |
| ops-decision | — | M02/M07 | M01/M04 |
| ops-playbook | M01 | M02 | — |
| ops-evidence | — | M05 | M01/M02 |
| ops-glossary | M08 | — | M01~M07 |
| ops-registry | — | M07 | M04 |
| ops-routes | M09 | M08 | — |
| config-status | M04 | — | — |

### 5.2 按 S0/S1 句速查

| S0 句 ID | 所属区域 | 所在页面数 |
|---------|---------|-----------|
| S-CORE-001~005 | 🔴 No-touch | ≥7 |
| S-LC-001~007 | 🔴 No-touch | ≥5 |
| S-JD-001~006 | 🔴 No-touch | ≥2 |
| S-SH-001~003 | 🔴 No-touch | ≥3 |
| S-ES-001~003 | 🟡 Controlled | ≥3 |
| S-MC-001~014 | 🔴 No-touch | ≥2 |
| S-PR-001~010 | 🟡 Controlled / 🔴 No-touch | ≥1 |

---

## 六、三区修改后的共同要求

**无论哪个区，改动后都必须：**

```
[1] 更新页面 P3 版本标注（当前页面最底部）
[2] 如涉及句子，查 OPS_SENTENCE_DIFF_MATRIX 确认是否需要同步
[3] 如涉及模块，查 OPS_MODULE_DEPENDENCY_MAP 确认影响范围
[4] 如涉及多个页面，确认所有镜像副本已同步
[5] 人工打开页面确认改动后上下文通顺
[6] 记录本次改动（时间/内容/原因/影响面）
```

---

*文档版本：v1.0（P3-44）*
*最后更新：2026-04-21*
*下次维护检查：下次有变更请求时先查本清单*
