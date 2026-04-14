# 对公 AI 雷达站 — Smoke 检查清单（SMOKE_CHECKLIST）

> 本文件列出 smoke test 的检查维度，每项对应 run_smoke.sh 的实际检查点。
> 建立时间：2026-04-07

---

## 检查维度总览

smoke test 共 38 项，分 6 个维度：

| 维度 | 检查项数 | 通过标准 |
|------|---------|---------|
| A. Pipeline 链路完整性 | ~8 项 | 所有 JSON 文件生成且非空 |
| B. 中间层 JSON 一致性 | ~10 项 | 文件间 `observedAt` 时间戳一致 |
| C. Review Queue 有效性 | ~5 项 | queue 非空，字段完整，无乱码 |
| D. Tracking 状态闭环 | ~5 项 | 所有条目有明确 status |
| E. 周报内容完整性 | ~5 项 | 第一节非空，数据标注月份 |
| F. Bundle 可用性 | ~5 项 | app-data.js 存在、大小合理、格式正确 |

---

## A. Pipeline 链路完整性

- [ ] `deposit_benchmark.json` 存在且非空
- [ ] `loan_benchmark.json` 存在且非空
- [ ] `loan_rate.json` 存在且非空
- [ ] `review-queue.json` 存在且非空
- [ ] `review-status.json` 存在且非空
- [ ] `tracking-items.json` 存在且非空
- [ ] `weekly-report-draft.md` 存在且非空
- [ ] `app-data.js` 存在且非空

---

## B. 中间层 JSON 一致性

- [ ] `deposit_benchmark.json` 的 `observedAt` 与 `loan_benchmark.json` 的 `observedAt` 一致
- [ ] `deposit_benchmark.json` 的 `observedAt` 与 `loan_rate.json` 的 `observedAt` 一致（若数据同月）
- [ ] 各 JSON 的 `observedAt` 与文件名/内容月份一致
- [ ] `deposit_benchmark.json` 数据条数 ≥ 8 家银行
- [ ] `loan_benchmark.json` 数据条数 ≥ 8 家银行
- [ ] `loan_rate.json` 数据条数 ≥ 4 家银行
- [ ] 各 JSON 中 `balance`、`rate` 字段为数值类型（非空）
- [ ] 各 JSON 无明显异常值（如负数余额、>20% 利率）

---

## C. Review Queue 有效性

- [ ] `review-queue.json` 长度 ≥ 1
- [ ] 每条 `id` 唯一，无重复
- [ ] 每条有 `summary`、`priority`、`source` 字段
- [ ] 无乱码（UTF-8 解码正常，无 `\ufffd`）
- [ ] 无纯占位内容（如"待补充"、"TODO"）

---

## D. Tracking 状态闭环

- [ ] `tracking-items.json` 长度 ≥ 1
- [ ] 每条有 `id`、`status`、`priority`、`summary` 字段
- [ ] `status` 值在允许集合内：{pending, in_review, accepted, rejected, closed, done}
- [ ] 无悬空引用（无对应 review 记录的 tracking 项）
- [ ] `review-status.json` 与 `review-queue.json` 条目一一对应

---

## E. 周报内容完整性

- [ ] `weekly-report-draft.md` 第一节"核心结论摘要"非空（> 50 字符）
- [ ] 利率数据携带月份标注（如"（2026-02）"）
- [ ] 存款对标数据 ≥ 4 家股份行
- [ ] 无重复段落或内容矛盾
- [ ] 无纯模板占位符残留（如"[栏目口径]"）

---

## F. Bundle 可用性

- [ ] `app-data.js` 存在
- [ ] 文件大小 > 50KB
- [ ] 包含 `window.APP_DATA` 注入
- [ ] `APP_DATA.deposit`、`APP_DATA.loan`、`APP_DATA.rate` 字段存在
- [ ] JSON 格式无语法错误（JS 可正常解析）

---

## 当前运行结果（2026-04-07）

```
smoke test: ✅ 38 / ⚠️ 0 / ❌ 0
```

**全部通过。**

---

## 快速定位失败项

如 smoke test FAIL，查看输出中 `❌` 行，对照上表定位维度：

| 输出关键词 | 可能问题 |
|-----------|---------|
| `observedAt mismatch` | B. 中间层 JSON 一致性 |
| `queue empty` | C. Review Queue 有效性 |
| `tracking status unclear` | D. Tracking 状态闭环 |
| `report section empty` | E. 周报内容完整性 |
| `bundle size too small` | F. Bundle 可用性 |
| `file not found` | A. Pipeline 链路完整性 |

---

## 手动快速检查命令

```bash
# 快速链路检查（不启动前端）
bash scripts/run_smoke.sh --fast

# 完整检查
bash scripts/run_smoke.sh --full

# 检查特定维度
bash scripts/run_smoke.sh --parse-only      # 仅 A
bash scripts/run_smoke.sh --queue-only      # 仅 C
bash scripts/run_smoke.sh --tracking-only   # 仅 D
bash scripts/run_smoke.sh --report-only     # 仅 E
bash scripts/run_smoke.sh --bundle-only     # 仅 F
```
