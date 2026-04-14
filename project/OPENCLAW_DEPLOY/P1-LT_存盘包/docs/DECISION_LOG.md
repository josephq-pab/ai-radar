# DECISION_LOG.md — Phase 3 关键决策记录

> 文档版本：v1.4（本次更新：增加 D-08 P1-1 状态持久化方案决策）
> 版本历史：
> - v1.0（2026-04-07）：初建
> - v1.1（2026-04-07）：增加 CC 编号映射，与 CHANGE_CONTROL v1.1 对齐
> - v1.2（2026-04-07）：增加 D-06 路径统一决策（P0-2 实施中发现并解决）
> - v1.3（2026-04-07）：增加 D-07 状态重置边界说明（P0-3 实施后记录）
> - v1.4（2026-04-07）：增加 D-08 P1-1 状态持久化方案决策（P1-1 实施前设计校准）
> 最近更新：2026-04-07
> 对应阶段：Phase 3 — 试点运营化 / MVP闭环

---

## 决策记录列表

---

### 决策 D-01

- **日期**：2026-04-07
- **决策事项**：微信公众号爬取方案降为 Backlog
- **背景**：用户要求推进 B 面（scraping 改写爬取公众号）。调研发现：搜狗微信 follow 跳转全部被 antispider 拦截；mp.weixin.qq.com URL 含加密 token 无法预测；wechatsogou 库 pip 安装超时不可用
- **备选方案**：
  1. 继续研究 wechatsogou 安装方案
  2. 手动维护公众号 URL 白名单
  3. 切换为苏商银行研究院（sif.suning.com）作为替代来源
- **最终选择**：方案3
- **选择原因**：苏商银行平台可访问、内容高质量、工程上完全可行；微信公众号壁垒在无外部依赖下不可解
- **放弃原因**：方案1 wechatsogou 安装超时，方案2需要人工维护 URL 白名单不可持续
- **对后续影响**：analyst_sources.json 新增 4 个苏商银行来源；微信公号在 wechatsogou 可用前不再主动推进
- **是否需要复查**：是（条件：wechatsogou 安装问题解决或有用户提供可抓取 URL 白名单）
- **对应 CC 编号**：CC-06（延后）

---

### 决策 D-02

- **日期**：2026-04-07
- **决策事项**：sif.suning.com profile 发现逻辑优先于 seedUrls
- **背景**：薛洪言等分析师的 profile 页（sif.suning.com/author/detail/8002）有完整文章列表，但 seedUrls 只有 1 条旧文章；旧版脚本只看 seedUrls，不解析 profile 页
- **备选方案**：
  1. 继续用 seedUrls，profile URL 仅作参考
  2. seedUrls 为空时自动从 profile 发现文章列表
- **最终选择**：方案2
- **选择原因**：最小干预原则；不改现有 seedUrls 逻辑，只在 seedUrls 为空时触发 profile 发现；避免对已有 seedUrls 的来源造成意外影响
- **放弃原因**：方案1无法利用 profile 页的完整文章列表
- **对后续影响**：薛洪言/孙扬已清空 seedUrls，触发 profile 发现；新增分析师均使用 profile 发现
- **是否需要复查**：否（逻辑简单稳定）
- **对应 CC 编号**：CC-07（已批准）

---

### 决策 D-03

- **日期**：2026-04-07
- **决策事项**：内容提取优先专有内容区 class（f-article-content），兜底用段落列表
- **背景**：sif.suning.com 文章在 `<div class="f-article-content">` 完整渲染，但旧版脚本用 `find_all('p')` + >30字过滤，导致所有文章内容为 0 字
- **备选方案**：
  1. 先尝试找 f-article-content 类 div，找不到再用段落列表
  2. 直接用完整 HTML 文本
  3. 调整段落 >30 字过滤阈值
- **最终选择**：方案1
- **选择原因**：f-article-content 是该平台标准内容容器，直接定位最准确；保留兜底逻辑兼容其他平台
- **放弃原因**：方案2太粗暴，会引入大量噪音；方案3阈值调整无法根本解决问题
- **对后续影响**：fetch_analyst_articles.py 中 fetch_url() 函数内容提取逻辑已修改
- **是否需要复查**：否（提取结果已验证，3832字成功）
- **对应 CC 编号**：CC-08（已批准）

---

### 决策 D-04

- **日期**：2026-04-07
- **决策事项**：Gate A 数据缺失不作为 Phase 3 主线任务
- **背景**：贷款利率数据 observedAt 停留在 2025-12-01，需要 2026-03 数据才能解除 Blocked 状态
- **备选方案**：
  1. 继续投入时间寻找 2026-03 数据来源
  2. 接受现状，在前端/报告中标注数据截止月份
  3. 用估算值临时替代
- **最终选择**：方案2
- **选择原因**：外部数据供给依赖非系统层可控因素；文档标注法不影响 MVP 闭环推进；避免在不可控事项上消耗 sprint 资源
- **放弃原因**：方案1持续消耗资源但无解；方案3影响数据准确性
- **对后续影响**：OPEN_ISSUES.md 中记录为外部依赖事项；前端/报告需有数据截止月份标注
- **是否需要复查**：是（外部数据到位时重新评估）
- **对应 CC 编号**：CC-09（已批准）

---

### 决策 D-05

- **日期**：2026-04-07
- **决策事项**：Phase 3 不做界面精致化，优先结构治理
- **背景**：用户指令明确"不以界面精致化替代结构治理"
- **备选方案**：
  1. 前端改版，提升视觉表现
  2. 专注输出分层、周期管理、角色视图等结构问题
- **最终选择**：方案2
- **选择原因**：Phase 3 性质是试点运营化，结构稳定比视觉好看更重要；界面精致化是锦上添花，不是 MVP 必需
- **放弃原因**：方案1在结构问题未解决前优先级不足
- **对后续影响**：前端改版计划移入 Backlog
- **是否需要复查**：否（与用户指令一致）
- **对应 CC 编号**：CC-10（已批准）

---

### 决策 D-06

- **日期**：2026-04-07
- **决策事项**：build_analyst_opinions.py 路径与 fetch_analyst_articles.py 路径统一
- **背景**：P0-2 实施中发现 build_analyst_opinions.py 的 BASE 指向 `BASE/data/processed/`（symlink到station工作区），而 fetch_analyst_articles.py 写入 `BASE/04_数据与规则/processed/`。两个路径指向不同文件（7条 vs 79条）。
- **备选方案**：
  1. 修改 fetch 使其写入 `BASE/data/processed/`（需要改 fetch_analyst_articles.py PROCESSED 路径）
  2. 修改 build 使其读取 `BASE/04_数据与规则/processed/`（只改 build）
  3. 保持 fetch 写 04_数据与规则/，统一 build 的 OUTPUT 到同一路径
- **最终选择**：方案3
- **选择原因**：fetch_analyst_articles.py 已稳定运行，写入 04_数据与规则/ 是实际数据位置；build 的 OUTPUT 只要指向同一位置即可，不需要改 fetch
- **修正内容**：
  - PROCESSED = BASE / '04_数据与规则' / 'processed'（原为 data/processed）
  - SOURCES_CONFIG = BASE / '04_数据与规则' / 'analyst_sources.json'（原为 config/analyst_sources.json，不存在）
  - OUTPUT = PROCESSED / 'analyst_opinions.json'（更新路径前缀）
- **对后续影响**：所有后续脚本均以 04_数据与规则/ 为准；station 工作区（data symlink 目标）不再写入
- **是否需要复查**：否（路径统一为一次性修正）
- **对应 CC 编号**：无（CHANGE_CONTROL 中无需新增，属于实施中必要修正）

---

### 决策 D-07

- **日期**：2026-04-07
- **决策事项**：reviewStatus / trackingStatus 状态重置边界说明
- **背景**：P0-3 实施中，为 M4b 演示在 analyst-review-queue.json 中增加了 reviewStatus 和 trackingStatus 字段。运营编辑者操作这些字段修改后，若重新运行 build_analyst_opinions.py，所有状态将被重置为初始值（pending/candidate）。
- **决策结论**：明确记录此边界限制，不试图在 Phase 3 MVP 阶段解决持久化问题。
- **边界说明**：
  - analyst-review-queue.json 中的 reviewStatus / trackingStatus 是"演示用状态字段"
  - 每次重新运行 build_analyst_opinions.py，所有 reviewStatus → pending，trackingStatus → candidate/pending
  - 状态持久化需要独立存储（如数据库或独立 JSON），不在当前 Phase 3 MVP 范围内
  - P1-1 追踪表建立后，可能引入独立的 review 状态存储机制
- **是否需要复查**：否（边界明确，MVP 阶段不做持久化）
- **对应 CC 编号**：无（范围已知，不触发变更控制）

---

### 决策 D-08

- **日期**：2026-04-07
- **决策事项**：P1-1 状态持久化方案决策
- **背景**：P1-1 实施前设计校准中发现三个候选方案：A（原文件内merge）/B（独立状态台账）/C（纯手工维护）。D-07 已确认"重新 build 会重置状态"是当前 MVP 的核心体验断点。
- **候选方案比较**：
  - 方案A（build 内 merge）：build 职责不纯净，review 状态与构建输出耦合
  - 方案B（独立台账）：职责分离，不改 build，tracker 独立持久化
  - 方案C（纯手工）：最稳但自动化程度低，不适合试点
- **最终选择**：方案B（独立状态台账型）
- **选择原因**：
  1. build 的评分/分层/输出职责保持纯净
  2. review 状态与 queue 分离，解释链清晰
  3. tracker 独立于 build，不因重新 build 而覆盖
  4. itemId（dedupKey[:8]）经两次连续 build 验证，跨 build 稳定，可作为关联键
- **方案B 实施口径**：
  - 新增 `reports/review-tracker.json`（状态台账）
  - 新增 `05_工具脚本/review-tracker.py`（upsert + merge）
  - analyst-review-queue.json 保持 build 纯输出，不修改
  - merge 时：tracker 覆盖 queue 的 reviewStatus/trackingStatus，queue 其他字段保留
- **对后续影响**：P1-1 的 fetch-run-log 追踪表与 review-tracker 是两个独立台账，各自独立维护
- **是否需要复查**：否（方案明确，实施已验证）
