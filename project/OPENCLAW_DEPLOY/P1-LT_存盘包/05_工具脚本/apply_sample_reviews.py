from __future__ import annotations

import json
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REVIEWS = BASE / 'reviews'
LOG = REVIEWS / 'review-log.jsonl'

SAMPLES = [
    {
        'reviewedAt': '2026-03-28T12:37:00',
        'itemId': 'core-1',
        'decision': 'modify',
        'originalText': '存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。',
        'editedText': '建议把存款差距拆解提升到经营视角，围绕竞争格局、经营节奏和重点产品结构来解释平安与重点同业之间的差距来源。',
        'reason': '原结论偏分析描述，不够像管理层汇报语言。',
        'category': '核心结论摘要',
        'source': 'weekly-report-draft.md'
    },
    {
        'reviewedAt': '2026-03-28T12:37:20',
        'itemId': 'pricing-1',
        'decision': 'modify',
        'originalText': '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。',
        'editedText': '建议将贷款产品结构、同业定价和风险收益并列呈现，形成更贴近经营决策的定价建议。',
        'reason': '需要更强调同业比较和经营决策用途。',
        'category': '策略建议',
        'source': 'weekly-report-draft.md'
    }
]


def main() -> None:
    REVIEWS.mkdir(parents=True, exist_ok=True)
    existing = set()
    if LOG.exists():
        for line in LOG.read_text(encoding='utf-8').splitlines():
            if line.strip():
                try:
                    existing.add((json.loads(line).get('itemId'), json.loads(line).get('decision')))
                except Exception:
                    pass
    with LOG.open('a', encoding='utf-8') as f:
        for sample in SAMPLES:
            key = (sample['itemId'], sample['decision'])
            if key in existing:
                continue
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    print(LOG)


if __name__ == '__main__':
    main()
