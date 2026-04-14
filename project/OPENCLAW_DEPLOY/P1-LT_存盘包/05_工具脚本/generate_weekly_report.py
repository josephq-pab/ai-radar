from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
PROCESSED = BASE / 'data' / 'processed'
REPORTS = BASE / 'reports'


def load_json(name: str) -> Any:
    return json.loads((PROCESSED / name).read_text(encoding='utf-8'))


def load_optional_json(name: str, default):
    path = PROCESSED / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def load_tracking_items() -> dict:
    """读取 tracking-items.json，路径为 REPORTS/ 而非 PROCESSED/reports/"""
    path = REPORTS / 'tracking-items.json'
    if not path.exists():
        return {'items': [], 'trackingStatusSummary': {}}
    return json.loads(path.read_text(encoding='utf-8'))


def load_optional_json_from_base(name: str, default):
    path = BASE / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def fmt_num(value: Any) -> str:
    if value in (None, ''):
        return '--'
    try:
        return f'{float(value):,.2f}'
    except Exception:
        return str(value)


def fmt_pct(value: Any) -> str:
    if value in (None, ''):
        return '--'
    try:
        v = float(value)
        if abs(v) > 1:
            return f'{v:.2f}%'
        return f'{v * 100:.2f}%'
    except Exception:
        return str(value)


def pick_bank(rows, bank_name):
    for row in rows:
        if row.get('bank') == bank_name:
            return row
    return None


def add_guidance(lines: list[str], guidance: list[str], prefix: str) -> None:
    for g in guidance or []:
        lines.append(f'- {prefix} {g}')


def build_report() -> str:
    summary = load_json('summary.json')
    deposits = load_json('deposit_benchmark.json')
    loans = load_json('loan_benchmark.json')
    rates = load_json('loan_rate.json')
    preference = load_optional_json('preference_profile.json', {'guidance': [], 'topThemes': [], 'totalReviews': 0})
    section_pref = load_optional_json('section_preferences.json', {'sections': {}})
    domain_templates = load_optional_json('domain_templates.json', {'domains': {}})
    interpretation_rules = load_optional_json('interpretation_rules.json', {'rules': {}})
    recommendation_rules = load_optional_json('recommendation_rules.json', {'rules': {}})
    review_queue = load_optional_json('review-queue.json', {'items': []})
    tracking_items = load_tracking_items()

    core_pref = section_pref.get('sections', {}).get('核心结论摘要', {})
    peer_pref = section_pref.get('sections', {}).get('同业动态观察', {})
    loan_pref = section_pref.get('sections', {}).get('贷款与产品观察', {})
    pricing_pref = section_pref.get('sections', {}).get('定价观察', {})
    strategy_pref = section_pref.get('sections', {}).get('策略建议', {})
    pending_pref = section_pref.get('sections', {}).get('待人工确认事项', {})

    deposit_domain = domain_templates.get('domains', {}).get('deposit', {})
    loan_domain = domain_templates.get('domains', {}).get('loan', {})
    pricing_domain = domain_templates.get('domains', {}).get('pricing', {})
    peer_domain = domain_templates.get('domains', {}).get('peer', {})

    deposit_rule = interpretation_rules.get('rules', {}).get('deposit', {})
    loan_rule = interpretation_rules.get('rules', {}).get('loan', {})
    pricing_rule = interpretation_rules.get('rules', {}).get('pricing', {})
    peer_rule = interpretation_rules.get('rules', {}).get('peer', {})

    observation_rule = recommendation_rules.get('rules', {}).get('observation', {})
    strategy_rule = recommendation_rules.get('rules', {}).get('strategy', {})
    action_rule = recommendation_rules.get('rules', {}).get('action', {})

    deposit_total = [x for x in deposits if x.get('metricCode') == 'balance_total']
    loan_general = [x for x in loans if x.get('metricCode') == 'loan_balance']
    rate_rows = [x for x in rates if x.get('bank') in summary['focusBanks']]

    dep_sorted = sorted(
        [x for x in deposit_total if x.get('bank') in summary['focusBanks']],
        key=lambda x: x.get('currentValue') or 0,
        reverse=True,
    )
    loan_sorted = sorted(
        [x for x in loan_general if x.get('bank') in summary['focusBanks']],
        key=lambda x: x.get('currentValue') or 0,
        reverse=True,
    )
    rate_sorted = sorted(rate_rows, key=lambda x: x.get('monthlyRate') or 999)

    pa_dep = pick_bank(dep_sorted, '平安银行')
    pa_loan = pick_bank(loan_sorted, '平安银行')
    pa_rate = pick_bank(rate_sorted, '平安银行')

    top_dep = dep_sorted[0] if dep_sorted else None
    top_loan = loan_sorted[0] if loan_sorted else None
    low_rate = rate_sorted[0] if rate_sorted else None

    lines: list[str] = []
    lines.append('# 对公 AI 雷达站周报（草稿）\n')

    lines.append('## 零、偏好学习指引\n')
    if preference.get('guidance'):
        for g in preference['guidance']:
            lines.append(f'- {g}')
    else:
        lines.append('- 默认先结论，后依据，再建议。')
    if preference.get('topThemes'):
        lines.append('- 当前识别到的重点偏好主题：' + ' / '.join(preference['topThemes']))
    lines.append(f'- 当前累计确认样本数：{preference.get("totalReviews", 0)}')

    lines.append('\n## 一、核心结论摘要\n')
    add_guidance(lines, core_pref.get('guidance', []), '[栏目口径]')
    add_guidance(lines, deposit_domain.get('guidance', [])[:2], '[板块模板]')
    add_guidance(lines, deposit_rule.get('rules', [])[:2], '[解释规则]')
    if top_dep:
        lines.append(f'- 存款对标看，当前重点股份行中，{top_dep["bank"]}在"{top_dep["metricGroup"]}"口径下体量领先，余额约 {fmt_num(top_dep["currentValue"])}。')
    if pa_dep:
        lines.append(f'- 平安银行当前"{pa_dep["metricGroup"]}"余额约 {fmt_num(pa_dep["currentValue"])}，较上月变动 {fmt_num(pa_dep["monthChange"])}，较年初变动 {fmt_num(pa_dep["yearChange"])}，需结合结构和口径进一步拆解。')
    if top_loan:
        lines.append(f'- 贷款对标看，{top_loan["bank"]}在"{top_loan["metricGroup"]}"口径下余额领先，约 {fmt_num(top_loan["currentValue"])}，说明头部股份行在重点对公贷款投放上仍具显著规模优势。')
    if pa_loan:
        lines.append(f'- 平安银行在贷款对标中当前余额约 {fmt_num(pa_loan["currentValue"])}，建议重点观察与同业的月增量、产品结构与定价联动，而不只看单点规模。')
    if low_rate and pa_rate:
        lines.append(f'- 贷款利率对标看，最低月度加权平均利率为 {low_rate["bank"]} 的 {fmt_pct(low_rate["monthlyRate"])}；平安银行当前约 {fmt_pct(pa_rate["monthlyRate"])}，后续应结合投放方向与风险收益评估定价空间。')

    lines.append('\n## 二、同业动态观察\n')
    add_guidance(lines, peer_pref.get('guidance', []), '[栏目口径]')
    add_guidance(lines, peer_domain.get('guidance', [])[:2], '[板块模板]')
    add_guidance(lines, peer_rule.get('rules', [])[:3], '[解释规则]')
    for row in dep_sorted[:8]:
        lines.append(f'- {row["bank"]}：存款余额 {fmt_num(row["currentValue"])}，较上月 {fmt_num(row["monthChange"])}，较年初 {fmt_num(row["yearChange"])}，年初以来增幅 {fmt_pct(row["yearGrowth"])}。')

    lines.append('\n## 三、贷款与产品观察\n')
    add_guidance(lines, loan_pref.get('guidance', []), '[栏目口径]')
    add_guidance(lines, loan_domain.get('guidance', [])[:2], '[板块模板]')
    add_guidance(lines, loan_rule.get('rules', [])[:3], '[解释规则]')
    for row in loan_sorted[:8]:
        lines.append(f'- {row["bank"]}：{row["metricGroup"]}余额 {fmt_num(row["currentValue"])}，月增量 {fmt_num(row["monthChange"])}，年增量 {fmt_num(row["yearChange"])}，年增幅 {fmt_pct(row["yearGrowth"])}。')

    lines.append('\n## 四、定价观察\n')
    add_guidance(lines, pricing_pref.get('guidance', []), '[栏目口径]')
    add_guidance(lines, pricing_domain.get('guidance', [])[:2], '[板块模板]')
    add_guidance(lines, pricing_rule.get('rules', [])[:3], '[解释规则]')
    for row in rate_sorted[:8]:
        lines.append(f'- {row["bank"]}：当月新发放加权平均利率 {fmt_pct(row["monthlyRate"])}，当年新发放加权平均利率 {fmt_pct(row["ytdRate"])}。')

    lines.append('\n## 五、观察提示\n')
    add_guidance(lines, observation_rule.get('style', [])[:2], '[生成规则]')
    lines.append(f'- [优先级:{observation_rule.get("defaultPriority", "medium")}] 存款对标若出现总量改善但增速仍落后于重点股份行，建议继续观察其可持续性与结构支撑。')
    lines.append(f'- [优先级:{observation_rule.get("defaultPriority", "medium")}] 若贷款月增量出现波动但产品与行业来源尚未拆清，建议先作为跟踪信号保留。')
    lines.append(f'- [优先级:{observation_rule.get("defaultPriority", "medium")}] 若利率位置变化已出现但尚无法区分是结构驱动还是收益承压，建议保持观察而不急于定性。')

    lines.append('\n## 六、策略建议\n')
    add_guidance(lines, strategy_pref.get('guidance', []), '[栏目口径]')
    add_guidance(lines, strategy_rule.get('style', [])[:2], '[生成规则]')
    lines.append(f'- [优先级:{strategy_rule.get("defaultPriority", "high")}] 建议把同业对标从"总量比较"升级为"总量 + 增量 + 结构 + 定价"四维联动分析，形成更稳定的经营研判框架。')
    lines.append(f'- [优先级:{strategy_rule.get("defaultPriority", "high")}] 建议在周报中单列平安银行与重点股份行差距来源拆解，重点说明差距来自规模、节奏、结构还是定价。')
    lines.append(f'- [优先级:{strategy_rule.get("defaultPriority", "high")}] 建议将贷款产品结构、同业定价与风险收益并列呈现，让策略建议更贴近经营决策。')

    lines.append('\n## 七、直接行动建议\n')
    add_guidance(lines, action_rule.get('style', [])[:2], '[生成规则]')
    lines.append(f'- [优先级:{action_rule.get("defaultPriority", "urgent")}] 本周应优先补齐平安银行存款与贷款差距的产品/行业拆解，形成管理层可直接使用的差距来源说明。')
    lines.append(f'- [优先级:{action_rule.get("defaultPriority", "urgent")}] 优先推动贷款与定价联动分析，补出"产品结构-利率水平-风险收益"三者关系。')
    lines.append(f'- [优先级:{action_rule.get("defaultPriority", "urgent")}] 针对重点同业中变化最明显的 1-2 家银行，启动专项盯防和打法复盘。')

    lines.append('\n## 八、待人工确认事项\n')
    add_guidance(lines, pending_pref.get('guidance', []), '[栏目口径]')
    add_guidance(
        lines,
        (deposit_rule.get('questionPrompts', [])[:1]
         + loan_rule.get('questionPrompts', [])[:1]
         + pricing_rule.get('questionPrompts', [])[:1]
         + peer_rule.get('questionPrompts', [])[:1]),
        '[追问提示]',
    )
    lines.append('- 上述观察提示中，哪些已经具备升级为正式策略建议的证据基础。')
    lines.append('- 直接行动建议中，哪些需要先补充产品、行业或客群拆解后再推动。')
    lines.append('- 对"较高/较低利率"的判断，是否需要结合风险收益与政策导向做二次校正。')

    # --- Section 9: Tracking Status Summary (D深化) ---
    lines.append('\n## 九、重点事项跟踪状态汇总\n')
    summary_tracking = tracking_items.get('trackingStatusSummary', {})
    if summary_tracking:
        lines.append(f'- 待研判：{summary_tracking.get("待研判", 0)} 项')
        lines.append(f'- 跟踪中：{summary_tracking.get("跟踪中", 0)} 项')
        lines.append(f'- 已上报：{summary_tracking.get("已上报", 0)} 项')
        lines.append(f'- 已行动：{summary_tracking.get("已行动", 0)} 项')
        lines.append(f'- 已关闭：{summary_tracking.get("已关闭", 0)} 项')
    else:
        lines.append('- 暂无跟踪状态汇总数据')

    # --- Section 10: Tracking Items (D深化) ---
    items = tracking_items.get('items', [])
    if items:
        lines.append('\n## 十、事项明细\n')
        for item in items:
            layer = item.get('layer', '待确认')
            priority = item.get('priority', 'medium')
            status = item.get('trackingStatus', '待研判')
            dimension = item.get('sourceDimension', '整体')
            theme = item.get('sourceTheme', '暂无')
            text = item.get('text', '暂无内容')
            latest = item.get('latestProgress', '')
            next_action = item.get('nextAction', '')
            source = item.get('sourceName', '')
            href = item.get('sourceHref', '#')
            lines.append(f'### {item.get("id", "未知")} [{layer}] [优先级:{priority}] [{status}]\n')
            lines.append(f'- 业务维度：{dimension} / 来源主题：{theme}')
            if text:
                lines.append(f'- 事项内容：{text}')
            if latest:
                lines.append(f'- 最新进展：{latest}')
            if next_action:
                lines.append(f'- 下一步动作：{next_action}')
            lines.append(f'- 来源页面：[{source}]({href})')
    else:
        lines.append('\n## 十、事项明细\n')
        lines.append('- 暂无事项数据')

    # ── 分析师观点补充（阶段D扩展）───────────────────────
    analyst_raw = load_optional_json_from_base('data/processed/analyst_opinions.json', {})
    analyst_records = analyst_raw.get('records', [])
    analyst_top = [r for r in analyst_records if r.get('enterReport', False)]
    if analyst_top:
        lines.append('\n## 十一、分析师观点补充\n')
        lines.append('> 以下观点来自公开可访问的分析师/专家署名文章，按相关性·可信度·可行动性综合评分筛选。观点不代表本行立场，仅供内部参考。\n')
        section_groups = {}
        for r in analyst_top:
            sec = r.get('reportSection', '一、核心结论摘要（分析师观点）')
            if sec not in section_groups:
                section_groups[sec] = []
            section_groups[sec].append(r)

        for sec, records in section_groups.items():
            lines.append(f'### {sec}\n')
            for r in records:
                analyst = r.get('analystName', '未知')
                org = r.get('org', '')
                title = r.get('articleTitle', '无标题')
                url = r.get('sourceUrl', '#')
                pub = r.get('publishedAt', '')
                summary = r.get('summary', '')
                rel = r.get('relevanceScore', 0)
                conf = r.get('confidenceScore', 0)
                act = r.get('actionabilityScore', 0)
                ref = r.get('isReferenceable', False)  # VALID 级别才有分析师归因

                if ref:
                    # ── VALID：可引用，写入分析师归因 ──────────────────
                    lines.append(f'#### {analyst}{f"（{org}）" if org else ""}')
                    lines.append(f'- 文章：[{title}]({url})' + (f' | {pub[:10]}' if pub else ''))
                    if summary:
                        lines.append(f'- 摘要：{summary[:200]}')
                    evs = r.get('evidenceSnippets', [])
                    vps = r.get('keyViewpoints', [])
                    if vps:
                        lines.append(f'- 核心观点：{vps[0][:150]}')
                    elif evs:
                        lines.append(f'- 关键数据：{evs[0][:150]}')
                    lines.append(f'- 评分：相关{rel:.0%} | 可信{conf:.0%} | 可行动{act:.0%}')
                    lines.append('')
                else:
                    # ── DEGRADED：不可引用，写入背景事实（不归因给分析师）──
                    # 标题不出现分析师姓名；正文不写"某分析师认为/指出"
                    # snippet 来源标注为"市场信息"而非"分析师观点"
                    evs = r.get('evidenceSnippets', [])
                    if evs:
                        # 取第一条 snippet 作为市场背景，不冠以分析师名义
                        market_fact = evs[0][:150]
                        lines.append(f'#### {title[:40]}')
                        lines.append(f'- 市场信息（来源：{url}，{pub[:10] if pub else "时间不详"}）')
                        lines.append(f'  {market_fact}')
                        lines.append(f'- 评分：相关{rel:.0%} | 可信{conf:.0%} | 可行动{act:.0%}')
                        lines.append(f'- 注：该来源正文为记者报道转写，不可直接引用为分析师观点')
                        lines.append('')
                    else:
                        # 既无 snippet 也无 viewpoints，仅作记录，不写无意义条目
                        pass
    else:
        lines.append('\n## 十一、分析师观点补充\n')
        lines.append('- 本期暂无符合条件的分析师观点进入周报')

    return '\n'.join(lines) + '\n'


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    content = build_report()
    path = REPORTS / 'weekly-report-draft.md'
    path.write_text(content, encoding='utf-8')
    print(path)


if __name__ == '__main__':
    main()
