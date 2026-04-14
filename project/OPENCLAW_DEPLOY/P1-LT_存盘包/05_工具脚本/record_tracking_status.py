from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REPORTS = BASE / 'reports'
PROCESSED = BASE / 'data' / 'processed'
LOG = REPORTS / 'tracking-status-log.jsonl'

USAGE = '''\nUsage:\n  python3 scripts/record_tracking_status.py <itemId> <trackingStatus> [progress] [nextAction] [--dry-run | --sandbox-dir <path>]\n\nValid trackingStatus: 待研判 | 跟踪中 | 已上报 | 已行动 | 已关闭\n\nExamples:\n  # 正式写入 tracking-status-log.jsonl\n  python3 scripts/record_tracking_status.py core-1 已行动 "已完成管理层汇报并下发专项复盘" "下周跟踪专项动作反馈"\n\n  # 演练模式\n  python3 scripts/record_tracking_status.py core-1 跟踪中 "test" --dry-run\n\n  # 在指定临时目录演练\n  python3 scripts/record_tracking_status.py core-1 已上报 "test" --sandbox-dir /tmp/ai-radar-drill\n\nNote on sandbox:\n  --sandbox-dir 把输出写入指定临时目录，演练结束后由使用者决定是否清理，\n  正式数据完全不受影响。\n'''


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


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

    if len(real_argv) < 2:
        print(USAGE)
        sys.exit(1)

    item_id = real_argv[0]
    tracking_status = real_argv[1]
    progress = real_argv[2] if len(real_argv) > 2 else ''
    next_action = real_argv[3] if len(real_argv) > 3 else ''

    # 状态校验（正式模式才做，dry-run 不卡）
    if not dry_run:
        rules = load_json(PROCESSED / 'tracking_status_rules.json', {'trackingStatuses': []})
        allowed = set(rules.get('trackingStatuses', []))
        if allowed and tracking_status not in allowed:
            print(json.dumps({
                'error': 'invalid_tracking_status',
                'allowed': sorted(allowed),
                'received': tracking_status,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    # 解析 sandbox 路径
    if sandbox_dir:
        sandbox_log = sandbox_dir / 'reports' / 'tracking-status-log.jsonl'
        if not sandbox_dir.exists():
            sandbox_dir.mkdir(parents=True, exist_ok=True)
            (sandbox_dir / 'reports').mkdir(parents=True, exist_ok=True)
        act_log = sandbox_log
        mode = 'sandbox'
    else:
        act_log = LOG
        mode = 'live'

    if dry_run:
        print(f'  [DRY-RUN MODE]')
        print(f'  itemId={item_id}  trackingStatus={tracking_status}')
        print(f'  progress={progress[:60] if progress else "(none)"}...')
        print(f'  nextAction={next_action[:60] if next_action else "(none)"}')
        print(f'  Would write to: {act_log} (mode={mode})')
        sys.exit(0)

    REPORTS.mkdir(parents=True, exist_ok=True)
    record = {
        'updatedAt': datetime.now().isoformat(timespec='seconds'),
        'itemId': item_id,
        'trackingStatus': tracking_status,
        'latestProgress': progress,
        'nextAction': next_action,
    }
    with act_log.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
