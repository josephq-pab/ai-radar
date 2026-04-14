#!/bin/bash
# run_smoke.sh — 对公 AI 雷达站快速验证入口
set -e
SCRIPT_BASE="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本"
PYTHON="/tmp/py39env/bin/python"
echo "=== AI雷达站 Smoke Test ==="
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY
MODE="${1:-"--fast"}"
echo "模式: $MODE"
$PYTHON "$SCRIPT_BASE/smoke_test.py" $MODE
