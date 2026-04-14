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
    pref = load_json('preference_profile.json', {'topThemes': [], 'guidance': []})
    section = load_json('section_preferences.json', {'sections': {}})
    domain = load_json('domain_templates.json', {'domains': {}})

    top = set(pref.get('topThemes', []))
    domains = domain.get('domains', {})

    rules = {
        'deposit': {
            'title': '存款板块数据解释规则',
            'focusOrder': ['总量位置', '月度变化', '年初以来变化', '重点产品/结构', '同业相对差距'],
            'rules': [
                '先看平安银行在重点股份行中的相对位置，再判断是否存在经营压力或阶段性机会。',
                '不能只看余额大小，要同时解释月度变化和年初以来变化是否一致。',
                '如总量改善但增速落后，要提示结构问题或持续性不足。',
                '如增速改善但总量仍弱，要提示追赶阶段与资源投入要求。',
            ],
            'questionPrompts': [
                '差距主要来自总量基础、月度节奏还是结构短板？',
                '是否需要拆到产品、行业或客户结构层面继续看？',
            ],
        },
        'loan': {
            'title': '贷款板块数据解释规则',
            'focusOrder': ['投放规模', '月增量', '年增量', '产品结构', '行业映射', '同业差距'],
            'rules': [
                '优先解释投放节奏，而不是只陈列贷款余额。',
                '若余额增长但月增量走弱，要提示投放动能边际变化。',
                '若增量改善但结构不清，要提示需要补充产品和行业拆解。',
                '贷款结论尽量落到业务打法、投向选择和经营侧含义。',
            ],
            'questionPrompts': [
                '增长来自哪些产品和行业？',
                '投放节奏变化是主动调节还是竞争承压？',
            ],
        },
        'pricing': {
            'title': '定价板块数据解释规则',
            'focusOrder': ['同业利率位置', '平安相对水平', '产品结构影响', '风险收益匹配', '经营含义'],
            'rules': [
                '不能孤立评价利率高低，必须结合产品结构和风险收益。',
                '若利率低于同业，要判断是战略让价、优质客群驱动，还是收益承压。',
                '若利率高于同业，要判断是风险补偿、结构差异，还是竞争力不足。',
                '定价结论最终应服务经营决策与资源配置。',
            ],
            'questionPrompts': [
                '利率差异主要由产品结构还是风险收益造成？',
                '当前定价水平对规模、收益和竞争位置意味着什么？',
            ],
        },
        'peer': {
            'title': '同业板块数据解释规则',
            'focusOrder': ['重点股份行排序', '平安相对位置', '差距来源', '竞争格局变化', '经营启示'],
            'rules': [
                '同业观察优先看平安与重点股份行的相对位置，而不是泛泛列榜。',
                '发现差距后要追问差距来自规模、增量、结构还是定价。',
                '同业变化要翻译成竞争格局和经营节奏变化。',
                '避免把同业数据写成资讯摘要，必须转成经营判断。',
            ],
            'questionPrompts': [
                '平安当前最值得盯住的同业是谁？',
                '差距是扩大、收敛，还是结构性错位？',
            ],
        },
    }

    if '管理层口径' in top:
        for item in rules.values():
            item['rules'].insert(0, '解释顺序采用管理层汇报口径：先结论，再证据，再经营含义。')
    if '经营视角' in top:
        for item in rules.values():
            item['rules'].append('每条解释尽量补一句经营影响，避免停留在数据描述。')
    if '同业对比' in top:
        for key in ('deposit', 'loan', 'pricing'):
            rules[key]['rules'].append('补充与重点同业的横向比较，增强判断基准。')
    if '定价联动' in top:
        for key in ('loan', 'pricing'):
            rules[key]['rules'].append('输出时同步检查定价、产品和风险收益三者是否一致。')

    sections = section.get('sections', {})
    for key, sec_name in [('deposit', '核心结论摘要'), ('peer', '同业动态观察'), ('loan', '贷款与产品观察'), ('pricing', '定价观察')]:
        sec = sections.get(sec_name, {})
        if sec.get('guidance'):
            rules[key]['sectionLinkedGuidance'] = sec.get('guidance', [])[:3]

    for key, dom in domains.items():
        if dom.get('guidance'):
            rules[key]['domainLinkedGuidance'] = dom.get('guidance', [])[:4]

    return {'rules': rules}


def main() -> None:
    out = PROCESSED / 'interpretation_rules.json'
    payload = build_rules()
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
