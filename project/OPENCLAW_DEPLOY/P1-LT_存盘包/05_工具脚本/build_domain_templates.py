from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REVIEWS = BASE / 'reviews'
PROCESSED = BASE / 'data' / 'processed'

DOMAIN_KEYWORDS = {
    'deposit': ['存款', '负债', '资金沉淀'],
    'loan': ['贷款', '投放', '授信', '融资'],
    'pricing': ['定价', '利率', '风险收益', '收益'],
    'peer': ['同业', '股份行', '竞争', '对标'],
}

THEME_KEYWORDS = {
    '经营视角': ['经营', '节奏', '资源配置'],
    '管理层口径': ['管理', '汇报', '口径'],
    '同业对比': ['同业', '对标', '竞争'],
    '结构拆解': ['结构', '拆解'],
    '产品结构': ['产品'],
    '定价联动': ['定价', '利率', '风险收益'],
    '行动建议': ['行动', '落地', '执行'],
    '策略推演': ['策略', '推演'],
}

DOMAIN_TITLES = {
    'deposit': '存款板块',
    'loan': '贷款板块',
    'pricing': '定价板块',
    'peer': '同业板块',
}


def detect_domains(text: str) -> list[str]:
    result = []
    for domain, kws in DOMAIN_KEYWORDS.items():
        if any(kw in text for kw in kws):
            result.append(domain)
    return result


def detect_themes(text: str) -> list[str]:
    result = []
    for theme, kws in THEME_KEYWORDS.items():
        if any(kw in text for kw in kws):
            result.append(theme)
    return result


def domain_guidance(domain: str, themes: list[str]) -> list[str]:
    base = []
    if domain == 'deposit':
        base.append('存款板块优先解释体量变化背后的经营原因，不只展示余额变化。')
        base.append('存款判断尽量同时覆盖总量、月度变化、年初以来变化和重点产品结构。')
    elif domain == 'loan':
        base.append('贷款板块优先说明投放节奏、结构变化和行业映射，不只报增量。')
        base.append('贷款判断尽量结合重点产品、行业投向和竞争态势。')
    elif domain == 'pricing':
        base.append('定价板块优先联动同业利率、产品结构和风险收益，不孤立讨论高低。')
        base.append('定价建议应服务经营决策，而不是停留在价格描述。')
    elif domain == 'peer':
        base.append('同业板块优先突出平安与重点股份行的相对位置和差距来源。')
        base.append('同业观察应把指标变化翻译为竞争格局和经营启示。')

    if '管理层口径' in themes:
        base.append('表达应更接近管理层汇报语言，结论先行。')
    if '经营视角' in themes:
        base.append('强调经营影响、经营节奏和资源配置含义。')
    if '结构拆解' in themes or '产品结构' in themes:
        base.append('补充结构拆解，避免只有总量判断。')
    if '同业对比' in themes and domain != 'peer':
        base.append('适度补充与重点同业的对比，增强判断参照。')
    if '定价联动' in themes and domain in ('loan', 'pricing'):
        base.append('输出时补充定价、产品和风险收益三者联动。')
    if '行动建议' in themes:
        base.append('结论后尽量给出可执行动作。')
    return base


def main() -> None:
    log_path = REVIEWS / 'review-log.jsonl'
    out_path = PROCESSED / 'domain_templates.json'

    theme_counter = defaultdict(Counter)
    examples = defaultdict(list)
    decision_counter = defaultdict(Counter)

    if log_path.exists():
        for line in log_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            text = ' '.join([
                item.get('originalText', ''),
                item.get('editedText', ''),
                item.get('reason', ''),
                item.get('category', ''),
            ])
            domains = detect_domains(text)
            themes = detect_themes(text)
            for domain in domains:
                decision_counter[domain][item.get('decision', 'unknown')] += 1
                for theme in themes:
                    theme_counter[domain][theme] += 1
                    if len(examples[domain]) < 5:
                        examples[domain].append({
                            'itemId': item.get('itemId', ''),
                            'decision': item.get('decision', ''),
                            'theme': theme,
                            'editedText': item.get('editedText', ''),
                            'reason': item.get('reason', ''),
                        })

    domains = {}
    for domain, title in DOMAIN_TITLES.items():
        top = [name for name, _ in theme_counter[domain].most_common(5)]
        domains[domain] = {
            'title': title,
            'topThemes': top,
            'decisionCount': dict(decision_counter[domain]),
            'guidance': domain_guidance(domain, top),
            'examples': examples[domain],
        }

    payload = {'domains': domains, 'domainTitles': DOMAIN_TITLES}
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out_path)


if __name__ == '__main__':
    main()
