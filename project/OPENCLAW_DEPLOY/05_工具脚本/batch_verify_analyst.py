#!/usr/bin/env python3
"""
scripts/batch_verify_analyst.py — Analyst 全量批次验证

策略：
  每次小批次（1~3个来源）用 Scrapling 抓取
  追加到 analyst_opinions_raw.json（不覆盖已验证的来源）
  每批次跑 build_analyst_opinions 并输出质量摘要
  用 checkpoint 文件跟踪哪些来源已验证

用法：
  python3 scripts/batch_verify_analyst.py                  # 按批次顺序跑下一个批次
  python3 scripts/batch_verify_analyst.py --batch 3        # 指定批次大小（默认2）
  python3 scripts/batch_verify_analyst.py --status         # 仅查看当前状态
  python3 scripts/batch_verify_analyst.py --run-all        # 跑完所有未验证来源
  python3 scripts/batch_verify_analyst.py --resume          # 续跑（跳过已验证的）
  python3 scripts/batch_verify_analyst.py --source analyst-deposit-001  # 单源验证
"""
import json
import time
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
PROCESSED = BASE / 'data' / 'processed'
OUTPUT_RAW = PROCESSED / 'analyst_opinions_raw.json'
OUTPUT_FINAL = PROCESSED / 'analyst_opinions.json'
CHECKPOINT = PROCESSED / '.batch_verify_checkpoint.json'
CONFIG = BASE / 'config' / 'analyst_sources.json'

BATCH_SIZE = 2  # 默认每批 2 个来源

# ── 全部 9 个来源（按 priority 排序）──────────────────────
ALL_SOURCES = [
    # 高优先级（对公存款）
    {'id': 'analyst-deposit-001', 'name': '董希淼',   'dimension': '对公存款', 'priority': 1},
    {'id': 'analyst-deposit-002', 'name': '薛洪言',   'dimension': '对公存款', 'priority': 1},
    {'id': 'analyst-deposit-003', 'name': '娄飞鹏',   'dimension': '对公存款', 'priority': 1},
    {'id': 'analyst-deposit-004', 'name': '连平',     'dimension': '对公存款', 'priority': 1},
    {'id': 'analyst-deposit-005', 'name': '周茂华',   'dimension': '对公存款', 'priority': 1},
    # 高优先级（对公贷款）
    {'id': 'analyst-loan-001',   'name': '温彬',     'dimension': '对公贷款', 'priority': 1},
    {'id': 'analyst-loan-002',   'name': '曾刚',     'dimension': '对公贷款', 'priority': 1},
    # 中优先级（对公整体）
    {'id': 'analyst-overall-001','name': '朱太辉',   'dimension': '对公整体', 'priority': 2},
    {'id': 'analyst-overall-002','name': '孙扬',     'dimension': '对公整体', 'priority': 2},
]


def load_sources_with_urls():
    """从 analyst_sources.json 加载每个来源的实际 URL"""
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    url_map = {}
    for src in config.get('sources', []):
        sid = src.get('id', '')
        seed_urls = src.get('seedUrls', [])
        if seed_urls:
            url_map[sid] = seed_urls[0]  # 取第一个 seed URL
    return url_map


def load_checkpoint():
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text(encoding='utf-8'))
    return {'verified': [], 'failed': [], 'last_run': None}


def save_checkpoint(cp):
    CHECKPOINT.write_text(json.dumps(cp, ensure_ascii=False, indent=2), encoding='utf-8')


def load_raw_opinions():
    if OUTPUT_RAW.exists():
        return json.loads(OUTPUT_RAW.read_text(encoding='utf-8'))
    return {'records': [], '_meta': {}}


def save_raw_opinions(data):
    OUTPUT_RAW.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def fetch_with_scrapling(url, timeout=20):
    """用 Scrapling 抓取，返回段落列表"""
    from scrapling.fetchers import Fetcher
    r = Fetcher.get(url, timeout=timeout)
    html = str(r.body)
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
        tag.decompose()
    text = soup.get_text(separator='\n', strip=True)
    paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 40]
    return soup, paras


def extract_title(soup) -> str:
    """从已解析的 soup 中提取标题，优先级：og:title > title > 第一段"""
    og = soup.find('meta', property='og:title')
    if og and og.get('content', '').strip():
        return og['content'].strip()
    title_tag = soup.find('title')
    if title_tag and title_tag.get_text(strip=True):
        return title_tag.get_text(strip=True)
    return ''


def build_raw_record(source_id, name, url, dimension, soup, paragraphs):
    content = '\n'.join(paragraphs[:15])
    dedup_key = hashlib.md5(f'{source_id}:{url}'.encode()).hexdigest()[:12]
    title = extract_title(soup)
    return {
        'id': f'op-{dedup_key}',
        'source': source_id,
        'sourceName': name,
        'dimension': [dimension],
        'url': url,
        'title': title if title else (paragraphs[0][:80] if paragraphs else ''),
        'content': content,
        'fetchedAt': datetime.now(timezone.utc).isoformat(),
        'status': 'fresh',
    }


def run_build():
    result = subprocess.run(
        [sys.executable, str(BASE / 'scripts' / 'build_analyst_opinions.py')],
        capture_output=True, text=True, timeout=60, cwd=str(BASE)
    )
    return result.returncode == 0


def get_quality_summary():
    if not OUTPUT_FINAL.exists():
        return None
    d = json.loads(OUTPUT_FINAL.read_text(encoding='utf-8'))
    s = d.get('summary', {})
    tiers = s.get('qualityTiers', {})
    return {
        'total': len(d.get('records', [])),
        'validCount': tiers.get('VALID', 0),
        'garbledCount': tiers.get('GARBLED', 0),
        'placeholderCount': tiers.get('PLACEHOLDER', 0),
        'degradedCount': tiers.get('DEGRADED', 0),
        'referenceableCount': s.get('referenceableCount', 0),
        'verdict': s.get('verdict', 'N/A'),
        'isReliableForReport': s.get('isReliableForReport', False),
        'builtAt': s.get('builtAt', 'N/A'),
    }


def show_status():
    cp = load_checkpoint()
    raw = load_raw_opinions()
    records = raw.get('records', [])
    before = get_quality_summary()

    print('=' * 52)
    print('  Batch Verify Analyst — 当前状态')
    print('=' * 52)
    print(f'已验证来源: {len(cp["verified"])} / {len(ALL_SOURCES)}')
    print(f'失败来源: {len(cp["failed"])}')
    print(f'上次运行: {cp.get("last_run", "从未")}')
    print()
    print('各来源状态：')
    url_map = load_sources_with_urls()
    for src in ALL_SOURCES:
        sid = src['id']
        status_icon = '✅' if sid in cp['verified'] else ('❌' if sid in cp['failed'] else '⬜')
        verified_record = next((r for r in records if r.get('source') == sid), None)
        if verified_record:
            clen = len(verified_record.get('content', ''))
            print(f'  {status_icon} {sid} ({src["name"]}): {clen} chars')
        else:
            print(f'  {status_icon} {sid} ({src["name"]}): 未抓取')
    print()
    if before:
        print('当前质量摘要（analyst_opinions.json）：')
        for k, v in before.items():
            if k != 'builtAt':
                print(f'  {k}: {v}')
    print('=' * 52)


def run_batch(source_ids, batch_label=''):
    """运行一批来源，返回 (success_count, fail_count)"""
    cp = load_checkpoint()
    url_map = load_sources_with_urls()
    raw_before = load_raw_opinions()

    print(f'\n{"="*52}')
    print(f'  批次 {batch_label}：{len(source_ids)} 个来源')
    print('=' * 52)

    # 记录抓取前状态
    before = get_quality_summary()
    if before:
        print(f'批次开始前: garbled={before["garbledCount"]} valid={before["validCount"]} '
              f'ref={before["referenceableCount"]} reliable={before["isReliableForReport"]}')

    new_records = []
    success_ids = []
    fail_ids = []

    for sid in source_ids:
        src = next((s for s in ALL_SOURCES if s['id'] == sid), None)
        if not src:
            print(f'  ⚠️ 未知来源: {sid}')
            continue

        url = url_map.get(sid)
        if not url:
            print(f'  ⚠️ {src["name"]}: 无 seed URL，跳过')
            fail_ids.append(sid)
            continue

        print(f'\n  [{src["name"]}] {sid}')
        print(f'    URL: {url[:60]}')
        try:
            start = time.time()
            soup, paras = fetch_with_scrapling(url, timeout=20)
            elapsed = time.time() - start
            record = build_raw_record(sid, src['name'], url, src['dimension'], soup, paras)
            new_records.append(record)
            success_ids.append(sid)
            print(f'    ✅ {len(paras)} 段落, {len(record["content"])} 字符, {elapsed:.1f}s')
            print(f'    内容预览: {record["content"][:80]}...')
        except Exception as e:
            fail_ids.append(sid)
            print(f'    ❌ {type(e).__name__}: {str(e)[:80]}')

    if not new_records:
        print('\n  无新记录写入')
        return 0, len(fail_ids)

    # 去重追加：移除同来源旧记录，追加新记录
    raw_data = load_raw_opinions()
    records = raw_data.get('records', [])
    for rec in new_records:
        records = [r for r in records if r.get('source', '') != rec['source']]
        records.append(rec)
    raw_data['records'] = records
    raw_data.setdefault('_meta', {})['lastBatchAt'] = datetime.now(timezone.utc).isoformat()
    save_raw_opinions(raw_data)
    print(f'\n  写入完成：{len(new_records)} 条新记录')

    # 跑 build
    print('\n  跑 build_analyst_opinions.py...')
    build_ok = run_build()
    if build_ok:
        print('  ✅ build 完成')
    else:
        print('  ⚠️ build 返回非零')

    # 抓取后状态
    after = get_quality_summary()
    if after and before:
        print(f'\n  质量变化:')
        for key in ['garbledCount', 'validCount', 'placeholderCount', 'referenceableCount']:
            b = before.get(key, 0)
            a = after.get(key, 0)
            delta = a - b
            icon = '↑' if delta > 0 else ('↓' if delta < 0 else '→')
            print(f'    {key}: {b} → {a} ({icon}{abs(delta)})')
        r_before = before.get('isReliableForReport', False)
        r_after = after.get('isReliableForReport', False)
        print(f'    isReliableForReport: {r_before} → {r_after}')

    # 更新 checkpoint
    cp = load_checkpoint()
    for sid in success_ids:
        if sid not in cp['verified']:
            cp['verified'].append(sid)
    for sid in fail_ids:
        if sid not in cp['failed']:
            cp['failed'].append(sid)
    cp['last_run'] = datetime.now(timezone.utc).isoformat()
    save_checkpoint(cp)

    return len(success_ids), len(fail_ids)


def get_next_batch(batch_size, skip_verified=True):
    """获取下一批待验证来源"""
    cp = load_checkpoint()
    verified = set(cp['verified'])
    failed = set(cp['failed'])
    all_ids = [s['id'] for s in ALL_SOURCES]

    # 按 priority 排序（高优先级在前）
    def sort_key(sid):
        src = next((s for s in ALL_SOURCES if s['id'] == sid), None)
        return (src['priority'] if src else 99, all_ids.index(sid))

    candidates = [s['id'] for s in ALL_SOURCES if s['id'] not in verified | failed]
    if skip_verified:
        candidates = [s['id'] for s in ALL_SOURCES
                      if (s['id'] not in verified and s['id'] not in failed)]
    candidates.sort(key=sort_key)
    return candidates[:batch_size]


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyst 全量批次验证')
    parser.add_argument('--batch', type=int, default=BATCH_SIZE, help=f'每批次来源数（默认{BATCH_SIZE}）')
    parser.add_argument('--batch-num', type=int, help='指定跑第几批次（从1开始）')
    parser.add_argument('--status', action='store_true', help='仅显示当前状态')
    parser.add_argument('--run-all', action='store_true', help='跑完所有未验证来源')
    parser.add_argument('--resume', action='store_true', help='续跑（跳过已验证）')
    parser.add_argument('--source', help='指定单个来源ID验证')
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.source:
        n_ok, n_fail = run_batch([args.source], f'单源 {args.source}')
        print(f'\n结果: 成功={n_ok} 失败={n_fail}')
        return

    batch_num = args.batch_num
    batch_size = args.batch

    if args.run_all:
        # 跑完所有
        print('=' * 52)
        print(f'  开始全量验证（batch_size={batch_size}）')
        print('=' * 52)
        total_ok = 0
        total_fail = 0
        batch_idx = 1
        while True:
            batch_ids = get_next_batch(batch_size)
            if not batch_ids:
                print(f'\n所有来源已验证完毕或无更多来源')
                break
            n_ok, n_fail = run_batch(batch_ids, f'{batch_idx}')
            total_ok += n_ok
            total_fail += n_fail
            if n_ok == 0 and n_fail == 0:
                break
            batch_idx += 1
        print(f'\n全量验证完成: 成功={total_ok} 失败={total_fail}')
        return

    if batch_num:
        # 指定批次
        cp = load_checkpoint()
        verified = set(cp['verified']) | set(cp['failed'])
        remaining = [s['id'] for s in ALL_SOURCES if s['id'] not in verified]
        remaining.sort()
        batch_ids = remaining[:batch_num * batch_size]
        batch_ids = batch_ids[(batch_num - 1) * batch_size: batch_num * batch_size]
        if not batch_ids:
            print(f'批次 {batch_num} 为空（已全部验证）')
            return
        n_ok, n_fail = run_batch(batch_ids, f'#{batch_num}')
        return

    # 默认：跑下一批次
    batch_ids = get_next_batch(batch_size)
    if not batch_ids:
        print('所有来源已验证完毕。')
        print()
        show_status()
        return

    print(f'待验证 {len(batch_ids)} 个来源: {batch_ids}')
    n_ok, n_fail = run_batch(batch_ids, '下一批次')
    print(f'\n结果: 成功={n_ok} 失败={n_fail}')

    # 展示当前状态
    print()
    show_status()


if __name__ == '__main__':
    main()
