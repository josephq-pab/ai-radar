# MIGRATION_NOTE.md

## 迁移记录

**从**: `/home/admin/.openclaw/workspace/ai-radar-station/OPENCLAW_DEPLOY/`
**到**: `/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/`
**时间**: 2026-04-07
**方式**: `cp -r` 原样复制

---

## 原样复制？

✅ 是 — 所有文件均原样复制，未做任何修改。

## 是否发现硬编码路径？

⚠️ 是 — 发现多处 `BASE = Path('/Users/josephq/.openclaw/workspace/projects/ai-radar-station')`

**临时解决方案**：在 `/tmp/run-pipeline.sh` 中通过 `OPENCLAW_DEPLOY_BASE` 环境变量注入，脚本 `paths.py` 已支持环境变量覆盖。

**长期建议**：将所有脚本中的 BASE 改为相对路径推导或统一环境变量注入，不再依赖硬编码路径。

## 迁移后验证

```bash
# 验证复制完整性
ls /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本/smoke_test.py
ls /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/04_数据与规则/processed/loan_rate.json

# 验证 pipeline 可运行
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本
OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY \
  /tmp/py39env/bin/python smoke_test.py --fast
```

## 后续建议

1. 在新 workspace 中首次运行 pipeline 前，更新 `/tmp/run-pipeline.sh` 的 `OPENCLAW_DEPLOY_BASE` 指向新路径
2. 统一把 `scripts/` 符号链接指向 `05_工具脚本/`
3. 消除硬编码路径是 Phase F 的工程化目标之一
