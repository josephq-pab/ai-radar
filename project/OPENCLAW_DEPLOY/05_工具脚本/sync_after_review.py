#!/usr/bin/env python3
"""
sync_after_review.py — 决策后低摩擦半自动同步

Single Source of Truth（Phase 2）：
  A/B/C gate、readinessLevels、gateType、blockers、goLiveCriteria
  统一由 rebuild_go_live_gate.py 生成。本脚本调用该脚本获取 gate 数据，
  不独立计算任何 gate 相关字段。

用法：
    # 正式执行（写入文件）
    python3 scripts/sync_after_review.py --confirm

    # 演练模式（只打印计划，不写文件）
    python3 scripts/sync_after_review.py --dry-run

    # 演练模式详细（显示每步会做什么）
    python3 scripts/sync_after_review.py --dry-run --verbose

行为：
    1. build_review_status.py       — 重建 review 确认状态
    2. build_tracking_items.py      — 重建 tracking 中间层（含状态覆盖）
    3. rebuild_go_live_gate.py     — 重建 A/B/C gate（单一真相源，含 gateType 同步）
    4. generate_weekly_report.py    — 重建周报（含第九+十节）
    5. build_web_bundle.py          — 重建前端 bundle
    6. fast-check（内联）            — 运行快速一致性校验
    7. run_summary 更新             — 由 rebuild_go_live_gate.py 内联完成

默认安全策略：
    - 默认 dry-run（不加 --dry-run 时也要求确认，除非加 --confirm）
    - 某一步失败时停在该步，打印错误，退出码非 0
    - 成功后打印汇总和当前可用性判断
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Phase 2: 统一路径解析
try:
    from paths import BASE, SCRIPTS, REPORTS, WEB_DATA
except ImportError:
    BASE = Path(__file__).resolve().parent.parent
    SCRIPTS = BASE / 'scripts'
    REPORTS = BASE / 'reports'
    WEB_DATA = BASE / 'apps' / 'web' / 'data'

DRY_RUN = '--dry-run' in sys.argv[1:]
VERBOSE = '--verbose' in sys.argv[1:]
CONFIRM = '--confirm' in sys.argv[1:]

STEPS = [
    {
        'name': 'build_review_status.py',
        'desc': '重建 review 确认状态',
        'script': 'build_review_status.py',
        'required': True,
    },
    {
        'name': 'build_tracking_items.py',
        'desc': '重建 tracking 中间层（含状态覆盖）',
        'script': 'build_tracking_items.py',
        'required': True,
    },
    {
        'name': 'rebuild_go_live_gate.py',
        'desc': '重建 A/B/C gate（单一真相源，含 readinessLevels + gateType 同步）',
        'script': 'rebuild_go_live_gate.py',
        'required': True,
    },
    {
        'name': 'generate_weekly_report.py',
        'desc': '重建周报（含第九+十节）',
        'script': 'generate_weekly_report.py',
        'required': True,
    },
    {
        'name': 'build_web_bundle.py',
        'desc': '重建前端 bundle',
        'script': 'build_web_bundle.py',
        'required': True,
    },
]


def header(msg: str) -> None:
    print(f'\n{"─"*52}')
    print(f'  {msg}')
    print(f'{"─"*52}')


def step(name: str, script: str, required: bool, dry_run: bool) -> bool:
    """运行单个步骤，返回是否成功"""
    cmd = [sys.executable, str(SCRIPTS / script)]
    if dry_run:
        icon = '  [DRY-RUN]'
        print(f'{icon} ▶ {name}')
        print(f'          {" ".join(str(c) for c in cmd)}')
        return True

    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    elapsed = time.time() - t0
    status = '✅ OK' if result.returncode == 0 else f'❌ FAIL ({result.returncode})'
    print(f'  ▶ {name}  {status}  ({elapsed:.1f}s)')
    if VERBOSE or result.returncode != 0:
        for line in result.stdout.strip().split('\n')[-5:]:
            if line.strip():
                print(f'    └ {line}')
    if result.returncode != 0:
        if result.stderr:
            for line in result.stderr.strip().split('\n')[:3]:
                if line.strip():
                    print(f'    └ [ERR] {line}')
        if required:
            print(f'\n  ❌ 必需步骤失败，停止同步。')
            return False
        else:
            print(f'  ⚠️  非必需步骤失败，继续。')
    return True


def run_fast_check(dry_run: bool) -> dict:
    """内联运行 fast-check，返回摘要

    Phase 2: 不再做独立 gate 计算，直接读取 go-live-gate.json 的最新状态。
    """
    if dry_run:
        print('\n  [DRY-RUN] ▶ fast-check（内联）')
        return {'PASS': 0, 'WARN': 0, 'FAIL': 0, 'exit_code': 0}

    print('\n  ▶ fast-check（内联）')
    t0 = time.time()

    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}

    # ── tracking-items ───────────────────────────────────
    ti_path = REPORTS / 'tracking-items.json'
    ok, ti_data, _ = True, None, ''
    try:
        ti_data = json.loads(ti_path.read_text(encoding='utf-8'))
    except Exception as e:
        ok = False
    if ok and ti_data:
        items = ti_data.get('items', [])
        summary = ti_data.get('trackingStatusSummary', {})
        outcomes['PASS'] += 1
        print(f'    ✅ tracking-items.json OK ({len(items)} items)')
        for st, cnt in summary.items():
            print(f'       └ {st}: {cnt}')
    else:
        outcomes['FAIL'] += 1
        print(f'    ❌ tracking-items.json 读取失败')

    # ── go-live-gate ─────────────────────────────────────
    # Phase 2: 验证 gate 单一真相源是否已更新
    gate_path = REPORTS / 'go-live-gate.json'
    gate_ok = False
    try:
        gate_data = json.loads(gate_path.read_text(encoding='utf-8'))
        gates = gate_data.get('gates', {})
        a_passed = gates.get('A_dataFreshness', {}).get('all_passed', False)
        b_passed = gates.get('B_analystQuality', {}).get('all_passed', False)
        c_passed = gates.get('C_pendingCompletion', {}).get('all_passed', False)
        readiness = gate_data.get('readinessStatus', {})
        rp = readiness.get('reportPrepReadiness', 'unknown')
        print(f'    ✅ go-live-gate.json OK')
        print(f'       └ A_gate: {"cleared" if a_passed else "blocked"}')
        print(f'       └ B_gate: {"cleared" if b_passed else "blocked"}')
        print(f'       └ C_gate: {"cleared" if c_passed else "blocked"}')
        print(f'       └ reportPrepReadiness: {rp}')
        outcomes['PASS'] += 1
        gate_ok = True
    except Exception as e:
        outcomes['FAIL'] += 1
        print(f'    ❌ go-live-gate.json 读取失败: {e}')

    # ── 周报第九+十节 ───────────────────────────────────
    wr_path = REPORTS / 'weekly-report-draft.md'
    if wr_path.exists():
        text = wr_path.read_text(encoding='utf-8')
        sec9 = '## 九、重点事项跟踪状态汇总' in text
        sec10 = '## 十、事项明细' in text
        if sec9:
            outcomes['PASS'] += 1
            print(f'    ✅ 周报第九节存在')
        else:
            outcomes['FAIL'] += 1
            print(f'    ❌ 周报第九节缺失')
        if sec10:
            outcomes['PASS'] += 1
            print(f'    ✅ 周报第十节存在')
        else:
            outcomes['FAIL'] += 1
            print(f'    ❌ 周报第十节缺失')

        # 一致性：第九节数字与 tracking-items 对比
        if sec9 and ti_data:
            summary = ti_data.get('trackingStatusSummary', {})
            import re as re2
            m = re2.search(r'待研判[：:]\s*(\d+)', text)
            if m:
                r9 = int(m.group(1))
                r10 = summary.get('待研判', 0)
                if r9 == r10:
                    outcomes['PASS'] += 1
                    print(f'    ✅ 第九节待研判={r9} 与 tracking-items={r10} 一致')
                else:
                    outcomes['FAIL'] += 1
                    print(f'    ❌ 第九节待研判={r9} 与 tracking-items={r10} 不一致')
        else:
            outcomes['FAIL'] += 1
    else:
        outcomes['FAIL'] += 1
        print(f'    ❌ weekly-report-draft.md 不存在')

    # ── bundle 一致性 ───────────────────────────────────
    bundle_path = WEB_DATA / 'app-data.js'
    if bundle_path.exists() and ti_data:
        bundle_text = bundle_path.read_text(encoding='utf-8')
        prefix_ok = bundle_text.startswith('window.AIRadarData = ')
        if prefix_ok:
            outcomes['PASS'] += 1
            print(f'    ✅ bundle 前缀正确')
        else:
            outcomes['FAIL'] += 1
            print(f'    ❌ bundle 前缀异常')

        # tracking items 数量对比（JSON 解析方式）
        import json as _json
        ti_items = ti_data.get('items', [])
        json_text = bundle_text[len('window.AIRadarData = '):].rstrip().rstrip(';').rstrip()
        try:
            bundle_data = _json.loads(json_text)
            ti_bundle = bundle_data.get('trackingItems', {})
            bundle_items = ti_bundle.get('items', []) if isinstance(ti_bundle, dict) else []
            bundle_count = len(bundle_items)
        except Exception:
            bundle_count = -1

        if bundle_count == len(ti_items):
            outcomes['PASS'] += 1
            print(f'    ✅ bundle trackingItems={bundle_count} 与 tracking-items.json={len(ti_items)} 一致')
        else:
            outcomes['FAIL'] += 1
            print(f'    ❌ bundle trackingItems={bundle_count} 与 tracking-items.json={len(ti_items)} 不一致')

        # mtime 检查
        from datetime import datetime as dt
        ti_mtime = dt.fromtimestamp(ti_path.stat().st_mtime)
        bundle_mtime = dt.fromtimestamp(bundle_path.stat().st_mtime)
        if bundle_mtime >= ti_mtime:
            outcomes['PASS'] += 1
            print(f'    ✅ bundle ({bundle_mtime.strftime("%H:%M")}) >= tracking-items ({ti_mtime.strftime("%H:%M")})')
        else:
            outcomes['WARN'] += 1
            print(f'    ⚠️  bundle ({bundle_mtime.strftime("%H:%M")}) < tracking-items ({ti_mtime.strftime("%H:%M")})，bundle 可能未更新')
    else:
        outcomes['FAIL'] += 1
        print(f'    ❌ bundle 不存在')

    elapsed = time.time() - t0
    total = outcomes['PASS'] + outcomes['WARN'] + outcomes['FAIL']
    print(f'\n  fast-check 汇总  ✅{outcomes["PASS"]}  ⚠️{outcomes["WARN"]}  ❌{outcomes["FAIL"]}  ({total} 项, {elapsed:.1f}s)')
    outcomes['exit_code'] = 1 if outcomes['FAIL'] > 0 else 0
    return outcomes


def update_run_summary(fast_result: dict, gate_data: dict = None) -> None:
    """在 run-summary.json 中注入本次同步信息和 gate 状态

    Phase 2: readinessLevels 和 gateType 由 rebuild_go_live_gate.py 统一维护。
    本函数仅补充 sync_after_review 特有的时序元数据。
    """
    rs_path = REPORTS / 'run-summary.json'
    if rs_path.exists():
        try:
            rs = json.loads(rs_path.read_text(encoding='utf-8'))
        except Exception:
            rs = {}
    else:
        rs = {}

    now = datetime.now(timezone.utc)
    rs['lastSyncAt'] = now.isoformat()
    rs['lastSyncMode'] = 'sync_after_review'
    rs['lastSyncFastCheck'] = fast_result

    # Phase 2: 合并 gate 状态（来自 go-live-gate.json）
    if gate_data:
        rs['gateSnapshot'] = {
            'generatedAt': gate_data.get('generatedAt'),
            'readinessStatus': gate_data.get('readinessStatus', {}),
            'gates': {
                k: {'all_passed': v.get('all_passed'), 'status': v.get('status')}
                for k, v in gate_data.get('gates', {}).items()
            },
        }

    # 总体 verdict
    if fast_result.get('exit_code', 1) == 0:
        rs['verdictAfterSync'] = 'usable'
        rs['verdictTextAfterSync'] = '本次同步后主链路一致，可正常用于浏览和周报承接'
    else:
        rs['verdictAfterSync'] = 'use_with_caution'
        rs['verdictTextAfterSync'] = '本次同步后仍存在不一致，请检查 ❌ 项'

    rs_path.write_text(json.dumps(rs, ensure_ascii=False, indent=2), encoding='utf-8')

    verdict_icon = '✅' if fast_result.get('exit_code', 1) == 0 else '⚠️'
    print(f'\n  {verdict_icon} 可用性判断: {rs["verdictTextAfterSync"]}')
    print(f'  📋 run-summary.json 已更新（lastSyncAt: {now.strftime("%H:%M:%S")}）')


def main() -> None:
    print('=' * 52)
    print('  sync_after_review — 决策后低摩擦半自动同步')
    print(f'  模式: {"DRY-RUN（演练）" if DRY_RUN else "CONFIRM 模式（正式执行）"}')
    print('=' * 52)

    if not CONFIRM and not DRY_RUN:
        print('\n  ⚠️  未指定 --confirm，将以演练模式运行。')
        print('  要正式执行，请加 --confirm：')
        print('    python3 scripts/sync_after_review.py --confirm')
        print('  要演练，请加 --dry-run：')
        print('    python3 scripts/sync_after_review.py --dry-run')
        print('  要查看详细计划，请加 --dry-run --verbose：')
        print('    python3 scripts/sync_after_review.py --dry-run --verbose')
        sys.exit(0)

    # 步骤 1-5：核心重建
    results = []
    for s in STEPS:
        ok = step(s['name'], s['script'], s['required'], DRY_RUN)
        results.append({'step': s['name'], 'ok': ok})
        if not ok and s['required']:
            print('\n  ❌ 同步在关键步骤失败。')
            print('  请修复后重新运行 sync_after_review.py。')
            sys.exit(1)

    if DRY_RUN:
        print('\n  [DRY-RUN] 以下步骤未实际执行。')
        print('\n  ✅ 演练完成，未写入任何文件。')
        print('  确认无误后，使用 --confirm 正式执行：')
        print('    python3 scripts/sync_after_review.py --confirm')
        sys.exit(0)

    # 步骤 6：fast-check
    fast_result = run_fast_check(dry_run=False)

    # 步骤 7：更新 run-summary（含 gate 快照）
    gate_data = None
    gate_path = REPORTS / 'go-live-gate.json'
    if gate_path.exists():
        try:
            gate_data = json.loads(gate_path.read_text(encoding='utf-8'))
        except Exception:
            pass
    update_run_summary(fast_result, gate_data)

    # 汇总
    print('\n' + '=' * 52)
    print('  同步完成汇总')
    print('=' * 52)
    for r in results:
        icon = '✅' if r['ok'] else '❌'
        print(f'  {icon} {r["step"]}')

    total = fast_result['PASS'] + fast_result['WARN'] + fast_result['FAIL']
    print(f'\n  fast-check  ✅{fast_result["PASS"]}  ⚠️{fast_result["WARN"]}  ❌{fast_result["FAIL"]}  ({total} 项)')

    pending_info = ''
    ti_path = REPORTS / 'tracking-items.json'
    if ti_path.exists():
        ti = json.loads(ti_path.read_text(encoding='utf-8'))
        summary = ti.get('trackingStatusSummary', {})
        pending = summary.get('待研判', 0)
        tracking = summary.get('跟踪中', 0)
        pending_info = f'待研判 {pending} 项，跟踪中 {tracking} 项'

    if fast_result['FAIL'] == 0:
        print(f'\n  ✅ 同步成功！当前状态：{pending_info}')
        print(f'  系统已就绪，可用于浏览和周报承接。')
        sys.exit(0)
    else:
        print(f'\n  ⚠️  同步完成但存在 {fast_result["FAIL"]} 个 ❌ 项。')
        print(f'  当前状态：{pending_info}')
        print(f'  请检查 ❌ 项后再用于正式汇报。')
        sys.exit(1)


if __name__ == '__main__':
    main()
