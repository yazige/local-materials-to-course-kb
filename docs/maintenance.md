# 队列维护与复核收口

这个项目跑起来之后，资料不会只停留在 `TBD` 和 `Done`。视频转写包、PPT 备注、关键帧、审核记录和待写入内容，通常会先落到：

```text
98_音视频处理工作区
```

这个目录不是新的资料入口，而是「草稿和复核工作区」。如果它长期堆着很多 `待复核` 文件夹，后面就会越来越难判断哪些已经写入、哪些只是草稿。

## 先盘点，不要一头扎进去

可以运行：

```bash
python3 skills/local-materials-to-course-kb/scripts/queue_inventory.py
```

它会输出：

- `media/TBD` 还有多少待处理资料；
- `media/Done` 有多少已归档资料；
- `98_音视频处理工作区` 里有多少 `待复核`、`处理中`、`测试中` 文件夹；
- 下一步建议先处理新资料，还是先收口待复核草稿。

如果你想拿到机器可读结果：

```bash
python3 skills/local-materials-to-course-kb/scripts/queue_inventory.py --format json
```

## 结构检查

如果刚改过索引、图片、目录或移动过源资料，建议运行：

```bash
python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py
```

它会检查：

- 八大分类目录是否齐全；
- `media/TBD` 和 `media/Done` 是否存在；
- 任务状态文件是否存在；
- Markdown 图片链接是否指向真实文件；
- 是否有 `.DS_Store` 这类系统隐藏文件；
- `98_音视频处理工作区` 是否有待复核积压。

如果需要 JSON：

```bash
python3 skills/local-materials-to-course-kb/scripts/verify_course_kb.py --format json
```

## 待复核工作区怎么收口

推荐做法：

1. 先选 1-3 个主题相近的 `待复核` 文件夹。
2. 优先看其中的 `06_待写入知识库内容` 和 `05_审核记录`。
3. 不要重新从原始视频或原始转写稿开始读，除非草稿明显不完整。
4. 写入正式知识库前，先和已有分类文档去重。
5. 写入后更新分类索引、总索引、案例表和审核记录。
6. 全部完成后，把文件夹后缀从 `待复核` 改成 `已写入`。
7. 如果只是保留痕迹，不再需要动作，可以再改成 `已归档`。

不要默认删除这些工作区。它们通常是以后追溯来源、解释审核判断的证据。
