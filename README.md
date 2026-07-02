# Local Materials To Course KB

先搭一套能长期接力的个人知识库，再安装 Skill 处理资料。顺序很重要：没有稳定入口、状态和索引，自动化只会更快地制造混乱。

## 首页主路径：先建库，再用 Skill

1. **安装 Obsidian**：它负责打开本地 Markdown、浏览链接、搜索和人工阅读。
2. **安装 Codex**：它负责采访、整理、更新与验证文件。
3. **选择 Vault**：选一个长期稳定的本地目录；开始前先确认存放路径与现阶段核心目标。
4. **让 AI 采访**：先把已有对话整理成个人信息摘要，再让 AI 一次只问一个问题；每次回答后立即更新相关页面。
5. **建立三层结构**：素材层保留原文，笔记层沉淀结论，规则层规定 AI 怎样接手。
6. **建立入口页**：至少包含 `生活.md`、`工作.md`、`学习.md`、`index.md`、`log.md`、`AGENTS.md` 和一个核心目标页。
7. **持续更新**：冲突显式保留，未知不编造；同步更新交叉链接、索引与日志。
8. **用 Obsidian 打开**这个目录作为 Vault，人工检查导航和链接。
9. **运行验证**，确认目录、主题入口和队列可用。
10. **安装 Skill**，再使用资料沉淀、知识库体检和创作复盘。
11. **可选配置三项自动化**；创建后默认 `PAUSED`，检查无误再启用。

完整采访提示与建库步骤见[从零搭建个人知识库](docs/build-your-personal-kb.md)，安装见[安装与初始化](docs/install.md)。

## 这套结构为什么不会越用越爆上下文

Obsidian 是本地知识的阅读与链接界面，不是把全库一次塞给 AI 的容器。真正控制上下文的是四道闸门：

- **索引定位**：先读 `index.md` 和分类索引，再打开当前任务相关页面；
- **主题拆页**：`01_知识主文档.md` 只做导航，正文进入 `01_知识主题/`；
- **状态文件**：`当前批次状态.md` 记录阶段、已完成项和下一步，换对话也能续跑；
- **单批次**：每次只处理一个合理批次，`Done` 只读，剩余 TBD 留给下一轮。

知识库增长时增加的是可定位的小页面，而不是每轮都要读取的总文档；因此单次上下文由任务范围决定，不会随着知识库增长线性膨胀。

## Skill 的三项一等能力

### 1. 资料沉淀队列

状态优先、先盘点再深读、一次一个批次。TBD 太多时主动拆批，并建议在低使用时段续跑；不得一轮清空。

### 2. 定期体检本地知识库

默认只读。检查断链、重复、孤岛、未整理、待确认、过期和索引覆盖，输出健康分、问题、前三优先事项和下一步。

### 3. 定期创作复盘

只读取指定创作资料目录，对照 AI 初稿、修改意见和最终稿；区分稳定规律、待观察、待确认，并把写入限制在 `reviews/wiki/index/log`。

## 快速安装与验证

把 `skills/local-materials-to-course-kb` 复制到 Codex Skills 目录，重启 Codex，然后运行：

```bash
python3 skills/local-materials-to-course-kb/scripts/init_personal_kb.py \
  --vault-root "/你的/个人知识库路径"
python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py \
  --vault-root "/你的/个人知识库路径"
```

把资料放入 `<vault>/素材/待整理/TBD`，再告诉 Codex：

```text
使用 $local-materials-to-course-kb 盘点 TBD，并只处理一个合理批次。
```

## 文档

- [从零搭建个人知识库](docs/build-your-personal-kb.md)
- [安装与初始化](docs/install.md)
- [三套 Codex 自动化](docs/automation.md)
- [队列维护与复核收口](docs/maintenance.md)
- [视频资料转课程知识库](docs/video-to-course-kb.md)
- [测试与回归](docs/testing.md)
- [优化历史](docs/history.md)

## 来源说明

建库与定期维护的思路参考了[飞书原文](https://my.feishu.cn/docx/FoLbdZXZzoX7TmxIiRycM5UhnJJ)以及 Andrej Karpathy 关于本地 raw/wiki 工作流的[公开 gist](https://gist.github.com/karpathy)。本文和项目提示词均为面向本项目的原创整理，没有复制长段原文。

## 许可证

MIT License。
