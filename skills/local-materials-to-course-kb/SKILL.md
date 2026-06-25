---
name: local-materials-to-course-kb
description: Use when整理本地PDF、Word、PPT、图片型文档、英文资料，或由视频/音频转出的Word/PPT/导读/笔记文档包为中文课程知识库、案例库、SOP、培训素材或Markdown资料库，需要分类到8个工作场景，审核过时错误违规高风险知识，多文件批量沉淀，额度暂停后继续投放资料，使用media/TBD与media/Done资料队列，或被自动化唤醒继续沉淀。
---

# Local Materials To Course KB

## Core Rule

Treat the task as course-editor work, not file conversion. Convert and extract only after understanding the training purpose, then audit knowledge before adding it to the long-term library.

Course sedimentation quality comes before batch size, speed, or the number of files processed. If the material set is too broad, too dense, cross-category, image-heavy, or likely to exceed the available context/credit budget, first produce an intake assessment and split plan instead of forcing all files into one deep sedimentation pass.

## Required Workflow

1. Confirm the business purpose, target audience, and intended course or work scenario when unclear.
2. Run the Initialization Gate before any source intake, especially on a new computer, shared skill install, empty workspace, or when `media/TBD/` and `media/Done/` are missing.
3. Run the Continuation And Intake Priority Gate before accepting new deep extraction work.
4. Run the Media Queue Gate when `media/TBD/` exists, when the user asks to process queued materials, or when no explicit source files are provided.
5. Run the Automation Wakeup Gate when the task is started by an automation, recurring run, scheduled check, or "continue queued sedimentation" prompt.
6. Run the Batch Sizing Feedback Gate before conversion or subagent assignment.
7. Before conversion, if the user provides a folder path or multiple Word document paths, follow the Folder And Multi-Word Intake Gate. Otherwise convert the source document to Markdown or text. For video/audio exports, Word transcript keyframes, or PowerPoint files, read `references/media-package-and-ppt.md` before extraction. For scanned PDFs or images, use OCR and mark uncertain recognition.
8. If the source is English or mixed-language, read `references/english-source-localization.md` and convert user-facing output into Chinese course language before sedimenting.
9. Extract only useful teaching images: diagrams, examples, screenshots, page visuals, frameworks, and before/after comparisons.
10. Read `references/classification-and-audit.md`, then choose exactly one primary category.
11. Run the knowledge audit before writing anything into the main knowledge files.
12. Check the existing knowledge base for duplicate or overlapping knowledge before adding new content.
13. Add only new, updated, better-explained, or case-supported approved content to the category files and images folder.
14. Put outdated, wrong, unsupported, uncertain,违规, or high-risk content into `99_审核与不沉淀记录.md` instead of the main knowledge files.
15. Update all index tables: category `00_索引.md`, root `00_总索引.md`, and the top table in any touched `02_案例库.md`.
16. Before reporting completion, read `references/completion-checklist.md` and run `scripts/verify_course_kb.py` when structural changes, index edits, images, or source moves occurred.

## Initialization Gate

Initialize the default course knowledge-base structure before reading or moving source materials.

1. Use the default root unless the user specifies another root:

```text
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库
```

2. Run the bundled initializer script resolved relative to this `SKILL.md`:

```text
scripts/init_course_kb.py
```

3. The initializer must create the root folder, eight category folders, category Markdown files, `00_总索引.md`, `99_审核与不沉淀记录.md`, `00_任务状态/当前批次状态.md`, `00_任务状态/待处理资料队列.md`, `media/TBD/`, and `media/Done/`.
4. If the root already exists but `media/TBD/`, `media/Done/`, or `00_任务状态/` are missing, run the initializer again; it must create missing folders/files without overwriting existing knowledge files.
5. After initialization, verify that both queue folders exist before telling the user to put materials into `TBD`.
6. For large queues or review backlogs, use `scripts/queue_inventory.py` for a read-only inventory before selecting work.

## Continuation And Intake Priority Gate

Use this gate at the start of every run, especially after credit/context limits, interrupted sessions, or when the user adds new materials while a previous sedimentation task may still be unfinished.

1. Create `00_任务状态/` if it is missing, then check whether there is an unfinished batch before deep-reading new sources. Look for explicit user notes, current conversation state, `00_任务状态/当前批次状态.md`, `00_任务状态/待处理资料队列.md`, draft files marked `待审核`/`待确认`/`待复核`, and media-package outputs under `06_待写入知识库内容/`.
2. If an unfinished batch exists, do not silently skip it and do not mix its official writes with new materials.
3. Default priority: finish the previous batch's audit, deduplication, official writes, indexes, and verification first.
4. If the user has supplied new materials at the same time, first register them in `00_任务状态/待处理资料队列.md` with file path, inferred topic, likely category, and suggested batch. Then continue the unfinished batch.
5. New materials may be processed in parallel only when they are clearly independent, have a separate batch ID, and the current unfinished batch has a reliable status handoff. Official knowledge-base writes must still remain separated by batch until the main thread merges and audits them.
6. Before pausing because of credit/context limits, time limits, or uncertainty, update `00_任务状态/当前批次状态.md` so the next run can resume safely.

Use this status template:

```markdown
## YYYY-MM-DD 批次名

| 字段 | 内容 |
|---|---|
| batch_id |  |
| source_files |  |
| current_stage | 盘点/提取/知识卡片/去重/审核/待写入/索引更新/验证 |
| completed_work |  |
| pending_work |  |
| chosen_primary_category |  |
| subagent_card_locations |  |
| audit_status |  |
| index_update_status |  |
| next_action |  |
```

## Batch Sizing Feedback Gate

Before deep extraction for folders, 3+ files, course packages, mixed formats, or uncertain categories, give the user a brief intake assessment. The purpose is to protect course quality, not to maximize file count.

The assessment must include:

- material_count: number of files and whether any are bundled source packages;
- source_types: Word, PDF, PPT/PPTX, image/scanned PDF, transcript, guide, notes, spreadsheet, or mixed;
- complexity_level: low/medium/high, with reasons such as images, OCR, speaker notes, English localization, Amazon rule verification, privacy review, or cross-category content;
- information_density: low/medium/high, based on teaching points, cases, screenshots, frameworks, transcript length, and notes;
- category_spread: likely one category, several adjacent categories, or uncertain/mixed;
- recommended_mode: inventory-only, split then process, or direct deep sedimentation;
- recommended_batch_size and first batch suggestion.

Default batch-size guidance:

| Material situation | Recommended deep-processing amount |
|---|---:|
| Same topic, mostly text Word/PDF | 6-10 files |
| Uncertain category or mixed topics | 3-5 files |
| PPT/PPTX with images or speaker notes | 2-4 files |
| Video/audio export packages with transcript/keyframes/PPT/notes | 1-3 packages |
| Amazon policy, fee, ads feature, account-safety, or time-sensitive tactics | 2-4 files |
| High-value course sedimentation where quality is the priority | 4-6 files |

If the supplied set exceeds the recommended size, first create an inventory and split plan. Deep-process only the highest-priority coherent batch unless the user explicitly asks for a broad first-pass inventory.

## Media Queue Gate

Use this gate when the user maintains materials under the knowledge-base `media/` folder instead of manually sending file paths each time.

Folder roles:

| Folder | Purpose | Rule |
|---|---|---|
| `media/TBD/` | Inbox for materials waiting to be sedimented | User may keep adding files and folders here. |
| `media/当前批次_YYYY-MM-DD_主题_v1_处理中/` | Active batch selected from TBD | Codex may deep-read and process only the selected active batch. |
| `media/Done/` | Processed source materials waiting for human review | Do not deep-read, modify, move, or delete these unless the user explicitly asks. |

Workflow:

1. Create `media/`, `media/TBD/`, and `media/Done/` if missing.
2. Inventory only top-level files and folders in `media/TBD/`; ignore `media/Done/`, active batch folders, hidden files, and system files.
3. Treat a course package folder as one source package when its files belong to the same lesson or recording.
4. Use the Batch Sizing Feedback Gate to choose a coherent amount by topic, likely category, complexity, and information density.
5. Move only the selected items from `media/TBD/` into one active batch folder under `media/` before deep extraction.
6. Record the active batch folder and selected source list in `00_任务状态/当前批次状态.md`.
7. If processing pauses before completion, leave the selected materials in the active batch folder and update `pending_work`; do not move them to `Done/`.
8. After official writes, indexes, audit records, and verification are complete, move the processed source files/folders from the active batch folder to `media/Done/YYYY-MM-DD_批次名/`.
9. After the move succeeds, delete the active batch folder only if it is empty. If it still contains files, do not delete it; report what remains and why.
10. Report to the user that the processed materials were moved to `Done/`, whether the active batch folder was removed, and that future sedimentation will not touch `Done/` unless explicitly requested.
11. If a move would overwrite an existing file or folder, create a date/batch subfolder or add a stable suffix; never overwrite processed materials.

If `media/TBD/` is empty, report that there are no queued materials and do not scan `media/Done/` for new work.

## Automation Wakeup Gate

Use this gate when Codex is launched by a recurring automation, scheduled check, or continuation prompt.

Automation can wake the task, but this skill owns the processing discipline. Do not rely on conversation memory for queue state; use the files under the knowledge-base root.

1. First run the Continuation And Intake Priority Gate. If an unfinished active batch exists, resume that batch before selecting new `TBD` items.
2. If no unfinished batch exists, inspect `media/TBD/`.
3. If `media/TBD/` contains files or folders, automatically start the next sedimentation batch without asking the user to pick files, unless the intake assessment finds high-risk ambiguity that requires human confirmation.
4. Process at most one coherent batch per automation run. Do not loop through all remaining `TBD` items in one run.
5. After finishing one batch, move processed sources to `media/Done/YYYY-MM-DD_批次名/`, remove the empty active batch folder, update indexes and status files, then stop. Let the next automation run handle the next batch.
6. If `media/TBD/` is empty and no unfinished batch exists, update the status note with `queue_status: empty` and stop. Do not scan `Done/`.
7. If credit, context, model limits, file complexity, OCR/image extraction, or official verification prevents completion, update `00_任务状态/当前批次状态.md` with the exact stage, pending work, and next action, then stop for the next automation run.
8. For long unattended runs, prefer cron-style standalone automations over thread heartbeats so each run starts with a cleaner context and reads the task state from files.

Use this run discipline:

| Situation | Action |
|---|---|
| `TBD` has queued materials and no unfinished batch | Select one safe batch and process it. |
| There is an unfinished active batch | Resume it before selecting anything new. |
| One batch completed successfully | Move sources to `Done`, clean empty active folder, update status, stop. |
| `TBD` is still non-empty after one batch | Leave remaining files in `TBD` for the next automation run. |
| Context is getting long or the current thread is overloaded | Write a concise handoff in `当前批次状态.md` and stop; next automation run should continue from files. |
| Credit or rate limit interrupts the run | Preserve active batch and status; do not move to `Done`. |

## Work Area Lifecycle Gate

Use this gate when `98_音视频处理工作区/` exists, when many folders are marked `待复核`, or when a run is reviewing drafts created from video/audio export packages.

1. Read `references/workspace-lifecycle.md` before touching work-area folders.
2. Treat `98_音视频处理工作区/` as a draft/review area, not as the automatic source queue.
3. Inventory work-area folders by status suffix: `处理中`, `测试中`, `待复核`, `已写入`, `已归档`, or `未标注`.
4. If many `待复核` folders exist, report the backlog and recommend a small review batch before creating more drafts.
5. Do not delete or reopen work-area folders unless the user explicitly asks. Rename status suffixes only after the official writes, indexes, audit records, and status notes match the new state.

## Folder And Multi-Word Intake Gate

Use this gate whenever the user provides a directory path, several `.doc`/`.docx` paths, or a mixed folder where Word documents are the main source type.

1. Do not immediately open and full-read all documents.
2. First create a file inventory from file names, extensions, parent folders, obvious date/version words, and only short previews or metadata when needed.
3. The inventory must identify: file path, file name, source type, inferred topic, possible knowledge type, complexity level, information density, likely category, and processing priority.
4. Use these possible knowledge types when practical: concept, framework, case, SOP, checklist, reusable template, risk/audit item, reference material.
5. Group files by inferred topic and decide whether they are dependent, duplicate/overlapping, or independent before deep extraction.
6. If there are more than 3 Word documents and the topics are similar, subagents may be used for extraction.
7. Assign each subagent a disjoint file set. A subagent may read only its assigned files plus required shared skill/reference instructions; it must not open, summarize, or compare files assigned to another subagent.
8. Subagents must output the Unified Knowledge Card Format below. Do not accept long-form source retellings, full transcripts, or chapter-by-chapter rewrites as the handoff format.
9. The main thread reads the subagent knowledge cards, not the full source text handled by subagents, then deduplicates, classifies, merges, audits, and writes the final Skill/reference or knowledge-base content.

## Unified Knowledge Card Format

Each subagent handoff must be a compact list of cards. One source may produce multiple cards, but each card should represent one reusable teaching point, case, template, or audit issue.

```markdown
### 知识卡片

- source_file:
- source_type:
- inferred_topic:
- possible_knowledge_type:
- suggested_primary_category:
- core_point:
- course_ready_summary:
- usage_scenario:
- approved_candidate:
- case_or_image_candidate:
- reusable_template_candidate:
- audit_risk:
- duplicate_or_conflict:
- uncertain_item:
- source_trace:
```

Rules for cards:

- Keep `course_ready_summary` short and rewritten for Chinese training use; do not paste long original paragraphs.
- Use `source_trace` for page, paragraph, slide number, timestamp, heading, or image order when available.
- Put unsupported, outdated, privacy-sensitive, high-risk, or unclear points into `audit_risk` or `uncertain_item`, not `approved_candidate`.
- For Word transcript exports with keyframes, include image count or nearest timestamp in `case_or_image_candidate` when useful.
- For PPT/PPTX files in a mixed batch, include speaker-notes extraction status in `source_trace` or `uncertain_item`.

## Multi-File Batch Workflow

Use batch mode when the user provides 3+ files, a course package, or several sources for the same topic. Batch mode speeds up extraction, but it does not change the audit rules or the quality-first batch-size limits.

For folders or multiple Word documents, complete the Folder And Multi-Word Intake Gate before using batch mode.

Parallel subagents, when used, are extraction-only:

- Do not let subagents modify original files.
- Do not let subagents write to the official knowledge-base Markdown files.
- Each subagent must handle only its assigned files and must not duplicate another subagent's source-reading work.
- Each subagent must produce structured knowledge cards with: file summary, suggested primary category, approved knowledge candidates, image candidates, reusable template candidates, audit risks, duplicates/conflicts, uncertain items, and for PPT/PPTX files the speaker-notes extraction status.
- The main thread must read the structured handoff cards itself before deciding what enters the official knowledge base.
- Do not use subagents as a reason to deep-process an oversized, cross-category, or unclear batch. Subagents can expand extraction capacity, but the main thread still owns classification, deduplication, audit, course rewriting, official writes, and verification.

The main thread owns all official writes:

1. Choose exactly one primary category for each source.
2. Merge duplicate points across files and against existing knowledge-base entries into one course-ready explanation.
3. Prefer stable principles and frameworks over dated screenshots, amounts, dates, approval nodes, or organization-specific settings.
4. Copy only approved teaching images into the category `images/` folder.
5. Write rejected, outdated, unsupported, privacy-sensitive, or high-risk items into `99_审核与不沉淀记录.md`.
6. Update root and category indexes only after the final merge is clear.
7. Verify case counts, image links, table formatting, source counts, and audit records before reporting completion.
8. Close any subagents after their reports have been merged.

Do not use batch mode for tightly dependent files that must be read in sequence, a single short file, or cases where every page requires main-thread judgment.

## Output Location

Default root:

```text
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库
```

If that parent path does not exist, create it. Do not modify, delete, or overwrite original source files.

Task-state files:

```text
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库/00_任务状态/当前批次状态.md
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库/00_任务状态/待处理资料队列.md
```

The initializer script creates these files if missing. Create `00_任务状态/` before writing or resuming batch status.

Media queue folders:

```text
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库/media/TBD
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库/media/Done
```

The initializer script creates these folders if missing, including on a new computer or a shared skill install. `TBD` is the only automatic source queue. `Done` is a processed-material holding area for the user's manual review and cleanup.

## Category Structure

Use these eight primary folders only:

```text
A-岗前通用&基础认知
B-Amazon运营&Listing优化
C-广告推广&站外增长
D-选品调研&产品开发
E-项目管理&跨部门协作
F-制度流程&SOP宣讲
G-管理领导力&导师培养
H-个人成长&读书技能分享
```

Each category uses:

```text
00_索引.md
01_知识主文档.md
02_案例库.md
03_可复用话术&模板.md
images/
```

One source material must have only one primary category. Other course uses should be cross-references in indexes, not duplicated正文.

## Media Package And PPT Handling

For video/audio export packages, Word transcript keyframes, and PPT/PPTX speaker notes, read `references/media-package-and-ppt.md`.

Key rule: prefer document exports before raw video/audio, keep transcript, keyframes, slide text, and speaker notes traceable, and mark notes extraction failures as `备注待人工确认`.

## Language Localization Gate

For English or mixed-language materials, the long-term knowledge base must be Chinese-first:

- Do not dump full English paragraphs into the main Markdown files.
- Translate and rewrite into clear Chinese training language, preserving the original meaning, structure, and useful concepts.
- Keep original-language screenshots only as source evidence or case images; add Chinese titles, explanations, and teaching notes around them.
- Rebuild important English frameworks, tables, checklists, and talk tracks as Chinese course-ready artifacts.
- Put stale resource lists, contact details, prices, dated claims, unsupported advice, and translation uncertainties into the audit record.

## Official Verification Gate

Before writing current Amazon platform rules, ads features, fee logic, policy requirements, account-safety guidance, AI tool availability, backend entrances, or time-sensitive marketplace tactics into the official knowledge base, verify current official sources when internet access is available.

Use official sources first, such as Amazon Ads, Amazon Seller Central/Sell on Amazon, or official Amazon policy/help pages. If official verification is unavailable, mark the item as `待核验` and keep it out of the main knowledge files.

Do not sediment as stable knowledge:

- fixed backend paths or menu names that may change;
- exact fees, minimum bids, thresholds, eligibility rules, or promotion dates without current official proof;
- discontinued features as current operations;
- third-party tool recommendations as long-term defaults;
- screenshots containing account, customer, order, advertising, or private business data unless properly desensitized.

## Existing Knowledge Dedup Gate

Before writing to the official knowledge base, compare the approved candidates with the existing category files, root index, category index, case library, templates, and audit record.

Do not duplicate knowledge that is already present. Use this decision table:

| Situation | Action |
|---|---|
| Same concept already exists with similar explanation | Do not add a new duplicate section; keep the existing section. |
| Same concept exists but the new source explains it more clearly | Merge or refine the existing explanation, preserving source traceability. |
| Same framework exists but the new source adds a useful example, image, checklist, or talk track | Add only the new case/template/reference, and cross-reference the existing knowledge section. |
| New source conflicts with existing knowledge | Do not silently overwrite; record the conflict, verify current sources if needed, and write uncertain or outdated points to `99_审核与不沉淀记录.md`. |
| New source updates a time-sensitive Amazon rule, feature, fee, policy, or tool | Verify official sources first; update the stable knowledge only if confirmed, and move obsolete wording to the audit record. |
| New source is less complete than existing knowledge | Do not sediment it; record it as a duplicate source only if useful for traceability. |

When a source is mostly duplicate, the processing note should clearly say:

- 已有知识库位置；
- 本次新增了什么；
- 哪些内容因重复未写入；
- 是否只补充案例图、话术模板、审核记录或索引引用。

## Knowledge Audit Gate

Classify each extracted point before sedimenting it:

| Result | Action |
|---|---|
| Approved | Add to the relevant category MD. |
| Possibly outdated | Do not add to main MD; record in audit file with reason. |
| Clearly wrong | Do not add; record the error and correction if known. |
| Unsupported claim | Do not add as fact; mark as needs verification. |
| High-risk or违规黑科技 | Do not provide operational steps; keep only risk recognition, defense, self-check, and compliant alternatives. |
| Unclear | Put in audit record or ask the user. |

For Amazon platform rules, fees, ad policy, review policy, account safety, or current marketplace tactics, treat dates and sources as important. If current verification is not available, mark the item as `待核验` instead of presenting it as confirmed.

## Safe Handling of 黑科技

Preserve defensive understanding, not execution instructions.

Keep:

- What the risky practice is at a high level
- Why teams may be tempted to use it
- Platform, account, legal, brand, and team-management risks
- Warning signs and self-check questions
- Defensive controls, prevention, and compliant alternatives

Remove:

- Specific tools, vendors, channels, accounts, or contact paths
- Step-by-step execution instructions
- Detection bypass methods
- Copyable scripts, prompts, or operational templates
- Any wording that encourages adoption

## File Naming

Use stable, reviewable names:

```text
YYYYMMDD_来源短名_用途_序号.png
YYYY-MM-DD_来源资料名_处理记录.md
```

Prefer Chinese filenames for user-facing files. Keep source filenames unchanged.

## Completion Checklist

Before reporting completion, read `references/completion-checklist.md`.

Minimum completion evidence:

- Original source files were not overwritten.
- Current batch state is explicit in `00_任务状态/当前批次状态.md`.
- Approved and rejected content are separated.
- Root/category indexes, case tables, audit records, and image links are updated when touched.
- Processed source materials are either still safely queued, in an active batch, or moved to `media/Done/YYYY-MM-DD_批次名/`.
- Any touched `98_音视频处理工作区/` folder has a clear status suffix and next action.
- `scripts/verify_course_kb.py` has been run when structure, indexes, images, or source moves changed.
