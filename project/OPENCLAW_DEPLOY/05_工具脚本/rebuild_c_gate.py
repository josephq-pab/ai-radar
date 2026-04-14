#!/usr/bin/env python3
"""
rebuild_c_gate.py — 重建 C gate（pending completion）阻断语义

业务规则（用户明确给出）：
- "批准后即可进入后续跟踪，不阻断本次汇报前准备"
- 已 approve 的事项：不算 C gate 阻断（即使 needReview=true / 有后续动作）
- 已 reject 的事项：不算阻断
- 只有尚未给出正式 decision（review-log 中为 empty/pending）的事项才算阻断

用法：
    python3 scripts/rebuild_c_gate.py            # 正式执行
    python3 scripts/rebuild_c_gate.py --dry-run  # 仅预览
    python3 scripts/rebuild_c_gate.py --report   # 仅输出报告
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REVIEW_LOG = BASE / 'reviews' / 'review-log.jsonl'
TRACKING = BASE / 'reports' / 'tracking-items.json'
GO_LIVE_GATE = BASE / 'reports' / 'go-live-gate.json'
REPORTS = BASE / 'reports'


def load_review_decisions():
    """从 review-log.jsonl 加载所有 itemId -> decision 映射"""
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
                    # 以最后一条记录为准
                    decisions[iid] = decision
            except Exception:
                pass
    return decisions


def load_tracking_items():
    """加载 tracking-items.json"""
    if not TRACKING.exists():
        return []
    d = json.loads(TRACKING.read_text(encoding='utf-8'))
    return d.get('items', [])


def classify_item(item, decisions):
    """
    按业务语义分类：
    - gate_blocker: 尚未完成决策，真正阻断 reportPrepReadiness
    - post_approval_followup: 已 approve/reject，仍需后续动作，但不阻断
    """
    iid = item.get('id', '')
    ts = item.get('trackingStatus', '')
    need_review = item.get('needReview', False)

    # 从 review-log 取决策
    decision = decisions.get(iid, '')

    # 尚未完成决策 → gate blocker
    if decision in ('', 'pending'):
        if ts == '待研判':
            return 'gate_blocker', 'waiting-for-review'
        elif ts in ('跟踪中', '已上报'):
            # 有 trackingStatus 但 review-log 无记录 = 静默 pending
            return 'gate_blocker', 'silent-pending'
        else:
            return 'gate_blocker', 'unresolved'

    # 已 approve → post-approval follow-up（不阻断）
    if decision == 'approve':
        return 'post_approval_followup', 'approved-follow-up'

    # 已 reject → 已关闭（不阻断）
    if decision == 'reject':
        return 'closed', 'rejected'

    # 其他（modify 等）→ follow-up
    return 'post_approval_followup', 'other-decision'


def rebuild_c_gate(dry_run=False):
    decisions = load_review_decisions()
    items = load_tracking_items()

    blockers = []
    followups = []
    closed = []

    for item in items:
        iid = item.get('id', '')
        classification, reason = classify_item(item, decisions)
        if classification == 'gate_blocker':
            blockers.append({
                'id': iid,
                'reason': reason,
                'trackingStatus': item.get('trackingStatus', ''),
                'text': item.get('text', '')[:60],
                'decision': decisions.get(iid, ''),
            })
        elif classification == 'post_approval_followup':
            followups.append({
                'id': iid,
                'reason': reason,
                'trackingStatus': item.get('trackingStatus', ''),
                'text': item.get('text', '')[:60],
                'decision': decisions.get(iid, ''),
                'nextAction': item.get('nextAction', ''),
            })
        else:
            closed.append({'id': iid, 'reason': reason})

    # 构建 C gate section
    c_gate = {
        'name': 'Pending 决策完成度',
        'readinessImpact': ['reportPrepReadiness'],
        'checks': [
            {
                'field': 'trueBlockerCount',
                'threshold': '0',
                'current': str(len(blockers)),
                'status': 'cleared' if len(blockers) == 0 else 'blocked',
                'blocking': len(blockers) > 0,
                'note': '仅统计尚未完成正式决策的事项；已 approve/reject 的后续动作不计入阻断'
            },
            {
                'field': 'postApprovalFollowupCount',
                'threshold': 'any',
                'current': str(len(followups)),
                'status': 'ok',
                'blocking': False,
                'note': '已批准但仍有后续动作，不阻断 reportPrepReadiness'
            },
        ],
        'gateBlockers': blockers,
        'postApprovalFollowups': followups,
        'closed': closed,
        'unblockCondition': 'trueBlockerCount == 0',
        'businessRule': '批准后即可进入后续跟踪，不阻断本次汇报前准备（用户确认，2026-04-01）',
    }

    # 更新 go-live-gate.json
    if GO_LIVE_GATE.exists():
        gate_data = json.loads(GO_LIVE_GATE.read_text(encoding='utf-8'))
    else:
        gate_data = {
            'version': 'go-live-gate-v1',
            'generatedAt': datetime.now(timezone.utc).isoformat(),
            'purpose': '明确 reportPrepReadiness 提升到 ready 的准入门槛',
            'gates': {},
            'readinessStatus': {},
            'goLiveCriteria': {},
        }

    gate_data['gates']['C_pendingCompletion'] = c_gate
    gate_data['generatedAt'] = datetime.now(timezone.utc).isoformat()

    report = {
        'c_gate': c_gate,
        'blocker_count': len(blockers),
        'followup_count': len(followups),
        'closed_count': len(closed),
        'blockers': blockers,
        'followups': followups,
    }

    if dry_run:
        print('[DRY-RUN] C gate rebuild preview:')
        print(f'  gateBlockers: {len(blockers)}')
        for b in blockers:
            print(f'    - {b["id"]} ({b["reason"]})')
        print(f'  postApprovalFollowups: {len(followups)}')
        for f in followups:
            print(f'    - {f["id"]} ({f["reason"]}) decision={f["decision"]}')
        print(f'  closed: {len(closed)}')
        print()
        print('Would write go-live-gate.json with:')
        print(json.dumps(c_gate, ensure_ascii=False, indent=2))
        return report

    # 正式写入
    GO_LIVE_GATE.write_text(json.dumps(gate_data, ensure_ascii=False, indent=2), encoding='utf-8')

    # 同时更新 run-summary.json 的 readinessLevels（只改 C gate 部分）
    run_summary_path = REPORTS / 'run-summary.json'
    if run_summary_path.exists():
        summary = json.loads(run_summary_path.read_text(encoding='utf-8'))
        rl = summary.get('readinessLevels', {})
        # 更新 reportPrepReadiness 的 gateType
        if blockers:
            existing = rl.get('reportPrepReadiness', {}).get('gateType', [])
            if 'C_pendingCompletion' not in existing:
                rl['reportPrepReadiness']['gateType'] = existing + ['C_pendingCompletion']
        else:
            existing = rl.get('reportPrepReadiness', {}).get('gateType', [])
            rl['reportPrepReadiness']['gateType'] = [g for g in existing if g != 'C_pendingCompletion']
        summary['readinessLevels'] = rl
        run_summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'C gate rebuilt:')
    print(f'  gateBlockers: {len(blockers)}')
    for b in blockers:
        print(f'    - {b["id"]} ({b["reason"]})')
    print(f'  postApprovalFollowups: {len(followups)}')
    for f in followups:
        print(f'    - {f["id"]} decision={f["decision"]}')
    print(f'  closed: {len(closed)}')
    print(f'  go-live-gate.json updated.')
    if blockers == []:
        print('  ✅ C gate cleared — no true blockers')
    return report


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    rebuild_c_gate(dry_run=dry)
