#!/bin/bash
# run_dev.sh — 对公 AI 雷达站本地开发完整链路
set -e
SCRIPT_BASE="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本"
FRONTEND_DIR="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/03_前端页面"
PYTHON="/tmp/py39env/bin/python"
echo "=== AI雷达站 开发链路 ==="
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY
if lsof -i :8787 > /dev/null 2>&1; then
    echo "  ⚠️  端口 8787 已被占用，跳过启动"
else
    cd "$FRONTEND_DIR" && python3 -m http.server 8787 &
    sleep 1
    echo "  ✅ 前端已启动: http://localhost:8787"
    cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY
fi
echo ""
echo "[2/3] 执行完整 pipeline ..."
$PYTHON "$SCRIPT_BASE/run-pipeline.py" --full
echo ""
echo "[3/3] Smoke test 快速验证 ..."
$PYTHON "$SCRIPT_BASE/smoke_test.py" --fast
echo ""
echo "=== 开发链路完成 ==="
