# Workspace Lifecycle Rules

## Purpose

Use this reference when `素材/待整理/待复核/课程资料/` contains draft folders or generated course-package outputs.

The review area is not the source queue. New sources enter through `TBD`; completed sources and fully closed review packages move to `Done`.

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
| `已归档` | Review is finished and the package is physically in `Done` | Do not reopen unless asked. |

## Start-of-Run Rule

1. Read `00_任务状态/当前批次状态.md`.
2. Check `素材/待整理/当前批次_*_处理中/`.
3. Inventory `待复核/课程资料/` by status without opening every folder.
4. If many items are waiting and no dialogue review is active, select only the next item; do not pre-read later items.
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
7. Treat `已写入` as a short-term pre-archive status. When no more action is expected and every independent item in the package is complete, move the package to `素材/待整理/Done/<稳定批次名>_已归档`.
8. Mark `已归档` only after the move succeeds, update live path references, then run `verify_course_kb.py` and `queue_inventory.py`.
9. 当前项完成并归档后，如果仍有待复核资料，立即选择下一项作为唯一活动复核项。

Raw transcripts may be opened only for the selected active batch after it enters extraction or review. If draft and audit files are complete, do not reopen raw transcripts merely for reassurance.

Moving a fully closed review package to `Done` is archival, not deletion. Never discard review items, overwrite an existing `Done` target, or move a multi-item package while any item remains active. If a name conflicts, use a date, batch directory, or stable suffix. If the move fails, keep the package in place as `已写入`, record `归档待重试` plus the reason and next action in state, handoff, and log, and do not claim it is archived.

## Dialogue Review Rule

Use this rule when the user wants AI to summarize course drafts and submit only uncertain business conclusions for confirmation.

### Resume gate

1. Resume the current dialogue review before selecting another item.
2. If the state or handoff already contains unresolved A/B, show those two questions unchanged and wait. Do not modify official knowledge first.
3. If no dialogue review is active, inventory by status and select only the next item as the sole active review item.
4. Do not process `TBD`, run a health check, or start a creation review in the same run.

### A/B state machine

- AI 先总结材料，只把需要用户业务判断的结论提交确认。
- A、B 是待确认槽位，不是必须补满的配额；仅在存在独立核心判断时使用。
- Each question states: 所属模块、适用场景、本题判断对象、不包含的范围、AI 建议.
- 同一判断链最多两层：第 1 层确认核心结论；第 2 层只补充必要边界或例外。第 2 层确认后必须收口，实施细节按实际情况判断；不得为了维持 A/B 数量继续生成同链追问。
- 用户回答 A 时，只处理 A，原样保留仍属独立判断的 B；只有当前项仍有阻塞写入的独立核心结论时，才补一个新 A。用户回答 B 时反向执行。
- If the user says the previous result is wrong, 暂停新问题, repair and verify the previous item first.
- Silence, automation wakeup, or an enabled schedule is not user confirmation.

### Confirmed-item sync contract

After one answer is explicitly confirmed, update only affected files:

1. official topic pages, necessary templates, and audit records;
2. the selected item's `资料摘要`, `可沉淀知识`, and `复核清单`;
3. affected category/root/scene indexes;
4. current batch status and the dialogue `接力摘要`;
5. root `index.md` and `log.md`.

Keep the untouched A or B visible in state and handoff only while it remains an independent active conclusion. Do not mark the whole review item complete merely because one conclusion was confirmed; after all necessary conclusions have either been confirmed or sent to audit, mark the item `已写入` and stop generating same-chain questions. Apply the archive gate above only after every independent item in the package is complete.

### Continuous queue rule

- 当前项完成并归档后，盘点课程资料复核队列；只要仍有待复核资料，就立即选择下一项。
- 一次只保持一个活动复核项。Do not batch-read or pre-open later items.
- After the next item is selected, repeat the complete review and archive flow. 完成后循环继续，直到队列清空。
- A pending A/B pauses at that item for explicit user confirmation. User silence is not confirmation, but the user should not need to issue a separate “continue” command after answering.
- Pause only for 待确认 A/B, correction of the previous item, or a 真实阻塞 such as missing evidence, tool/permission failure, or a required context handoff. Record the blocker and do not skip ahead.

### Scenario gate

Before official writes, decide:

- 知识主题型：只选择一个主分类；
- 问题场景型：不强行归入单一分类，保留完整场景，可复用知识进入对应模块，并用双向链接连接。

Do not use a cross-module scenario as permission to copy the same prose into several categories.

## Completion Rule

- no active source batch is left without a status update;
- source files remain in TBD, the active batch, or Done;
- touched review items have a clear status and next action;
- no successfully closed review package remains in `待复核/课程资料`; a failed move remains there as `已写入` with `归档待重试`;
- if the dialogue-review queue is not empty, the next item is active or the state records a pending A/B or other real blocker;
- official writes are discoverable through indexes and audit records.
