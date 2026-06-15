# 数字图像处理知识库

这是一个由 Codex 长期维护的 Obsidian 风格个人学习知识库，围绕《数字图像处理基础（朱虹）》进行转述、归纳和实验化整理。

## 当前进度

- 全书目录已初步覆盖，`wiki/` 中已经建立第 1 章到第 11 章的章节与小节入口。
- 第 1 章已完成基础细化，可作为概念入口。
- 第 2 章“图像增强”已完成精品样板化，包含公式、步骤、原创教学图示、代码链接和复习问题。
- 第 3 章“图像几何变换”已升级为第二个精品样板章节，包含可学习 wiki、可运行代码、原创图示和语义图谱关系。
- 第 4 章到第 11 章已按模板升级为结构化精修初版，后续可按第 2/3 章样板继续深化。
- `raw/books/`、`raw/extracted_text/` 和 `raw/temp/` 只用于本地处理，不应提交公开仓库；公开仓库不包含原书 PDF 或原始抽取文本。

## 用 Obsidian 打开

1. 在 Obsidian 中选择“打开本地仓库”。
2. 选择仓库目录：`D:\image-processing`。
3. 从 `index.md` 或 `wiki/00_导航.md` 进入知识库。
4. 如果需要查看内嵌 PDF，请按下一节放入合法本地副本。

## 本地 PDF 阅读

公开仓库不显示原书 PDF。若你拥有合法副本，可在本地放入：

```text
raw/books/数字图像处理基础_朱虹.pdf
```

每个 wiki 小节顶部的 Obsidian 内嵌 PDF 阅读块会从对应页码打开，便于边看整理笔记边核对原书。不要把 PDF 提交到 GitHub。

## 运行代码示例

安装依赖：

```powershell
pip install -r requirements.txt
```

第 2 章图像增强示例：

```powershell
$env:MPLBACKEND='Agg'
python examples/02_image_enhancement/gamma_correction.py
python examples/02_image_enhancement/histogram_equalization.py
```

第 3 章几何变换示例：

```powershell
python examples/03_geometric_transform/image_translation.py --dx 30 --dy 20
python examples/03_geometric_transform/image_rotation.py --angle 30 --interpolation linear
python examples/03_geometric_transform/image_resize.py --scale-x 0.75 --scale-y 0.75 --interpolation area
python examples/03_geometric_transform/geometric_correction.py --strength 0.18
```

默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。

## 重新生成图谱

`wiki/` 的 Obsidian 双链是知识图谱主数据源，`graph/semantic_edges.json` 补充第 3 章语义关系：

```powershell
python tools/build_graph_from_wiki.py
```

输出：

- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`
- `graph/knowledge_graph.html`

## 健康检查

```powershell
python -m unittest discover -s tests
python tools/check_links.py
python tools/check_coverage.py
python tools/health_check.py
```

## 后续章节精修方式

后续章节请按第 2/3 章样板推进：

1. 先补齐“来源与状态”、公式、步骤、图示、代码和复习问题。
2. 只生成本章真正需要的原创教学图示。
3. 示例代码必须能独立运行，并使用合成样例或用户自备图片。
4. 将新的语义关系写入 `graph/semantic_edges.json`，再重建图谱。
5. 提交前运行完整健康检查。
