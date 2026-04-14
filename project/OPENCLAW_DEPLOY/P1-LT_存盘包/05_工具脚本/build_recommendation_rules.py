from __future__ import annotations

import json
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
PROCESSED = BASE / 'data' / 'processed'


def load_json(name: str, default):
    path = PROCESSED / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def build_rules():
    pref = load_json('preference_profile.json', {'topThemes': []})
    domains = load_json('domain_templates.json', {'domains': {}}).get('domains', {})
    interpretation = load_json('interpretation_rules.json', {'rules': {}}).get('rules', {})

    top = set(pref.get('topThemes', []))

    rules = {
        'observation': {
            'title': '观察提示生成规则',
            'purpose': '用于提示值得持续跟踪的变化，不直接下结论推动动作。',
            'criteria': [
                '指标出现边际变化，但证据尚不足以直接形成策略动作。',
                '趋势已经出现，但仍需补充结构、行业或产品拆解。',
                '同业相对位置出现变化，需要持续跟踪而非立即处置。',
            ],
            'style': [
                '用“值得关注”“建议跟踪”“需继续观察”等表述，避免过度下判断。',
                '每条观察尽量说明触发数据和潜在经营含义。',
            ],
            'defaultPriority': 'medium',
            'needReview': False,
        },
        'strategy': {
            'title': '策略建议生成规则',
            'purpose': '用于形成经营判断后的方向性建议。',
            'criteria': [
                '同业差距、结构变化或定价变化已经具备较清晰方向。',
                '可以形成资源配置、经营节奏、产品打法或客户策略建议。',
                '结论具备一定证据基础，但不一定需要立即执行动作。',
            ],
            'style': [
                '用“建议优化”“建议加强”“建议调整”等策略表达。',
                '必须说明建议服务的经营目标或竞争格局变化。',
            ],
            'defaultPriority': 'high',
            'needReview': True,
        },
        'action': {
            'title': '直接行动建议生成规则',
            'purpose': '用于推动近期需要执行或明确跟进的事项。',
            'criteria': [
                '问题或机会较明确，且已有足够证据支持近期动作。',
                '可以落到产品、客户、行业、定价或经营动作层面。',
                '如不及时行动，可能带来明显经营损失或错失窗口。',
            ],
            'style': [
                '用“建议尽快”“本周应”“优先推动”等动作语言。',
                '动作要具体，可落到责任对象、节奏或优先顺序。',
            ],
            'defaultPriority': 'urgent',
            'needReview': True,
        },
    }

    if '管理层口径' in top:
        for item in rules.values():
            item['style'].insert(0, '先写结论，再写依据，最后写动作或影响。')
    if '行动建议' in top:
        rules['strategy']['style'].append('策略建议要尽量靠近可执行动作，避免空泛。')
        rules['action']['style'].append('直接行动建议要明确优先级和执行紧迫性。')
    if '经营视角' in top:
        for item in rules.values():
            item['style'].append('建议必须落到经营影响，而不是只停留在数据描述。')

    domain_mapping = {
        'deposit': {
            'observation': ['存款增速、结构或同业位置变化但尚需进一步拆解时，优先生成观察提示。'],
            'strategy': ['存款板块策略建议优先围绕负债结构优化、重点产品组织和客户经营节奏。'],
            'action': ['存款板块直接行动建议优先落到重点产品推动、客户维护或阶段性资源配置。'],
        },
        'loan': {
            'observation': ['贷款动能变化但产品或行业来源尚不清晰时，优先生成观察提示。'],
            'strategy': ['贷款板块策略建议优先围绕投放节奏、重点行业、产品结构和竞争打法。'],
            'action': ['贷款板块直接行动建议优先落到重点行业投放、产品推动和名单制跟踪。'],
        },
        'pricing': {
            'observation': ['利率变化出现异常但尚未确认结构原因时，优先生成观察提示。'],
            'strategy': ['定价板块策略建议优先围绕风险收益平衡、产品组合和同业策略响应。'],
            'action': ['定价板块直接行动建议优先落到重点产品调价、客群筛选或价格授权校准。'],
        },
        'peer': {
            'observation': ['同业位置变化但差距来源仍不充分时，优先生成观察提示。'],
            'strategy': ['同业板块策略建议优先围绕竞争应对、资源配置和经营节奏调整。'],
            'action': ['同业板块直接行动建议优先落到重点同业盯防、专项复盘和打法纠偏。'],
        },
    }

    for domain_key, values in domain_mapping.items():
        linked = {
            'domainTitle': domains.get(domain_key, {}).get('title', domain_key),
            'interpretationTitle': interpretation.get(domain_key, {}).get('title', ''),
        }
        for rule_key in ('observation', 'strategy', 'action'):
            rules[rule_key].setdefault('domainSpecific', {})[domain_key] = {
                'guidance': values[rule_key],
                'linked': linked,
            }

    return {'rules': rules}


def main() -> None:
    out = PROCESSED / 'recommendation_rules.json'
    payload = build_rules()
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
