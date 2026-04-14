# 对公 AI 雷达站 — 运行手册（RUNBOOK）

> 本文件记录三个统一运行入口的作用、依赖、参数和成功标准。
> 建立时间：2026-04-07

---

## 入口一：run_dev.sh

### 作用
本地开发完整链路：启动前端 HTTP Server + 执行完整 pipeline（解析→review→周报→bundle→校验）。

### 依赖
- Python 3.9（`/tmp/py39env/bin/python`）
- `requirements.txt` 依赖已安装
- `04_数据与规则/` 下有原始 Excel 文件
- 端口 8787 未被占用

### 关键参数
无参数，默认跑完整链路。

### 成功判定标准
- 前端 HTTP Server 在 8787 端口启动成功
- pipeline 输出 `✅ 主链路一致，bundle 新鲜`
- smoke test 38/38 PASS
- `app-data.js` 生成时间戳为当天

### 失败处理
- 端口占用：`lsof -i :8787 | grep LISTEN` 查进程
- 数据缺失：停在对应步骤，输出具体缺失文件名

---

## 入口二：run_smoke.sh

### 作用
快速验证主链路一致性（smoke test）。不修改数据，不启动前端。

### 依赖
- Python 3.9
- `scripts/smoke_test.py` 可执行
- `04_数据与规则/` 下中间层 JSON 文件存在

### 关键参数
| 参数 | 说明 |
|------|------|
| `--fast` | 仅快速校验（主链路一致性，<10s） |
| `--full` | 完整校验（全部检查，60s+） |
| `--parse-only` | 只校验 parse 环节 |
| `--queue-only` | 只校验 review queue 环节 |
| `--tracking-only` | 只校验 tracking 环节 |
| `--report-only` | 只校验周报环节 |
| `--bundle-only` | 只校验 bundle 环节 |

默认 `--fast`。

### 成功判定标准
- 输出 `PASS`（非 `WARN` 或 `FAIL`）
- 全部 38 项检查通过
- 关联的 JSON 文件时间戳一致

### 失败处理
- 某项 FAIL：该步骤数据/文件问题，定位到具体检查项
- 数据过期：检查 `observedAt` 时间戳

---

## 入口三：run_report.sh

### 作用
重生成周报和前端数据包（review 完成后执行）。不重跑 parse。

### 依赖
- Python 3.9
- `scripts/generate_weekly_report.py`
- `scripts/build_web_bundle.py`
- 中间层 JSON 文件（`deposit_benchmark.json` 等）已存在
- `06_进展状态/review-status.json` 已更新

### 关键参数
无参数，默认重生成周报 + 打包 bundle。

如需单独执行：
```bash
python3 scripts/generate_weekly_report.py    # 仅周报
python3 scripts/build_web_bundle.py            # 仅 bundle
```

### 成功判定标准
- `06_进展状态/weekly-report-draft.md` 生成时间戳为当天
- `03_前端页面/app-data.js` 生成时间戳为当天
- 周报第一节核心结论不为空

### 失败处理
- 中间层 JSON 缺失：先跑 `bash scripts/run_smoke.sh` 确认
- review-status.json 过期：先执行 `python3 scripts/record_review.py`

---

## 月度数据导入（如有 Excel 更新）

```bash
# 先 dry-run 看影响
python3 scripts/import_monthly_data.py --dry-run

# 确认无误后正式导入
python3 scripts/import_monthly_data.py --confirm
```

---

## 日常运行命令参考（OPENCLAW_DEPLOYMENT.md）

```bash
# 完整链路
bash scripts/run_dev.sh

# 仅 smoke test
bash scripts/run_smoke.sh

# 仅报告生成
bash scripts/run_report.sh

# 启动前端（不跑 pipeline）
cd 03_前端页面 && python3 -m http.server 8787
```

---

## 路径约定

| 路径变量 | 实际值 |
|----------|--------|
| `OPENCLAW_DEPLOY_BASE` | `/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY` |
| `DATA_DIR` | `$OPENCLAW_DEPLOY_BASE/04_数据与规则` |
| `SCRIPT_DIR` | `$OPENCLAW_DEPLOY_BASE/scripts` |
| `REPORT_DIR` | `$OPENCLAW_DEPLOY_BASE/06_进展状态` |
| `FRONTEND_DIR` | `$OPENCLAW_DEPLOY_BASE/03_前端页面` |
