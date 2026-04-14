#!/usr/bin/env python3
"""
generate_ops_dashboard.py — 生成运营行动面板

用法：
    python3 scripts/generate_ops_dashboard.py

产物：
    reports/ops-dashboard.json   — 机器可读版本
    reports/ops-dashboard.md    — 人类可读版本

内容：
    1. 本周阻塞项（blocking）
    2. 本周必须动作（must-do）
    3. 本周不必做的事（avoid）
    4. 条件触发动作（conditional-actions）
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REPORTS = BASE / 'reports'
PROCESSED = BASE / 'data' / 'processed'


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def main() -> None:
    now = datetime.now(timezone.utc)

    # ── 读取各数据源 ──────────────────────────────────
    run_summary = load_json(REPORTS / 'run-summary.json')
    ti = load_json(REPORTS / 'tracking-items.json')
    rs = load_json(REPORTS / 'review-status.json')
    ao = load_json(PROCESSED / 'analyst_opinions.json')

    # 解析 freshness
    deposit_fresh = None
    loan_fresh = None
    rate_fresh = None
    deposit_raw = load_json(PROCESSED / 'deposit_benchmark.json')
    loan_raw = load_json(PROCESSED / 'loan_benchmark.json')
    rate_raw = load_json(PROCESSED / 'loan_rate.json')
    if deposit_raw and isinstance(deposit_raw, list) and deposit_raw:
        dates = sorted(set(r.get('observedAt', '') for r in deposit_raw if r.get('observedAt')))
        deposit_fresh = dates[-1] if dates else None
    if loan_raw and isinstance(loan_raw, list) and loan_raw:
        dates = sorted(set(r.get('observedAt', '') for r in loan_raw if r.get('observedAt')))
        loan_fresh = dates[-1] if dates else None
    if rate_raw and isinstance(rate_raw, list) and rate_raw:
        dates = sorted(set(r.get('observedAt', '') for r in rate_raw if r.get('observedAt')))
        rate_fresh = dates[-1] if dates else None

    # analyst quality
    KNOWN_GARBLED = ['æ', 'å', 'è', 'ï', '¶', '¹', '¸', '»', '鏍稿績', '钁ｅ笇', '�']
    PLACEHOLDER_TITLES = {'finance.eastmoney.com', '37619039f873daba6891f6e99b61fac2'}
    ao_records = ao.get('records', []) if ao else []

    # timezone-safe date comparison
    def days_old(date_str):
        if not date_str:
            return None
        d = datetime.fromisoformat(date_str)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return (now - d).days
    ao_valid = [r for r in ao_records
                if r.get('articleTitle', '').strip()
                and not any(c in r.get('articleTitle', '') for c in KNOWN_GARBLED)
                and r.get('articleTitle', '').strip() not in PLACEHOLDER_TITLES]
    ao_garbled = [r for r in ao_records if any(c in r.get('articleTitle', '') for c in KNOWN_GARBLED)]
    ao_placeholder = [r for r in ao_records if r.get('articleTitle', '').strip() in PLACEHOLDER_TITLES]

    # pending items
    all_items = ti.get('items', []) if ti else []
    pending_items = [i for i in all_items if i.get('trackingStatus') in ('待研判', '跟踪中')]
    stagnation_info = None
    if run_summary:
        stagnation_info = run_summary.get('trustSummary', {}).get('trackingStagnation', {})
    readiness = None
    if run_summary:
        readiness = run_summary.get('readinessLevels', {})

    # ── 构建阻塞项 ────────────────────────────────────
    blocking = []

    if deposit_fresh is None or loan_fresh is None:
        blocking.append({
            'id': 'missing-benchmark-data',
            'severity': 'critical',
            'title': '核心 benchmark 数据缺失或无法解析',
            'description': '存款或贷款对标数据文件不存在或解析失败',
            'action': '检查 data/raw/ 目录下的 Excel 文件',
            'owner': '系统',
        })
    elif deposit_fresh and days_old(deposit_fresh) and days_old(deposit_fresh) > 30:
        blocking.append({
            'id': 'stale-benchmark-data',
            'severity': 'high',
            'title': f'核心 benchmark 数据过期（最新：{deposit_fresh}）',
            'description': f'deposit/loan observedAt={deposit_fresh}，已超过 30 天。rate observedAt={rate_fresh}。',
            'action': '推动业务侧提供 2026-03 月度数据，放入 data/raw/ 后执行 import_monthly_data.py --confirm',
            'owner': '业务分析师',
        })

    if rate_fresh and days_old(rate_fresh) and days_old(rate_fresh) > 45:
        blocking.append({
            'id': 'stale-rate-data',
            'severity': 'high',
            'title': f'贷款利率数据严重过期（最新：{rate_fresh}）',
            'description': f'loan_rate observedAt={rate_fresh}，已超过 45 天，对利率判断影响较大',
            'action': '优先推动提供 2026-03 贷款利率数据',
            'owner': '业务分析师',
        })

    if len(ao_valid) < 3:
        blocking.append({
            'id': 'insufficient-analyst-input',
            'severity': 'medium',
            'title': f'analyst 层有效记录不足（{len(ao_valid)} 条）',
            'description': f'有效 {len(ao_valid)} 条，乱码 {len(ao_garbled)} 条，空/占位 {len(ao_placeholder)} 条。周报引用 analyst 层需人工确认。',
            'action': '修复抓取脚本编码问题，或扩大白名单至有效分析师 ≥5 人',
            'owner': '技术/业务',
        })

    # 静默 pending
    silent = stagnation_info.get('silentPending', []) if stagnation_info else []
    if silent:
        blocking.append({
            'id': 'silent-pending-items',
            'severity': 'medium',
            'title': f'{len(silent)} 项静默 pending（无 review 记录）',
            'description': '这些事项从未进入 review 流程，时间戳不可信，可能长期悬停',
            'action': '逐项确认是否仍需跟踪：是则进入 review 流程，否则关闭',
            'items': [{'id': s['id'], 'text': s['text'][:50]} for s in silent],
            'owner': '邱非',
        })

    if stagnation_info and stagnation_info.get('stagnationLevel', 0) >= 2:
        blocking.append({
            'id': 'tracking-stagnation',
            'severity': 'medium',
            'title': f'tracking 存在停滞（level={stagnation_info.get("stagnationLevel")}）',
            'description': stagnation_info.get('stagnationText', ''),
            'action': '检查 review-log 和 tracking-status-log，推动 pending 项流转',
            'owner': '邱非',
        })

    # ── 必须动作 ────────────────────────────────────────
    must_do = []

    if deposit_fresh and days_old(deposit_fresh) and days_old(deposit_fresh) > 25:
        must_do.append({
            'id': 'get-march-data',
            'priority': 'high',
            'title': '推动提供 2026-03 月度数据文件',
            'description': '当前 benchmark 数据截至 2026-02，月报节奏要求每月 5 日前到位',
            'steps': [
                '联系业务分析师获取 2026-03 存款/贷款/利率 Excel',
                '放入 data/raw/ 目录',
                '执行 python3 scripts/import_monthly_data.py --dry-run 验证',
                '确认无误后执行 python3 scripts/import_monthly_data.py --confirm',
                '执行 python3 scripts/smoke_test.py --fast 验证',
            ],
            'trigger': '一旦收到新文件',
        })

    if len(ao_valid) < 3:
        must_do.append({
            'id': 'fix-analyst-layer',
            'priority': 'medium',
            'title': '处理 analyst 层抓取质量问题',
            'description': f'当前有效仅 {len(ao_valid)} 条，乱码 {len(ao_garbled)} 条，需修复编码或更换数据源',
            'steps': [
                f'检查 fetch_analyst_articles.py 编码处理逻辑',
                '对乱码记录（董希淼、娄飞鹏、连平）补充 articleTitle',
                '扩大有效分析师白名单，目标 ≥5 条有效记录',
                '执行 python3 scripts/fetch_analyst_articles.py 重新抓取',
                '执行 python3 scripts/build_analyst_opinions.py',
                '验证 analyst_opinions.json records 中有效记录数',
            ],
            'trigger': 'analyst 抓取质量问题修复后',
        })

    if pending_items:
        # 按类型分组
        pending_by_cat = {}
        for item in pending_items:
            cat = item.get('sourceDimension', '未知')
            if cat not in pending_by_cat:
                pending_by_cat[cat] = []
            pending_by_cat[cat].append({'id': item.get('id', ''), 'text': item.get('text', '')[:50]})

        for cat, items in pending_by_cat.items():
            must_do.append({
                'id': f'review-pending-{cat}',
                'priority': 'medium',
                'title': f'推进 {cat} pending 项 review',
                'description': f'共 {len(items)} 项待研判/跟踪中，需在汇报前完成确认',
                'steps': [
                    f'逐项 review：python3 scripts/record_review.py <itemId> <decision>',
                    'decision 可选：approve / modify / reject',
                    '修改后执行 python3 scripts/sync_after_review.py --confirm',
                    '执行 python3 scripts/smoke_test.py --fast 验证',
                ],
                'items': items,
                'trigger': '汇报前至少 1 天',
            })

    # ── 不必做的事 ──────────────────────────────────────
    avoid = [
        {
            'id': 'avoid-ui-redesign',
            'title': '不要进行 UI 重构或高保真改版',
            'reason': '当前阶段重点是数据链路和运营可信度，不是视觉层',
        },
        {
            'id': 'avoid-expand-pages',
            'title': '不要新增一级页面或扩张页面数量',
            'reason': '四页主链路已稳定，继续扩张会增加维护成本和一致性风险',
        },
        {
            'id': 'avoid-db-migration',
            'title': '不要推进数据库迁移或 API 落地',
            'reason': '这些属于工程化阶段，当前阶段是真实试运行验证',
        },
        {
            'id': 'avoid-new-analyst-batch',
            'title': '不要在本轮大批量增加分析师白名单',
            'reason': '先把现有 9 条记录质量问题修好，再扩白名单才有意义',
        },
    ]

    # ── 条件触发动作 ──────────────────────────────────
    conditional_actions = [
        {
            'condition': '收到 2026-03 数据文件',
            'action': '月度数据导入',
            'commands': [
                'python3 scripts/import_monthly_data.py --dry-run',
                '# 确认扫描结果后',
                'python3 scripts/import_monthly_data.py --confirm',
                'python3 scripts/sync_after_review.py --confirm',
                'python3 scripts/smoke_test.py --fast',
            ],
            'verify': [
                '检查 reports/run-summary.json dataFreshness.blocked == false',
                '确认 deposit/loan/rate observedAt 已更新为 2026-03',
            ],
        },
        {
            'condition': 'analyst 抓取网络恢复',
            'action': '重新抓取分析师观点',
            'commands': [
                'python3 scripts/fetch_analyst_articles.py',
                'python3 scripts/build_analyst_opinions.py',
            ],
            'verify': [
                '检查 data/processed/analyst_opinions.json records 中有效记录 ≥3 条',
                '检查无乱码标题',
            ],
        },
        {
            'condition': '邱非对 pending 项拍板',
            'action': '决策后同步',
            'commands': [
                'python3 scripts/record_review.py <itemId> <decision> [editedText]',
                'python3 scripts/sync_after_review.py --confirm',
                'python3 scripts/smoke_test.py --fast',
            ],
            'verify': [
                '确认 tracking-items.json 状态已更新',
                '确认周报第九+十节数据一致',
                '确认 bundle 已同步',
            ],
        },
        {
            'condition': '每周一（周报前）',
            'action': '周前检查清单',
            'commands': [
                'python3 scripts/smoke_test.py --fast',
                'python3 scripts/smoke_test.py --pending-aging',
                '# 检查 run-summary readiness 分级',
                'cat reports/run-summary.json | python3 -c "import json,sys; r=json.load(sys.stdin); print(r.get(\"verdictText\"))"',
            ],
            'verify': [
                'fast-check 全 PASS',
                'reportPrepReadiness.level != not_ready',
                '所有阻塞项已处理',
            ],
        },
    ]

    # ── 组装产物 ────────────────────────────────────────
    dashboard = {
        'generatedAt': now.isoformat(),
        'reportPrepReadiness': readiness.get('reportPrepReadiness', {}).get('level', 'unknown') if readiness else 'unknown',
        'internalDiscussionReadiness': readiness.get('internalDiscussionReadiness', {}).get('level', 'unknown') if readiness else 'unknown',
        'browseReadiness': readiness.get('browseReadiness', {}).get('level', 'unknown') if readiness else 'unknown',
        'blocking': blocking,
        'mustDo': must_do,
        'avoid': avoid,
        'conditionalActions': conditional_actions,
        'dataFreshness': {
            'deposit': deposit_fresh,
            'loan': loan_fresh,
            'rate': rate_fresh,
        },
        'analystQuality': {
            'valid': len(ao_valid),
            'garbled': len(ao_garbled),
            'placeholder': len(ao_placeholder),
            'verdict': 'insufficient' if len(ao_valid) < 3 else ('partial' if len(ao_valid) < 5 else 'adequate'),
        },
        'pendingSummary': {
            'total': len(pending_items),
            'byCategory': {},
        },
    }

    # 写 JSON
    REPORTS.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS / 'ops-dashboard.json'
    json_path.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2), encoding='utf-8')

    # 写 Markdown
    rl_icon = {'ready': '✅', 'limited': '⚠️', 'restricted': '⚠️', 'not_ready': '❌', 'blocked': '❌'}
    rl_name = {
        'browseReadiness': '浏览可用性',
        'internalDiscussionReadiness': '内部讨论可用性',
        'reportPrepReadiness': '汇报前准备可用性',
    }

    md_lines = [f'# 对公 AI 雷达站 — 运营行动面板', f'', f'**生成时间:** {now.strftime("%Y-%m-%d %H:%M UTC")}', f'']

    md_lines += ['## 当前可用性分级', '']
    if readiness:
        for key, name in rl_name.items():
            info = readiness.get(key, {})
            icon = rl_icon.get(info.get('level', '?'), '?')
            md_lines.append(f'**{icon} {name}:** {info.get("verdictText", "")}')
            if info.get('blockers'):
                for b in info['blockers']:
                    md_lines.append(f'  - {b}')
            md_lines.append(f'  → {info.get("recommendation", "")}')
            md_lines.append('')
    else:
        md_lines.append('*（run-summary.json 不存在，无法读取 readiness 分级）*')

    md_lines += ['## 本周阻塞项', '']
    if blocking:
        sev_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡'}
        for item in blocking:
            icon = sev_icon.get(item.get('severity', 'medium'), '⚪')
            md_lines.append(f'### {icon} {item["title"]}')
            md_lines.append(f'{item.get("description", "")}')
            md_lines.append(f'**负责方:** {item.get("owner", "未知")}')
            md_lines.append(f'**建议动作:** {item.get("action", "")}')
            md_lines.append('')
    else:
        md_lines.append('✅ 无阻塞项，系统可正常推进。')
        md_lines.append('')

    md_lines += ['## 本周必须动作', '']
    if must_do:
        prio_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        for item in must_do:
            icon = prio_icon.get(item.get('priority', 'medium'), '⚪')
            md_lines.append(f'### {icon} {item["title"]}')
            md_lines.append(f'{item.get("description", "")}')
            if item.get('steps'):
                md_lines.append('**执行步骤:**')
                for s in item['steps']:
                    md_lines.append(f'  {s}')
            md_lines.append(f'**触发条件:** {item.get("trigger", "随时可执行")}')
            md_lines.append('')
    else:
        md_lines.append('✅ 无积压必须动作。')
        md_lines.append('')

    md_lines += ['## 本周不必做的事', '']
    for item in avoid:
        md_lines.append(f'### ⛔ {item["title"]}')
        md_lines.append(f'{item["reason"]}')
        md_lines.append('')

    md_lines += ['## 条件触发动作', '']
    for cond in conditional_actions:
        md_lines.append(f'### 📋 条件：{cond["condition"]}')
        md_lines.append(f'**动作：** {cond["action"]}')
        md_lines.append('**命令序列:**')
        for cmd in cond.get('commands', []):
            md_lines.append(f'    {cmd}')
        md_lines.append('**验证要点:**')
        for v in cond.get('verify', []):
            md_lines.append(f'  - {v}')
        md_lines.append('')

    md_lines += ['## 数据新鲜度', '']
    md_lines.append(f'- deposit benchmark: {deposit_fresh or "未知"}')
    md_lines.append(f'- loan benchmark: {loan_fresh or "未知"}')
    md_lines.append(f'- loan rate: {rate_fresh or "未知"}')
    md_lines.append('')

    md_lines += ['## Analyst 层质量', '']
    md_lines.append(f'- 有效记录: {len(ao_valid)} 条')
    md_lines.append(f'- 乱码记录: {len(ao_garbled)} 条 {"⚠️ 需修复" if ao_garbled else ""}')
    md_lines.append(f'- 空/占位记录: {len(ao_placeholder)} 条 {"⚠️ 需替换" if ao_placeholder else ""}')
    verdict_txt = {'adequate': '✅ 充足', 'partial': '⚠️ 部分可用', 'insufficient': '❌ 不足'}
    md_lines.append(f'- 判定: {verdict_txt.get(dashboard["analystQuality"]["verdict"], "?")}（目标 ≥5 条有效）')
    md_lines.append('')

    md_path = REPORTS / 'ops-dashboard.md'
    md_path.write_text('\n'.join(md_lines), encoding='utf-8')

    # ── 打印摘要 ───────────────────────────────────────
    rl = readiness
    print(f'运营行动面板已生成：')
    print(f'  JSON: {json_path}')
    print(f'  MD:   {md_path}')
    print()
    print(f'【当前 readiness 分级】')
    if rl:
        for key, name in rl_name.items():
            info = rl.get(key, {})
            icon = rl_icon.get(info.get('level', '?'), '?')
            print(f'  {icon} {name}: {info.get("verdictText", "")}')
    print()
    print(f'【本周阻塞项】: {len(blocking)} 项')
    for b in blocking:
        sev = b.get('severity', '?')
        print(f'  [{sev}] {b["title"]}')
    print()
    print(f'【本周必须动作】: {len(must_do)} 项')
    for m in must_do:
        print(f'  [{m.get("priority","?")}] {m["title"]}')
    print()
    print(f'【本周不必做】: {len(avoid)} 项')
    for a in avoid:
        print(f'  ⛔ {a["title"]}')
    print()
    print(f'【条件触发动作】: {len(conditional_actions)} 个条件')


if __name__ == '__main__':
    main()
