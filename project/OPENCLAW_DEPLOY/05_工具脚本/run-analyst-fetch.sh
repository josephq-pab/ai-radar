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
#   ./run-analyst-fetch.sh              # 执行抓取（默认：对公存款）
#   ./run-analyst-fetch.sh --check      # dry-run 模式（不写文件）
#   ./run-analyst-fetch.sh --dim-trial  # 维度扩展试探：对公存款+对公贷款 两次抓取并合并
#
# 前置条件：
#   - python3 环境可用（/tmp/py39env/bin/python3）
#   - 依赖已安装：pip install scrapling beautifulsoup4
#
# 产出：
#   - 默认模式：更新 04_数据与规则/processed/analyst_opinions_raw.json
#   - --check 模式：仅展示抓取预览，不写文件
#   - --dim-trial 模式：两次抓取后合并到 analyst_opinions_raw.json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY"
PYTHON="/tmp/py39env/bin/python3"
FETCH_SCRIPT="${SCRIPT_DIR}/fetch_analyst_articles.py"
OUTPUT="${BASE}/04_数据与规则/processed/analyst_opinions_raw.json"

MODE="${1:-}"

_do_fetch() {
    local dim="$1"
    local out_file="$2"
    echo "  >> 抓取维度: ${dim}"
    "${PYTHON}" "${FETCH_SCRIPT}" --dimension "${dim}" --output "${out_file}"
}

_do_merge() {
    local file_a="$1"
    local file_b="$2"
    local out_merged="$3"
    echo "  >> 合并两次抓取结果..."
    "${PYTHON}" -c "
import json

def load_records(path):
    try:
        with open(path) as f:
            d = json.load(f)
        return d.get('records', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

ra = load_records('${file_a}')
rb = load_records('${file_b}')

# dedup by (title, analystName, publishedAt)
seen = set()
merged = []
for r in ra + rb:
    key = (r.get('title',''), r.get('analystName',''), r.get('publishedAt',''))
    if key not in seen:
        seen.add(key)
        merged.append(r)

with open('${out_merged}', 'w') as f:
    json.dump({'records': merged, 'fetchedAt': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'}, f, ensure_ascii=False, indent=2)

print(f'  合并完成: {len(ra)} + {len(rb)} -> {len(merged)} 条（去重后）')
"
}

if [[ "${MODE}" == "--check" ]]; then
    echo "=========================================="
    echo "  analyst 数据抓取检查模式（dry-run）"
    echo "  模式: --check（不写文件）"
    echo "=========================================="
    "${PYTHON}" "${FETCH_SCRIPT}" --dry-run --dimension 对公存款
    echo ""
    echo "[check] dry-run 完成，建议查看上方输出后："
    echo "  - 若确认抓取，按正常模式执行：./run-analyst-fetch.sh"
    echo "  - 若做维度扩展试探：./run-analyst-fetch.sh --dim-trial"
    echo "  - 然后执行 preflight 检查，判断是否值得运行完整轮次"

elif [[ "${MODE}" == "--dim-trial" ]]; then
    echo "=========================================="
    echo "  analyst 数据抓取 — 维度扩展试探模式"
    echo "  模式: 对公存款 + 对公贷款 两次抓取并合并"
    echo "  输出: ${OUTPUT}"
    echo "=========================================="
    TMPDIR=$(mktemp -d)
    FILE_A="${TMPDIR}/fetch_a.json"
    FILE_B="${TMPDIR}/fetch_b.json"
    # Always do 对公存款 first to preserve existing pool as base
    _do_fetch "对公存款" "${FILE_A}"
    echo ""
    _do_fetch "对公贷款" "${FILE_B}"
    echo ""
    _do_merge "${FILE_A}" "${FILE_B}" "${OUTPUT}"
    rm -rf "${TMPDIR}"
    echo ""
    echo "抓取完成（维度扩展试探模式）。数据已刷新至：${OUTPUT}"
    echo "建议下一步：执行 preflight 检查，判断是否值得运行完整轮次。"
    echo "  preflight 命令：读取 analyst_opinions_raw.json 的 fetchedAt 与条数"

else
    echo "=========================================="
    echo "  analyst 数据抓取（人工刷新）"
    echo "  入口: fetch_analyst_articles.py"
    echo "  输出: ${OUTPUT}"
    echo "=========================================="
    "${PYTHON}" "${FETCH_SCRIPT}" --dimension 对公存款
    echo ""
    echo "抓取完成。数据已刷新。"
    echo "建议下一步：执行 preflight 检查，判断是否值得运行完整轮次。"
    echo "  preflight 命令：读取 analyst_opinions_raw.json 的 fetchedAt 与条数"
    echo "  完整运行命令：./run-analyst.sh"
fi
