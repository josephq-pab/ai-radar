from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REVIEWS = BASE / 'reviews'
PROCESSED = BASE / 'data' / 'processed'

KEYWORDS = {
    '经营': '经营视角',
    '管理': '管理层口径',
    '口径': '管理层口径',
    '同业': '同业对比',
    '定价': '定价联动',
    '利率': '定价联动',
    '结构': '结构拆解',
    '产品': '产品结构',
    '行业': '行业映射',
    '节奏': '经营节奏',
    '竞争': '竞争格局',
    '建议': '行动建议',
    '行动': '行动建议',
    '策略': '策略推演',
}


def classify_text(*parts: str) -> list[str]:
    text = ' '.join([p for p in parts if p])
    tags = []
    for kw, tag in KEYWORDS.items():
        if kw in text:
            tags.append(tag)
    return sorted(set(tags))


def main() -> None:
    log_path = REVIEWS / 'review-log.jsonl'
    profile_path = PROCESSED / 'preference_profile.json'

    if not log_path.exists():
        profile = {
            'totalReviews': 0,
            'decisionCount': {},
            'themeCount': {},
            'topThemes': [],
            'guidance': [
                '默认先结论，后依据，再建议。',
                '强调经营视角、策略推演和行动建议。',
                '重要结论应尽量绑定同业、结构、定价中的至少一个维度。'
            ]
        }
        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding='utf-8')
        print(profile_path)
        return

    decision_counter = Counter()
    theme_counter = Counter()
    category_counter = Counter()
    examples = defaultdict(list)

    for line in log_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        decision = item.get('decision', 'unknown')
        decision_counter[decision] += 1
        category = item.get('category', '')
        if category:
            category_counter[category] += 1
        tags = classify_text(item.get('editedText', ''), item.get('reason', ''), item.get('originalText', ''))
        for tag in tags:
            theme_counter[tag] += 1
            if len(examples[tag]) < 3:
                examples[tag].append({
                    'itemId': item.get('itemId', ''),
                    'decision': decision,
                    'reason': item.get('reason', ''),
                    'editedText': item.get('editedText', ''),
                })

    top_themes = [name for name, _ in theme_counter.most_common(6)]

    guidance = []
    if '管理层口径' in top_themes:
        guidance.append('生成结论时优先采用管理层汇报口径，避免过于技术化或资料罗列。')
    if '经营视角' in top_themes:
        guidance.append('结论要落到经营影响、经营节奏和经营判断，不停留在信息描述。')
    if '同业对比' in top_themes:
        guidance.append('重要结论尽量补充与重点股份行的对比，不单独看平安自身指标。')
    if '结构拆解' in top_themes or '产品结构' in top_themes:
        guidance.append('涉及存贷款判断时，优先补充结构拆解和产品维度，而非只报总量。')
    if '定价联动' in top_themes:
        guidance.append('涉及贷款和利率时，应联动定价、产品、风险收益视角输出建议。')
    if '行动建议' in top_themes or '策略推演' in top_themes:
        guidance.append('每份报告都应从事实推演到策略，再落到行动建议。')

    if not guidance:
        guidance = [
            '默认先结论，后依据，再建议。',
            '重要结论应结合经营影响与行动建议。'
        ]

    profile = {
        'totalReviews': sum(decision_counter.values()),
        'decisionCount': dict(decision_counter),
        'categoryCount': dict(category_counter),
        'themeCount': dict(theme_counter),
        'topThemes': top_themes,
        'guidance': guidance,
        'examples': dict(examples),
    }
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding='utf-8')
    print(profile_path)


if __name__ == '__main__':
    main()
