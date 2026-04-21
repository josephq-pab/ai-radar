# CONFIG_CONTROL_PLAN_V1.md — 配置管控方案

> 档案编号：CFG-CTL-01
> 文档版本：v1.0（新建）
> 编制日期：2026-04-16
> 对应阶段：P3（系统化建设 — 配置管控先行）
> 状态：**配置管控方案 v1.0**

---

## 一、当前配置散点问题

### 问题清单

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| C1 | analyst_sources.json 是唯一来源配置 | data/analyst_sources.json | 散落，无统一入口 |
| C2 | preflight 阈值在脚本里硬编码 | build_analyst_opinions.py / smoke_test.py | 调整需要改代码 |
| C3 | Gate A/B/C 阈值在多个脚本分散 | rebuild_c_gate.py / rebuild_go_live_gate.py | 阈值不一致风险 |
| C4 | confirmLevel 在 build 脚本里写死 | build_analyst_opinions.py | 调整需要改代码 |
| C5 | 运行入口分散 | run-analyst.sh / run-analyst-fetch.sh / 多个独立脚本 | 运营者记忆成本高 |
| C6 | 无配置变更日志 | — | 配置变更不可追溯 |
| C7 | 无统一页面查看当前配置状态 | — | 无法快速判断"系统现在正常吗" |

---

## 二、统一配置入口最小方案

**不做**：大型配置后台、数据库、权限体系。

**要做**：单页配置状态展示 + 配置变更日志。

### 最小配置展示页

集成到 `index.html` 或新建 `config-status.html`：

| 展示项 | 数据来源 | 更新频率 |
|--------|---------|---------|
| 激活来源列表 | analyst_sources.json | 手动刷新 |
| 停用来源列表 | analyst_sources.json | 手动刷新 |
| Gate A/B/C 状态 | go-live-gate.json | 随运行更新 |
| preflight 结果 | 末次运行摘要 | 随运行更新 |
| 上次运行时间 | change-summary.json | 随运行更新 |
| 本月抓取文章数 | change-summary.json | 随运行更新 |

**实现方式**：纯静态 HTML + JavaScript 读取 JSON 文件，不做后端。

---

## 三、配置变更日志方案

### 最小实现

在 `data/config-change-log.md`（纯 Markdown）记录每次配置变更：

```
## 2026-04-16 配置变更记录

### 变更1
- 时间：2026-04-16 15:30
- 变更人：用户
- 变更内容：新增来源 李超（浙商证券宏观）
- 变更文件：data/analyst_sources.json
- 变更前：sources=9
- 变更后：sources=10
- 验证结果：✅ dry-run 通过
```

### 写入规则

- 每次修改 analyst_sources.json 前必须先记录
- 每次修改 preflight/Gate 阈值前必须先记录
- 记录后执行验证，确认通过才算正式生效
- **不得直接修改配置而不记录**

---

## 四、配置优先级排序

### 第一优先（影响 MVP 闭环）

| 配置 | 当前状态 | 目标 |
|------|---------|------|
| analyst_sources.json | ✅ 唯一配置源 | 保持，并增加变更日志 |
| 运行入口 | ⚠️ 分散 | run-analyst.sh 统一，文档同步 |
| 配置展示页 | ❌ 缺失 | 新建 config-status.html |

### 第二优先（提升运营可维护性）

| 配置 | 当前状态 | 目标 |
|------|---------|------|
| preflight 阈值 | 硬编码 | 文档化当前值到 SYSTEM_MVP_SCOPE.md，暂不改代码 |
| Gate 阈值 | 多处分散 | 文档化当前值到 SYSTEM_MVP_SCOPE.md，暂不改代码 |
| 配置变更日志 | ❌ 缺失 | data/config-change-log.md |

### 第三优先（本期不动）

| 配置 | 原因 |
|------|------|
| confirmLevel 动态调整 | 需要更多反馈数据后再决策 |
| 自动告警阈值 | MVP 阶段人工监控足够 |

---

## 五、配置生效边界

**本期配置管控的边界**：

1. **只能通过 analyst_sources.json 变更来源**，不得直接修改脚本
2. **阈值变更必须记录**，不得直接修改脚本中的硬编码值
3. **每次配置变更后必须执行 dry-run 验证**，确认通过才算生效
4. **配置变更不影响已生成的输出**，只影响后续运行

**本期不做的配置能力**：

- 不做动态阈值调整（需要更多数据后再设计）
- 不做多环境配置分离（dev/prod 分开是正式部署需求）
- 不做配置版本回滚（手动从日志恢复即可）

---

## 六、验收标准

| 验收项 | 标准 |
|--------|------|
| 配置展示页可打开 | index.html 或 config-status.html 能展示所有关键配置 |
| 配置变更有日志 | 每次改 analyst_sources.json 都有记录 |
| 来源启停不需改脚本 | 只需改配置文件 + 验证，不需要改 Python 代码 |
| 运行入口统一 | 一个命令完成全链路，不需要记忆多个脚本 |

---

*记录：AI雷达站 agent，2026-04-16 15:22 GMT+8（P3 配置管控方案）*
