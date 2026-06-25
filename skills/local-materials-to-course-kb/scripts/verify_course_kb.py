#!/usr/bin/env python3
"""Verify the course knowledge-base structure and common maintenance issues."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from init_course_kb import CATEGORIES, DEFAULT_ROOT


IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def relative_label(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add_missing(errors: list[str], root: Path, path: Path, kind: str) -> None:
    if kind == "folder":
        exists = path.is_dir()
    else:
        exists = path.is_file()
    if not exists:
        errors.append(f"缺少{kind}: {relative_label(root, path)}")


def visible_status(name: str) -> str:
    return name.rsplit("_", 1)[-1] if "_" in name else "未标注"


def check_markdown_images(root: Path, markdown_file: Path, errors: list[str]) -> None:
    if not markdown_file.exists():
        return

    text = markdown_file.read_text(encoding="utf-8")
    for match in IMAGE_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if "://" in target or target.startswith("#"):
            continue
        target_path = Path(target)
        if not target_path.is_absolute():
            target_path = markdown_file.parent / target_path
        if not target_path.exists():
            label = relative_label(root, markdown_file)
            errors.append(f"图片链接不存在: {label} -> {target}")


def build_report(root: Path) -> dict:
    root = root.expanduser()
    errors: list[str] = []
    warnings: list[str] = []

    required_files = [
        root / "00_总索引.md",
        root / "99_审核与不沉淀记录.md",
        root / "00_任务状态" / "当前批次状态.md",
        root / "00_任务状态" / "待处理资料队列.md",
    ]
    required_folders = [
        root,
        root / "00_任务状态",
        root / "media",
        root / "media" / "TBD",
        root / "media" / "Done",
    ]

    for path in required_folders:
        add_missing(errors, root, path, "folder")
    for path in required_files:
        add_missing(errors, root, path, "file")

    category_reports = []
    for category, _desc in CATEGORIES:
        category_dir = root / category
        add_missing(errors, root, category_dir, "folder")
        category_files = [
            category_dir / "00_索引.md",
            category_dir / "01_知识主文档.md",
            category_dir / "02_案例库.md",
            category_dir / "03_可复用话术&模板.md",
        ]
        add_missing(errors, root, category_dir / "images", "folder")
        for path in category_files:
            add_missing(errors, root, path, "file")
            check_markdown_images(root, path, errors)
        category_reports.append({"name": category, "path": str(category_dir)})

    for hidden in sorted(root.rglob(".DS_Store")):
        warnings.append(f"发现 macOS 隐藏文件，可忽略或清理: {relative_label(root, hidden)}")

    media = root / "media"
    if media.exists():
        for active in sorted(media.glob("当前批次_*_处理中")):
            warnings.append(f"发现未完成当前批次: {relative_label(root, active)}")

    work_area = root / "98_音视频处理工作区"
    work_status_counts: dict[str, int] = {}
    if work_area.exists():
        for child in sorted(work_area.iterdir(), key=lambda item: item.name):
            if child.name.startswith(".") or not child.is_dir():
                continue
            status = visible_status(child.name)
            work_status_counts[status] = work_status_counts.get(status, 0) + 1
        review_count = work_status_counts.get("待复核", 0)
        if review_count:
            warnings.append(
                f"98_音视频处理工作区 有 {review_count} 个待复核工作区，建议先盘点收口。"
            )

    return {
        "root": str(root),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "category_count": len(category_reports),
        "work_area_status_counts": work_status_counts,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# 本地资料转课程知识库结构验证",
        "",
        f"- 根目录：`{report['root']}`",
        f"- 结构状态：{'通过' if report['ok'] else '存在错误'}",
        f"- 分类数量：{report['category_count']}",
        "",
        "## 错误",
        "",
    ]
    if report["errors"]:
        lines.extend(f"- {item}" for item in report["errors"])
    else:
        lines.append("- 无")

    lines.extend(["", "## 警告", ""])
    if report["warnings"]:
        lines.extend(f"- {item}" for item in report["warnings"])
    else:
        lines.append("- 无")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check required folders, Markdown image links, and queue state."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    report = build_report(args.root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
