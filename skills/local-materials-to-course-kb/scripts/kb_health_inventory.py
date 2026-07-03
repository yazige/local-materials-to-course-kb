#!/usr/bin/env python3
"""Build a bounded, read-only knowledge-base health inventory without leaking body text."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote


WIKI_LINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PENDING_RE = re.compile(r"待确认|冲突待确认|TODO|待整理|待补充", re.IGNORECASE)
STALE_RE = re.compile(r"可能过时|已过期|过期", re.IGNORECASE)
ENTRY_NAMES = {
    "README.md",
    "AGENTS.md",
    "index.md",
    "log.md",
    "00_总索引.md",
    "00_索引.md",
    "01_知识主文档.md",
    "02_案例库.md",
    "03_可复用话术&模板.md",
    "99_审核与不沉淀记录.md",
    "当前批次状态.md",
    "待处理资料队列.md",
}
SKIP_PARTS = {".git", ".obsidian", ".claude", ".workbuddy", "__pycache__"}
SOURCE_PARTS = {
    "素材",
    "raw",
    "TBD",
    "Done",
    "02_转写稿",
    "98_音视频处理工作区",
}


def relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_hidden_or_internal(root: Path, path: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    return any(part.startswith(".") or part in SKIP_PARTS for part in rel_parts)


def is_source_material(root: Path, path: Path) -> bool:
    rel_parts = set(path.relative_to(root).parts)
    return bool(rel_parts & SOURCE_PARTS) or "转写稿" in path.name


def limited(items: list[Any], limit: int) -> dict[str, Any]:
    return {
        "total": len(items),
        "items": items[:limit],
        "truncated": len(items) > limit,
    }


def normalize_target(raw_target: str) -> str | None:
    target = unquote(raw_target.strip().strip("<>"))
    if not target or "://" in target or target.startswith(("mailto:", "#")):
        return None
    target = target.split("#", 1)[0].strip()
    return target or None


def resolve_target(vault: Path, source: Path, target: str) -> Path | None:
    candidate = Path(target)
    candidates = [source.parent / candidate, vault / candidate]
    expanded: list[Path] = []
    for item in candidates:
        expanded.append(item)
        if not item.suffix:
            expanded.append(item.with_suffix(".md"))
    for item in expanded:
        if item.exists():
            return item.resolve()
    return expanded[-1].resolve() if expanded else None


def extract_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in WIKI_LINK_RE.finditer(text):
        raw = match.group(1).split("|", 1)[0]
        normalized = normalize_target(raw)
        if normalized:
            targets.append(normalized)
    for match in MARKDOWN_LINK_RE.finditer(text):
        normalized = normalize_target(match.group(1))
        if normalized:
            targets.append(normalized)
    return targets


def visible_top_level_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for child in path.iterdir() if not child.name.startswith("."))


def build_report(vault: Path, limit: int = 50) -> dict[str, Any]:
    vault = vault.expanduser().resolve()
    all_files = [
        path
        for path in vault.rglob("*")
        if path.is_file() and not is_hidden_or_internal(vault, path)
    ]
    markdown_paths = [path for path in all_files if path.suffix.lower() == ".md"]
    source_markdown = [
        path for path in markdown_paths if is_source_material(vault, path)
    ]
    scanned_markdown = [
        path for path in markdown_paths if not is_source_material(vault, path)
    ]
    scanned_set = {path.resolve() for path in scanned_markdown}

    inbound: defaultdict[Path, int] = defaultdict(int)
    broken_links: list[dict[str, str]] = []
    pending: set[str] = set()
    stale: set[str] = set()
    digest_paths: defaultdict[str, list[str]] = defaultdict(list)

    for path in scanned_markdown:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel_path = relative(vault, path)
        if PENDING_RE.search(text):
            pending.add(rel_path)
        if STALE_RE.search(text):
            stale.add(rel_path)
        if path.stat().st_size >= 20:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            digest_paths[digest].append(rel_path)
        for target in extract_targets(text):
            resolved = resolve_target(vault, path, target)
            if resolved is None or not resolved.exists():
                broken_links.append({"source": rel_path, "target": target})
            elif resolved in scanned_set:
                inbound[resolved] += 1

    duplicate_groups = [
        {"paths": sorted(paths)}
        for paths in digest_paths.values()
        if len(paths) > 1
    ]
    duplicate_groups.sort(key=lambda item: item["paths"])

    topic_pages = [
        path
        for path in scanned_markdown
        if "01_知识主题" in path.parts and path.name not in ENTRY_NAMES
    ]
    orphan_candidates = sorted(
        relative(vault, path) for path in topic_pages if inbound[path.resolve()] == 0
    )

    queue = vault / "素材" / "待整理"
    tbd_count = visible_top_level_count(queue / "TBD")
    course_review_count = visible_top_level_count(queue / "待复核" / "课程资料")
    creation_review_count = visible_top_level_count(
        queue / "待复核" / "创作复盘"
    )

    broken_links.sort(key=lambda item: (item["source"], item["target"]))
    duplicate_groups.sort(key=lambda item: item["paths"])
    pending_items = sorted(pending)
    stale_items = sorted(stale)

    summary = {
        "files_total": len(all_files),
        "markdown_scanned": len(scanned_markdown),
        "source_markdown_skipped": len(source_markdown),
        "broken_links": len(broken_links),
        "exact_duplicate_groups": len(duplicate_groups),
        "orphan_candidates": len(orphan_candidates),
        "pending_confirmation": len(pending_items),
        "stale_candidates": len(stale_items),
        "index_uncovered": len(orphan_candidates),
        "tbd_items": tbd_count,
        "course_review_items": course_review_count,
        "creation_review_items": creation_review_count,
    }
    return {
        "vault_root": str(vault),
        "read_only": True,
        "body_text_included": False,
        "candidate_limit": limit,
        "summary": summary,
        "candidates": {
            "broken_links": limited(broken_links, limit),
            "exact_duplicate_groups": limited(duplicate_groups, limit),
            "orphan_candidates": limited(orphan_candidates, limit),
            "pending_confirmation": limited(pending_items, limit),
            "stale_candidates": limited(stale_items, limit),
            "index_uncovered": limited(orphan_candidates, limit),
        },
    }


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(f"Vault: {report['vault_root']}")
    print("模式: 只读；不输出页面正文")
    for key, value in summary.items():
        print(f"- {key}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="只读统计知识库健康候选，不输出页面正文。"
    )
    parser.add_argument("--vault-root", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit 必须大于 0")
    if not args.vault_root.expanduser().is_dir():
        parser.error("知识库目录不存在")

    report = build_report(args.vault_root, args.limit)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
