# 安装与初始化

## 适用环境

这个项目主要面向 Codex 的本地 skill 工作流。你需要：

- 一台能运行 Codex 的电脑；
- Python 3，用来运行初始化脚本；
- 一个用于存放知识库的本地目录。

默认目录是：

```text
~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库
```

如果你不想用这个目录，可以在运行初始化脚本时指定自己的路径。

## 安装 skill

把项目里的这个文件夹复制到你的 Codex skill 目录：

```text
skills/local-materials-to-course-kb
```

复制后，重启 Codex。重启是为了让 Codex 重新读取 skill。

## 初始化知识库

在 Codex 里说：

```text
使用 local-materials-to-course-kb 初始化课程知识库。
```

或者直接运行初始化脚本：

```bash
python3 skills/local-materials-to-course-kb/scripts/init_course_kb.py
```

脚本会自动创建：

```text
本地资料转课程知识库/
├── 00_总索引.md
├── 00_任务状态/
│   ├── 当前批次状态.md
│   └── 待处理资料队列.md
├── 99_审核与不沉淀记录.md
├── media/
│   ├── TBD/
│   └── Done/
├── A-岗前通用&基础认知/
├── B-Amazon运营&Listing优化/
├── C-广告推广&站外增长/
├── D-选品调研&产品开发/
├── E-项目管理&跨部门协作/
├── F-制度流程&SOP宣讲/
├── G-管理领导力&导师培养/
└── H-个人成长&读书技能分享/
```

如果这些文件或文件夹已经存在，脚本不会覆盖已有内容，只会补缺失项。

## 维护脚本

初始化脚本只负责搭好架子。日常跑久了以后，可以用另外两个脚本做检查。

盘点待处理资料和待复核工作区：

```bash
python3 skills/local-materials-to-course-kb/scripts/queue_inventory.py
```

检查知识库结构、图片链接和常见问题：

```bash
python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py
```

如果你不是在项目根目录运行脚本，可以指定知识库路径：

```bash
python3 skills/local-materials-to-course-kb/scripts/queue_inventory.py --root "~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库"
python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py --root "~/Desktop/AI工作台/06_培训教程与分享资料/本地资料转课程知识库"
```

## 日常怎么用

把待处理资料放进：

```text
media/TBD
```

然后告诉 Codex：

```text
使用 local-materials-to-course-kb 继续沉淀 TBD 里的资料。
```

Codex 会先判断资料数量、类型、复杂度、信息密度和分类跨度，再选择一个合理批次处理。

处理完成后，源资料会移动到：

```text
media/Done/YYYY-MM-DD_批次名
```

`Done` 里的资料不会被重复处理。你可以之后人工看一遍，没价值的再删。

## 不建议怎么用

不建议一次把所有资料直接叫 Codex 深度处理。更好的方式是把资料都放进 `TBD`，让 skill 自动分批。

也不建议把已经处理过的资料再放回 `TBD`，除非你确实想重新沉淀。
