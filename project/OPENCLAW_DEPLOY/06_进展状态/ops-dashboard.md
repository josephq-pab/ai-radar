# 对公 AI 雷达站 — 运营行动面板

**生成时间:** 2026-04-01 01:52 UTC

## 当前可用性分级

**✅ 浏览可用性:** 主链路一致，bundle 新鲜，页面可正常浏览
  → 可正常用于日常查看与内部跟踪

**⚠️ 内部讨论可用性:** 存在 1 项限制，参考时需注意
  - analyst 层有 4 条乱码，4 条空/占位
  → 可用于内部复盘，但需在引用时注明数据截止时间

**⚠️ 汇报前准备可用性:** 存在 1 项限制，需在汇报前处理
  - analyst 层不足以支撑周报正式引用（3 条有效，4 条乱码，2 条空/占位）
  → 建议在汇报前解决阻塞项

## 本周阻塞项

### 🟠 核心 benchmark 数据过期（最新：2026-02-28）
deposit/loan observedAt=2026-02-28，已超过 30 天。rate observedAt=2026-02-01。
**负责方:** 业务分析师
**建议动作:** 推动业务侧提供 2026-03 月度数据，放入 data/raw/ 后执行 import_monthly_data.py --confirm

### 🟠 贷款利率数据严重过期（最新：2026-02-01）
loan_rate observedAt=2026-02-01，已超过 45 天，对利率判断影响较大
**负责方:** 业务分析师
**建议动作:** 优先推动提供 2026-03 贷款利率数据

## 本周必须动作

### 🔴 推动提供 2026-03 月度数据文件
当前 benchmark 数据截至 2026-02，月报节奏要求每月 5 日前到位
**执行步骤:**
  联系业务分析师获取 2026-03 存款/贷款/利率 Excel
  放入 data/raw/ 目录
  执行 python3 scripts/import_monthly_data.py --dry-run 验证
  确认无误后执行 python3 scripts/import_monthly_data.py --confirm
  执行 python3 scripts/smoke_test.py --fast 验证
**触发条件:** 一旦收到新文件

### 🟡 推进 存款 pending 项 review
共 2 项待研判/跟踪中，需在汇报前完成确认
**执行步骤:**
  逐项 review：python3 scripts/record_review.py <itemId> <decision>
  decision 可选：approve / modify / reject
  修改后执行 python3 scripts/sync_after_review.py --confirm
  执行 python3 scripts/smoke_test.py --fast 验证
**触发条件:** 汇报前至少 1 天

### 🟡 推进 贷款 pending 项 review
共 3 项待研判/跟踪中，需在汇报前完成确认
**执行步骤:**
  逐项 review：python3 scripts/record_review.py <itemId> <decision>
  decision 可选：approve / modify / reject
  修改后执行 python3 scripts/sync_after_review.py --confirm
  执行 python3 scripts/smoke_test.py --fast 验证
**触发条件:** 汇报前至少 1 天

### 🟡 推进 整体对公业务 pending 项 review
共 3 项待研判/跟踪中，需在汇报前完成确认
**执行步骤:**
  逐项 review：python3 scripts/record_review.py <itemId> <decision>
  decision 可选：approve / modify / reject
  修改后执行 python3 scripts/sync_after_review.py --confirm
  执行 python3 scripts/smoke_test.py --fast 验证
**触发条件:** 汇报前至少 1 天

## 本周不必做的事

### ⛔ 不要进行 UI 重构或高保真改版
当前阶段重点是数据链路和运营可信度，不是视觉层

### ⛔ 不要新增一级页面或扩张页面数量
四页主链路已稳定，继续扩张会增加维护成本和一致性风险

### ⛔ 不要推进数据库迁移或 API 落地
这些属于工程化阶段，当前阶段是真实试运行验证

### ⛔ 不要在本轮大批量增加分析师白名单
先把现有 9 条记录质量问题修好，再扩白名单才有意义

## 条件触发动作

### 📋 条件：收到 2026-03 数据文件
**动作：** 月度数据导入
**命令序列:**
    python3 scripts/import_monthly_data.py --dry-run
    # 确认扫描结果后
    python3 scripts/import_monthly_data.py --confirm
    python3 scripts/sync_after_review.py --confirm
    python3 scripts/smoke_test.py --fast
**验证要点:**
  - 检查 reports/run-summary.json dataFreshness.blocked == false
  - 确认 deposit/loan/rate observedAt 已更新为 2026-03

### 📋 条件：analyst 抓取网络恢复
**动作：** 重新抓取分析师观点
**命令序列:**
    python3 scripts/fetch_analyst_articles.py
    python3 scripts/build_analyst_opinions.py
**验证要点:**
  - 检查 data/processed/analyst_opinions.json records 中有效记录 ≥3 条
  - 检查无乱码标题

### 📋 条件：邱非对 pending 项拍板
**动作：** 决策后同步
**命令序列:**
    python3 scripts/record_review.py <itemId> <decision> [editedText]
    python3 scripts/sync_after_review.py --confirm
    python3 scripts/smoke_test.py --fast
**验证要点:**
  - 确认 tracking-items.json 状态已更新
  - 确认周报第九+十节数据一致
  - 确认 bundle 已同步

### 📋 条件：每周一（周报前）
**动作：** 周前检查清单
**命令序列:**
    python3 scripts/smoke_test.py --fast
    python3 scripts/smoke_test.py --pending-aging
    # 检查 run-summary readiness 分级
    cat reports/run-summary.json | python3 -c "import json,sys; r=json.load(sys.stdin); print(r.get("verdictText"))"
**验证要点:**
  - fast-check 全 PASS
  - reportPrepReadiness.level != not_ready
  - 所有阻塞项已处理

## 数据新鲜度

- deposit benchmark: 2026-02-28
- loan benchmark: 2026-02-28
- loan rate: 2026-02-01

## Analyst 层质量

- 有效记录: 3 条
- 乱码记录: 4 条 ⚠️ 需修复
- 空/占位记录: 2 条 ⚠️ 需替换
- 判定: ⚠️ 部分可用（目标 ≥5 条有效）
