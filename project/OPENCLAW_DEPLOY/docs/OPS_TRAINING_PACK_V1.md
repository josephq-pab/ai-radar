# OPS_TRAINING_PACK_V1.md — 使用者训练包

> 文档版本：v1.0（P3-40）
> 创建时间：2026-04-21
> 对应阶段：Phase 3 — 试点运营化 / P3-40 使用者上手训练、误用防护与演练题包功能包第一期
> 目的：让新使用者 / 老使用者 / 不同角色能正确使用十页，而不是用错

---

## 一、角色训练目标矩阵

### 角色1：领导 / 审阅者

| 项目 | 内容 |
|------|------|
| 最小需要会什么 | ①看 radar-home 首页状态横幅 ②看 ops-brief 最新快报 ③看 single-chain-ops 当前停点 |
| 最不需要学什么 | config-status 详细参数 / ops-playbook 执行步骤 / ops-glossary 全部术语 |
| 最容易误用什么 | 直接深查 ops-evidence（想看细节但不应优先）|
| 最適从哪几页开始 | radar-home → ops-brief → single-chain-ops |

### 角色2：日常运营者（值班员）

| 项目 | 内容 |
|------|------|
| 最小需要会什么 | ① ops-brief 快读判断 ② single-chain-ops 是否有动作判断 ③ 值班四步巡检路径 ④ 停点判断 |
| 最不需要学什么 | config-status 全部参数 / ops-playbook 全部执行细节 / ops-glossary 全部术语 |
| 最容易误用什么 | ops-decision 每轮必看 / ops-evidence 当默认入口 / ops-playbook 当思考页 |
| 最適从哪几页开始 | ops-brief → single-chain-ops → radar-home 四步路径 → ops-routes 值班路径 |

### 角色3：协作者（产品/风控/其他部门）

| 项目 | 内容 |
|------|------|
| 最小需要会什么 | ① radar-home 全局状态 ② ops-brief 最新动态 ③ ops-registry 真源归属 |
| 最不需要学什么 | 全部执行细节 / 配置参数 / 内部判断规则 |
| 最容易误用什么 | 把 ops-decision 当成讨论入口 / 把 ops-glossary 当成完整培训材料 |
| 最適从哪几页开始 | radar-home → ops-brief → ops-registry |

### 角色4：新接手者（交接场景）

| 项目 | 内容 |
|------|------|
| 最小需要会什么 | ① 十页各自角色 ② 核心三页闭环 ③ 生命周期七阶段 ④ 最小值班路径 ⑤ 边界场景判断 |
| 最不需要学什么 | 在还没真实输入时背完整规则 / 提前记住所有边界场景 |
| 最容易误用什么 | 把 ops-glossary 当第一本教材从头读 / 把 ops-routes 当规则原文背诵 |
| 最適从哪几页开始 | radar-home → ops-routes 新手路径 → ops-brief → single-chain-ops → ops-glossary 查疑 |

### 角色5：偶发查看者（偶尔看一眼）

| 项目 | 内容 |
|------|------|
| 最小需要会什么 | ① radar-home 首页状态横幅 ② ops-brief 一句话最新状态 |
| 最不需要学什么 | 任何规则细节 / 路径逻辑 / 边界判断 |
| 最容易误用什么 | 把 ops-evidence 当入口 / 把 ops-decision 当成必读 |
| 最適从哪几页开始 | radar-home（只看状态横幅和四步路径） |

---

## 二、第一次上手的最小学习顺序

### 新手第一天路径（约30分钟）

```
第1步：radar-home（10分钟）
  → 看首页状态横幅（理解当前系统状态）
  → 读"四步最小值班路径"模块（理解值班起点）
  → 看"第一次来先学什么"模块（知道不要从哪里开始）

第2步：ops-routes（5分钟）
  → 看角色路径总览（知道十页各自是什么）
  → 记住：首页→快报→运营是核心三页，其他是辅助/索引

第3步：ops-brief（5分钟）
  → 看快报格式（知道信息怎么组织）
  → 记住：快报不是规则页，是状态快照

第4步：single-chain-ops（10分钟）
  → 看当前停点位置（知道运营页在哪里）
  → 记住：运营页不是证据页，是判断页

第5步：ops-glossary（随查）
  → 遇到术语再查，不要从头读
```

---

## 三、不同角色最小必看集

| 角色 | 最小必看（3页以内）| 建议看（+2页）| 不需要先看 |
|------|-----------------|-------------|-----------|
| 领导/审阅者 | radar-home + ops-brief + single-chain-ops | ops-registry（查真源）| config / playbook / glossary 全文 |
| 日常运营者 | ops-brief + single-chain-ops + ops-routes（值班路径）| radar-home（状态横幅）| config / glossary 全文 |
| 协作者 | radar-home + ops-brief + ops-registry | ops-routes（角色总览）| playbook / decision / evidence |
| 新接手者 | radar-home + ops-routes + ops-brief | single-chain-ops + ops-glossary（查疑）| config / evidence |
| 偶发查看者 | radar-home（状态横幅）| ops-brief（一句话）| 其他全部 |

---

## 四、常见误用提醒（按页面）

### radar-home（首页）
- ❌ 不要把首页当证据页（证据在 ops-evidence）
- ❌ 不要把首页当配置页（配置在 config-status）
- ❌ 不要把首页当规则页（规则在 ops-glossary / ops-casebook）
- ✅ 首页是总入口：先看状态横幅 → 再看四步值班路径 → 再按角色进入

### ops-brief（快报）
- ❌ 不要把快报当规则学习材料（快报是最新的状态，不是规则本身）
- ❌ 不要期望在快报里看到完整分析（快读 = 1~2句状态描述）
- ✅ 快报只是让你快速判断"有没有值得看的新东西"

### single-chain-ops（运营）
- ❌ 不要把运营页当证据页（证据在 ops-evidence）
- ❌ 不要每次都翻到最深处（没有新信号就停在判断层）
- ✅ 运营页的核心问题是"现在要不要动"，不是"系统里有什么"

### ops-decision（决策）
- ❌ 决策页不是默认入口（没有触发条件不要来）
- ❌ 决策页不是留痕页（留痕在 ops-evidence）
- ❌ 决策页不是配置页（配置在 config-status）
- ✅ 决策页只在"边界不清 / 触发待判 / 异常待判"时才来

### ops-playbook（执行流程）
- ❌ 还没进入准备/执行阶段时，不要先看 playbook
- ❌ 不要把 playbook 当思考页（先判断，再执行，不是先想执行步骤）
- ✅ playbook 只在"已经确认要执行 / 已经在准备中"时才有意义

### config-status（配置）
- ❌ 不要把 config 当理解全局的起点
- ❌ 不要期望在 config 里看到业务规则（config 只管参数和来源）
- ✅ config 只在"核参数 / 对比配置 / 检查 Gate"时优先来

### ops-evidence（证据）
- ❌ ops-evidence 不是默认入口
- ❌ 不要在第一次上手时就读证据页（会迷失）
- ✅ 只在"解释 / 补材料 / 需要证明为什么成立"时才进

### ops-glossary（术语）
- ❌ 不要把 glossary 当第一本教材从头读
- ❌ 不要期望 glossary 里有完整培训内容（glossary 只是查疑用的）
- ✅ glossary 是"遇到术语再查"的工具，不是学习路径

### ops-registry（登记/真源）
- ❌ 不要把 registry 当首页
- ❌ 不要在 registry 里找业务判断（registry 只管真源和版本）
- ✅ registry 是"冲突时查谁更权威"的裁判页

### ops-routes（路径）
- ❌ 不要把 routes 当规则原文背诵
- ❌ 不要把 routes 当每次必读（routes 是路径选择工具，不是内容）
- ✅ routes 是"按角色 / 按场景 / 按时间"选择正确路径的索引

---

## 五、训练完成标准

### 新手完成标准（达到即为"可正确使用"）

1. 能说出核心三页是哪三个（radata-home / ops-brief / single-chain-ops）
2. 能说出运营页的核心判断问题（"现在要不要动"）
3. 能说出四步值班巡检路径（首页状态 → 快报判断 → 运营判断 → 停点）
4. 能说出决策页的进入条件（边界不清 / 触发待判 / 异常待判）
5. 能说出证据页的进入条件（解释 / 补材料 / 成立依据）
6. 能说出 config 页不是理解全局的起点
7. 能说出 glossary 的正确用法（查疑，不是学习）
8. 能说出第二链路当前状态（冻结）

### 老用户复习完成标准（达到即为"可保持正确使用"）

1. 能在真实输入出现时，正确判断"这是边界场景还是普通场景"
2. 能判断"这条新输入应该停在哪里"
3. 能发现自己在误用哪个页面，并主动回到正确路径
4. 能向新接手者正确解释十页各自角色

---

## 六、最小训练路径（按角色细分）

### 领导/审阅者路径（5分钟）
```
radar-home（状态横幅）→ ops-brief（快报一句话）→ single-chain-ops（当前停点）→ ops-registry（查真源，如需要）
```

### 日常运营者路径（值班路径，10分钟上手）
```
ops-brief（先判断有没有新东西）→ single-chain-ops（判断要不要动）→ ops-decision（如边界不清）→ 停点
```

### 协作者路径（10分钟）
```
radar-home（全局状态）→ ops-brief（当前动态）→ ops-registry（真源归属，如需要）
```

### 新接手者路径（30分钟）
```
radar-home → ops-routes → ops-brief → single-chain-ops → ops-glossary（查疑）→ ops-casebook（边界场景）
```
