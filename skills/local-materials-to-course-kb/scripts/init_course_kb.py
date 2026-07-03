#!/usr/bin/env python3
"""Initialize the course area inside a local Markdown knowledge base."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Optional


DEFAULT_VAULT_ROOT = Path.home() / "Documents" / "个人知识库"

CATEGORIES = [
    ("A-岗前通用&基础认知", "岗前通用、基础认知、通用工作方法"),
    ("B-Amazon运营&Listing优化", "Amazon日常运营、Listing、内容与转化"),
    ("C-广告推广&站外增长", "广告、推广、站外、增长策略"),
    ("D-选品调研&产品开发", "选品、类目、竞品产品、产品开发与迭代"),
    ("E-项目管理&跨部门协作", "项目推进、会议、协作、复盘"),
    ("F-制度流程&SOP宣讲", "制度、流程、SOP、标准动作宣讲"),
    ("G-管理领导力&导师培养", "管理、领导力、辅导、导师培养"),
    ("H-个人成长&读书技能分享", "读书、技能、思考模型、个人成长"),
]


def resolve_roots(
    vault_root: Optional[Path] = None,
    course_root: Optional[Path] = None,
) -> tuple[Path, Path, Path]:
    if vault_root is not None:
        vault = vault_root.expanduser()
        course = vault / "知识库" / "课程知识库"
    elif course_root is not None:
        course = course_root.expanduser()
        if course.parent.name == "知识库":
            vault = course.parent.parent
        else:
            vault = course
    else:
        vault = DEFAULT_VAULT_ROOT
        course = vault / "知识库" / "课程知识库"
    queue = vault / "素材" / "待整理"
    return vault, course, queue


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def category_index(name: str, desc: str) -> str:
    today = date.today().isoformat()
    return f"""# {name}

用途：{desc}

创建日期：{today}

主题入口：[[01_知识主文档]]；正文按主题存放在 `01_知识主题/`。

## 已沉淀资料索引

| 日期 | 来源资料 | 写入位置 | 核心主题 | 可用于课程 |
|---|---|---|---|---|

## 相关课程引用

| 课程/模块 | 引用内容 | 对应文档位置 |
|---|---|---|
"""


def knowledge_entry(name: str) -> str:
    return f"""# {name} - 知识主文档

> 本页只做主题导航。新增正文写入 `01_知识主题/`，不要在入口页持续追加长内容。

## 主题导航
"""


def case_doc(name: str) -> str:
    return f"""# {name} - 案例库

> 放真实案例、截图、图表、页面视觉和对比图。每个案例都要注明来源和教学用途。

## 案例列表

| 日期 | 案例标题 | 图片文件 | 可讲主题 | 来源 |
|---|---|---|---|---|
"""


def template_doc(name: str) -> str:
    return f"""# {name} - 可复用话术&模板

> 放 SOP、检查清单、课程话术和模板说明，不放未经审核的风险操作步骤。

## SOP

## 检查清单

## 课程讲解话术

## AI 提示词模板
"""


def root_index() -> str:
    today = date.today().isoformat()
    rows = "\n".join(f"| {name} | {desc} | | | |" for name, desc in CATEGORIES)
    return f"""# 课程知识库

创建日期：{today}

## 使用原则

1. 原始资料只读保存，不覆盖。
2. 每份资料只进入一个主分类。
3. 先审核、去重，再沉淀。
4. 分类入口页只负责导航，正文按主题拆页。
5. 过时、错误、证据不足和高风险内容进入审核记录。

## 八大分类总览

| 分类 | 用途 | 累计资料数 | 主要课程 | 最近更新 |
|---|---|---|---|---|
{rows}

## 最近处理记录

| 日期 | 来源资料 | 主分类 | 处理结果 | 备注 |
|---|---|---|---|---|
"""


def audit_doc() -> str:
    return """# 审核与不沉淀记录

> 记录不适合进入正式知识页的内容，包括过时、错误、证据不足、待核验和高风险内容。

## 不沉淀知识清单

| 日期 | 来源资料 | 内容摘要 | 判断 | 不沉淀原因 | 安全保留内容 | 建议动作 |
|---|---|---|---|---|---|---|
"""


def current_batch_status_doc() -> str:
    return """# 当前批次状态

> 每次沉淀前先查看这里。存在未完成批次时，先恢复，不选择新资料。

## 当前状态

| 字段 | 内容 |
|---|---|
| queue_status | 未开始 |
| batch_id |  |
| source_files |  |
| current_stage |  |
| completed_work |  |
| pending_work |  |
| chosen_primary_category |  |
| audit_status |  |
| index_update_status |  |
| next_action |  |
"""


def pending_queue_doc() -> str:
    return """# 待处理资料队列

| 日期 | 文件/文件夹路径 | 推断主题 | 可能分类 | 复杂度 | 信息密度 | 建议批次 | 状态 |
|---|---|---|---|---|---|---|---|
"""


def init_kb(course_root: Path, queue_root: Path, dry_run: bool = False) -> None:
    targets: list[tuple[Path, str | None]] = [
        (course_root / "00_总索引.md", root_index()),
        (course_root / "99_审核与不沉淀记录.md", audit_doc()),
        (
            course_root / "00_任务状态" / "当前批次状态.md",
            current_batch_status_doc(),
        ),
        (
            course_root / "00_任务状态" / "待处理资料队列.md",
            pending_queue_doc(),
        ),
        (queue_root / "TBD", None),
        (queue_root / "Done", None),
        (queue_root / "待复核" / "课程资料", None),
        (queue_root / "待复核" / "创作复盘", None),
    ]

    for name, desc in CATEGORIES:
        category_dir = course_root / name
        targets.extend(
            [
                (category_dir / "00_索引.md", category_index(name, desc)),
                (category_dir / "01_知识主文档.md", knowledge_entry(name)),
                (category_dir / "01_知识主题", None),
                (category_dir / "02_案例库.md", case_doc(name)),
                (category_dir / "03_可复用话术&模板.md", template_doc(name)),
                (category_dir / "images", None),
            ]
        )

    created = 0
    skipped = 0
    for path, content in targets:
        if dry_run:
            action = "mkdir" if content is None else "write"
            print(f"[dry-run] {action}: {path}")
            continue
        if content is None:
            if path.exists():
                skipped += 1
            else:
                path.mkdir(parents=True, exist_ok=True)
                created += 1
        elif write_if_missing(path, content):
            created += 1
        else:
            skipped += 1

    if not dry_run:
        print(f"Course knowledge base ready: {course_root}")
        print(f"Queue ready: {queue_root}")
        print(f"Created: {created}")
        print(f"Skipped existing: {skipped}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a course knowledge base inside a Markdown vault."
    )
    parser.add_argument("--vault-root", type=Path)
    parser.add_argument(
        "--root",
        type=Path,
        help="Existing course root; prefer --vault-root for new installations.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    _vault, course, queue = resolve_roots(args.vault_root, args.root)
    init_kb(course, queue, args.dry_run)


if __name__ == "__main__":
    main()
