# Media Package And PPT Handling

## Purpose

Use this reference when processing video/audio export packages, Word transcript files with keyframes, PPT/PPTX decks, or course packages that combine transcript, slides, guide notes, and human notes.

## Media Export Package Gate

Do not create a separate video/audio skill by default. Treat video/audio training materials as document packages after they are exported by tools such as 通义听悟 or other transcription systems.

For video/audio sources, prefer the lowest-cost document-first workflow:

1. Primary input: the timestamped original transcript `.docx` (`原文`) when it contains full transcript text and embedded keyframe images.
2. Optional input: a keyframe `.pptx` only when it contains speaker notes, cleaner slide images, missing visuals, or additional context not present in the Word transcript.
3. Optional input: a guided-reading or summary `.docx` (`导读`) for quick orientation, but never use it as the only source for official sedimentation.
4. Optional input: the user's own learning notes when they contain human corrections, examples, opinions, or decisions; if they are auto-generated summaries, treat them as auxiliary only.
5. Raw video/audio files are not required when the exported transcript package is complete. Use raw media only when the transcript is missing, obviously incomplete, or the user asks for direct media review.

For every media export package, first write an input-choice note that answers:

- Which file is the primary source?
- Are embedded keyframes present and complete enough?
- Is a PPT/PPTX needed for speaker notes or better images?
- Are user notes human-written or auto-generated?
- What terminology needs correction before course writing?

The default outputs for media export packages are:

```text
00_输入文件判断/来源名_输入文件判断_v1_待复核.md
01_资料清单/来源名_资料清单_v1_待复核.md
02_转写稿/来源名_原文转写稿_v1_待校准.md
02_转写稿/来源名_术语校准记录_v1_待复核.md
03_课程笔记草稿/来源名_课程笔记草稿_v1_待审核.md
04_关键帧候选/来源名_Word关键帧提取_v1_待筛选.md
04_关键帧候选/来源名_关键帧筛选建议_v1_待复核.md
05_审核记录/来源名_审核记录草稿_v1_待复核.md
06_待写入知识库内容/来源名_待写入内容_v1_待确认.md
```

Correct obvious transcription errors by context and domain vocabulary, but keep a terminology calibration record. For Amazon operations, common examples include tool names, ad abbreviations, SKU/ASIN terms, parent/child variation terms, and brand/ad product names.

## Word Transcript Keyframe Gate

For video/audio tools that export `.docx` transcripts with embedded keyframe images, the Word file can be treated as the primary source when it contains full timestamped transcript text and inline keyframes.

For every timestamped `.docx` transcript export:

1. Extract the full transcript text with timestamps as the main source.
2. Extract embedded inline images as keyframe candidates, preserving their appearance order.
3. Link each extracted image to the nearest preceding timestamp or surrounding paragraph when possible.
4. Record image count and whether images appear complete compared with the source package.
5. If the `.docx` already includes complete keyframes, the separate keyframe PPT is optional unless it contains speaker notes, cleaner slide images, or additional context.
6. If a separate PPT/PPTX is provided, compare it with Word images and avoid duplicating the same visual evidence.
7. If the PPT/PPTX has speaker notes, process those notes under the PowerPoint Speaker Notes Gate.

## PowerPoint Speaker Notes Gate

Speaker notes in PowerPoint presenter view are a first-class source, not optional metadata. They often contain the instructor talk track, examples, cautions, transitions, and context that are missing from the visible slide.

For every `.ppt` or `.pptx` source:

1. Extract visible slide content and speaker notes separately, with slide number traceability.
2. If speaker notes exist, include them in the source extraction report and audit them like main content.
3. If no speaker notes are found, record `未发现演讲者备注`.
4. If notes cannot be extracted, record `备注待人工确认`; do not assume the deck has no notes.
5. If speaker notes explain a slide image, case, table, or framework, carry that explanation into the candidate case/image notes.
6. If speaker notes contain internal-only, outdated, unsupported, privacy-sensitive, or high-risk information, keep it out of the main knowledge files and record it in the audit log.
7. If speaker notes conflict with visible slide text, preserve both in the extraction report and resolve the conflict during the audit gate.

Speaker notes can become approved knowledge, reusable talk tracks, checklists, or audit records only after the same review standard as visible slide content.
