#!/usr/bin/env python3
"""Initialize a portable Markdown personal knowledge base."""

from __future__ import annotations

import argparse
from pathlib import Path

from init_course_kb import DEFAULT_VAULT_ROOT, init_kb, resolve_roots, write_if_missing


README = """# 我的个人知识库

第一次打开先看：

1. [[index]]
2. [[AGENTS]]
3. [[知识库/课程知识库/00_总索引]]
4. [[素材/待整理/README]]

AI 接手时先读入口文件，再按当前任务只读取相关主题页，不扫描全库。
"""

AGENTS = """# 个人知识库维护规则

1. 开始时只读 `README.md`、`AGENTS.md`、`index.md` 和当前任务相关页面。
2. 原始资料放入 `素材/待整理/TBD`，不覆盖、不编造。
3. 每次最多处理一个合理批次；完成后原资料移入 `Done`。
4. 课程正文写入分类下的 `01_知识主题/`，`01_知识主文档.md` 只做导航。
5. `待复核/课程资料` 与 `待复核/创作复盘` 分开处理。
6. 更新知识后同步更新索引和 `log.md`。
7. 删除、部署、上传、凭证和计费操作必须先确认。
"""

INDEX = """# 知识库索引

## 课程知识库

- [[知识库/课程知识库/00_总索引]]
- [[知识库/课程知识库/00_任务状态/当前批次状态]]

## 素材

- [[素材/待整理/README]]

## 复盘

- `reviews/`：创作复盘记录。
- `wiki/`：稳定写作规律和协作规则。
"""

MATERIALS_ROOT_README = """# 素材

新资料统一放入 `待整理/TBD/`。不要把原始资料直接写进正式知识页。

队列说明见 [[待整理/README]]。
"""

MATERIALS_README = """# 素材待整理区

| 文件夹 | 用途 |
|---|---|
| `TBD/` | 等待处理的新资料 |
| `Done/` | 已完成沉淀的原始资料，只读 |
| `待复核/课程资料/` | 等待确认的课程草稿 |
| `待复核/创作复盘/` | AI 初稿、修改意见和最终稿 |
"""


def init_personal_kb(vault: Path, dry_run: bool = False) -> None:
    targets: list[tuple[Path, str | None]] = [
        (vault / "README.md", README),
        (vault / "AGENTS.md", AGENTS),
        (vault / "index.md", INDEX),
        (vault / "log.md", "# 知识库更新日志\n"),
        (vault / "素材" / "README.md", MATERIALS_ROOT_README),
        (vault / "素材" / "待整理" / "README.md", MATERIALS_README),
        (vault / "reviews", None),
        (vault / "wiki", None),
    ]
    for path, content in targets:
        if dry_run:
            print(f"[dry-run] {'mkdir' if content is None else 'write'}: {path}")
        elif content is None:
            path.mkdir(parents=True, exist_ok=True)
        else:
            write_if_missing(path, content)

    _vault, course, queue = resolve_roots(vault_root=vault)
    init_kb(course, queue, dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a portable personal knowledge base and course area."
    )
    parser.add_argument("--vault-root", type=Path, default=DEFAULT_VAULT_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    init_personal_kb(args.vault_root.expanduser(), args.dry_run)


if __name__ == "__main__":
    main()
