#!/usr/bin/env python3
"""
paths.py — 项目路径配置

所有脚本统一从此处导入路径配置，不再各自硬编码 BASE。
用法：
    from paths import BASE, SCRIPTS, REPORTS, DATA, etc.
"""
from __future__ import annotations

import os
from pathlib import Path

# ── 原则 ─────────────────────────────────────────────────────────
# 1. 始终以本文件所在目录为锚点，推算项目根目录
# 2. 不依赖环境变量 HOME、USER 等不确定因素
# 3. 可通过 PROJECT_DIR 环境变量覆盖（用于测试或非标准部署）
# ────────────────────────────────────────────────────────────────

# ── 部署环境路径覆盖 ──────────────────────────────────────────
# 在此填入实际部署路径，确保所有脚本指向正确目录
_SCRIPT_DIR = Path(__file__).resolve().parent  # .../OPENCLAW_DEPLOY/05_工具脚本
_DEPLOY_BASE = os.environ.get('OPENCLAW_DEPLOY_BASE')
if _DEPLOY_BASE:
    BASE = Path(_DEPLOY_BASE)
else:
    BASE = _SCRIPT_DIR.parent  # 自动从脚本位置推导

SCRIPTS      = BASE / 'scripts'
DATA         = BASE / 'data'
RAW_DATA     = DATA / 'raw'
PROCESSED    = DATA / 'processed'
REPORTS      = BASE / 'reports'
REVIEWS      = BASE / 'reviews'
WEB_DATA     = BASE / 'apps' / 'web' / 'data'
OPS          = BASE / 'ops'
CONFIG       = BASE / 'config'

# ── 派生路径别名（与旧脚本兼容）────────────────────────────────
WEB_APPS     = BASE / 'apps' / 'web'

# ── 关键产物路径 ────────────────────────────────────────────────
REVIEW_LOG           = REVIEWS / 'review-log.jsonl'
TRACKING_ITEMS       = REPORTS / 'tracking-items.json'
REVIEW_STATUS        = REPORTS / 'review-status.json'
REVIEW_QUEUE         = REPORTS / 'review-queue.json'
WEEKLY_REPORT        = REPORTS / 'weekly-report-draft.md'
RUN_SUMMARY          = REPORTS / 'run-summary.json'
GO_LIVE_GATE         = REPORTS / 'go-live-gate.json'
ANALYST_OPINIONS     = PROCESSED / 'analyst_opinions.json'
ANALYST_OPINIONS_RAW = PROCESSED / 'analyst_opinions_raw.json'

# ── 快速检测：项目根目录是否存在 ───────────────────────────────
def assert_project_root(path: Path = BASE) -> None:
    """调试用：确认项目根目录结构完整"""
    required = [SCRIPTS, DATA, REPORTS, REVIEWS]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError(
            f"项目根目录不完整，缺少: {', '.join(missing)}\n"
            f"BASE resolved to: {path}\n"
            f"scripts/__file__ = {__file__}"
        )


if __name__ == '__main__':
    # 直接运行时输出诊断信息
    print(f"paths.py 诊断:")
    print(f"  __file__   = {__file__}")
    print(f"  _SCRIPT_DIR= {_SCRIPT_DIR}")
    print(f"  BASE       = {BASE}")
    for name, path in [
        ("SCRIPTS", SCRIPTS),
        ("DATA", DATA),
        ("PROCESSED", PROCESSED),
        ("REPORTS", REPORTS),
        ("REVIEWS", REVIEWS),
        ("WEB_DATA", WEB_DATA),
    ]:
        status = "✅" if path.exists() else "❌ MISSING"
        print(f"  {name:15s} {status}  {path}")
