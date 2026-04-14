# 月度数据导入操作手册

## 概述

本文档定义 benchmark/rate 核心数据的月度更新流程。

---

## 一、数据文件约定

### 输入位置

```
data/raw/
├── 存款对标数据_YYYYMM.xlsx
├── 贷款对标数据_YYYYMM.xlsx
└── 利率数据_YYYYMM.xlsx
```

### 输出位置

```
data/processed/
├── deposit_benchmark.json
├── loan_benchmark.json
└── loan_rate.json
```

---

## 二、导入流程

### Step 1: 准备新文件

1. 从业务方获取最新月度数据文件
2. 检查文件格式是否与现有文件一致
3. 将文件放入 `data/raw/` 目录

### Step 2: 更新配置

编辑 `config/source_files.json`，更新文件名：

```json
{
  "files": [
    "存款对标数据_202603.xlsx",
    "贷款对标数据_202603.xlsx", 
    "利率数据_202603.xlsx"
  ]
}
```

### Step 3: 执行导入

```bash
cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station

# 方式一：完整刷新（推荐）
python3 scripts/run-pipeline.py --mode full

# 方式二：仅解析数据
python3 scripts/parse_initial_data.py
```

### Step 4: 校验结果

```bash
# 检查生成的 JSON 文件
python3 -c "
import json
for f in ['deposit_benchmark', 'loan_benchmark', 'loan_rate']:
    with open(f'data/processed/{f}.json') as fp:
        data = json.load(fp)
    print(f'{f}: {len(data)} 条记录')
"
```

### Step 5: 确认导入成功

检查 `reports/run-summary.json`：

```json
{
  "dataFreshness": {
    "observedAt": {
      "deposit_benchmark.json": "2026-03-31",
      "loan_benchmark.json": "2026-03-31",
      "loan_rate.json": "2026-03-01"
    },
    "stale": false
  }
}
```

---

## 三、校验逻辑

### 必要校验

| 检查项 | 通过条件 |
|--------|----------|
| 文件存在 | 文件在 `data/raw/` 目录中 |
| 文件可读 | 能正常打开和解析 |
| 格式正确 | 列名与现有文件一致 |
| 数据非空 | 至少有 1 条有效记录 |

### 校验脚本

```python
import json
from pathlib import Path

def validate_import():
    files = ['deposit_benchmark', 'loan_benchmark', 'loan_rate']
    results = []
    
    for f in files:
        path = Path(f'data/processed/{f}.json')
        if not path.exists():
            results.append((f, 'FAIL', '文件不存在'))
            continue
        
        with open(path) as fp:
            data = json.load(fp)
        
        if not data:
            results.append((f, 'FAIL', '数据为空'))
        else:
            results.append((f, 'PASS', f'{len(data)} 条记录'))
    
    return results
```

---

## 四、当前阻塞状态

### 状态：等待新文件

| 项目 | 说明 |
|------|------|
| **当前数据时间** | 2026-02-28 |
| **当前状态** | 偏旧（31 天） |
| **阻塞原因** | 无 2026-03 月度原始文件 |
| **解除条件** | 获取并导入 2026-03 数据文件 |

### 运行摘要中已暴露

```json
{
  "dataFreshness": {
    "assessment": {
      "benchmark_level": "偏旧",
      "benchmark_age_days": 31
    },
    "blocked": true,
    "blockedReason": "等待 2026-03 月度数据文件"
  }
}
```

---

## 五、导入演练记录

### 演练说明

当前无 2026-03 新文件，以下为演练流程（非真实导入）：

1. **假设场景**：收到 `存款对标数据_202603.xlsx`
2. **操作步骤**：
   - 将文件放入 `data/raw/`
   - 更新配置
   - 运行 `python3 scripts/run-pipeline.py --mode full`
3. **预期结果**：
   - `deposit_benchmark.json` observedAt 更新为 2026-03-31
   - `reports/change-summary.json` 显示文件已更新

**状态**：流程已固化，等待真实文件导入

---

## 六、负责人与时间

| 事项 | 责任人 | 时间 |
|------|--------|------|
| 获取新数据文件 | 业务分析师 | 每月 5 日前 |
| 导入校验 | 数据管理员 | 收到文件后 1 日内 |
| 确认可用 | 邱非 | 导入后确认 |
