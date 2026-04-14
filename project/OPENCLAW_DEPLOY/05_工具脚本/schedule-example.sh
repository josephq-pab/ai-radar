#!/bin/bash
# =====================================================
# 对公 AI 雷达站 - 试运行调度脚本示例（Phase 2 基线）
# =====================================================
# 路径：所有脚本使用项目相对路径，不再硬编码 HOME
#
# 使用方式:
#   1. Cron: 将命令加入 crontab（参见 ../ops/cron.example）
#   2. Launchd: 创建 plist 文件并加载（参见 docs/trial-runbook.md）
#   3. 手动: ./schedule-example.sh daily|weekly|smoke|full
# =====================================================

set -e

# ============ 路径配置（Phase 2: 相对路径）===============
# 脚本所在目录 → 项目根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"   # .../ai-radar-station/scripts
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"       # .../ai-radar-station
LOG_DIR="${PROJECT_DIR}/logs"

# 运行时区
TZ="Asia/Shanghai"
export TZ

# ============ 函数定义 ============

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

run_full() {
    log "开始执行: full 模式 (数据解析 + analyst 抓取 + 周报生成 + tracking + web bundle + smoke test)"
    cd "$PROJECT_DIR"
    python3 scripts/run-pipeline.py --full 2>&1 | tee -a "${LOG_DIR}/full-$(date '+%Y%m%d-%H%M%S').log"
}

run_rebuild() {
    log "开始执行: rebuild-only 模式 (仅重建周报 + tracking + web bundle，不跑解析)"
    cd "$PROJECT_DIR"
    python3 scripts/run-pipeline.py --rebuild-only 2>&1 | tee -a "${LOG_DIR}/rebuild-$(date '+%Y%m%d-%H%M%S').log"
}

run_smoke() {
    log "开始执行: smoke-only 模式 (轻量校验)"
    cd "$PROJECT_DIR"
    python3 scripts/smoke_test.py --fast 2>&1 | tee -a "${LOG_DIR}/smoke-$(date '+%Y%m%d-%H%M%S').log"
}

check_health() {
    # 读取 run-summary.json 判断健康度
    local summary_file="${PROJECT_DIR}/reports/run-summary.json"
    if [ ! -f "$summary_file" ]; then
        echo "⚠️ run-summary.json 不存在，可能未正常完成运行"
        return 1
    fi

    # 提取 verdict（兼容有无 exitCode 字段）
    local verdict
    verdict=$(python3 -c "import json,sys; d=json.load(open('$summary_file')); print(d.get('verdict','unknown'))" 2>/dev/null || echo "unknown")
    local success
    success=$(python3 -c "import json,sys; d=json.load(open('$summary_file')); print(d.get('success',''))" 2>/dev/null || echo "unknown")

    if [ "$verdict" = "usable" ] || [ "$success" = "True" ]; then
        echo "✅ 运行成功 (verdict=$verdict)"
        return 0
    else
        echo "⚠️ 运行可能存在异常 (verdict=$verdict, success=$success)"
        return 1
    fi
}

# ============ 主逻辑 ============

# 创建日志目录
mkdir -p "$LOG_DIR"

MODE="${1:-daily}"

case "$MODE" in
    daily)
        log "========== 日常刷新模式 =========="
        run_rebuild
        check_health
        ;;
    weekly)
        log "========== 周报刷新模式 =========="
        run_full
        check_health
        ;;
    smoke)
        log "========== 轻量校验模式 =========="
        run_smoke
        ;;
    full)
        log "========== 完整刷新模式 =========="
        run_full
        check_health
        ;;
    *)
        echo "用法: $0 [daily|weekly|smoke|full]"
        echo "  daily  - 工作日轻量刷新 (rebuild-only，不跑数据解析)"
        echo "  weekly - 每周完整刷新 (full)"
        echo "  smoke  - 仅运行 smoke test"
        echo "  full   - 手动执行完整刷新"
        exit 1
        ;;
esac

log "========== 执行完成 =========="
