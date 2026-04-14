# 对公 AI 雷达站 — 运行摘要

**Run ID:** `20260407-013053`
**时间:** 2026-04-07 01:30 UTC
**持续:** 0.0s

**总体结论:** ✅ 本次可正常用于浏览、内部讨论和汇报前准备

**smoke test:** ✅38  ⚠️0  ❌0


## 可用性分级

**✅ browseReadiness:** 主链路一致，bundle 新鲜，页面可正常浏览
  → 以 go-live-gate.json 为准

**✅ internalDiscussionReadiness:** 主链路一致，bundle 新鲜，页面可正常浏览
  → 以 go-live-gate.json 为准

**⚠️ reportPrepReadiness:** 存在限制条件，引用时需注明
  → 以 go-live-gate.json 为准

**数据模式:** real（文件名含版本标识或文件新鲜（7天内）: ['贷款利率-2602.xlsx', '股份行人行口径贷款对标数据260228.xlsx', '贷款对标数据_2026年3月.xlsx', '2026年2月同业对标数据_更新格式_余额和年日均.xlsx', '存款对标数据_2026年3月.xlsx']）

## 核心产物状态

| 产物 | 状态 | 大小 | 记录数 | 修改时间 |
|---|---|---|---|---|
| `deposit_benchmark.json` | ✅ | 12.8KB | - | 09:30 |
| `loan_benchmark.json` | ✅ | 4.8KB | - | 09:30 |
| `loan_rate.json` | ✅ | 4.9KB | - | 09:30 |
| `review-queue.json` | ✅ | 13.4KB | 15 | 09:30 |
| `review-status.json` | ✅ | 6.6KB | 15 | 09:30 |
| `tracking-items.json` | ✅ | 15.9KB | 15 | 09:30 |
| `weekly-report-draft.md` | ✅ | 21.5KB | - | 09:30 |
| `app-data.js` | ✅ | 132.9KB | - | 09:30 |
| `analyst_opinions.json` | ✅ | 29.6KB | 0 | 09:30 |

## 可信度摘要

- review queue 模式: **real** (0/15 条兜底)
- tracking 状态: 待研判 1/15 (7%)
  - 已上报: 8 项
  - 已关闭: 2 项
  - 已行动: 0 项
  - 待研判: 1 项
  - 跟踪中: 4 项
- analyst 层: 6 条有效，0 条乱码，1 条空/占位
  - ⚠️ 有效 6 条 | 乱码 0 条 | 空/占位 1 条 | analyst 层可引用 6 条，可参考 1 条，0 条乱码不可引用
  - lastReviewAt: 2026-04-01T20:15:18
  - ⚠️ 静默 pending（无 review 记录）: 1 项
    - 0d413c5ada98 | 平安银行当前"境内本外币存款"余额约 23,156.56，较上月变动 1,308
- loan dedup: 去重后 11 条
  - ℹ️ dedup风险: 若源 Excel 新版本出现在后面（新行），可能因保留第一条而丢失最新数据。

## 数据新鲜度

- ✅ `deposit_benchmark.json` observedAt: 2026-03-31
- ✅ `loan_benchmark.json` observedAt: 2026-03-31
- ⚠️ `loan_rate.json` observedAt: 2026-02-01
- analyst_opinions fetchedAt: 2026-04-07