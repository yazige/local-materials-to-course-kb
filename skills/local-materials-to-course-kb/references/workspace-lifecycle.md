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

## Dialogue Review Rule

Use this rule when the user wants AI to summarize course drafts and submit only uncertain business conclusions for confirmation.

### Resume gate

1. Resume the current dialogue review before selecting another item.
2. If the state or handoff already contains unresolved A/B, show those two questions unchanged and wait. Do not modify official knowledge first.
3. If no dialogue review is active, inventory by status, select 1–3 related candidates, then enter dialogue with only one selected item.
4. Do not process `TBD`, run a health check, or start a creation review in the same run.

### A/B state machine

- AI 先总结材料，只把需要用户业务判断的结论提交确认。
- 同时保留 A、B 两个待确认问题。
- Each question states: 所属模块、适用场景、本题判断对象、不包含的范围、AI 建议.
- 用户回答 A 时，只处理 A，原样保留 B，完成后补一个新 A；用户回答 B 时反向执行。
- If the user says the previous result is wrong, 暂停新问题, repair and verify the previous item first.
- Silence, automation wakeup, or an enabled schedule is not user confirmation.

### Confirmed-item sync contract

After one answer is explicitly confirmed, update only affected files:

1. official topic pages, necessary templates, and audit records;
2. the selected item's `资料摘要`, `可沉淀知识`, and `复核清单`;
3. affected category/root/scene indexes;
4. current batch status and the dialogue `接力摘要`;
5. root `index.md` and `log.md`.

Keep the untouched A or B visible in state and handoff. Do not mark the whole review item complete merely because one conclusion was confirmed.

### Scenario gate

Before official writes, decide:

- 知识主题型：只选择一个主分类；
- 问题场景型：不强行归入单一分类，保留完整场景，可复用知识进入对应模块，并用双向链接连接。

Do not use a cross-module scenario as permission to copy the same prose into several categories.

## Completion Rule

- no active source batch is left without a status update;
- source files remain in TBD, the active batch, or Done;
- touched review items have a clear status and next action;
- official writes are discoverable through indexes and audit records.
