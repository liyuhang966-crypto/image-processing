# 数字图像处理知识库

这是一个由 Codex 长期维护的 Obsidian 风格个人学习知识库，围绕《数字图像处理基础（朱虹）》进行转述、归纳和实验化整理。

## 当前进度

- 全书目录已初步覆盖，`wiki/` 中已经建立第 1 章到第 11 章的章节与小节入口。
- 第 1 章已完成基础细化，可作为概念入口。
- 第 2 章已进入重点精修，并补充公式、算法步骤、原创教学图示、代码链接和复习问题。
- 第 3 章到第 11 章已按同一模板升级为结构化精修初版，后续仍需逐章补图、复核公式和深化例题。
- `raw/books/`、`raw/extracted_text/` 和 `raw/temp/` 只用于本地处理，不应提交公开仓库；公开仓库不包含原书 PDF 或原始抽取文本。

## 本地 PDF 阅读

公开仓库不显示原书 PDF。若你拥有合法副本，可在本地放入：

```text
raw/books/数字图像处理基础_朱虹.pdf
```

每个 wiki 小节顶部的 Obsidian 内嵌 PDF 阅读块会从对应页码打开，便于边看整理笔记边核对原书。

## 入口

- `index.md`
- `wiki/00_导航.md`
- `wiki/99_术语表.md`
- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`
- `graph/knowledge_graph.html`
- `coverage_report.md`

## 校验

```powershell
python -m unittest discover -s tests
python tools/check_links.py
python tools/health_check.py
```
