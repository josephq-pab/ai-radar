# 月度数据导入总结

**版本**: F8-20260331  
**更新时间**: 2026-03-31 11:44 +08:00

---

## 一、当前数据状态

| 数据集 | observedAt | 文件 | 新鲜度 |
|--------|-----------|------|--------|
| deposit_benchmark | 2026-02-28 | 2026年2月同业对标数据_更新格式_余额和年日均.xlsx | ⚠️ 偏旧(31天) |
| loan_benchmark | 2026-02-28 | 股份行人行口径贷款对标数据260228.xlsx | ⚠️ 偏旧(31天) |
| loan_rate | 2026-02-01 | 贷款利率-2602.xlsx | 🔴 过旧(58天) |

---

## 二、本轮执行状态

### 状态：流程已固化，等待2026-03月度原始文件

**本轮为演练验证（非真实导入）**

本轮在无新文件的情况下，执行了流程验证：
- ✅ 导入流程文档已就位
- ✅ 校验脚本可执行
- ✅ 运行摘要可正确暴露数据陈旧状态
- ❌ 无法执行真实导入（无新文件）

### 当前阻塞点

| 阻塞项 | 说明 | 解除条件 |
|--------|------|----------|
| deposit_benchmark 新文件 | 需要2026年3月存款对标数据 | 业务方提供新文件 |
| loan_benchmark 新文件 | 需要2026年3月贷款对标数据 | 业务方提供新文件 |
| loan_rate 新文件 | 需要2026年3月利率数据 | 业务方提供新文件 |

---

## 三、运行摘要中的陈旧暴露

当前 `reports/run-summary.json` 中已正确暴露：

```json
{
  "dataFreshness": {
    "raw_file_mtimes": {
      "股份行人行口径贷款对标数据260228.xlsx": "2026-03-28",
      "2026年2月同业对标数据_更新格式_余额和年日均.xlsx": "2026-03-28",
      "贷款利率-2602.xlsx": "2026-03-28"
    },
    "observedAt": {
      "deposit_benchmark.json": "2026-02-28",
      "loan_benchmark.json": "2026-02-28",
      "loan_rate.json": "2026-02-01"
    },
    "raw_age_days": 2,
    "stale": false,
    "assessment": {
      "benchmark_age_days": 31,
      "benchmark_level": "偏旧",
      "loan_rate_age_days": 58,
      "loan_rate_level": "过旧"
    }
  }
}
```

---

## 四、拿到新文件后的导入步骤

### Step 1: 放置文件

将收到的2026年3月数据文件放入 `data/raw/`：
```
data/raw/
├── 2026年3月同业对标数据_更新格式_余额和年日均.xlsx  (替换原存款文件)
├── 股份行人行口径贷款对标数据260228.xlsx              (替换原贷款文件)
└── 贷款利率-2603.xlsx                                (替换原利率文件)
```

### Step 2: 执行导入

```bash
cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station
python3 scripts/run-pipeline.py --mode full
```

### Step 3: 验证结果

```bash
# 检查 observedAt 是否更新
cat reports/run-summary.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('deposit:', d['dataFreshness']['observedAt']['deposit_benchmark.json'])
print('loan:', d['dataFreshness']['observedAt']['loan_benchmark.json'])
print('rate:', d['dataFreshness']['observedAt']['loan_rate.json'])
"
```

### Step 4: 预期通过项

| 校验项 | 预期结果 |
|--------|----------|
| deposit_benchmark.json | 33条记录，observedAt = 2026-03 |
| loan_benchmark.json | 20条记录，observedAt = 2026-03 |
| loan_rate.json | 16条记录，observedAt = 2026-03 |

---

## 五、负责人与时间

| 事项 | 责任人 | 时间 |
|------|--------|------|
| 获取2026-03存款/贷款/利率数据文件 | 业务分析师 | 每月5日前 |
| 放置文件到 data/raw/ | 数据管理员 | 收到文件当日 |
| 执行导入并验证 | 数据管理员 | 放置文件后1小时内 |
| 确认数据可用 | 邱非 | 导入后当日确认 |

---

## 六、历史导入记录

| 日期 | 类型 | 说明 |
|------|------|------|
| 2026-03-28 | 初始导入 | deposit_benchmark, loan_benchmark, loan_rate 全部从原始Excel导入 |
| 2026-03-31 | 本轮验证 | 流程验证，无新文件导入 |
