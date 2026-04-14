# HANDOFF.md - AI雷达站交接文档

## 来源

从总控台（main）迁移，原始项目路径：
`/home/admin/.openclaw/workspace/ai-radar-station/OPENCLAW_DEPLOY/`

## 迁移时间

2026-04-07

## 迁移方式

原样复制（cp -r），未修改任何项目文件。

---

## ⚠️ 路径声明

**旧路径已废弃（历史备份，不再开发）**：
```
/home/admin/.openclaw/workspace/ai-radar-station/OPENCLAW_DEPLOY/
```

**唯一开发路径**：
```
/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/
```

所有操作（代码修改、测试、运行、报告）**一律在新路径进行**。

---

## 项目当前状态

| 项目 | 状态 |
|------|------|
| smoke_test | 38/38 PASS |
| A gate | ❌ 阻断（缺贷款利率数据） |
| B gate | ✅ CLEARED |
| C gate | ✅ CLEARED |
| analyst 抓取 | ✅ scrapling 正常（6/7 成功） |
| 周报生成 | ✅ 正常 |

## 已知硬编码路径（待修复）

所有脚本中 `BASE = Path('/Users/josephq/...')` 已通过以下方式临时修复：
- 在 `/home/admin/.openclaw/workspace-ai-radar/scripts/run-pipeline.sh` 中设置 `OPENCLAW_DEPLOY_BASE` 环境变量
- `paths.py` 支持 `OPENCLAW_DEPLOY_BASE` 环境变量覆盖

**建议**：长期方案是将 BASE 改为相对路径或环境变量注入，不再依赖硬编码 Mac 路径。

## 待完成项

1. 补充 2026-03 贷款利率数据 → 解除 A gate 阻断
2. 将 `OPENCLAW_DEPLOY_BASE` 环境变量方案固化为标准部署方式
3. Phase F 工程化迁移
