# 覆盖检查报告

## 总体状态

- 全书目录：已初步覆盖。
- 第 1 章：已细化。
- 第 2 章：已精修为后续章节样板，包含核心概念、关键公式、算法步骤、直观理解、使用场景、优点、局限性、方法对比、代码链接和复习问题。
- 第 3 章到第 11 章：已升级为结构化精修初版，仍待逐章补图、复核公式和深化例题。

## 公开仓库边界

- `raw/books/*` 不提交，公开仓库不包含原书 PDF。
- `raw/extracted_text/*` 不提交，公开仓库不包含原始抽取文本。
- `raw/temp/*` 不提交。
- 上述目录仅保留 README 占位文件。

## 第 2 章教学图示

本次只生成第 2 章必要教学图示，保存于 `assets/extracted_figures/`：

- `ch02_gamma_curves.png`
- `ch02_contrast_stretching.png`
- `ch02_gray_window_slicing.png`
- `ch02_histogram_equalization.png`
- `ch02_adaptive_histogram_equalization.png`
- `ch02_pseudo_color_lut.png`
- `ch02_retinex_decomposition.png`

这些图是原创教学示意图，不是原书截图，可提交公开仓库。

## 公式复核

- 第 2 章常用公式已补入，但符号、页码和原书编号仍需人工复核。
- 第 3 章到第 11 章只放入章节级复习锚点公式，不宣称逐小节完整覆盖。

## 代码运行检查

第 2 章示例已在无界面 Matplotlib 后端逐个运行通过，输入为仓库自动生成的合成灰度样例 `assets/sample_images/sample_gray.png`：

- `gamma_correction.py`
- `contrast_stretching.py`
- `gray_level_window.py`
- `histogram_equalization.py`
- `adaptive_histogram_equalization.py`
- `pseudo_color.py`
- `retinex_enhancement.py`

合成样例可自由提交，不使用原书图片作为测试输入。

## 图谱生成

- 主数据源：`wiki/` 的 Obsidian 链接。
- 输出：`graph/knowledge_graph.json`、`graph/mermaid_graph.md`、`graph/knowledge_graph.html`。
- `src/graph_builder.py` 默认调用 wiki 图谱生成逻辑；CSV 构建函数仅保留用于 starter 测试兼容。
