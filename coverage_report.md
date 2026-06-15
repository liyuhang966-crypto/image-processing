# 覆盖检查报告

## 总体状态

- 全书目录：已初步覆盖。
- 第 1 章：已细化。
- 第 2 章：已精修为第一个精品样板，覆盖核心概念、公式、算法步骤、教学图示、代码链接和复习问题。
- 第 3 章：已精修为第二个精品样板，新增原创几何变换图示、独立可运行示例、来源状态栏目和语义图谱关系。
- 第 4 章到第 11 章：已升级为结构化精修初版，仍待逐章补图、复核公式和深化例题。

## 公开仓库边界

- `raw/books/*` 不提交，公开仓库不包含原书 PDF。
- `raw/extracted_text/*` 不提交，公开仓库不包含原始抽取文本。
- `raw/temp/*` 不提交。
- 上述目录仅保留 README 占位文件。

## 第 2 章教学图示

- `ch02_gamma_curves.png`
- `ch02_contrast_stretching.png`
- `ch02_gray_window_slicing.png`
- `ch02_histogram_equalization.png`
- `ch02_adaptive_histogram_equalization.png`
- `ch02_pseudo_color_lut.png`
- `ch02_retinex_decomposition.png`

## 第 3 章教学图示

- `ch03_translation_grid.png`
- `ch03_mirror_transform.png`
- `ch03_rotation_center.png`
- `ch03_resize_interpolation.png`
- `ch03_shear_transform.png`
- `ch03_affine_transform.png`
- `ch03_geometric_correction.png`

这些图均为原创教学示意图，不是原书截图，可提交公开仓库。

## 公式复核

- 第 2 章和第 3 章常用公式已整理为复习锚点。
- 坐标原点、旋转方向、变量命名和原书编号仍需对照本地合法 PDF 人工复核。

## 代码运行检查

第 2 章示例已使用合成灰度图运行通过。

第 3 章示例已升级为独立脚本，默认使用 `assets/sample_images/sample_gray.png`，输出写入 `examples/output/`：

- `image_translation.py`
- `image_mirror.py`
- `image_rotation.py`
- `image_resize.py`
- `image_shear.py`
- `affine_transform.py`
- `geometric_correction.py`

## 图谱生成

- 主数据源：`wiki/` 的 Obsidian 链接。
- 第 3 章语义关系：`graph/semantic_edges.json`。
- 输出：`graph/knowledge_graph.json`、`graph/mermaid_graph.md`、`graph/knowledge_graph.html`。
