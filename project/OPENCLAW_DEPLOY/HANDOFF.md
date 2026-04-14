# 对公 AI 雷达站 — 交接文档（HANDOFF）
## 第一轮开发迭代 | 2026-04-08

> 本文件记录第一轮开发迭代（2026-04-07 ~ 2026-04-08）的关键决策、产出、入口、
> 已知问题和回退/接续操作。
> 本次交接：系统迁移后 → 第一轮开发迭代完成状态

---

## 一、迭代周期

- **起始**：2026-04-07（系统从旧路径迁移完成，HANDOFF v1 创建）
- **结束**：2026-04-08（第一轮开发迭代完成）
- **迭代定位**：试点运行机制搭建 + analyst 试运行

---

## 二、关键架构说明

### 2.1 当前有效路径

| 路径类型 | 路径 | 说明 |
|---------|------|------|
| **主项目根目录** | `.../workspace-ai-radar/project/OPENCLAW_DEPLOY/` | 当前开发/运行路径 |
| **旧路径（只读备份）** | `.../workspace/ai-radar-station/OPENCLAW_DEPLOY/` | 历史备份，不再开发 |
| **reports/ 是 symlink** | `→ /home/admin/.openclaw/workspace/ai-radar-station/OPENCLAW_DEPLOY/06_进展状态` | ⚠️ 写入 reports/ 的文件实际落入旧路径 |
| **真实 reports** | `.../workspace/ai-radar-station/OPENCLAW_DEPLOY/06_进展状态/` | symlink 指向位置 |

**重要**：任何通过 `reports/` 写入的文件（如 pilot-tracking-ledger.csv、ROUND_RECAP 等）实际落在旧路径。如需备份或迁移，接续方应同时保留新旧路径。

---

## 三、入口清单（已验证可用）

### 3.1 analyst 试点运行入口（核心）

```bash
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本

# Step 0: 数据刷新（可选，视需要）
./run-analyst-fetch.sh              # 真实抓取，刷新 analyst_opinions_raw.json
./run-analyst-fetch.sh --check      # dry-run 安全检查，不写文件

# Step 1: preflight 判断
#   读取 analyst_opinions_raw.json 的 fetchedAt 和条数
#   判断是否满足 A/B/C 触发条件
#   参考 PILOT_RUN_SOP.md Section 五

# Step 2: 满足条件则执行
./run-analyst.sh                    # build → queue → merge → export
```

### 3.2 底层脚本（不推荐直接调用）

| 脚本 | 用途 | 备注 |
|------|------|------|
| `build_analyst_opinions.py` | 构建 analyst opinions | 被 run-analyst.sh 调用 |
| `generate_review_queue.py` | 生成 review queue | 被 run-analyst.sh 调用 |
| `review-tracker.py merge` | 合并 tracker 状态 | 被 run-analyst.sh 调用 |
| `review-tracker.py export` | 导出 ledger CSV | 被 run-analyst.sh 调用 |
| `fetch_analyst_articles.py` | 抓取分析师文章 | 被 run-analyst-fetch.sh 调用 |

### 3.3 历史包袱（勿动）

- `run-pipeline.py`：系统性路径过时，引用 Phase 2 旧入口，不再作为 analyst 试点入口
- `scripts/` 目录：Phase 1 旧脚本，不影响当前试点

---

## 四、本轮迭代产出

### 4.1 新建文件（本轮新增）

| 文件 | 版本 | 用途 |
|------|------|------|
| `05_工具脚本/run-analyst.sh` | — | analyst 试点运行统一入口 |
| `05_工具脚本/run-analyst-fetch.sh` | — | analyst 数据人工刷新统一入口 |
| `05_工具脚本/fetch_analyst_articles.py`（修改） | — | 增强 dry-run 输出可解释性 |
| `docs/PILOT_RUN_SOP.md` | v1.4 | fetch → preflight → run 三步节奏 |
| `docs/REVIEW_LOG.md` | v1.16 | 全量 review 记录（R-22~R-31）|
| `docs/CHANGE_CONTROL.md` | v1.11 | 变更登记（CC-15~CC-20）|
| `docs/P1_CANDIDATES.md` | v1.9 | P1 优先级任务全表（含 P1-6/P1-6a）|
| `docs/CROSS_ROUND_CHECKLIST.md` | v1.0 | 跨轮触发清单 |
| `reports/ROUND_RECAP/ROUND_COMPARISON.md` | v1.1 | 三轮数字对比（ROUND-01~03）|
| `reports/ROUND_RECAP/ROUND_RECAP_2026-04-08.md` | — | ROUND-01 recap |
| `reports/ROUND_RECAP/ROUND_RECAP_2026-04-08_v2.md` | — | ROUND-02/03 recap |
| `reports/pilot-tracking-ledger.csv` | — | 轻量台账（5行）|

### 4.2 关键 SHA256（用于回退验证）

```
run-analyst.sh           : e5cb08134ce16720dd9fec9fa6fe367afec6fcb0959d538fd40aefb69c40a66e
run-analyst-fetch.sh     : 55edc0103a7224704ae6f874e31c976f22b970fcd0ba17d1bc14fed659d9761a
fetch_analyst_articles.py: de7ad7108913fc48f3e19629a37c8922ed90e9657f7bd28c5d71e523c3dcd1d1
```

### 4.3 本轮完成的任务

| 任务 | 结论 |
|------|------|
| P1-4（多轮复盘机制）| ✅ 完成 |
| P1-3a（run-analyst.sh wrapper）| ✅ 完成 |
| P1-3b（preflight 机制）| ✅ 完成 |
| P1-6（fetch 入口统一）| ✅ 完成 |
| P1-6a（dry-run 可解释性增强）| ✅ 完成 |
| ROUND-01/02/03 | ✅ 执行完成（三轮数据相同，机制验证通过）|
| ROUND-04 | ✅ preflight 正确阻止无意义运行 |

---

## 五、数据状态

### 5.1 当前 analyst 数据

| 指标 | 值 |
|------|-----|
| raw 总数 | 79 条 |
| usable 总数 | 29 条 |
| queue 条数 | 5 条 |
| fetchedAt | 2026-04-07T14:51:11（无更新）|
| 数据刷新触发 | 依赖人工执行 fetch，无自动调度 |

### 5.2 已知数据限制

- analyst fetch 层：依赖人工触发，无自动抓取
- 当前 fetchedAt 自 2026-04-07 后无变化（无新数据进入 pipeline）
- preflight 机制已验证：若无新数据，正确阻止无意义运行

---

## 六、已知阻断与开放问题

### 6.1 阻断项

| 编号 | 描述 | 状态 |
|------|------|------|
| ED-01（A Gate）| 缺 2026-03 贷款利率数据，loan_rate.json observedAt = 2025-12-01 | 持续等待外部数据 |
| ED-02（wechatsogou）| 微信文章抓取依赖外部工具 | 持续等待 |

### 6.2 开放问题（不阻断试点）

| 编号 | 描述 | 备注 |
|------|------|------|
| OI-03 | 来源先验权重过重（薛洪言 4/5 占比 80%）| 持续 3 轮，未触发修复 |
| OI-04 | confirmLevel 非人工验证 | 持续开放 |
| — | reports/ 是 symlink 指向旧路径 | 架构问题，不影响当前运行 |

---

## 七、回退操作

### 7.1 如需回退 run-analyst.sh

```bash
# 从备份恢复（备份位于 07_历史备份/第一轮开发迭代-iter1-2026-04-08/05_工具脚本/）
cp /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/07_历史备份/第一轮开发迭代-iter1-2026-04-08/05_工具脚本/run-analyst.sh \
   /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本/
```

### 7.2 如需回退 run-analyst-fetch.sh

```bash
cp /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/07_历史备份/第一轮开发迭代-iter1-2026-04-08/05_工具脚本/run-analyst-fetch.sh \
   /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本/
```

### 7.3 如需回退 fetch_analyst_articles.py

```bash
cp /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/07_历史备份/第一轮开发迭代-iter1-2026-04-08/05_工具脚本/fetch_analyst_articles.py \
   /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本/
```

### 7.4 如需回退文档

```bash
# 文档备份位于 07_历史备份/第一轮开发迭代-iter1-2026-04-08/docs/
cp -r /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/07_历史备份/第一轮开发迭代-iter1-2026-04-08/docs/* \
      /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/docs/
```

---

## 八、接续操作建议

### 8.1 继续试点运行

```bash
# 确认数据是否有更新
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本
./run-analyst-fetch.sh --check   # 先检查

# 如有更新，执行 preflight 判断，再决定是否运行
# 参考 PILOT_RUN_SOP.md Section 四/五
```

### 8.2 下次触发时机

- **数量触发**：raw 新增 ≥5 条
- **时间触发**：距 ROUND-03 满 14 天（2026-04-22 前后）
- **例外触发**：明确异常 / OI 需提前复查 / 用户指令

### 8.3 下一轮最值得关注的点

1. analyst fetch 层何时有新数据（当前无自动抓取，依赖人工）
2. 若连续多轮无新数据，需评估 fetch 层为何未更新
3. OI-03（来源权重）和 OI-04（confirmLevel）如需修复，另立任务

---

## 九、禁止事项

- 不得在旧路径（`workspace/ai-radar-station/`）进行开发
- 不得将 run-pipeline.py 作为 analyst 试点入口
- 不得在未完成 preflight 判断前直接执行 run-analyst.sh
- 不得将 reports/ 目录作为唯一可靠存储（其为 symlink 指向旧路径）

---

## 十、文档版本

| 文件 | 当前版本 |
|------|---------|
| HANDOFF.md | v2（第一轮开发迭代）|
| PILOT_RUN_SOP.md | v1.4 |
| REVIEW_LOG.md | v1.16 |
| CHANGE_CONTROL.md | v1.11 |
| P1_CANDIDATES.md | v1.9 |

---

*本 handover 文档覆盖 2026-04-07 迁移至 2026-04-08 第一轮开发迭代完成的完整状态。
如需更早阶段的交接信息，参考 07_历史备份/ 目录。*
