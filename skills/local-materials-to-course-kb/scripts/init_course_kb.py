#!/usr/bin/env python3
"""Initialize the local course knowledge-base folder structure."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


DEFAULT_ROOT = (
    Path.home()
    / "Desktop"
    / "AI工作台"
    / "06_培训教程与分享资料"
    / "本地资料转课程知识库"
)

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

## 本分类适合放什么

- {desc}
- 只放本分类主场景内容。跨课程复用时在索引中引用，不重复复制正文。
- 费用、政策、平台入口、官方福利等强时效内容先进入审核记录，复核后再用于课程。

## 已沉淀资料索引

| 日期 | 来源资料 | 写入位置 | 核心主题 | 可用于课程 |
|---|---|---|---|---|

## 相关课程引用

| 课程/模块 | 引用内容 | 对应文档位置 |
|---|---|---|
"""


def knowledge_doc(name: str) -> str:
    return f"""# {name} - 知识主文档

> 只沉淀经过审核、适合长期复用的知识。过时、错误、高风险或待核验内容不要写入这里。

## 稳定知识

## 方法框架

## 课程讲解要点
"""


def case_doc(name: str) -> str:
    return f"""# {name} - 案例库

> 放真实案例、截图、图表、页面视觉、对比图。每张图片必须能解释它适合讲什么。

## 案例列表

| 日期 | 案例标题 | 图片文件 | 可讲主题 | 来源 |
|---|---|---|---|---|
"""


def template_doc(name: str) -> str:
    return f"""# {name} - 可复用话术&模板

> 放 SOP、检查清单、课程话术、提示词、表格模板说明。不要放未经审核的风险操作步骤。

## SOP

## 检查清单

## 课程讲解话术

## AI 提示词模板
"""


def root_index() -> str:
    today = date.today().isoformat()
    rows = "\n".join(f"| {name} | {desc} | | | |" for name, desc in CATEGORIES)
    return f"""# 本地资料转课程知识库

创建日期：{today}

## 使用原则

1. 原始资料不覆盖、不删除、不直接修改。
2. 每份资料只进入一个主分类。
3. 先审核，再沉淀。
4. 过时、错误、证据不足、高风险内容进入 `99_审核与不沉淀记录.md`。
5. 黑科技只保留风险识别、防御、自查和合规替代方案，不保留可执行教程。

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

> 记录不适合进入主知识库的内容，包括过时、错误、证据不足、待核验、高风险和仅保留防御的内容。

## 不沉淀知识清单

| 日期 | 来源资料 | 内容摘要 | 判断 | 不沉淀原因 | 可保留的安全知识 | 建议动作 |
|---|---|---|---|---|---|---|

## 高风险/黑科技防御记录

| 日期 | 来源资料 | 风险类型 | 高层描述 | 防御与自查 | 合规替代方案 |
|---|---|---|---|---|---|
"""


def current_batch_status_doc() -> str:
    return """# 当前批次状态

> 自动化或人工继续沉淀前，先查看这里。若无未完成批次，填写 queue_status 即可。

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
| subagent_card_locations |  |
| audit_status |  |
| index_update_status |  |
| next_action |  |
"""


def pending_queue_doc() -> str:
    return """# 待处理资料队列

> 当新资料暂不适合立刻沉淀，或自动化需要记录下一批建议时，写在这里。

| 日期 | 文件/文件夹路径 | 推断主题 | 可能分类 | 复杂度 | 信息密度 | 建议批次 | 状态 |
|---|---|---|---|---|---|---|---|
"""


def init_kb(root: Path, dry_run: bool) -> None:
    targets: list[tuple[Path, str | None]] = [
        (root / "00_总索引.md", root_index()),
        (root / "99_审核与不沉淀记录.md", audit_doc()),
        (root / "00_任务状态" / "当前批次状态.md", current_batch_status_doc()),
        (root / "00_任务状态" / "待处理资料队列.md", pending_queue_doc()),
        (root / "media" / "TBD", None),
        (root / "media" / "Done", None),
    ]

    for name, desc in CATEGORIES:
        category_dir = root / name
        targets.extend(
            [
                (category_dir / "00_索引.md", category_index(name, desc)),
                (category_dir / "01_知识主文档.md", knowledge_doc(name)),
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
        print(f"Knowledge base ready: {root}")
        print(f"Created: {created}")
        print(f"Skipped existing: {skipped}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the local course knowledge-base directory template."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"Knowledge-base root path. Default: {DEFAULT_ROOT}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files.",
    )
    args = parser.parse_args()
    init_kb(args.root.expanduser(), args.dry_run)


if __name__ == "__main__":
    main()
