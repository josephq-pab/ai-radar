#!/bin/bash
# AI雷达站 Pipeline 入口
# Workspace: /home/admin/.openclaw/workspace-ai-radar
export OPENCLAW_DEPLOY_BASE=/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY
export PATH=/tmp/py39env/bin:$PATH
cd /home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY/05_工具脚本
exec /tmp/py39env/bin/python -B run-pipeline.py "$@"
