# Classification And Audit Rules

## Material Type Gate

Before choosing a category, decide whether the material is:

- **知识主题型**：围绕一个稳定知识主题展开。只选择一个主分类，其他用途只做索引交叉引用。
- **问题场景型**：围绕一个具体问题、目标、约束和决策过程展开，且需要多个知识模块共同解决。不强行归入单一分类。

For a problem scenario:

1. 保留完整场景，包括问题、目标、约束、决策顺序和复盘方式；
2. 把可复用知识维护到对应模块的 `01_知识主题/`；
3. 场景页与模块知识建立双向链接；
4. 不在多个分类复制同一份知识正文；
5. 在状态中记录 `资料类型：问题场景型`、场景入口和涉及模块，不填写虚假的单一主分类；
6. 项目已有场景目录时沿用真实路径；没有时先向用户确认入口，不擅自重构信息架构；
7. 同步场景索引和实际承接知识的模块索引；总索引只更新导航和摘要，不复制多份来源正文；
8. 某个知识点没有权威归属时标记待确认并暂停该项，不要为了收口强行选择分类。

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

If a **knowledge-topic material** fits several categories, choose the category that matches the main teaching use. Add secondary references only in indexes. This one-primary-category rule does not apply to problem-scenario materials handled by the Material Type Gate.

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

1. Keep root `00_总索引.md` navigation-only: category links, cumulative count, latest update and one-sentence summaries. Never add knowledge正文 there.
2. Deduplicate in this fixed order: root index → category index → filename/title/keyword search → candidate topic pages. Never open a whole category by default.
3. For a knowledge-topic material, add one row to the primary category `已沉淀资料索引` table.
4. For a problem scenario, update the scene index once and update only the module indexes that actually receive reusable knowledge.
5. Add course references only to category `相关课程引用` tables. Do not duplicate the same source-index row across modules.
6. Update root `八大分类总览` with cumulative count, main courses, and latest update for touched categories.
7. Add one row to root `最近处理记录`.
8. If images or cases were added, fill the table at the top of `02_案例库.md`.

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
