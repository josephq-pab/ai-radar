# FRONTEND_COMPONENT_BOUNDARY_RULES_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE5-1（STAGE257）
- **日期**：2026-04-24
- **前提**：PHASE4_BASELINE_FREEZE_NOTE（Phase 4 基线已冻结，不得回退）

---

## 一、组件边界定义原则

### 1.1 组件化目标
将高度重复、结构稳定、职责单一的结构抽象为组件，减少页面间的重复代码，降低后续变更的维护成本。

### 1.2 组件化约束
- **不得破坏页面语义**：用户看到的是页面，不是组件列表
- **不得移除治理语法**：首屏四问、停止条件、支援化表达等治理语法必须保留
- **不得改变层级优先级**：L1 主结论不能因为组件化而被降级

---

## 二、组件候选清单

### 2.1 高优先级抽象（可立即执行）

| 组件名 | 代码 | 对应 Block | 理由 |
|--------|------|-----------|------|
| FirstScreenJudge | COMP-FIRST-SCREEN | SHARED-FIRST-SCREEN | 十页完全一致，可直接抽象 |
| FooterNav | COMP-FOOTER-NAV | SHARED-FOOTER-NAV | 结构固定，参数简单（7/10页）|
| GovernanceFold | COMP-GOVERNANCE-FOLD | SHARED-GOVERNANCE-FOLD | 统一收纳 L5 内容 |
| PageMeta | COMP-PAGE-META | SHARED-META | 版本/角色元信息 |
| SupportLocationBanner | COMP-SUPPORT-BANNER | SHARED-SUPPORT-LOCATION | 支援页专用，格式固定 |

### 2.2 中优先级抽象（Phase 5-2 考虑）

| 组件名 | 代码 | 对应 Block | 理由 |
|--------|------|-----------|------|
| StopConditionBadge | COMP-STOP-BADGE | SHARED-STOP-CONDITION | 口径固定（"即可停止/即可返回"），但条件文本因页而异 |
| EvidenceCard | COMP-EVIDENCE-CARD | ops-evidence 证据块 | 格式固定，但内容差异大 |
| DecisionConclusion | COMP-DECISION-CONCLUSION | ops-decision 结论块 | 三选一格式（执行/等待/升级），可参数化 |

### 2.3 低优先级抽象（暂不处理）

| 组件名 | 代码 | 原因 |
|--------|------|------|
| ActionRouteBlock | COMP-ACTION-ROUTE | 内容因页面差异极大，不适合抽象 |
| SectionBlock | COMP-SECTION | 各页 section 结构差异大 |
| BriefSummary | COMP-BRIEF-SUMMARY | 快报考情内容不适合模板化 |

---

## 三、页面专属内容（禁止组件化）

以下内容为页面语义层，不得抽象为跨页复用组件：

### 3.1 radar-home.html 专属

- 触发条件展示区（首页特有的"有没有事"判断逻辑）
- 进入下一轮运行提示

### 3.2 single-chain-ops.html 专属

- 当前阶段状态展示
- 配置/Gate 确认入口序列
- 证据/决策/流程入口序列

### 3.3 ops-decision.html 专属

- 三选一决策结论（执行/等待/升级）
- 场景判断说明区

### 3.4 ops-playbook.html 专属

- 当前应执行步骤展示
- 执行步骤序列

### 3.5 ops-evidence.html 专属

- 冻结依据展示
- 证据链详情区

### 3.6 ops-brief.html 专属

- 快报核心结论区
- 快报不够用时的跳转指引

### 3.7 ops-routes.html 专属

- 选路结果展示
- 四类角色路径序列

### 3.8 ops-glossary.html 专属

- 术语查询结果展示
- 术语定义内容

### 3.9 ops-registry.html 专属

- 真源查询结果展示
- 对象状态信息

### 3.10 config-status.html 专属

- 配置项状态展示
- 正常/异常结论

---

## 四、组件边界判定规则

### 4.1 适合组件化的判断条件

满足以下**全部条件**时，适合抽象为组件：
1. 该结构在**三页以上**以相同或高度相似格式出现
2. 该结构的职责**单一且稳定**（不随业务内容变化）
3. 该结构的**呈现格式不依赖页面上下文**
4. 抽象为组件后**不影响页面语义的完整性**

### 4.2 不适合组件化的判断条件

满足以下**任一条件**时，不适合抽象为组件：
1. 该结构的**内容由页面业务逻辑决定**（如当前阶段状态）
2. 该结构包含**页面间差异化的判断逻辑**
3. 该结构是**页面语义的核心表达**
4. 抽象后会导致**页面失去上下文可读性**

### 4.3 "半组件半页面"中间状态禁止

禁止出现以下中间状态：
- ❌ 首屏判定区分为"组件部分"和"页面部分"两部分
- ❌ Footer Navigation 部分链接组件化、部分硬编码
- ❌ 治理折叠区组件内又嵌套页面级 details

---

## 五、组件接口设计原则

### 5.1 组件参数原则

```typescript
// Good: 参数少且语义清晰
interface FirstScreenJudgeProps {
  question1: string;  // "现在有没有事"
  question2: string;  // "值不值得继续读"
  question3: string;  // "当前最重要的结论是什么"
  question4: string;  // "下一眼该看哪里"
}

// Bad: 参数过多或过于细化
interface BadFirstScreenJudgeProps {
  bgColor: string;
  paddingTop: number;
  borderRadius: number;
  // ... 过度参数化
}
```

### 5.2 组件 Slots 原则

需要页面差异化内容时，使用 Slot 而非参数：

```html
<!-- Good: 使用 Slot -->
<FirstScreenJudge>
  <ConclusionSlot>等待态正常</ConclusionSlot>
</FirstScreenJudge>

<!-- Bad: 传递过多 HTML 片段 -->
<FirstScreenJudge conclusionHtml="<div>等待态正常</div>" />
```

---

## 六、Phase 5 组件化执行边界

### 6.1 Phase 5-1（当前阶段）范围

**只产出文档，不实际重构代码**：
- ✅ 定义组件边界
- ✅ 标注组件候选
- ✅ 定义接口原则
- ❌ 不实际将 HTML 替换为组件标签

### 6.2 Phase 5-2 及之后

**实际组件化实施**：
- Phase 5-2：FirstScreenJudge / FooterNav / GovernanceFold / PageMeta 四个高优先级组件
- Phase 5-3：StopConditionBadge / SupportLocationBanner
- Phase 5-4：EvidenceCard / DecisionConclusion（视情况）

### 6.3 禁止事项

- ❌ 不得在 Phase 5-1 进行实际组件重构
- ❌ 不得以组件化为由修改已冻结的 Phase 4 页面内容
- ❌ 不得引入新的交互机制或脚本能力
- ❌ 不得改变页面层级优先级

---

## 七、组件化风险控制

| 风险 | 描述 | 控制措施 |
|------|------|---------|
| 过度组件化 | 把不适合抽象的内容强行组件化 | 用 4.2 规则严格判定 |
| 治理语法丢失 | 组件化后首屏四问等语法被稀释 | 治理语法必须作为 Slot 内容保留 |
| 层级破坏 | 组件化导致 L1 被降级 | 组件内不得折叠 L1/L2 内容 |
| 中间状态 | 半组件半页面导致维护困难 | 禁止出现中间状态，要么完整组件化，要么保持页面语义 |
