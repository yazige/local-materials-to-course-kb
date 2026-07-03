# Workspace Lifecycle Rules

## Purpose

Use this reference when `素材/待整理/待复核/课程资料/` contains draft folders or generated course-package outputs.

The review area is not the source queue. New sources enter through `TBD`; completed sources move to `Done`.

## Folder Roles

| Area | Role | Rule |
|---|---|---|
| `素材/待整理/TBD/` | New source inbox | Select only one coherent batch per run. |
| `素材/待整理/当前批次_*_处理中/` | Active source batch | Preserve until complete or safely paused. |
| `素材/待整理/Done/` | Processed source archive | Keep read-only; do not re-read automatically. |
| `素材/待整理/待复核/课程资料/` | Draft extraction, audit and candidate-write area | Review deliberately; do not treat as new input. |
| `素材/待整理/待复核/创作复盘/` | AI draft, human feedback and final-copy comparisons | Keep separate from course-material review. |

## Status Suffixes

| Status | Meaning | Next action |
|---|---|---|
| `处理中` | Extraction or drafting is active | Resume before selecting new sources. |
| `测试中` | Output or extraction quality is being checked | Verify before official writes. |
| `待复核` | Draft needs review, deduplication or audit | Prefer closing it before adding more drafts. |
| `已写入` | Approved content is in official pages and indexes | Keep for short-term traceability. |
| `已归档` | Review is finished | Do not reopen unless asked. |

## Start-of-Run Rule

1. Read `00_任务状态/当前批次状态.md`.
2. Check `素材/待整理/当前批次_*_处理中/`.
3. Inventory `待复核/课程资料/` by status without opening every folder.
4. If many items are waiting, report the count and recommend a 1–3 item review batch.
5. If the task explicitly continues TBD, process only one coherent source batch and leave the review backlog visible.
6. Do not read raw transcripts during inventory or health checks.

Use `scripts/queue_inventory.py --vault-root "<vault>"` for a quick inventory.

## Review-Batch Rule

When closing a course review item:

1. Read only the selected item and official topic pages needed for deduplication.
2. Start from `06_待写入知识库内容/` when present; do not restart from raw media unless the draft is incomplete.
3. Check `05_审核记录/` before official writes.
4. Write approved, deduplicated content into `01_知识主题/`, then update `01_知识主文档.md` navigation.
5. Update root index, category index, case table, audit record and current batch status.
6. Mark `已写入` only after official files and indexes match.
7. Mark `已归档` when no more action is expected.

Raw transcripts may be opened only for the selected active batch after it enters extraction or review. If draft and audit files are complete, do not reopen raw transcripts merely for reassurance.

Do not delete review items unless the user explicitly asks.

## Completion Rule

- no active source batch is left without a status update;
- source files remain in TBD, the active batch, or Done;
- touched review items have a clear status and next action;
- official writes are discoverable through indexes and audit records.
