# 状态源与主从关系说明

**版本**: F11-20260331  
**用途**: 明确各产物的数据主从关系，当出现不一致时知道该信谁、先修谁。

---

## 一、Source of Truth 层级

### 第一层（主状态源，不可替代）

| 文件 | 说明 |
|------|------|
| `reviews/review-log.jsonl` | 所有 review 决策的原始记录，含 semanticAction/editedText/reason 等全部语义 |
| `data/raw/*.xlsx` | 存款/贷款/利率原始数据文件 |

### 第二层（从第一层派生，自动重建）

| 文件 | 生成方式 | 依赖 |
|------|----------|------|
| `reports/review-status.json` | `build_review_status.py` 读取 review-log.jsonl | review-log.jsonl |
| `reports/tracking-items.json` | `build_tracking_items.py` 读取 review-status.json + review-queue.json | review-status.json, review-queue.json |
| `data/processed/deposit_benchmark.json` | `parse_initial_data.py` 读取 raw/*.xlsx | raw/*.xlsx |
| `data/processed/loan_benchmark.json` | 同上 | raw/*.xlsx |
| `data/processed/loan_rate.json` | 同上 | raw/*.xlsx |

### 第三层（从第二层派生，自动重建）

| 文件 | 生成方式 | 依赖 |
|------|----------|------|
| `reports/weekly-report-draft.md` | `generate_weekly_report.py` 读取 tracking-items.json + summary.json 等 | tracking-items.json, summary.json |
| `reports/review-queue.json` | `generate_review_queue.py` 读取 weekly-report-draft.md + analyst_opinions.json | weekly-report-draft.md |
| `reports/app-data.js` | `build_web_bundle.py` 读取各 processed/ 文件 | tracking-items.json, summary.json, deposit_benchmark.json 等 |
| `reports/run-summary.json` | `run-pipeline.py` smoke test 后生成 | 各第二、三层文件 |

---

## 二、主从依赖图

```
review-log.jsonl (第一层)
        ↓
review-status.json (第二层)
        ↓
tracking-items.json (第二层) ← data/raw/*.xlsx (第一层)
        ↓
weekly-report-draft.md (第三层) ← summary.json (第二层)
        ↓
review-queue.json (第三层) ← analyst_opinions.json (第二层)
        ↓
app-data.js (第三层)
        ↓
run-summary.json (第四层)
```

---

## 三、当不一致时应该信谁

### 场景1：run-summary 和 weekly report 数字不一致

**先信**: `reports/tracking-items.json` 的 `trackingStatusSummary`  
**次信**: `reports/review-status.json` 的汇总计数  
**处理**: 重建 tracking-items（`build_tracking_items.py`），然后重建周报

### 场景2：review-status 显示某项已 approve，但 tracking-items 还显示 pending

**先信**: `reviews/review-log.jsonl` 的最后一条记录  
**处理**: 重建 review-status（`build_review_status.py`），然后重建 tracking-items

### 场景3：周报显示旧状态，但 tracking-items 已更新

**原因**: `run-pipeline.py --rebuild-only` 的步骤顺序错误（周报在 tracking 之前跑）  
**处理**: 执行 `run-pipeline.py --rebuild-only`，新版本已修复顺序

### 场景4：raw 数据文件已更新，但 processed JSON 还是旧的

**先信**: `data/raw/*.xlsx` 的 mtime  
**处理**: 执行 `run-pipeline.py --mode full`（而非 rebuild-only）

---

## 四、各产物的重建优先级

| 场景 | 重建顺序 |
|------|----------|
| review 决策已写入，但周报未更新 | ① `build_tracking_items.py` → ② `generate_weekly_report.py` |
| review-status 需要刷新 | ① `build_review_status.py` → ② `build_tracking_items.py` → ③ `generate_weekly_report.py` |
| raw 数据已更新 | `run-pipeline.py --mode full` |
| 只刷新展示层 | `run-pipeline.py --rebuild-only` |

---

## 五、一致性自动校验

smoke_test.py 已增加以下校验：

1. **第九节一致性**: 周报第九节的"待研判：X 项"必须与 `tracking-items.json` 的 `trackingStatusSummary.待研判` 一致，不一致时报 FAIL
2. **trackingStatusSummary 兜底模式**: 若 pending 率 > 80% 且连续 3 次运行未变化，报 WARN
3. **review-queue 兜底模式**: 若 fallback 率 > 50%，报 WARN

---

## 六、最小修复命令

当发现不一致时，依次执行：

```bash
cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station

# 如果 review-log 有新记录，重建 review-status
python3 scripts/build_review_status.py

# 重建 tracking-items（读取最新的 review-status）
python3 scripts/build_tracking_items.py

# 重建周报（读取最新的 tracking-items）
python3 scripts/generate_weekly_report.py

# 完整重建（包含 analyst 抓取）
python3 scripts/run-pipeline.py --mode full
```

---

## 七、何时用哪种运行模式

| 模式 | 何时用 |
|------|--------|
| `--mode full` | raw 数据已更新，或 analyst 来源需要重新抓取 |
| `--rebuild-only` | 只改了 review 决策，或只改了配置/模板 |
| `--mode parse` | 只改了 raw 数据文件 |
| `--mode report` | 只改动了周报模板或生成规则 |
