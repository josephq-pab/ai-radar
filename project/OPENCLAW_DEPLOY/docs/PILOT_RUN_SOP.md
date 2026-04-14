# PILOT_RUN_SOP.md — 试点运行标准操作手册

> 文档版本：v1.6（本次更新：P1-11 增加 --dim-trial 维度扩展试探模式；Step 0 fetch 入口更新）
> 建立日期：2026-04-07
> 对应阶段：P1-3 实施
> 适用范围：双周试点运行（运营编辑者单角色）

---

## 一、目的与适用范围

**目的**：将当前 MVP 能力组织为可执行、可复盘、可持续运行的小规模试点标准操作流程。

**适用范围**：
- 当前仅服务小规模试点运行
- 不适用于正式大规模运营
- 由运营编辑者（单角色）执行

**本手册不是**：
- 系统功能说明书
- 正式运营制度文件
- 多角色协同规范

---

## 二、周期触发条件

### 主触发条件（满足任一即触发）

| 条件 | 说明 |
|------|------|
| **时间触发** | 距上次完整运行已满14天 |
| **数量触发** | 自上次运行以来，新增 raw 记录 ≥5 条 |

### 触发例外

> **例外执行条件**（需显式记录原因）：
> - 明确异常 / OI 需提前复查
> - 用户明确要求推进
>
> **明确不作为例外执行理由**：
> - "只是想验证脚本可跑"不属于有效例外理由
>
> **不进入完整轮次**：若既不满足常规触发，也不满足例外条件，则：
> - 记录"触发检查已执行，本轮无需完整复核"
> - 在 ROUND_RECAP 中注明
> - 不进入 run-analyst.sh 执行

### 当前运行方式

- **人工执行**，无 cron / 自动化调度
- 触发条件由运营编辑者自行判断
- 建议在日历/任务工具中设置14天提醒

---

## 三、角色

**单角色运行**：运营编辑者

- 负责全部操作步骤
- 不做权限拆分
- 后续根据试点需要再评估是否扩展

---

## 四、数据刷新（Step 0 — fetch）

**何时需要执行 fetch**：在启动任何轮次前（包括 preflight），如果距上次 fetch 已经较久，或手动检查发现 fetchedAt 未更新，应先执行 fetch 刷新数据。

### 4.0.1 统一 fetch 入口

```bash
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本

# 方式一：dry-run 模式（安全检查，不写文件）
./run-analyst-fetch.sh --check

# 方式二：正式抓取（默认：对公存款 单一维度）
./run-analyst-fetch.sh

# 方式三：维度扩展试探（对公存款+对公贷款 两次抓取并合并）
# 适用场景：确认当前单一维度已触及瓶颈，需要引入新维度来源时
./run-analyst-fetch.sh --dim-trial
```

### 4.0.2 fetch 后"数据已刷新"判断口径

fetch 完成后，判断数据是否已真正刷新：

| 信号 | 说明 |
|------|------|
| fetchedAt 变化 | 数据已刷新（最新抓取时间已更新）|
| raw 条数变化 | 有新增记录进入池 |
| fetchedAt 变化 + 条数增加 | 完整刷新，新增内容需进一步判断 |

**注意**："数据已刷新" ≠ "值得跑下一轮"。是否值得跑由 Step 1 preflight 判断。

**若 fetch 后数据无变化**：说明当前数据源无新增，维持现状，等待下次 fetch 时机。

### 4.0.3 当前 fetch 层与 run-analyst.sh 的关系

```
fetch_analyst_articles.py（抓取）
    ↓ 产出 analyst_opinions_raw.json
run-analyst.sh（构建 → queue → merge → export）
```

两者完全分离：fetch 负责刷新数据，run-analyst.sh 负责处理已存在的数据。不要将两者自动串联。

---

## 五、每轮开始前检查（Preflight）

**重要**：每次启动轮次前，必须先完成以下 preflight 检查，不得直接执行 run-analyst.sh。

### 4.1 raw 新增快速检查

```bash
# 读取当前 raw 数据状态
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/04_数据与规则/processed
cat analyst_opinions_raw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
records = d.get('records', [])
fetched_at = d.get('fetchedAt', 'unknown')
print(f'raw 总记录数: {len(records)}')
print(f'fetchedAt: {fetched_at}')
"
```

对比上轮 ROUND_RECAP 中记录的 raw 总数，判断新增数量。

### 4.2 触发判断（按顺序判断，满足即停止）

**A. 数量触发（常规执行）**
- 若 raw 新增 ≥5 条 → 直接进入 run-analyst.sh

**B. 时间触发（常规执行）**
- 若距上次已满 14 天 → 直接进入 run-analyst.sh

**C. 例外执行（需显式记录原因）**
- 若存在以下情况，可例外执行：
  - 明确异常 / OI 需提前复查
  - 用户明确要求推进
- 必须在 ROUND_RECAP 中显式写明例外执行原因

**D. 不进入完整轮次**
- 若 A/B/C 均不满足 → 本轮不进入完整执行
- 记录"触发检查已执行，本轮无需完整复核"
- 在 ROUND_RECAP 中注明

**D-续. fetchedAt 已变化但 raw 未达触发（需人工判断）**

> 这是 D 的补充路径。当 fetchedAt 发生变化（说明数据已刷新），但 raw 净增 <5 且距上次未满 14 天时：
>
> **信号**：fetchedAt 变化 + raw 净增 <5
> **可能原因**：内容替换型刷新（去重替换旧文，而非净新增）
> **操作**：不自动进入轮次，但运营编辑者应：
> 1. 查看 queue 条目（`generate_review_queue.py` 输出）是否需要刷新
> 2. 若 queue 中的条目已明显陈旧 → 可考虑进入轮次（走例外执行路径 C，需记录原因）
> 3. 若 queue 仍有效 → 维持 D 结论
>
> **注意**：当前无法自动区分"内容是否真的被替换"，该判断需人工完成。
> 当没有 pre-fetch 快照时，运营编辑者的主观判断是唯一判断依据。

### 4.3 确认工作目录

```
/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/
```

---

## 六、每轮执行步骤

### Step 1：运行采集与构建（analyst 统一入口）

```bash
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本
OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY \
./run-analyst.sh
```

**说明**：本脚本为 analyst 试点运行专用统一入口（run-analyst.sh），执行 orchestration 调用：
1. `build_analyst_opinions.py`
2. `generate_review_queue.py`
3. `review-tracker.py merge`
4. `review-tracker.py export`

> **历史说明**：`run-pipeline.py` 为 Phase 2 旧入口，路径和依赖已过时，本阶段不作为 analyst 试点入口使用。

**输出**：
- `04_数据与规则/processed/analyst_opinions_raw.json`（追加/覆盖）
- `04_数据与规则/processed/analyst_opinions.json`（覆盖）
- `reports/analyst-review-queue.json`（覆盖，top-5）

**预期**：
- raw 新增记录出现
- usable 池有新条目
- review_queue 更新

### Step 2：更新 tracker 状态

对上一轮 pending 的 items 进行 upsert（运营编辑者判断）：

```bash
# 语法
OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY \
/tmp/py39env/bin/python 05_工具脚本/review-tracker.py upsert \
  --item-id <itemId> \
  --review-status <pending|confirmed|rejected> \
  --tracking-status <pending|candidate|follow_up|closed> \
  --note "<可选备注>"
```

**示例**（review 后状态）：
```bash
OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY \
/tmp/py39env/bin/python 05_工具脚本/review-tracker.py upsert \
  --item-id analyst-72873eb4 \
  --review-status confirmed \
  --tracking-status follow_up \
  --note "薛洪言护城河观点，与对公存款维度高度相关，建议保留"
```

**状态枚举说明**：

| 字段 | 可选值 | 说明 |
|------|--------|------|
| reviewStatus | `pending` | 待 review |
| reviewStatus | `confirmed` | 确认有效 |
| reviewStatus | `rejected` | 驳回 |
| trackingStatus | `pending` | 待处理 |
| trackingStatus | `candidate` | 候选 |
| trackingStatus | `follow_up` | 跟进中 |
| trackingStatus | `closed` | 已关闭 |

**review 后典型流转**：
- 确认并跟进：`reviewStatus=confirmed` + `trackingStatus=follow_up`
- 确认并关闭：`reviewStatus=confirmed` + `trackingStatus=closed`
- 驳回：`reviewStatus=rejected` + `trackingStatus=closed`

### Step 3：导出轻量台账

```bash
OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY \
/tmp/py39env/bin/python 05_工具脚本/review-tracker.py export \
  --output reports/pilot-tracking-ledger.csv
```

**输出**：`reports/pilot-tracking-ledger.csv`（UTF-8-sig BOM，Excel/飞书可直接打开）

**用途**：人工可读快照，记录当前所有 items 的状态

### Step 4：人工 review 与判断

1. 打开 `pilot-tracking-ledger.csv`
2. 对新出现的 pending items 做判断
3. 对已 review 的 items 根据判断更新状态
4. 将判断结果通过 Step 2 的 upsert 写入 tracker

---

## 七、每轮结束后产出

| 产出 | 说明 | 必须/可选 |
|------|------|---------|
| analyst-review-queue.json | 当前 queue 状态 | 系统自动生成 |
| review-tracker.json | 当轮 upsert 结果 | 必须 |
| pilot-tracking-ledger.csv | 当轮台账快照 | 必须 |
| ROUND_RECAP（填写） | 当轮小结 | 必须 |
| ROUND_COMPARISON（更新） | 跨轮数字对比表 | 必须（每轮追加一行） |

**ROUND_COMPARISON 填写时点**：每轮结束后，与 ROUND_RECAP 同时填写。字段见 `reports/ROUND_RECAP/ROUND_COMPARISON.md`。

---

## 八、来源复核触发条件

以下情况需更新 `analyst_review_matrix.md` / `analyst_review_notes.md`：

| 触发条件 | 说明 |
|---------|------|
| **周期触发** | 距上次复核满4~6周 |
| **usable 数量大幅变化** | 某来源的 usable 数量变化超过 ±3 条 |
| **首次出现 raw** | 某来源首次出现 raw 记录（如董希淼、温彬等0 raw来源开始有数据） |
| **queue 贡献明显变化** | 某来源在 top-5 中的占比发生显著变化 |
| **长期0 usable 来源状态变化** | 顾慧君/王锟等原本 0 usable 的来源出现新 raw |

**来源复核操作**：
1. 重新统计各来源的 raw/ops/usable/ref/enterReport 数量
2. 更新 matrix 对应行的数值
3. 检查 notes 中该来源的结论是否需要调整
4. 在 ROUND_RECAP 中记录"来源复核已执行"

---

## 九、只记台账不升级的情况

以下情况**不进入 OPEN_ISSUES**，只在 ROUND_RECAP 中记录：

- 单纯 confirmLevel 与期望不符但无实质影响
- 单条 enterReport 数量波动但无系统性变化
- 排序结果受 top-k 截断影响（薛洪言主导 top-5，OI-03 相关）
- 某来源单轮 usable 数量轻微波动（±1~2条）
- review queue 数量因 raw 数据变化自然波动

---

## 十、需进入 OPEN_ISSUES 的情况

以下情况需在 ROUND_RECAP 中标注，并建议进入 OPEN_ISSUES：

- 发现新来源抓取失败（非预期，且非平台壁垒）
- 某来源抓取逻辑异常（如 raw 数量大幅下降）
- review 判断与 confirmLevel 系统性偏离（如 P1 级被大量驳回）
- 任何影响试点正常推进的异常
- Gate A 数据持续缺失（外部依赖）

---

## 十一、当前不做事项

- ❌ 不做自动 cron / 调度
- ❌ 不做 UI 按钮 / 前端页面
- ❌ 不做数据库 / 服务端持久层
- ❌ 不做多角色权限体系
- ❌ 不做完整任务系统
- ❌ 不做 analyst_sources.json 自动生效修改
- ❌ 不做 confirmLevel 规则重构
- ❌ 不做评分权重 / top-k 调整
- ❌ 不把本 SOP 上升为正式运营制度
