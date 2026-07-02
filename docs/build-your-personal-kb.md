# 从零搭建自己的 Karpathy 式本地知识库

这是一套“本地 Markdown + AI 接力”的实现。方法参考[飞书原文](https://my.feishu.cn/docx/FoLbdZXZzoX7TmxIiRycM5UhnJJ)与 Andrej Karpathy 的[公开 gist](https://gist.github.com/karpathy)，下文是针对本项目重新设计的中文操作指南。

## 1. 安装并选定 Vault

安装 Obsidian 和 Codex。Obsidian 负责本地阅读、搜索、链接与人工校对；Codex 负责采访、整理、更新和验证。

选择一个长期稳定的目录作为 Vault。让 AI 开始建文件前，必须先确认两件事：

1. 知识库存放路径；
2. 你现阶段最想解决的问题或核心目标。

## 2. 先准备可追溯的采访材料

可以让常用 AI 根据历史对话整理一份个人信息摘要，再交给 Codex。摘要只是素材，不自动等于事实；不确定、冲突或过期内容要显式标记。

之后让 Codex 一次只问一个问题。每次回答后立即：

- 更新最相关的个人页、目标页或项目页；
- 补充交叉链接；
- 更新 `index.md`；
- 向 `log.md` 追加记录；
- 保留“已确认 / 历史记录 / 推断待确认 / 冲突待确认”的状态。

## 3. 建立三层结构和稳定入口

- **素材层**：保存原文、对话摘要、会议纪要和课程资料，只读不覆盖。
- **笔记层**：保存确认后的个人信息、目标、项目与主题知识。
- **规则层**：用 `README.md`、`AGENTS.md` 和 Skill 约束不同 AI 的接手方式。

最小入口包括：

```text
生活.md
工作.md
学习.md
目标_核心目标.md
README.md
AGENTS.md
index.md
log.md
```

## 4. 初始化并用 Obsidian 打开

```bash
python3 skills/local-materials-to-course-kb/scripts/init_personal_kb.py \
  --vault-root "/你的/个人知识库路径"
```

脚本只补缺失项，不覆盖现有知识。运行后，用 Obsidian 打开该目录作为 Vault，检查入口页、链接和目录是否符合自己的习惯。

## 5. 验证骨架

```bash
python3 skills/local-materials-to-course-kb/scripts/queue_inventory.py \
  --vault-root "/你的/个人知识库路径"
python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py \
  --vault-root "/你的/个人知识库路径"
```

验证通过后再安装并使用 Skill，把新资料放进 `素材/待整理/TBD`。

## 6. 为什么不会随着知识库增长把上下文撑爆

- **索引定位**：先从 `index.md`、分类索引和主题导航找到目标，不扫全库。
- **主题拆页**：入口页只放导航，正文拆成一个主题一页。
- **状态文件**：当前批次状态记录阶段和下一步，换模型、换窗口也能恢复。
- **单批次**：每轮只深读一批，`Done` 只读，剩余 TBD 留待后续。

这四层边界把“库有多大”和“本轮读多少”拆开。页面数量可以持续增加，但每次任务只取与当前目标有关的有限集合，所以不会随着知识库增长线性增加上下文。

## 7. 安装 Skill，再考虑自动化

把本项目的 Skill 复制到 Codex Skills 目录并重启 Codex。先手动跑通一个小批次，再按需配置：

1. 资料沉淀队列；
2. 本地知识库每周体检；
3. 每周创作复盘。

三项自动化默认 `PAUSED`。资料沉淀应安排在低使用时段且每次一个批次；体检默认只读；创作复盘只能读取指定创作资料区。

## 8. 长期维护的判断标准

- 原始资料可追溯；
- 入口能定位所有重要页面；
- 主题页不过度膨胀或重复；
- 当前状态能让另一个 AI 直接接手；
- 未确认和过期信息没有混成当前事实。
