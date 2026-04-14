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

DEFAULT_SECTIONS = ['核心结论摘要', '同业动态观察', '贷款与产品观察', '定价观察', '策略建议', '待人工确认事项']


def classify_text(*parts: str) -> list[str]:
    text = ' '.join([p for p in parts if p])
    tags = []
    for kw, tag in KEYWORDS.items():
        if kw in text:
            tags.append(tag)
    return sorted(set(tags))


def section_guidance(section: str, themes: list[str]) -> list[str]:
    guidance = []
    if section == '核心结论摘要':
        guidance.append('先结论，再依据，再建议，避免信息罗列。')
        if '管理层口径' in themes:
            guidance.append('使用管理层汇报语言，突出判断和取舍。')
        if '经营视角' in themes:
            guidance.append('落到经营影响、竞争格局和经营节奏。')
    elif section == '同业动态观察':
        guidance.append('强调重点股份行对比，不孤立描述单家银行。')
        if '同业对比' in themes:
            guidance.append('优先呈现平安与重点同业差距来源。')
        if '竞争格局' in themes:
            guidance.append('把指标变化翻译为竞争格局变化。')
    elif section == '贷款与产品观察':
        guidance.append('不要只报总量，要拆产品和结构。')
        if '产品结构' in themes or '结构拆解' in themes:
            guidance.append('强化产品结构、行业结构和投放节奏联动。')
    elif section == '定价观察':
        guidance.append('定价判断应和同业、产品、风险收益联动。')
        if '定价联动' in themes:
            guidance.append('避免孤立讨论利率高低，强调经营决策含义。')
    elif section == '策略建议':
        guidance.append('从事实推演到策略，再落到行动建议。')
        if '行动建议' in themes:
            guidance.append('建议要可执行，避免空泛表述。')
    elif section == '待人工确认事项':
        guidance.append('明确指出需要你确认的判断边界、口径或优先级。')
    return guidance


def main() -> None:
    log_path = REVIEWS / 'review-log.jsonl'
    out_path = PROCESSED / 'section_preferences.json'

    section_themes = defaultdict(Counter)
    section_examples = defaultdict(list)
    section_decisions = defaultdict(Counter)

    if log_path.exists():
        for line in log_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            section = item.get('category') or '未分类'
            section_decisions[section][item.get('decision', 'unknown')] += 1
            tags = classify_text(item.get('editedText', ''), item.get('reason', ''), item.get('originalText', ''))
            for tag in tags:
                section_themes[section][tag] += 1
                if len(section_examples[section]) < 5:
                    section_examples[section].append({
                        'itemId': item.get('itemId', ''),
                        'decision': item.get('decision', ''),
                        'tag': tag,
                        'editedText': item.get('editedText', ''),
                        'reason': item.get('reason', ''),
                    })

    sections = {}
    for section in DEFAULT_SECTIONS + [s for s in section_themes.keys() if s not in DEFAULT_SECTIONS]:
        top = [name for name, _ in section_themes[section].most_common(5)]
        sections[section] = {
            'topThemes': top,
            'decisionCount': dict(section_decisions[section]),
            'guidance': section_guidance(section, top),
            'examples': section_examples[section],
        }

    payload = {
        'sections': sections,
        'defaultSections': DEFAULT_SECTIONS,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out_path)


if __name__ == '__main__':
    main()
