# Phase 2 基线 — 未决事项清单

> 版本：v2-baseline | 日期：2026-04-02

---

## 一、P0（阻断正式汇报）

### O-1：A gate 数据新鲜度阻断

**现状**：`deposit_benchmark.json` 和 `loan_benchmark.json` 的 `observedAt` 已更新至 2026-03-31 ✅，但 `loan_rate.json` 的 `observedAt` 仍为 **2025-12-01**，低于 A gate 阈值 2026-03-01。

**影响**：A gate 处于 BLOCKED 状态，`reportPrepReadiness` 无法达到 `ready`。

**解法**：
```bash
# 在有 2026-03 月贷款利率原始 Excel 时执行
python3 scripts/import_monthly_data.py --confirm
```

**前置条件**：
- [ ] 取得 2026-03 贷款利率原始 Excel（如 `贷款利率-2603.xlsx`）
- [ ] 确认文件存放于 `data/raw/` 目录
- [ ] 文件 observedAt 字段 ≥ 2026-03-01

---

### O-2：B gate reportableCount=0

**状态：✅ 已关闭（2026-04-03）**

Phase 2.1 已通过 Layer 3 提取 + VALID 语义门控 + quarantine 配置驱动解决：
- Layer 3 从薛洪言、连平正文中成功提取 viewpoints（2条）和 snippets（3条）
- 周茂华记者转写稿被 VALID 语义门控降级为 DEGRADED，isReferenceable=False
- 董希淼坏源（cebnet.com.cn）已移入 quarantine，garbledCount=0
- B gate: garbledCount=0 ✅ usableCount=4 ✅ reportableCount=3 ✅ isReliableForReport=True ✅

**变更文件**：`build_analyst_opinions.py`（P2.1-A~D）、`generate_weekly_report.py`（P2.1-E）

# 运行下一批次（默认2个来源）
python3 scripts/batch_verify_analyst.py

# 验证 B gate 状态
python3 scripts/rebuild_go_live_gate.py --check
```

方案 B（直接抓取，可能引入乱码，需后续 batch_verify）：
```bash
python3 scripts/fetch_analyst_articles.py
python3 scripts/build_analyst_opinions.py
python3 scripts/rebuild_go_live_gate.py --check
```

---

## 二、P1（影响链路可信度，尽快处理）

### O-3：run-summary.json 与 go-live-gate.json 一致性警告

**状态：✅ 已关闭（2026-04-03）**

`rebuild_go_live_gate.py` 已内置 `sync_run_summary()`，每次执行时自动将 gate 状态同步至 `run-summary.json`。本轮全链路验证 `一致性检查: OK` ✅。

---

### O-4：smoke_test.py 的 `check_baseline()` 未接入

**现状**：`check_baseline()` 函数在 `smoke_test.py` 底部定义但从未被 `main()` 调用。

**解法**：在 `smoke_test.py` 中添加 `--baseline` 隐藏标志，或将其输出整合到 `run-summary.json` 的 `trustSummary` 中。

---

### O-5：`docs/trial-runbook.md` 仍有部分路径引用需验证

**现状**：`docs/trial-runbook.md` 中 Launchd plist 片段的路径仍为绝对路径。

**状态**：Launchd plist 路径为 `/Users/josephq/...` 格式，macOS 系统服务路径理论上可接受，但建议验证是否与 `schedule-example.sh` 的动态路径方案一致。

---

## 三、P2（非阻断，择机处理）

### O-6：`rebuild_c_gate.py` 保留但未在同步链路中使用

**现状**：`rebuild_c_gate.py` 仍存在于 `scripts/`，但 `sync_after_review.py` 已改用 `rebuild_go_live_gate.py` 统一处理。

**选项**：
- A：保留（作为独立 C gate 诊断工具）
- B：标记为 deprecated（输出说明指向 `rebuild_go_live_gate.py`）
- C：删除

---

### O-7：周报日期引用为 2026-02-02（旧数据特征）

**现状**：`smoke_test.py` 报告周报中找到日期 `2026-02-02`，与 A gate 阻断原因一致。

**影响**：不影响链路一致性，但表明周报内容基于旧数据。

**解法**：更新源数据（O-1）后重新生成周报。

---

### O-8：`run-pipeline.py` 仍独立计算 `readinessLevels`

**现状**：`run-pipeline.py` 的 `generate_run_summary()` 独立构建 `readiness_levels`，与 `go-live-gate.json` 存在理论分歧风险。

**说明**：Phase 2 已建立 `go-live-gate.json` 作为单一真相源，`run-pipeline.py` 的 `readiness_levels` 仅用于 `run-summary.json` 展示，`sync_after_review.py` 会用 `gateSnapshot` 字段补充最新 gate 状态。实际分歧风险较低。

**建议**：后续版本考虑让 `run-pipeline.py` 直接读取 `go-live-gate.json` 填充 `readiness_levels`。

---

## 四、变更日志（2026-04-02）

| 日期 | 事项 | 发起 |
|------|------|------|
| 2026-04-02 | Phase 2 基线收敛：路径配置化、Gate 单一真相源、Analyst 语义重构、文档对齐 | 邱非 |
