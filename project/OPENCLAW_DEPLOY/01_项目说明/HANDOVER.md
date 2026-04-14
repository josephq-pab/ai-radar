# 对公 AI 雷达站｜项目交接与代码复盘文档

> 目标接手方：AI Agent（可读代码、理解架构、做代码复盘）
> 交接方：Sylvia（前序维护者）
> 项目路径：`/Users/josephq/.openclaw/workspace/projects/ai-radar-station/`
> 最近活跃：2026-04-01（上午 F15/F16，下午 F18）

---

## 一、项目是什么

**对公 AI 雷达站**是一个面向平安银行公司业务管理部的经营情报与观点研判系统，核心功能：

- 接入**同业对标数据**（存款/贷款/利率）、**外部分析师观点**、**政策信息**
- 加工成结构化情报，服务内部讨论（internalDiscussion）和正式汇报（reportPrep）准备
- 支持人工 review 确认 → 闭环跟踪 → 周报生成的全链路

**当前版本**：原型 v0.1，尚未进入生产环境

**核心技术栈**：Python 3.9（注意：非 3.10+，部分新库受限），BeautifulSoup4，Scrapling 0.2.99，Node.js（前端页面）

---

## 二、目录结构

```
ai-radar-station/
├── README.md                    # 项目概述（早期版本，已旧）
├── run-daily.sh                # 统一运行入口（调 run-pipeline.py）
│
├── apps/web/                   # 前端 HTML 页面（静态 HTML + JS，无框架）
│   ├── index.html              # 首页总览
│   ├── deposit.html            # 存款深案例页
│   ├── loan.html               # 贷款深案例页
│   ├── tracking.html           # 重点事项跟踪闭环页
│   ├── weekly-report.html      # 周报承接页
│   ├── peer-monitor.html      # 同业动态页（二级）
│   ├── policy-industry.html   # 政策行业页（二级）
│   └── data/
│       └── app-data.js        # 前端数据 bundle（全量 JSON 打包）
│
├── config/
│   └── analyst_sources.json    # 外部分析师白名单配置（9个来源）
│                               # 含 ID/name/URL/维度/优先级/crawlMode
│
├── data/
│   ├── raw/                   # 原始数据文件（人工上传）
│   │   ├── 2026年2月同业对标数据_更新格式_余额和年日均.xlsx   ← 当前最新
│   │   ├── 股份行人行口径贷款对标数据260228.xlsx
│   │   └── 贷款利率-2602.xlsx
│   │   # ⚠️ 2026-03 文件尚未到位
│   │
│   ├── processed/              # 所有脚本的中间输出
│   │   ├── deposit_benchmark.json/csv    # 存款对标（33条记录）
│   │   ├── loan_benchmark.json/csv       # 贷款对标（52条记录）
│   │   ├── loan_rate.json/csv            # 利率数据（16条记录）
│   │   ├── analyst_opinions.json         # 分析师观点（当前5条，含质量摘要）
│   │   ├── analyst_opinions_raw.json     # 原始抓取结果（批次验证用）
│   │   ├── summary.json                  # 存款+贷款+利率合计摘要
│   │   ├── dashboard.json                # dashboard 数据
│   │   ├── quality_report.json           # 数据质量报告
│   │   ├── .batch_verify_checkpoint.json # analyst 批次验证 checkpoint
│   │   ├── interpretation_rules.json     # 数据解释规则
│   │   ├── recommendation_rules.json     # 建议生成规则（观察/策略/行动）
│   │   ├── preference_profile.json       # 周报偏好画像
│   │   ├── section_preferences.json     # 栏目偏好
│   │   ├── domain_templates.json        # 板块模板
│   │   └── tracking_status_rules.json   # review状态→tracking状态映射规则
│   │
│   └── analyst_cache/           # analyst 抓取缓存（当前为空目录）
│
├── docs/                       # 项目文档（早期产物，部分已旧）
│   ├── ARCHITECTURE.md         # 系统架构图（mermaid flow）
│   ├── DATA_MODEL.md          # 数据模型
│   ├── REPORT_TEMPLATE.md      # 周报模板
│   ├── PRD.md                  # 产品需求文档
│   ├── BUILD_PLAN.md          # 建设计划（已相对旧）
│   ├── PROGRESS_LOG.md        # 进展日志（最新历史记录）
│   ├── operator-guide.md      # 运营指南
│   ├── troubleshooting.md      # 故障排查
│   ├── state-source-of-truth.md
│   ├── data-contract.md
│   ├── data-refresh-policy.md
│   ├── data-time-semantics.md
│   ├── incident-severity.md
│   ├── acceptance/checklist.md
│   ├── monthly-refresh-playbook.md
│   ├── migration-prep/system-map.md
│   └── trial-runbook.md
│
├── ops/
│   └── cron.example           # cron 调度示例（未正式接入调度）
│
├── reports/                    # 各类报告与判定输出
│   ├── weekly-report-draft.md  # 周报草稿（主要输出物之一）
│   ├── run-summary.json      # 运行摘要（readinessLevels/goLiveCriteria）
│   ├── run-summary.md
│   ├── go-live-gate.json     # A/B/C 三类 gate 状态（当前关键产物）
│   ├── go-live-gate.md
│   ├── review-status.json    # review 确认状态汇总
│   ├── tracking-items.json   # tracking 中间层（17条，含状态/进展/下一步）
│   ├── review-queue.json     # 待 review 项队列
│   ├── analyst-review-queue.json
│   ├── pending-resolution-pack.json  # pending 项处置包
│   ├── fetch-health.json      # analyst 来源抓取健康状态
│   ├── freshness.json         # 各文件新鲜度
│   ├── ops-dashboard.json    # 运营 dashboard
│   ├── monthly-import-readiness.json
│   ├── march-refresh-action-sheet.json  # 3月数据导入执行清单
│   ├── source-maintenance.json
│   ├── change-summary.json
│   ├── review-decision-pack.json
│   ├── review-worklist.json
│   └── tracking-status-log.jsonl  # tracking 业务状态变更日志
│
├── reviews/
│   └── review-log.jsonl      # 所有 review 决策的不可篡改日志
│                               # 格式：{itemId, decision, reason, editedText, reviewedAt}
│
├── scripts/                   # 26 个 Python 脚本（核心资产）
│   ├── run-pipeline.py        # 统一运行入口（parse→周报→bundle→smoke）
│   ├── smoke_test.py           # 全链路一致性校验（59项检查）
│   ├── sync_after_review.py   # review 后半自动同步（5步链路）
│   │
│   │   # ── 数据层 ──
│   ├── import_monthly_data.py  # 月度数据导入（未跑，缺3月文件）
│   ├── parse_initial_data.py   # 原始 Excel 解析（历史用过）
│   │
│   │   # ── Analyst 采集 ──
│   ├── fetch_analyst_articles.py   # 分析师观点抓取（9个来源）
│   ├── build_analyst_opinions.py    # 观点构建+评分+去重+生成 review queue
│   ├── batch_verify_analyst.py      # 批次化 analyst 验证（新增，实验性）
│   ├── verify_analyst_fix.py        # 单批次 analyst 验证（早期用）
│   │
│   │   # ── 报告生成 ──
│   ├── generate_weekly_report.py    # 周报生成（主要输出）
│   ├── generate_review_queue.py      # review 队列生成
│   ├── generate_ops_dashboard.py      # 运营 dashboard 生成
│   │
│   │   # ── 规则构建 ──
│   ├── build_review_status.py         # review 状态汇总
│   ├── build_tracking_items.py       # tracking 中间层构建
│   ├── build_web_bundle.py           # 前端 bundle 打包
│   ├── build_analyst_opinions.py     # analyst 观点构建（见上）
│   ├── build_preference_profile.py   # 偏好画像
│   ├── build_interpretation_rules.py # 解释规则
│   ├── build_recommendation_rules.py # 建议生成规则
│   ├── build_domain_templates.py    # 板块模板
│   ├── build_section_preferences.py # 栏目偏好
│   │
│   │   # ── Review 记录 ──
│   ├── record_review.py              # 写入 review-log.jsonl（正式决策链路）
│   ├── record_tracking_status.py    # 独立记录 tracking 业务状态
│   │   # 已知问题：未接入 sync 链路（见第六节风险）
│   │
│   │   # ── Gate 重建 ──
│   ├── rebuild_c_gate.py            # C gate 重建（review-log→go-live-gate）
│   ├── rebuild_go_live_gate.py      # A/B/C 三类 gate 统一重建（新增，主链路）
│   │
│   │   # ── 检查 ──
│   ├── check_fetch_health.py         # fetch 健康检查
│   ├── apply_sample_reviews.py      # 批量应用 review（实验性）
│   │
│   └── schedule-example.sh
│
└── skills/
    └── scrapling-official/          # Scrapling 官方 skill（安装于项目中）
        ├── SKILL.md                  # 完整使用文档
        ├── examples/                 # 4个示例文件
        └── references/               # 详细参考文档（fetching/parsing/spiders）
```

---

## 三、数据流（完整链路）

```
[raw/ Excel文件]
    ↓ import_monthly_data.py / parse_initial_data.py
[data/processed/ 中间JSON]
    ↓ build_*.py (多个脚本)
[data/processed/ 最终JSON] + [reports/ 报告]
    ↓ build_web_bundle.py
[apps/web/data/app-data.js]
    ↓
[HTML页面] → [人工review] → record_review.py
    ↓
[review-log.jsonl] → sync_after_review.py (5步)
    ↓                   ↓
    ↓           rebuild_c_gate.py
    ↓           rebuild_go_live_gate.py
    ↓           generate_weekly_report.py
    ↓           build_web_bundle.py
    ↓
[go-live-gate.json] [weekly-report-draft.md] [run-summary.json]
```

---

## 四、三类 Gate 系统（当前核心业务逻辑）

### A_gate — 数据新鲜度
- **阻塞条件**：`deposit_observedAt < 2026-03-01` 或 `loan_observedAt < 2026-03-01` 或 `rate_observedAt < 2026-03-01`
- **数据来源**：`data/processed/deposit_benchmark.json[].observedAt` 等
- **解除条件**：3月数据文件放入 `data/raw/` 后执行 `import_monthly_data.py --confirm`
- **当前状态**：🔴 BLOCKED（缺3月文件）

### B_gate — Analyst 输入质量
- **阻塞条件**：`garbledCount > 0` OR `referenceableCount < 3` OR `isReliableForReport == false`
- **正式清除门槛**（定义在 `rebuild_go_live_gate.py`）：
  ```
  garbledCount == 0
  AND referenceableCount >= 3
  AND isReliableForReport == true
  ```
- **数据来源**：`data/processed/analyst_opinions.json` 的 qualityTiers 摘要
- **解除条件**：Scrapling 抓取 + build_analyst_opinions.py 重跑
- **当前状态**：✅ CLEARED（2026-04-01 批次验证后：garbled=0, ref=5, reliable=true）
- **已验证来源**：4/9（董希淼、薛洪言、娄飞鹏、周茂华）
- **未验证来源**：5/9（连平、温彬、曾刚、朱太辉、孙扬）

### C_gate — Pending 决策完成度
- **核心业务语义**（用户2026-04-01确认）：
  > "批准后即可进入后续跟踪，不阻断本次汇报前准备。"
- **阻断逻辑**：只统计 `decision` 为空/pending 的事项
- **已 approve/reject 的项**：归入 `postApprovalFollowups`，不计入阻断
- **数据来源**：`reviews/review-log.jsonl` × `reports/tracking-items.json`
- **当前状态**：✅ CLEARED（0个真实阻断，15个后续跟踪项）

---

## 五、readiness 分级系统

三个 readiness 等级（定义在 `run-pipeline.py` 和 `smoke_test.py`）：

| Readiness | 定义 | 当前值 |
|-----------|------|--------|
| browseReadiness | 页面/bundle/tracking/周报是否可正常浏览 | ready ✅ |
| internalDiscussionReadiness | 数据是否足以支撑内部复盘 | limited ⚠️（受A阻塞）|
| reportPrepReadiness | 是否足以支撑正式汇报前准备 | limited ⚠️（受A阻塞）|

---

## 六、Review 与 Tracking 双轨状态系统

### 两套状态的区别
- **review 状态**（review-log.jsonl）：内容确认结果（pending/approve/modify/reject）
- **tracking 状态**（tracking-items.json）：事项业务推进进度（待研判/跟踪中/已上报/已行动/已关闭）

### 当前 tracking-status → review 映射规则（`data/processed/tracking_status_rules.json`）：
```
pending    → 待研判
modify     → 跟踪中
approve    → 已上报
reject     → 已关闭
```

### 独立 tracking 状态日志
`scripts/record_tracking_status.py` 可独立推进 tracking 状态（不依赖 review 变化），写入 `reviews/tracking-status-log.jsonl`，但：
⚠️ **当前问题**：`record_tracking_status.py` 尚未接入 `sync_after_review.py` 链路，需手动触发或等待接入。

---

## 七、Scrapling 集成现状

- **版本**：0.2.99（Python 3.9 最高可用版本）
- **Python 要求**：⚠️ Scrapling 0.4.3+ 需要 Python 3.10+，当前环境为 3.9.6
- **安装方式**：`pip3 install scrapling` + `pip3 install camoufox cssselect w3lib tldextract`
- **使用方式**：
  ```python
  from scrapling.fetchers import Fetcher
  r = Fetcher.get(url, timeout=20)
  html = str(r.body)  # 获取 HTML 字符串
  soup = BeautifulSoup(html, 'html.parser')
  ```
- **Skill**：`skills/scrapling-official/` 已安装，含完整文档和示例
- **已验证可用站点**：东方财富(eastmoney)、新华网(xinhuanet)、新浪(sina)
- **已知限制站点**：cebnet.com.cn（返回低版本浏览器提示）

---

## 八、批次化 Analyst 验证机制

**目的**：避免全量 pipeline 被 SIGTERM 超时中断

**机制**：`scripts/batch_verify_analyst.py`

**用法**：
```bash
# 查看当前状态
python3 scripts/batch_verify_analyst.py --status

# 跑下一批次（默认2个来源）
python3 scripts/batch_verify_analyst.py

# 指定单源验证
python3 scripts/batch_verify_analyst.py --source analyst-deposit-003

# 续跑（跳过已验证的）
python3 scripts/batch_verify_analyst.py --resume

# 跑完所有未验证来源
python3 scripts/batch_verify_analyst.py --run-all
```

**Checkpoint 文件**：`data/processed/.batch_verify_checkpoint.json`

**注意**：全量 pipeline（`fetch_analyst_articles.py`）在当前环境下会被 SIGTERM 中断，不建议直接使用。

---

## 九、已知风险与技术债（供代码复盘参考）

### 高优先级
1. **`record_tracking_status.py` 未接入 sync 链路**
   - 独立 tracking 状态写入后，不会自动触发 `sync_after_review.py` 重建
   - 需手动补跑或接入链路

2. **全量 analyst pipeline 被 SIGTERM**
   - `fetch_analyst_articles.py` 全量跑在当前环境超时
   - 临时方案：`batch_verify_analyst.py` 批次验证
   - 根本方案待定

3. **Python 3.9 限制**
   - Scrapling 0.4.3+ 不可用
   - 部分现代 Python 语法不可用（如 f-string dict 访问）
   - 建议升级到 3.10+

### 中优先级
4. **`go-live-gate.json` 为静态文件**
   - 只有 C gate 通过 `rebuild_c_gate.py` / `rebuild_go_live_gate.py` 动态更新
   - A/B gate 的 A_dataFreshness/B_analystQuality 部分依赖 `run-pipeline.py` 写入
   - 建议：A/B/C 三者均由 `rebuild_go_live_gate.py` 作为唯一 source

5. **`sync_after_review.py` 步骤顺序**
   - 当前 `rebuild_c_gate.py` 在 `build_tracking_items.py` 之后
   - 但 `rebuild_go_live_gate.py` 需要同步跑，需要确保顺序一致

6. **`WAITING_FOR_DATA` / `WAITING_FOR_BUSINESS` 硬编码**
   - 在 `smoke_test.py` 的 `run_pending_aging()` 中硬编码了两个 item ID
   ```python
   WAITING_FOR_DATA = {'1dbd4051cc58'}      # 已 reject
   WAITING_FOR_BUSINESS = {'581527c09784'}   # 已 approve
   ```
   - 这两个 ID 已处理完毕，硬编码残留需清理

### 低优先级
7. **docs/ 目录下部分文档已旧**
   - README.md 是早期版本，部分内容过时
   - NEXT_STEPS.md 有残留污染
   - 建议以 `PROGRESS_LOG.md` 和 `BUILD_PLAN.md` 为准

8. **`run-pipeline.py` 的 gateType 推断逻辑有冗余**
   ```python
   # 内部讨论 readiness 的 gateType 推断：
   'gateType': ['A_dataFreshness'] if (fresh_blockers) else ['B_analystQuality'] if (analyst_blockers) else (['C_pending'] if ... else [])
   ```
   - 与 `rebuild_go_live_gate.py` 的 gateType 逻辑存在重复定义
   - 建议统一到 `rebuild_go_live_gate.py` 作为单一真相源

---

## 十、当前系统状态快照

**文件新鲜度**：
```
deposit_benchmark.json : observedAt=2026-02-28  freshness=偏旧
loan_benchmark.json   : observedAt=2026-02-28  freshness=偏旧
loan_rate.json        : observedAt=2025-12-01  freshness=过旧
analyst_opinions.json : builtAt=2026-04-01 14:24
```

**Analyst 质量**（批次验证后）：
```
total: 5 records
VALID: 0 / GARBLED: 0 / PLACEHOLDER: 0 / DEGRADED: 5
referenceableCount: 5
isReliableForReport: true
```

**Gate 状态**（2026-04-01 22:24）：
```
A_dataFreshness:     BLOCKED (缺3月数据)
B_analystQuality:    CLEARED ✅
C_pendingCompletion:  CLEARED ✅（0个真实阻断）
```

**readinessLevels**：
```
browseReadiness:            ready ✅
internalDiscussionReadiness: limited ⚠️（受A阻塞）
reportPrepReadiness:        limited ⚠️（受A阻塞）
```

**待办 pending**：
```
已关闭: 2项（1dbd4051cc58 reject, 76e4940707f4 reject）
已上报: 9项
跟踪中: 6项
待研判: 0项 ✅
```

---

## 十一、复盘建议关注点

供接手方重点审查的方向：

1. **`rebuild_go_live_gate.py` vs `run-pipeline.py` 的 gateType 逻辑一致性**
   - 两者都在计算 readiness gateType，存在重复定义风险
   - 建议确认 `run-summary.json` 的 gateType 以哪个为准

2. **`sync_after_review.py` 的步骤完整性**
   - 当前 5 步：review_status → tracking_items → rebuild_c_gate → weekly_report → bundle
   - 缺失：`rebuild_go_live_gate.py`（A/B/C 统一重建）未接入
   - 建议：把 `rebuild_go_live_gate.py` 加入该链路

3. **analyst 批次验证后的质量含义**
   - 当前 DEGRADED=5 但 isReliableForReport=true
   - 需要理解 `build_analyst_opinions.py` 的评分逻辑是否合理
   - DEGRADED 是否等同于"质量不足"需要判断

4. **`record_tracking_status.py` 未接入链路的影响**
   - 独立 tracking 状态变更不能自动传播到 bundle
   - 需确认这是否是设计意图

5. **全量 pipeline SIGTERM 根因**
   - 是网络超时？是 session 超时？是 Scrapling 浏览器进程问题？
   - `batch_verify_analyst.py` 解决了问题，但全量脚本架构本身是否有必要修复

---

## 十二、Git 近期提交参考

```
F18 (2026-04-01 晚):
  - 新建 rebuild_go_live_gate.py（A/B/C 统一重建）
  - 新建 batch_verify_analyst.py（批次验证）
  - 新建 rebuild_c_gate.py（C gate 独立重建）
  - 新建 verify_analyst_fix.py（早期单批次验证）
  - 修改 sync_after_review.py（增加 rebuild_c_gate 步骤）
  - 多次脚本语法修复

F15/F16 (2026-04-01 下午):
  - C gate 拍板：1dbd4051cc58 reject，581527c09784 approve
  - C gate 语义修正：批准后不阻断
  - analyst 编码修复验证（Scrapling 集成）
```

---

## 十三、给接手 Agent 的操作备忘

**不要做的**：
- 不要在没有 2026-03 数据文件的情况下跑 `import_monthly_data.py --confirm`
- 不要直接跑全量 `fetch_analyst_articles.py`（会 SIGTERM）
- 不要修改 `review-log.jsonl` 的历史行（只追加）

**可以安全做的**：
- 跑 `python3 scripts/smoke_test.py --fast`（只读校验，不写文件）
- 跑 `python3 scripts/sync_after_review.py --dry-run`（预览，不写）
- 跑 `python3 scripts/batch_verify_analyst.py --status`（只读）
- 跑 `python3 scripts/rebuild_go_live_gate.py --check`（一致性检查，不写）

**最优先待决事项**：
1. 等业务侧提供 2026-03 数据文件（解除 A gate）
2. 续跑剩余 5 个 analyst 来源（`--resume` 或 `--run-all`）
3. 接入 `rebuild_go_live_gate.py` 到 `sync_after_review.py` 链路

---

*本文档生成时间：2026-04-02 02:07 GMT+8*
*交接方：Sylvia（OpenClaw AI Agent）*
