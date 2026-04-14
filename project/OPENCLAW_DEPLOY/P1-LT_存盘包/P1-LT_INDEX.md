# P1-LT 存盘包 — 主索引与快速上手指南

> 版本：v1.0
> 打包时间：2026-04-08
> 包含范围：Phase 3 + P1-1 ~ P1-LT 全部产物

---

## 一、本包用途

本包是 AI雷达站项目（P1-LT 阶段）的完整存盘包。
任何一个 Agent 接到本包后，应能在 **10 分钟内**理解当前完整状态，并在 **30 分钟内**复现当前运行能力。

---

## 二、目录结构

```
P1-LT_存盘包/
├── P1-LT_INDEX.md          ← 本文件（主索引 + 快速上手）
├── AGENTS.md               ← Agent 角色定义
├── HANDOFF.md              ← 交接文档（项目全貌）
├── README.md               ← 项目说明
├── RUNBOOK.md              ← 运行手册
├── docs/                   ← 全部设计/决策/记录文档
│   ├── REVIEW_LOG.md       ← 所有复盘记录（R-01 ~ R-44）
│   ├── CHANGE_CONTROL.md   ← 全部变更控制记录
│   ├── P1_CANDIDATES.md   ← P1 任务总览与状态
│   ├── PILOT_RUN_SOP.md   ← 试点运行 SOP（v1.6）
│   ├── DIMENSION_EXPANSION_PROPOSAL.md  ← 维度扩展草案
│   ├── SOURCE_CHANGE_PROPOSAL.md         ← 来源变更草案
│   ├── OPEN_ISSUES.md     ← 开放问题清单
│   ├── ROUND_RECAP_TEMPLATE.md          ← 轮次复盘模板
│   ├── CROSS_ROUND_CHECKLIST.md          ← 跨轮触发清单
│   └── ... (共 28 个文档)
├── 05_工具脚本/            ← 全部可执行脚本
│   ├── run-analyst.sh      ← 统一运行入口
│   ├── run-analyst-fetch.sh ← 统一 fetch 入口（含 --dim-trial）
│   ├── fetch_analyst_articles.py  ← 分析师文章抓取脚本
│   └── run-pipeline.py     ← 历史入口（已不推荐使用）
├── 04_数据与规则/
│   ├── analyst_sources.json ← 来源配置（活跃状态、维度、优先级）
│   ├── analyst_opinions.json        ← 可引用观点库
│   └── analyst_opinions_raw.json   ← 原始抓取结果
├── reports/
│   ├── analyst-review-queue.json    ← 当前待 review 队列
│   ├── analyst-tracking-ledger.csv  ← 历史追踪台账
│   └── ROUND_RECAP/                 ← 各轮次复盘文档
├── eval/
│   └── ... (评估规则)
└── (其他支撑文档)
```

---

## 三、当前项目状态（2026-04-08）

### 阶段完成度

| 项目 | 状态 |
|------|------|
| Phase 3 | ✅ 完成并收口 |
| P1-1 ~ P1-13 | ✅ 全部完成 |
| P1-LT（长期复用包）| ✅ 当前所处阶段 |
| ROUND-01 ~ ROUND-04 | ✅ 全部完成 |

### 数据状态

| 指标 | 值 | 说明 |
|------|---|------|
| raw 总数 | 49 | 合并后（dim-trial 双维度抓取）|
| usable | 28 | 可引用观点 |
| queue | 5 | 待 review（温彬/薛洪言/周茂华 pending）|
| confirmed | 4 | 已确认可用 |
| 薛洪言占比 | 42.9% | 首次改善（vs 51.7%）|
| fetchedAt | 2026-04-08T09:57:30Z | 上次真实抓取时间 |

### dim-trial 状态

- **定义**：观察中的准基线（不是临时试探，也不升格为正式默认）
- **有效性**：已验证1次（温彬/曾刚进入池，占比改善）
- **可重复性**：未验证（仅1次）
- **观察窗口**：P0/P1/P2 三级触发，14天自动

---

## 四、核心运行入口

### 统一运行入口
```bash
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY
./05_工具脚本/run-analyst.sh
```

### 统一 fetch 入口
```bash
# 标准 fetch（对公存款维度）
./05_工具脚本/run-analyst-fetch.sh

# 维度扩展试探（对公存款 + 对公贷款）
./05_工具脚本/run-analyst-fetch.sh --dim-trial

# dry-run 检查
./05_工具脚本/run-analyst-fetch.sh --dry-run
./05_工具脚本/run-analyst-fetch.sh --dim-trial --dry-run
```

### preflight 检查（手动）
```bash
# 检查当前是否满足运行条件
python3 -c "
import json, time
with open('04_数据与规则/processed/analyst_opinions_raw.json') as f:
    d = json.load(f)
print('fetchedAt:', d.get('fetchedAt'))
print('raw条数:', len(d.get('records',[])))
"
```

---

## 五、dim-trial 观察窗口（核心机制）

### 三级触发条件

| 优先级 | 触发条件 | 下次激活动作 |
|--------|---------|------------|
| P0 | fetchedAt 变化 | 立即激活完整判断 |
| P1 | raw 新增 ≥5 | 立即激活完整判断 |
| P2 | 满14天（~2026-04-22）| 自动激活完整判断 |

### 使用方式

本项目不自动轮询。每次检查时：
1. 先检查 P0/P1/P2 是否触发
2. 若触发 → 执行分支 B（fetch → preflight → 轮次 → 复验）
3. 若未触发 → 留痕并停止

---

## 六、关键文档索引

| 你需要什么 | 看哪个文档 |
|-----------|-----------|
| 快速理解项目全貌 | `README.md` |
| 交接/转交时的状态说明 | `HANDOFF.md` |
| 如何运行当前系统 | `RUNBOOK.md` |
| 所有决策记录（按时间顺序）| `docs/REVIEW_LOG.md` |
| 所有变更控制记录 | `docs/CHANGE_CONTROL.md` |
| P1 任务全部状态 | `docs/P1_CANDIDATES.md` |
| 当前试点运行 SOP | `docs/PILOT_RUN_SOP.md` |
| 维度扩展决策与状态 | `docs/DIMENSION_EXPANSION_PROPOSAL.md` |
| 来源配置当前状态 | `04_数据与规则/analyst_sources.json` |
| 原始抓取数据 | `04_数据与规则/processed/analyst_opinions_raw.json` |
| 当前待 review 队列 | `reports/analyst-review-queue.json` |
| 轮次复盘模板 | `docs/ROUND_RECAP_TEMPLATE.md` |
| 跨轮触发清单 | `docs/CROSS_ROUND_CHECKLIST.md` |
| 开放问题清单 | `docs/OPEN_ISSUES.md` |

---

## 七、持续开放问题

| 编号 | 问题 | 状态 | 备注 |
|------|------|------|------|
| OI-03 | 来源先验权重过重（薛洪言占比）| ⚠️ 改善中 | 42.9%，需持续验证 |
| OI-04 | confirmLevel 非人工验证 | ⏳ 开放中 | 不阻断试点 |
| Gate A | 贷款利率数据缺失 | ⏳ 外部依赖 | 持续等待 |
| ED-02 | wechatsogou 可用性 | ⏳ 外部依赖 | 持续等待 |

---

## 八、下次触发条件

| 触发 | 条件 | 预计时间 |
|------|------|---------|
| P0 | fetchedAt 变化 | 不确定 |
| P1 | raw 新增 ≥5 | 不确定 |
| P2 | 满14天 | ~2026-04-22 |

---

## 九、快速复现清单

任何一个 Agent 接到本包后，按以下顺序验证：

1. **检查数据完整性**
   ```bash
   cat 04_数据与规则/processed/analyst_opinions_raw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('raw:', len(d['records'])); print('fetchedAt:', d['fetchedAt'])"
   cat 04_数据与规则/processed/analyst_opinions.json | python3 -c "import json,sys; d=json.load(sys.stdin); u=[r for r in d['records'] if r.get('isReferenceable')]; print('usable:', len(u))"
   ```

2. **验证 fetch 脚本可运行**
   ```bash
   cd /path/to/P1-LT_存盘包
   ./05_工具脚本/run-analyst-fetch.sh --dry-run
   ```

3. **验证 run 脚本可运行**
   ```bash
   ./05_工具脚本/run-analyst.sh --dry-run
   ```

4. **验证 preflight 机制**
   - 检查 fetchedAt 是否变化
   - 检查 raw 是否 ≥5 新增
   - 按 PILOT_RUN_SOP.md 的 A/B/C/D/D-续 判断

---

## 十、版本信息

| 文件 | 当前版本 |
|------|---------|
| REVIEW_LOG.md | v1.29 |
| CHANGE_CONTROL.md | v1.23 |
| P1_CANDIDATES.md | v1.16 |
| PILOT_RUN_SOP.md | v1.6 |
| DIMENSION_EXPANSION_PROPOSAL.md | v1.1 |
| SOURCE_CHANGE_PROPOSAL.md | v1.0 |
| OPEN_ISSUES.md | v1.2 |
| ROUND_COMPARISON.md | v1.1 |
| CROSS_ROUND_CHECKLIST.md | v1.0 |

---

## 十一、关键脚本 SHA256

| 脚本 | SHA256 |
|------|--------|
| run-analyst.sh | `e5cb08134ce16720dd9fec9fa6fe367afec6fcb0959d538fd40aefb69c40a66e` |
| run-analyst-fetch.sh | `b4e90...`（--dim-trial版）|
| fetch_analyst_articles.py | `de7ad7108913fc48f3e19629a37c8922ed90e9657f7bd28c5d71e523c3dcd1d1` |

---

## 十二、接手检查表

- [ ] README.md 已读
- [ ] HANDOFF.md 已读
- [ ] RUNBOOK.md 已读
- [ ] dim-trial 观察窗口机制已理解
- [ ] P0/P1/P2 触发条件已理解
- [ ] 当前数据状态已确认（raw/usable/fetchedAt）
- [ ] fetch 脚本 dry-run 验证通过
- [ ] run 脚本 dry-run 验证通过
- [ ] REVIEW_LOG 最新记录已读
- [ ] 持续开放问题已确认
- [ ] 下次触发条件已知

---

> 本文件是 P1-LT 存盘包的主索引。如有疑问，先查本文档；本文档无法回答的问题，查 HANDOFF.md 或 REVIEW_LOG.md。
