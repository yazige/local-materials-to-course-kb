# Workspace Lifecycle Rules

## Purpose

Use this reference when the knowledge base contains `98_音视频处理工作区/`, draft folders marked `待复核`, or many generated media-package outputs waiting to be reviewed.

The work area is a review and staging zone. It is not the automatic source queue. New source materials still enter through `media/TBD/`; processed source materials still move to `media/Done/`.

## Folder Roles

| Area | Role | Rule |
|---|---|---|
| `media/TBD/` | New source-material inbox | Select only one coherent batch per run. |
| `media/当前批次_*_处理中/` | Active source batch | Preserve until the batch is complete or safely paused. |
| `media/Done/` | Processed source-material holding area | Do not re-read automatically. |
| `98_音视频处理工作区/` | Draft extraction, transcript, notes, audit, and candidate-write workspace | Review and close deliberately; do not treat every folder as new source. |

## Status Suffixes

Use one of these suffixes in work-area folder names:

| Status | Meaning | Next action |
|---|---|---|
| `处理中` | Extraction or draft creation is still active | Resume from the newest status note before selecting new sources. |
| `测试中` | Output format or extraction quality is being checked | Verify before official writes. |
| `待复核` | Drafts exist and need review, deduplication, audit, or official write decision | Prefer closing these before creating more draft work. |
| `已写入` | Approved content has been written to official category files and indexes | Keep for short-term traceability or move to archive. |
| `已归档` | Review is finished and no more action is expected | Do not reopen unless the user asks. |

## Start-of-Run Rule

At the start of a run:

1. Read `00_任务状态/当前批次状态.md`.
2. Check `media/当前批次_*_处理中/`.
3. Inventory `98_音视频处理工作区/` by status, without deep-reading every draft folder.
4. If there are many `待复核` folders, report the count and recommend a review batch before starting new extraction.
5. If the user or automation explicitly asks to continue `TBD`, still process only one coherent source batch and leave the review backlog visible.

Use `scripts/queue_inventory.py` for a quick inventory when the queue is large.

## Review-Batch Rule

When closing a `待复核` work-area folder:

1. Read only that selected work-area folder plus the official category files needed for deduplication.
2. Start from `06_待写入知识库内容/` when present; do not restart from raw media unless the draft is clearly incomplete.
3. Check `05_审核记录/` before official writes.
4. Write only approved, deduplicated, course-ready content into official category files.
5. Update root index, category index, case table, audit record, and `00_任务状态/当前批次状态.md`.
6. Rename the work-area folder from `待复核` to `已写入` only after official files and indexes are updated.
7. Rename to `已归档` when the folder is kept only for traceability and no further action is expected.

Do not delete work-area folders unless the user explicitly asks. If cleanup is needed, propose an archive move first.

## Recommended Review Inventory Output

For a large backlog, report:

| Field | Meaning |
|---|---|
| work_area_total | Total top-level folders under `98_音视频处理工作区/`. |
| status_counts | Count by suffix: `处理中`, `测试中`, `待复核`, `已写入`, `已归档`, `未标注`. |
| review_backlog | The first 10-30 `待复核` folders. |
| recommended_review_batch | 1-3 related folders to close next. |
| risk_note | Any names suggesting account safety, fees, ads policy, legal, tax, or high-risk tactics. |

## Completion Rule

Before reporting that a run is complete:

- no active source batch should be left without a status update;
- new source files should be either still in `TBD`, inside the active batch, or moved to `Done`;
- any touched work-area folder should have a clear suffix and a next action;
- official writes should be verifiable through indexes and audit records.
