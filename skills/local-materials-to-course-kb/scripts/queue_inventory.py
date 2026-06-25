#!/usr/bin/env python3
"""Inventory the course knowledge-base queue without reading source content."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from init_course_kb import DEFAULT_ROOT


KNOWN_STATUSES = {"处理中", "测试中", "待复核", "已写入", "已归档", "已完成"}


def visible_children(path: Path) -> tuple[list[dict[str, str]], int]:
    if not path.exists():
        return [], 0

    items: list[dict[str, str]] = []
    hidden_count = 0
    for child in sorted(path.iterdir(), key=lambda item: item.name):
        if child.name.startswith("."):
            hidden_count += 1
            continue
        items.append(
            {
                "name": child.name,
                "path": str(child),
                "type": "folder" if child.is_dir() else "file",
            }
        )
    return items, hidden_count


def status_from_name(name: str) -> str:
    suffix = name.rsplit("_", 1)[-1] if "_" in name else ""
    return suffix if suffix in KNOWN_STATUSES else "未标注"


def build_inventory(root: Path) -> dict:
    root = root.expanduser()
    media = root / "media"
    tbd = media / "TBD"
    done = media / "Done"
    work_area = root / "98_音视频处理工作区"

    tbd_items, tbd_hidden = visible_children(tbd)
    done_items, done_hidden = visible_children(done)
    _, media_hidden = visible_children(media)

    work_items: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    if work_area.exists():
        for child in sorted(work_area.iterdir(), key=lambda item: item.name):
            if child.name.startswith(".") or not child.is_dir():
                continue
            status = status_from_name(child.name)
            status_counts[status] += 1
            work_items.append(
                {
                    "name": child.name,
                    "path": str(child),
                    "status": status,
                }
            )

    review_backlog = [item for item in work_items if item["status"] == "待复核"]
    if review_backlog:
        next_action = "先收口 98_音视频处理工作区 的待复核内容，再从 TBD 选择新批次。"
    elif tbd_items:
        next_action = "从 media/TBD 选择一个主题清晰、规模合适的批次继续沉淀。"
    else:
        next_action = "当前 TBD 队列为空；无需处理 Done，等待新资料进入 TBD。"

    return {
        "root": str(root),
        "media": {
            "tbd_path": str(tbd),
            "done_path": str(done),
            "tbd_count": len(tbd_items),
            "done_count": len(done_items),
            "hidden_ignored_count": media_hidden + tbd_hidden + done_hidden,
            "tbd_items": tbd_items,
            "done_items": done_items,
        },
        "work_area": {
            "path": str(work_area),
            "exists": work_area.exists(),
            "total_dirs": len(work_items),
            "status_counts": dict(sorted(status_counts.items())),
            "review_backlog": review_backlog,
        },
        "next_recommended_action": next_action,
    }


def render_markdown(report: dict, limit: int) -> str:
    lines = [
        "# 本地资料转课程知识库队列盘点",
        "",
        f"- 根目录：`{report['root']}`",
        f"- TBD 待处理顶层项：{report['media']['tbd_count']}",
        f"- Done 已归档顶层项：{report['media']['done_count']}",
        f"- 已忽略隐藏/System 文件：{report['media']['hidden_ignored_count']}",
        f"- 音视频处理工作区：{report['work_area']['total_dirs']} 个",
        f"- 建议动作：{report['next_recommended_action']}",
        "",
        "## TBD 顶层资料",
        "",
        "| 序号 | 类型 | 名称 |",
        "|---:|---|---|",
    ]
    for index, item in enumerate(report["media"]["tbd_items"][:limit], start=1):
        lines.append(f"| {index} | {item['type']} | {item['name']} |")
    if report["media"]["tbd_count"] > limit:
        lines.append(f"|  |  | 还有 {report['media']['tbd_count'] - limit} 项未显示 |")

    lines.extend(["", "## 待复核工作区", "", "| 序号 | 状态 | 名称 |", "|---:|---|---|"])
    for index, item in enumerate(report["work_area"]["review_backlog"][:limit], start=1):
        lines.append(f"| {index} | {item['status']} | {item['name']} |")
    if len(report["work_area"]["review_backlog"]) > limit:
        remaining = len(report["work_area"]["review_backlog"]) - limit
        lines.append(f"|  |  | 还有 {remaining} 个待复核工作区未显示 |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventory media/TBD, media/Done, and review work areas."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    report = build_inventory(args.root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report, args.limit), end="")


if __name__ == "__main__":
    main()
