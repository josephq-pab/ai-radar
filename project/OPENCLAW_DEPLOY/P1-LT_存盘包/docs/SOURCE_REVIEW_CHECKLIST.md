# SOURCE_REVIEW_CHECKLIST.md — 来源复核触发条件与核查要点

> 文档版本：v1.0（初建）
> 建立日期：2026-04-07
> 对应阶段：P1-3 试点运行
> 依据：analyst_review_matrix.md / analyst_review_notes.md（2026-04-07 版）

---

## 一、目的

本清单用于判断何时需要更新 `analyst_review_matrix.md` 和 `analyst_review_notes.md`。
**不是**：正式治理规则 / analyst_sources.json 自动变更依据。

---

## 二、复核触发条件

以下任一条件满足时，需触发来源复核：

| # | 触发条件 | 说明 |
|---|---------|------|
| T1 | 距上次复核满4~6周 | 时间触发，建议每月一次 |
| T2 | 某来源 usable 数量变化超过 ±3 条 | 数量触发，需对比上一轮 matrix |
| T3 | 某来源首次出现 raw 记录 | 如原本 0 raw 的温彬/曾刚等开始有数据 |
| T4 | 某来源在 top-5 中占比发生显著变化 | 如某来源从0条突然变多条 |
| T5 | 长期0 usable 来源状态改变 | 如顾慧君/王锟出现2024年后新文章 |

---

## 三、触发后的操作

### 3.1 重新统计

对照 `analyst_opinions_raw.json` / `analyst_opinions.json` / `analyst-review-queue.json`，重新统计：

```bash
# 统计某来源 usable 数量
/tmp/py39env/bin/python -c "
import json
ops = json.load(open('04_数据与规则/processed/analyst_opinions.json'))
recs = [r for r in ops.get('records',[]) if r.get('analystName','') == 'XXX']
usable = [r for r in recs if r.get('isUsable', False)]
print(f'usable: {len(usable)} / {len(recs)}')
"
```

### 3.2 更新 matrix

编辑 `docs/analyst_review_matrix.md`，更新对应来源的行：
- 填入新的 rawTotal / opsTotal / usable / referenceable / enterReport / queueItems
- 重新判定 provisionalRecommendation

### 3.3 更新 notes

编辑 `docs/analyst_review_notes.md`，对应来源的结论段落：
- 若判断发生变化（如 observe → keep），在段落中更新结论并说明原因
- 若判断不变，可补充新的观察证据

### 3.4 记录复核历史

在 ROUND_RECAP 中注明：
- 触发条件（T1~T5）
- 复核日期
- 主要变化摘要

---

## 四、本轮（2026-04-07）初始状态参考

| 来源 | 当前结论 | 建议下次复核时间 |
|------|---------|---------------|
| 薛洪言 | keep | 2026-05-07（~4周）|
| 周茂华 | keep | 2026-05-07 |
| 连平 | observe | 2026-05-07 |
| 娄飞鹏 | observe | 2026-05-07 |
| 付一夫 | observe | 2026-05-07 |
| 顾慧君 | pending-check | 发现2024年后新文章时 |
| 王锟 | pending-check | 发现2024年后新文章时 |
| 温彬/曾刚/朱太辉/孙扬/杜娟 | pending-check | 首次出现 raw 时 |
| 董希淼 | pending-check（已inactive） | 无需主动复核 |

---

## 五、不触发复核的正常波动

以下情况**不需要**更新 matrix / notes：

- 某来源单轮 usable 数量 ±1~2 条的正常波动
- confirmLevel 分布略有变化但无系统性偏离
- queue 中顺序的正常轮换
- 某来源 enterReport 从0变1或从1变0的单次波动

这些情况记入当轮 ROUND_RECAP 的"本轮新发现"即可。
