#!/bin/bash
# run_report.sh — 对公 AI 雷达站报告生成入口
set -e
SCRIPT_BASE="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本"
PYTHON="/tmp/py39env/bin/python"
DEPLOY="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY"
echo "=== AI雷达站 报告生成 ==="
cd "$DEPLOY"
echo "时间: $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "[1/3] 检查中间层 JSON ..."
REQUIRED_FILES=(
    "04_数据与规则/processed/deposit_benchmark.json"
    "04_数据与规则/processed/loan_benchmark.json"
    "04_数据与规则/processed/loan_rate.json"
    "06_进展状态/review-status.json"
    "06_进展状态/review-queue.json"
)
for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$DEPLOY/$f" ]; then
        echo "  ❌ 缺失: $f"
        echo "  → 请先执行: bash scripts/run_smoke.sh"
        exit 1
    fi
    echo "  ✅ $f"
done
echo ""
echo "[2/3] 生成周报 ..."
$PYTHON "$SCRIPT_BASE/generate_weekly_report.py"
echo "  ✅ 周报生成完成"
echo ""
echo "[3/3] 打包前端 bundle ..."
$PYTHON "$SCRIPT_BASE/build_web_bundle.py"
echo "  ✅ Bundle 打包完成"
echo ""
REPORT_TS=$(date -r "$DEPLOY/06_进展状态/weekly-report-draft.md" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "未知")
BUNDLE_TS=$(date -r "$DEPLOY/03_前端页面/app-data.js" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "未知")
echo "=== 报告生成完成 ==="
echo "周报时间戳: $REPORT_TS"
echo "Bundle时间戳: $BUNDLE_TS"
