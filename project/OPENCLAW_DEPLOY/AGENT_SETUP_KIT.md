# 对公 AI 雷达站 — OpenClaw Agent 接管完整配置包

> 用途：新 OpenClaw 环境 agent 从零接管对公 AI 雷达站项目
> 生成时间：2026-04-06
> 包含：工作区配置 + 记忆注入 + 技能安装 + 验证步骤 + 接管指令

---

## 第一步：基础文件配置

### 1.1 解压部署包到工作区

在 OpenClaw 沙箱或目标机器上执行：

```bash
# 将 zip 包传到目标机器后解压到 projects 目录
cd ~/.openclaw/workspace
unzip 对公AI雷达站_OPENCLAW部署包_20260406.zip

# 确认目录结构存在
ls projects/ai-radar-station/OPENCLAW_DEPLOY/
```

### 1.2 确认项目路径

部署包解压后的项目路径：
```
~/.openclaw/workspace/projects/ai-radar-station/
```

**注意**：所有脚本使用 `scripts/paths.py` 统一路径，脚本之间禁止硬编码路径。
项目根目录由 `paths.py` 的 `__file__` 自举机制自动推导，无需设置环境变量。

---

## 第二步：安装 Python 依赖

```bash
cd ~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY
pip3 install -r requirements.txt

# 验证安装
python3 -c "import bs4, scrapling, openpyxl; print('依赖 OK')"
```

---

## 第三步：更新 Agent 记忆（Memory Injection）

### 3.1 在新 agent 的 MEMORY.md 中追加以下内容

```markdown
## 对公 AI 雷达站项目（活跃）

- 项目路径：projects/ai-radar-station/
- 部署包：OPENCLAW_DEPLOY/（解压后直接可用）
- 核心脚本入口：scripts/run-pipeline.py
- 统一路径配置：scripts/paths.py（所有脚本路径来源）
- 前端页面：apps/web/*.html（直接浏览器打开）
- 依赖：beautifulsoup4 / scrapling 0.2.99 / openpyxl
- 原始数据：data/raw/（人工上传 Excel）
- 中间层：data/processed/*.json（脚本产出）
- A/B/C Gate 状态查询：python3 scripts/rebuild_go_live_gate.py --check
- 健康检查：python3 scripts/smoke_test.py --fast（59 项）
- 当前阻断项：A gate（缺 2026-03 贷款利率数据）
- Phase 2 基线已收敛（2026-04-03 完成）
- Phase F（工程化迁移）待开始
- 参考设计规范：OPENCLAW_DEPLOY/08_设计规范补充/
```

### 3.2 更新/创建 memory 文件

```bash
# 创建今日记忆文件
cat > ~/.openclaw/workspace/memory/2026-04-06.md << 'EOF'
# 2026-04-06 日志

## 对公 AI 雷达站部署包

- 生成了完整部署包：OPENCLAW_DEPLOY/
- 包含：项目说明 + 规范文档 + 前端页面 + 数据与规则 + 工具脚本 + 进展状态 + 历史备份 + 设计规范
- 同步给了邱非用于迁移到新环境
- 当前唯一阻断项：A gate 数据缺口（缺 2026-03 贷款利率数据）
- 新环境 agent 接管后应优先处理 smoke_test.py --fast 验证
EOF
```

---

## 第四步：OpenClaw 技能配置（Skills）

### 4.1 推荐安装的技能

**必要技能（项目自带脚本需要）：**
```bash
# 无需额外技能，所有工具均为 Python 标准库 + requirements.txt
```

**建议技能（提升分析能力）：**
```bash
# 数据可视化（用于生成图表报告）
npx skills add data-visualization

# 项目文档（用于生成/更新 README）
npx skills add project-documentation

# PingAn PC 设计规范（前端 UI 开发参照）
# 技能已位于：~/.agents/skills/pingan-pc-design-system/
```

### 4.2 技能配置（SKILL.md 引用路径）

如果新环境需要重新注册技能，在 OpenClaw 配置中添加：

```yaml
# skills 配置
skills:
  - name: pingan-pc-design-system
    path: ~/.agents/skills/pingan-pc-design-system
    description: 平安智慧对公 PC 前端设计规范
```

---

## 第五步：验证环境完整性

### 5.1 快速验证命令（依次执行）

```bash
cd ~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/05_工具脚本

# 1. 验证 Python 语法
python3 -m py_compile paths.py
python3 -m py_compile smoke_test.py

# 2. 验证路径配置
python3 -c "
from paths import BASE, SCRIPTS, DATA, PROCESSED, REPORTS
print('BASE:', BASE)
print('SCRIPTS:', SCRIPTS)
print('All paths resolve correctly')
"

# 3. 运行健康检查
python3 smoke_test.py --fast

# 预期结果：59/59 PASS
```

### 5.2 验证前端页面

```bash
# 确认前端文件完整
ls -la ../03_前端页面/

# 检查 app-data.js 是否存在
ls -la ../03_前端页面/app-data.js
```

### 5.3 验证 gate 状态

```bash
python3 rebuild_go_live_gate.py --check

# 预期输出：
# A gate: BLOCKED（数据新鲜度，非本次引入）
# B gate: CLEARED
# C gate: CLEARED
```

---

## 第六步：接管指令（Agent Briefing）

### 6.1 给新 agent 的接管 prompt

将以下内容发给新环境的 agent（或写入 agent 的 session）：

---

**Agent 接管指令：**

请读取以下文件了解项目背景和运行方式：

1. `~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/OPENCLAW_DEPLOYMENT.md` — 完整部署说明
2. `~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/AGENT_BRIEFING.md` — 快速接管指南
3. `~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/06_进展状态/CURRENT_STATUS.md` — 当前状态

**接管第一步：**

```bash
cd ~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/05_工具脚本
python3 smoke_test.py --fast
```

确认 59/59 PASS 后报告结果。

**当前未决事项（按优先级）：**

| 优先级 | 事项 | 解决方案 |
|--------|------|---------|
| P0 | A gate 数据缺口 | 确认 2026-03 贷款利率 Excel 是否可用 |
| P1 | O-3 run-summary 一致性警告 | `python3 sync_after_review.py --confirm` |

---

### 6.2 Agent 常用工具箱

```bash
# 完整重建
python3 scripts/run-pipeline.py --full

# 分步执行（调试用）
python3 scripts/parse_initial_data.py
python3 scripts/build_interpretation_rules.py
python3 scripts/build_recommendation_rules.py
python3 scripts/generate_review_queue.py
python3 scripts/sync_after_review.py --confirm
python3 scripts/build_web_bundle.py

# 查看 gate 状态
python3 scripts/rebuild_go_live_gate.py --check

# 记录 review（事项确认后）
python3 scripts/record_review.py <itemId> <approve|modify|reject> [text]

# 记录 tracking 状态更新
python3 scripts/record_tracking_status.py <itemId> <status>

# 分析师观点抓取（需网络）
python3 scripts/fetch_analyst_articles.py
python3 scripts/batch_verify_analyst.py

# 打开前端页面（macOS）
open ../03_前端页面/index.html
```

---

## 第七步：每日运行节奏（cron 配置示例）

```bash
# 每日 08:00 运行健康检查 + 打包前端
0 8 * * * cd ~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/05_工具脚本 && python3 smoke_test.py --fast >> ~/logs/radar-health.log 2>&1

# 每周日 08:00 完整重建 + 周报
0 8 * * 0 cd ~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/05_工具脚本 && python3 run-pipeline.py --full >> ~/logs/radar-weekly.log 2>&1

# 每月初 08:00 月度数据导入（需人工确认原始 Excel 就位）
0 8 1 * * cd ~/.openclaw/workspace/projects/ai-radar-station/OPENCLAW_DEPLOY/05_工具脚本 && python3 import_monthly_data.py --confirm
```

---

## 第八步：关键文件索引

| 用途 | 文件路径 |
|------|---------|
| 部署说明（必读） | `OPENCLAW_DEPLOY/OPENCLAW_DEPLOYMENT.md` |
| Agent 快速指南 | `OPENCLAW_DEPLOY/AGENT_BRIEFING.md` |
| 当前状态快照 | `OPENCLAW_DEPLOY/06_进展状态/CURRENT_STATUS.md` |
| 项目交接文档 | `OPENCLAW_DEPLOY/01_项目说明/HANDOVER.md` |
| Phase 2 结项报告 | `OPENCLAW_DEPLOY/02_规范文档/CLOSURE_REPORT.md` |
| 未决事项清单 | `OPENCLAW_DEPLOY/02_规范文档/OPEN_ISSUES.md` |
| 路径配置（只读） | `05_工具脚本/paths.py` |
| 统一入口脚本 | `05_工具脚本/run-pipeline.py` |
| 健康检查 | `05_工具脚本/smoke_test.py` |
| Gate 状态 | `06_进展状态/go-live-gate.json` |
| 前端首页 | `03_前端页面/index.html` |
| 设计规范 | `OPENCLAW_DEPLOY/08_设计规范补充/` |

---

## 常见问题

**Q：smoke_test.py 报 FAIL 怎么办？**
A：查看 `OPENCLAW_DEPLOY/06_进展状态/CURRENT_STATUS.md` 的未决事项，逐项处理。常见 FAIL 多为数据文件路径问题，确认 `data/raw/` 下 Excel 文件存在。

**Q：A gate 一直 BLOCKED？**
A：正常——缺少 2026-03 原始数据。需获取数据后执行 `import_monthly_data.py --confirm` 清除。

**Q：前端页面空白？**
A：先运行 `python3 build_web_bundle.py`，再用浏览器打开 HTML 文件。

**Q：scripts/paths.py 报错找不到模块？**
A：确保当前目录在 `05_工具脚本/` 下，且已安装 `requirements.txt`。

---

*如需进一步协助，读取 `OPENCLAW_DEPLOYMENT.md` 的详细说明，或运行 `smoke_test.py --fast` 报出具体 FAIL 项后询问。*
