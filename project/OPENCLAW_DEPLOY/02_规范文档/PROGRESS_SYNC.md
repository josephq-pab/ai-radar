# 对公 AI 雷达站｜进展同步与意见征求

**文档日期：** 2026-03-30
**发送方：** 邱非 / Sylvia
**用途：** 新成员同步 + 征求意见
**状态：** 主动征询

---

## 一、项目背景与目标

### 背景
对公业务（公司银行业务）一直是银行的核心板块，但目前缺乏一个系统化、可更新的"AI 增强型跟踪工具"，能够：
- 持续跟踪同业动态与对标数据
- 快速生成对公相关的结构化分析（存款/贷款/定价）
- 把分析结论转化为可执行的重点事项跟踪

### 目标
在 OpenClaw（AI 工作环境）内搭建"对公 AI 雷达站"，实现：
1. **数据链路可重建**：从原始 Excel → 中间层 JSON → 前端页面，随时可刷新
2. **分析链路可解释**：观察/策略/行动建议由规则生成，非硬编码
3. **事项链路可闭环**：分析结论 → tracking 事项 → 状态更新 → 周报承接
4. **后续可迁移**：原型底座可拆解迁移到正式环境（服务器/API/数据库）

### 核心用户
- 对公业务负责人（邱非）
- 主要使用方式：每日/每周刷新 + 随时查看存款/贷款/tracking 页

---

## 二、当前已完成的成果

### 2.1 页面体系（六页）

| 页面 | 定位 | 说明 |
|------|------|------|
| `index.html` | 首页总览 | 存款/贷款/定价三维度 Top8 同业对标 + 重点事项摘要 |
| `deposit.html` | 存款深案例 | 存款对标 + 观察/策略/行动建议 + 存款相关 tracking 事项 |
| `loan.html` | 贷款深案例 | 贷款对标 + 观察/策略/行动建议 + 贷款相关 tracking 事项 |
| `tracking.html` | 重点事项跟踪 | 全部 tracking 事项的状态、进展、下一步动作 |
| `weekly-report.html` | 周报承接页 | 完整周报草稿 + tracking 状态汇总 |
| `peer-monitor.html` | 同业分析承接 | 同业对标详细数据 |

路径：`projects/ai-radar-station/apps/web/`

### 2.2 数据中间层

| 文件 | 内容 |
|------|------|
| `deposit_benchmark.json` | 存款同业数据（33家银行，按平安视角排名） |
| `loan_benchmark.json` | 贷款同业数据（52家银行） |
| `loan_rate.json` | 贷款利率数据（16家银行） |
| `dashboard.json` | 首页三维度 Top8 同业对标汇总 |
| `analyst_opinions_raw.json` | 外部分析师观点原始抓取结果 |
| `analyst_opinions.json` | 筛选后的高价值分析师观点 |

### 2.3 规则中间层

| 文件 | 内容 |
|------|------|
| `interpretation_rules.json` | 观察判定规则（什么样的数据特征构成什么样的观察结论） |
| `recommendation_rules.json` | 建议生成规则（观察结论 → 策略建议 → 可执行行动） |
| `tracking_status_rules.json` | tracking 业务状态映射规则 |
| `preference_profile.json` | 报告偏好画像（语言风格/结构偏好） |
| `section_preferences.json` | 各节内容偏好（存款/贷款/同业/定价） |
| `domain_templates.json` | 领域报告模板 |

### 2.4 分析与事项链路

| 文件 | 内容 |
|------|------|
| `review-queue.json` | 待确认事项队列（来自规则生成的分析结论） |
| `review-status.json` | 事项确认状态（pending/modify/approve/reject） |
| `tracking-items.json` | tracking 事项汇总（含业务状态/进展/下一步动作） |
| `weekly-report-draft.md` | 本周周报草稿（九节完整版） |
| `review-log.jsonl` | 事项确认历史日志 |
| `tracking-status-log.jsonl` | tracking 业务状态变更日志 |

### 2.5 脚本工具链（8个）

```
parse_initial_data.py         → 原始 Excel → 中间层 JSON
build_interpretation_rules.py → 观察判定规则构建
build_recommendation_rules.py → 建议生成规则构建
generate_weekly_report.py     → 周报草稿生成
generate_review_queue.py      → review 队列生成
build_review_status.py        → review 状态构建
build_tracking_items.py      → tracking 中间层构建
build_web_bundle.py           → 前端数据包构建

record_review.py              → 记录确认意见（人工操作）
record_tracking_status.py     → 记录 tracking 业务状态变更（人工操作）
fetch_analyst_articles.py     → 外部分析师观点抓取（自动）
```

### 2.6 外部分析师来源（白名单，9位）

| 分析师 | 机构 | 维度 | 优先级 |
|--------|------|------|--------|
| 董希淼 | 招联首席经济学家 | 存款/贷款/整体 | 高 |
| 薛洪言 | 星图金融研究院 | 存款 | 高 |
| 娄飞鹏 | 邮储银行研究员 | 存款/贷款 | 高 |
| 连平 | 广开首席产业研究院 | 存款/整体 | 高 |
| 周茂华 | 光大银行金融市场部 | 存款/贷款 | 中 |
| 温彬 | 民生银行首席经济学家 | 贷款/整体 | 高 |
| 曾刚 | 上海金融与发展实验室 | 贷款/整体 | 高 |
| 朱太辉 | 国家金融与发展实验室 | 整体 | 中 |
| 孙扬 | 星图金融研究院 | 整体 | 中 |

---

## 三、已完成的建设阶段

| 阶段 | 内容 | 状态 |
|------|------|------|
| A | 基线治理文档（PROJECT_BASELINE / BUILD_PLAN / PROGRESS_LOG） | ✅ 完成 |
| B | 四页主链路（首页/存款/贷款/tracking）收口 | ✅ 完成 |
| C | tracking 中间层正式化（规则拆分/独立状态日志） | ✅ 完成 |
| D | 规则链路深化（建议规则进入页面生成） | ✅ 完成 |
| E | 试运行 SOP + 周节奏固化（每日邮件同步） | ✅ 完成 |
| F | 工程化迁移准备 | ⏳ 待开始 |

---

## 四、当前运行节奏

| 时间 | 动作 |
|------|------|
| 每日 08:00 | 日报邮件发送（当日进展同步） |
| 每周 日 08:00 | 周报邮件发送（本周进展同步 + 工具透明度说明） |
| 每周 日 08:30 | Self-improvement 复盘 |
| 工作日随时 | 手动刷新数据：`python3 scripts/*.py` |
| 工作日随时 | 事项确认：`python3 scripts/record_review.py <itemId> <decision> [text]` |
| 工作日随时 | 状态更新：`python3 scripts/record_tracking_status.py <itemId> <status>` |

---

## 五、待解决问题与决策点

### 问题 1：阶段 F 走向（需确认）

当前原型在本地 OpenClaw 环境跑通。阶段 F 工程化迁移方向取决于实际使用场景：

| 选项 | 说明 | 影响 |
|------|------|------|
| A：继续本地运行 | OpenClaw 沙箱作为长期工具，定期手动刷新 | 工程化最浅，快速迭代 |
| B：迁移到内网服务器 | 部署为正式服务，自动化定时刷新 | 需要 API/数据库/服务器，适合多用户 |
| C：其他形式 | 待补充 | — |

### 问题 2：外部分析师来源扩展策略

当前白名单每人仅 1-2 个 seed URL，采集深度不足。接下来：

| 选项 | 说明 |
|------|------|
| A：继续补现有分析师文章 URL | 稳扎稳打，每人多补 3-5 篇高质量文章 |
| B：引入新分析师来源 | 扩大覆盖广度，补充新面孔 |
| C：优先解决微信公号抓取 | 微信是高价值内容集中地，但抓取难度大 |
| D：组合策略 | A+C 结合 |

### 问题 3：试运行节奏评估

当前每日 08:00 发送日报，每周 日 08:00 发送周报。tracking 状态可随时手动更新。

- 节奏是否合适？
- 有无需要增减的节点？
- 事项确认/状态更新的操作成本是否可接受？

### 问题 4：分析与事项的质量标准

当前 review 队列中：
- 有 6 条"待研判"事项（pending）
- 有 1 条"跟踪中"（modify）
- 有 1 条"已行动"（core-1）

质量判断标准尚未正式确立：
- 什么样的结论算"好结论"？
- 什么样的事项值得进入 tracking？
- 什么样的事项应该直接关闭（reject）？

---

## 六、请新伙伴重点关注的点

1. **整体架构**：当前六页面 + 中间层 + 脚本工具链的架构是否合理？有没有明显的缺失或冗余？

2. **规则体系**：观察判定规则 / 建议生成规则是否贴合实际业务判断？有没有需要补充或修正的维度？

3. **分析师来源**：9 位白名单分析师是否覆盖了最重要的声音？有没有我们还没覆盖到的关键人物？

4. **使用体验**：如果你是对公业务负责人，当前页面结构和内容是否能直接用于工作汇报？还是需要大幅调整？

5. **任何你觉得值得指出的问题**：不限于上述范围，欢迎直接指出。

---

## 七、文档与代码路径

```
projects/ai-radar-station/
├── apps/web/              # 前端页面（直接浏览器打开 .html）
├── config/                # 配置（analyst_sources.json）
├── data/
│   ├── processed/         # 中间层 JSON 文件
│   └── raw/               # 原始 Excel 数据
├── docs/                  # 项目文档（PRD / 架构 / 进度 / SOP）
├── reports/               # 运行时输出（review / tracking / 周报）
├── reviews/               # review 操作日志
└── scripts/               # 脚本工具链

workspace/
├── SOUL.md / IDENTITY.md  # 助手配置
├── memory/                # 每日进展日志
└── mail-output/           # 发送的邮件存档
```

---

## 八、联系方式

- 主要使用人：邱非
- 助手：Sylvia（OpenClaw agent）
- 数据刷新：每次新数据到来后运行完整脚本序列
- 事项操作：通过 `record_review.py` 和 `record_tracking_status.py` 记录

---

**请新伙伴在阅读后，针对第五节的四个问题给出意见，以及对第六节的关注点提供反馈。**