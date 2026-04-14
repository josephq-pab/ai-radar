#!/usr/bin/env bash
#
# run-analyst-fetch.sh — analyst 数据人工刷新统一入口
#
# 职责边界：
#   - 只做 fetch orchestration（调用 fetch_analyst_articles.py）
#   - 不内嵌 preflight 判断
#   - 不内嵌 run-analyst.sh
#   - 不做自动进入下一轮的联动
#
# 使用方式：
#   ./run-analyst-fetch.sh         # 执行真实抓取，刷新 analyst_opinions_raw.json
#   ./run-analyst-fetch.sh --check # dry-run 模式，只展示待抓取内容，不写文件
#
# 前置条件：
#   - python3 环境可用（/tmp/py39env/bin/python3）
#   - 依赖已安装：pip install scrapling beautifulsoup4
#
# 产出：
#   - 默认模式：更新 04_数据与规则/processed/analyst_opinions_raw.json
#   - --check 模式：仅展示抓取预览，不写文件

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY"
PYTHON="/tmp/py39env/bin/python3"
FETCH_SCRIPT="${SCRIPT_DIR}/fetch_analyst_articles.py"

MODE="${1:-}"

if [[ "${MODE}" == "--check" ]]; then
    echo "=========================================="
    echo "  analyst 数据抓取检查模式（dry-run）"
    echo "  模式: --check（不写文件）"
    echo "=========================================="
    "${PYTHON}" "${FETCH_SCRIPT}" --dry-run --dimension 对公存款
    echo ""
    echo "[check] dry-run 完成，建议查看上方输出后："
    echo "  - 若确认抓取，按正常模式执行：./run-analyst-fetch.sh"
    echo "  - 然后执行 preflight 检查，再决定是否运行完整轮次"
else
    echo "=========================================="
    echo "  analyst 数据抓取（人工刷新）"
    echo "  入口: fetch_analyst_articles.py"
    echo "  输出: ${BASE}/04_数据与规则/processed/analyst_opinions_raw.json"
    echo "=========================================="
    "${PYTHON}" "${FETCH_SCRIPT}" --dimension 对公存款
    echo ""
    echo "抓取完成。数据已刷新。"
    echo "建议下一步：执行 preflight 检查，判断是否值得运行完整轮次。"
    echo "  preflight 命令：读取 analyst_opinions_raw.json 的 fetchedAt 与条数"
    echo "  完整运行命令：./run-analyst.sh"
fi
