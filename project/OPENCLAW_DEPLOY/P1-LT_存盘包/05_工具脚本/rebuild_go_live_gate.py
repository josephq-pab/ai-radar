#!/usr/bin/env python3
"""
rebuild_go_live_gate.py — 统一重建 go-live-gate（A/B/C 三类 gate）

Single Source of Truth 约定（Phase 2）：
  本脚本是 A/B/C gate、readinessLevels、gateType、blockers、goLiveCriteria
  的唯一生成入口。禁止在其他脚本中独立计算这些字段。

数据来源：
  A gate → data/processed/ 下各文件的 observedAt + freshness
  B gate → data/processed/analyst_opinions.json + reports/fetch-health.json
  C gate → reviews/review-log.jsonl + reports/tracking-items.json

用法：
    python3 scripts/rebuild_go_live_gate.py            # 正式执行
    python3 scripts/rebuild_go_live_gate.py --dry-run  # 仅预览
    python3 scripts/rebuild_go_live_gate.py --check    # 一致性检查（不写入）
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Phase 2: 统一路径解析 ──────────────────────────────────────
try:
    from paths import (
        BASE, REPORTS, DATA, PROCESSED,
        ANALYST_OPINIONS, REVIEW_LOG, TRACKING_ITEMS,
        RUN_SUMMARY, GO_LIVE_GATE,
    )
except ImportError:
    # 兼容：paths.py 尚未部署时使用相对路径回退
    BASE = Path(__file__).resolve().parent.parent
    REPORTS = BASE / 'reports'
    DATA = BASE / 'data'
    PROCESSED = DATA / 'processed'
    ANALYST_OPINIONS = PROCESSED / 'analyst_opinions.json'
    REVIEW_LOG = BASE / 'reviews' / 'review-log.jsonl'
    TRACKING_ITEMS = REPORTS / 'tracking-items.json'
    RUN_SUMMARY = REPORTS / 'run-summary.json'
    GO_LIVE_GATE = REPORTS / 'go-live-gate.json'

# B gate 正式清除门槛（Phase 2 语义）
#   usableCount      = VALID + DEGRADED（内容可读，非乱码非占位）
#   reportableCount  = 已进入周报（isReportable=True）
#   isReliableForReport = B gate 汇总判断，由 build_analyst_opinions.py 统一计算
B_GATE_THRESHOLDS = {
    'garbledCount_max': 0,
    'usableCount_min': 3,          # Phase 2: 看可用量，而非 referenceable
    'reportableCount_min': 1,      # Phase 2: 必须有已进周报的内容
    'isReliableForReport_req': True,
}

# A gate 阈值
A_THRESHOLD = '2026-03-01'
A_FILES = {
    'deposit': PROCESSED / 'deposit_benchmark.json',
    'loan': PROCESSED / 'loan_benchmark.json',
    'rate': PROCESSED / 'loan_rate.json',
}

C_BUSINESS_RULE = '批准后即可进入后续跟踪，不阻断本次汇报前准备（用户确认，2026-04-01）'


def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def assess_a_gate():
    checks = []
    all_passed = True
    for name, file_path in A_FILES.items():
        data = load_json(file_path)
        if data is None:
            observed = None
        elif isinstance(data, dict):
            observed = data.get('observedAt') or data.get('lastUpdated')
        elif isinstance(data, list):
            observed = data[0].get('observedAt') if data else None
        else:
            observed = None
        status = 'cleared' if (observed and observed >= A_THRESHOLD) else 'blocked'
        if status == 'blocked':
            all_passed = False
        checks.append({
            'field': name + '_observedAt',
            'threshold': A_THRESHOLD,
            'current': observed or 'N/A',
            'status': status,
            'blocking': status == 'blocked',
        })
    unblock_cmd = 'python3 scripts/import_monthly_data.py --confirm'
    return {
        'name': '数据新鲜度',
        'readinessImpact': ['internalDiscussionReadiness', 'reportPrepReadiness'],
        'checks': checks,
        'unblockCommand': unblock_cmd,
        'verificationCommand': 'python3 scripts/smoke_test.py --fast',
        'unblockCondition': 'deposit_observedAt >= 2026-03-01 AND loan_observedAt >= 2026-03-01 AND rate_observedAt >= 2026-03-01',
        'all_passed': all_passed,
    }, all_passed


def assess_b_gate():
    """B gate：Analyst 输入质量

    Phase 2 清除标准（与 build_analyst_opinions.py 保持同步）：
      garbledCount == 0  AND  usableCount >= 3  AND  reportableCount >= 1

    语义：
      usableCount     = VALID + DEGRADED（内容可读）
      reportableCount = 已进入周报（isReportable=True）
      isReliableForReport = 由 build_analyst_opinions.py 统一计算的综合判断

    不再使用 referenceableCount（Phase 1 遗留，与 DEGRADED 冲突）。
    """
    analyst_data = load_json(ANALYST_OPINIONS)

    if analyst_data and 'summary' in analyst_data:
        s = analyst_data['summary']
        tiers = s.get('qualityTiers', {})
        garbled = tiers.get('GARBLED', 0)
        valid = tiers.get('VALID', 0)
        degraded = tiers.get('DEGRADED', 0)
        placeholder = tiers.get('PLACEHOLDER', 0)
        # Phase 2: 使用拆分后的字段
        usable = s.get('usableCount', valid + degraded)
        referenceable = s.get('referenceableCount', valid)
        reportable = s.get('reportableCount', 0)
        is_reliable = s.get('isReliableForReport', False)
        b_gate_status = s.get('bGateStatus', 'blocked')
        verdict = s.get('verdict', 'N/A')
    elif analyst_data:
        records = analyst_data.get('records', [])
        garbled = sum(1 for r in records if r.get('qualityTier') == 'GARBLED')
        valid = sum(1 for r in records if r.get('qualityTier') == 'VALID')
        degraded = sum(1 for r in records if r.get('qualityTier') == 'DEGRADED')
        placeholder = sum(1 for r in records if r.get('qualityTier') == 'PLACEHOLDER')
        usable = valid + degraded
        referenceable = valid
        reportable = sum(1 for r in records if r.get('isReportable', False))
        is_reliable = garbled == 0 and usable >= 3 and reportable >= 1
        b_gate_status = 'cleared' if is_reliable else ('marginal' if garbled == 0 and usable >= 3 else 'blocked')
        verdict = 'N/A'
    else:
        garbled = valid = degraded = placeholder = usable = referenceable = reportable = 0
        is_reliable = False
        b_gate_status = 'blocked'
        verdict = 'no_data'

    garbled_ok = garbled <= B_GATE_THRESHOLDS['garbledCount_max']
    usable_ok = usable >= B_GATE_THRESHOLDS['usableCount_min']
    reportable_ok = reportable >= B_GATE_THRESHOLDS['reportableCount_min']
    reliable_ok = is_reliable

    # Phase 2 B gate 状态机
    if garbled == 0 and usable >= 3 and reportable >= 1:
        b_status = 'cleared'
    elif garbled == 0 and usable >= 3 and reportable == 0:
        b_status = 'marginal'   # 有可用内容但尚未进周报
    else:
        b_status = 'blocked'

    gaps = []
    if garbled > 0:
        gaps.append('garbledCount=%d（目标: 0）' % garbled)
    if usable < 3:
        gaps.append('usableCount=%d（目标: >=3）' % usable)
    if reportable < 1:
        gaps.append('reportableCount=%d（目标: >=1）' % reportable)
    if not is_reliable:
        gaps.append('isReliableForReport=false')

    checks = [
        {
            'field': 'garbledCount',
            'threshold': '0',
            'current': str(garbled),
            'status': 'cleared' if garbled_ok else 'blocked',
            'blocking': not garbled_ok,
        },
        {
            'field': 'usableCount',
            'threshold': '>=3',
            'current': str(usable),
            'status': 'cleared' if usable_ok else 'blocked',
            'blocking': not usable_ok,
            'note': 'usable = VALID + DEGRADED（内容可读，非乱码非占位）',
        },
        {
            'field': 'reportableCount',
            'threshold': '>=1',
            'current': str(reportable),
            'status': 'cleared' if reportable_ok else 'blocked',
            'blocking': not reportable_ok,
            'note': 'reportable = 已进入周报（isReportable=True）',
        },
        {
            'field': 'isReliableForReport',
            'threshold': 'True',
            'current': str(is_reliable),
            'status': 'cleared' if reliable_ok else 'blocked',
            'blocking': not reliable_ok,
        },
    ]

    unblock_cmd = 'python3 scripts/fetch_analyst_articles.py && python3 scripts/build_analyst_opinions.py'
    verify_cmd = 'python3 scripts/smoke_test.py --fast'
    return {
        'name': 'Analyst 输入质量',
        'readinessImpact': ['internalDiscussionReadiness', 'reportPrepReadiness'],
        'checks': checks,
        'gaps': gaps,
        'qualityTiers': {'GARBLED': garbled, 'VALID': valid, 'DEGRADED': degraded, 'PLACEHOLDER': placeholder},
        'usableCount': usable,
        'referenceableCount': referenceable,   # 保留，仅 VALID 级别
        'reportableCount': reportable,        # Phase 2 新增
        'verdict': verdict,
        'isReliableForReport': is_reliable,
        'bGateClearCriteria': 'garbledCount==0 AND usableCount>=3 AND reportableCount>=1',
        'unblockCommand': unblock_cmd,
        'verificationCommand': verify_cmd,
        'unblockCondition': 'garbledCount==0 AND usableCount>=3 AND reportableCount>=1',
        'clearCriteria': B_GATE_THRESHOLDS,
        'all_passed': b_status == 'cleared',
        'status': b_status,
    }, b_status != 'blocked'


def load_review_decisions():
    decisions = {}
    if REVIEW_LOG.exists():
        for line in REVIEW_LOG.read_text().strip().split('\n'):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                iid = entry.get('itemId', '')
                decision = entry.get('decision', '')
                if iid:
                    decisions[iid] = decision
            except Exception:
                pass
    return decisions


def assess_c_gate():
    """C gate：Pending 决策完成度

    业务规则（Phase 2 确认）：
      - 已 approve/modify：不算阻断（后续动作不计入）
      - 已 reject：不算阻断（已关闭）
      - 尚未给出正式 decision（empty/pending）：阻断

    Single Source of Truth：本函数是 C gate blockers 的唯一生成入口。
    """
    decisions = load_review_decisions()
    tracking_data = load_json(TRACKING_ITEMS)
    blockers = []
    followups = []
    closed = []

    if tracking_data and 'items' in tracking_data:
        for item in tracking_data['items']:
            iid = item.get('id', '')
            ts = item.get('trackingStatus', '')
            decision = decisions.get(iid, '')
            if decision in ('', 'pending'):
                blockers.append({'id': iid, 'reason': 'no-decision', 'trackingStatus': ts})
            elif decision in ('approve', 'modify'):
                followups.append({'id': iid, 'decision': decision, 'trackingStatus': ts})
            elif decision == 'reject':
                closed.append({'id': iid})

    checks = [
        {
            'field': 'trueBlockerCount',
            'threshold': '0',
            'current': str(len(blockers)),
            'status': 'cleared' if len(blockers) == 0 else 'blocked',
            'blocking': len(blockers) > 0,
            'note': '仅统计尚未完成正式决策的事项；已批准后续动作不计入阻断',
        },
        {
            'field': 'postApprovalFollowupCount',
            'threshold': 'any',
            'current': str(len(followups)),
            'status': 'ok',
            'blocking': False,
            'note': C_BUSINESS_RULE,
        },
    ]

    return {
        'name': 'Pending 决策完成度',
        'readinessImpact': ['reportPrepReadiness'],
        'checks': checks,
        'gateBlockers': blockers,
        'postApprovalFollowups': followups,
        'closed': closed,
        'unblockCondition': 'trueBlockerCount == 0',
        'businessRule': C_BUSINESS_RULE,
        'all_passed': len(blockers) == 0,
    }, len(blockers) == 0


def check_consistency(gate_data):
    warnings = []
    summary = load_json(RUN_SUMMARY)
    if not summary:
        warnings.append('run-summary.json 不存在，无法做一致性检查')
        return warnings

    rl = summary.get('readinessLevels', {})
    rp_gates = [g for g in rl.get('reportPrepReadiness', {}).get('gateType', [])]

    for gk in ['A_dataFreshness', 'B_analystQuality', 'C_pendingCompletion']:
        gv = gate_data['gates'].get(gk, {})
        is_blocked = not gv.get('all_passed', False)
        in_summary = gk in rp_gates
        if is_blocked and not in_summary:
            warnings.append('%s: go-live-gate=blocked，但 run-summary 未列入' % gk)
        elif not is_blocked and in_summary:
            warnings.append('%s: go-live-gate=cleared，但 run-summary 仍列入' % gk)

    return warnings


def sync_run_summary(gate_data):
    summary = load_json(RUN_SUMMARY)
    if not summary:
        return False
    rl = summary.get('readinessLevels', {})

    rp_gates = []
    for gk, gv in gate_data['gates'].items():
        if gk == 'C_pendingCompletion':
            # C gate: add only if there are true blockers
            blockers = gv.get('gateBlockers', [])
            if blockers:
                rp_gates.append(gk)
        else:
            # A/B gate: add if NOT all_passed (i.e., still blocked)
            if not gv.get('all_passed', False):
                rp_gates.append(gk)

    if 'reportPrepReadiness' in rl:
        rl['reportPrepReadiness']['gateType'] = rp_gates

    summary['readinessLevels'] = rl
    RUN_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    return True


def rebuild(dry_run=False, check_only=False):
    print('=' * 52)
    print('  rebuild_go_live_gate — 统一重建 go-live-gate')
    print('=' * 52)

    # A gate
    print('\n[1] A gate（数据新鲜度）...')
    a_gate, a_passed = assess_a_gate()
    a_icon = 'cleared' if a_passed else 'BLOCKED'
    print('    结果: %s' % a_icon)
    for c in a_gate['checks']:
        c_status = c['status']
        print('    [%s] %s: %s (阈值: %s)' % (c_status, c['field'], c['current'], c['threshold']))

    # B gate
    print('\n[2] B gate（Analyst 输入质量）...')
    b_gate, b_cleared = assess_b_gate()
    b_status = b_gate.get('status', 'blocked')
    print('    结果: %s' % b_status)
    for c in b_gate['checks']:
        print('    [%s] %s: %s (阈值: %s)' % (c['status'], c['field'], c['current'], c['threshold']))
    if b_gate.get('gaps'):
        for g in b_gate['gaps']:
            print('    差距: %s' % g)
    print('    清除标准: garbledCount=0 AND usableCount>=3 AND reportableCount>=1')
    print('    (Phase 2: usable=VALID+DEGRADED, reportable=已进入周报)')

    # C gate
    print('\n[3] C gate（Pending 决策完成度）...')
    c_gate, c_passed = assess_c_gate()
    c_icon = 'CLEARED' if c_passed else 'BLOCKED'
    print('    结果: %s' % c_icon)
    print('    gateBlockers: %d' % len(c_gate['gateBlockers']))
    print('    postApprovalFollowups: %d (不阻断reportPrep)' % len(c_gate['postApprovalFollowups']))
    print('    closed: %d' % len(c_gate['closed']))

    gate_data = {
        'version': 'go-live-gate-v1',
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'purpose': '明确 reportPrepReadiness 提升到 ready 的准入门槛',
        'gates': {
            'A_dataFreshness': a_gate,
            'B_analystQuality': b_gate,
            'C_pendingCompletion': c_gate,
        },
        'readinessStatus': {
            'browseReadiness': 'ready',
            'internalDiscussionReadiness': 'ready' if b_cleared else 'limited',
            'reportPrepReadiness': 'ready' if (a_passed and b_cleared and c_passed) else 'limited',
        },
        'goLiveCriteria': {
            'reportPrepReadiness_ready_required': {
                'A_dataFreshness': 'PASS' if a_passed else 'FAIL',
                'B_analystQuality': 'PASS' if b_cleared else 'FAIL',
                'C_pendingCompletion': 'PASS' if c_passed else 'FAIL_or_soft_block',
            }
        },
        'clearCriteria': {
            'A': 'deposit/loan/rate observedAt >= 2026-03-01',
            'B': 'garbledCount==0 AND usableCount>=3 AND reportableCount>=1 (Phase 2)',
            'C': 'trueBlockerCount==0 (不含已批准后续动作)',
        },
    }

    # 一致性检查
    print('\n[4] run-summary 一致性检查...')
    warnings = check_consistency(gate_data)
    if warnings:
        for w in warnings:
            print('    WARN: %s' % w)
    else:
        print('    OK: run-summary 与 go-live-gate 一致')

    if check_only:
        return gate_data

    if dry_run:
        print('\n[DRY-RUN] 跳过写入')
        return gate_data

    # 写入
    GO_LIVE_GATE.write_text(json.dumps(gate_data, ensure_ascii=False, indent=2), encoding='utf-8')
    gen_at = gate_data['generatedAt']
    print('\n    go-live-gate.json 已更新 (%s)' % gen_at)

    sync_ok = sync_run_summary(gate_data)
    if sync_ok:
        print('    run-summary.json gateType 已同步')
    else:
        print('    run-summary.json 同步失败')

    # 汇总
    print('\n' + '=' * 52)
    overall = []
    overall.append('A ' + ('PASS' if a_passed else 'FAIL'))
    overall.append('B ' + ('PASS' if b_cleared else ('MARGINAL' if b_gate.get('status') == 'marginal' else 'FAIL')))
    overall.append('C ' + ('PASS' if c_passed else 'FAIL'))
    print('  汇总: ' + ' / '.join(overall))
    print('=' * 52)

    return gate_data


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    check = '--check' in sys.argv
    rebuild(dry_run=dry, check_only=check)
