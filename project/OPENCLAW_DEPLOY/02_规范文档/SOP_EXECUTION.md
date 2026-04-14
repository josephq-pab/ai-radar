# 对公 AI 雷达站｜试运行执行手册

> 本手册用于将 SOP（试运行操作规范）落地为可执行的操作指南，配合 BUILD_PLAN.md 阶段 E 使用。

---

## 一、每周运行节奏

| 时间 | 动作 | 脚本/工具 |
|------|------|----------|
| 每周一 | 刷新对标数据（存款/贷款/利率） | `python3 scripts/parse_initial_data.py` |
| 每周一 | 更新解释规则和建议规则 | `python3 scripts/build_interpretation_rules.py && scripts/build_recommendation_rules.py` |
| 每周二 | 生成周报草稿 | `python3 scripts/generate_weekly_report.py` |
| 每周二 | 生成待确认事项队列 | `python3 scripts/generate_review_queue.py` |
| 每周三 | 查看案例页（存款/贷款）确认分析结论 | 浏览器打开 `apps/web/deposit.html` / `loan.html` |
| 每周四 | 确认/修改/驳回待确认事项 | `python3 scripts/record_review.py <itemId> <decision> [editedText] [reason]` |
| 每周四 | 构建 review 状态 + tracking 中间层 | `python3 scripts/build_review_status.py && scripts/build_tracking_items.py` |
| 每周四 | 如有 tracking 状态变更 | `python3 scripts/record_tracking_status.py <itemId> <status> [progress] [nextAction]` |
| 每周五 | 打包前端数据 | `python3 scripts/build_web_bundle.py` |
| 每周五 | 同步邮件发送 | `bash ../../scripts/run-daily-report.sh` |

---

## 二、数据刷新完整命令序列

> Phase 2: 所有脚本支持从项目根目录运行，无需硬编码绝对路径。
> 统一使用 `python3 scripts/<script>` 从 `projects/ai-radar-station/` 执行。

```bash
cd /Users/josephq/.openclaw/workspace/projects/ai-radar-station
python3 scripts/parse_initial_data.py
python3 scripts/build_interpretation_rules.py
python3 scripts/build_recommendation_rules.py
python3 scripts/generate_weekly_report.py
python3 scripts/generate_review_queue.py
python3 scripts/build_review_status.py
python3 scripts/build_tracking_items.py
python3 scripts/build_web_bundle.py
```

---

## 三、人工确认节点

1. **案例页确认**：确认存款/贷款页的关键观察、建议动作是否符合管理层汇报口径
2. **事项入池确认**：确认 review queue 中哪些事项需要进入 tracking 闭环
3. **状态变更确认**：当 tracking 状态从"跟踪中"推进到"已上报"或"已行动"时，需人工确认
4. **周报出稿确认**：每周五确认周报草稿内容无误后，发送给相关方

---

## 四、事项闭环操作

### 查看跟踪页
```bash
# 浏览器打开
open apps/web/tracking.html
```

### 记录确认意见
```bash
python3 scripts/record_review.py <itemId> <decision> [editedText] [reason]

# 示例
python3 scripts/record_review.py core-1 modify "建议把差距拆解更偏经营视角" "原表述不够像管理层汇报语言"
```

### 推进 tracking 状态
```bash
python3 scripts/record_tracking_status.py <itemId> <status> [progress] [nextAction]

# 示例：将 core-1 推进为"已行动"
python3 scripts/record_tracking_status.py core-1 已行动 "已完成管理口径沟通并转入专项跟进" "下周复盘专项推进结果"
```

### 查看当前事项状态
```bash
cat reports/tracking-items.json | python3 -m json.tool
```

---

## 五、页面查看路径

| 页面 | 文件路径 |
|------|----------|
| 首页总览 | `apps/web/index.html` |
| 存款深案例 | `apps/web/deposit.html` |
| 贷款深案例 | `apps/web/loan.html` |
| 重点事项跟踪 | `apps/web/tracking.html` |
| 周报与专题 | `apps/web/weekly-report.html` |
| 同业分析 | `apps/web/peer-monitor.html` |

---

## 六、当前阶段关注指标

- 链路跑通率：8 脚本是否全部成功
- 页面承接率：存款/贷款/tracking 页是否正确展示数据
- 事项闭环率：trackingItems 中的事项是否正确反映业务状态
- 页面/事项/周报一致性：三者口径是否统一
- 待补项暴露质量：待补数据/待补口径是否清晰标识

---

## 七、升级触发条件

以下情况出现时，应考虑升级到阶段 F（工程化迁移准备）：

- 试运行连续 2 周跑通且邱非确认可用
- 数据来源需要从本地文件升级为数据库或 API
- 需要多人协同使用
- 页面需要部署到正式环境