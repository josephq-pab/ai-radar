# 对公 AI 雷达站

面向平安银行公司业务管理部的经营情报、观点研判与策略建议系统原型项目。

## 当前阶段

- 已完成产品定义 v0.1
- 已完成首期架构设计 v0.1
- 已完成首批数据结构识别
- 已完成三类 Excel 的首版解析脚本
- 已完成四页主链路原型与动态化雏形：首页总览 / 存款深案例 / 贷款深案例 / 重点事项跟踪
- 已完成周报与专题承接页、同业分析承接页、政策与行业预留页
- 已完成基线对齐方案，明确收敛到“首页总览 + 存款深案例 + 贷款深案例 + 重点事项跟踪”四页主链路
- 已完成 `apps/web/tracking.html`，将 `reviewQueue` / `reviewStatus` / 建议分层结果收编为重点事项闭环页
- 已完成周报生成脚本 v0
- 已完成待确认队列与确认状态汇总机制
- 已完成偏好画像生成与周报偏好学习闭环 v0
- 已完成栏目模板与板块口径偏好细化 v0
- 已完成板块级模板（存款 / 贷款 / 定价 / 同业）接入周报生成与页面展示 v0
- 已完成数据解释规则（先看什么、怎么判断、要追问什么）接入周报与页面展示 v0
- 已完成建议生成规则（观察提示 / 策略建议 / 直接行动建议）接入周报与页面展示 v0

## 目录结构

```text
projects/ai-radar-station/
  README.md
  docs/
    PRD.md
    ARCHITECTURE.md
    DATA_MODEL.md
    DATA_DISCOVERY.md
    REPORT_TEMPLATE.md
    NEXT_STEPS.md
    BASELINE_ALIGNMENT.md
  apps/
    web/
      index.html
      deposit.html
      loan.html
      tracking.html
      weekly-report.html
      peer-monitor.html
      policy-industry.html
      data/
        app-data.js
  data/
    raw/
    processed/
  reports/
  reviews/
  scripts/
    parse_initial_data.py
    generate_weekly_report.py
    generate_review_queue.py
    record_review.py
    build_review_status.py
    build_preference_profile.py
    build_interpretation_rules.py
    build_recommendation_rules.py
    build_web_bundle.py
```

## 首批输入数据

来自：`/Users/josephq/Downloads/对公AI雷达站/数据/`

包括：
- 同业对标余额与年日均数据
- 股份行贷款对标数据
- 贷款利率数据

## 已产出内容

### 数据层
- `data/processed/deposit_benchmark.json/csv`
- `data/processed/loan_benchmark.json/csv`
- `data/processed/loan_rate.json/csv`
- `data/processed/summary.json`
- `data/processed/dashboard.json`
- `data/processed/quality_report.json`
- `data/processed/preference_profile.json`
- `data/processed/interpretation_rules.json`
- `data/processed/recommendation_rules.json`

### 页面层
- 首页总览页 `apps/web/index.html`
- 存款深案例页 `apps/web/deposit.html`
- 贷款深案例页 `apps/web/loan.html`
- 重点事项跟踪页 `apps/web/tracking.html`
- 周报与专题承接页 `apps/web/weekly-report.html`
- 同业分析承接页 `apps/web/peer-monitor.html`
- 政策与行业预留页 `apps/web/policy-industry.html`

### 报告与闭环层
- 周报草稿 `reports/weekly-report-draft.md`
- 待确认队列 `reports/review-queue.json`
- 确认状态汇总 `reports/review-status.json`
- 前端数据 bundle `apps/web/data/app-data.js`

## 运行方式

### 1. 解析数据
```bash
python3 scripts/parse_initial_data.py
```

### 2. 生成建议规则与周报草稿
```bash
python3 scripts/build_recommendation_rules.py
python3 scripts/generate_weekly_report.py
```

### 3. 生成待确认队列与状态汇总
```bash
python3 scripts/generate_review_queue.py
python3 scripts/build_review_status.py
```

### 4. 打包前端数据
```bash
python3 scripts/build_web_bundle.py
```

## 当前可体验路径

建议按以下顺序体验：

1. `apps/web/index.html`：查看首页总览与主链路入口
2. `apps/web/deposit.html`：查看存款深案例、建议动作与跟踪摘要
3. `apps/web/loan.html`：查看贷款深案例、定价联动与跟踪摘要
4. `apps/web/tracking.html`：查看待确认事项、状态流转、下一步动作与来源回溯
5. `apps/web/weekly-report.html`：查看周报草稿、规则透明化与确认机制

## 项目目标

围绕同业、政策、行业三大优先信息源，服务整体、存款、贷款三大业务板块，输出：
- 趋势判断
- 经营建议
- 业务结构建议
- 定价建议
- 周报与专题报告

## 下一步计划

1. 将建议层级、下一步动作、来源页回溯从前端推断逐步下沉为正式中间层字段
2. 继续增强 tracking 页的状态视图、详情联动与回写能力
3. 继续优化首页、存款深案例、贷款深案例与跟踪页的一致性
4. 增加政策 / 行业输入与专题触发规则
5. 搭建 API 与前后端代码骨架，并预留可信环境迁移结构
6. 用真实 review 持续训练偏好画像、解释规则和建议生成规则
