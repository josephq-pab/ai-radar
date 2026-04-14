# Change Summary - F9-20260331

**版本**: F9 抓取质量修复 + 人工决策提效 + 月度导入就绪
**生成时间**: 2026-03-31T16:35:00+08:00
**运行模式**: rebuild-only (fetch受网络限制未能live执行)

---

## 本轮主要变化

### 脚本修复

| 文件 | 修复内容 |
|------|----------|
| scripts/fetch_analyst_articles.py | 编码修复、标题提取优先级、URL日期校验、域名超时、重试机制修复 |
| scripts/build_analyst_opinions.py | _repair_mojibake增加GBK方案、_title_from_url避免短slug |

### 新增产物

| 文件 | 说明 |
|------|------|
| scripts/import_monthly_data.py | 月度导入专用入口，dry-run + confirm 模式 |
| reports/review-decision-pack.md | Top 5 + 续处理项决策包（可打印/直接使用） |
| reports/review-decision-pack.json | 决策包结构化版 |
| reports/monthly-import-readiness.md | 月度导入就绪报告 |
| reports/monthly-import-readiness.json | 月度导入就绪JSON版 |

---

## 下一步行动

| 角色 | 动作 | 时间 |
|------|------|------|
| 邱非 | 处理Top 5 pending | 本周一/二 |
| 业务分析师 | 获取2026-03数据文件 | 每月5日前 |
| 数据管理员 | 导入新文件 | 收到文件后当日 |
| (网络恢复后) | 重新抓取验证修复效果 | 验证后 |

---

# Change Summary - F10-20260331-正式决策执行

**版本**: F10 正式决策落地
**执行时间**: 2026-03-31T17:09:00+08:00
**执行模式**: dry-run → 正式写入 → rebuild验证

---

## 一、执行前摘要

| 项目 | 内容 |
|------|------|
| 决策数量 | 11条（含1个拆分确认） |
| 执行前 pending | 14 / 17 |
| 执行后 pending | 3 / 17 |
| 执行链路 | record_review.py → build_review_status.py → run-pipeline.py rebuild |
| 备份 | reviews/review-log.jsonl.bak-20260331170900 |

---

## 二、决策落地结果

### 直接 approve（5条）

| itemId | 状态 | 写入 | 关键内容 |
|--------|------|------|----------|
| core-2 | approve | ✅ | 贷款格局核心结论 |
| b152aadd3128 | approve | ✅ | 平安银行差距拆解框架 |
| db0e95bbf972 | approve | ✅ | 本周优先行动：差距拆解 |
| e0577e72a2ab | approve | ✅ | 四维联动框架 |
| 2000687cea45 | approve | ✅ | 产品结构+定价+风险收益并列 |

### modify 后通过（3条）

| itemId | 状态 | 写入 | 关键修改 |
|--------|------|------|----------|
| 71fb598e78c9 | modify | ✅ | 补月份标注"（2026-02）" |
| 7321bf1067d1 | modify | ✅ | "重点观察"→"建议结合"（行动导向） |
| 9334692ed21f | modify | ✅ | "优先推动"→"本周推动" |

### 拆分确认（1条，关联落地3条）

| itemId | 状态 | 写入 | 说明 |
|--------|------|------|------|
| 8e2abb43cefd | approve | ✅ | 批准拆分：b87627d97665升级策略；1dbd4051cc58继续pending；76e4940707f4保持reject |
| b87627d97665 | pending（待升级） | ⚠️ | queue中category仍为观察提示，系统限制无法自动升级 |
| 1dbd4051cc58 | pending | ✅ | 继续pending（按拆分决定） |
| 76e4940707f4 | rejected | ✅ | 保持reject（按拆分决定） |

### 用户补充信息落地（2条 modify）

| itemId | 状态 | 写入 | 关键修改 |
|--------|------|------|----------|
| 5e0503d31a25 | modify | ✅ | 补全重点同业：招商银行、中信银行 |
| 568dac78e5a7 | modify | ✅ | 补全优先拆解方向：存款差距来源+贷款产品/行业 |

---

## 三、review-status 最终状态

| 状态 | 数量 |
|------|------|
| approve | 7 |
| modify | 6 |
| pending | 3 |
| reject | 1 |
| **合计** | **17** |

pending 3项：`b87627d97665`（升级待手动）、`1dbd4051cc58`（等3月利率）、`581527c09784`（用户选A）

---

## 四、tracking-items 状态变化

| 指标 | 执行前 | 执行后 |
|------|--------|--------|
| 待研判 | 14 (82%) | 3 (18%) |
| 跟踪中 | 1 | 6 |
| 已上报 | 1 | 7 |
| 已行动 | 0 | 0 |
| 已关闭 | 1 | 1 |

---

## 五、run-summary trustSummary（关键片段）

```json
"trackingPending": 3,
"trackingTotal": 17,
"pendingRate": "18%",
"trackingStatusSummary": {
  "待研判": 3,
  "跟踪中": 6,
  "已上报": 7,
  "已行动": 0,
  "已关闭": 1
}
```

---

## 六、系统限制说明

### `b87627d97665` 无法自动从"观察提示"升级为"策略建议"

原因：`build_review_queue.py` 从周报草稿提取 queue items 时，category 字段由周报章节决定，无法通过 `review-log.jsonl` 写入修改。

近似落地方式：`8e2abb43cefd`（approve）中已记录拆分决定，b87627d97665 的新文本和升级意图已在 editedText 中注明。系统层面该 item 仍为 pending category="观察提示"。

如需彻底解决，需手动修改 `reports/review-queue.json` 中 b87627d97665 的 category 字段为"策略建议"，然后重建。

---

## 七、备份位置

```
reviews/review-log.jsonl.bak-20260331170900
```

如需回滚：
```bash
cp reviews/review-log.jsonl.bak-20260331170900 reviews/review-log.jsonl
python3 scripts/build_review_status.py
```
