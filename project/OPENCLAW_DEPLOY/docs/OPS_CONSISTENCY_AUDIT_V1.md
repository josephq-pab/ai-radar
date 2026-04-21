# OPS_CONSISTENCY_AUDIT_V1.md — 全站一致性审计报告

> 文档版本：v1.0（P3-39）
> 审计时间：2026-04-20
> 对应阶段：Phase 3 — 试点运营化 / P3-39 全站一致性审计、口径归一与重复压缩功能包第一期
> 审计范围：十页 HTML + 核心 OPS 文档
> 审计目的：识别硬冲突/软漂移/重复堆叠/模块顺序问题/页面角色混淆，形成修复动作清单

---

## 变更控制

| 编号 | 日期 | 变更内容 | 分类 |
|------|------|---------|------|
| CC-89 | 2026-04-20 | P3-39 全站一致性审计、口径归一与重复压缩功能包第一期 | 已批准 |

---

## 一、审计范围

### 页面（10个）

| 页面 | 文件 | 最近更新版本 |
|------|------|------------|
| radar-home.html | 首页总入口 | P3-38 ✅ |
| ops-brief.html | 状态快报 | P3-38 ✅ |
| single-chain-ops.html | 单链路运营入口 | P3-38 ✅ |
| ops-decision.html | 运营决策助手 | P3-38 ✅ |
| ops-routes.html | 角色路径 | P3-38 ✅ |
| ops-registry.html | 版本与真源登记 | P3-38 ✅ |
| ops-evidence.html | 运营证据与历史入口 | P3-38 ✅ |
| config-status.html | 配置快照 | **P3-29 ❌ 严重落后** |
| ops-playbook.html | 运营执行流程 | **P3-29 ❌ 严重落后** |
| ops-glossary.html | 术语与口径 | **P3-25 ❌ 严重落后** |

### 核心文档（18个）

OPS_CORE_LOOP_V1.md / OPS_AUX_JUMP_RULES_V1.md / OPS_RETURN_LOOP_V1.md / OPS_STOP_RULES_V1.md / OPS_INPUT_RESPONSE_V1.md / OPS_DAILY_ROUTINE_V1.md / OPS_SHIFT_OUTPUT_V1.md / OPS_ESCALATION_PACK_V1.md / OPS_DECISION_REPLY_V1.md / OPS_LIFECYCLE_MAP_V1.md / OPS_CASEBOOK_V1.md / OPS_BOUNDARY_CASES_V1.md / STAGE2_SINGLE_CHAIN_STATUS.md / FEEDBACK_TRACKING_STATUS.md / REVIEW_LOG.md / CHANGE_CONTROL.md / OPS_EXCEPTION_RULES_V1.md / OPS_OPEN_ITEMS_V1.md

---

## 二、审计维度矩阵

| 维度 | radar | brief | ops | decision | routes | registry | evidence | config | playbook | glossary |
|------|-------|-------|-----|----------|--------|----------|----------|--------|----------|----------|
| 1. 状态主线一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌旧版 | ❌旧版 | ❌旧版 |
| 2. 页面角色一致性 | ✅ | ✅ | ⚠️缺meta | ⚠️缺meta | ⚠️缺meta | ✅ | ⚠️缺meta | ❌缺meta | ❌缺meta | ❌缺meta |
| 3. 模块顺序一致性 | ✅ | ✅ | ⚠️旧注释 | ✅ | ✅ | ✅ | ✅ | ⚠️旧注释 | ⚠️旧注释 | ⚠️旧注释 |
| 4. 术语一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌未同步 | ❌未同步 | ❌未同步 |
| 5. 生命周期一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌未同步 | ❌未同步 | ❌未同步 |
| 6. 路径规则一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌未同步 | ❌未同步 | ❌未同步 |
| 7. 真源引用一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | N/A | N/A |
| 8. 重复解释密度 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️待压缩 | ⚠️待压缩 | ⚠️待压缩 |
| 9. 误判澄清一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | N/A | N/A |
| 10. 导航与交叉引用一致性 | ✅ | ✅ | ❌缺nav | ✅ | ✅ | ✅ | ❌缺nav | ❌缺nav | ✅ | ❌缺nav |
| 11. 版本/元信息一致性 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌P3-29 | ❌P3-29 | ❌P3-25 |
| 12. 冗余与压缩空间 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️待处理 | ⚠️待处理 | ⚠️待处理 |

---

## 三、硬冲突清单

**结论：未发现硬冲突**

检查项：
- 状态主线定义（等待态W/轻响应态L/评估态A/准备态P/升级态E/回复吸收态R/回收停点S）在所有页一致
- V7基线冻结描述在所有页一致
- 第二链路冻结描述在所有页一致
- RUN-next冻结描述在所有页一致
- 核心三页闭环描述一致
- 辅助页单跳规则描述一致

---

## 四、软漂移清单

### 4.1 版本标识落后（高优先级）

| 页面 | 当前标识版本 | 应为版本 | 影响 |
|------|------------|---------|------|
| config-status.html | P3-29 | P3-38 | 用户看到版本混乱，不信任感 |
| ops-playbook.html | P3-29/P3-25 | P3-38 | 同上 |
| ops-glossary.html | P3-25 | P3-38 | 同上 |

### 4.2 缺少 meta 信息区块（中优先级）

| 页面 | 缺少 meta 区块 | 影响 |
|------|--------------|------|
| config-status.html | ✅ 缺少 | 无法快速判断页面角色 |
| ops-playbook.html | ✅ 缺少 | 同上 |
| ops-glossary.html | ✅ 缺少 | 同上 |
| single-chain-ops.html | ⚠️ 注释旧P3-31 | 影响可读性 |
| ops-evidence.html | ⚠️ 注释旧P3-4~P3-10 | 影响可读性 |

### 4.3 缺少 footer-nav 导航（高优先级）

| 页面 | 是否有 footer-nav | 十页导航完整 |
|------|-----------------|------------|
| config-status.html | ❌ 无 | — |
| single-chain-ops.html | ❌ 无 | — |
| ops-evidence.html | ❌ 无 | — |
| ops-glossary.html | ❌ 无 | — |

其余页面 footer-nav 完整（radar-home / ops-decision / ops-playbook / ops-registry / ops-brief / ops-routes 均有）。

### 4.4 模块注释标记过时（低优先级）

| 页面 | 过时注释 | 影响 |
|------|---------|------|
| single-chain-ops.html | P3-31 / P3-33 注释标记 | 影响代码可读性，不影响功能 |
| ops-evidence.html | P3-4~P3-10 注释标记 | 同上 |
| ops-playbook.html | P3-7 / P3-29 注释标记 | 同上 |
| config-status.html | P3-2 / P3-29 注释标记 | 同上 |

---

## 五、重复堆叠清单

### 5.1 可以压缩的内容

| 位置 | 重复说明 | 建议 |
|------|---------|------|
| 页面 footer | "V7基线冻结" 完整描述在每个页面 footer 均重复 | 统一为标准句：V7 基线冻结 / 小范围月度试用等待触发 |
| radar-home 状态横幅 | 多期 P3-XX 状态横幅残留 | 统一为当前 P3-38 状态横幅，删除旧版横幅注释 |
| 各页统一状态横幅 | 部分页面仍有旧版横幅区块 | 统一为当前 P3-38 版本 |

### 5.2 保留厚度的内容（不应压缩）

| 位置 | 内容 | 保留理由 |
|------|------|---------|
| radar-home 首页总入口 | 全站状态横幅 + 生命周期总览 | 首页需要完整性 |
| ops-brief 快报 | 每期快报内容 | 快报需要记录时间戳 |
| single-chain-ops 运营页 | 状态流转详细说明 | 运营判断需要详细依据 |
| 各 OPS 文档 | 每期变更记录 | 可追溯性需要 |

---

## 六、模块顺序问题清单

| 页面 | 问题 | 建议 |
|------|------|------|
| config-status | 缺少统一状态横幅（直接从 header badge 跳到配置内容）| 在 header badge 后增加当前状态横幅，与其他页对齐 |
| single-chain-ops | footer-nav 缺失 | 增加 footer-nav，与其他九页对齐 |
| ops-evidence | footer-nav 缺失 | 增加 footer-nav，与其他九页对齐 |
| ops-glossary | footer-nav 缺失 | 增加 footer-nav，与其他九页对齐 |

---

## 七、页面角色混淆点

| 页面 | 混淆风险 | 当前状态 |
|------|---------|---------|
| config-status | 可能被当成生命周期入口 | ✅ 实际是配置/Gate/参数核对页（角色正确，但缺少自述）|
| ops-playbook | 可能被当成决策入口 | ✅ 实际是执行流程页（角色正确，但 meta 缺失）|
| ops-glossary | 可能被当成帮助中心 | ✅ 实际是术语定义页（角色正确，但 meta 缺失）|
| single-chain-ops | 可能被当成首页 | ✅ 实际是运营入口（角色正确，但缺 meta 自述）|

**结论**：页面角色实际定位正确，但 meta 自述缺失导致用户无法快速判断页面职责。

---

## 八、统一口径基线（已建立）

详见 `docs/OPS_COPY_BASELINE_V1.md`，核心内容：

- **当前统一状态主线**：
  `V7 基线冻结 / 小范围月度试用等待触发 / 十页入口可用 + 页面主次可区分 + 核心三页默认闭环可用 + 辅助页单跳深查可用 + 深查回收闭环可用 + 默认停点可判断 + 新输入最小响应可用 + 日常值班最小巡检可用 + 值班结果可输出 + 需要拍板时可最小升级 + 拍板回复可最小回写 + 生命周期总览可统一解释 + 典型场景可快速套用 + 相似场景边界可快速区分 + 全站口径一致性已收口 / 第二链路冻结`

- **页面角色标准写法**：
  - 核心层：首页总入口 / 状态快报 / 单链路运营入口
  - 辅助层：决策助手 / 执行流程 / 配置快照 / 证据入口
  - 索引层：术语口径 / 真源登记 / 角色路径

- **七阶段标准写法**：等待态(W) / 轻响应态(L) / 评估态(A) / 准备态(P) / 升级态(E) / 回复吸收态(R) / 回收停点(S)

- **统一短句**：
  - V7 基线冻结 / 小范围月度试用等待触发
  - 第二链路冻结（结构性来源候选由人工评估，不自动解冻）
  - RUN-next 由人工确认，V7 基线冻结
  - 轻微信号 ≠ 评估项（留痕即可）
  - 补材料 ≠ 否决（信息不够，补完可继续）
  - 暂不推进 ≠ 否决（维持等待，可再提）
  - 来源候选 ≠ 解冻（候选≠可用）
  - 同意准备 ≠ RUN-next 已开启（V7 基线冻结）

---

## 九、修复动作清单

| 优先级 | 动作 | 涉及页面/文档 |
|--------|------|------------|
| P0 | 将 config-status.html 更新至 P3-38（版本号 + footer + meta 区块 + 状态横幅 + footer-nav）| config-status.html |
| P0 | 将 ops-playbook.html 更新至 P3-38（版本号 + footer + meta 区块）| ops-playbook.html |
| P0 | 将 ops-glossary.html 更新至 P3-38（版本号 + footer + meta 区块 + footer-nav）| ops-glossary.html |
| P0 | 为 single-chain-ops.html 添加 footer-nav（十页导航）| single-chain-ops.html |
| P0 | 为 ops-evidence.html 添加 footer-nav（十页导航）| ops-evidence.html |
| P1 | 清理 single-chain-ops.html 过时的 P3-31/P3-33 注释标记 | single-chain-ops.html |
| P1 | 清理 ops-evidence.html 过时的 P3-4~P3-10 注释标记 | ops-evidence.html |
| P1 | 为 config-status.html 增加统一状态横幅（与其他九页对齐）| config-status.html |
| P2 | 更新 STAGE2_SINGLE_CHAIN_STATUS.md（追加第四十一节 P3-39）| STAGE2_SINGLE_CHAIN_STATUS.md |
| P2 | 更新 FEEDBACK_TRACKING_STATUS.md（P3-39 状态）| FEEDBACK_TRACKING_STATUS.md |
| P2 | 更新 REVIEW_LOG.md（R-102）| REVIEW_LOG.md |
| P2 | 更新 CHANGE_CONTROL.md（CC-89）| CHANGE_CONTROL.md |

---

## 十、审计结论

1. **硬冲突**：未发现。状态主线、七阶段定义、V7 冻结描述在所有页一致。
2. **软漂移**：3个页面版本严重落后（config-status P3-29 / ops-playbook P3-29 / ops-glossary P3-25），4个页面缺少 footer-nav，3个页面缺少 meta 信息区块。
3. **重复堆叠**：footer 中 V7 基线描述略有重复，不影响使用，暂不处理。
4. **模块顺序**：4个页面缺少 footer-nav，与其他六页不一致，需要对齐。
5. **页面角色**：所有页面角色定位正确，但部分页面缺少自述 meta。
6. **推荐方案**：方案B（审计 + 版本更新 + nav 补齐 + meta 补齐 + 跟踪文档同步），不做大规模重构。
