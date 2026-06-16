# 数字图像处理知识库

## 推荐：使用 Obsidian Canvas 作为主知识图谱

1. 在 Obsidian 中选择“打开本地文件夹作为库”。
2. 选择 `D:\image-processing`。
3. 打开 `wiki/00_导航.md`。
4. 点击“总览 Canvas”进入 `数字图像处理知识图谱.canvas`。
5. 需要查看章节之间的少量强关系时，打开 `数字图像处理跨章关系.canvas`。

Graph View 只是辅助关系浏览，不作为主图。如果 Graph View 显示混乱，请直接使用 Canvas；固定分区、课程地图式入口都在 Canvas 中维护。

## Obsidian 原生知识库入口

本仓库可以直接作为 Obsidian vault 打开：

1. 安装并打开 Obsidian。
2. 选择“打开本地文件夹作为库”。
3. 选择 `D:\image-processing`。
4. 打开 `wiki/00_导航.md` 作为学习入口。
5. 打开 `数字图像处理知识图谱.canvas` 查看固定章节分区总览。
6. 如果需要阅读原书，把合法 PDF 副本放到 `raw/books/数字图像处理基础_朱虹.pdf`。

Graph View 只作为辅助关系浏览，不建议依赖它展示固定章节布局。固定分区关系图请使用 Obsidian Canvas：总览 Canvas 展示 11 个章节区域，每章目录中还有独立 Canvas。

本地 Graph View 过滤配置可通过以下命令恢复：

```powershell
python tools/configure_obsidian_graph.py
```

Canvas 可通过以下命令重新生成：

```powershell
python tools/build_obsidian_canvas.py
```

这是一个由 Codex 长期维护的 Obsidian 风格个人学习知识库，围绕《数字图像处理基础（朱虹）》进行转述、归纳和实验化整理。

## 当前进度

- 全书目录已初步覆盖，`wiki/` 中已经建立第 1 章到第 11 章的章节与小节入口。
- 第 1 章已完成基础细化，可作为概念入口。
- 第 2 章“图像增强”已完成精品样板化，包含公式、步骤、原创教学图示、代码链接和复习问题。
- 第 3 章“图像几何变换”已升级为第二个精品样板章节，包含可学习 wiki、可运行代码、原创图示和语义图谱关系。
- 第 4 章“图像去噪”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 5 章“图像锐化”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 6 章“图像的分割”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 7 章“二值图像处理”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 8 章“彩色图像处理”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 9 章“图像变换”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 10 章“图像压缩编码”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- 第 11 章“深度学习与图像处理”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。
- `raw/books/`、`raw/extracted_text/` 和 `raw/temp/` 只用于本地处理，不应提交公开仓库；公开仓库不包含原书 PDF 或原始抽取文本。

## 用 Obsidian 打开

1. 在 Obsidian 中选择“打开本地仓库”。
2. 选择仓库目录：`D:\image-processing`。
3. 从 `index.md` 或 `wiki/00_导航.md` 进入知识库。
4. 如果 Graph View 出现大量 `README`、维护文档或孤立节点，运行 `python tools/configure_obsidian_graph.py` 重置本地图谱过滤条件。
5. 如果需要查看内嵌 PDF，请按下一节放入合法本地副本。

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

第 4 章图像去噪示例：

```powershell
python examples/04_image_denoising/mean_filter.py --kernel-size 5
python examples/04_image_denoising/median_filter.py --kernel-size 5
python examples/04_image_denoising/k_nearest_mean_filter.py --kernel-size 5 --k 8
python examples/04_image_denoising/symmetric_nearest_mean_filter.py --kernel-size 5
python examples/04_image_denoising/non_local_means_filter.py --h 10
```

第 5 章图像锐化示例：

```powershell
python examples/05_image_sharpening/sobel_operator.py --kernel-size 3 --direction both
python examples/05_image_sharpening/laplacian_operator.py --amount 0.7
python examples/05_image_sharpening/canny_edge_detection.py --low 60 --high 160
python examples/05_image_sharpening/log_filter.py --sigma 1.2
```

第 6 章图像分割示例：

```powershell
python examples/06_image_segmentation/threshold_segmentation.py --threshold 128
python examples/06_image_segmentation/max_entropy_threshold.py
python examples/06_image_segmentation/otsu_threshold.py
python examples/06_image_segmentation/region_growing.py --seed-x 85 --seed-y 120 --tolerance 28
```

第 7 章二值图像处理示例：

```powershell
python examples/07_binary_image_processing/erosion_dilation.py --operation both --kernel-size 5
python examples/07_binary_image_processing/opening_closing.py --operation both --kernel-size 5
python examples/07_binary_image_processing/connected_component_labeling.py --connectivity 8
python examples/07_binary_image_processing/contour_labeling.py --min-area 30
python examples/07_binary_image_processing/thinning.py --max-iterations 80
```

第 8 章彩色图像处理示例：

```powershell
python examples/08_color_image_processing/color_spaces.py --space hsv
python examples/08_color_image_processing/white_balance.py --percentile 95
python examples/08_color_image_processing/gray_world.py
python examples/08_color_image_processing/color_compensation.py --red-gain 1.05 --blue-gain 0.95
```

第 9 章图像变换示例：

```powershell
python examples/09_image_transform/one_dimensional_fourier_transform.py
python examples/09_image_transform/two_dimensional_fft.py
python examples/09_image_transform/spectrum_visualization.py --gamma 0.4
python examples/09_image_transform/wavelet_decomposition.py --wavelet haar
python examples/09_image_transform/wavelet_denoising.py --threshold 12
```

第 10 章图像压缩编码示例：

```powershell
python examples/10_image_compression/rle_encoding.py --threshold 128
python examples/10_image_compression/huffman_encoding_demo.py
python examples/10_image_compression/jpeg_idea_demo.py --quality 24
python examples/10_image_compression/wavelet_compression_demo.py --keep-ratio 0.15
```

第 11 章深度学习与图像处理示例：

```powershell
python examples/11_deep_learning_image_processing/cnn_layers_demo.py
python examples/11_deep_learning_image_processing/srcnn_structure_demo.py
python examples/11_deep_learning_image_processing/lenet5_structure_demo.py
python examples/11_deep_learning_image_processing/alexnet_structure_demo.py
python examples/11_deep_learning_image_processing/yolo_concept_demo.py
```

默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。

## 重新生成图谱

`wiki/` 的 Obsidian 双链是知识图谱主数据源，`graph/semantic_edges.json` 补充精品章节的语义关系：

```powershell
python tools/build_graph_from_wiki.py
```

输出：

- `graph/knowledge_graph.json`：完整机器可读图谱。
- `graph/mermaid_graph.md`：清爽学习视图，只画章节包含关系和语义关系。

HTML 图谱已废弃，不再生成；固定分区主图谱请使用 Obsidian Canvas。

Obsidian 自带 Graph View 是本地 UI 状态，不提交 `.obsidian/`。需要恢复清爽视图时运行：

```powershell
python tools/configure_obsidian_graph.py
```

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

