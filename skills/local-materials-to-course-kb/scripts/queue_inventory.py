#!/usr/bin/env python3
"""Inventory a personal knowledge-base intake queue without reading source content."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Optional

from init_course_kb import DEFAULT_VAULT_ROOT, resolve_roots


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


def review_inventory(path: Path) -> tuple[list[dict[str, str]], Counter[str], int]:
    items: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    hidden_count = 0
    if not path.exists():
        return items, counts, hidden_count

    for child in sorted(path.iterdir(), key=lambda item: item.name):
        if child.name.startswith("."):
            hidden_count += 1
            continue
        status = status_from_name(child.name)
        counts[status] += 1
        items.append(
            {
                "name": child.name,
                "path": str(child),
                "type": "folder" if child.is_dir() else "file",
                "status": status,
            }
        )
    return items, counts, hidden_count


def build_inventory(
    vault_root: Optional[Path] = None,
    course_root: Optional[Path] = None,
) -> dict:
    vault, course, queue = resolve_roots(vault_root, course_root)
    tbd = queue / "TBD"
    done = queue / "Done"
    course_review = queue / "待复核" / "课程资料"
    creation_review = queue / "待复核" / "创作复盘"

    tbd_items, tbd_hidden = visible_children(tbd)
    done_items, done_hidden = visible_children(done)
    _, queue_hidden = visible_children(queue)
    course_items, course_counts, course_hidden = review_inventory(course_review)
    creation_items, creation_counts, creation_hidden = review_inventory(
        creation_review
    )

    review_backlog = [
        item for item in course_items if item["status"] not in {"已写入", "已归档", "已完成"}
    ]
    if review_backlog:
        next_action = "先收口“待复核/课程资料”的未完成内容，再从 TBD 选择新批次。"
    elif tbd_items:
        next_action = "从“素材/待整理/TBD”选择一个主题清晰、规模合适的批次。"
    else:
        next_action = "TBD 为空；Done 保持只读，等待新资料进入待整理队列。"

    return {
        "vault_root": str(vault),
        "course_root": str(course),
        "queue": {
            "root": str(queue),
            "tbd_path": str(tbd),
            "done_path": str(done),
            "tbd_count": len(tbd_items),
            "done_count": len(done_items),
            "hidden_ignored_count": (
                queue_hidden
                + tbd_hidden
                + done_hidden
                + course_hidden
                + creation_hidden
            ),
            "tbd_items": tbd_items,
            "done_items": done_items,
        },
        "course_review": {
            "path": str(course_review),
            "exists": course_review.exists(),
            "total_items": len(course_items),
            "status_counts": dict(sorted(course_counts.items())),
            "active_backlog": review_backlog,
        },
        "creation_review": {
            "path": str(creation_review),
            "exists": creation_review.exists(),
            "total_items": len(creation_items),
            "status_counts": dict(sorted(creation_counts.items())),
        },
        "next_recommended_action": next_action,
    }


def render_markdown(report: dict, limit: int) -> str:
    queue = report["queue"]
    review = report["course_review"]
    lines = [
        "# 本地资料转课程知识库队列盘点",
        "",
        f"- 知识库根目录：`{report['vault_root']}`",
        f"- TBD 待处理顶层项：{queue['tbd_count']}",
        f"- Done 已归档顶层项：{queue['done_count']}",
        f"- 已忽略隐藏/System 文件：{queue['hidden_ignored_count']}",
        f"- 课程资料待复核区：{review['total_items']} 项",
        f"- 创作复盘区：{report['creation_review']['total_items']} 项",
        f"- 建议动作：{report['next_recommended_action']}",
        "",
        "## TBD 顶层资料",
        "",
        "| 序号 | 类型 | 名称 |",
        "|---:|---|---|",
    ]
    for index, item in enumerate(queue["tbd_items"][:limit], start=1):
        lines.append(f"| {index} | {item['type']} | {item['name']} |")
    if queue["tbd_count"] > limit:
        lines.append(f"|  |  | 还有 {queue['tbd_count'] - limit} 项未显示 |")

    lines.extend(
        ["", "## 课程资料待复核区", "", "| 序号 | 状态 | 名称 |", "|---:|---|---|"]
    )
    for index, item in enumerate(review["active_backlog"][:limit], start=1):
        lines.append(f"| {index} | {item['status']} | {item['name']} |")
    if len(review["active_backlog"]) > limit:
        remaining = len(review["active_backlog"]) - limit
        lines.append(f"|  |  | 还有 {remaining} 项未显示 |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventory TBD, Done, course-review, and creation-review queues."
    )
    parser.add_argument(
        "--vault-root",
        type=Path,
        help="Personal knowledge-base root. This is the preferred option.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Legacy course-root option, kept for compatibility.",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    report = build_inventory(args.vault_root or DEFAULT_VAULT_ROOT, args.root)
    if args.root is not None and args.vault_root is None:
        report = build_inventory(course_root=args.root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report, args.limit), end="")


if __name__ == "__main__":
    main()
