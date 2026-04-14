# 对公 AI 雷达站 — 项目说明

> **唯一开发路径**：`/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/`
> 本文件最后更新：2026-04-07

---

## 项目定位

对公 AI 雷达站是面向银行对公业务管理部的经营情报与观点研判系统。

**核心链路：**
1. 接入同业对标数据（存款/贷款/利率）+ 外部分析师观点 + 政策信息
2. 加工成结构化情报 → 人工 review 确认 → 闭环跟踪 → 周报生成

**当前阶段：** Phase 2 完成，Phase F（工程化迁移）待开始

---

## 目录结构

| 目录 | 用途 |
|------|------|
| `01_项目说明/` | 项目背景、目标、架构 |
| `02_规范文档/` | PRD、架构、数据模型、SOP |
| `03_前端页面/` | 7个 HTML 页面 + 前端数据包 |
| `04_数据与规则/` | 原始数据（含 processed/ 子目录），迁移自旧路径，内容与 `data/` 相同 |
| `05_工具脚本/` | Python 脚本入口（含 paths.py 统一路径配置） |
| `06_进展状态/` | 人工维护的状态文档（CURRENT_STATUS.md 等） |
| `07_历史备份/` | 关键历史版本快照 |
| `08_设计规范补充/` | 前端 UI 参照标准 |
| `data/` | **脚本使用的当前数据目录**（由 paths.py 管理，含 processed/ 和 raw/） |
| `docs/` | 阻断项说明、评估规则 |
| `eval/` | Smoke 检查清单、评估规则 |
| `reports/` | review/tracking 产物（由 Python 脚本写入） |
| `reviews/` | review 日志 |

---

## 环境信息

- **Python：** `/tmp/py39env/bin/python`（3.9.25）
- **Scrapling：** 0.2.99（抓取用）
- **前端端口：** 8787
- **数据路径：** `04_数据与规则/`

---

## 运行入口（三个统一入口）

| 脚本 | 作用 |
|------|------|
| `scripts/run_dev.sh` | 本地开发：启动前端 + 跑全量 pipeline |
| `scripts/run_smoke.sh` | 快速验证：smoke test 38 项检查 |
| `scripts/run_report.sh` | 报告生成：周报重生成 + bundle 打包 |

详见 `RUNBOOK.md`。

---

## Gate 状态

| Gate | 状态 | 说明 |
|------|------|------|
| A | ❌ BLOCKED | 贷款利率数据停留在 2025-12-01，目标 ≥ 2026-03-01 |
| B | ✅ CLEARED | usable=4, referenceable=2, reportable=3 |
| C | ✅ CLEARED | 0 blockers，15 followups |

**唯一阻断项：** 缺少 2026-03 贷款利率 Excel 文件。

---

## 验证状态

- **smoke test：** ✅ 38/38 PASS
- **pipeline：** ✅ 主链路一致，bundle 新鲜
- **前端：** 可在 8787 端口正常浏览

---

## 路径声明

- **唯一开发路径（2026-04-07 起）：** `/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/`
- **旧路径（仅作历史备份，不再开发）：** `/home/admin/.openclaw/workspace/ai-radar-station/OPENCLAW_DEPLOY/`
- 所有新开发、测试、运行必须在唯一开发路径内进行

---

## 依赖安装

```bash
/tmp/py39env/bin/pip install -r requirements.txt
```

或手动安装核心依赖：
```bash
pip install beautifulsoup4 scrapling==0.2.99 openpyxl
```
