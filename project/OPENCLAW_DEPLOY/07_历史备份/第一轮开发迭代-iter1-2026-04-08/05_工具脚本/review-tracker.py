#!/usr/bin/env python3
"""
scripts/review-tracker.py

独立状态台账工具：管理 reviewStatus / trackingStatus 的持久化。

职责：
- upsert：按 itemId 写入或更新状态到 review-tracker.json
- merge：输出 merged view（queue + tracker，tracker 覆盖 queue 初始状态）
- 不修改 analyst-review-queue.json（那是 build 的纯输出）

用法：
    # upsert 一条状态
    python3 review-tracker.py --upsert --item-id analyst-72873eb4 \
        --review-status confirmed --tracking-status follow_up --note "确认引用"

    # 读取 merged view
    python3 review-tracker.py --merge

    # 查询单条状态
    python3 review-tracker.py --get --item-id analyst-72873eb4
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
TRACKER = BASE / 'reports' / 'review-tracker.json'
QUEUE = BASE / 'reports' / 'analyst-review-queue.json'


def _load_tracker() -> dict:
    """加载 tracker 台账，不存在则返回空结构"""
    if not TRACKER.exists():
        return {"schema": "review-tracker v1.0", "description": "", "records": {}}
    return json.loads(TRACKER.read_text(encoding='utf-8'))


def _save_tracker(data: dict) -> None:
    """保存 tracker 台账"""
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    TRACKER.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def upsert(item_id: str, review_status: str = None, tracking_status: str = None, note: str = None) -> dict:
    """按 itemId upsert 状态，返回更新后的记录"""
    tracker = _load_tracker()
    records = tracker.setdefault('records', {})

    if item_id not in records:
        records[item_id] = {
            "itemId": item_id,
            "reviewStatus": "pending",
            "trackingStatus": "pending",
            "updatedAt": None,
            "note": ""
        }

    rec = records[item_id]
    now = datetime.now(timezone.utc).isoformat()

    if review_status is not None:
        rec["reviewStatus"] = review_status
    if tracking_status is not None:
        rec["trackingStatus"] = tracking_status
    if note is not None:
        rec["note"] = note

    rec["updatedAt"] = now
    records[item_id] = rec
    tracker["records"] = records
    _save_tracker(tracker)

    return rec


def get(item_id: str) -> Optional[dict]:
    """查询单条状态，不存在返回 None"""
    tracker = _load_tracker()
    return tracker.get("records", {}).get(item_id)


def merge() -> dict:
    """合并 queue 和 tracker，返回 merged view。
    
    规则：tracker 覆盖 queue 的 reviewStatus / trackingStatus 初始值。
    queue 的其他字段（title/score/confirmLevel 等）完全保留。
    """
    if not QUEUE.exists():
        print("[WARN] analyst-review-queue.json 不存在，请先运行 build", file=sys.stderr)
        return {}

    queue_data = json.loads(QUEUE.read_text(encoding='utf-8'))
    tracker = _load_tracker()
    tracker_records = tracker.get("records", {})

    merged_items = []
    for item in queue_data.get("items", []):
        item_id = item.get("id", "")
        tracked = tracker_records.get(item_id, {})

        merged = dict(item)
        # tracker 覆盖 queue 的状态字段（若 tracker 中存在该 itemId）
        if tracked:
            merged["reviewStatus"] = tracked.get("reviewStatus", item.get("reviewStatus", "pending"))
            merged["trackingStatus"] = tracked.get("trackingStatus", item.get("trackingStatus", "pending"))
            merged["trackerUpdatedAt"] = tracked.get("updatedAt", None)
            merged["trackerNote"] = tracked.get("note", "")
        # 若 tracker 中不存在，保持 queue 原始值
        # （已在 merged = dict(item) 中保留）

        merged_items.append(merged)

    return {"items": merged_items, "total": len(merged_items)}


def export_csv(output_path: str = None) -> str:
    """将 merge 结果导出为 CSV（pilot-tracking-ledger.csv）
    
    字段：itemId / analystName / articleTitle / confirmLevel / reviewStatus / trackingStatus / updatedAt / note / source
    用途：面向运营编辑者的轻量追踪表，用于试点沟通与状态复核
    """
    import csv
    result = merge()
    if not result or not result.get("items"):
        print("[WARN] merge 结果为空，无法导出 CSV", file=sys.stderr)
        return ""

    if output_path is None:
        output_path = str(BASE / "reports" / "pilot-tracking-ledger.csv")

    fieldnames = [
        "itemId",
        "analystName",
        "articleTitle",
        "confirmLevel",
        "reviewStatus",
        "trackingStatus",
        "updatedAt",
        "note",
        "source"
    ]

    rows = []
    for item in result["items"]:
        # 优先用 tracker 的 updatedAt（人工操作时间），fallback 到 queue 的 updatedAt
        updated_at = item.get("trackerUpdatedAt") or item.get("updatedAt", "")
        rows.append({
            "itemId": item.get("id", ""),
            "analystName": item.get("source", ""),        # queue 中 source 即 analystName
            "articleTitle": item.get("articleTitle", ""),
            "confirmLevel": item.get("confirmLevel", ""),
            "reviewStatus": item.get("reviewStatus", "pending"),
            "trackingStatus": item.get("trackingStatus", "pending"),
            "updatedAt": updated_at,
            "note": item.get("trackerNote", ""),
            "source": item.get("source", "")               # 保留 source 用于来源聚合统计
        })

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path
def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="review-tracker：状态台账工具")
    sub = parser.add_subparsers(dest="cmd")

    # upsert
    p_upsert = sub.add_parser("upsert", help="upsert 单条状态")
    p_upsert.add_argument("--item-id", required=True, help="itemId，如 analyst-72873eb4")
    p_upsert.add_argument("--review-status", choices=["pending", "confirmed", "rejected"], help="review 状态")
    p_upsert.add_argument("--tracking-status", choices=["pending", "candidate", "follow_up", "closed"], help="tracking 状态")
    p_upsert.add_argument("--note", default="", help="状态变更备注")

    # get
    p_get = sub.add_parser("get", help="查询单条状态")
    p_get.add_argument("--item-id", required=True)

    # merge
    sub.add_parser("merge", help="输出 merged view（queue + tracker 合并）")

    # export
    p_export = sub.add_parser("export", help="导出 merged view 为 CSV（pilot-tracking-ledger.csv）")
    p_export.add_argument("--output", default=None, help="输出路径，默认 reports/pilot-tracking-ledger.csv")

    args = parser.parse_args()

    if args.cmd == "upsert":
        rec = upsert(args.item_id, args.review_status, args.tracking_status, args.note)
        print(f"[OK] {rec['itemId']} -> reviewStatus={rec['reviewStatus']} trackingStatus={rec['trackingStatus']} updatedAt={rec['updatedAt']}")

    elif args.cmd == "get":
        rec = get(args.item_id)
        if rec:
            print(json.dumps(rec, ensure_ascii=False, indent=2))
        else:
            print(f"[INFO] {args.item_id} 在 tracker 中不存在")

    elif args.cmd == "merge":
        result = merge()
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("[ERROR] merge 失败", file=sys.stderr)
            sys.exit(1)

    elif args.cmd == "export":
        path = export_csv(args.output)
        if path:
            print(f"[OK] CSV 已导出: {path}")
        else:
            print("[ERROR] CSV 导出失败", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
