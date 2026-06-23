# English Source Localization Rules

## Purpose

Use these rules when an English or mixed-language source is being turned into the Chinese course knowledge base. This is not a bilingual translation task. The goal is to preserve useful knowledge, then rewrite it into Chinese training material that can be reused in courses, SOPs, checklists, and case libraries.

## Output Principle

Write Chinese-first outputs:

| Output | Rule |
|---|---|
| `01_知识主文档.md` | Chinese explanations, Chinese headings, Chinese frameworks. Do not paste long English paragraphs. |
| `02_案例库.md` | Original English screenshots are allowed as evidence, but case title, teaching value, risk notes, and image alt text must be Chinese. |
| `03_可复用话术&模板.md` | Rebuild as Chinese SOPs, checklists, tables, talk tracks, or prompts. |
| `00_索引.md` and `00_总索引.md` | Chinese summaries and Chinese course names. |
| `99_审核与不沉淀记录.md` | Chinese audit notes; mention if a rejected item is stale, promotional, unsupported, or only useful as source traceability. |

## Translation Quality Standard

Use the practical version of 信、达、雅:

- 信: preserve meaning, hierarchy, claims, dates, conditions, and caveats.
- 达: use natural Chinese training language; split long English sentences and reduce stiff literal wording.
- 雅: keep it professional and readable, but do not over-polish into literary prose.

Prefer course-ready rewriting over sentence-by-sentence translation. Extract models, checklists, examples, risks, and reusable wording.

## What To Preserve

Keep and localize:

- Definitions, frameworks, models, and step-by-step methods that remain useful.
- Self-assessment tables, checklists, process templates, rubrics, and prompts.
- Good examples that can become teaching cases.
- Important source title, author, date, page, or version information for traceability.
- Original English terms when they are necessary for search or professional recognition.

## What To Audit Instead Of Sedimenting

Record these in `99_审核与不沉淀记录.md`:

- Old prices, phone numbers, email addresses, purchase channels, publisher promotion, and resource lists.
- Claims tied to old platform rules, laws, market conditions, or organizational context.
- Unsupported data, fixed ratios, broad generalizations, or advice without context.
- Translation uncertainty caused by bad OCR, broken typography, missing pages, or unclear diagrams.
- Any risky tactic that should only be kept as risk recognition or defensive guidance.

## Terminology Rules

- First important technical or professional term can use `中文（English）`; later use Chinese.
- Keep standard product/platform names in English when that is how users recognize them: Amazon, Listing, Q&A, SOP, API, SKU, ASIN, Markdown.
- Use consistent Chinese terms inside the same document.
- Avoid awkward literal translation. Choose the term that fits the user's training scenario.

Example for mentor materials:

| English | Preferred Chinese |
|---|---|
| mentor | 导师 |
| mentee | 学员 |
| mentoring | 导师制 / 带教 |
| active listening | 主动倾听 |
| building trust | 建立信任 |
| encouraging | 鼓励与正向反馈 |
| corrective feedback | 纠偏反馈 |
| managing risks | 风险管理 |
| opening doors | 打开机会之门 / 资源引荐 |
| following through | 兑现承诺 / 跟进落地 |

## Chinese Style Rules

- Use Chinese punctuation in Chinese prose: ，。；：？！、（）.
- Add spaces between Chinese and English or numbers: `AI 工具`, `3 个阶段`, `Amazon Listing`.
- Use full-width Chinese brackets for explanations: `大语言模型（LLM）`.
- Avoid English straight quotes in Chinese prose. Prefer Chinese quotes such as 「」 when quoting terms.
- Avoid repeated punctuation, excessive bolding, and progress notes inside the final knowledge docs.
- Remove filler words that do not help training: “其实”、 “那么”、 “好的”、 “您可以”.
- Keep paragraphs short enough for training use; split long English arguments into digestible Chinese bullets or tables.

## Markdown Rules

- Use normal Markdown headings, lists, and tables.
- Do not use bilingual `<mark>` highlighting for this knowledge base unless the user explicitly asks for bilingual output.
- Use code formatting only for literal commands, file names, variables, API names, or prompt placeholders.
- When a screenshot remains English, add a Chinese caption and explain how to teach it.

## Case Image Rules

English screenshots can be useful, but they must not be the only teaching artifact.

For each English screenshot kept:

1. Give it a Chinese filename when copied into `images/`.
2. Add a Chinese case title.
3. Explain what the image teaches.
4. State whether it is source evidence, a model diagram, a worksheet, or a UI example.
5. If the image is a framework or worksheet, recreate the usable version in Chinese Markdown whenever practical.

## Quick QA Before Completion

Check before reporting completion:

- Main knowledge docs contain no long untranslated English paragraphs.
- Key frameworks and tables have Chinese versions.
- English screenshots, if retained, have Chinese captions and teaching notes.
- Dated, promotional, or unsupported English-source details are in the audit record.
- Terminology is consistent within the touched category.
- Chinese/English spacing and Chinese punctuation look clean.
