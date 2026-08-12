#!/usr/bin/env python3
"""Verify the portable vault layout and course knowledge-base structure."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Optional

from init_course_kb import CATEGORIES, DEFAULT_VAULT_ROOT, resolve_roots


IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
EXPECTED_CATEGORY_NAMES = {name for name, _desc in CATEGORIES}


def relative_label(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add_missing(errors: list[str], root: Path, path: Path, kind: str) -> None:
    exists = path.is_dir() if kind == "folder" else path.is_file()
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


def cleanup_macos_metadata(root: Path) -> int:
    """Remove Finder metadata only; never touch other hidden files or folders."""
    removed = 0
    for path in sorted(root.rglob(".DS_Store")):
        if path.is_file() or path.is_symlink():
            path.unlink()
            removed += 1
    return removed


def build_report(
    vault_root: Optional[Path] = None,
    course_root: Optional[Path] = None,
) -> dict:
    vault, course, queue = resolve_roots(vault_root, course_root)
    errors: list[str] = []
    warnings: list[str] = []
    macos_metadata_removed_count = cleanup_macos_metadata(vault)

    required_files = [
        course / "00_总索引.md",
        course / "99_审核与不沉淀记录.md",
        course / "00_任务状态" / "当前批次状态.md",
        course / "00_任务状态" / "待处理资料队列.md",
    ]
    required_folders = [
        vault,
        course,
        course / "00_任务状态",
        queue,
        queue / "TBD",
        queue / "Done",
        queue / "待复核",
        queue / "待复核" / "课程资料",
        queue / "待复核" / "创作复盘",
    ]

    for path in required_folders:
        add_missing(errors, vault, path, "folder")
    for path in required_files:
        add_missing(errors, vault, path, "file")

    category_reports = []
    for category, _desc in CATEGORIES:
        category_dir = course / category
        add_missing(errors, vault, category_dir, "folder")
        category_files = [
            category_dir / "00_索引.md",
            category_dir / "01_知识主文档.md",
            category_dir / "02_案例库.md",
            category_dir / "03_可复用话术&模板.md",
        ]
        add_missing(errors, vault, category_dir / "01_知识主题", "folder")
        add_missing(errors, vault, category_dir / "images", "folder")
        for path in category_files:
            add_missing(errors, vault, path, "file")
        if category_dir.exists():
            markdown_files = category_files + list(
                (category_dir / "01_知识主题").glob("*.md")
            )
            for path in markdown_files:
                check_markdown_images(vault, path, errors)
        category_reports.append({"name": category, "path": str(category_dir)})

    if course.exists():
        actual_categories = {
            child.name
            for child in course.iterdir()
            if child.is_dir() and len(child.name) > 2 and child.name[1:2] == "-"
        }
        for name in sorted(actual_categories - EXPECTED_CATEGORY_NAMES):
            warnings.append(f"发现额外分类，验证器未将其计入标准八类: {name}")

    for active in sorted(queue.glob("当前批次_*_处理中")):
        warnings.append(f"发现未完成当前批次: {relative_label(vault, active)}")

    review_area = queue / "待复核" / "课程资料"
    work_status_counts: dict[str, int] = {}
    if review_area.exists():
        for child in sorted(review_area.iterdir(), key=lambda item: item.name):
            if child.name.startswith("."):
                continue
            status = visible_status(child.name)
            work_status_counts[status] = work_status_counts.get(status, 0) + 1
        review_count = work_status_counts.get("待复核", 0)
        if review_count:
            warnings.append(
                f"课程资料区有 {review_count} 项待复核，建议先盘点收口。"
            )

    return {
        "vault_root": str(vault),
        "course_root": str(course),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "category_count": len(category_reports),
        "course_review_status_counts": work_status_counts,
        "macos_metadata_removed_count": macos_metadata_removed_count,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# 本地资料转课程知识库结构验证",
        "",
        f"- 知识库根目录：`{report['vault_root']}`",
        f"- 课程知识库：`{report['course_root']}`",
        f"- 结构状态：{'通过' if report['ok'] else '存在错误'}",
        f"- 标准分类数量：{report['category_count']}",
    ]
    if report["macos_metadata_removed_count"]:
        lines.append(
            "- 已自动清理 macOS Finder 元数据："
            f"{report['macos_metadata_removed_count']} 个 `.DS_Store`"
        )
    lines.extend([
        "",
        "## 错误",
        "",
    ])
    lines.extend(f"- {item}" for item in report["errors"]) if report[
        "errors"
    ] else lines.append("- 无")

    lines.extend(["", "## 警告", ""])
    lines.extend(f"- {item}" for item in report["warnings"]) if report[
        "warnings"
    ] else lines.append("- 无")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check the vault queue, course pages, image links, and review backlog."
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
    args = parser.parse_args()

    if args.root is not None and args.vault_root is None:
        report = build_report(course_root=args.root)
    else:
        report = build_report(vault_root=args.vault_root or DEFAULT_VAULT_ROOT)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
