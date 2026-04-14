#!/usr/bin/env python3
"""
scripts/import_monthly_data.py

月度数据导入脚本。
在已有 parse_initial_data.py 基础上封装，提供清晰的导入入口和校验。

用法:
    # 演练（不实际导入）
    python3 scripts/import_monthly_data.py --dry-run

    # 演练并显示详细步骤
    python3 scripts/import_monthly_data.py --dry-run --verbose

    # 执行导入（先 dry-run 确认无误后再执行）
    python3 scripts/import_monthly_data.py --confirm

    # 指定输入目录（默认 data/raw/）
    python3 scripts/import_monthly_data.py --input-dir /path/to/new/files --confirm
"""

import json
import sys
from datetime import datetime
from pathlib import Path

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
RAW = BASE / 'data' / 'raw'
PROCESSED = BASE / 'data' / 'processed'

# 标准文件模式
REQUIRED_FILES = {
    'deposit': {
        'patterns': ['*存款*', '*同业对标*', '*余额*'],
        'output': 'deposit_benchmark.json',
        'description': '存款对标数据'
    },
    'loan': {
        'patterns': ['*贷款*', '*人行口径*'],
        'output': 'loan_benchmark.json',
        'description': '贷款对标数据'
    },
    'rate': {
        'patterns': ['*利率*'],
        'output': 'loan_rate.json',
        'description': '利率数据'
    }
}

def scan_input_dir(input_dir: Path) -> dict:
    """扫描输入目录，返回找到的文件"""
    found = {k: None for k in REQUIRED_FILES}
    if not input_dir.exists():
        return found
    for f in input_dir.iterdir():
        if f.is_dir() or not f.suffix.lower() in ('.xlsx', '.xls', '.csv'):
            continue
        fname_lower = f.name.lower()
        for key, spec in REQUIRED_FILES.items():
            if found[key]:
                continue
            for pat in spec['patterns']:
                if pat.replace('*', '') in fname_lower:
                    found[key] = f
                    break
    return found

def check_import_ready(found: dict) -> tuple[bool, list]:
    """检查是否满足导入条件"""
    issues = []
    for key, fpath in found.items():
        desc = REQUIRED_FILES[key]['description']
        if fpath is None:
            issues.append(f"缺少 {desc} 文件（预期模式: {REQUIRED_FILES[key]['patterns']}）")
        elif not fpath.exists():
            issues.append(f"{desc} 文件不存在: {fpath}")
        else:
            issues.append(f"✅ {desc}: {fpath.name}")
    return len([f for f in found.values() if f]) >= 2, issues

def run_parse() -> dict:
    """调用现有的 parse_initial_data.py"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(BASE / 'scripts' / 'parse_initial_data.py')],
        capture_output=True, text=True, cwd=str(BASE)
    )
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }

def validate_output() -> dict:
    """校验生成的文件"""
    checks = []
    for key, spec in REQUIRED_FILES.items():
        out_path = PROCESSED / spec['output']
        if not out_path.exists():
            checks.append(('FAIL', spec['output'], '文件不存在'))
            continue
        try:
            with open(out_path) as f:
                data = json.load(f)
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                count = len(data.get('records', data.get('data', [])))
            else:
                count = 'unknown'
            checks.append(('PASS', spec['output'], f'{count} 条记录'))
        except Exception as e:
            checks.append(('FAIL', spec['output'], str(e)))
    return checks

def run_rebuild() -> dict:
    """触发 rebuild-only 模式"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(BASE / 'scripts' / 'run-pipeline.py'), '--mode', 'rebuild-only'],
        capture_output=True, text=True, cwd=str(BASE)
    )
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description='月度数据导入工具')
    parser.add_argument('--input-dir', default=str(RAW), help='输入文件目录')
    parser.add_argument('--dry-run', action='store_true', help='仅检查，不导入')
    parser.add_argument('--confirm', action='store_true', help='确认执行导入（需先 dry-run）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    mode = '演练' if args.dry_run else '真实导入'
    print(f"\n{'='*50}")
    print(f"  月度数据导入工具 | {mode} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")

    print(f"[1/4] 扫描输入目录: {input_dir}")
    found = scan_input_dir(input_dir)
    ready, issues = check_import_ready(found)
    for issue in issues:
        print(f"  {issue}")

    if not ready:
        print(f"\n❌ 导入条件不满足（仅找到 {sum(1 for f in found.values() if f)}/{len(found)} 个文件）")
        print(f"\n💡 提示:")
        print(f"  - 将新文件放入: {input_dir}")
        print(f"  - 文件命名应包含: 存款/贷款/利率 等关键词")
        print(f"  - 当前目录文件: {[f.name for f in input_dir.iterdir() if f.is_file()] if input_dir.exists() else '目录不存在'}")
        print(f"\n  如无新文件但想演练流程，使用: python3 scripts/import_monthly_data.py --dry-run --input-dir data/raw/")
        return

    print(f"\n✅ 导入条件满足（{sum(1 for f in found.values() if f)}/{len(found)} 个文件）")

    if args.dry_run:
        print(f"\n[演练模式] 以下为演练步骤，实际不会修改任何文件:\n")
    else:
        if not args.confirm:
            print(f"\n⚠️  未加 --confirm，不执行实际导入。加 --confirm 确认。")
            return
        print(f"\n[真实导入模式]\n")

    print(f"[2/4] {'演练' if args.dry_run else '执行'} 数据解析...")
    parse_result = run_parse()
    if parse_result['returncode'] != 0:
        print(f"  ❌ 解析失败: {parse_result['stderr'][:200]}")
        return
    print(f"  ✅ 解析完成")

    print(f"\n[3/4] {'演练' if args.dry_run else '执行'} 输出校验...")
    checks = validate_output()
    for status, fname, detail in checks:
        icon = '✅' if status == 'PASS' else '❌'
        print(f"  {icon} [{status}] {fname}: {detail}")

    if any(s == 'FAIL' for s, _, _ in checks):
        print(f"\n❌ 导入失败，部分文件生成异常")
        return

    if args.dry_run:
        print(f"\n[演练结束] 真实导入命令: python3 scripts/import_monthly_data.py --confirm")
        return

    print(f"\n[4/4] 执行 rebuild-only (重建报告)...")
    rebuild_result = run_rebuild()
    if rebuild_result['returncode'] != 0:
        print(f"  ⚠️ rebuild 失败: {rebuild_result['stderr'][:200]}")
    else:
        print(f"  ✅ rebuild 完成")

    print(f"\n{'='*50}")
    print(f"  ✅ 月度导入完成 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    print(f"\n  导入文件:")
    for key, fpath in found.items():
        if fpath:
            print(f"    {REQUIRED_FILES[key]['description']}: {fpath.name}")
    print(f"\n  生成的 JSON:")
    for key, spec in REQUIRED_FILES.items():
        out_path = PROCESSED / spec['output']
        if out_path.exists():
            print(f"    {spec['output']} ({out_path.stat().st_size:,} bytes)")
    print(f"\n  下一步:")
    print(f"    1. 检查 deposit_benchmark.json / loan_benchmark.json / loan_rate.json 的 observedAt")
    print(f"    2. 运行: python3 scripts/check_fetch_health.py")
    print(f"    3. 生成周报: python3 scripts/run-pipeline.py --mode rebuild-only")

if __name__ == '__main__':
    main()
