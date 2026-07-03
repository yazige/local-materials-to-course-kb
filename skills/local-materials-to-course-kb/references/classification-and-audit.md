# Classification And Audit Rules

## Category Decision Table

| Folder | Use for |
|---|---|
| A-岗前通用&基础认知 | Company basics, role onboarding, common work habits, platform overview, customer awareness, shared vocabulary. |
| B-Amazon运营&Listing优化 | Listing title, bullet points, A+, images, keywords, reviews, conversion, listing diagnosis, store operations. |
| C-广告推广&站外增长 | Amazon Ads, CPC, campaign structure, promotion rhythm, external traffic, influencer, deals, sales growth. |
| D-选品调研&产品开发 | Market research, category analysis, product opportunity, competitor product design, feature iteration, packaging. |
| E-项目管理&跨部门协作 | Project plans, milestones, meetings, communication, cross-team collaboration, execution tracking, reviews. |
| F-制度流程&SOP宣讲 | Company rules, SOPs, handover process, approval flow, standard operating procedures, internal training. |
| G-管理领导力&导师培养 | Coaching, mentoring, management, leadership, team growth, feedback, performance, trainer development. |
| H-个人成长&读书技能分享 | Reading notes, learning methods, thinking models, productivity, personal skills, general sharing topics. |

If one material fits several categories, choose the category that matches the main teaching use. Add secondary references only in indexes.

## Document Update Targets

| Content type | Write to |
|---|---|
| Stable concepts, frameworks, definitions, methods, including audited PPT speaker-note explanations | `01_知识主题/<主题>.md`; update navigation in `01_知识主文档.md` |
| Real cases, screenshots, comparisons, examples, plus speaker-note context that explains them | `02_案例库.md` and `images/` |
| SOPs, checklists, scripts, prompt templates, reusable wording, and audited speaker talk tracks | `03_可复用话术&模板.md` |
| Navigation, source list, course references | `00_索引.md` and root `00_总索引.md` |
| Outdated, wrong, unsupported, risky, or uncertain content | root `99_审核与不沉淀记录.md` |

## Index Update Rules

After every material is processed:

1. Add one row to the category `已沉淀资料索引` table.
2. Add course references only to the category `相关课程引用` table. Do not put source-index rows there.
3. Update root `八大分类总览` with cumulative count, main courses, and latest update for the touched category.
4. Add one row to root `最近处理记录`.
5. If images or cases were added, fill the table at the top of `02_案例库.md`.

## Audit Questions

Check every important knowledge point:

1. Is there a date, platform version, policy version, or market condition attached?
2. Could this have changed recently?
3. Is the source credible enough for training?
4. Is the claim supported by data, examples, or official rules?
5. Does it contradict current Amazon platform norms, account safety, legal compliance, or company values?
6. Could a new employee misuse it if written as an instruction?
7. Should it be converted into a safe defense/risk-management note instead of a how-to?
8. For PPT/PPTX sources, were speaker notes extracted, confirmed absent, or clearly marked as `备注待人工确认`?
9. Do speaker notes contain internal-only context, privacy-sensitive details, unsupported claims, or outdated talk tracks that should stay out of the main knowledge files?

## Audit Labels

Use these labels in records:

| Label | Meaning |
|---|---|
| `已沉淀` | Safe enough to add to the main knowledge files. |
| `待核验` | Plausible but needs current source checking. |
| `可能过时` | Date-sensitive and likely stale. |
| `明确错误` | Contradicted by logic, calculation, source, or known rules. |
| `证据不足` | Interesting but not reliable enough for training. |
| `高风险` | Could harm account, compliance, legal, brand, or team safety. |
| `仅保留防御` | Keep only risk recognition, prevention, and compliant alternatives. |

## Audit Record Template

Append entries to `99_审核与不沉淀记录.md`:

```markdown
### YYYY-MM-DD 来源资料名

| 内容摘要 | 判断 | 不沉淀原因 | 可保留的安全知识 | 建议动作 |
|---|---|---|---|---|
|  | 待核验/可能过时/明确错误/高风险/仅保留防御 |  |  |  |
```

## Approved Knowledge Entry Template

Append accepted knowledge with traceability:

```markdown
## 主题标题

- 来源：文件名 / 页码或章节 / 处理日期
- 适用场景：
- 核心结论：
- 可用于课程：
- 注意事项：

### 关键内容

### 可讲案例

### 相关图片
```

## Image Case Template

Use this in `02_案例库.md`:

```markdown
## 案例标题

- 来源：
- 图片文件：
- 适用课程/场景：
- 可以讲什么：
- 风险或注意事项：

![案例图](images/文件名.png)
```

## PPT Speaker Notes Audit Addendum

When processing `.ppt` or `.pptx` files, speaker notes must be reviewed as a separate source layer. Do not merge them silently into slide text.

Use this extraction status in handoff reports:

| Status | Meaning | Action |
|---|---|---|
| `已提取备注` | Speaker notes were found and extracted by slide. | Audit and decide whether to write into main docs, case notes, templates, or audit records. |
| `未发现演讲者备注` | The deck appears to contain no speaker notes. | Record this in the source summary. |
| `备注待人工确认` | The tool could not read notes or the file format may hide them. | Do not treat notes as absent; ask for manual export or reprocess with a notes-capable method. |

Speaker notes are especially useful for course intent, instructor examples, transition wording, scenario setup, warnings, and facilitation tips. They are also more likely to contain internal-only context, so privacy and authorization checks are mandatory.
