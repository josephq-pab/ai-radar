#!/bin/bash
# run-analyst.sh — analyst 试点运行统一入口
# ===========================================
# 职责：orchestration only，不含任何评分/过滤/review 业务逻辑
# 调用范围：
#   1. build_analyst_opinions.py      （构建 analyst opinions）
#   2. generate_review_queue.py        （生成 review queue）
#   3. review-tracker.py merge         （合并 tracker 状态）
#   4. review-tracker.py export        （导出 ledger CSV）
#
# 使用方式：
#   cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本
#   OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY ./run-analyst.sh
#
# 注意：本脚本为 analyst 试点运行专用入口
#       run-pipeline.py 为 Phase 2 旧入口，本阶段不作为 analyst 试点入口

set -euo pipefail

# ── 路径配置 ─────────────────────────────────────────────
BASE="${OPENCLAW_DEPLOY_BASE:-/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY}"
PYTHON="${PYTHON:-/tmp/py39env/bin/python3}"
SCRIPT_DIR="$BASE/05_工具脚本"
REPORTS_DIR="$BASE/reports"

echo "═══════════════════════════════════════════════════"
echo "  analyst 试点运行 — 统一入口"
echo "  BASE: $BASE"
echo "═══════════════════════════════════════════════════"

# ── Step 1: build_analyst_opinions.py ───────────────────
echo ""
echo "▶ Step 1/4: build_analyst_opinions.py"
if ! OPENCLAW_DEPLOY_BASE="$BASE" "$PYTHON" "$SCRIPT_DIR/build_analyst_opinions.py"; then
    echo "❌ build_analyst_opinions.py 失败，退出"
    exit 1
fi
echo "✅ Step 1 完成"

# ── Step 2: generate_review_queue.py ────────────────────
echo ""
echo "▶ Step 2/4: generate_review_queue.py"
if ! OPENCLAW_DEPLOY_BASE="$BASE" "$PYTHON" "$SCRIPT_DIR/generate_review_queue.py"; then
    echo "❌ generate_review_queue.py 失败，退出"
    exit 1
fi
echo "✅ Step 2 完成"

# ── Step 3: review-tracker.py merge ─────────────────────
echo ""
echo "▶ Step 3/4: review-tracker.py merge"
if ! OPENCLAW_DEPLOY_BASE="$BASE" "$PYTHON" "$SCRIPT_DIR/review-tracker.py" merge; then
    echo "⚠️  review-tracker.py merge 失败，继续（可能无新增变化）"
else
    echo "✅ Step 3 完成"
fi

# ── Step 4: review-tracker.py export ───────────────────
echo ""
echo "▶ Step 4/4: review-tracker.py export"
OPENCLAW_DEPLOY_BASE="$BASE" "$PYTHON" "$SCRIPT_DIR/review-tracker.py" export \
    --output "$REPORTS_DIR/pilot-tracking-ledger.csv"
echo "✅ Step 4 完成"

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ analyst 试点运行完成"
echo "  output: $REPORTS_DIR/analyst-review-queue.json"
echo "  ledger: $REPORTS_DIR/pilot-tracking-ledger.csv"
echo "═══════════════════════════════════════════════════"
