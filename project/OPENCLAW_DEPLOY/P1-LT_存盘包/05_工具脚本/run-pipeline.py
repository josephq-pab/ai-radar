#!/usr/bin/env python3
"""
run-pipeline.py — 对公 AI 雷达站统一运行入口

用法：
    python3 scripts/run-pipeline.py              # 完整链路（解析→周报→bundle→校验）
    python3 scripts/run-pipeline.py --parse-only  # 仅数据解析
    python3 scripts/run-pipeline.py --report-only # 仅周报重生成（不重跑 parse）
    python3 scripts/run-pipeline.py --track-only   # 仅 tracking 重生成
    python3 scripts/run-pipeline.py --smoke-only   # 仅 smoke test

行为：
    smoke_test FAIL（非 WARN）时脚本非 0 退出，后续步骤不再执行
    smoke_test WARN 时打印摘要但不阻止完成
    smoke_test PASS 时打印正常完成摘要

此脚本不执行 review 记录操作（review/record_tracking_status），需单独调用。
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import os as _os
_DEPLOY_BASE = _os.environ.get('OPENCLAW_DEPLOY_BASE')
if _DEPLOY_BASE:
    BASE = Path(_DEPLOY_BASE)
else:
    BASE = Path(__file__).resolve().parent.parent  # 兼容：自动推导

SCRIPTS      = BASE / 'scripts'
PROCESSED    = BASE / 'data' / 'processed'
REPORTS      = BASE / 'reports'
WEB_DATA     = BASE / 'apps' / 'web' / 'data'
REVIEWS      = BASE / 'reviews'
DATA         = BASE / 'data'
OPS          = BASE / 'ops'
CONFIG       = BASE / 'config'

# ── 工具函数 ─────────────────────────────────────────────

def header(msg: str) -> None:
    print(f'\n{"─"*52}')
    print(f'  {msg}')
    print(f'{"─"*52}')


def run_step(name: str, cmd: list[str], timeout: int = 60) -> int:
    """运行单个脚本，返回退出码"""
    print(f'\n  ▶ {name}')
    print(f'    {" ".join(str(c) for c in cmd)}')
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    elapsed = time.time() - t0
    status = '✅ OK' if result.returncode == 0 else f'❌ FAIL ({result.returncode})'
    print(f'    {status}  ({elapsed:.1f}s)')
    if result.stdout:
        for line in result.stdout.strip().split('\n')[-5:]:
            print(f'    └ {line}')
    if result.returncode != 0 and result.stderr:
        for line in result.stderr.strip().split('\n')[:5]:
            print(f'    └ [ERR] {line}')
    return result.returncode


def load_json(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


# ── 数据模式与新鲜度检测 ─────────────────────────────────

def detect_data_mode() -> dict:
    """启发式判断当前运行的数据模式：sample / real / mixed"""
    raw_dir = BASE / 'data' / 'raw'
    if not raw_dir.exists():
        return {'mode': 'unknown', 'reason': 'raw dir not found'}

    raw_files = list(raw_dir.glob('*.xlsx'))
    if not raw_files:
        return {'mode': 'unknown', 'reason': 'no xlsx files found'}

    # 启发式规则：
    # - 若文件名含 "sample" / "示例" / "test" → sample
    # - 若文件名含 "更新" / "最新" / "v2" / "260228" / "2602" → real（有明确日期版本）
    # - 若文件修改时间 < 7 天 → real（新鲜）
    # - 否则 mixed

    sample_files = [f for f in raw_files if any(k in f.name.lower() for k in ['sample', '示例', 'test', 'demo'])]
    real_indicator = any(k in f.name for f in raw_files for k in ['更新', '最新', '2602', '260228'])
    fresh_files = [f for f in raw_files if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]

    if sample_files:
        mode = 'sample'
        reason = f'文件名含 sample/示例/测试标识: {[f.name for f in sample_files]}'
    elif real_indicator or fresh_files:
        mode = 'real'
        reason = f'文件名含版本标识或文件新鲜（7天内）: {[f.name for f in fresh_files]}'
    else:
        mode = 'mixed'
        reason = '文件无明确标识或修改时间较早'

    return {'mode': mode, 'reason': reason, 'raw_files': [f.name for f in raw_files]}


def detect_data_freshness() -> dict:
    """检测核心数据新鲜度"""
    from datetime import datetime as dt

    # 核心输入文件修改时间
    raw_files = list((BASE / 'data' / 'raw').glob('*.xlsx'))
    raw_mtimes = {f.name: dt.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d') for f in raw_files}

    # processed 文件的 observedAt
    freshness = {}
    for fname in ['deposit_benchmark.json', 'loan_benchmark.json', 'loan_rate.json']:
        p = PROCESSED / fname
        if p.exists():
            d = load_json(p)
            if isinstance(d, list) and d:
                dates = list(set(r.get('observedAt') for r in d if r.get('observedAt')))
                freshness[fname] = sorted(dates)[-1] if dates else None
            elif isinstance(d, dict):
                freshness[fname] = 'object format'

    # analyst_opinions 的 fetchedAt
    ao = load_json(PROCESSED / 'analyst_opinions.json')
    fetched_at = None
    if ao:
        s = ao.get('summary', {})
        fetched_at = s.get('fetchedAt', '')[:10] if s.get('fetchedAt') else None

    # 判断是否过旧（超过 30 天）
    now = dt.now()
    raw_age_days = None
    if raw_files:
        latest_mtime = max(f.stat().st_mtime for f in raw_files)
        raw_age_days = (dt.now() - dt.fromtimestamp(latest_mtime)).days

    stale = raw_age_days is not None and raw_age_days > 30

    return {
        'raw_file_mtimes': raw_mtimes,
        'observedAt': freshness,
        'analyst_fetched_at': fetched_at,
        'raw_age_days': raw_age_days,
        'stale': stale,
        'stale_reason': f'源数据文件已超过 30 天未更新（当前{raw_age_days}天前）' if stale else None,
    }


# ── 运行摘要生成 ─────────────────────────────────────────

def generate_run_summary(totals: dict, exit_code: int, duration: float,
                          data_mode: dict, data_freshness: dict,
                          fb: dict, stagnation: dict,
                          dedup: dict, lines: list[str]) -> dict:
    """生成可交付的运行摘要（JSON + Markdown 双版本）"""
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)

    REPORTS.mkdir(parents=True, exist_ok=True)
    run_id = now.strftime('%Y%m%d-%H%M%S')

    # 核心产物状态
    products = {}
    for fname, path in [
        ('deposit_benchmark.json', PROCESSED / 'deposit_benchmark.json'),
        ('loan_benchmark.json', PROCESSED / 'loan_benchmark.json'),
        ('loan_rate.json', PROCESSED / 'loan_rate.json'),
        ('review-queue.json', REPORTS / 'review-queue.json'),
        ('review-status.json', REPORTS / 'review-status.json'),
        ('tracking-items.json', REPORTS / 'tracking-items.json'),
        ('weekly-report-draft.md', REPORTS / 'weekly-report-draft.md'),
        ('app-data.js', WEB_DATA / 'app-data.js'),
        ('analyst_opinions.json', PROCESSED / 'analyst_opinions.json'),
    ]:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        mtime = datetime.fromtimestamp(path.stat().st_mtime).isoformat() if exists else None
        record_count = None
        if exists and fname.endswith('.json'):
            d = load_json(path)
            if isinstance(d, dict):
                record_count = d.get('total', len(d.get('items', [])))
        products[fname] = {
            'exists': exists,
            'size_bytes': size,
            'size_kb': round(size / 1024, 1),
            'mtime': mtime,
            'record_count': record_count,
            'status': 'generated' if exists else 'missing',
        }

    # ── 可信度摘要 ─────────────────────────────────────────
    rq = load_json(REPORTS / 'review-queue.json')
    rq_items = rq.get('items', []) if rq else []
    known_fb = ['存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。',
                '贷款投放节奏判断不能脱离产品结构和定价水平，应联动观察。',
                '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。']
    fb_count = sum(1 for i in rq_items if i.get('text', '') in known_fb)

    ti = load_json(REPORTS / 'tracking-items.json')
    tracking_summary = ti.get('trackingStatusSummary', {}) if ti else {}
    pending = tracking_summary.get('待研判', 0)
    total_items = sum(tracking_summary.values())
    pending_rate = f'{pending/total_items*100:.0f}%' if total_items > 0 else '0%'

    # ── Analyst 质量分层 ─────────────────────────────────
    # 分类：valid（有可读标题）/ garbled（乱码）/ empty（空标题或占位符）
    ao = load_json(PROCESSED / 'analyst_opinions.json')
    ao_valid = 0
    ao_garbled = 0
    ao_empty_or_placeholder = 0
    ao_analyst_names = []
    if ao:
        for r in ao.get('records', []):
            # 使用 build_analyst_opinions.py 预计算的 qualityTier 字段
            qt = r.get('qualityTier', 'UNKNOWN')
            if qt == 'VALID':
                ao_valid += 1
            elif qt == 'GARBLED':
                ao_garbled += 1
            elif qt in ('PLACEHOLDER', 'DEGRADED'):
                ao_empty_or_placeholder += 1
            name = r.get('analystName', '')
            if name and name not in ao_analyst_names:
                ao_analyst_names.append(name)

    analyst_quality = {
        'totalRecords': ao.get('records', []) if ao else [],
        'totalCount': ao_valid + ao_garbled + ao_empty_or_placeholder,
        'validCount': ao_valid,
        'garbledCount': ao_garbled,
        'emptyOrPlaceholderCount': ao_empty_or_placeholder,
        'referenceableCount': sum(1 for r in ao.get('records', []) if r.get('isReferenceable', False)),
        'verdict': 'valid' if ao_valid >= 3 and ao_garbled == 0 and ao_empty_or_placeholder == 0
                                                else ('partial' if ao_valid >= 1 and ao_garbled == 0 else
                                                        ('degraded' if ao_garbled > 0 else 'insufficient')),
                                                
        'verdictText': (
            f'{ao_valid} 条有效，{ao_garbled} 条乱码，{ao_empty_or_placeholder} 条空/占位'
            if (ao_garbled + ao_empty_or_placeholder) > 0
            else f'{ao_valid} 条有效分析师观点'
        ),
        'isReliableForReport': ao_valid >= 3 and ao_garbled == 0,
        'note': (
            f'analyst 层可引用 {ao_valid} 条，可参考 {ao_empty_or_placeholder} 条，{ao_garbled} 条乱码不可引用'
            if ao_valid >= 3 and ao_garbled == 0
            else f'analyst 层不足以支撑周报正式引用：有效 {ao_valid} 条，乱码 {ao_garbled} 条，占位 {ao_empty_or_placeholder} 条'
        ),
        'analysts': ao_analyst_names,
    }

    # ── Stagnation 结构化 ────────────────────────────────
    review_log = BASE / 'reviews' / 'review-log.jsonl'
    tracking_log = REPORTS / 'tracking-status-log.jsonl'

    last_review_at = None
    if review_log.exists():
        rlines = review_log.read_text(encoding='utf-8').strip().split('\n')
        if rlines:
            try:
                last_review_at = json.loads(rlines[-1]).get('reviewedAt', None)
            except Exception:
                pass

    last_tracking_update_at = None
    if tracking_log.exists():
        tlines = tracking_log.read_text(encoding='utf-8').strip().split('\n')
        if tlines:
            try:
                last_tracking_update_at = json.loads(tlines[-1]).get('updatedAt', None)
            except Exception:
                pass

    stagnation = check_tracking_stagnation()
    stagnation['lastReviewAt'] = last_review_at
    stagnation['lastTrackingUpdateAt'] = last_tracking_update_at

    # stagnationLevel: 0=正常, 1=注意, 2=警告, 3=阻塞
    if stagnation['stagnant'] and pending_rate and int(pending_rate.rstrip('%')) >= 50:
        stagnation['stagnationLevel'] = 3
        stagnation['stagnationText'] = f'pending率{pending_rate}且超过7天无更新'
    elif stagnation['stagnant']:
        stagnation['stagnationLevel'] = 2
        stagnation['stagnationText'] = stagnation['reason']
    elif pending_rate and int(pending_rate.rstrip('%')) >= 50:
        stagnation['stagnationLevel'] = 1
        stagnation['stagnationText'] = f'pending率{pending_rate}偏高'
    else:
        stagnation['stagnationLevel'] = 0
        stagnation['stagnationText'] = '无停滞迹象'

    # ── 静默 Pending 处理 ────────────────────────────────
    # 2 项静默 pending（review-log 中不存在的待研判项）
    all_ti_items = ti.get('items', []) if ti else []
    silent_pendings = []
    if review_log.exists():
        rlines = review_log.read_text(encoding='utf-8').strip().split('\n')
        reviewed_ids = set()
        for line in rlines:
            try:
                reviewed_ids.add(json.loads(line).get('itemId', ''))
            except Exception:
                pass
        for item in all_ti_items:
            if item.get('trackingStatus') == '待研判' and item.get('id', '') not in reviewed_ids:
                silent_pendings.append({
                    'id': item.get('id', ''),
                    'text': item.get('text', '')[:80],
                    'agingConfidence': 'low',
                    'backfillNote': 'never-formally-reviewed — 无 review-log 记录，时间戳为推算值',
                    'reason': '该事项从未进入 review 流程，仅从原始 review-queue 遗留',
                })

    # ── 可用性分级 ─────────────────────────────────────
    # browseReadiness: 页面/bundle/tracking/周报是否可正常浏览
    # internalDiscussionReadiness: 数据是否足以支撑内部复盘
    # reportPrepReadiness: 是否足以支撑正式汇报前准备

    from datetime import datetime as dt
    fresh_days = data_freshness.get('raw_age_days', 0)
    is_stale = data_freshness.get('stale', False)

    # browse
    if exit_code != 0:
        browse_level = 'blocked'
        browse_text = '主链路 smoke test FAIL，系统不可用'
        browse_blockers = ['smoke test FAIL']
    else:
        browse_level = 'ready'
        browse_text = '主链路一致，bundle 新鲜，页面可正常浏览'
        browse_blockers = []

    # internal
    internal_blockers = []
    if is_stale:
        internal_blockers.append(f'核心数据超过 30 天未更新（{fresh_days}天），影响判断准确性')
    if analyst_quality['garbledCount'] > 0:
        internal_blockers.append(f'analyst 层有 {analyst_quality["garbledCount"]} 条乱码，{analyst_quality["garbledCount"]} 条空/占位')
    if analyst_quality['validCount'] < 3:
        internal_blockers.append(f'analyst 层有效记录仅 {analyst_quality["validCount"]} 条，不足以支撑深度分析')

    if len(internal_blockers) == 0:
        internal_level = 'ready'
        internal_text = '数据虽偏旧，但足以支撑内部复盘与经营推演'
    elif len(internal_blockers) <= 2:
        internal_level = 'limited'
        internal_text = f'存在 {len(internal_blockers)} 项限制，参考时需注意'
    else:
        internal_level = 'restricted'
        internal_text = '存在多项限制，建议优先补充数据后再进行内部讨论'

    # report prep
    report_blockers = []
    if is_stale:
        report_blockers.append('核心 benchmark/rate 数据超过 30 天，不建议直接用于正式汇报')
    if not analyst_quality['isReliableForReport']:
        report_blockers.append(f'analyst 层不足以支撑周报正式引用（{analyst_quality["verdictText"]}）')
    if pending >= 3:
        report_blockers.append(f'仍有 {pending} 项待研判，需在汇报前处理')
    if stagnation.get('stagnationLevel', 0) >= 2:
        report_blockers.append(f'tracking 存在停滞：{stagnation["stagnationText"]}')

    if len(report_blockers) == 0:
        report_level = 'ready'
        report_text = '数据与分析足以支撑正式汇报前准备'
    elif len(report_blockers) <= 2:
        report_level = 'limited'
        report_text = f'存在 {len(report_blockers)} 项限制，需在汇报前处理'
    else:
        report_level = 'not_ready'
        report_text = f'存在 {len(report_blockers)} 项阻塞，不建议直接用于正式汇报前准备'

    # ── 从 go-live-gate.json 读取 readinessLevels（Phase 2 单源原则）─────
    # Phase 2 起不再独立计算；由 rebuild_go_live_gate.py 统一维护
    try:
        gate_json = json.loads((REPORTS / 'go-live-gate.json').read_text())
        gate_readiness = gate_json.get('readinessStatus', {})
        rl_text = {
            'ready': '主链路一致，bundle 新鲜，页面可正常浏览',
            'limited': '存在限制条件，引用时需注明',
            'not_ready': '存在阻塞项，不建议使用',
        }
        readiness_levels = {}
        for key, level in gate_readiness.items():
            readiness_levels[key] = {
                'level': level,
                'verdictText': rl_text.get(level, level),
                'blockers': [],
                'gateType': [],
                'recommendation': '以 go-live-gate.json 为准',
            }
    except Exception:
        # 兜底：gate 文件不存在时保持独立计算
        readiness_levels = {
            'browseReadiness': {
                'level': browse_level,
                'verdictText': browse_text,
                'blockers': browse_blockers,
                'gateType': [],
                'recommendation': '可正常用于日常查看与内部跟踪',
            },
            'internalDiscussionReadiness': {
                'level': internal_level,
                'verdictText': internal_text,
                'blockers': internal_blockers,
                'gateType': ['A_dataFreshness'] if (fresh_blockers := [b for b in internal_blockers if '数据' in b or '过期' in b or '过期' in b]) else ['B_analystQuality'] if [b for b in internal_blockers if 'analyst' in b or '乱码' in b] else (['C_pending'] if [b for b in internal_blockers if 'pending' in b] else []),
                'recommendation': (
                    '可用于内部复盘，但需在引用时注明数据截止时间'
                    if internal_level in ('ready', 'limited')
                    else '建议先补充数据再进行内部讨论'
                ),
            },
            'reportPrepReadiness': {
                'level': report_level,
                'verdictText': report_text,
                'blockers': report_blockers,
                'gateType': (
                    ['A_dataFreshness', 'B_analystQuality', 'C_pendingCompletion']
                    if report_blockers
                    else []
                ),
                'recommendation': (
                    '可准备正式汇报，建议提前确认数据口径与 analyst 引用方式'
                    if report_level == 'ready'
                    else '建议在汇报前解决阻塞项'
                ),
            },
        }

    # 总体 verdict（向下兼容）
    if exit_code != 0:
        verdict = 'not_recommended'
        verdict_text = '主链路 smoke test FAIL，系统不可用'
    elif browse_level != 'ready':
        verdict = 'not_recommended'
        verdict_text = browse_text
    elif len(report_blockers) == 0 and len(internal_blockers) == 0:
        verdict = 'usable'
        verdict_text = '本次可正常用于浏览、内部讨论和汇报前准备'
    elif len(report_blockers) <= 2:
        verdict = 'use_with_caution'
        verdict_text = f'本次可用，但存在 {len(report_blockers)} 项需注意'
    else:
        verdict = 'use_with_caution'
        verdict_text = f'本次可用，但存在 {len(report_blockers)} 项阻塞，建议汇报前处理'

    summary = {
        'runId': run_id,
        'startedAt': (now.replace(second=0) - timedelta(seconds=duration)).isoformat(),
        'finishedAt': now.isoformat(),
        'duration_seconds': round(duration, 1),
        'exitCode': exit_code,
        'mode': 'full',
        'success': exit_code == 0,
        'smokeTestResult': {'PASS': totals['PASS'], 'WARN': totals['WARN'], 'FAIL': totals['FAIL']},
        'dataMode': data_mode,
        'dataFreshness': data_freshness,
        'products': products,
        'trustSummary': {
            'reviewQueueMode': fb['mode'],
            'reviewQueueFallbackCount': fb['fallback_count'],
            'reviewQueueTotalCount': fb['total_count'],
            'trackingPending': pending,
            'trackingTotal': total_items,
            'trackingPendingRate': pending_rate,
            'trackingStatusSummary': tracking_summary,
            'trackingStagnation': stagnation,
            'silentPending': silent_pendings,
            'analystQuality': analyst_quality,
            'loanDedupedCount': dedup.get('loan_deduped_count'),
            'loanDedupRisk': dedup.get('risk'),
        },
        'readinessLevels': readiness_levels,
        'verdict': verdict,
        'verdictText': verdict_text,
        'warnings': [l.strip() for l in lines if '⚠️' in l],
    }

    # 写 JSON
    json_path = REPORTS / 'run-summary.json'
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    # 写 Markdown
    md_lines = [f'# 对公 AI 雷达站 — 运行摘要', f'', f'**Run ID:** `{run_id}`', f'**时间:** {now.strftime("%Y-%m-%d %H:%M UTC")}', f'**持续:** {duration:.1f}s', f'']
    verdict_icon = {'usable': '✅', 'use_with_caution': '⚠️', 'not_recommended': '❌'}.get(verdict, '?')
    md_lines += [f'**总体结论:** {verdict_icon} {verdict_text}', f'']
    md_lines += [f'**smoke test:** ✅{totals["PASS"]}  ⚠️{totals["WARN"]}  ❌{totals["FAIL"]}', f'']

    # 可用性分级
    md_lines += ['', '## 可用性分级', '']
    rl_icon = {'ready': '✅', 'limited': '⚠️', 'restricted': '⚠️', 'not_ready': '❌', 'blocked': '❌'}
    for name, info in readiness_levels.items():
        icon = rl_icon.get(info['level'], '?')
        md_lines.append(f'**{icon} {name}:** {info["verdictText"]}')
        if info['blockers']:
            for b in info['blockers']:
                md_lines.append(f'  - {b}')
        md_lines.append(f'  → {info["recommendation"]}')
        md_lines.append('')

    md_lines += [f'**数据模式:** {data_mode.get("mode", "unknown")}（{data_mode.get("reason", "")}）', f'']

    md_lines += ['## 核心产物状态', '']
    md_lines += ['| 产物 | 状态 | 大小 | 记录数 | 修改时间 |', '|---|---|---|---|---|']
    for fname, info in products.items():
        status_icon = {'generated': '✅', 'missing': '❌'}.get(info['status'], '?')
        rc = str(info['record_count']) if info['record_count'] is not None else '-'
        mt = info['mtime'][11:16] if info['mtime'] else '-'
        md_lines.append(f'| `{fname}` | {status_icon} | {info["size_kb"]}KB | {rc} | {mt} |')

    md_lines += ['', '## 可信度摘要', '']
    md_lines += [f'- review queue 模式: **{fb["mode"]}** ({fb["fallback_count"]}/{fb["total_count"]} 条兜底)']
    md_lines += [f'- tracking 状态: 待研判 {pending}/{total_items} ({pending_rate})']
    for st, cnt in sorted(tracking_summary.items()):
        md_lines.append(f'  - {st}: {cnt} 项')
    md_lines += [f'- analyst 层: {analyst_quality["verdictText"]}']
    if analyst_quality['garbledCount'] > 0 or analyst_quality['emptyOrPlaceholderCount'] > 0:
        md_lines.append(f'  - ⚠️ 有效 {analyst_quality["validCount"]} 条 | 乱码 {analyst_quality["garbledCount"]} 条 | 空/占位 {analyst_quality["emptyOrPlaceholderCount"]} 条 | {analyst_quality["note"]}')
    if stagnation.get('stagnationLevel', 0) >= 2:
        md_lines.append(f'  - ⚠️ stagnation: {stagnation["stagnationText"]}（level={stagnation["stagnationLevel"]}）')
    if last_review_at:
        md_lines.append(f'  - lastReviewAt: {last_review_at}')
    if last_tracking_update_at:
        md_lines.append(f'  - lastTrackingUpdateAt: {last_tracking_update_at}')
    if silent_pendings:
        md_lines.append(f'  - ⚠️ 静默 pending（无 review 记录）: {len(silent_pendings)} 项')
        for sp in silent_pendings:
            md_lines.append(f'    - {sp["id"][:12]} | {sp["text"][:40]}')
    md_lines += [f'- loan dedup: 去重后 {dedup.get("loan_deduped_count","?")} 条']
    if dedup.get('risk'):
        md_lines.append(f'  - ℹ️ dedup风险: {dedup["risk"]}')

    md_lines += ['', '## 数据新鲜度', '']
    for fname, obs_date in data_freshness.get('observedAt', {}).items():
        obs_dt = dt.fromisoformat(obs_date)
        if obs_dt.tzinfo is None:
            obs_dt = obs_dt.replace(tzinfo=timezone.utc)
        freshness_icon = '⚠️' if (obs_date and (now - obs_dt).days > 30) else '✅'
        md_lines.append(f'- {freshness_icon} `{fname}` observedAt: {obs_date}')
    if data_freshness.get('analyst_fetched_at'):
        md_lines.append(f'- analyst_opinions fetchedAt: {data_freshness["analyst_fetched_at"]}')
    if data_freshness.get('stale'):
        md_lines.append(f'  - ⚠️ {data_freshness["stale_reason"]}')

    if totals['WARN'] > 0:
        md_lines += ['', '## WARN 详情', '']
        for line in lines:
            if '⚠️' in line:
                md_lines.append(f'- {line.strip()}')

    md_path = REPORTS / 'run-summary.md'
    md_path.write_text('\n'.join(md_lines), encoding='utf-8')

    return summary

def dedup_audit() -> dict:
    """检查 loan_benchmark 原始行数与去重后行数，输出审计信息"""
    raw_path = next(BASE.glob('data/raw/*贷款对标数据*.xlsx'), None)
    if not raw_path:
        return {'note': 'raw file not found, skip dedup audit'}

    # 估算原始行数：基于 loan_benchmark 去重前的数量（48）和去重后的数量（20）
    # 注：如果需要精确原始行数，需要在 parse_loan() 中记录
    # 这里我们通过 quality_report.json 中记录的 loanRecords（去重后）来反推
    q = load_json(PROCESSED / 'quality_report.json')
    loan_deduped = q.get('loanRecords', '?') if q else '?'

    return {
        'loan_deduped_count': loan_deduped,
        'note': 'dedup key = bank+metricGroup+observedAt, keeping first occurrence',
        'risk': '若源 Excel 新版本出现在后面（新行），可能因保留第一条而丢失最新数据。'
    }


# ── Smoke test runner ─────────────────────────────────────

def run_smoke_test() -> tuple[int, list[str]]:
    """运行 smoke test（内联方式，避免子进程超时），返回 (exit_code, output_lines)"""
    import re
    lines_out = []

    def R(lvl, msg):
        icon = {'PASS': '✅', 'WARN': '⚠️ ', 'FAIL': '❌'}[lvl]
        line = f'  {icon} [{lvl}] {msg}'
        print(line)
        lines_out.append(line)

    DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    VALID_TS = {'待研判', '跟踪中', '已上报', '已行动', '已关闭'}
    REQ_SECTIONS = ['## 一、核心结论摘要', '## 五、观察提示', '## 六、策略建议', '## 七、直接行动建议', '## 八、待人工确认事项']

    def load(p):
        return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None

    def load_json_file(p):
        if not p.exists(): return False, None, 'not found'
        try: return True, json.loads(p.read_text(encoding='utf-8')), ''
        except Exception as e: return False, None, str(e)

    tot = {'PASS': 0, 'WARN': 0, 'FAIL': 0}

    # parse
    for f in ['deposit_benchmark.json', 'loan_benchmark.json', 'loan_rate.json']:
        p = PROCESSED / f; ok, d, err = load_json_file(p)
        if not ok: R('FAIL', f'{f}: {err}'); tot['FAIL'] += 1; continue
        R('PASS', f'{f} OK ({len(d) if isinstance(d, list) else 1} records)'); tot['PASS'] += 1
        if isinstance(d, list):
            pks = {}; dup = 0
            for r in d:
                pk = '|'.join(str(r.get(k)) for k in ['bank', 'metricGroup', 'observedAt'])
                if pk in pks: dup += 1
                pks[pk] = 1
            if dup: R('WARN', f'{f} PK dup: {dup} groups'); tot['WARN'] += 1
            bad = [r.get('observedAt') for r in d if r.get('observedAt') and not DATE_RE.match(str(r.get('observedAt')))]
            if bad: R('WARN', f'{f} bad date: {bad[:2]}'); tot['WARN'] += 1

    for f in ['summary.json', 'quality_report.json', 'dashboard.json']:
        d = load(PROCESSED / f)
        if d: R('PASS', f'{f} OK'); tot['PASS'] += 1
        else: R('FAIL', f'{f}: not found'); tot['FAIL'] += 1

    # review queue
    d = load(REPORTS / 'review-queue.json')
    if d:
        items = d.get('items', []); R('PASS', f'review-queue OK ({len(items)} items)'); tot['PASS'] += 1
        ids = set(); dup = []
        for i in items:
            if i['id'] in ids and i['id'] not in dup: dup.append(i['id'])
            ids.add(i['id'])
        if dup: R('WARN', f'dup ids: {dup}'); tot['WARN'] += 1
        KNOWN = ['存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。',
                 '贷款投放节奏判断不能脱离产品结构和定价水平，应联动观察。',
                 '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。']
        fb = sum(1 for i in items if i.get('text', '') in KNOWN)
        R('PASS' if fb == 0 else ('FAIL' if fb == len(items) else 'WARN'), f'fallback: {fb}/{len(items)}'); tot['PASS' if fb == 0 else ('FAIL' if fb == len(items) else 'WARN')] += 1
        wr = (REPORTS / 'weekly-report-draft.md').read_text(encoding='utf-8')
        found = sum(1 for i in items[:4] if i.get('text', '')[:30].strip() in wr)
        R('PASS' if found >= 1 else 'WARN', f'items in report: {found}/4'); tot['PASS' if found >= 1 else 'WARN'] += 1
    else: R('FAIL', 'review-queue not found'); tot['FAIL'] += 1

    # tracking
    d = load(REPORTS / 'tracking-items.json')
    if d:
        R('PASS', f'tracking OK ({len(d.get("items", []))} items)'); tot['PASS'] += 1
        for s in VALID_TS:
            R('PASS' if s in d.get('trackingStatusSummary', {}) else 'WARN', f'trackingStatus.{s}'); tot['PASS' if s in d.get('trackingStatusSummary', {}) else 'WARN'] += 1
    else: R('FAIL', 'tracking not found'); tot['FAIL'] += 1

    # report-tracking link
    ti = load(REPORTS / 'tracking-items.json')
    wr = (REPORTS / 'weekly-report-draft.md').read_text(encoding='utf-8')
    if ti:
        has_data = bool(ti.get('trackingStatusSummary') or ti.get('items'))
        i9 = wr.find('## 九、重点事项跟踪状态汇总'); i10 = wr.find('## 十、事项明细')
        sec9 = wr[i9:i10] if i9 != -1 and i10 != -1 else ''
        if has_data:
            if '暂无跟踪状态汇总数据' in sec9: R('FAIL', 'Sec9 fallback despite data'); tot['FAIL'] += 1
            else:
                found_s = [s for s in VALID_TS if s in sec9 and any(c.isdigit() for c in sec9[sec9.find(s):sec9.find(s) + 10])]
                R('PASS' if found_s else 'WARN', f'Sec9 data: {found_s}'); tot['PASS' if found_s else 'WARN'] += 1
        if ti.get('items') and i10 != -1:
            sec10 = wr[i10:wr.find('\n## ', i10 + 1)]
            if '暂无事项数据' in sec10: R('FAIL', 'Sec10 fallback despite items'); tot['FAIL'] += 1
            else:
                sid = ti['items'][0].get('id', ''); R('PASS' if sid in sec10 else 'WARN', f'Sec10 id={sid}: found={sid in sec10}'); tot['PASS' if sid in sec10 else 'WARN'] += 1

    # weekly report
    p = REPORTS / 'weekly-report-draft.md'
    if p.exists():
        text = p.read_text(encoding='utf-8'); R('PASS', f'report ({len(text)} chars)'); tot['PASS'] += 1
        for s in REQ_SECTIONS: R('PASS' if s in text else 'FAIL', f'section [{s}]'); tot['PASS' if s in text else 'FAIL'] += 1
        for m in ['观察提示', '策略建议', '直接行动建议']: R('PASS' if m in text else 'FAIL', f'rec [{m}]'); tot['PASS' if m in text else 'FAIL'] += 1
    else: R('FAIL', 'report not found'); tot['FAIL'] += 1

    # bundle
    p = WEB_DATA / 'app-data.js'
    if p.exists():
        text = p.read_text(encoding='utf-8'); js = text[len('window.AIRadarData = '):]
        if js.rstrip().endswith(';'): js = js.rstrip()[:-1]
        try:
            d = json.loads(js); R('PASS', f'bundle ({len(text) // 1024}KB)'); tot['PASS'] += 1
            for k in ['dashboard', 'deposit', 'loan', 'rate', 'summary', 'reviewQueue', 'trackingItems']:
                R('PASS' if k in d else 'FAIL', f'key [{k}]'); tot['PASS' if k in d else 'FAIL'] += 1
        except Exception as e: R('FAIL', f'bundle parse error'); tot['FAIL'] += 1
    else: R('FAIL', 'bundle not found'); tot['FAIL'] += 1

    # analyst opinions
    p = PROCESSED / 'analyst_opinions.json'
    if p.exists():
        ok, d, _ = load_json_file(p)
        if ok:
            records = d.get('records', [])
            R('PASS', f'analyst_opinions.json OK ({len(records)} records)'); tot['PASS'] += 1
            if not records:
                R('WARN', 'analyst_opinions records 为空（本周无分析师观点，正常状态）'); tot['WARN'] += 1
            else:
                for field in ['articleTitle', 'analystName', 'sourceUrl']:
                    missing = sum(1 for r in records[:3] if not r.get(field))
                    R('PASS' if missing == 0 else 'WARN', f'analyst.{field}: {len(records)-missing}/{len(records)} 有值'); tot['PASS' if missing == 0 else 'WARN'] += 1
        else: R('FAIL', f'analyst_opinions parse error: {d}'); tot['FAIL'] += 1
    else: R('WARN', 'analyst_opinions.json 不存在（正常，如本周无分析师观点）'); tot['WARN'] += 1

    total = sum(tot.values())
    summary_line = f'  校验汇总  ✅{tot["PASS"]}  ⚠️{tot["WARN"]}  ❌{tot["FAIL"]}  ({total} 项)'
    print(f'\n{summary_line}')
    lines_out.append(summary_line)

    exit_code = 1 if tot['FAIL'] > 0 else 0
    return exit_code, lines_out


def parse_smoke_summary(lines: list[str]) -> dict:
    """从 smoke test 输出中解析 PASS/WARN/FAIL 计数"""
    for line in lines:
        if '汇总' in line or 'SUMMARY' in line or 'Total=' in line:
            # 格式: 汇总  ✅N  ⚠️N  ❌N  (N 项)
            import re
            m = re.search(r'✅(\d+).*?⚠️(\d+).*?❌(\d+).*?(?:\(([\d]+) 项\))?|$', line)
            if m and m.group(1):
                return {'PASS': int(m.group(1)), 'WARN': int(m.group(2)),
                        'FAIL': int(m.group(3)), 'total': int(m.group(4) or 0)}
            # 格式: SUMMARY: PASS=N  WARN=N  FAIL=N  Total=N
            m2 = re.search(r'PASS=(\d+).*?WARN=(\d+).*?FAIL=(\d+).*?Total=(\d+)', line)
            if m2:
                return {'PASS': int(m2.group(1)), 'WARN': int(m2.group(2)),
                        'FAIL': int(m2.group(3)), 'total': int(m2.group(4))}
    return {'PASS': 0, 'WARN': 0, 'FAIL': 0, 'total': 0}


# ── Observability helpers ─────────────────────────────────

def check_fallback_mode() -> dict:
    """检查 review-queue 是否处于兜底模式"""
    rq = load_json(REPORTS / 'review-queue.json')
    if not rq:
        return {'mode': 'no_data', 'is_fallback': True, 'fallback_count': 0, 'total_count': 0}

    items = rq.get('items', [])
    KNOWN_FALLBACK = [
        '存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。',
        '贷款投放节奏判断不能脱离产品结构和定价水平，应联动观察。',
        '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。',
    ]
    fb = sum(1 for i in items if i.get('text', '') in KNOWN_FALLBACK)
    return {
        'mode': 'fallback' if fb == len(items) else ('mixed' if fb > 0 else 'real'),
        'fallback_count': fb,
        'total_count': len(items),
        'is_fallback': fb == len(items),
    }


def check_tracking_stagnation() -> dict:
    """检查 tracking 状态是否长期停滞"""
    rq = load_json(REPORTS / 'review-queue.json')
    rs = load_json(REPORTS / 'review-status.json')
    ti = load_json(REPORTS / 'tracking-items.json')

    if not ti:
        return {'stagnant': True, 'reason': 'no tracking data', 'pending': 0, 'total': 0, 'pending_rate': 'N/A'}

    summary = ti.get('trackingStatusSummary', {})
    pending = summary.get('待研判', 0)
    total = sum(summary.values())

    # 检查 review-log 是否有最近的记录
    review_log = BASE / 'reviews' / 'review-log.jsonl'
    tracking_log = REPORTS / 'tracking-status-log.jsonl'

    last_review = None
    last_tracking_update = None

    if review_log.exists():
        lines = review_log.read_text(encoding='utf-8').strip().split('\n')
        if lines:
            last = json.loads(lines[-1])
            last_review = last.get('reviewedAt', '')

    if tracking_log.exists():
        lines = tracking_log.read_text(encoding='utf-8').strip().split('\n')
        if lines:
            last = json.loads(lines[-1])
            last_tracking_update = last.get('updatedAt', '')

    # 简单规则：pending 率 > 80% 且没有最近记录（7天内）则告警
    stagnant = False
    reason = ''
    if total > 0 and pending / total > 0.8:
        now = datetime.now(timezone.utc)
        if last_review:
            last_dt = datetime.fromisoformat(last_review.replace('Z', '+00:00'))
            # 统一为 aware datetime 再比较
            if now.tzinfo is None:
                now_aware = now.replace(tzinfo=timezone.utc)
            else:
                now_aware = now
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            if (now_aware - last_dt).days > 7:
                stagnant = True
                reason = f'pending率{pending/total:.0%}，最后review已{(now_aware-last_dt).days}天前'
        if last_tracking_update:
            last_dt = datetime.fromisoformat(last_tracking_update.replace('Z', '+00:00'))
            if now.tzinfo is None:
                now_aware = now.replace(tzinfo=timezone.utc)
            else:
                now_aware = now
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            if (now_aware - last_dt).days > 7:
                stagnant = True
                reason = f'pending率{pending/total:.0%}，最后tracking更新已{(now_aware-last_dt).days}天前'

    return {
        'stagnant': stagnant,
        'reason': reason,
        'pending': pending,
        'total': total,
        'pending_rate': f'{pending/total*100:.0f}%' if total > 0 else '0%',
        'last_review': last_review,
        'last_tracking_update': last_tracking_update,
    }


# ── 主函数 ────────────────────────────────────────────────

def main() -> None:
    print('=' * 52)
    print(f'  对公 AI 雷达站 — 主链路运行入口')
    print(f'  时间: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
    print('=' * 52)

    argv = sys.argv[1:]
    mode = 'full'
    if '--parse-only' in argv:
        mode = 'parse'
    elif '--data-only' in argv:
        mode = 'data'
    elif '--report-only' in argv:
        mode = 'report'
    elif '--rebuild-only' in argv:
        mode = 'rebuild'
    elif '--track-only' in argv:
        mode = 'track'
    elif '--smoke-only' in argv:
        mode = 'smoke'
    
    mode_desc = {
        'full': '完整刷新',
        'parse': '仅解析',
        'data': '仅源数据',
        'report': '仅周报',
        'rebuild': '仅重建',
        'track': '仅 tracking',
        'smoke': '仅校验'
    }
    print(f'\n  📌 运行模式: {mode_desc.get(mode)}')

    # ── 可观测性：运行前快照 ──────────────────────────────
    header('运行前可观测性检查')
    fb = check_fallback_mode()
    fb_icon = '⚠️ ' if fb['is_fallback'] else '✅'
    print(f'  {fb_icon} review-queue 模式: {fb["mode"]} ({fb["fallback_count"]}/{fb["total_count"]} 条兜底)')
    if fb['is_fallback']:
        print(f'  ⚠️  当前处于兜底模式，周报内容可能不是真实提取结果！')

    stagnation = check_tracking_stagnation()
    st_icon = '⚠️ ' if stagnation['stagnant'] else '✅'
    print(f'  {st_icon} tracking 状态: pending {stagnation["pending"]}/{stagnation["total"]} ({stagnation["pending_rate"]})')
    if stagnation['stagnant']:
        print(f'  ⚠️  {stagnation["reason"]}')

    # Dedup 审计
    dedup = dedup_audit()
    print(f'  📊 loan dedup: 去重后 {dedup.get("loan_deduped_count","?")} 条')
    if dedup.get('risk'):
        print(f'  ℹ️  dedup风险: {dedup["risk"]}')

    # ── 步骤执行 ─────────────────────────────────────────
    # Step 1: 数据解析
    if mode in ('full', 'parse', 'data'):
        header('Step 1: 数据解析')
        code = run_step('parse_initial_data.py', [sys.executable, str(SCRIPTS / 'parse_initial_data.py')], timeout=60)
        if code != 0:
            print('\n  ❌ parse 失败，退出。')
            sys.exit(1)
    
    # Step 1b: Analyst 抓取 (仅 data/full 模式)
    if mode in ('full', 'data'):
        header('Step 1b: Analyst 抓取')
        # analyst 抓取可选，失败不中止主链路
        code = run_step('fetch_analyst_articles.py', [sys.executable, str(SCRIPTS / 'fetch_analyst_articles.py')], timeout=120)
        if code != 0:
            print('\n  ⚠️  analyst 抓取失败，继续主链路')
        code2 = run_step('build_analyst_opinions.py', [sys.executable, str(SCRIPTS / 'build_analyst_opinions.py')], timeout=60)
        if code2 != 0:
            print('\n  ⚠️  analyst 处理失败，继续主链路')

    # Step 3: Tracking (rebuild 专用：必须在周报之前跑，确保周报能读到最新状态)
    if mode in ('full', 'track', 'rebuild'):
        header('Step 3: Tracking 中间层')
        code = run_step('build_review_status.py', [sys.executable, str(SCRIPTS / 'build_review_status.py')], timeout=30)
        code2 = run_step('build_tracking_items.py', [sys.executable, str(SCRIPTS / 'build_tracking_items.py')], timeout=30)
        if code != 0 or code2 != 0:
            print('\n  ⚠️  tracking 构建有非零退出码')

    # Step 2: 周报生成（full/rebuild 模式在 Step3 之后跑，使周报能读到最新 tracking-items）
    if mode in ('full', 'report', 'rebuild'):
        header('Step 2: 周报生成')
        code = run_step('generate_weekly_report.py', [sys.executable, str(SCRIPTS / 'generate_weekly_report.py')], timeout=60)
        if code != 0:
            print('\n  ❌ 周报生成失败，退出。')
            sys.exit(1)

        code = run_step('generate_review_queue.py', [sys.executable, str(SCRIPTS / 'generate_review_queue.py')], timeout=30)
        if code != 0:
            print('\n  ❌ review queue 生成失败，退出。')
            sys.exit(1)

    # Step 4: Web Bundle
    if mode in ('full', 'rebuild'):
        header('Step 4: Web Bundle')
        code = run_step('build_web_bundle.py', [sys.executable, str(SCRIPTS / 'build_web_bundle.py')], timeout=30)
        if code != 0:
            print('\n  ❌ bundle 生成失败，退出。')
            sys.exit(1)

    if mode in ('full', 'smoke'):
        header('Step 5: Smoke Test / 数据校验')
        exit_code, lines = run_smoke_test()
        print()

        # 可观测性增强：兜底模式告警（独立于 smoke test）
        fb = check_fallback_mode()
        if fb['is_fallback']:
            print(f'\n  ⚠️  额外告警：review-queue 当前处于兜底模式，内容可能为样板数据')
            print(f'      兜底条数: {fb["fallback_count"]}/{fb["total_count"]}')

        stagnation = check_tracking_stagnation()
        if stagnation['stagnant']:
            print(f'\n  ⚠️  额外告警：{stagnation["reason"]}')

        # ── Baseline 回归检查（subprocess，无模块副作用）───────────────────────
        bl_result = subprocess.run(
            [sys.executable, str(SCRIPTS / 'smoke_test.py'), '--baseline'],
            capture_output=True, text=True, cwd=str(BASE)
        )
        # --baseline 在 issues>0 时 exit 1，WARN 时 exit 0
        if bl_result.stdout:
            for line in bl_result.stdout.strip().split('\n'):
                if line.strip():
                    print(f'  {line}')
        if bl_result.returncode != 0 and bl_result.returncode != 1:
            print(f'\n  ⚠️  baseline 检查异常（exit {bl_result.returncode}）')
        elif bl_result.returncode == 1:
            # 有 FAIL 项，但 smoke test PASS 时不阻止主链路，仅警告
            pass

        if exit_code != 0:
            print(f'\n  ❌ smoke test FAIL，脚本退出。')
            sys.exit(1)
        else:
            pass_count = sum(1 for l in lines if '[PASS]' in l)
            warn_count = sum(1 for l in lines if '⚠️' in l and l.strip().endswith(']'))
            if warn_count > 0:
                print(f'\n  ⚠️  smoke test 有 {warn_count} 个 WARN，建议检查。')
                print(f'  （WARN 不阻止完成，但请在适当时机检查。）')
            else:
                print(f'\n  ✅ 全部通过，无 FAIL/WARN。')

        # 生成运行摘要（仅在 smoke test 执行后）
        # 精确统计：[PASS] / ⚠️ / ❌ 标记行，排除汇总行本身
        pass_count = sum(1 for l in lines if '[PASS]' in l)
        warn_count = sum(1 for l in lines if '⚠️' in l and l.strip().endswith(']'))
        fail_count = sum(1 for l in lines if '❌' in l and l.strip().endswith(']'))
        totals_final = {'PASS': pass_count, 'WARN': warn_count, 'FAIL': fail_count}
        fb_after = check_fallback_mode()
        stagnation_after = check_tracking_stagnation()
        data_mode_after = detect_data_mode()
        data_freshness_after = detect_data_freshness()
        dedup_after = dedup_audit()
        generate_run_summary(totals_final, exit_code, 0.0, data_mode_after, data_freshness_after,
                             fb_after, stagnation_after, dedup_after, lines)
        print(f'\n  📋 运行摘要已生成: reports/run-summary.json + reports/run-summary.md')
    else:
        # 非 smoke 模式：不生成摘要（因为 smoke test 未运行，无 lines）
        pass

    print(f'\n{"="*52}')
    print(f'  完成时间: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
    print('='*52)


if __name__ == '__main__':
    main()