# 数字图像处理知识库

这是一个由 Codex 长期维护的 Obsidian 风格个人学习知识库，资料来源为《数字图像处理基础（朱虹）》。

## 来源

原始 PDF：

```text
C:\Users\lizi\Desktop\学习\数字图像处理基础 (朱虹)(1).pdf
```

项目内处理路径：

```text
raw/books/数字图像处理基础_朱虹.pdf
```

当前仓库在 D 盘，源 PDF 在 C 盘，硬链接不可用；本机未允许创建文件符号链接，因此当前项目内 PDF 是普通副本，约 43MB。该目录已被 `.gitignore` 忽略，不会上传。

## 当前进度

- 已读取 PDF：233 页，内置目录 140 项。
- 已确认页码关系：PDF 页码 = 书中页码 + 15。
- 已抽取第 1 章全文和第 2 章预览文本到 `raw/extracted_text/`。
- 已细化第 1 章 wiki 和第 1 章知识关系图。
- 第 2 章及后续章节只建立了必要关系占位，等待继续细化。

## 入口

- `index.md`
- `wiki/00_导航.md`
- `wiki/01_引言/README.md`
- `graph/mermaid_graph.md`
- `coverage_report.md`

## 依赖

```powershell
pip install -r requirements.txt
```

本轮已使用 PyMuPDF 读取 PDF；不下载模型，不调用外部 API。

## 校验

```powershell
python -m unittest discover -s tests
```

后续维护时还需要检查 Obsidian 断链和知识图谱孤立节点。
