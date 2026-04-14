#!/usr/bin/env python3
"""
scripts/verify_analyst_fix.py — B gate 小批量 live 验证

只验证 2 个代表性来源：
- 连平（东方财富）：之前 garbled，现在用 Scrapling 验证
- 薛洪言（新华网）：之前 garbled，现在用 Scrapling 验证

链路：Scrapling fetch → 写入 analyst_opinions_raw → build_analyst_opinions → 质量摘要对比

用法：
    python3 scripts/verify_analyst_fix.py
    python3 scripts/verify_analyst_fix.py --dry-run
"""
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
PROCESSED = BASE / 'data' / 'processed'
OUTPUT_RAW = PROCESSED / 'analyst_opinions_raw.json'
OUTPUT_FINAL = PROCESSED / 'analyst_opinions.json'

# ── 测试来源 ──────────────────────────────────────────────
TEST_SOURCES = [
    {
        'id': 'analyst-deposit-004',
        'name': '连平',
        'url': 'https://finance.eastmoney.com/a/202602243652417892.html',
        'dimension': '对公存款',
    },
    {
        'id': 'analyst-deposit-002',
        'name': '薛洪言',
        'url': 'https://app.xinhuanet.com/news/article.html?articleId=681e0d3749f7ec90a2e12472059100d9',
        'dimension': '对公存款',
    },
]

def fetch_with_scrapling(url, timeout=20):
    """用 Scrapling 抓取，返回清洗后文本段落列表"""
    from scrapling.fetchers import Fetcher
    r = Fetcher.get(url, timeout=timeout)
    html = str(r.body)
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
        tag.decompose()
    text = soup.get_text(separator='\n', strip=True)
    paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 40]
    return paras

def build_raw_record(source_id, name, url, dimension, paragraphs):
    """将抓取结果构建为 raw opinion 记录"""
    content = '\n'.join(paragraphs[:15])  # 最多 15 段
    dedup_key = hashlib.md5(f'{source_id}:{url}'.encode()).hexdigest()[:12]
    return {
        'id': f'op-{dedup_key}',
        'source': source_id,
        'sourceName': name,
        'dimension': [dimension],
        'url': url,
        'title': paragraphs[0][:80] if paragraphs else '',
        'content': content,
        'fetchedAt': datetime.now(timezone.utc).isoformat(),
        'status': 'fresh',
    }

def load_raw_opinions():
    """加载当前 analyst_opinions_raw.json"""
    if OUTPUT_RAW.exists():
        return json.loads(OUTPUT_RAW.read_text(encoding='utf-8'))
    return {'records': []}

def save_raw_opinions(data):
    OUTPUT_RAW.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def run_build():
    """调 build_analyst_opinions.py"""
    import subprocess
    result = subprocess.run(
        [__import__('sys').executable, str(BASE / 'scripts' / 'build_analyst_opinions.py')],
        capture_output=True, text=True, timeout=60,
        cwd=str(BASE)
    )
    return result.returncode, result.stdout, result.stderr

def get_quality_summary():
    """从 analyst_opinions.json 读取质量摘要"""
    if not OUTPUT_FINAL.exists():
        return None
    d = json.loads(OUTPUT_FINAL.read_text(encoding='utf-8'))
    s = d.get('summary', {})
    return {
        'total': len(d.get('records', [])),
        'validCount': s.get('qualityTiers', {}).get('VALID', 0),
        'garbledCount': s.get('qualityTiers', {}).get('GARBLED', 0),
        'placeholderCount': s.get('qualityTiers', {}).get('PLACEHOLDER', 0),
        'degradedCount': s.get('qualityTiers', {}).get('DEGRADED', 0),
        'referenceableCount': s.get('referenceableCount', 0),
        'verdict': s.get('verdict', 'N/A'),
        'isReliableForReport': s.get('isReliableForReport', False),
        'builtAt': s.get('builtAt', 'N/A'),
    }

def main():
    import sys
    dry = '--dry-run' in sys.argv

    print('=' * 52)
    print('  B gate 小批量 live 验证')
    print('=' * 52)

    # ── 阶段 1：抓取前状态 ──────────────────────────────────
    print('\n[阶段 1] 抓取前 analyst_opinions 状态：')
    before = get_quality_summary()
    if before:
        for k, v in before.items():
            print(f'  {k}: {v}')
    else:
        print('  analyst_opinions.json 不存在，跳过 before 对比')

    # ── 阶段 2：Scrapling 抓取 ──────────────────────────────
    print('\n[阶段 2] Scrapling live 抓取：')
    raw_before = load_raw_opinions()
    existing_sources = {r.get('source', '') for r in raw_before.get('records', []) if r.get('source')}

    new_records = []
    for src in TEST_SOURCES:
        print(f'\n  抓取 {src["name"]} ({src["id"]})...')
        if dry:
            print(f'  [DRY] {src["url"]}')
            new_records.append({'id': f'dry-{src["id"]}', 'source': src['id'], 'status': 'dry'})
            continue
        try:
            start = time.time()
            paras = fetch_with_scrapling(src['url'], timeout=20)
            elapsed = time.time() - start
            record = build_raw_record(src['id'], src['name'], src['url'], src['dimension'], paras)
            new_records.append(record)
            char_count = len(record['content'])
            print(f'  ✅ 成功：{len(paras)} 段落, {char_count} 字符, 耗时 {elapsed:.1f}s')
            print(f'     内容预览：{record["content"][:80]}...')
        except Exception as e:
            print(f'  ❌ 失败：{type(e).__name__} {str(e)[:80]}')
            new_records.append({'id': f'err-{src["id"]}', 'source': src['id'], 'status': 'error', 'error': str(e)[:80]})

    if dry:
        print('\n[DRY-RUN] 跳过写入和 build')
        return

    # ── 阶段 3：写入 raw opinions（去重追加）───────────────
    print('\n[阶段 3] 写入 analyst_opinions_raw.json...')
    raw_data = load_raw_opinions()
    records = raw_data.get('records', [])
    initial_count = len(records)

    # 移除同来源旧记录，追加新记录
    for rec in new_records:
        if rec.get('status') in ('dry', 'error'):
            continue
        records = [r for r in records if r.get('source', '') != rec['source']]
        records.append(rec)

    raw_data['records'] = records
    raw_data['_meta'] = raw_data.get('_meta', {})
    raw_data['_meta']['lastVerifyAt'] = datetime.now(timezone.utc).isoformat()
    raw_data['_meta']['verifySources'] = [s['id'] for s in TEST_SOURCES]
    save_raw_opinions(raw_data)
    print(f'  写入完成：从 {initial_count} 条 → {len(records)} 条')

    # ── 阶段 4：跑 build ───────────────────────────────────
    print('\n[阶段 4] 运行 build_analyst_opinions.py...')
    code, stdout, stderr = run_build()
    if code == 0:
        print('  ✅ build 完成')
    else:
        print(f'  ⚠️ build 返回码 {code}')
        if stderr:
            print(f'     stderr: {stderr[:200]}')

    # ── 阶段 5：抓取后状态 & 对比 ─────────────────────────
    print('\n[阶段 5] 抓取后 analyst_opinions 状态：')
    after = get_quality_summary()
    if after:
        for k, v in after.items():
            print(f'  {k}: {v}')

    if before and after:
        print('\n[对比] before → after：')
        changes = []
        for key in ['validCount', 'garbledCount', 'placeholderCount', 'referenceableCount']:
            b = before.get(key, 0)
            a = after.get(key, 0)
            delta = a - b
            icon = '↑' if delta > 0 else ('↓' if delta < 0 else '→')
            changes.append(f'  {key}: {b} → {a} ({icon}{abs(delta)})')
        for line in changes:
            print(line)
        print(f'  verdict: {before.get("verdict","N/A")} → {after.get("verdict","N/A")}')
        print(f'  isReliableForReport: {before.get("isReliableForReport")} → {after.get("isReliableForReport")}')

    print('\n' + '=' * 52)
    print('  B gate 验证完成')
    print('=' * 52)

if __name__ == '__main__':
    main()
