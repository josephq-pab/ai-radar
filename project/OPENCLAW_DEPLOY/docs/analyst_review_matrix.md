# analyst_review_matrix.md — 来源有效性评估矩阵

> 文档版本：v1.0（初建）
> 建立日期：2026-04-07
> 对应阶段：P1-2 实施
> 数据来源：analyst_opinions_raw.json / analyst_opinions.json / analyst-review-queue.json / analyst_sources.json
> 样本说明：本轮数据为单轮抓取结果（2026-04-07），结论为**试行版/阶段性建议**，建议在2~3轮试点数据后复核

---

## 评估字段说明

| 列名 | 定义 | 数据来源 |
|------|------|---------|
| sourceId | 来源唯一标识 | analyst_sources.json |
| analystName | 分析师姓名 | analyst_sources.json |
| rawTotal | 原始抓取总记录数 | analyst_opinions_raw.json |
| opsTotal | 进入结构化观点池记录数 | analyst_opinions.json |
| usable | 内容可用（usable=true）记录数 | analyst_opinions.json |
| usableRate | usable / opsTotal | 计算得出 |
| referenceable | 可直接引用（isReferenceable=true）记录数 | analyst_opinions.json |
| refRate | referenceable / usable | 计算得出 |
| enterReport | 进入周报（enterReport=true）记录数 | analyst_opinions.json |
| queueItems | 进入 review_queue（top-5）的条数 | analyst-review-queue.json |
| latestYear | 原始记录中最新年份 | analyst_opinions_raw.json |
| provisionalRecommendation | 试行建议结论 | 人工判定 |

---

## 评估矩阵

| sourceId | analystName | rawTotal | opsTotal | usable | usableRate | referenceable | refRate | enterReport | queueItems | latestYear | provisionalRecommendation |
|----------|------------|----------|----------|--------|------------|--------------|---------|-------------|------------|------------|------------------------|
| analyst-deposit-002 | 薛洪言 | 20 | 15 | 15 | 100% | 12 | 80% | 4 | 4 | 2025 | **keep** |
| analyst-deposit-003 | 娄飞鹏 | 2 | 1 | 1 | 100% | 1 | 100% | 0 | 0 | 2026 | **observe** |
| analyst-deposit-004 | 连平 | 2 | 2 | 2 | 100% | 2 | 100% | 0 | 0 | 2026 | **observe** |
| analyst-deposit-005 | 周茂华 | 2 | 2 | 2 | 100% | 2 | 100% | 1 | 1 | 2026 | **keep** |
| analyst-deposit-006 | 顾慧君 | 20 | 0 | 0 | — | 0 | — | 0 | 0 | 2022 | **pending-check** |
| analyst-deposit-007 | 付一夫 | 20 | 9 | 9 | 100% | 8 | 89% | 0 | 0 | 2024 | **observe** |
| analyst-deposit-008 | 王锟 | 13 | 0 | 0 | — | 0 | — | 0 | 0 | 2019 | **pending-check** |
| analyst-deposit-001 | 董希淼 | 0 | 0 | 0 | — | 0 | — | 0 | 0 | — | **pending-check** |
| analyst-loan-001 | 温彬 | 0 | 0 | 0 | — | 0 | — | 0 | 0 | — | **pending-check** |
| analyst-loan-002 | 曾刚 | 0 | 0 | 0 | — | 0 | — | 0 | 0 | — | **pending-check** |
| analyst-overall-001 | 朱太辉 | 0 | 0 | 0 | — | 0 | — | 0 | 0 | — | **pending-check** |
| analyst-overall-002 | 孙扬 | 0 | 0 | 0 | — | 0 | — | 0 | 0 | — | **pending-check** |
| analyst-overall-003 | 杜娟 | 0 | 0 | 0 | — | 0 | — | 0 | 0 | — | **pending-check** |

---

## 结论分布汇总

| 结论类型 | 来源数 | 来源列表 |
|---------|-------|---------|
| keep | 2 | 薛洪言、周茂华 |
| observe | 3 | 娄飞鹏、连平、付一夫 |
| pending-check | 8 | 顾慧君、王锟、董希淼、温彬、曾刚、朱太辉、孙扬、杜娟 |

---

## 关键发现

1. **薛洪言主导 top-5（4/5）**：review_queue 5条中4条来自薛洪言，但这是排序/OI-03问题，不是来源质量问题
2. **连平/周茂华被挤出 top-5**：连平综合分0.86未被选入周报，周茂华仅1条入选，均为排序截断（OI-03来源权重过重）
3. **付一夫usable=9但0 enterReport**：质量高（VALID=8/ref=8），但被薛洪言文章截断，非来源质量差
4. **顾慧君/王锟 0 usable 原因**：min_year=2024过滤（raw有内容但全在2024年前），非来源质量问题
5. **6个来源0 raw记录**：温彬/曾刚/朱太辉/孙扬/杜娟/董希淼，抓取层未触达，需人工确认来源URL状态
