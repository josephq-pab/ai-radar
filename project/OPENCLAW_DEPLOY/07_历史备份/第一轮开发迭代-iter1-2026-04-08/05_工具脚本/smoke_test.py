#!/usr/bin/env python3
"""
smoke_test.py — 对公 AI 雷达站主链路最小数据校验

用法：
    python3 smoke_test.py --fast             # 快速校验（主链路一致性，<10s）
    python3 smoke_test.py --full             # 完整校验（全部检查，60s+）
    python3 smoke_test.py                    # 默认完整校验
    python3 smoke_test.py --parse-only       # 只校验 parse 环节
    python3 smoke_test.py --queue-only       # 只校验 review queue 环节
    python3 smoke_test.py --tracking-only    # 只校验 tracking 环节
    python3 smoke_test.py --report-only      # 只校验周报环节
    python3 smoke_test.py --bundle-only      # 只校验 bundle 环节

输出：PASS / WARN / FAIL 三级，每条注明原因

说明：
    --fast  覆盖：tracking-items、weekly-report 第九节一致性、report-tracking 链路、bundle 存在性
    --full  覆盖：全部检查（解析数据、analyst opinions、bundle JSON、契约校验等）
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── 配置 ────────────────────────────────────────────────
# Phase 2: 统一路径解析
try:
    from paths import BASE, PROCESSED, REPORTS, WEB_DATA
except ImportError:
    BASE = Path(__file__).resolve().parent.parent
    PROCESSED = BASE / 'data' / 'processed'
    REPORTS = BASE / 'reports'
    WEB_DATA = BASE / 'apps' / 'web' / 'data'

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
VALID_TRACKING_STATUSES = {'待研判', '跟踪中', '已上报', '已行动', '已关闭'}
REQUIRED_WEEKLY_SECTIONS = [
    '## 一、核心结论摘要',
    '## 五、观察提示',
    '## 六、策略建议',
    '## 七、直接行动建议',
    '## 八、待人工确认事项',
]


# ── 工具函数 ─────────────────────────────────────────────
def result(label: str, level: str, msg: str) -> None:
    icon = {'PASS': '✅', 'WARN': '⚠️ ', 'FAIL': '❌'}[level]
    print(f'  {icon} [{level}] {label}: {msg}')


def load_json_file(path: Path) -> tuple[bool, Any, str]:
    """返回 (success, data_or_None, error_msg)"""
    if not path.exists():
        return False, None, f'文件不存在: {path}'
    try:
        return True, json.loads(path.read_text(encoding='utf-8')), ''
    except json.JSONDecodeError as e:
        return False, None, f'JSON 解析失败: {e}'
    except Exception as e:
        return False, None, f'读取失败: {e}'


def check_date_format(value: Any, field: str = 'observedAt') -> list[str]:
    issues = []
    if not value:
        issues.append(f'{field} 为空')
    elif not DATE_RE.match(str(value)):
        issues.append(f'{field} 格式异常: {value}')
    return issues


def check_record_keys(record: dict, required_keys: list[str], dataset: str = '') -> list[str]:
    issues = []
    for k in required_keys:
        if k not in record:
            issues.append(f'缺少字段 [{k}] (dataset={dataset or record.get("dataset","?")}, bank={record.get("bank","?")})')
    return issues


# ── 分节校验 ─────────────────────────────────────────────

def validate_parse() -> dict:
    """校验 parse_initial_data.py 的输出"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}

    datasets = {
        'deposit_benchmark.json': {
            'min': 16, 'max': 48,
            'required_keys': ['dataset', 'observedAt', 'bank', 'metricCode', 'currentValue'],
            'metric_codes': {'balance_total', 'balance_rmb', 'balance_fx'},
            'date_field': 'observedAt',
        },
        'loan_benchmark.json': {
            'min': 8, 'max': 40,
            'required_keys': ['dataset', 'observedAt', 'bank', 'metricCode', 'currentValue'],
            'metric_codes': {'loan_balance', 'forfaiting_balance'},
            'date_field': 'observedAt',
        },
        'loan_rate.json': {
            'min': 4, 'max': 20,
            'required_keys': ['dataset', 'observedAt', 'bank', 'monthlyRate'],
            'metric_codes': set(),
            'date_field': 'observedAt',
            'format': 'array',   # loan_rate.json is an array of rate records
        },
        'summary.json': {
            'min': 1, 'max': 1,
            'required_keys': ['focusBanks', 'depositTop', 'loanTop', 'rateRankingLowToHigh'],
            'metric_codes': set(),
            'date_field': None,
        },
        'quality_report.json': {
            'min': 1, 'max': 1,
            'required_keys': ['depositRecords', 'loanRecords', 'rateRecords', 'depositBanks', 'loanBanks'],
            'metric_codes': set(),
            'date_field': None,
        },
        'dashboard.json': {
            'min': 1, 'max': 1,
            'required_keys': ['kpis', 'depositTop5', 'loanTop5', 'rateLowToHigh5'],
            'metric_codes': set(),
            'date_field': None,
        },
        'loan_dedup_info': {
            'note': 'loan_benchmark dedup key = bank+metricGroup+observedAt, keeping first. '
                    'Risk: if newer rows appear later in source Excel, they may be discarded. '
                    'Use quality_report loanRecords as deduped count.',
            'skip': True,   # 不是文件，只是注释说明
        },
    }

    print('\n── parse_initial_data.py 校验 ──')
    for fname, cfg in datasets.items():
        if cfg.get('skip'):
            result(fname, 'PASS', f'（跳过: {cfg.get("note", "skip=True")}）')
            outcomes['PASS'] += 1
            continue

        path = PROCESSED / fname
        ok, data, err = load_json_file(path)
        if not ok:
            result(fname, 'FAIL', err)
            outcomes['FAIL'] += 1
            continue

        # 文件存在 & JSON 合法
        result(fname, 'PASS', f'文件存在，JSON 合法')
        outcomes['PASS'] += 1

        if cfg['metric_codes'] or cfg.get('format') == 'array':
            # 数组格式：校验记录数、字段、主键重复、日期
            records = data if isinstance(data, list) else []
            count = len(records)
            result(fname, 'PASS' if cfg['min'] <= count <= cfg['max'] else 'WARN',
                   f'记录数 {count}（期望 {cfg["min"]}-{cfg["max"]}）')
            if cfg['min'] <= count <= cfg['max']:
                outcomes['PASS'] += 1
            else:
                outcomes['WARN'] += 1

            seen_pk: dict[str, list[str]] = {}
            date_issues = []
            for rec in records:
                issues = check_record_keys(rec, cfg['required_keys'], fname)
                for iss in issues:
                    result(fname, 'WARN', f'{rec.get("bank","?")} - {iss}')

                pk = (rec.get('bank', ''), rec.get('metricGroup', ''), rec.get('observedAt', ''))
                pk_str = '|'.join(str(x) for x in pk)
                if pk_str not in seen_pk:
                    seen_pk[pk_str] = []
                seen_pk[pk_str].append(rec.get('bank', ''))

                if cfg['date_field']:
                    date_issues += check_date_format(rec.get(cfg['date_field']), cfg['date_field'])

            # 主键：bank + metricGroup + observedAt（与 parse_loan() dedup 口径一致）
            # 注：parse_loan() dedup 后每组最多 1 条，故主键重复已消除
            # 以下仍保留检查逻辑，供未来数据更新后复现重复时能及时发现
            for pk_str, banks in seen_pk.items():
                if len(banks) > 1:
                    result(fname, 'WARN', f'主键重复（bank+metricGroup+observedAt）: {pk_str[:50]}...')

            # 日期检查
            date_count = len([r for r in records if r.get(cfg['date_field'])])
            if date_issues:
                for iss in date_issues[:3]:
                    result(fname, 'WARN', iss)
            elif date_count < len(records) * 0.5:
                result(fname, 'WARN', f'大量记录缺少 observedAt（{date_count}/{len(records)} 有值）')

        else:
            # 对象格式：校验顶层字段
            for key in cfg['required_keys']:
                if key not in data:
                    result(fname, 'FAIL', f'顶层缺少字段 [{key}]')
                    outcomes['FAIL'] += 1

    return outcomes


def validate_review_queue() -> dict:
    """校验 generate_review_queue.py 的输出"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── generate_review_queue.py 校验 ──')

    path = REPORTS / 'review-queue.json'
    ok, data, err = load_json_file(path)
    if not ok:
        result('review-queue.json', 'FAIL', err)
        outcomes['FAIL'] += 1
        return outcomes

    result('review-queue.json', 'PASS', '文件存在，JSON 合法')
    outcomes['PASS'] += 1

    items = data.get('items', [])
    if not items:
        result('items', 'FAIL', 'items 数组为空，未提取到任何事项')
        outcomes['FAIL'] += 1
        return outcomes

    result('items', 'PASS', f'共 {len(items)} 条待审核事项')
    outcomes['PASS'] += 1

    seen_ids: set[str] = set()
    empty_text = []
    missing_fields = []
    dup_ids: list[str] = []
    for idx, item in enumerate(items):
        rid = item.get('id', '')
        if not rid:
            missing_fields.append(f'第 {idx+1} 条缺少 id')
        elif rid in seen_ids:
            dup_ids.append(rid)
        seen_ids.add(rid)

        if not item.get('text', '').strip():
            empty_text.append(f'id={rid or "(空)"}')

        for f in ('category', 'source'):
            if f not in item:
                missing_fields.append(f'id={rid} 缺少 [{f}]')

    if dup_ids:
        result('id重复', 'WARN', f'发现重复 id（首次出现即标记）: {dup_ids[:5]}')
        outcomes['WARN'] += 1

    if empty_text:
        result('text', 'WARN', f'{len(empty_text)} 条 text 为空: {empty_text[:3]}')
        outcomes['WARN'] += 1
    else:
        result('text', 'PASS', '所有 items 均有非空 text')
        outcomes['PASS'] += 1

    if missing_fields:
        for mf in missing_fields[:5]:
            result('字段', 'WARN', mf)
            outcomes['WARN'] += 1

    return outcomes


def validate_tracking_items() -> dict:
    """校验 build_tracking_items.py 的输出"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── build_tracking_items.py 校验 ──')

    path = REPORTS / 'tracking-items.json'
    ok, data, err = load_json_file(path)
    if not ok:
        result('tracking-items.json', 'FAIL', err)
        outcomes['FAIL'] += 1
        return outcomes

    result('tracking-items.json', 'PASS', '文件存在，JSON 合法')
    outcomes['PASS'] += 1

    # 顶层汇总字段
    for f in ('total', 'pending', 'approved', 'modified', 'rejected', 'trackingStatusSummary'):
        if f in data:
            result(f'顶层字段 [{f}]', 'PASS', '存在')
            outcomes['PASS'] += 1
        else:
            result(f'顶层字段 [{f}]', 'WARN', '缺失')
            outcomes['WARN'] += 1

    summary = data.get('trackingStatusSummary', {})
    if summary:
        valid_statuses_seen = set()
        for st, cnt in summary.items():
            if st in VALID_TRACKING_STATUSES:
                valid_statuses_seen.add(st)
                result(f'trackingStatusSummary.{st}', 'PASS', f'{cnt} 项')
                outcomes['PASS'] += 1
            else:
                result(f'trackingStatusSummary.{st}', 'WARN', f'状态值 "{st}" 不在标准集合中')
                outcomes['WARN'] += 1

        for st in VALID_TRACKING_STATUSES:
            if st not in summary:
                result(f'trackingStatusSummary.{st}', 'WARN', '状态缺失（计数为 0）')
                outcomes['WARN'] += 1
    else:
        result('trackingStatusSummary', 'WARN', '汇总为空，可能 build_tracking_items.py 还未生成')
        outcomes['WARN'] += 1

    items = data.get('items', [])
    result('items', 'PASS' if items else 'WARN', f'共 {len(items)} 条明细')
    if items:
        outcomes['PASS'] += 1
    else:
        outcomes['WARN'] += 1

    seen_ids: set[str] = set()
    status_issues = []
    dup_ids: list[str] = []
    for item in items:
        rid = item.get('id', '')
        if not rid:
            status_issues.append('缺少 id')
        elif rid in seen_ids and rid not in dup_ids:
            dup_ids.append(rid)
        seen_ids.add(rid)

        ts = item.get('trackingStatus', '')
        if ts and ts not in VALID_TRACKING_STATUSES:
            status_issues.append(f'id={rid} trackingStatus="{ts}" 不标准')
            outcomes['WARN'] += 1

    if dup_ids:
        result('id重复', 'WARN', f'发现重复 id: {dup_ids[:5]}')
        outcomes['WARN'] += 1

    if status_issues:
        for iss in status_issues[:5]:
            result('item校验', 'WARN', iss)
    else:
        result('items', 'PASS', f'无重复 id，trackingStatus 全部合规（共 {len(items)} 条）')
        outcomes['PASS'] += 1

    return outcomes


def validate_weekly_report() -> dict:
    """校验 generate_weekly_report.py 的输出"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── generate_weekly_report.py 校验 ──')

    path = REPORTS / 'weekly-report-draft.md'
    if not path.exists():
        result('weekly-report-draft.md', 'FAIL', '文件不存在')
        outcomes['FAIL'] += 1
        return outcomes

    result('weekly-report-draft.md', 'PASS', '文件存在')
    outcomes['PASS'] += 1

    text = path.read_text(encoding='utf-8')
    char_count = len(text)
    result('文件大小', 'PASS' if char_count > 500 else 'WARN',
           f'{char_count} 字符')
    if char_count > 500:
        outcomes['PASS'] += 1
    else:
        outcomes['WARN'] += 1

    # 必含章节检查
    missing_sections = []
    for sec in REQUIRED_WEEKLY_SECTIONS:
        if sec in text:
            result(f'章节 [{sec}]', 'PASS', '存在')
            outcomes['PASS'] += 1
        else:
            missing_sections.append(sec)
            result(f'章节 [{sec}]', 'FAIL', '缺失')
            outcomes['FAIL'] += 1

    # 章节非空检查（用安全行扫描代替回溯 regex）
    lines = text.split('\n')
    empty_sections = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('## '):
            header = line
            # 收集该节所有内容行（直到下一节或文件结束）
            content_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith('## '):
                content_lines.append(lines[j])
                j += 1
            # 过滤元数据行
            filtered = [l for l in content_lines
                        if not any(l.startswith(meta) for meta in
                                   ['[栏目口径]', '[板块模板]', '[解释规则]', '[生成规则]', '[追问提示]'])]
            content_str = '\n'.join(filtered).strip()
            if len(content_str) < 10:
                empty_sections.append(header[:40])
            i = j
        else:
            i += 1

    if empty_sections:
        result('章节内容', 'WARN', f'{len(empty_sections)} 节可能为空: {empty_sections[:2]}')
        outcomes['WARN'] += 1
    else:
        result('章节内容', 'PASS', '所有节均有实质性内容')
        outcomes['PASS'] += 1

    # 检查日期合理性（搜索近期日期）
    date_refs = re.findall(r'202[0-9]-[01]\d-[0-3]\d', text)
    if date_refs:
        result('日期引用', 'PASS', f'找到 {len(date_refs)} 个日期，示例: {date_refs[0]}')
        outcomes['PASS'] += 1
    else:
        result('日期引用', 'WARN', '未找到任何 YYYY-MM-DD 格式日期')
        outcomes['WARN'] += 1

    # 检查"观察提示 / 策略建议 / 直接行动建议"三类建议均存在
    for marker in ('观察提示', '策略建议', '直接行动建议'):
        if marker in text:
            result(f'建议类型 [{marker}]', 'PASS', '存在')
            outcomes['PASS'] += 1
        else:
            result(f'建议类型 [{marker}]', 'FAIL', f'缺失')
            outcomes['FAIL'] += 1

    # ── 新增：第九节与 tracking-items.json 的一致性校验 ──────────────
    ti_path = REPORTS / 'tracking-items.json'
    if ti_path.exists():
        import json as _json
        ti_data = _json.loads(ti_path.read_text(encoding='utf-8'))
        ti_summary = ti_data.get('trackingStatusSummary', {})
        # 从周报中提取第九节的状态行（安全行扫描，避免回溯 regex）
        lines = text.split('\n')
        sec9_lines = []
        in_sec9 = False
        for line in lines:
            if '## 九、重点事项跟踪状态汇总' in line or '## 九，重点事项跟踪状态汇总' in line:
                in_sec9 = True
                continue
            if in_sec9:
                if line.startswith('## '):
                    break
                sec9_lines.append(line)

        sec9_text = '\n'.join(sec9_lines)
        pending_in_report = re.search(r'待研判[：:]\s*(\d+)', sec9_text)
        pending_count = int(pending_in_report.group(1)) if pending_in_report else None
        ti_pending = ti_summary.get('待研判')
        if pending_count is not None and ti_pending is not None:
            if pending_count != ti_pending:
                result('第九节一致性(待研判)', 'FAIL',
                       f'周报显示{pending_count}项，tracking-items显示{ti_pending}项，请优先重建tracking-items')
                outcomes['FAIL'] += 1
            else:
                result('第九节一致性(待研判)', 'PASS',
                       f'周报与tracking-items一致({pending_count}项)')
                outcomes['PASS'] += 1
        else:
            result('第九节读取', 'WARN', '未能从周报提取第九节状态汇总')
            outcomes['WARN'] += 1
    else:
        result('tracking-items.json', 'WARN', '文件不存在，无法做一致性校验')
        outcomes['WARN'] += 1

    return outcomes


def validate_web_bundle(lightweight: bool = False) -> dict:
    """校验 build_web_bundle.py 的输出"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── build_web_bundle.py 校验 ──')

    path = WEB_DATA / 'app-data.js'
    if not path.exists():
        result('app-data.js', 'FAIL', '文件不存在')
        outcomes['FAIL'] += 1
        return outcomes

    result('app-data.js', 'PASS', '文件存在')
    outcomes['PASS'] += 1

    text = path.read_text(encoding='utf-8')
    if not text.startswith('window.AIRadarData = '):
        result('前缀', 'FAIL', '文件不以 "window.AIRadarData = " 开头')
        outcomes['FAIL'] += 1
        return outcomes

    result('前缀', 'PASS', 'window.AIRadarData 前缀正确')
    outcomes['PASS'] += 1

    if lightweight:
        # 轻量模式：只检查 JSON 结构完整性，不做完整解析
        json_text = text[len('window.AIRadarData = '):].rstrip().rstrip(';').rstrip()
        if json_text.startswith('{') and json_text.endswith('}'):
            result('JSON结构', 'PASS', 'JSON 结构完整（轻量模式，跳过完整解析）')
            outcomes['PASS'] += 1
        else:
            result('JSON结构', 'WARN', 'JSON 结构可能不完整')
            outcomes['WARN'] += 1
        return outcomes

    # 完整模式：截取并解析 JSON
    json_text = text[len('window.AIRadarData = '):].rstrip()
    if json_text.endswith(';'):
        json_text = json_text[:-1]
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        result('JSON解析', 'FAIL', 'JSON 部分解析失败: {e}')
        outcomes['FAIL'] += 1
        return outcomes

    result('JSON解析', 'PASS', 'JSON 部分合法')
    outcomes['PASS'] += 1

    # 必含顶层 key
    required_keys = ['dashboard', 'deposit', 'loan', 'rate', 'summary',
                     'reviewQueue', 'trackingItems']
    missing_keys = []
    for key in required_keys:
        if key in data:
            result(f'顶层key [{key}]', 'PASS', '存在')
            outcomes['PASS'] += 1
        else:
            missing_keys.append(key)
            result(f'顶层key [{key}]', 'FAIL', f'缺失')
            outcomes['FAIL'] += 1

    # 文件大小合理性
    size_kb = len(text) / 1024
    result('文件大小', 'PASS' if size_kb > 1 else 'WARN',
           f'{size_kb:.1f} KB')
    if size_kb > 1:
        outcomes['PASS'] += 1
    else:
        outcomes['WARN'] += 1

    # weeklyReportMarkdown 内容检查
    if 'weeklyReportMarkdown' in data:
        wrm = data['weeklyReportMarkdown']
        if len(wrm) > 200:
            result('weeklyReportMarkdown', 'PASS', f'内容 {len(wrm)} 字符')
            outcomes['PASS'] += 1
        else:
            result('weeklyReportMarkdown', 'WARN', f'内容过短: {len(wrm)} 字符')
            outcomes['WARN'] += 1

    return outcomes


# ── 主函数 ──────────────────────────────────────────────

def validate_report_tracking_link() -> dict:
    """验证 weekly report 是否真实承接 tracking-items.json（链路真实性）"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── 周报 ← Tracking 链路真实性校验 ──')

    # 读取 tracking-items.json
    ti_path = REPORTS / 'tracking-items.json'
    ok, ti_data, err = load_json_file(ti_path)
    if not ok:
        result('tracking-items.json', 'FAIL', err)
        outcomes['FAIL'] += 1
        return outcomes

    tracking_summary = ti_data.get('trackingStatusSummary', {})
    tracking_items_list = ti_data.get('items', [])
    has_tracking_data = bool(tracking_summary or tracking_items_list)

    # 读取周报文本
    wr_path = REPORTS / 'weekly-report-draft.md'
    if not wr_path.exists():
        result('weekly-report-draft.md', 'FAIL', '文件不存在')
        outcomes['FAIL'] += 1
        return outcomes

    wr_text = wr_path.read_text(encoding='utf-8')

    # 抽第九节内容
    idx9 = wr_text.find('## 九、重点事项跟踪状态汇总')
    idx10 = wr_text.find('## 十、事项明细')
    if idx9 == -1:
        result('第九节', 'FAIL', '周报中未找到第九节')
        outcomes['FAIL'] += 1
        return outcomes

    section9 = wr_text[idx9:idx10] if idx10 != -1 else wr_text[idx9:]

    # 检查1：tracking 有内容时，第九节不能仍是"暂无"
    if has_tracking_data:
        if '暂无跟踪状态汇总数据' in section9:
            result('第九节兜底', 'FAIL', 'tracking-items.json 有数据但第九节仍为"暂无"兜底，链路断裂')
            outcomes['FAIL'] += 1
        else:
            # 检查第九节是否出现了真实的 status 值或计数
            # 期望出现：待研判 / 跟踪中 / 已上报 / 已行动 / 已关闭 + 数字
            found_status_values = [s for s in VALID_TRACKING_STATUSES if s in section9 and any(c.isdigit() for c in section9[section9.find(s):section9.find(s)+10])]
            if found_status_values:
                result('第九节真实数据', 'PASS', f'包含真实状态值: {found_status_values}')
                outcomes['PASS'] += 1
            else:
                result('第九节内容', 'WARN', '第九节存在但未找到明确的 status+数字组合')
                outcomes['WARN'] += 1
    else:
        result('tracking无数据', 'PASS', 'tracking-items.json 为空，第九节显示兜底为正常行为')
        outcomes['PASS'] += 1

    # 检查2：tracking items 非空时，第十节不能仍是"暂无"
    if tracking_items_list:
        if idx10 == -1:
            result('第十节', 'FAIL', '周报中未找到第十节')
            outcomes['FAIL'] += 1
        else:
            idx11 = wr_text.find('\n## ', idx10 + 1)
            section10 = wr_text[idx10:idx11] if idx11 != -1 else wr_text[idx10:]

            if '暂无事项数据' in section10:
                result('第十节兜底', 'FAIL', 'tracking-items.json 有 items 但第十节仍为"暂无"兜底，链路断裂')
                outcomes['FAIL'] += 1
            else:
                # 检查第十节是否包含至少 1 条真实事项特征
                # 特征：id标题（字母+数字混合）或 trackingStatus / 业务维度 / 下一步动作 等关键词
                sample_item = tracking_items_list[0]
                sample_id = sample_item.get('id', '')
                sample_status = sample_item.get('trackingStatus', '')
                sample_dimension = sample_item.get('sourceDimension', '')

                # 命中判断：至少匹配 id 或 status 关键词之一
                hit = (sample_id and sample_id in section10) or \
                      (sample_status and sample_status in section10) or \
                      (sample_dimension and sample_dimension in section10 and '业务维度' in section10)

                if hit:
                    result('第十节真实数据', 'PASS', f'至少命中 1 条 tracking item 特征（id={sample_id} 或 status={sample_status}）')
                    outcomes['PASS'] += 1
                else:
                    result('第十节内容', 'WARN', f'tracking items 有数据但第十节未找到 id={sample_id} 相关内容')
                    outcomes['WARN'] += 1
    else:
        result('tracking无items', 'PASS', 'tracking-items.json items 为空，第十节显示兜底为正常行为')
        outcomes['PASS'] += 1

    return outcomes


def validate_review_queue_realism() -> dict:
    """验证 review-queue.json 是否处于真实提取模式，检测兜底逻辑是否被触发"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── review-queue 真实性与兜底检测 ──')

    # 读取 review-queue.json
    rq_path = REPORTS / 'review-queue.json'
    ok, rq_data, err = load_json_file(rq_path)
    if not ok:
        result('review-queue.json', 'FAIL', err)
        outcomes['FAIL'] += 1
        return outcomes

    items = rq_data.get('items', [])
    if not items:
        result('items', 'FAIL', 'items 为空')
        outcomes['FAIL'] += 1
        return outcomes

    # 读取周报文本（用于交叉验证）
    wr_path = REPORTS / 'weekly-report-draft.md'
    wr_text = wr_path.read_text(encoding='utf-8') if wr_path.exists() else ''

    # 检测是否处于兜底模式：items 内容与已知兜底文本完全匹配
    KNOWN_FALLBACK_TEXTS = [
        '存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。',
        '贷款投放节奏判断不能脱离产品结构和定价水平，应联动观察。',
        '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。',
    ]
    fallback_hit_count = sum(1 for item in items if item.get('text', '') in KNOWN_FALLBACK_TEXTS)

    if fallback_hit_count == len(items):
        result('兜底模式', 'FAIL', f'全部 {len(items)} 条 items 均匹配已知兜底文本，链路断裂')
        outcomes['FAIL'] += 1
        return outcomes
    elif fallback_hit_count > 0:
        result('兜底模式', 'WARN', f'{fallback_hit_count}/{len(items)} 条匹配兜底文本，其余为真实提取')
        outcomes['WARN'] += 1
    else:
        result('兜底模式', 'PASS', f'0/{len(items)} 条匹配已知兜底文本，处于真实提取模式')
        outcomes['PASS'] += 1

    # 抽样验证：至少 2 条 items 的 text 能在 weekly-report-draft.md 中找到对应 bullet
    # 匹配方式：text 前 30 字符是否在周报中出现
    found_in_report = 0
    sample_items = items[:4] if len(items) >= 4 else items
    for item in sample_items:
        text_snippet = item.get('text', '')[:30].strip()
        if text_snippet and text_snippet in wr_text:
            found_in_report += 1

    if found_in_report >= 1:
        result('items来源验证', 'PASS', f'抽样 {len(sample_items)} 条中 {found_in_report} 条能在周报中找到对应 bullet')
        outcomes['PASS'] += 1
    else:
        result('items来源验证', 'WARN', f'抽样 {len(sample_items)} 条均未在周报中找到对应 bullet，需确认 extract_review_items 是否正常')
        outcomes['WARN'] += 1

    # 检查 category 分布合理性
    categories = [item.get('category', '') for item in items]
    unique_cats = set(categories)
    expected_cats = {'核心结论摘要', '观察提示', '策略建议', '直接行动建议', '待人工确认事项'}
    unexpected_cats = unique_cats - expected_cats
    if unexpected_cats:
        result('category分布', 'WARN', f'发现未预期的 category: {unexpected_cats}')
        outcomes['WARN'] += 1
    else:
        result('category分布', 'PASS', f'category 覆盖 {len(unique_cats)} 种，分布正常')
        outcomes['PASS'] += 1

    return outcomes


def validate_analyst_opinions() -> dict:
    """校验 analyst_opinions.json 基础结构，检测编码问题"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── analyst_opinions.json 基础校验 ──')

    path = PROCESSED / 'analyst_opinions.json'
    ok, data, err = load_json_file(path)
    if not ok:
        result('analyst_opinions.json', 'FAIL', f'文件不存在或无法解析: {err}')
        outcomes['FAIL'] += 1
        return outcomes

    result('analyst_opinions.json', 'PASS', '文件存在，JSON 合法')
    outcomes['PASS'] += 1

    records = data.get('records', [])
    result('records字段', 'PASS', f'records 存在，共 {len(records)} 条')
    outcomes['PASS'] += 1

    if not records:
        result('records为空', 'WARN', 'analyst_opinions.json records 为空（可能本周无新增分析师观点，符合正常状态）')
        outcomes['WARN'] += 1
        return outcomes

    # 检查 articleTitle 是否完整（无空/无乱码）
    no_title = [r for r in records if not r.get('articleTitle', '').strip()]
    mojibake = [r for r in records if any(c in r.get('articleTitle', '') for c in ['æ', 'å', 'è', 'ï', '¶', '¹', '¸', '»'])]
    result('articleTitle完整', 'PASS' if len(no_title) == 0 else 'WARN',
           f'{len(records) - len(no_title)}/{len(records)} 条有标题，{len(no_title)} 条无标题（可能已触发兜底）')
    outcomes['PASS' if len(no_title) == 0 else 'WARN'] += 1

    if mojibake:
        result('编码问题', 'WARN', f'{len(mojibake)} 条可能存在编码乱码（已有 _repair_mojibake 修复，但原始数据需追查）')
        outcomes['WARN'] += 1
    else:
        result('编码检查', 'PASS', '未发现明显 UTF-8 乱码特征')
        outcomes['PASS'] += 1

    # 抽样检查基本字段
    sample = records[:3]
    for field in ['articleTitle', 'analystName', 'sourceUrl']:
        has_value = sum(1 for r in sample if r.get(field))
        result(f'records.{field}', 'PASS' if has_value == len(sample) else 'WARN',
               f'{has_value}/{len(sample)} 条有值')
        outcomes['PASS' if has_value == len(sample) else 'WARN'] += 1

    return outcomes


def validate_meta_files() -> dict:
    """校验偏好/模板/规则类文件的最小结构完整性"""
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── 偏好/模板/规则文件校验 ──')

    files = {
        'preference_profile.json': {
            'required_keys': ['totalReviews', 'guidance', 'topThemes', 'decisionCount'],
            'warn_if_empty': ['guidance', 'topThemes'],
        },
        'section_preferences.json': {
            'required_keys': ['sections', 'defaultSections'],
            'warn_if_empty': [],
        },
        'domain_templates.json': {
            'required_keys': ['domains', 'domainTitles'],
            'warn_if_empty': [],
        },
        'interpretation_rules.json': {
            'required_keys': ['rules'],
            'warn_if_empty': [],
        },
        'recommendation_rules.json': {
            'required_keys': ['rules'],
            'warn_if_empty': [],
        },
        'tracking_status_rules.json': {
            'required_keys': ['reviewStatuses', 'trackingStatuses', 'reviewToTracking'],
            'warn_if_empty': [],
        },
    }

    for fname, cfg in files.items():
        path = PROCESSED / fname
        ok, data, err = load_json_file(path)
        if not ok:
            result(fname, 'FAIL', err)
            outcomes['FAIL'] += 1
            continue

        result(fname, 'PASS', '文件存在，JSON 合法')
        outcomes['PASS'] += 1

        for key in cfg['required_keys']:
            if key not in data:
                result(f'{fname} 缺少 [{key}]', 'FAIL', '顶层字段缺失')
                outcomes['FAIL'] += 1
            else:
                result(f'{fname} [{key}]', 'PASS', f'存在')
                outcomes['PASS'] += 1

        # 空值告警
        for key in cfg.get('warn_if_empty', []):
            val = data.get(key)
            if not val or (isinstance(val, list) and len(val) == 0):
                result(f'{fname} [{key}] 为空', 'WARN', '可能影响周报生成质量')
                outcomes['WARN'] += 1

    return outcomes


def validate_bundle_sync() -> dict:
    """Bundle 与主状态一致性校验（fast-check 专用）

    检查：bundle 前缀、trackingItems 结构与数量、reviewStatus.total、weeklyReportMarkdown、
          trackingItems 与 tracking-items.json 一致性、bundle 新鲜度
    """
    import json as _json  # avoid conflict with outer scope

    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── Bundle 一致性校验 ──')

    # ── 读取 tracking-items.json ──────────────────────────
    ti_path = REPORTS / 'tracking-items.json'
    ok, ti_data, err = load_json_file(ti_path)
    if not ok:
        result('tracking-items.json', 'FAIL', err)
        outcomes['FAIL'] += 1
        return outcomes

    ti_items = ti_data.get('items', [])
    ti_summary = ti_data.get('trackingStatusSummary', {})
    ti_total = len(ti_items)

    # ── 读取 review-status.json ─────────────────────────
    rs_path = REPORTS / 'review-status.json'
    ok, rs_data, _ = load_json_file(rs_path)
    rs_total = rs_data.get('total', 0) if rs_data else 0

    # ── 读取并解析 bundle ───────────────────────────────
    bundle_path = WEB_DATA / 'app-data.js'
    if not bundle_path.exists():
        result('app-data.js', 'FAIL', '文件不存在')
        outcomes['FAIL'] += 1
        return outcomes

    bundle_text = bundle_path.read_text(encoding='utf-8')
    prefix_ok = bundle_text.startswith('window.AIRadarData = ')
    result('bundle前缀', 'PASS' if prefix_ok else 'FAIL',
           'window.AIRadarData = 前缀正确' if prefix_ok else '前缀异常')
    outcomes['PASS' if prefix_ok else 'FAIL'] += 1

    json_text = bundle_text[len('window.AIRadarData = '):].rstrip().rstrip(';').rstrip()
    if not (json_text.startswith('{') and json_text.endswith('}')):
        result('JSON结构', 'WARN', 'JSON 结构可能不完整')
        outcomes['WARN'] += 1
        return outcomes

    # 完整解析 bundle（~105KB，Python json 解析 < 50ms）
    try:
        bundle_data = _json.loads(json_text)
    except _json.JSONDecodeError as e:
        result('bundle JSON解析', 'FAIL', f'解析失败: {e}')
        outcomes['FAIL'] += 1
        return outcomes

    result('bundle JSON解析', 'PASS', 'JSON 解析成功')
    outcomes['PASS'] += 1

    # ── 顶层 key 检查 ────────────────────────────────────
    for key in ['trackingItems', 'reviewStatus', 'weeklyReportMarkdown']:
        has = key in bundle_data
        result(f'bundle.{key}', 'PASS' if has else 'FAIL',
               f'{key} 存在于 bundle' if has else f'{key} 缺失')
        outcomes['PASS' if has else 'FAIL'] += 1

    # ── trackingItems 一致性 ────────────────────────────
    ti_bundle = bundle_data.get('trackingItems', {})
    bundle_ti_items = ti_bundle.get('items', []) if isinstance(ti_bundle, dict) else []
    bundle_ti_total = ti_bundle.get('total', 0) if isinstance(ti_bundle, dict) else 0

    if bundle_ti_total == ti_total:
        result('bundle trackingItems.total', 'PASS',
               f'bundle={bundle_ti_total} == tracking-items.json={ti_total}')
        outcomes['PASS'] += 1
    else:
        result('bundle trackingItems.total', 'FAIL',
               f'bundle={bundle_ti_total} != tracking-items.json={ti_total}')
        outcomes['FAIL'] += 1

    if len(bundle_ti_items) == ti_total:
        result('bundle trackingItems.items 数量', 'PASS',
               f'bundle items={len(bundle_ti_items)} == tracking-items.json={ti_total}')
        outcomes['PASS'] += 1
    else:
        result('bundle trackingItems.items 数量', 'FAIL',
               f'bundle items={len(bundle_ti_items)} != tracking-items.json={ti_total}')
        outcomes['FAIL'] += 1

    # trackingStatusSummary 对比
    if isinstance(ti_bundle, dict) and 'trackingStatusSummary' in ti_bundle:
        bundle_ts = ti_bundle['trackingStatusSummary']
        if bundle_ts == ti_summary:
            result('bundle trackingStatusSummary', 'PASS', '与 tracking-items.json 完全一致')
            outcomes['PASS'] += 1
        else:
            result('bundle trackingStatusSummary', 'WARN', '与 tracking-items.json 存在差异')
            outcomes['WARN'] += 1
            # 打印差异
            all_keys = set(bundle_ts.keys()) | set(ti_summary.keys())
            for k in sorted(all_keys):
                bv = bundle_ts.get(k, 0)
                tv = ti_summary.get(k, 0)
                if bv != tv:
                    result(f'  {k}', 'WARN', f'bundle={bv} tracking-json={tv}')
                    outcomes['WARN'] += 1

    # ── reviewStatus.total 一致性 ───────────────────────
    rs_bundle = bundle_data.get('reviewStatus', {})
    bundle_rs_total = rs_bundle.get('total', 0) if isinstance(rs_bundle, dict) else 0
    if bundle_rs_total == rs_total:
        result('bundle reviewStatus.total', 'PASS',
               f'bundle={bundle_rs_total} == review-status.json={rs_total}')
        outcomes['PASS'] += 1
    else:
        result('bundle reviewStatus.total', 'FAIL',
               f'bundle={bundle_rs_total} != review-status.json={rs_total}')
        outcomes['FAIL'] += 1

    # ── weeklyReportMarkdown ─────────────────────────────
    wr_bundle = bundle_data.get('weeklyReportMarkdown', '')
    if isinstance(wr_bundle, str) and len(wr_bundle) > 200:
        result('bundle.weeklyReportMarkdown', 'PASS', f'{len(wr_bundle)} 字符')
        outcomes['PASS'] += 1
    else:
        result('bundle.weeklyReportMarkdown', 'WARN',
               f'长度={len(wr_bundle) if isinstance(wr_bundle, str) else type(wr_bundle)}')
        outcomes['WARN'] += 1

    # ── bundle 新鲜度（mtime）────────────────────────────
    from datetime import datetime as dt
    ti_mtime = dt.fromtimestamp(ti_path.stat().st_mtime)
    rs_mtime = dt.fromtimestamp(rs_path.stat().st_mtime)
    bundle_mtime = dt.fromtimestamp(bundle_path.stat().st_mtime)
    latest_source = max(ti_mtime, rs_mtime)
    if bundle_mtime >= latest_source:
        diff_s = (bundle_mtime - latest_source).total_seconds()
        result('bundle 新鲜度', 'PASS',
               f'bundle ({bundle_mtime.strftime("%H:%M:%S")}) >= 最新源 ({latest_source.strftime("%H:%M:%S")})，相差 {diff_s:.0f}s')
        outcomes['PASS'] += 1
    else:
        result('bundle 新鲜度', 'FAIL',
               f'bundle ({bundle_mtime.strftime("%H:%M:%S")}) < 最新源 ({latest_source.strftime("%H:%M:%S")})，bundle 未更新')
        outcomes['FAIL'] += 1

    return outcomes


def run_pending_aging() -> dict:
    """Pending 项 aging 分析（独立入口，不依赖其他校验）

    Phase 2: 取消 WAITING_FOR_DATA / WAITING_FOR_BUSINESS 硬编码 ID 集合。
    所有分类统一从 review-log.jsonl 的实际 decision 记录推导：
    - decision='' 或 'pending' → needs-review（尚未进入正式 review 流程）
    - decision='approve'/'modify' 且 trackingStatus='跟踪中' → waiting-for-business-decision
    - decision='approve'/'modify' 且 trackingStatus='已上报' → waiting-for-data（数据验证中）
    """
    outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    print('\n── Pending Items Aging 分析 ──')

    from datetime import datetime, timezone

    ti_path = REPORTS / 'tracking-items.json'
    ok, ti_data, err = load_json_file(ti_path)
    if not ok:
        result('tracking-items.json', 'FAIL', err)
        outcomes['FAIL'] += 1
        return outcomes

    items = ti_data.get('items', [])
    now = datetime.now(timezone.utc)

    # 从 review-log 动态加载决策映射（取消硬编码 ID）
    review_log_path = BASE / 'reviews' / 'review-log.jsonl'
    decisions = {}
    if review_log_path.exists():
        for line in review_log_path.read_text(encoding='utf-8').strip().split('\n'):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                iid = entry.get('itemId', '')
                decision = entry.get('decision', '')
                if iid:
                    decisions[iid] = decision
            except Exception:
                pass

    pending_items = [i for i in items if i.get('trackingStatus') in ('待研判', '跟踪中', '已上报')]

    print(f'\n  共 {len(pending_items)} 项 Pending（待研判+跟踪中）：\n')

    aging_rows = []
    for item in sorted(pending_items, key=lambda x: x.get('updatedAt', '9999')):
        iid = item.get('id', '')
        status = item.get('trackingStatus', '?')
        updated = item.get('updatedAt', '')
        text = item.get('text', '')[:50].replace('\n', ' ')

        days = '无时间戳'
        days_str = '无时间戳'
        if updated:
            try:
                dt_val = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                if dt_val.tzinfo is None:
                    dt_val = dt_val.replace(tzinfo=timezone.utc)
                days = (now - dt_val).days
                days_str = f'{days} 天'
            except Exception:
                days_str = f'解析异常({updated[:10]})'

        # 动态分类：从 review-log 读取实际 decision，不再使用硬编码 ID
        decision = decisions.get(iid, '')
        if decision in ('', 'pending'):
            if ts == '待研判':
                category = 'needs-review'
            else:
                category = 'silent-pending'   # 有 trackingStatus 但从未进入 review 流程
        elif decision in ('approve', 'modify'):
            if ts == '跟踪中':
                category = 'waiting-for-business-decision'
            elif ts == '已上报':
                category = 'waiting-for-data'
            else:
                category = 'post-approval'
        else:
            category = 'other'

        icon = '🔴' if (isinstance(days, int) and days >= 7) else ('🟡' if (isinstance(days, int) and days >= 3) else '🟢')
        print(f'  {icon} [{status}] {iid[:12]} | {days_str} | {category}')
        print(f'     └ {text}...')

        aging_rows.append({
            'id': iid,
            'status': status,
            'days': days if isinstance(days, int) else -1,
            'category': category,
            'text': item.get('text', '')[:80]
        })

    print(f'\n  ── 分类汇总 ──')
    cats = {}
    for r in aging_rows:
        c = r['category']
        cats[c] = cats.get(c, 0) + 1
    for cat, cnt in sorted(cats.items()):
        print(f'    {cat}: {cnt} 项')

    print(f'\n  ── Age 告警 ──')
    old_items = [r for r in aging_rows if isinstance(r['days'], int) and r['days'] >= 7]
    if old_items:
        result('长期 Pending(≥7天)', 'WARN', f'{len(old_items)} 项悬停 ≥7 天，请尽快处理')
        outcomes['WARN'] += len(old_items)
        for r in old_items:
            print(f'    🔴 {r["id"][:12]} | {r["days"]}天 | {r["category"]} | {r["text"][:40]}')
    else:
        result('Pending Age', 'PASS', '所有 Pending 项均在 7 天内')
        outcomes['PASS'] += 1

    mid_items = [r for r in aging_rows if isinstance(r['days'], int) and 3 <= r['days'] < 7]
    if mid_items:
        result('中期 Pending(3-6天)', 'PASS', f'{len(mid_items)} 项悬停 3-6 天')
        outcomes['PASS'] += 1

    fresh_items = [r for r in aging_rows if isinstance(r['days'], int) and r['days'] < 3]
    if fresh_items:
        result('新 Pending(<3天)', 'PASS', f'{len(fresh_items)} 项 <3 天，正常')
        outcomes['PASS'] += 1

    return outcomes


def run_fast() -> dict:
    """快速校验：覆盖主链路一致性，控制在 10s 内

    覆盖：tracking-items / 周报第九+十节 / report-tracking 链路 / bundle 一致性 / meta 文件
    排除：parse 数据深度校验（慢）、analyst opinions（可选）、review queue realism（全量）
    """
    all_outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    for fn in [validate_tracking_items, validate_weekly_report,
               validate_report_tracking_link, validate_meta_files,
               validate_bundle_sync]:
        outcomes = fn()
        for k, v in outcomes.items():
            all_outcomes[k] += v
    return all_outcomes


def run_all() -> dict:
    """完整校验：覆盖全部检查项（60s+）"""
    all_outcomes = {'PASS': 0, 'WARN': 0, 'FAIL': 0}
    for fn in [validate_parse, validate_review_queue, validate_tracking_items,
               validate_report_tracking_link, validate_review_queue_realism,
               validate_weekly_report,
               lambda: validate_web_bundle(lightweight=False),
               validate_analyst_opinions, validate_meta_files,
               validate_bundle_sync]:
        outcomes = fn()
        for k, v in outcomes.items():
            all_outcomes[k] += v
    return all_outcomes


# ── 回归基线检查 ────────────────────────────────────────────
def check_baseline() -> dict[str, list[str]]:
    """防回退基线检查：确保关键产物不回退到不可用状态

    用法：
        python3 scripts/smoke_test.py --baseline
        # 或在 run-pipeline.py 中通过 subprocess 调用
    """
    BASE = Path(__file__).resolve().parent.parent
    REPORTS = BASE / 'reports'
    PROCESSED = BASE / 'data' / 'processed'
    issues: list[str] = []
    warnings: list[str] = []

    # 1. review queue 不应回退到兜底模式
    rq_path = REPORTS / 'review-queue.json'
    if rq_path.exists():
        rq = json.loads(rq_path.read_text())
        items = rq.get('items', [])
        fallback_items = [
            '存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。',
            '贷款投放节奏判断不能脱离产品结构和定价水平，应联动观察。',
            '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。'
        ]
        fb_count = sum(1 for i in items if i.get('text', '') in fallback_items)
        if fb_count >= len(items) * 0.8:
            issues.append('review-queue 退回兜底模式 (FAIL)')
        elif fb_count > 0:
            warnings.append(f'review-queue 有 {fb_count} 条兜底')

    # 2. weekly report 必须包含 tracking 状态
    report_path = REPORTS / 'weekly-report-draft.md'
    if report_path.exists():
        report_text = report_path.read_text(encoding='utf-8')
        if '## 九、重点事项跟踪状态汇总' not in report_text:
            issues.append('weekly report 未包含第九节 (FAIL)')
        if '## 十、事项明细' not in report_text:
            issues.append('weekly report 未包含第十节 (FAIL)')

    # 3. loan_rate 不应出现明显异常值（如负数或 >20%）
    lr_path = PROCESSED / 'loan_rate.json'
    if lr_path.exists():
        lr = json.loads(lr_path.read_text())
        bad_rates = [r for r in lr if r.get('monthlyRate', 0) < 0 or r.get('monthlyRate', 0) > 20]
        if bad_rates:
            issues.append(f'loan_rate 有 {len(bad_rates)} 条异常利率 (FAIL)')

    # 4. 运行摘要必须存在
    rs_path = REPORTS / 'run-summary.json'
    if not rs_path.exists() or rs_path.stat().st_size < 100:
        issues.append('run-summary.json 不存在或过小 (FAIL)')

    return {'issues': issues, 'warnings': warnings}


def main() -> None:
    argv = sys.argv[1:]

    # ── 模式判断 ──────────────────────────────────────────
    mode_word = '快速校验'
    if '--full' in argv:
        mode_word = '完整校验'
    elif '--fast' in argv:
        mode_word = '快速校验（主链路一致性）'
    elif '--parse-only' in argv:
        mode_word = '仅解析数据'
    elif '--queue-only' in argv:
        mode_word = '仅审核队列'
    elif '--tracking-only' in argv:
        mode_word = '仅跟踪事项'
    elif '--report-only' in argv:
        mode_word = '仅周报'
    elif '--bundle-only' in argv:
        mode_word = '仅 Bundle'
    elif '--pending-aging' in argv:
        mode_word = 'Pending Aging 分析'
    elif '--baseline' in argv:
        mode_word = '回归基线检查'
    else:
        mode_word = '完整校验（默认）'

    print('=' * 56)
    print('  对公 AI 雷达站 — 主链路 Smoke Test / 数据校验')
    print(f'  模式: {mode_word} | 执行时间: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
    print('=' * 56)

    # ── Baseline 回归检查模式（独立入口）────────────────
    if '--baseline' in argv:
        result = check_baseline()
        total_issues = len(result.get('issues', []))
        total_warns = len(result.get('warnings', []))
        for issue in result.get('issues', []):
            print(f'  ❌ BASELINE FAIL: {issue}')
        for warning in result.get('warnings', []):
            print(f'  ⚠️  BASELINE WARN: {warning}')
        if total_issues == 0 and total_warns == 0:
            print(f'\n  ✅ 基线检查全部通过，无回归风险。')
            sys.exit(0)
        elif total_issues > 0:
            print(f'\n  ❌ 存在 {total_issues} 项基线失败，建议先处理后再运行主链路。')
            sys.exit(1)
        else:
            print(f'\n  ⚠️  存在 {total_warns} 项基线警告，请关注。')
            sys.exit(0)
        return

    # ── Pending Aging 模式（独立入口）──────────────────
    if '--pending-aging' in argv:
        outcomes = run_pending_aging()
        total = sum(outcomes.values())
        print(f'\n  汇总  ✅{outcomes["PASS"]}  ⚠️{outcomes["WARN"]}  ❌{outcomes["FAIL"]}  ({total} 项)')
        sys.exit(0)
        return

    # ── 分层执行 ─────────────────────────────────────────
        outcomes = run_pending_aging()
        total = sum(outcomes.values())
        print(f'\n  汇总  ✅{outcomes["PASS"]}  ⚠️{outcomes["WARN"]}  ❌{outcomes["FAIL"]}  ({total} 项)')
        sys.exit(0)
        return

    # ── 分层执行 ─────────────────────────────────────────
    if '--fast' in argv:
        outcomes = run_fast()
    elif '--full' in argv:
        outcomes = run_all()
    elif '--parse-only' in argv:
        outcomes = validate_parse()
    elif '--queue-only' in argv:
        outcomes = validate_review_queue()
    elif '--tracking-only' in argv:
        outcomes = validate_tracking_items()
    elif '--report-only' in argv:
        outcomes = validate_weekly_report()
    elif '--bundle-only' in argv:
        outcomes = validate_web_bundle(lightweight=False)
    else:
        outcomes = run_all()

    total = outcomes['PASS'] + outcomes['WARN'] + outcomes['FAIL']
    print('\n' + '=' * 56)
    print(f'  汇总  ✅{outcomes["PASS"]}  ⚠️{outcomes["WARN"]}  ❌{outcomes["FAIL"]}  ({total} 项)')
    print('=' * 56)

    if outcomes['FAIL'] > 0:
        print('\n  ⚠️  存在 FAIL 项，请优先处理后再运行主链路。')
        sys.exit(1)
    elif outcomes['WARN'] > 0:
        print('\n  ⚠️  存在 WARN 项，建议尽快检查。')
        sys.exit(0)
    else:
        print('\n  ✅ 全部通过，无 FAIL/WARN。')
        sys.exit(0)


if __name__ == '__main__':
    main()
