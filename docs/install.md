# 安装与初始化

## 需要什么

- Codex；
- Python 3；
- 一个长期使用的本地目录；
- Obsidian（推荐，但不是脚本运行的必需品）。

## 安装 Skill

把项目中的目录复制到 Codex Skills 目录：

```text
skills/local-materials-to-course-kb
```

复制后重启 Codex，让应用重新读取 Skill。

## 初始化完整个人知识库

```bash
python3 skills/local-materials-to-course-kb/scripts/init_personal_kb.py \
  --vault-root "/你的/个人知识库路径"
```

如果你已经有个人知识库，只想补齐课程区：

```bash
python3 skills/local-materials-to-course-kb/scripts/init_course_kb.py \
  --vault-root "/你的/个人知识库路径"
```

脚本只创建缺失项，不覆盖已有文件。

## 初始化后的关键目录

```text
<vault>/
├── 素材/待整理/
│   ├── TBD/
│   ├── Done/
│   └── 待复核/
│       ├── 课程资料/
│       └── 创作复盘/
└── 知识库/课程知识库/
    ├── 00_任务状态/
    ├── 00_总索引.md
    ├── 99_审核与不沉淀记录.md
    └── A-H 八个标准分类/
        ├── 01_知识主文档.md
        └── 01_知识主题/
```

## 验证

```bash
python3 skills/local-materials-to-course-kb/scripts/queue_inventory.py \
  --vault-root "/你的/个人知识库路径"

python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py \
  --vault-root "/你的/个人知识库路径"
```

旧版 `--root` 参数仍保留，但新安装建议统一使用 `--vault-root`。

## 日常使用

1. 把新资料放进 `素材/待整理/TBD`。
2. 让 Codex 使用 `$local-materials-to-course-kb` 盘点。
3. 每次只处理一个批次。
4. 完成验证后，源资料进入 `素材/待整理/Done/YYYY-MM-DD_批次名`。

`Done` 默认只读。不要把已处理资料放回 TBD，除非你明确要重新沉淀。
