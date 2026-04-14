#!/usr/bin/env python3
"""
scripts/check_fetch_health.py
检查 analyst fetch 的健康状态，生成 per-source 级别的健康摘要。
"""

import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
CONFIG = BASE / 'config' / 'analyst_sources.json'
PROCESSED = BASE / 'data' / 'processed'
REPORTS = BASE / 'reports'

def main():
    # 读取源配置
    with open(CONFIG) as f:
        config = json.load(f)
    
    sources = config.get('sources', [])
    
    # 读取最近的抓取结果
    raw_path = PROCESSED / 'analyst_opinions_raw.json'
    if not raw_path.exists():
        print("❌ analyst_opinions_raw.json 不存在")
        return
    
    with open(raw_path) as f:
        raw = json.load(f)
    
    records = raw.get('records', [])
    fetched_at = raw.get('fetchedAt', '')
    
    # 构建 source_id -> records 映射
    source_records = {}
    for r in records:
        # 从原始数据中提取 analyst name
        analyst = r.get('analystName', r.get('author', ''))
        if analyst not in source_records:
            source_records[analyst] = []
        source_records[analyst].append(r)
    
    # 构建健康摘要
    health_summary = {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'fetchedAt': fetched_at,
        'totalSources': len(sources),
        'totalRecords': len(records),
        'sources': []
    }
    
    for src in sources:
        name = src.get('name', '')
        src_id = src.get('id', '')
        
        # 查找该源的记录
        src_records = source_records.get(name, [])
        
        # 统计状态
        status_counts = {}
        for r in src_records:
            st = r.get('status', 'unknown')
            status_counts[st] = status_counts.get(st, 0) + 1
        
        # 确定该源的总体状态
        if not src_records:
            overall_status = 'no_records'
            failure_reason = '本次运行未抓取到记录'
        elif status_counts.get('success', 0) > 0:
            overall_status = 'success'
            failure_reason = ''
        elif status_counts.get('skipped_old', 0) > 0:
            overall_status = 'skipped'
            failure_reason = f'文章早于2024年，已跳过 ({status_counts.get("skipped_old", 0)} 条)'
        elif status_counts.get('pending', 0) > 0:
            overall_status = 'degraded'
            failure_reason = '记录状态为 pending，可能抓取不完整'
        else:
            overall_status = 'failed'
            failure_reason = ', '.join([f'{k}: {v}' for k, v in status_counts.items()])
        
        # 检查连续失败
        last_success = None
        last_failure = None
        consecutive_failures = 0
        
        # 读取历史状态（如果有）
        history_path = REPORTS / 'fetch-history.json'
        if history_path.exists():
            with open(history_path) as f:
                history = json.load(f)
            src_history = history.get('sources', {}).get(src_id, {})
            last_success = src_history.get('lastSuccess')
            last_failure = src_history.get('lastFailure')
            consecutive_failures = src_history.get('consecutiveFailures', 0)
        
        # 更新连续失败计数
        if overall_status in ('failed', 'degraded'):
            consecutive_failures += 1
        elif overall_status == 'success':
            consecutive_failures = 0
            last_success = fetched_at
        
        if overall_status != 'success':
            last_failure = fetched_at
        
        # 建议处理
        if consecutive_failures >= 3:
            recommendation = '建议暂时降级或替换'
        elif overall_status == 'failed':
            recommendation = '需要检查失败原因'
        elif overall_status == 'degraded':
            recommendation = '观察中，暂不干预'
        elif overall_status == 'skipped':
            recommendation = '正常跳过，无需干预'
        else:
            recommendation = '继续保留'
        
        health_summary['sources'].append({
            'id': src_id,
            'name': name,
            'org': src.get('org', ''),
            'status': overall_status,
            'failureReason': failure_reason,
            'recordCount': len(src_records),
            'statusBreakdown': status_counts,
            'lastSuccess': last_success,
            'lastFailure': last_failure,
            'consecutiveFailures': consecutive_failures,
            'recommendation': recommendation,
            'active': src.get('active', True)
        })
    
    # 写入健康摘要
    health_path = REPORTS / 'fetch-health.json'
    with open(health_path, 'w') as f:
        json.dump(health_summary, f, indent=2, ensure_ascii=False)
    
    # 生成 markdown 版本
    md_lines = [
        '# Analyst Fetch 健康摘要',
        '',
        f'生成时间: {health_summary["generatedAt"]}',
        f'抓取时间: {health_summary["fetchedAt"]}',
        '',
        '## 源状态汇总',
        '',
        '| 源 | 状态 | 记录数 | 失败原因 | 建议 |',
        '|---|---|---|---|---|',
    ]
    
    for src in health_summary['sources']:
        md_lines.append(f"| {src['name']} | {src['status']} | {src['recordCount']} | {src['failureReason'][:40] if src['failureReason'] else ''} | {src['recommendation']} |")
    
    md_lines.append('')
    md_lines.append('## 状态说明')
    md_lines.append('')
    md_lines.append('- **success**: 抓取成功')
    md_lines.append('- **degraded**: 部分成功或状态异常')
    md_lines.append('- **failed**: 抓取失败')
    md_lines.append('- **skipped**: 正常跳过（如文章过旧）')
    md_lines.append('- **no_records**: 本次未抓取到记录')
    md_lines.append('')
    md_lines.append('## 建议')
    md_lines.append('')
    md_lines.append('- **继续保留**: 正常运行')
    md_lines.append('- **观察中**: 暂不干预')
    md_lines.append('- **需要检查**: 单次失败，建议关注')
    md_lines.append('- **建议暂时降级**: 连续失败 3+ 次')
    
    md_path = REPORTS / 'fetch-health.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    
    print(f"✅ fetch-health.json 已生成")
    print(f"✅ fetch-health.md 已生成")
    
    # 打印摘要
    print()
    print("=== 源状态 ===")
    for src in health_summary['sources']:
        status_icon = '✅' if src['status'] == 'success' else ('⚠️' if src['status'] in ('degraded', 'skipped') else '❌')
        print(f"{status_icon} {src['name']}: {src['status']} ({src['recordCount']} records)")

if __name__ == '__main__':
    main()
