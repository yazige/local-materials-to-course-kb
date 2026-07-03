# Completion Checklist

Use this checklist before reporting completion for a sedimentation run.

## Source And Queue Safety

- Original files were not overwritten.
- Initialization Gate was run; the vault root, `00_任务状态/`, `素材/待整理/TBD/`, and `素材/待整理/Done/` exist before source intake.
- Continuation And Intake Priority Gate was run, and any unfinished previous batch was completed first or explicitly queued with a safe status handoff.
- If new materials arrived while a previous batch was unfinished, the new materials were registered separately and not silently mixed into previous official writes.
- If using the source queue, `素材/待整理/TBD/`, `Done/`, and one active batch folder were handled according to the queue rules.
- Only selected `TBD` items were moved into the active batch folder; `Done` materials were not used as new sources.
- If started by automation, the Automation Wakeup Gate was followed and at most one coherent batch was processed.
- If `TBD` still has remaining materials after one batch, they were left in `TBD` for the next run.
- If credit/context/model limits interrupted the run, active-batch files were preserved and `当前批次状态.md` contains enough detail for the next run.

## Intake And Extraction

- Batch Sizing Feedback Gate was run for folders, 3+ files, course packages, mixed formats, or uncertain categories.
- The user-facing intake feedback included material count, source types, complexity level, information density, category spread, recommended mode, and recommended batch size.
- For folder paths or multiple Word document paths, a file inventory was created before full document extraction.
- For media export packages, the primary document choice was recorded, transcript/keyframe completeness was checked, and optional PPT/user notes were handled only when useful.
- For PPT/PPTX sources, speaker notes were extracted, recorded as absent, or marked `备注待人工确认`.
- For multi-file batches, subagent file assignments were disjoint, structured knowledge cards were reviewed by the main thread, duplicate points were merged, and any subagents were closed.

## Knowledge Quality

- Exactly one primary category was chosen.
- Approved content and rejected content are separated.
- Existing category files and indexes were checked for duplicate or overlapping knowledge; duplicate content was skipped, merged, or cross-referenced instead of appended as a new section.
- Uncertain, outdated, wrong, or high-risk content is visible in the audit record.
- English or mixed-language sources were localized into Chinese course language, with no long untranslated English blocks in user-facing knowledge docs.
- New entries did not create empty placeholder sections that make the file harder to scan.

## Official Files And Indexes

- Every extracted image is referenced from a Markdown file.
- Root and category indexes were updated, including category count, main courses, latest update, and correct table placement.
- Case-list tables were filled when cases or images were added; useful entries were not left only in narrative sections.
- New knowledge was written to `01_知识主题/`; `01_知识主文档.md` remains a navigation page.
- After successful completion, processed source materials from the active batch were moved to `素材/待整理/Done/YYYY-MM-DD_批次名/`, or any failure to move them was reported clearly.
- If the active batch folder became empty after the move, it was deleted so `素材/待整理/` does not accumulate stale `当前批次_*_处理中` folders.
- If the active batch folder was not deleted, the final user message explains what remains and why.
- The final user message states whether processed materials were moved to `Done/`, whether the active batch folder was removed, and reminds that future runs ignore `Done/` unless explicitly requested.

## Work Area And Verification

- If `素材/待整理/待复核/课程资料/` was touched, the selected item has a clear suffix: `处理中`, `测试中`, `待复核`, `已写入`, or `已归档`.
- If many `待复核` work areas exist, the final note reports the backlog and recommended next review batch.
- `scripts/verify_course_kb.py` was run when structural changes, index edits, images, or source moves occurred.
