from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
REPORTS = BASE / 'reports'

# 硬编码的稳定 id（与 review-log.jsonl 已记录的历史 id 对齐）
# 按前缀长度降序排列，防止短前缀被长前缀的子串误匹配
# 注意：pricing-1 的原始文本来自六节（策略建议），不带 `[优先级:high]` 前缀
HARDCODED_ID_MAP = {
    '[优先级:high] 建议将贷款产品结构、同业定价': 'pricing-1',  # 一节中的原文本
    '建议将贷款产品结构、同业定价和风险收益并列呈现，让策略建议更贴近经营决策。': 'pricing-1',  # 六节中的实际文本（无优先级标签）
    '存款对标看，当前重点股份行中': 'core-1',
    '贷款对标看，兴业银行在"余额"口径下': 'core-2',
}


def stable_id(text: str, category: str = '') -> str:
    """生成稳定的 id：精确匹配已知硬编码项（完整文本比较），否则用内容 hash"""
    # 按前缀长度降序排列，防止短前缀被长前缀的子串误匹配
    sorted_map = sorted(HARDCODED_ID_MAP.items(), key=lambda x: -len(x[0]))
    for prefix, fixed_id in sorted_map:
        if text.startswith(prefix):
            return fixed_id
    key = f"{category}:{text[:30]}".encode()
    return hashlib.md5(key).hexdigest()[:12]


def extract_section(text: str, start_marker: str, end_marker: str | None = None) -> str:
    """提取两个标记之间的内容"""
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return ''
    start_idx = text.find('\n', start_idx)
    if start_idx == -1:
        return ''
    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        if end_idx == -1:
            return text[start_idx + 1:]
        return text[start_idx + 1:end_idx]
    return text[start_idx + 1:]


def extract_bullets(section_text: str, skip_priority_tag: bool = False) -> list[str]:
    """提取真实事项行，过滤元数据/规则类行

    skip_priority_tag=True 时：过滤 `[优先级:...]` 开头的行（一节中这些是规则模板）
    skip_priority_tag=False 时：保留 `[优先级:...]` 开头的行（五至八节中这些是真实事项）
    """
    lines = section_text.split('\n')
    result = []
    meta_prefixes = ('[栏目口径]', '[生成规则]', '[追问提示]')
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith('- '):
            continue
        content = stripped[1:].strip()
        if len(content) <= 10:
            continue
        if content.startswith(meta_prefixes):
            continue
        if skip_priority_tag and content.startswith('[优先级:'):
            continue
        result.append(content)
    return result


def clean_bullet(text: str) -> str:
    """清理 bullet 行末的优先级标签"""
    return re.sub(r'\[优先级:[^\]]+\]\s*', '', text).strip()


def extract_review_items() -> list[dict]:
    report_path = REPORTS / 'weekly-report-draft.md'
    text = report_path.read_text(encoding='utf-8') if report_path.exists() else ''
    if not text:
        return []

    items = []

    # 核心结论摘要（一节）：过滤元数据行 + 过滤优先级标签行（这些都是规则模板，不是真实事项）
    section_1 = extract_section(text, '## 一、核心结论摘要', '## 二、同业动态观察')
    for bullet in extract_bullets(section_1, skip_priority_tag=True):
        text_clean = clean_bullet(bullet)
        # 过滤 [板块模板] / [解释规则] 等元数据行
        if text_clean and not text_clean.startswith(('[板块模板]', '[解释规则]')):
            items.append({
                'id': stable_id(text_clean, 'core'),
                'category': '核心结论摘要',
                'source': 'weekly-report-draft.md',
                'text': text_clean
            })

    # 观察提示（五节）
    section_5 = extract_section(text, '## 五、观察提示', '## 六、策略建议')
    for bullet in extract_bullets(section_5):
        text_clean = clean_bullet(bullet)
        if text_clean:
            items.append({
                'id': stable_id(text_clean, 'obs'),
                'category': '观察提示',
                'source': 'weekly-report-draft.md',
                'text': text_clean
            })

    # 策略建议（六节）
    section_6 = extract_section(text, '## 六、策略建议', '## 七、直接行动建议')
    for bullet in extract_bullets(section_6):
        text_clean = clean_bullet(bullet)
        if text_clean:
            items.append({
                'id': stable_id(text_clean, 'strategy'),
                'category': '策略建议',
                'source': 'weekly-report-draft.md',
                'text': text_clean
            })

    # 直接行动建议（七节）
    section_7 = extract_section(text, '## 七、直接行动建议', '## 八、待人工确认事项')
    for bullet in extract_bullets(section_7):
        text_clean = clean_bullet(bullet)
        if text_clean:
            items.append({
                'id': stable_id(text_clean, 'action'),
                'category': '直接行动建议',
                'source': 'weekly-report-draft.md',
                'text': text_clean
            })

    # 待人工确认事项（八节）
    section_8 = extract_section(text, '## 八、待人工确认事项', '## 九、重点事项跟踪状态汇总')
    for bullet in extract_bullets(section_8):
        text_clean = clean_bullet(bullet)
        if text_clean:
            items.append({
                'id': stable_id(text_clean, 'pending'),
                'category': '待人工确认事项',
                'source': 'weekly-report-draft.md',
                'text': text_clean
            })

    return items


def main() -> None:
    items = extract_review_items()

    # 兜底：若无提取结果，沿用原有 3 条硬编码项（保持兼容性）
    if not items:
        items = [
            {
                'id': 'core-1',
                'category': '核心结论摘要',
                'source': 'weekly-report-draft.md',
                'text': '存款对标应从总量、月度变化、年初以来变化三维度拆解平安与重点同业差距来源。'
            },
            {
                'id': 'core-2',
                'category': '核心结论摘要',
                'source': 'weekly-report-draft.md',
                'text': '贷款投放节奏判断不能脱离产品结构和定价水平，应联动观察。'
            },
            {
                'id': 'pricing-1',
                'category': '策略建议',
                'source': 'weekly-report-draft.md',
                'text': '建议将贷款产品结构与定价对比并列呈现，为产品、行业和定价建议提供更扎实依据。'
            }
        ]

    report_path = REPORTS / 'weekly-report-draft.md'
    text = report_path.read_text(encoding='utf-8') if report_path.exists() else ''

    payload = {
        'reportFile': str(report_path),
        'reportPreview': text[:4000],
        'items': items
    }
    out = REPORTS / 'review-queue.json'
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'review-queue.json written: {len(items)} items')


if __name__ == '__main__':
    main()