# 对公 AI 雷达站下一步施工说明

## 一、当前正式基线

当前项目必须以以下文档作为正式基线：

- `docs/PROJECT_BASELINE.md`
- `docs/BASELINE_ALIGNMENT.md`
- `docs/BUILD_PLAN.md`
- `docs/PROGRESS_LOG.md`

如实现与前期资料或上述治理文档冲突，默认修正实现，不反向以现状定义需求。

## 二、当前可直接查看的页面

目录：`projects/ai-radar-station/apps/web/`

### 一级核心页面
- `index.html`：首页总览
- `deposit.html`：存款深案例页
- `loan.html`：贷款深案例页
- `tracking.html`：重点事项跟踪页

### 二级承接页
- `weekly-report.html`：周报与专题承接页
- `peer-monitor.html`：同业分析承接页

### 后续预留页
- `policy-industry.html`：政策与行业预留页

## 三、每次刷新数据的建议顺序

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

执行后，页面读取的 `apps/web/data/app-data.js` 会更新。

## 四、记录确认意见

```bash
python3 scripts/record_review.py <itemId> <decision> [editedText] [reason]
```

示例：

```bash
python3 scripts/record_review.py core-1 modify "建议把结论改成更偏经营视角" "原表述不够像管理层汇报语言"
```

记录会写入：
- `reviews/review-log.jsonl`

## 五、当前严格执行的下一步顺序

1. ~~已完成~~ tracking 中间层正式化
2. ~~已完成~~ 四页主链路一致性校验
3. ~~已完成~~ 规则链路进一步进入生成过程
4. ~~已完成~~ 试运行周节奏落地
5. ~~已完成~~ 工程化迁移准备
6. **新增** 外部分析师观点接入（进行中）
   - 白名单已建立（9 位分析师，存款/贷款/整体三维度）
   - 抓取脚本已运行（9 条全部成功）
   - 结构化中间层已构建（5 条高价值观点进入周报）
   - tracking 闭环已接入（5 条分析师事项进入 tracking）
   - 下一步：扩大白名单、补抓微信文章、处理编码问题

## 六、当前不建议优先推进的事项

- 新增更多一级页面
- 继续扩张周报页为独立主系统
- 继续强化同业页为一级强入口
- 提前深挖政策与行业页
- 在高保真视觉层投入过多精力

## 七、执行纪律

- 先对齐文档，再扩实现
- 先稳主链路，再扩二级页
- 先稳中间层，再谈工程化
- 每轮推进后，记得同步更新 `docs/PROGRESS_LOG.md`
