# CONFIG_OBJECT_INVENTORY_V1.md — 配置对象清单

> 档案编号：CFG-INV-01
> 文档版本：v1.0（新建）
> 编制日期：2026-04-16
> 对应阶段：P3-1（配置优先 — 配置对象盘点）
> 状态：**配置对象基线文档 v1.0**

---

## 一、配置对象分类总览

| 类别 | 包含配置项数 | 集中程度 |
|------|------------|---------|
| A. 来源配置 | 9项 | ✅ 集中（analyst_sources.json）|
| B. 运行配置 | 7项 | ⚠️ 部分分散 |
| C. 规则配置 | 6项 | ⚠️ 硬编码为主 |
| D. Gate/展示配置 | 5项 | ⚠️ 部分分散 |
| E. 路径配置 | 1项 | ✅ 集中（paths.py）|

---

## 二、来源配置（A类）

**当前唯一来源**：`data/analyst_sources.json`

| # | 配置项 | 字段路径 | 是否散落 | 是否纳入第一期 | 备注 |
|---|------|---------|---------|--------------|------|
| A1 | 来源列表 | sources[] | ❌ 集中 | ✅ 必须 | 9个来源，8激活1停用 |
| A2 | 来源启停 | sources[].active | ❌ 集中 | ✅ 必须 | |
| A3 | seedUrls | sources[].seedUrls | ❌ 集中 | ✅ 必须 | 含 status/inactive 说明 |
| A4 | profileUrl | sources[].profileUrl | ❌ 集中 | ✅ 必须 | |
| A5 | 维度标签 | sources[].dimension | ❌ 集中 | ✅ 必须 | 对公存款/贷款/整体 |
| A6 | 优先级 | sources[].priority | ❌ 集中 | ✅ 建议 | high/medium |
| A7 | crawlMode | sources[].crawlMode | ❌ 集中 | ⚠️ 可后置 | auto/semi |
| A8 | quarantine 信息 | sources[]._quarantine | ❌ 集中 | ⚠️ 可后置 | 仅来源失效时需要 |
| A9 | 标签（tags）| sources[].tags | ❌ 集中 | ❌ 不纳入 | 太细，非核心配置 |

---

## 三、运行配置（B类）

| # | 配置项 | 当前落点 | 是否散落 | 是否纳入第一期 | 备注 |
|---|------|---------|---------|--------------|------|
| B1 | BASE 路径 | paths.py | ❌ 集中 | ✅ 已有（隐含）| 不需要展示 |
| B2 | 输出路径（REPORTS）| paths.py | ❌ 集中 | ✅ 已有（隐含）| 不需要展示 |
| B3 | 运行入口 | 05_工具脚本/run-analyst.sh | ⚠️ 分散 | ✅ 纳入口状态页 | |
| B4 | top-k 默认值 | build_analyst_opinions.py（代码）| ⚠️ 硬编码 | ✅ 必须 | 当前默认=5 |
| B5 | min-rel 默认值 | build_analyst_opinions.py（代码）| ⚠️ 硬编码 | ✅ 建议 | 当前默认=0.4 |
| B6 | dry-run 模式 | 脚本参数 | ⚠️ 分散 | ✅ 纳入口状态页 | |
| B7 | dim-trial 模式 | 脚本参数 | ⚠️ 分散 | ⚠️ 可后置 | 当前仅试探用 |

---

## 四、规则配置（C类）

| # | 配置项 | 当前落点 | 是否散落 | 是否纳入第一期 | 备注 |
|---|------|---------|---------|--------------|------|
| C1 | B gate 阈值 | rebuild_go_live_gate.py（代码）| ⚠️ 硬编码 | ✅ 必须 | usable≥3/reportable≥1/garbled=0 |
| C2 | confirmLevel 映射 | build_analyst_opinions.py（代码）| ⚠️ 硬编码 | ✅ 建议（明文化）| P1/P2/P3 规则 |
| C3 | A gate 阈值 | rebuild_c_gate.py（代码）| ⚠️ 硬编码 | ⚠️ 可后置 | 已冻结（外部依赖）|
| C4 | 双门槛（5000万/1000万）| ACTION_EXPRESSION_RULES_V7.md | ❌ 集中 | ✅ 必须（文档层）| |
| C5 | 三档条件 | ACTION_EXPRESSION_RULES_V7.md | ❌ 集中 | ✅ 必须（文档层）| |
| C6 | 主体角色规则 | ACTION_EXPRESSION_RULES_V7.md | ❌ 集中 | ✅ 必须（文档层）| |

---

## 五、Gate/展示配置（D类）

| # | 配置项 | 当前落点 | 是否散落 | 是否纳入第一期 | 备注 |
|---|------|---------|---------|--------------|------|
| D1 | Gate A 状态 | reports/go-live-gate.json | ❌ 集中 | ✅ 必须 | 当前 blocked（rate数据旧）|
| D2 | Gate B 状态 | reports/go-live-gate.json | ❌ 集中 | ✅ 必须 | 当前 cleared |
| D3 | Gate C 状态 | reports/go-live-gate.json | ❌ 集中 | ✅ 必须 | 当前 passed |
| D4 | 当前内容基线版本 | TRIAL_BASELINE_FREEZE_V7.md | ❌ 集中 | ✅ 必须 | V7，当前冻结 |
| D5 | 当前试用对象与周期 | TRIAL_SEND_PACK_V7.md + PILOT_CYCLE_PLAN_V1.md | ⚠️ 分散 | ✅ 必须 | 赵总/曾总/邱非 |

---

## 六、路径配置（E类）

| # | 配置项 | 当前落点 | 是否散落 | 是否纳入第一期 | 备注 |
|---|------|---------|---------|--------------|------|
| E1 | 所有路径定义 | paths.py | ❌ 集中 | ✅ 已有（隐含）| 不需要展示 |

---

## 七、散落程度评估

| 散落类型 | 严重程度 | 现状描述 |
|---------|---------|---------|
| 来源配置 | — | ✅ 完全集中，analyst_sources.json 是唯一来源 |
| 路径配置 | — | ✅ 完全集中，paths.py 是唯一路径定义 |
| 规则阈值 | **高** | ⚠️ top-k / min-rel / B gate 阈值在 Python 代码里硬编码，调整需要改代码 |
| 试用状态 | 中 | ⚠️ 分散在多个 Markdown（基线冻结/试用周期/发送包）|
| 运行入口 | 低 | ⚠️ run-analyst.sh 是统一入口，但还有 run-pipeline.py 旧入口 |

**最大缺口**：**top-k / B gate 阈值在代码里硬编码**——调整需要改代码，有破坏风险，且无变更记录。

---

## 八、第一期纳入清单汇总

| 纳入项 | 来源 | 展示位置 |
|--------|------|---------|
| A1~A6 | analyst_sources.json | 配置状态页 |
| B3~B5 | 脚本参数 / 代码 | 配置状态页（明文化当前值）|
| C1~C2 | 代码 | 配置状态页（明文化当前值）|
| C4~C6 | Markdown 文档 | 配置状态页（引用文档路径）|
| D1~D3 | go-live-gate.json | 配置状态页 |
| D4~D5 | Markdown 文档 | 配置状态页（引用文档路径）|

---

*记录：AI雷达站 agent，2026-04-16 15:50 GMT+8（P3-1 配置对象盘点）*
