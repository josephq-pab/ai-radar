# 试运行手册 (Trial Runbook)

## 概述

本文档定义对公 AI 雷达站从"可试运行"升级为"可稳定试运行"的执行方案。

## 目标

- 系统可按明确节奏自动运行
- 异常能被及时发现和分级
- 数据新旧可解释
- 试运行问题可持续沉淀

---

## 一、运行节奏

### 1.1 日常刷新 (Daily)

| 项目 | 说明 |
|------|------|
| **触发时间** | 工作日 08:00 (可调整) |
| **运行模式** | `rebuild-only` |
| **执行内容** | 周报重建 + tracking 更新 + web bundle 刷新 |
| **预期耗时** | ~10 秒 |
| **依赖** | 核心数据文件已存在 |

### 1.2 周报刷新 (Weekly)

| 项目 | 说明 |
|------|------|
| **触发时间** | 每周五 08:00 (或按需) |
| **运行模式** | `full` |
| **执行内容** | 完整刷新：数据解析 + analyst 抓取 + 周报生成 + tracking + web bundle + smoke test |
| **预期耗时** | ~60 秒 |
| **依赖** | analyst 源可用 |

### 1.3 手动触发

> ⚠️ CLI 标志说明：`run-pipeline.py` 使用独立标志（如 `--full`、`--rebuild-only`），
> 不是 `--mode full`。使用错误标志会导致静默降级为默认（full）行为。

```bash
# 完整刷新（含 analyst 抓取，可能耗时较长）
cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station
python3 scripts/run-pipeline.py --full

# 仅重建（review 决策后，或配置变更后使用）
python3 scripts/run-pipeline.py --rebuild-only

# 仅 smoke test（验证数据链路）
python3 scripts/run-pipeline.py --smoke-only

# 演练模式（预览 rebuild-only 会做什么，不写入文件）
python3 scripts/run-pipeline.py --rebuild-only --dry-run
```

### 1.4 决策后同步（review / tracking 状态变更后）

> 当 review 或 tracking 状态变更后，使用 sync_after_review.py 统一同步链路。
> 该脚本会自动调用 rebuild_go_live_gate.py 更新 gate 状态。

```bash
cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station

# 演练模式（预览要做什么）
python3 scripts/sync_after_review.py --dry-run

# 正式执行
python3 scripts/sync_after_review.py --confirm
```

---

## 二、调度方式示例

### 2.1 Cron (macOS / Linux)

> CLI 标志：`run-pipeline.py` 使用独立标志，不是 `--mode full`。

```bash
# 日常刷新: 工作日 08:00（仅 rebuild，不跑数据解析）
0 8 * * 1-5 cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station && python3 scripts/run-pipeline.py --rebuild-only >> logs/cron-daily.log 2>&1

# 周报刷新: 每周五 08:00（完整刷新）
0 8 * * 5 cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station && python3 scripts/run-pipeline.py --full >> logs/cron-weekly.log 2>&1
```

### 2.2 Launchd (macOS)

创建 `~/Library/LaunchAgents/com.airadar.daily.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.airadar.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/josephq/.openclaw/workspace/projects/ai-radar-station/scripts/schedule-example.sh</string>
        <string>daily</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>1</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>2</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>3</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>4</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>5</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/josephq/.openclaw/workspace/projects/ai-radar-station/logs/launchd-daily.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/josephq/.openclaw/workspace/projects/ai-radar-station/logs/launchd-daily.error</string>
</dict>
</plist>
```

加载:
```bash
launchctl load ~/Library/LaunchAgents/com.airadar.daily.plist
```

---

## 三、异常处理

### 3.1 异常等级定义

| 等级 | 说明 | 处理方式 |
|------|------|----------|
| **P0** | 阻断试运行，必须立即处理 | 停止使用，优先修复 |
| **P1** | 不阻断，但影响可信度或业务理解 | 尽快处理，使用时注意风险 |
| **P2** | 非阻断观察项，可后续优化 | 记录跟踪，择机处理 |

### 3.2 WARN / FAIL 处理

#### WARN (警告)

- **含义**: 检测到异常，但不影响核心功能
- **处理**: 检查警告内容，确认影响后继续使用
- **示例**: analyst fetch 部分源失败、dedup 存在风险

#### FAIL (失败)

- **含义**: 核心功能异常，无法正常使用
- **处理**: 立即停止使用，检查日志并修复
- **示例**: 核心数据文件缺失、解析失败、smoke test FAIL

### 3.3 需人工介入的场景

1. `verdict` 不为 `usable`
2. `smokeTestResult.FAIL > 0`
3. `reviewQueueFallbackCount` 异常高 (>30%)
4. tracking 状态异常集中于某一状态
5. 数据新鲜度显示 `stale: true`

---

## 四、运行日志

| 日志类型 | 位置 | 说明 |
|----------|------|------|
| 运行摘要 | `reports/run-summary.json` | 机器可读 |
| 运行摘要 | `reports/run-summary.md` | 人读 |
| 变化摘要 | `reports/change-summary.json` | 数据变化 |
| 全量日志 | `logs/*.log` | 调试用 |

---

## 五、健康度判断

查看 `reports/run-summary.json` 中的字段:

- `verdict`: `usable` / `unusable`
- `verdictText`: 简要说明
- `success`: `true` / `false`
- `exitCode`: 0 为成功

示例:
```bash
# 判断本次运行是否可用
python3 -c "
import json
s = json.load(open('reports/run-summary.json'))
print(f' verdict: {s.get(\"verdict\")}')
print(f' verdictText: {s.get(\"verdictText\")}')
print(f' success: {s.get(\"success\")}')
"
```
