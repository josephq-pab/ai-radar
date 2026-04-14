#!/usr/bin/env python3
"""
scripts/build_analyst_opinions.py

将原始抓取结果构建为结构化观点中间层。
- 去重（同 dedupKey）
- 打 relevance / confidence / actionability 评分
- 筛选"高相关+有证据+可行动"进入周报
- 生成 review queue

运行：
    python3 scripts/build_analyst_opinions.py
    python3 scripts/build_analyst_opinions.py --top-k 5
"""

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
PROCESSED = BASE / '04_数据与规则' / 'processed'
RAW = PROCESSED / 'analyst_opinions_raw.json'
OUTPUT = PROCESSED / 'analyst_opinions.json'
REVIEW_QUEUE_OUT = BASE / 'reports' / 'analyst-review-queue.json'
SOURCES_CONFIG = BASE / '04_数据与规则' / 'analyst_sources.json'


def _load_inactive_source_ids() -> set[str]:
    """从 analyst_sources.json 读取 active: false 的 source ID 列表。

    用途：替代硬编码 QUARANTINED_SOURCES，实现配置驱动。
    若配置文件不存在或解析失败，返回空集（不阻断主流程）。
    """
    try:
        import json as _json
        data = _json.loads(SOURCES_CONFIG.read_text(encoding='utf-8'))
        return {
            src['id'] for src in data.get('sources', [])
            if not src.get('active', True)
        }
    except Exception:
        return set()


# ─── 评分函数 ────────────────────────────────────────────

BANK_KEYWORDS = [
    '存款', '贷款', '对公', '公司业务', '企业贷款', '负债', '息差',
    '净息差', '揽储', '存款利率', 'LPR', '利率', '贷款定价', '不良',
    '信贷', '公司银行', '同业', '资产', '负债端', '大额存单', '定期',
    '活期', '存款搬家', '银行经营', '商业银行', '股份行', '平安',
    '招商', '兴业', '中信', '浦发', '民生', '光大', '华夏', '广发',
    '浙商', '邮储', '国有大行', '贷款投放', '信贷投放', '企业融资',
    '小微', '普惠', '续贷', '并购', '跨境', '交易银行',
]
ACTION_KEYWORDS = [
    '建议', '应', '需要', '推动', '加强', '优化', '提升', '关注',
    '加快', '完善', '强化', '重点', '优先', '建议加强', '建议优化',
    '建议关注', '值得关注', '建议推动',
]
EVIDENCE_KEYWORDS = [
    '%', '亿元', '万亿', '亿', '增长', '下降', '提升', '回落',
    '扩大', '收窄', '提高', '降低', '创', '首次', '持续', '显著',
    '环比', '同比', '累计', '年化', '不良率', '净息差', '增速',
]


def score_relevance(text: str, dimension: str, record: dict = None) -> float:
    """0-1，越高越相关"""
    # 基于维度标签和 analyst name 评分，不依赖文本可读性
    if not record:
        return 0.3  # 保守默认值

    dims = record.get('dimension', [])
    dim = dims[0] if dims else ''

    # 分析师维度的先验权重
    dim_priority = {
        '对公存款': ['董希淼', '薛洪言', '娄飞鹏', '连平', '周茂华'],
        '对公贷款': ['温彬', '曾刚', '董希淼', '娄飞鹏', '周茂华'],
        '对公整体': ['曾刚', '连平', '温彬', '朱太辉', '孙扬'],
    }
    analysts_for_dim = dim_priority.get(dim, [])
    analyst = record.get('analystName', '')

    if analyst in analysts_for_dim:
        base = 0.6
    elif analyst in dim_priority.get('对公存款', []) or analyst in dim_priority.get('对公贷款', []):
        base = 0.4
    else:
        base = 0.2

    # 有 evidence snippets 加分
    if record.get('evidenceSnippets'):
        base += 0.15
    # 有 viewpoints 加分
    if record.get('keyViewpoints'):
        base += 0.1

    return min(base, 1.0)


# ─── Layer 3：内容提取 ────────────────────────────────────
# 宁缺毋滥：仅当 content 非空但 keyViewpoints / evidenceSnippets 均为空时触发
# 不生成泛化空话；提取失败则保持原样


def _is_meaningful_sentence(sent: str) -> bool:
    """判断句子是否有实质内容（非导航、非日期行、非分隔符）"""
    if not sent or len(sent.strip()) < 15:
        return False
    import re
    if re.match(r'^\d{4}年\d{1,2}月\d{1,2}日', sent.strip()):
        return False
    if sent.strip().startswith('http'):
        return False
    if any(k in sent for k in ['违法和不良信息举报', '版权所有', 'copyright', 'law21@']):
        return False
    return True


def _split_sentences(text: str) -> list[str]:
    import re
    parts = re.split(r'(?<=[。！？\n])', text)
    return [p.strip() for p in parts if p.strip()]


def extract_viewpoints_and_snippets(record: dict) -> dict:
    """Layer 3：保守型内容提取。

    仅对 content 非空但 keyViewpoints / evidenceSnippets 均为空的记录触发。
    宁缺毋滥：提取失败或不满足阈值则不动原数组，保持 []。
    返回 record 自身（in-place 修改）。

    TODO(Phase-后续)：当前依赖规则匹配，后续应改为 LLM 提取以提升召回率。
    """
    content = record.get('content', '')
    vps = record.get('keyViewpoints', [])
    evs = record.get('evidenceSnippets', [])

    if not content or len(content) < 200:
        return record
    if vps or evs:
        return record  # 已有值，不覆盖

    sents = _split_sentences(content)

    # ── 提取 keyViewpoints（最多 2 条）──────────────────
    # 严格要求：必须满足以下条件之一
    # (a) 含"XXX表示/指出/认为/称"等显式分析师引语格式（且>=25字）
    # (b) 含预判词"将/预计/有望"且>=40字（排除短小的新闻事实句）
    # 排除：近日、记者、据悉 等新闻套话开头
    found_vps = []
    news_lead_kw = ['近日', '据悉', '记者', '本報', '本报', '社论',
                     '采访', '走访', '了解', '获悉', '从相关渠道']
    analyst_attr_kw = ['表示', '指出', '认为', '称', '强调', '分析',
                        '判断', '评价', '称', '补充', '告诉']
    foresight_kw = ['将', '预计', '预期', '有望', '将推动', '将促进',
                     '将成为', '意味着', '表明', '显示']

    for s in sents:
        if len(found_vps) >= 2:
            break
        if not _is_meaningful_sentence(s):
            continue
        # 跳过新闻套话开头
        if any(s.startswith(k) for k in news_lead_kw):
            continue
        # 跳过含记者/近日等新闻套话（不管位置）
        if '记者' in s[:30] and ('近日' in s[:50] or '从' in s[:20]):
            continue

        # 条件A：显式分析师引语
        has_attr = any(k in s for k in analyst_attr_kw) and ('：' in s or '"' in s or '"' in s)
        cond_a = has_attr and len(s) >= 25
        # 条件B：预判类长句
        has_foresight = any(k in s for k in foresight_kw)
        cond_b = has_foresight and len(s) >= 40

        if cond_a or cond_b:
            found_vps.append(s)

    # ── 提取 evidenceSnippets（最多 3 条）───────────────
    # 要求：含具体数字关键词 + 长度>=25（排除短新闻句）
    # 排除：标题重复句、新闻套话开头
    found_evs = []
    title = record.get('articleTitle', '')
    num_kw = ['%', '亿元', '万亿', '亿', '增长', '下降', '提升', '回落',
              '扩大', '收窄', '提高', '降低', '创', '首次', '持续',
              '环比', '同比', '累计', '年化', '增速', '占比']

    for s in sents:
        if len(found_evs) >= 3:
            break
        if not _is_meaningful_sentence(s) or len(s) < 25:
            continue
        # 跳过新闻套话开头
        if any(s.startswith(k) for k in news_lead_kw):
            continue
        has_num = any(k in s for k in num_kw)
        # 跳过与标题重复的句子
        if title and (s[:40] == title[:40] or s[:20] in title):
            continue
        if has_num and s not in found_vps:
            found_evs.append(s)

    if found_vps:
        record['keyViewpoints'] = found_vps
        record['_layer3_viewpoints'] = len(found_vps)
    if found_evs:
        record['evidenceSnippets'] = found_evs
        record['_layer3_snippets'] = len(found_evs)

    return record


# ─── 质量分层 ──────────────────────────────────────────
GARBLED_CHARS = frozenset(['�', 'æ', 'å', 'è', 'ï', '¶', '¹', '¸', '»',
                            '鏍', '钁', '涓', '澶', '閫', '杩', '瀵', '浠', '鍥', '椤'])
PLACEHOLDER_TITLES = frozenset([
    'finance.eastmoney.com', '37619039f873daba6891f6e99b61fac2',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
])


def classify_analyst_record(record: dict) -> dict:
    """对单条 analyst 记录进行质量分层，返回增强字段。

    语义约定（Phase 2 基线）：
    - isUsable:        内容可读（不是 GARBLED / PLACEHOLDER），可用于参考
    - isReferenceable: 内容值得引用（VALID 级别；DEGRADED 不算）
    - isReportable:    已进入周报（decide_enter_report 之后由调用方设置）
    - qualityNote:      人工可读的质量说明

    与 Phase 1 的区别：
    - 原 isReferenceable 对 DEGRADED 也返回 True，导致 B gate 中
      "referenceableCount >= 3" 的阈值被 DEGRADED 满足，与 isReliableForReport 冲突。
    - Phase 2 起，isReferenceable 仅涵盖 VALID，彻底消除语义歧义。
    """

    title = record.get('articleTitle', '')

    # ── 内容质量初筛：检测浏览器错误提示页 ────────────────
    # 此类页面 title 通常正常但 content 开头为浏览器升级提示，无分析价值
    content = record.get('content', '')
    is_browser_error_page = (
        content.startswith('敬爱的用户，您的浏览器版本过低')
        or content.startswith('您的浏览器版本过低')
    )

    # 检测乱码
    has_garbled = any(c in GARBLED_CHARS for c in title)
    # 检测占位符标题
    is_placeholder = (
        not title.strip()
        or title.strip() in PLACEHOLDER_TITLES
        or (title.strip().isdigit() and len(title.strip()) > 10)
        or title.strip().startswith('http')
    )
    # 检测摘要也乱码
    summary = record.get('summary', '')
    summary_garbled = any(c in GARBLED_CHARS for c in summary) if summary else False

    # ── 质量定级 ──────────────────────────────────────────
    # 浏览器错误提示页 → 内容实质不可用（虽有 title 但 content 无分析价值）
    if has_garbled or summary_garbled or is_browser_error_page:
        quality_tier = 'GARBLED'
        is_usable = False
        is_referenceable = False
        quality_note = '内容为乱码或浏览器错误提示页，无分析价值'
    elif is_placeholder:
        quality_tier = 'PLACEHOLDER'
        is_usable = False
        is_referenceable = False
        quality_note = '标题为占位符或URL，非真实文章'
    elif title.strip() and len(title.strip()) >= 10:
        quality_tier = 'VALID'
        is_usable = True
        is_referenceable = True          # VALID → 可引用
        quality_note = '标题可读，内容完整，可引用'
    else:
        quality_tier = 'DEGRADED'
        is_usable = True                # DEGRADED → 可用但不完美
        is_referenceable = False        # DEGRADED → 不可直接引用（与 VALID 区分）
        quality_note = '标题较短或质量一般，建议人工复核后再引用'

    record['qualityTier'] = quality_tier
    record['isUsable'] = is_usable
    record['isReferenceable'] = is_referenceable
    record['isReportable'] = False
    record['qualityNote'] = quality_note
    return record


def _is_analyst_evidence(sentence: str) -> bool:
    """判断一个句子是否属于'分析师正式引语/观点'。

    严格要求：必须满足引语格式（分析师名字+引号/冒号+观点），排除：
    - 新闻套话（近日、据悉、记者注意到）
    - 数据事实句（含数字但无分析师引语）
    - 含"银行"等通用词+动词的普通句子
    """
    import re

    # 显式分析师引语格式：名字+机构/职称+：或" + 观点
    # 例如："招联首席经济学家董希淼表示，..."、"上海金融与发展实验室副主任董希淼称，..."
    # 也接受：薛洪言表示、杨海平指出、连平认为 等直接引语格式

    # 格式A：机构+职称+表示/指出/认为/称+引号/冒号后的内容
    # 格式B：直接以"XXX称/表示/指出/认为"开头

    # 先排除新闻套话句（近日、据悉、记者注意到等）
    news_intro = ['近日', '据悉', '记者注意到', '记者问询', '记者走访',
                  '从相关渠道', '本報', '本报', '采访']
    for kw in news_intro:
        if sentence.startswith(kw):
            return False

    # 格式A：名字/职称+表示/指出/认为/称 + 引号或中文冒号
    # 例如: "董希淼表示：..." 或 "研究员董希淼指出："
    _dq = '"'   # ASCII double quote (avoid raw-string escaping issues in char class)
    analyst_quote_pattern = re.compile(
        r'[\u4e00-\u9fff]{2,4}'
        r'(?:[研究员院士总裁首席主管]?[\u4e00-\u9fff]{1,4})?'
        r'(?:[：:' + _dq + r'])'
    )
    if analyst_quote_pattern.search(sentence):
        # 确认不是记者引用（"记者"出现在引语前）
        # 合理的分析师引语中，"记者"不应在分析师名字之前
        if re.search(r'记者[\u4e00-\u9fff]{1,4}(称|表示|指出|认为)', sentence):
            return False
        return True

    _q = '[\u201c\u201d"' + _dq   # opening quotes: left double quote, right double quote, ASCII quote
    direct_pattern = re.compile(
        r'^' + _q + r'?[\u4e00-\u9fff]{2,4}(?:称|表示|指出|认为|强调)'
    )
    if direct_pattern.match(sentence.strip()):
        return True

    return False


def _post_extraction_quality_gate(record: dict) -> dict:
    """Phase 2.1 新增：正文内容质量门控。

    在 Layer 3 提取完成后执行。修正 classify_analyst_record() 的 title-only 误判：
    - VALID 文章若 viewpoints=0 且 snippets 中无明确分析师引语 → 降级为 DEGRADED
    - 理由：分析师名字出现在标题 ≠ 正文有分析师观点（可能是记者报道）
    - DEGRADED 文章：isUsable=True（内容可读），isReferenceable=False（不可直接引用）
    - 降级后重新评估是否 reportable（actionabilityScore 预计已很低）
    """
    if record.get('qualityTier') != 'VALID':
        return record

    vps = record.get('keyViewpoints', [])
    evs = record.get('evidenceSnippets', [])
    analyst_ev_count = sum(1 for e in evs if _is_analyst_evidence(e))

    # 条件：viewpoints=0 且无分析师引语类 snippets → 正文实质是新闻转写，不是分析师观点
    if len(vps) == 0 and analyst_ev_count == 0:
        record['qualityTier'] = 'DEGRADED'
        record['isReferenceable'] = False
        record['qualityNote'] = (
            '标题可读但正文为新闻转写，无分析师本人观点，DEGRADED 不可直接引用'
        )
        record['_downgradedFromValid'] = True

    return record


def score_confidence(text: str, evidence: list, viewpoints: list) -> float:
    """0-1，越高可信"""
    base = score_relevance(text, '')
    ev_count = len(evidence)
    vp_count = len(viewpoints)
    return min(base + ev_count * 0.1 + vp_count * 0.05, 1.0)


def score_actionability(viewpoints: list, evidence: list) -> float:
    """0-1，越高越可行动"""
    if not viewpoints and not evidence:
        return 0.0
    vp_act = sum(1 for v in viewpoints if any(k in v for k in ACTION_KEYWORDS))
    ev_has = sum(1 for e in evidence if any(k in e for k in EVIDENCE_KEYWORDS))
    return min(vp_act * 0.3 + ev_has * 0.2, 1.0)


def decide_enter_report(record: dict) -> tuple[bool, str]:
    rel = record.get('relevanceScore', 0) or 0
    conf = record.get('confidenceScore', 0) or 0
    act = record.get('actionabilityScore', 0) or 0
    title = record.get('articleTitle', '')

    if rel >= 0.4 and conf >= 0.3 and act >= 0.3:
        dim = record.get('dimension', ['对公整体'])[0]
        section_map = {
            '对公存款': '二、同业动态观察（分析师观点）',
            '对公贷款': '三、贷款与产品观察（分析师观点）',
            '对公整体': '一、核心结论摘要（分析师观点）',
        }
        return True, section_map.get(dim, '一、核心结论摘要（分析师观点）')

    if '平安' in title and rel >= 0.3:
        return True, '一、核心结论摘要（分析师观点）'

    return False, ''


def decide_tracking(record: dict) -> bool:
    """只有两类进 tracking：(a)明确需业务动作跟进 (b)明确需后续数据验证"""
    act = record.get('actionabilityScore', 0) or 0
    ev = record.get('evidenceSnippets', [])
    # 有具体数据+有动作建议 -> 进 tracking
    has_evidence = len(ev) > 0
    has_action = any(k in ' '.join(record.get('keyViewpoints', [])) for k in ['建议', '应', '需要', '推动', '关注'])
    return has_evidence and (has_action or act >= 0.5)


# ─── 主逻辑 ────────────────────────────────────────────

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--top-k', type=int, default=5, help='最多进周报的观点数')
    parser.add_argument('--min-rel', type=float, default=0.4, help='最低相关性阈值')
    args = parser.parse_args()

    print("=== 构建分析师观点中间层 ===\n")

    if not RAW.exists():
        print(f"[ERROR] 找不到原始抓取文件: {RAW}")
        print("请先运行: python3 scripts/fetch_analyst_articles.py")
        return

    raw_data = json.loads(RAW.read_text(encoding='utf-8'))
    raw_records: list[dict] = raw_data.get('records', [])
    print(f"原始记录: {len(raw_records)} 条")

    # ── 来源隔离：剔除 active: false 的 source（配置驱动，不硬编码）────
    inactive_sources = _load_inactive_source_ids()
    pre_quarantine_count = len(raw_records)
    raw_records = [r for r in raw_records if r.get('source', '') not in inactive_sources]
    q_count = pre_quarantine_count - len(raw_records)
    if q_count > 0:
        print(f"  [QUARANTINE] 剔除 {q_count} 条 inactive 来源（{sorted(inactive_sources)}）")

    # ── 去重 ──
    seen = set()
    deduped = []
    for r in raw_records:
        dk = r.get('dedupKey') or r.get('id', '')
        if dk and dk not in seen:
            seen.add(dk)
            deduped.append(r)
        elif not dk:
            deduped.append(r)
    print(f"去重后: {len(deduped)} 条")

    # ── 评分 ──
    scored = []
    for r in deduped:
        # ══════════════════════════════════════════════════════════════
        # SKIP_OLD 记录直接过滤：不参与评分，不进入 reviewed 层
        # 理由：内容为 2024 年前旧文，不符合"2024 年后"抓取要求
        # ══════════════════════════════════════════════════════════════
        if r.get('crawlStatus') == 'skipped_old':
            continue
        # 编码修复：处理双重编码乱码（GBK→UTF8）和 GBK 混 UTF8
        for field in ('articleTitle', 'summary', 'keyViewpoints', 'evidenceSnippets'):
            if field in r:
                if isinstance(r[field], list):
                    r[field] = [_repair_mojibake(_try_decode(x)) for x in r[field]]
                elif isinstance(r[field], str):
                    r[field] = _repair_mojibake(_try_decode(r[field]))

        # ── 字段兼容层（统一 articleTitle / analystName / sourceUrl）─────────
        r['articleTitle'] = r.get('articleTitle') or r.get('title', '')
        r['analystName'] = r.get('analystName') or r.get('sourceName', '')
        r['sourceUrl'] = r.get('sourceUrl') or r.get('url', '')
        r['publishedAt'] = r.get('publishedAt') or r.get('fetchedAt', '')

        # ── 兜底 articleTitle（先于 extraction 执行，使提取逻辑可感知标题）──
        if not r.get('articleTitle', '').strip():
            fallback = _fallback_title(r)
            r['_originalTitleMissing'] = True
            r['articleTitle'] = fallback
            print(f"  [TITLE FALLBACK] {(r.get('dedupKey') or r.get('id', '?'))[:12]} -> \"{fallback}\"")
        else:
            r['_originalTitleMissing'] = False

        # ── 内容质量预检（先于 extraction 执行，避免对垃圾内容做无效提取）──
        content = r.get('content', '')
        is_browser_error = (
            content.startswith('敬爱的用户，您的浏览器版本过低')
            or content.startswith('您的浏览器版本过低')
        )
        # 检测内容是否过旧（2023 及以前，且非当前目标月份），用于存款对公场景
        import re
        content_year_match = re.search(r'20(?:1[6-9]|2[0-5])', content[:200])
        content_year = int(content_year_match.group()) if content_year_match else 2026
        is_stale_content = content_year < 2026

        # ── Layer 3：内容提取（先于评分执行，使提取结果参与 score）──
        # 触发条件：content 有实质内容(>=200字) + viewpoints/snippets 仍为空
        #           + 内容质量预检通过（非浏览器错误页，非过时内容）
        if (content and len(content) >= 200
                and not r.get('keyViewpoints') and not r.get('evidenceSnippets')
                and not is_browser_error and not is_stale_content):
            extract_viewpoints_and_snippets(r)

        dims = r.get('dimension', ['对公整体'])
        dim = dims[0] if dims else '对公整体'
        combined = f"{r.get('summary','')} {r.get('articleTitle','')} {''.join(r.get('keyViewpoints',[]))}"
        rel = score_relevance(combined, dim, r)
        conf = score_confidence(combined, r.get('evidenceSnippets', []), r.get('keyViewpoints', []))
        act = score_actionability(r.get('keyViewpoints', []), r.get('evidenceSnippets', []))

        r['relevanceScore'] = round(rel, 3)
        r['confidenceScore'] = round(conf, 3)
        r['actionabilityScore'] = round(act, 3)

        # ── 质量分层（在 extraction + title fallback 完成后执行）────────
        classify_analyst_record(r)
        # ── 正文内容质量门控（Phase 2.1：修正 title-only VALID 误判）──
        _post_extraction_quality_gate(r)
        scored.append(r)

    # ── 决策 ──
    reportable = []
    for r in scored:
        ok, section = decide_enter_report(r)
        r['enterReport'] = ok
        r['reportSection'] = section if ok else ''
        # 同步 isReportable（Phase 2 新增语义字段）
        r['isReportable'] = ok
        if ok:
            reportable.append(r)

    # 按综合分排序
    for r in scored:
        r['_composite'] = r['relevanceScore'] * 0.4 + r['confidenceScore'] * 0.3 + r['actionabilityScore'] * 0.3

    scored.sort(key=lambda x: x['_composite'], reverse=True)

    # 限制 top-k 进入周报
    reportable.sort(key=lambda x: x['_composite'], reverse=True)
    top_k = args.top_k
    top_records = reportable[:top_k]
    for r in scored:
        if r not in top_records:
            r['enterReport'] = False
            r['reportSection'] = ''
            r['isReportable'] = False
    for r in top_records:
        r['enterReport'] = True
        r['isReportable'] = True

    # ── tracking 接入 ──
    tracking_candidates = []
    for r in scored:
        if decide_tracking(r) and r['enterReport']:
            tracking_candidates.append(r)

    # ── 生成 review queue ──
    review_items = []
    for r in top_records:
        # ── confirmLevel 最小可行映射 ────────────────────────────────
        # 规则（Phase 3 MVP 最小版）：
        #   P1：VALID + 综合分 >= 0.75，或 VALID + 高相关性(>=0.8) + 有证据
        #   P2：VALID + 综合分 >= 0.60，或 DEGRADED + 综合分 >= 0.50
        #   P3：其余进入周报记录
        # 不足说明：当前为规则映射，非人工分级；精确分级需 P1-1 追踪表建立后补充
        composite = r.get('_composite', 0) or 0
        is_valid = r.get('qualityTier') == 'VALID'
        has_evidence = bool(r.get('evidenceSnippets'))
        rel = r.get('relevanceScore', 0) or 0

        if is_valid and composite >= 0.75:
            confirm_level = 'P1'
        elif is_valid and composite >= 0.60:
            confirm_level = 'P2'
        elif not is_valid and composite >= 0.50:
            confirm_level = 'P2'
        else:
            confirm_level = 'P3'

        item = {
            'id': f"analyst-{(r.get('dedupKey') or r.get('id', 'unknown'))[:8]}",
            'category': '分析师观点',
            'source': r['analystName'],
            'dimension': r['dimension'],
            'articleTitle': r['articleTitle'],
            'sourceUrl': r['sourceUrl'],
            'publishedAt': r['publishedAt'],
            'text': _extract_actionable_text(r),
            'relevanceScore': r['relevanceScore'],
            'confidenceScore': r['confidenceScore'],
            'actionabilityScore': r['actionabilityScore'],
            'qualityTier': r['qualityTier'],
            'isReferenceable': r['isReferenceable'],
            'confirmLevel': confirm_level,
            'qualityNote': r['qualityNote'],
            'enterReport': r['enterReport'],
            'reportSection': r['reportSection'],
            'trackingCandidate': r in tracking_candidates,
            # ── M4b 最小闭环演示状态字段（Phase 3 MVP）────────────
            # reviewStatus：确认操作状态（pending → confirmed/rejected）
            # trackingStatus：跟进状态（pending/candidate/follow_up/closed）
            # 注意事项：重新运行 build 会重置为 pending，不具备持久化能力
            'reviewStatus': 'pending',
            'trackingStatus': 'candidate' if r in tracking_candidates else 'pending',
        }
        review_items.append(item)

    # ── 输出 analyst_opinions.json ──
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # 质量分层统计
    quality_tiers = {'VALID': 0, 'DEGRADED': 0, 'GARBLED': 0, 'PLACEHOLDER': 0}
    usable_count = 0          # isUsable = True（内容可读，非乱码非占位）
    referenceable_count = 0    # isReferenceable = True（VALID 级别）
    reportable_count = 0      # isReportable = True（已进入周报）
    for r in scored:
        qt = r.get('qualityTier', 'UNKNOWN')
        quality_tiers[qt] = quality_tiers.get(qt, 0) + 1
        if r.get('isUsable', False):
            usable_count += 1
        if r.get('isReferenceable', False):
            referenceable_count += 1
        if r.get('isReportable', False):
            reportable_count += 1

    # Phase 2 B gate 清除标准：
    #   garbledCount == 0  AND  usableCount >= 3  AND  reportableCount >= 1
    # "usable" = isUsable (VALID + DEGRADED)，保证分析师层有基本可读内容
    # "reportable" = 已进入周报，保证 B gate 清除时真正有内容可引用
    is_reliable = (
        quality_tiers['GARBLED'] == 0
        and usable_count >= 3
        and reportable_count >= 1
    )

    OUTPUT.write_text(
        json.dumps({'records': scored, 'summary': {
            'total': len(scored),
            'reportable': len(top_records),
            'trackingCandidates': len(tracking_candidates),
            'qualityTiers': quality_tiers,
            # Phase 2 新增：拆分语义
            'usableCount': usable_count,          # 内容可读（非乱码非占位）
            'referenceableCount': referenceable_count,  # VALID 级别，可引用
            'reportableCount': reportable_count,  # 已进入周报
            # 兼容旧接口（deprecated，语义已修正）
            'isReliableForReport': is_reliable,
            # 详细说明
            'bGateClearCriteria': (
                'garbledCount==0 AND usableCount>=3 AND reportableCount>=1'
            ),
            'bGateStatus': (
                'cleared' if is_reliable else
                ('marginal' if quality_tiers['GARBLED'] == 0 and usable_count >= 3 else 'blocked')
            ),
            'byDimension': {
                d: sum(1 for r in scored if d in r.get('dimension', []))
                for d in ['对公存款', '对公贷款', '对公整体']
            },
            'fetchedAt': raw_data.get('fetchedAt', ''),
            'builtAt': datetime.now(timezone.utc).isoformat(),
        }}, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"结构化观点已保存: {OUTPUT}")
    print(f"质量分层: VALID={quality_tiers['VALID']} DEGRADED={quality_tiers['DEGRADED']} "
          f"GARBLED={quality_tiers['GARBLED']} PLACEHOLDER={quality_tiers['PLACEHOLDER']}")
    print(f"  usableCount={usable_count} | referenceableCount={referenceable_count} "
          f"| reportableCount={reportable_count}")
    print(f"  isReliableForReport={is_reliable} | B gate: "
          f"{'cleared' if is_reliable else 'blocked/marginal'}")

    # ── 输出 review queue ──
    REVIEW_QUEUE_OUT.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_QUEUE_OUT.write_text(
        json.dumps({'items': review_items, 'total': len(review_items)}, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"观点 review queue 已保存: {REVIEW_QUEUE_OUT}")

    # ── 打印摘要 ──
    print(f"\n=== 评分摘要 ===")
    print(f"总记录: {len(scored)} | 进入周报: {len(top_records)} | tracking候选: {len(tracking_candidates)}")
    print(f"\n进入周报的观点（按综合分排序）:")
    for i, r in enumerate(top_records, 1):
        rel = r['relevanceScore']
        conf = r['confidenceScore']
        act = r['actionabilityScore']
        composite = rel * 0.4 + conf * 0.3 + act * 0.3
        print(f"  {i}. [{r['analystName']}] {r['articleTitle'][:50]}")
        print(f"     综合分={composite:.2f} | rel={rel:.2f} conf={conf:.2f} act={act:.2f} | {r['reportSection']}")

    print(f"\n未进入周报的高相关记录（可手动确认）:")
    no_report = [r for r in scored if r['relevanceScore'] >= args.min_rel and not r['enterReport']]
    for r in no_report[:5]:
        print(f"  [{r['analystName']}] rel={r['relevanceScore']:.2f} | {r['articleTitle'][:50]}")


def _try_decode(text: str) -> str:
    """尝试 UTF-8，失败后尝试 GBK，适用于某些抓取源编码错误"""
    if not text:
        return ''
    try:
        text.encode('utf-8').decode('utf-8')
        return text
    except Exception:
        pass
    # 尝试 GBK
    try:
        return text.encode('utf-8').decode('gbk', errors='replace')
    except Exception:
        pass
    return text


def _repair_mojibake(text: str) -> str:
    """修复双重编码问题：GBK→UTF-8→Windows-1252 产生的乱码
    也处理中文 GBK 被误判为 UTF-8 的情况。
    """
    if not text or len(text) < 3:
        return text
    try:
        # Western European mojibake 检测（原有的）
        has_mojibake_western = any(c in text for c in ['æ', 'å', 'è', 'ï', '¶', '¹', '¸', '»', '¼', '½'])
        # 中文乱码检测：大量中文却含替换字符，或含中文字符但替换比例过高
        has_chinese = sum(1 for c in text if '\u4e00' <= c <= '\u9fff') > 5
        replacement_ratio = text.count('\ufffd') / max(len(text), 1)
        mojibake_chars = sum(1 for c in text if c in 'Ã§Ã©Ã Ã¤Ã«Ã®')
        if (has_chinese and (replacement_ratio > 0.005 or mojibake_chars > 5)) or has_mojibake_western:
            # 方案A：latin-1 round-trip（处理西欧字符）
            repaired_western = text.encode('latin-1').decode('utf-8', errors='replace')
            if not any(c in repaired_western for c in ['æ', 'å', 'è', 'ï', '¶']):
                return repaired_western
            # 方案B：GBK decode（处理中文编码错误）
            try:
                # 如果文本包含大量字节序列符合 GBK 双字节模式，尝试解码
                repaired_gbk = text.encode('latin-1', errors='replace').decode('gbk', errors='replace')
                chinese_count = sum(1 for c in repaired_gbk if '\u4e00' <= c <= '\u9fff')
                if chinese_count > 10:
                    return repaired_gbk
            except Exception:
                pass
        return text
    except Exception:
        return text


def _title_from_url(url: str) -> str | None:
    """从 URL 中提取尽可能有意义的标题片段（如 URL slug 包含日期或关键词）"""
    if not url:
        return None
    parts = url.rstrip('/').split('/')
    # 取最后一个非扩展名的 path segment
    for p in reversed(parts):
        if p in ('https:', 'http:', 'www.cebnet.com.cn', 'index.html', ''):
            continue
        # 去除文件扩展名
        slug = p.replace('.html', '').replace('.htm', '')
        # 跳过纯日期串（20260202）或纯数字
        if slug.isdigit() and len(slug) >= 8:
            continue
        # 跳过太短的 slug（通常无意义）
        if len(slug) < 3:
            continue
        return slug
    return None


def _fallback_title(record: dict) -> str:
    """为缺少标题的记录生成兜底标题"""
    analyst = _repair_mojibake(_try_decode(record.get('analystName', '未知分析师')))
    pub = _try_decode(str(record.get('publishedAt', '')))[:10]
    url = record.get('sourceUrl', '')
    from_url = _title_from_url(url)
    if from_url:
        return _repair_mojibake(from_url)
    return f'{analyst} {pub[:10]} 观点'


def _extract_actionable_text(record: dict) -> str:
    """从记录中提取最有行动价值的文字片段"""
    title = _repair_mojibake(_try_decode(record.get('articleTitle', '')))
    vps_raw = record.get('keyViewpoints', [])
    evs_raw = record.get('evidenceSnippets', [])
    vps = [_repair_mojibake(_try_decode(v)) for v in vps_raw]
    evs = [_repair_mojibake(_try_decode(e)) for e in evs_raw]

    # 优先用 viewpoint（行动建议类），其次用 evidence（有数据类）
    for vp in vps:
        if any(k in vp for k in ['建议', '应', '需要', '推动', '关注']):
            return vp[:200]
    for vp in vps:
        if len(vp) > 30:
            return vp[:200]
    for ev in evs:
        if any(k in ev for k in ['亿元', '%', '增长', '下降']):
            return ev[:200]
    return (title + '。' + (vps[0] if vps else ''))[:200]


if __name__ == '__main__':
    main()