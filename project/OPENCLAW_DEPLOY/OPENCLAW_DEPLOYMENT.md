# 对公 AI 雷达站 — OpenClaw 部署说明

> 部署包生成时间：2026-04-06
> 生成方：Sylvia
> 用途：迁移至新环境，继续开发

---

## 📦 包内容概览

| 文件夹 | 内容 |
|--------|------|
| `01_项目说明/` | 项目背景、目标、架构、交接文档 |
| `02_规范文档/` | PRD、架构、数据模型、建设计划、试运行 SOP |
| `03_前端页面/` | 7个 HTML 页面 + 前端数据包 |
| `04_数据与规则/` | 原始数据、中间层 JSON、规则文件 |
| `05_工具脚本/` | 全部 Python 脚本（入口脚本 + 工具链） |
| `06_进展状态/` | 当前进度状态、Open Issues、Closure 报告 |
| `07_历史备份/` | 关键历史版本快照 |
| `08_设计规范补充/` | 平安智慧对公设计规范（前端 UI 参照标准） |

---

## 🎯 项目是什么

**对公 AI 雷达站**是一个面向银行对公业务管理部的经营情报与观点研判系统。

**核心功能：**
- 接入同业对标数据（存款/贷款/利率）+ 外部分析师观点 + 政策信息
- 加工成结构化情报，服务人工 review 确认 → 闭环跟踪 → 周报生成

**当前阶段：** 原型 v0.1，已完成 Phase 2 基线收敛，待进入 Phase F（工程化迁移）

**技术栈：** Python 3.9（非 3.10+）+ BeautifulSoup4 + Scrapling 0.2.99 + 静态 HTML/JS

---

## ⚡ 快速启动（30分钟内可看到页面）

### 步骤 1：安装依赖

```bash
# Python 依赖
pip3 install beautifulsoup4 scrapling openpyxl

# 或一键安装
pip3 install -r requirements.txt
```

### 步骤 2：构建前端数据包

```bash
cd 05_工具脚本
python3 scripts/build_web_bundle.py
```

### 步骤 3：打开页面

```bash
# 直接在浏览器打开
open ../03_前端页面/index.html
# 或
open 03_前端页面/index.html
```

按以下顺序体验：
1. `index.html` — 首页总览
2. `deposit.html` — 存款深案例
3. `loan.html` — 贷款深案例
4. `tracking.html` — 重点事项跟踪闭环页
5. `weekly-report.html` — 周报草稿承接页

---

## 🔄 日常运行命令

### 完整刷新（全量重建）

```bash
cd 05_工具脚本
python3 scripts/run-pipeline.py --full
```

### 分步执行

```bash
# 1. 解析原始 Excel 数据
python3 scripts/parse_initial_data.py

# 2. 生成建议规则
python3 scripts/build_interpretation_rules.py
python3 scripts/build_recommendation_rules.py

# 3. 生成 review 队列
python3 scripts/generate_review_queue.py

# 4. 确认事项后记录意见
python3 scripts/record_review.py <itemId> <approve|modify|reject> [text]

# 5. 同步 review 状态并重建 gate
python3 scripts/sync_after_review.py --confirm

# 6. 打包前端数据（每次修改后必须执行）
python3 scripts/build_web_bundle.py
```

### 健康检查

```bash
python3 scripts/smoke_test.py --fast   # 快速检查
python3 scripts/smoke_test.py --baseline  # 基线回归检查
```

### 查看当前 gate 状态

```bash
python3 scripts/rebuild_go_live_gate.py --check
```

---

## 📁 目录结构

```
ai-radar-station/
├── apps/web/                      # 前端页面（直接浏览器打开）
│   ├── index.html                 # 首页总览
│   ├── deposit.html              # 存款深案例
│   ├── loan.html                 # 贷款深案例
│   ├── tracking.html             # 重点事项跟踪闭环
│   ├── weekly-report.html        # 周报草稿承接页
│   ├── peer-monitor.html         # 同业动态页
│   ├── policy-industry.html      # 政策行业页
│   └── data/app-data.js         # 前端数据 bundle（JSON 打包）
│
├── config/
│   └── analyst_sources.json      # 外部分析师白名单（9个来源）
│
├── data/
│   ├── raw/                      # 原始 Excel 数据（人工上传）
│   └── processed/                # 中间层 JSON（脚本产出）
│
├── docs/                         # 项目文档
│   ├── ARCHITECTURE.md          # 系统架构
│   ├── DATA_MODEL.md            # 数据模型
│   ├── PRD.md                   # 产品需求文档
│   ├── BASELINE_STATE.md        # Phase 2 基线状态
│   ├── CLOSURE_REPORT.md        # Phase 2 结项报告
│   ├── OPEN_ISSUES.md           # 未决事项清单
│   ├── PROGRESS_SYNC.md         # 进展同步文档
│   ├── SOP_EXECUTION.md         # 试运行 SOP
│   ├── trial-runbook.md         # 试运行操作手册
│   └── PHASE2_CHANGES.md        # Phase 2 变更说明
│
├── reports/                      # 运行时输出
│   ├── go-live-gate.json        # A/B/C gate 状态（关键！）
│   ├── review-queue.json         # 待确认事项队列
│   ├── review-status.json        # 事项确认状态
│   ├── tracking-items.json       # tracking 事项汇总
│   └── weekly-report-draft.md    # 周报草稿
│
├── reviews/                      # review 操作日志（append-only）
│
├── scripts/                      # 工具脚本
│   ├── run-pipeline.py          # 统一运行入口（推荐用这个）
│   ├── paths.py                 # 路径配置（所有脚本的路径来源）
│   ├── parse_initial_data.py    # Excel → 中间层 JSON
│   ├── generate_review_queue.py  # 生成待确认队列
│   ├── record_review.py          # 记录 review 意见
│   ├── sync_after_review.py      # 同步 review → 重建 gate → 周报
│   ├── rebuild_go_live_gate.py   # 重建 A/B/C gate
│   ├── smoke_test.py            # 健康检查
│   ├── build_web_bundle.py      # 打包前端数据
│   └── fetch_analyst_articles.py # 抓取分析师文章
│
└── HANDOVER.md                  # 项目交接文档
```

---

## 🔑 关键概念（新手必读）

### Gate 机制（A/B/C 三级门控）

| Gate | 含义 | 当前状态 |
|------|------|---------|
| **A gate** | 数据新鲜度（observedAt 是否足够新） | BLOCKED（需 2026-03 数据） |
| **B gate** | Analyst 观点可信度（是否足够真实可用） | CLEARED ✅ |
| **C gate** | Tracking 闭环（待确认事项是否有待处理） | CLEARED ✅ |

### Review 流程

```
分析结论生成 → review-queue.json（待确认）
     ↓ 人工确认（approve/modify/reject）
review-log.jsonl（追加记录）
     ↓ sync_after_review.py
review-status.json（更新确认状态）
     ↓
tracking-items.json（更新 tracking 状态）
     ↓
go-live-gate.json（更新 C gate）
     ↓
weekly-report-draft.md（更新周报草稿）
     ↓
build_web_bundle.py
     ↓
前端页面更新
```

### 状态优先级

```
pending（待确认）→ modify（已确认待行动）→ core-1/2/3（执行中）→ done（已完成）
                   ↘ reject（不跟进）
```

---

## ⚠️ 当前未决事项（P0 阻断）

| 事项 | 状态 | 解决方案 |
|------|------|---------|
| O-1：A gate 数据新鲜度 | BLOCKED | 取得 2026-03 原始 Excel → `import_monthly_data.py --confirm` |
| O-3：run-summary 与 gate 一致性 | WARN | `sync_after_review.py --confirm` 后消除 |

---

## 🗂️ 设计规范参照

前端页面 UI 风格应参照：
- `08_设计规范补充/` 文件夹内的平安智慧对公设计规范
- 核心规范：蓝色调、32px 表单控件、紧凑布局、表格/筛选/反馈模式

---

## 📞 联系方式

- 主要使用人：邱非
- OpenClaw Agent：Sylvia
- 数据刷新：每次新数据到来后运行 `run-pipeline.py --full`
- 事项确认：`python3 scripts/record_review.py <itemId> <approve|modify|reject>`
- 状态更新：`python3 scripts/record_tracking_status.py <itemId> <status>`

---

## 📋 OpenClaw Agent 指令模板

新环境部署后，在 OpenClaw 中输入以下指令让 Agent 接手：

```
请读取 OPENCLAW_DEPLOY/OPENCLAW_DEPLOYMENT.md 了解项目背景和运行方式，
然后接管 对公AI雷达站 项目。
当前未决事项：O-1（A gate 数据需更新）和 O-3（run-summary 一致性警告）。
下一步优先处理 O-1：确认 2026-03 原始数据是否到位。
```

---
