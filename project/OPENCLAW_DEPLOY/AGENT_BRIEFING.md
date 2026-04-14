# 对公 AI 雷达站 — OpenClaw Agent 接手指南

> 给新环境中的 OpenClaw Agent 阅读

## 项目定位

对公 AI 雷达站是平安银行对公业务管理部的经营情报系统，核心链路：

```
原始 Excel 数据
    ↓ parse_initial_data.py
中间层 JSON（deposit_benchmark / loan_benchmark / loan_rate）
    ↓ build_interpretation_rules.py + build_recommendation_rules.py
规则文件（interpretation_rules / recommendation_rules）
    ↓ generate_review_queue.py
review-queue.json（待确认事项）
    ↓ 人工确认（record_review.py）
review-log.jsonl（追加记录）
    ↓ sync_after_review.py
review-status.json + tracking-items.json + weekly-report-draft.md + go-live-gate.json
    ↓ build_web_bundle.py
前端数据包 app-data.js → 刷新 HTML 页面
```

## 你需要知道的

1. **路径配置**：`scripts/paths.py` 是所有路径的单一来源，脚本之间通过它共享路径，不允许硬编码
2. **Gate 机制**：
   - A gate = 数据新鲜度（observedAt 是否够新）
   - B gate = Analyst 观点可信度
   - C gate = Tracking 闭环状态
   - 当前唯一阻断项是 A gate（缺 2026-03 数据）
3. **Review 是 append-only**：`reviews/review-log.jsonl` 只能追加，不能修改历史
4. **数据文件**：原始数据在 `data/raw/`，中间层在 `data/processed/`，切勿混淆
5. **smoke_test** 是你的好朋友：任何修改后先跑 `--fast` 确认没有引入问题

## 常用命令

```bash
# 健康检查（每次操作后必跑）
python3 scripts/smoke_test.py --fast

# 完整重建
python3 scripts/run-pipeline.py --full

# 只跑同步链路（review 后必跑）
python3 scripts/sync_after_review.py --confirm

# 查看 gate 状态
python3 scripts/rebuild_go_live_gate.py --check
```

## 接手第一步

运行 `smoke_test.py --fast`，确认 59/59 PASS 后告知用户。

## 遇到问题

查看 `docs/OPEN_ISSUES.md` 和 `docs/CLOSURE_REPORT.md`，大多数问题都有记录。

---

如需了解更多，读取 `OPENCLAW_DEPLOYMENT.md`。
