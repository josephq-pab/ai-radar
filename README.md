# AI雷达站 Agent - 自述

## ⚠️ 重要路径声明

**唯一开发路径**（2026-04-07 起）：

```
/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/
```

**旧路径已废弃**：`/home/admin/.openclaw/workspace/ai-radar-station/OPENCLAW_DEPLOY/`（历史备份，不再开发）

凡涉及 AI 雷达站的代码修改、测试、运行、报告输出，**一律在本路径进行**。

---

**Agent ID**: ai-radar
**显示名**: AI雷达站
**项目**: 对公 AI 雷达站
**状态**: 独立运行，新路径为唯一开发路径

---

## 项目概况

| 项目 | 说明 |
|------|------|
| 项目名称 | 对公 AI 雷达站 |
| 当前路径 | `/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/` |
| Pipeline | `python3 05_工具脚本/run-pipeline.py --full` |
| 前端端口 | 8787 |
| Python | `/tmp/py39env/bin/python` |
| smoke_test | 38/38 PASS |

---

## 当前阻断

- **A gate**：缺 2026-03 贷款利率数据
- 需将 `贷款利率-2603.xlsx`（或同义文件）放入 `04_数据与规则/raw/`

---

## 目录结构

```
project/OPENCLAW_DEPLOY/
├── 01_项目说明/       ← 项目文档
├── 02_规范文档/       ← PRD/架构/数据契约
├── 03_前端页面/       ← HTML 页面（浏览器打开）
├── 04_数据与规则/
│   ├── raw/           ← 原始 Excel（数据入口）
│   ├── processed/     ← JSON 中间层
│   └── analyst_cache/ ← 抓取缓存
├── 05_工具脚本/       ← 所有 Python 脚本
└── 06_进展状态/       ← 报告/状态 JSON
```

---

## 常用命令

```bash
# 运行完整 pipeline
bash /tmp/run-pipeline.sh --full

# 快速检查 smoke_test
/tmp/py39env/bin/python 05_工具脚本/smoke_test.py --fast

# 查看 gate 状态
/tmp/py39env/bin/python 05_工具脚本/rebuild_go_live_gate.py --check

# 更新分析师观点
/tmp/py39env/bin/python 05_工具脚本/fetch_analyst_articles.py --dimension 对公存款 --min-year 2024
```
