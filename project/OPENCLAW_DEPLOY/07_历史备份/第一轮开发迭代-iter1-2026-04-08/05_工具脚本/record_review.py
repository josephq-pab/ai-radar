from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REVIEWS = BASE / 'reviews'
QUEUE = BASE / 'reports' / 'review-queue.json'
LOG = REVIEWS / 'review-log.jsonl'

USAGE = '''\nUsage:\n  python3 scripts/record_review.py <itemId> <decision> [editedText] [reason] [--dry-run | --sandbox-dir <path>]\n\nDecision values: pending | modify | approve | reject\n\nExamples:\n  # 正式写入 review-log.jsonl\n  python3 scripts/record_review.py core-1 modify "把结论改得更偏经营口径" "原表述不够管理层化"\n\n  # 演练模式（不写正式文件，显示结果后退出）\n  python3 scripts/record_review.py core-1 approve "内容OK" --dry-run\n\n  # 在指定临时目录演练\n  python3 scripts/record_review.py core-1 modify "test" --sandbox-dir /tmp/ai-radar-drill\n\nSemantic action values (optional, for formal promotion semantics):\n  promote_to_strategy  - 升级为策略建议\n  promote_to_action     - 升级为直接行动建议\n  keep_observation      - 保持观察提示\n  continue_pending      - 继续pending\n  (leave empty for null/None)\n\nNote on sandbox:\n  --sandbox-dir 把所有输出写入指定临时目录（queue/log 均指向那里），\n  演练结束后该目录由使用者决定是否清理，正式数据完全不受影响。\n'''


def main() -> None:
    # 解析 sandbox/dry-run 参数
    sandbox_dir = None
    dry_run = False
    argv = sys.argv[1:]
    real_argv = []
    i = 0
    while i < len(argv):
        if argv[i] == '--dry-run':
            dry_run = True
        elif argv[i] == '--sandbox-dir':
            if i + 1 >= len(argv):
                print('Error: --sandbox-dir requires an argument')
                sys.exit(1)
            sandbox_dir = Path(argv[i + 1])
            i += 2
            continue
        else:
            real_argv.append(argv[i])
        i += 1

    # 解析 semantic-action
    semantic_action = None
    new_real_argv = []
    i = 0
    while i < len(real_argv):
        if real_argv[i] == '--semantic-action':
            if i + 1 >= len(real_argv):
                print('Error: --semantic-action requires an argument')
                sys.exit(1)
            semantic_action = real_argv[i + 1]
            i += 2
            continue
        new_real_argv.append(real_argv[i])
        i += 1
    real_argv = new_real_argv

    if len(real_argv) < 2:
        print(USAGE)
        sys.exit(1)

    item_id = real_argv[0]
    decision = real_argv[1]
    edited_text = real_argv[2] if len(real_argv) > 2 else ''
    reason = real_argv[3] if len(real_argv) > 3 else ''

    # 解析 sandbox 路径
    if sandbox_dir:
        sandbox_queue = sandbox_dir / 'reports' / 'review-queue.json'
        sandbox_log = sandbox_dir / 'reviews' / 'review-log.jsonl'
        if not sandbox_dir.exists():
            sandbox_dir.mkdir(parents=True, exist_ok=True)
            (sandbox_dir / 'reports').mkdir(parents=True, exist_ok=True)
            (sandbox_dir / 'reviews').mkdir(parents=True, exist_ok=True)
            # 复制 queue 文件到 sandbox
            shutil.copy2(QUEUE, sandbox_queue)
        act_queue = sandbox_queue
        act_log = sandbox_log
        mode = 'sandbox'
    else:
        act_queue = QUEUE
        act_log = LOG
        mode = 'live'

    if dry_run:
        print(f'  [DRY-RUN MODE]')
        print(f'  itemId={item_id}  decision={decision}')
        print(f'  editedText={edited_text[:60] if edited_text else "(none)"}...')
        print(f'  reason={reason[:60] if reason else "(none)"}')
        print(f'  queue={act_queue}')
        print(f'  log={act_log}')
        print(f'  Would write to: {act_log} (mode={mode})')
        sys.exit(0)

    REVIEWS.mkdir(parents=True, exist_ok=True)

    queue = {'items': []}
    if act_queue.exists():
        queue = json.loads(act_queue.read_text(encoding='utf-8'))

    matched = None
    for item in queue.get('items', []):
        if item.get('id') == item_id:
            matched = item
            break

    record = {
        'reviewedAt': datetime.now().isoformat(timespec='seconds'),
        'itemId': item_id,
        'decision': decision,
        'semanticAction': semantic_action,
        'originalText': matched.get('text', '') if matched else '',
        'editedText': edited_text,
        'reason': reason,
        'category': matched.get('category', '') if matched else '',
        'source': matched.get('source', '') if matched else '',
    }

    with act_log.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
