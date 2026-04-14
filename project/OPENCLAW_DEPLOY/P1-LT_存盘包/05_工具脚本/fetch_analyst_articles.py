#!/usr/bin/env python3
"""
scripts/fetch_analyst_articles.py

外部分析师观点采集脚本 - 第二版
目标：从公开可访问的网页/文章抓取分析师观点，输出为观点中间层。

使用原则：
- 优先公开可抓取来源
- 半自动优先，遇到障碍自动降级不卡住
- 第一阶段以对公存款为主跑通闭环
- 2024年之后的文章才抓取（可通过 --min-year 修改）

运行方式：
    python3 scripts/fetch_analyst_articles.py
    python3 scripts/fetch_analyst_articles.py --dimension 对公存款
    python3 scripts/fetch_analyst_articles.py --dry-run
    python3 scripts/fetch_analyst_articles.py --min-year 2023

依赖：
    pip install requests beautifulsoup4
"""

from __future__ import annotations

import json
import re
import hashlib
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 可选依赖检查
try:
    from scrapling.fetchers import Fetcher
    from bs4 import BeautifulSoup

    HAS_SCRAPLING = True
    HAS_BS4 = True
except ImportError:
    HAS_SCRAPLING = False
    HAS_BS4 = False
    import sys
    print("❌ 缺少 scrapling，请运行: /tmp/py39env/bin/pip install scrapling==0.2.99", file=sys.stderr)
    sys.exit(1)

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
CONFIG = BASE / '04_数据与规则' / 'analyst_sources.json'
PROCESSED = BASE / '04_数据与规则' / 'processed'
CACHE = BASE / '04_数据与规则' / 'analyst_cache'
CACHE.mkdir(parents=True, exist_ok=True)

# 抓取统计 (全局)
FETCH_STATS = {
    'total': 0,
    'success': 0,
    'failed': 0,
    'skipped': 0,
    'encoding_fixed': 0,
}

CRAWL_CONFIGS = {
    'auto': {
        'timeout': 15,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
        'retry': 1,
        'backoff': 30,
    },
    'semi': {
        'timeout': 20,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        },
        'retry': 2,
        'backoff': 60,
    },
}


def make_dedup_key(title: str, author: str, published_at: str) -> str:
    raw = f"{title}|{author}|{published_at}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def extract_date_from_url(url: str) -> str:
    """尝试从URL中提取日期或返回空字符串"""
    patterns = [
        r'(\d{8})',
        r'(\d{4}-\d{2}-\d{2})',
        r'(\d{4})\.(\d{2})\.(\d{2})',
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            raw = m.group(1)
        # 校验是否为有效日期（年月日范围合理）
            if len(raw) == 8 and raw.isdigit():
                y, m_, d = int(raw[:4]), int(raw[4:6]), int(raw[6:8])
                if 1990 <= y <= 2030 and 1 <= m_ <= 12 and 1 <= d <= 31:
                    return raw
            else:
                return raw  # 其他格式直接返回
    return ''


def year_from_published(published_at: str) -> int | None:
    """从 publishedAt 字段解析年份，返回 None 表示无法解析"""
    if not published_at:
        return None
    for pat in [r'^(\d{4})-', r'^(\d{4})\.', r'^(\d{4})']:
        m = re.match(pat, str(published_at))
        if m:
            return int(m.group(1))
    return None


def is_too_old(published_at: str, min_year: int = 2024) -> bool:
    """返回 True 表示文章年份早于 min_year，应当跳过"""
    year = year_from_published(published_at)
    if year is None:
        return False  # 无法解析日期，默认保留
    return year < min_year


def fetch_url(url: str, mode: str = 'auto', min_year: int = 2024) -> dict[str, Any]:
    """抓取单个URL（scrapling 版本）。min_year 参数控制只抓取该年份之后的文章。"""
    cfg = CRAWL_CONFIGS.get(mode, CRAWL_CONFIGS['auto'])
    result = {
        'url': url,
        'fetchedAt': datetime.now(timezone.utc).isoformat(),
        'status': 'success',
        'title': '',
        'author': '',
        'publishedAt': '',
        'content': '',
        'summary': '',
        'keyViewpoints': [],
        'evidenceSnippets': [],
        'failureReason': '',
        'crawlMode': mode,
        'skipped': False,
        'skipReason': '',
    }

    if not HAS_SCRAPLING:
        result['status'] = 'dependency_missing'
        result['failureReason'] = '缺少 scrapling 库，请运行: /tmp/py39env/bin/pip install scrapling==0.2.99'
        return result

    # 域名级别 timeout 覆盖
    domain_timeout_overrides = {
        'eastmoney.com': 20,
        'news.cn': 20,
        'sina.com.cn': 15,
        '21jingji.com': 15,
        'shifd.net': 15,
        'stcn.com': 20,
        'nifd.cn': 20,
    }
    url_timeout = cfg['timeout']
    for domain, override_timeout in domain_timeout_overrides.items():
        if domain in url:
            url_timeout = override_timeout
            break

    # scrapling 自动处理重试、UA、编码检测、Redirect
    last_error = None
    status = None
    resp = None
    for attempt in range(cfg['retry'] + 1):
        try:
            resp = Fetcher.get(url, timeout=url_timeout)
            status = resp.status
            break
        except Exception as e:
            last_error = f'{type(e).__name__}: {str(e)[:100]}'
            if attempt < cfg['retry']:
                time.sleep(cfg['backoff'])
            continue

    if resp is None:
        result['status'] = 'request_error'
        result['failureReason'] = last_error or '请求失败'
        return result

    # 状态码处理
    if status == 200:
        # scrapling 已自动处理编码，直接用 body 字符串
        text = str(resp.body)

        try:
            soup = BeautifulSoup(text, 'html.parser')
        except Exception:
            soup = BeautifulSoup(text[:10000], 'html.parser')

        result['_encoding_note'] = 'scrapling自动检测'

        # 提取标题
        title_tag = (
            soup.find('meta', property='og:title') or
            soup.find('meta', {'name': 'twitter:title'}) or
            soup.find('h1') or
            soup.find('title')
        )
        if title_tag:
            result['title'] = title_tag.get('content', '') or title_tag.get_text(strip=True)
        paragraphs = soup.find_all('p')
        if not result['title'] and paragraphs:
            first_p = paragraphs[0].get_text(strip=True)
            if len(first_p) > 10:
                result['title'] = first_p[:60]

        # 提取作者
        author_meta = (
            soup.find('meta', {'name': 'author'}) or
            soup.find('meta', {'property': 'article:author'}) or
            soup.find('span', class_=re.compile(r'author', re.I))
        )
        if author_meta:
            result['author'] = author_meta.get('content', '') or author_meta.get_text(strip=True)

        # 提取发布时间
        time_tag = (
            soup.find('time') or
            soup.find('span', class_=re.compile(r'date|time|publ', re.I)) or
            soup.find('meta', property='article:published_time')
        )
        if time_tag:
            pub = time_tag.get('datetime', '') or time_tag.get_text(strip=True)
            result['publishedAt'] = pub[:19] if pub else ''
        if not result['publishedAt']:
            result['publishedAt'] = extract_date_from_url(url)

        # 日期过滤
        if is_too_old(result['publishedAt'], min_year):
            result['status'] = 'skipped_old'
            result['skipped'] = True
            result['skipReason'] = f'文章发布于 {result["publishedAt"]}，早于{min_year}年，已跳过'
            return result

        # 提取正文：优先专有内容区，其次段落列表
        main_content = []
        # 方案1：专有内容 div（sif.suning.com 等平台使用 f-article-content 等 class）
        content_classes = ['f-article-content', 'article-content', 'article_content',
                           'post-content', 'entry-content', 'article-body']
        for content_tag in soup.find_all('div', class_=lambda x: x and any(
            c in (x if isinstance(x, (list, tuple)) else [x]) for c in content_classes
        )):
            text = content_tag.get_text(separator='\n', strip=True)
            if len(text) > 200:
                lines = [l for l in text.split('\n') if l.strip() and len(l.strip()) > 10]
                main_content = lines[:50]
                break

        # 方案2：标准段落（兜底）
        if not main_content:
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                ptext = p.get_text(strip=True)
                if len(ptext) > 30:
                    main_content.append(ptext)
            main_content = main_content[:30]

        result['content'] = '\n'.join(main_content[:50])

        # 生成摘要
        if result['content']:
            result['summary'] = result['content'][:300].replace('\n', ' ')

        # 关键观点片段：从 main_content 中提取
        judgment_words = ['建议', '认为', '指出', '显示', '预计', '可能', '需要', '应该', '值得关注', '注意']
        for text in main_content:
            if len(text) > 50 and any(w in text for w in judgment_words):
                result['keyViewpoints'].append(text)
            if len(result['keyViewpoints']) >= 5:
                break
        # 证据片段
        for text in main_content:
            if any(c in text for c in ['%', '亿元', '万亿', '增长', '下降', '利率', '息差']) and len(text) > 30:
                result['evidenceSnippets'].append(text)
            if len(result['evidenceSnippets']) >= 3:
                break

    elif status == 403:
        result['status'] = 'permission_denied'
        result['failureReason'] = f'HTTP 403 - 需要登录或权限禁止（URL: {url}）'
    elif status == 404:
        result['status'] = 'dead_link'
        result['failureReason'] = 'HTTP 404 - 页面不存在'
    elif status == 429:
        result['status'] = 'rate_limited'
        result['failureReason'] = 'HTTP 429 - 请求频率超限，30分钟后重试'
    else:
        result['status'] = 'http_error'
        result['failureReason'] = f'HTTP {status}'

    return result



def load_sources(config_path: Path, dimension_filter: str | None = None) -> list[dict]:
    data = json.loads(config_path.read_text(encoding='utf-8'))
    sources = data.get('sources', [])
    if dimension_filter:
        return [s for s in sources if dimension_filter in s.get('dimension', [])]
    return sources


def discover_articles_from_profile(profile_url: str) -> list[dict[str, str]]:
    """
    从 profile 页面自动发现文章 URL 列表。
    目前支持 sif.suning.com（星图金融研究院）。
    返回 [{'url': ..., 'title': ...}, ...]
    """
    if 'sif.suning.com/author/detail/' not in profile_url:
        return []
    try:
        resp = Fetcher.get(profile_url, timeout=15)
        if resp.status != 200:
            return []
        soup = BeautifulSoup(str(resp.body), 'html.parser')
        articles = []
        seen = set()
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            if '/article/detail/' not in href:
                continue
            full_url = href if href.startswith('http') else f'https://sif.suning.com{href}'
            if full_url in seen:
                continue
            seen.add(full_url)
            title = a.get_text(strip=True)[:80]
            articles.append({'url': full_url, 'title': title})
        return articles
    except Exception:
        return []


def fetch_all(dimension_filter: str | None = None, dry_run: bool = False, min_year: int = 2024) -> list[dict]:
    sources = load_sources(CONFIG, dimension_filter)
    results = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    for src in sources:
        if not src.get('active', False):
            continue

        name = src['name']
        org = src['org']
        dims = src.get('dimension', [])
        mode = src.get('crawlMode', 'auto')
        seed_urls = src.get('seedUrls', [])
        tags = src.get('tags', [])
        notes = src.get('notes', '')
        platform = src.get('platform', 'web')
        profile_url = src.get('profileUrl', '')
        account_name = src.get('accountName', name)

        # 如果 seedUrls 为空但有 profileUrl，尝试从 profile 页发现文章
        if not seed_urls and profile_url:
            discovered = discover_articles_from_profile(profile_url)
            if discovered:
                seed_urls = [d['url'] for d in discovered]
                if dry_run:
                    print(f"[DRY] {name} ({mode}) -> 从profile发现 {len(seed_urls)} 篇文章")
                else:
                    print(f"[PROFILE] {name} 从profile页发现 {len(seed_urls)} 篇文章")
            elif dry_run:
                print(f"[DRY] {name} ({mode}) -> 0 URLs (profile无文章)")

        if dry_run and seed_urls:
            print(f"[DRY] {name} ({mode}) -> {len(seed_urls)} URLs")
            continue

        for url in seed_urls:
            print(f"  Fetching: {name} | {url[:60]}...")
            r = fetch_url(url, mode, min_year)

            dedup_key = make_dedup_key(r['title'], name, r['publishedAt'])

            record = {
                'source': src['id'],
                'dimension': dims,
                'analystName': name,
                'org': org,
                'platform': platform,
                'accountName': account_name,
                'articleTitle': r['title'],
                'sourceUrl': r['url'],
                'publishedAt': r['publishedAt'],
                'retrievedAt': fetched_at,
                'summary': r['summary'],
                'keyViewpoints': r['keyViewpoints'],
                'evidenceSnippets': r['evidenceSnippets'],
                'dedupKey': dedup_key,
                'tags': tags,
                'crawlStatus': r['status'],
                'failureReason': r['failureReason'],
                'skipped': r.get('skipped', False),
                'skipReason': r.get('skipReason', ''),
                'profileUrl': profile_url,
                'relevanceScore': None,
                'confidenceScore': None,
                'actionabilityScore': None,
                'reviewDecision': None,
                'enterReport': None,
                'reportSection': None,
                'trackingItemId': None,
                'status': 'pending',
                'notes': notes,
            }

            results.append(record)

            if r['status'] == 'success':
                status_icon = '✅'
            elif r['status'] == 'skipped_old':
                status_icon = '⏭️'
            else:
                status_icon = '⚠️'
            extra = r.get('skipReason', '') or r.get('failureReason', '')
            title = r['title'][:40] if r['title'] else '(无标题)'
            print(f"    {status_icon} {r['status']} - {title} | {extra}")

        # 避免过快请求
            if mode == 'auto':
                time.sleep(1)

    return results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description='抓取分析师观点文章')
    parser.add_argument('--dimension', '-d', choices=['对公存款', '对公贷款', '对公整体'], help='限定抓取维度')
    parser.add_argument('--dry-run', action='store_true', help='只列出来源不实际抓取')
    parser.add_argument('--output', '-o', default=None, help='输出文件路径')
    parser.add_argument('--min-year', type=int, default=2024, help='只抓取此年份之后的文章（默认2024）')
    args = parser.parse_args()

    dim = args.dimension or '对公存款'
    min_year = args.min_year
    print(f"=== 分析师观点抓取开始 | 维度: {dim} | 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 过滤: >= {min_year}年 ===\n")

    results = fetch_all(dimension_filter=dim, dry_run=args.dry_run, min_year=min_year)

    if args.dry_run:
        print(f"\n[DRY RUN] 已跳过实际抓取（dry-run 模式）")
        print(f"      提示：年份过滤（>=2024）只在实际抓取时生效，dry-run 无法预判过滤结果")
        print(f"      如需真正刷新数据，请执行：./run-analyst-fetch.sh")
        return

    print(f"\n=== 抓取完成 | 共 {len(results)} 条记录 ===")
    success_count = sum(1 for r in results if r['crawlStatus'] == 'success')
    skipped_count = sum(1 for r in results if r['crawlStatus'] == 'skipped_old')
    failure_count = len(results) - success_count - skipped_count
    # 编码修复统计
    encoding_fixed = sum(1 for r in results if r.get('_encoding_used') and r.get('_encoding_used') not in ('utf-8', 'utf-8-replaced'))
    
    # 写入抓取统计
    stats = {
        'total': len(results),
        'success': success_count,
        'failed': failure_count,
        'skipped': skipped_count,
        'encoding_fixed': encoding_fixed,
        'generatedAt': datetime.now().isoformat()
    }
    (PROCESSED / 'fetch-stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"  成功: {success_count}")
    print(f"  已跳过（早于{min_year}年）: {skipped_count}")
    print(f"  失败/降级: {failure_count}")

    out_path = Path(args.output) if args.output else (PROCESSED / 'analyst_opinions_raw.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({'records': results, 'fetchedAt': datetime.now().isoformat()}, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"\n原始抓取结果已保存: {out_path}")

    failures = [r for r in results if r['crawlStatus'] not in ('success', 'skipped_old')]
    if failures:
        print(f"\n--- 失败/降级源汇总 ({len(failures)} 条) ---")
        for f in failures:
            print(f"  [{f['crawlStatus']}] {f['analystName']} | {f['sourceUrl'][:50]} | {f['failureReason']}")


if __name__ == '__main__':
    main()