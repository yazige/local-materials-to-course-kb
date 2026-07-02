# Local Materials To Course KB

一套给 Codex 使用的本地知识库 Skill：先搭好能长期维护的个人知识库，再把 PDF、Word、PPT、图片、英文资料和音视频转写包沉淀成主题知识、案例、SOP 与审核记录。

它解决的不是“把文件转成 Markdown”，而是三个更实际的问题：

1. 新资料怎样持续进入知识库，又不重复处理；
2. 知识越积越多时，怎样按需读取，不把上下文撑爆；
3. 怎样定期检查知识库、复盘创作，而不把所有动作混在一起。

## 你会得到什么

- 一套可直接初始化的 Obsidian / Markdown 个人知识库；
- `TBD → 当前批次 → Done` 的资料队列；
- 按主题拆页的课程知识库；
- 对过时、错误、证据不足和高风险内容的审核机制；
- 资料沉淀、知识库体检、创作复盘三套自动化模板；
- 队列盘点和结构验证脚本。

## 先理解这套结构

Obsidian 在这里主要是本地 Markdown 的阅读、链接和检索界面。真正让知识库可持续的，是目录职责、索引、状态文件、主题拆页和 Skill 里的处理规则。

```text
个人知识库/
├── README.md
├── AGENTS.md
├── index.md
├── log.md
├── 素材/待整理/
│   ├── TBD/
│   ├── Done/
│   └── 待复核/
│       ├── 课程资料/
│       └── 创作复盘/
├── 知识库/课程知识库/
│   └── <分类>/
│       ├── 01_知识主文档.md   # 只做导航
│       └── 01_知识主题/       # 正文按主题拆页
├── reviews/
└── wiki/
```

AI 每次先读入口和相关主题页，而不是把整个知识库塞进上下文。库越大，文件会变多，但单次任务读取的范围不会跟着无限增长。

## 快速开始

1. 先读[从零搭建个人知识库](docs/build-your-personal-kb.md)。
2. 把 `skills/local-materials-to-course-kb` 安装到 Codex 的 Skills 目录。
3. 重启 Codex。
4. 让 Codex 执行：

```text
使用 $local-materials-to-course-kb 在我指定的目录初始化个人知识库。
```

也可以直接运行：

```bash
python3 skills/local-materials-to-course-kb/scripts/init_personal_kb.py \
  --vault-root "/你的/个人知识库路径"
```

5. 把新资料放入：

```text
<个人知识库>/素材/待整理/TBD
```

6. 告诉 Codex：

```text
使用 $local-materials-to-course-kb 盘点 TBD，并只处理一个合理批次。
```

## 三种长期用法

### 资料沉淀

先盘点、再拆批。完成审核、去重、正式写入和验证后，源资料才会进入 `Done`。

### 知识库体检

默认只读。检查积压、断链、孤立页面、重复主题、过时信息和旧路径残留，先给问题清单，不擅自批量修复。

### 创作复盘

把 AI 初稿、人工修改意见和最终稿放进 `待复核/创作复盘`。单次复盘写入 `reviews/`，重复出现的稳定规律再进入 `wiki/`。

三套自动化模板都以 `PAUSED` 状态创建，不会安装后自行运行。详见[自动化设置](docs/automation.md)。

## 为什么不会越用越容易爆上下文

- `index.md` 和分类索引负责定位；
- `01_知识主文档.md` 只保留主题导航；
- 正文拆到 `01_知识主题/`；
- 每次最多处理一个批次；
- `Done` 不自动重读；
- `当前批次状态.md` 负责跨会话接力。

也就是说，知识库增长靠“增加可定位的小页面”，不是靠“不断加长一个总文件”。

## 文档

- [从零搭建个人知识库](docs/build-your-personal-kb.md)
- [安装与初始化](docs/install.md)
- [三套 Codex 自动化](docs/automation.md)
- [队列维护与复核收口](docs/maintenance.md)
- [视频资料转课程知识库](docs/video-to-course-kb.md)
- [测试与回归](docs/testing.md)
- [优化历史](docs/history.md)

## 许可证

MIT License。你可以按自己的行业调整分类、审核规则和输出模板。
