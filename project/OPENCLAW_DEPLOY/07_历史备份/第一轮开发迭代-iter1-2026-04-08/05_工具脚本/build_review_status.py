from __future__ import annotations

import json
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REVIEWS = BASE / 'reviews'
REPORTS = BASE / 'reports'


def main() -> None:
    log_path = REVIEWS / 'review-log.jsonl'
    latest = {}
    if log_path.exists():
        for line in log_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            latest[item['itemId']] = item

    queue = {'items': []}
    queue_path = REPORTS / 'review-queue.json'
    if queue_path.exists():
        queue = json.loads(queue_path.read_text(encoding='utf-8'))

    items = []
    for item in queue.get('items', []):
        review = latest.get(item['id'])
        status = review['decision'] if review else 'pending'
        items.append({
            'id': item['id'],
            'category': item.get('category', ''),
            'text': item.get('text', ''),
            'status': status,
            'semanticAction': review.get('semanticAction', '') if review else '',
            'editedText': review.get('editedText', '') if review else '',
            'reason': review.get('reason', '') if review else '',
            'reviewedAt': review.get('reviewedAt', '') if review else '',
        })

    out = {
        'total': len(items),
        'pending': len([x for x in items if x['status'] == 'pending']),
        'approved': len([x for x in items if x['status'] == 'approve']),
        'modified': len([x for x in items if x['status'] == 'modify']),
        'rejected': len([x for x in items if x['status'] == 'reject']),
        'items': items,
    }
    (REPORTS / 'review-status.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(REPORTS / 'review-status.json')


if __name__ == '__main__':
    main()
