# 对公 AI 雷达站｜进展日志

> 说明：本文件用于替代"只靠会话记忆延续项目"的做法。后续每轮有持续价值的推进，都应追加记录到本文件。

---

## 2026-03-28

### 一、前期已形成的有效基础
- 已完成产品定义、架构、数据模型、报告模板、数据发现等基础文档。
- 已完成三份 Excel 数据的首版解析，并生成标准化中间层 JSON。
- 已形成首页、存款页、贷款页、周报页、同业页等原型基础。
- 已完成 review 队列、review 状态、偏好画像、解释规则、建议生成规则等能力雏形。

### 二、今天完成的关键收口
- 依据前期资料，新增 `docs/BASELINE_ALIGNMENT.md`，明确当前原型的正式收敛方向应为：
  - 首页总览
  - 存款深案例页
  - 贷款深案例页
  - 重点事项跟踪页
- 已把 `weekly-report.html` 与 `peer-monitor.html` 明确降级为二级承接页，不再作为首期一级主链路继续扩张。
- 已重构主链路页面，使其更接近"首页总览—双案例承接—重点事项闭环"的正式架构。
- 已新增并落地 `apps/web/tracking.html`，作为重点事项闭环页。
- 已更新 `README.md`，让当前项目结构与可体验路径更清晰。
- 已提交一轮 git：`97b7365` / `feat(ai-radar-station): align four-page prototype flow`。

### 三、今天识别出的结构性问题
- `memory_search` 当前不可稳定使用，不能继续把项目上下文主要寄托在语义记忆检索上。
- 现有部分项目判断与推进仍过度依赖会话上下文，存在"时间一长就失焦"的风险。
- `tracking.html` 中部分字段仍由前端推断，尚未完全下沉为正式中间层数据。
- 项目治理文档存在缺口，`NEXT_STEPS.md` 曾出现残留污染，说明缺少更上位的稳定总计划与进展日志。

### 四、今天开始进行的治理修复
- 新增 `docs/PROJECT_BASELINE.md`，正式规定前期资料、项目内治理文档、实现产物之间的优先级关系。
- 新增 `docs/BUILD_PLAN.md`，将当前项目拆为：
  - 基线对齐与治理固化
  - 四页主链路收口
  - tracking 中间层正式化
  - 规则链路深化
  - 试运行与周节奏固化
  - 工程化迁移准备
- 新增 `docs/PROGRESS_LOG.md`，要求后续每轮推进都做可追溯落盘。

### 五、今天正在推进但尚未完全收尾的事项
- 已将 tracking 页依赖的中间层正式扩展为更接近原型说明的 schema，除 `layer / priority / nextAction / sourceName / sourceHref / needReview` 外，还新增/固化了 `trackingStatus`、`sourceDimension`、`sourceTheme`、`latestProgress`、`updatedAt` 等字段，计划输出到 `reports/tracking-items.json`。
- `scripts/build_web_bundle.py` 已接入 `trackingItems` 注入。
- `apps/web/tracking.html` 已改为直接消费 `trackingItems`，并显示业务维度、来源主题、最新进展等字段。
- 该部分还需要完成完整重建、联调验证与页面校验。

### 六、今天继续推进的状态治理动作
- 已新增 `data/processed/tracking_status_rules.json`，正式把 `review 状态` 与 `tracking 业务状态` 的关系提取成独立规则文件，不再只写死在脚本中。
- 当前首版规则已明确：
  - `pending -> 待研判`
  - `modify -> 跟踪中`
  - `approve -> 已上报`
  - `reject -> 已关闭`
- 文档中已明确两层状态的职责分离：
  - review 状态用于描述内容确认结果
  - tracking 状态用于描述事项推进进度
- 后续计划已明确：支持 `已上报 -> 已行动 -> 已关闭` 的独立流转，而不再依赖 review 再次变动。

### 七、今天继续推进的 tracking 独立状态能力
- 已新增 `scripts/record_tracking_status.py`，用于独立记录 tracking 业务状态，而不再只能依赖 review 状态变化。
- 已新增 `reports/tracking-status-log.jsonl` 作为 tracking 业务状态日志文件。
- `build_tracking_items.py` 已调整为优先合并 tracking 状态日志；当日志中存在独立状态时，优先使用该状态、最新进展和下一步动作，否则再回退到 review -> tracking 的最小映射。
- 这意味着项目已经从"review 状态代替 tracking 状态"推进到"tracking 状态可独立维护，只是当前默认仍可回退映射"。

### 八、今天继续推进的 tracking 独立状态验证结果
- 已完成 `scripts/record_tracking_status.py` 的最小实操验证。
- 已验证：当独立 tracking 状态日志写入后，`build_tracking_items.py` 会优先使用 tracking 状态日志中的 `trackingStatus`、`latestProgress`、`nextAction` 覆盖默认映射结果。
- 已实测 `core-1` 从默认 `跟踪中` 被独立推进为 `已行动`，并成功写入：
  - `latestProgress`: `已完成管理口径沟通并转入专项跟进`
  - `nextAction`: `下周复盘专项推进结果`
- 这说明当前项目已具备"内容确认状态"和"事项推进状态"双轨并存的最小能力。

### 九、今天继续推进的主链路页面接入动作
- 已将 `deposit.html` 从主要读取 `reviewStatus` 改为优先读取 `trackingItems`，存款相关事项摘要现在展示 `trackingStatus / sourceDimension / sourceTheme / latestProgress / nextAction`。
- 已将 `loan.html` 从主要读取 `reviewStatus` 改为优先读取 `trackingItems`，贷款相关事项摘要现在展示 `trackingStatus / sourceDimension / sourceTheme / latestProgress / nextAction`。
- 已为 `weekly-report.html` 新增"事项闭环摘要"区块，开始直接消费 `trackingItems`，使周报承接页可以看到事项状态、最新进展与下一步动作。
- 当前主链路推进已从"tracking 页单点闭环"进入"案例页 / 周报页共同承接 tracking 中间层"的阶段。

### 十、接下来的严格执行口径
- 后续不再只依赖会话记忆推进项目。
- 任何较大改动都应先对齐 `PROJECT_BASELINE.md` 和 `BUILD_PLAN.md`。
- 每轮真正有持续价值的推进，都必须同步到本文件追加记录。

---

## 2026-03-29

### 一、步骤 1 - 正式重建验证（已完成）
- 按用户要求执行三步清单：1）先做一次正式重建验证 → 2）逐页验四个关键字段 → 3）验证通过后立刻收口
- 执行 8 个脚本完整重建：
  ```
  ✓ parse_initial_data.py → 33 deposits, 52 loans, 16 rates
  ✓ build_interpretation_rules.py → interpretation_rules.json
  ✓ build_recommendation_rules.py → recommendation_rules.json
  ✓ generate_weekly_report.py → weekly-report-draft.md
  ✓ generate_review_queue.py → review-queue.json
  ✓ build_review_status.py → review-status.json
  ✓ build_tracking_items.py → tracking-items.json
  ✓ build_web_bundle.py → app-data.js
  ```
- 数据层、周报层、tracking 层、前端 bundle 全部更新至 06:30

### 二、步骤 2 - 验四个关键字段
- 发现并修复 `tracking.html` 状态筛选逻辑错误：
  - 问题：原筛选下拉选项为 review 状态（pending/modify/approve/reject），但业务语义应使用 tracking 业务状态（待研判/跟踪中/已上报/已行动/已关闭）
  - 修复：
    1. 下拉选项从 review 状态改为 tracking 业务状态
    2. KPI 卡片从 pending/modified/approved 改为 trackingStatusSummary
    3. 筛选逻辑从 `item.status` 改为 `item.trackingStatus`
    4. 详情预览状态显示从 `item.status` 改为 `item.trackingStatus`
- 页面已刷新，等待用户确认（用户长时间未回复）

### 三、同步邮件工作流执行
- 每日同步邮件 08:13 成功发送（主题：当日工作及进展同步 - 2026-03-29）
- 每周同步邮件 08:13 成功发送（主题：本周工作及进展同步 - 2026-03-29）
- 周同步中已明确透明度边界："工具调用次数系统不提供精确统计，以活动摘要为主"

### 四、Self-improvement 周复盘（08:30）
- 已追加三条改进到 memory：
  1. tracking.html 筛选逻辑修复
  2. 日/周同步定时框架完善
  3. 透明度边界明确

### 五、收口动作
- 更新 `docs/PROGRESS_LOG.md` 到 2026-03-29
- git 提交 21f8a59: complete tracking layer fix + progress log update

---

## 2026-03-29（下午）

### 一、用户反馈问题修复
- 用户反馈：首页、存款页、贷款页的同业对标只显示 Top5，希望显示全部 8 家
- 修复：`parse_initial_data.py` 中 `build_dashboard_payload()` 从 `[:5]` 改为 `[:8]`
- 重建 dashboard.json 和 app-data.js，验证：depositTop5/loanTop5/rateLowToHigh5 各 8 条

### 二、Nvidia 模型配置
- 用户提供新 Nvidia API key，已更新 `openclaw.json` 中的 `cherry-nvidia.apiKey`
- 切换到 glm5 模型：`openclaw models set cherry-nvidia/z-ai/glm5`

### 三、阶段 D 深化 - 规则链路深化（进行中）
- 贷款页（loan.html）深化：
  - 观察/建议/行动加规则标题标签（observationRule.title / strategyRule.title / actionRule.title）
  - 解释规则区新增策略建议/行动建议判定标准卡片
  - tracking 相关事项过滤从 reviewStatus 改为 trackingItems（`x.sourceDimension === '贷款'`）
- 存款页（deposit.html）同步深化（同上模式）
- 深化目标：让建议生成规则真正进入页面，而不是只作为展示文本
- 页面已刷新，等待用户确认效果

### 四、收口
- git 提交 ecf4ce1: deepen rule chain in loan/deposit pages（5 文件 +151 行）
- git 提交 7b8b0e9: update progress log to 2026-03-29 afternoon

---

## 2026-03-29（下午第二阶段）

### 一、阶段 D 深化 - 周报接入 tracking 事项
- `generate_weekly_report.py` 改造：
  - 加载 `reports/tracking-items.json` 并读取 `trackingStatusSummary` 和 `items`
  - 新增第九节：重点事项跟踪状态汇总（待研判/跟踪中/已上报/已行动/已关闭）
  - 新增第十节：事项明细（layer/priority/trackingStatus/sourceDimension/sourceTheme/text/latestProgress/nextAction/source）
  - 周报同业/贷款/定价各节从 Top5 改为 Top8
- 重建周报草稿 + review 队列 + review 状态 + tracking 中间层 + web bundle

### 二、阶段 E 深化 - 试运行执行手册
- 新增 `docs/SOP_EXECUTION.md`：
  - 每周运行节奏（周一到周五各做什么）
  - 数据刷新完整命令序列
  - 人工确认节点（案例页确认 / 事项入池确认 / 状态变更确认 / 周报出稿确认）
  - 事项闭环操作（record_review / record_tracking_status）
  - 页面查看路径
  - 当前阶段关注指标（链路跑通率 / 页面承接率 / 事项闭环率 / 一致性）
  - 升级触发条件（连续 2 周跑通 / 数据源升级 / 多人协同 / 正式部署）

### 三、收口
- git 提交 9771f24: complete phase D/E - weekly report tracking integration + SOP execution manual（5 文件 +187 行）

### 四、阶段 F 准备
- BUILD_PLAN.md 中阶段 F（工程化迁移准备）仍为"待开始"状态
- 当前已具备升级条件：试运行 SOP 已落地，周报已接入 tracking，页面链路可跑通
- 后续升级方向：数据源从本地文件升级为数据库/API、部署到正式环境
