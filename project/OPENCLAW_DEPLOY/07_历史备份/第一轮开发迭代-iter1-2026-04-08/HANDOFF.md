# 对公 AI 雷达站 — 交接文档（HANDOFF）

> 本文件记录本次迁移的关键决策、已知问题和后续行动。
> 建立时间：2026-04-07

---

## 迁移背景

原项目从 `workspace/ai-radar-station/OPENCLAW_DEPLOY/` 迁移至
`workspace-ai-radar/project/OPENCLAW_DEPLOY/`（新路径）。

旧路径保留作为历史备份，不再进行开发。

---

## 迁移完成项

| 完成项 | 状态 | 备注 |
|--------|------|------|
| 项目文件完整复制 | ✅ | 所有目录和文件已迁移 |
| smoke test 38/38 PASS | ✅ | 主链路验证通过 |
| 前端页面 8787 可访问 | ✅ | 静态 HTML 正常 |
| 统一运行入口 | ✅ | run_dev / run_smoke / run_report |
| 评估规则文档 | ✅ | eval/ 目录下 |
| 阻断项文档 | ✅ | docs/CURRENT_BLOCKERS.md |

---

## 当前唯一阻断项

**A Gate 阻断 — 缺 2026-03 贷款利率数据**

- **位置：** `04_数据与规则/利率/` 目录下无 2026-03 相关 Excel
- **现状：** loan_rate.json observedAt = 2025-12-01，目标 ≥ 2026-03-01
- **影响：** A gate 始终 BLOCKED，周报利率数据标注为 2026-02
- **解决路径：** 取得 2026-03 贷款利率 Excel → `python3 scripts/import_monthly_data.py --confirm`

---

## 关键配置文件

| 文件 | 用途 |
|------|------|
| `05_工具脚本/paths.py` | 所有路径配置（BASE/data/reports 等） |
| `05_工具脚本/smoke_test.py` | 验证主链路一致性 |
| `05_工具脚本/run-pipeline.py` | 完整 pipeline 入口（--full / --fast 等参数） |
| `05_工具脚本/import_monthly_data.py` | 月度数据导入（dry-run / --confirm） |
| `05_工具脚本/build_web_bundle.py` | 前端数据包打包 |
| `05_工具脚本/generate_weekly_report.py` | 周报生成 |

## 目录结构说明

Python 脚本通过 `paths.py` 管理的产物目录：

| paths.py 变量 | 实际路径 | 说明 |
|-------------|---------|------|
| `BASE` | `.../OPENCLAW_DEPLOY/` | 项目根目录 |
| `DATA` | `BASE/data/` | 原始数据（含 processed/ 子目录） |
| `PROCESSED` | `BASE/data/processed/` | 中间层 JSON |
| `REPORTS` | `BASE/reports/` | review/tracking 产物 |
| `WEB_DATA` | `BASE/apps/web/data/` | 前端数据包 |
| `REVIEWS` | `BASE/reviews/` | review 日志 |

`06_进展状态/` 是人工维护的状态文档目录（CURRENT_STATUS.md 等），与 `reports/` 是不同目录，各有用途。

---

## 前端运行

```bash
# 在 03_前端页面/ 目录下
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/03_前端页面
python3 -m http.server 8787
```

---

## Agent 行为边界

- 只处理 AI雷达站项目，不操作数字员工相关文件
- 遇到数据缺失时：先定位问题文件 → 报告阻断点 → 给出最小下一步命令
- 输出格式：事实 / 判断 / 建议，三段式
- 不在旧路径继续开发

---

## 后续最值得做的事（按优先级）

1. **补齐 2026-03 贷款利率数据**（解除 A gate 阻断）
2. **运行 `sync_after_review.py --confirm`**（消除 O-3 一致性警告）
3. **决策 Phase F 方向**（本地继续 / 内网服务器迁移 / 其他）
