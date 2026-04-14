from __future__ import annotations

import json
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REPORTS = BASE / 'reports'
PROCESSED = BASE / 'data' / 'processed'

LAYER_TO_RULE_KEY = {
    '观察提示': 'observation',
    '策略建议': 'strategy',
    '直接行动建议': 'action',
    '待人工确认事项': 'strategy',
}

# 语义动作 → 目标 layer 的显式映射（优先级高于 infer_layer）
SEMANTIC_ACTION_TO_LAYER = {
    'promote_to_strategy': '策略建议',
    'promote_to_action': '直接行动建议',
    'keep_observation': '观察提示',
}

# 语义动作 → 是否改变 layer（promote 动作才改变）
SEMANTIC_ACTION_CHANGES_LAYER = {
    'promote_to_strategy': True,
    'promote_to_action': True,
    'keep_observation': False,
    'continue_pending': False,
}

REVIEW_STATUS_TO_TRACKING_STATUS = {
    'pending': '待研判',
    'modify': '跟踪中',
    'approve': '已上报',
    'reject': '已关闭',
}


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def infer_layer(category: str = '', text: str = '') -> str:
    joined = f'{category} {text}'
    if '观察提示' in joined:
        return '观察提示'
    if '直接行动建议' in joined:
        return '直接行动建议'
    if '策略建议' in joined:
        return '策略建议'
    if '待人工确认事项' in joined:
        return '待人工确认事项'
    if '策略' in category:
        return '策略建议'
    return '待人工确认事项'


def infer_source_dimension(category: str = '', text: str = '') -> str:
    joined = f'{category} {text}'
    if '存款' in joined:
        return '存款'
    if '贷款' in joined or '定价' in joined:
        return '贷款'
    return '整体对公业务'


def infer_source_theme(category: str = '', text: str = '') -> str:
    joined = f'{category} {text}'
    if '定价' in joined or '利率' in joined:
        return '对标分析/定价观察'
    if '同业' in joined or '差距' in joined:
        return '同业动态/对标分析'
    if '策略' in joined:
        return '建议动作'
    return '核心结论/待确认事项'


def next_action_by_status(status: str, layer: str, dimension: str) -> str:
    if status == 'pending':
        return f'优先确认{dimension}相关口径、证据和经营含义是否充分，再决定是否升级为{layer}。'
    if status == 'modify':
        return '按修改意见回写周报、案例页和 tracking 事项说明，确保前后台口径一致。'
    if status == 'approve':
        return '可进入正式周报、案例页或专题输出，并继续跟踪是否需要升级为具体动作。'
    if status == 'reject':
        return '补充证据、重写结论，必要时降级为观察提示继续跟踪。'
    return '待补充下一步动作。'


def source_meta_by_dimension(dimension: str) -> tuple[str, str]:
    if dimension == '存款':
        return '存款深案例', './deposit.html'
    if dimension == '贷款':
        return '贷款深案例', './loan.html'
    return '首页总览', './index.html'


def latest_progress_text(status: str, text: str, reason: str) -> str:
    if status == 'modify' and reason:
        return f'已收到修改意见：{reason}'
    if status == 'approve':
        return '已通过当前轮确认，可纳入正式输出。'
    if status == 'reject':
        return '当前结论已驳回，等待补充证据或改写。'
    return f'待进一步研判：{text[:40]}'


def build_items():
    queue = load_json(REPORTS / 'review-queue.json', {'items': []})
    status = load_json(REPORTS / 'review-status.json', {'items': []})
    recommendation = load_json(PROCESSED / 'recommendation_rules.json', {'rules': {}})
    tracking_status_rules = load_json(PROCESSED / 'tracking_status_rules.json', {'reviewToTracking': {}})

    tracking_log_path = REPORTS / 'tracking-status-log.jsonl'
    tracking_latest = {}
    if tracking_log_path.exists():
        for line in tracking_log_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            tracking_latest[row['itemId']] = row

    status_map = {item['id']: item for item in status.get('items', [])}
    rules = recommendation.get('rules', {})
    review_to_tracking = tracking_status_rules.get('reviewToTracking', {})

    items = []
    for item in queue.get('items', []):
        status_item = status_map.get(item['id'], {})
        item_status = status_item.get('status', 'pending')
        text = status_item.get('editedText') or status_item.get('text') or item.get('text', '')
        raw_text = item.get('text', '')
        category = status_item.get('category') or item.get('category', '未分类')
        reason = status_item.get('reason', '')
        reviewed_at = status_item.get('reviewedAt', '')

        # 语义动作：优先用 semanticAction 决定 layer（promote 动作覆盖原 category）
        semantic_action = status_item.get('semanticAction') or item.get('semanticAction')
        if semantic_action and SEMANTIC_ACTION_CHANGES_LAYER.get(semantic_action, False):
            layer = SEMANTIC_ACTION_TO_LAYER.get(semantic_action, infer_layer(category, text))
        else:
            layer = infer_layer(category, text)
        dimension = infer_source_dimension(category, text)
        theme = infer_source_theme(category, text)
        source_name, source_href = source_meta_by_dimension(dimension)
        rule_key = LAYER_TO_RULE_KEY.get(layer, 'strategy')
        priority = rules.get(rule_key, {}).get('defaultPriority', 'medium')
        need_review = rules.get(rule_key, {}).get('needReview', True)
        tracking_state = tracking_latest.get(item['id'], {})
        tracking_status = tracking_state.get('trackingStatus') or review_to_tracking.get(item_status, '待研判')
        latest_progress = tracking_state.get('latestProgress') or latest_progress_text(item_status, text, reason)
        next_action = tracking_state.get('nextAction') or next_action_by_status(item_status, layer, dimension)
        updated_at = tracking_state.get('updatedAt') or reviewed_at

        items.append({
            'id': item['id'],
            'name': f'{category}-{item["id"]}',
            'category': category,
            'status': item_status,
            'trackingStatus': tracking_status,
            'sourceDimension': dimension,
            'sourceTheme': theme,
            'text': text,
            'rawText': raw_text,
            'latestProgress': latest_progress,
            'reason': reason,
            'reviewedAt': reviewed_at,
            'updatedAt': updated_at,
            'sourceName': source_name,
            'sourceHref': source_href,
            'sourceFile': item.get('source', ''),
            'layer': layer,
            'priority': priority,
            'needReview': need_review,
            'nextAction': next_action,
        })

    payload = {
        'total': len(items),
        'pending': len([x for x in items if x['status'] == 'pending']),
        'approved': len([x for x in items if x['status'] == 'approve']),
        'modified': len([x for x in items if x['status'] == 'modify']),
        'rejected': len([x for x in items if x['status'] == 'reject']),
        'trackingStatusSummary': {
            '待研判': len([x for x in items if x['trackingStatus'] == '待研判']),
            '跟踪中': len([x for x in items if x['trackingStatus'] == '跟踪中']),
            '已上报': len([x for x in items if x['trackingStatus'] == '已上报']),
            '已行动': len([x for x in items if x['trackingStatus'] == '已行动']),
            '已关闭': len([x for x in items if x['trackingStatus'] == '已关闭']),
        },
        'items': items,
    }
    return payload


def main() -> None:
    out = REPORTS / 'tracking-items.json'
    payload = build_items()
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
