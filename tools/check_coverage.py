"""Coverage checks for refined digital image processing wiki chapters."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SECTIONS = [
    "## 来源与状态",
    "## 核心概念",
    "## 关键公式",
    "## 算法步骤",
    "## 教学图示",
    "## 对应代码",
    "## 相关知识",
    "## 复习问题",
]

REQUIRED_CHAPTER2_WIKI = [
    "2.1_γ校正.md",
    "2.2_对比度线性展宽.md",
    "2.3_灰级窗与灰级窗切片.md",
    "2.3.1_灰级窗.md",
    "2.3.2_灰级窗切片.md",
    "2.4_动态范围调整.md",
    "2.4.1_线性动态范围调整.md",
    "2.4.2_非线性动态范围调整.md",
    "2.5_直方图均衡化.md",
    "2.6_自适应直方图均衡化.md",
    "2.7_伪彩色.md",
    "2.8_Retinex图像增强方法.md",
    "2.x_习题.md",
]

REQUIRED_CHAPTER3_WIKI = [
    "3.1_图像的位置变换.md",
    "3.1.1_图像的平移.md",
    "3.1.2_图像的镜像.md",
    "3.1.3_图像的旋转.md",
    "3.2_图像的形状变换.md",
    "3.2.1_图像的缩小.md",
    "3.2.2_图像的放大.md",
    "3.2.3_图像的错切.md",
    "3.3_齐次坐标与图像的仿射变换.md",
    "3.4_图像几何畸变的校正.md",
    "3.x_习题.md",
]

REQUIRED_CHAPTER3_FIGURES = [
    "ch03_translation_grid.png",
    "ch03_mirror_transform.png",
    "ch03_rotation_center.png",
    "ch03_resize_interpolation.png",
    "ch03_shear_transform.png",
    "ch03_affine_transform.png",
    "ch03_geometric_correction.png",
]

REQUIRED_CHAPTER3_CODE = [
    "image_translation.py",
    "image_mirror.py",
    "image_rotation.py",
    "image_resize.py",
    "image_shear.py",
    "affine_transform.py",
    "geometric_correction.py",
]

REQUIRED_CHAPTER4_WIKI = [
    "4.1_图像噪声.md",
    "4.2_均值滤波.md",
    "4.2.1_均值滤波的原理.md",
    "4.2.2_均值滤波方法.md",
    "4.3_中值滤波.md",
    "4.3.1_中值滤波的原理.md",
    "4.3.2_中值滤波方法.md",
    "4.4_边界保持类平滑滤波.md",
    "4.4.1_K近邻均值滤波.md",
    "4.4.2_对称近邻均值滤波.md",
    "4.5_非局部均值滤波.md",
    "4.x_习题.md",
]

REQUIRED_CHAPTER4_FIGURES = [
    "ch04_noise_models.png",
    "ch04_mean_filter_kernel.png",
    "ch04_median_filter_window.png",
    "ch04_edge_preserving_filters.png",
    "ch04_non_local_means.png",
]

REQUIRED_CHAPTER4_CODE = [
    "mean_filter.py",
    "median_filter.py",
    "k_nearest_mean_filter.py",
    "symmetric_nearest_mean_filter.py",
    "non_local_means_filter.py",
]

REQUIRED_CHAPTER5_WIKI = [
    "5.1_图像细节的基本特征.md",
    "5.2_一阶微分算子.md",
    "5.2.1_具有方向性的一阶微分算子.md",
    "5.2.2_Roberts交叉微分算子.md",
    "5.2.3_Sobel微分算子.md",
    "5.2.4_Priwitt微分算子.md",
    "5.3_二阶微分算子.md",
    "5.3.1_Laplacian微分算子.md",
    "5.3.2_Wallis微分算子.md",
    "5.4_微分算子在边缘检测中的应用.md",
    "5.5_Canny算子.md",
    "5.6_LOG滤波算法.md",
    "5.x_习题.md",
]

REQUIRED_CHAPTER5_FIGURES = [
    "ch05_detail_profiles.png",
    "ch05_first_derivative_kernels.png",
    "ch05_roberts_sobel_prewitt.png",
    "ch05_laplacian_sharpening.png",
    "ch05_canny_pipeline.png",
    "ch05_log_filter.png",
]

REQUIRED_CHAPTER5_CODE = [
    "roberts_operator.py",
    "sobel_operator.py",
    "prewitt_operator.py",
    "laplacian_operator.py",
    "canny_edge_detection.py",
    "log_filter.py",
]

REQUIRED_CHAPTER6_WIKI = [
    "6.1_阈值分割方法.md",
    "6.1.1_p-参数法.md",
    "6.1.2_最大熵方法.md",
    "6.1.3_最大类间、类内方差比法.md",
    "6.2_区域生长分割方法.md",
    "6.x_习题.md",
]

REQUIRED_CHAPTER6_FIGURES = [
    "ch06_threshold_histogram.png",
    "ch06_p_parameter_threshold.png",
    "ch06_max_entropy_threshold.png",
    "ch06_otsu_variance.png",
    "ch06_region_growing.png",
]

REQUIRED_CHAPTER6_CODE = [
    "threshold_segmentation.py",
    "max_entropy_threshold.py",
    "otsu_threshold.py",
    "region_growing.py",
]

REQUIRED_CHAPTER7_WIKI = [
    "7.1_二值图像中的基本概念.md",
    "7.1.1_连接与点特性.md",
    "7.1.2_几何特征.md",
    "7.2_腐蚀与膨胀.md",
    "7.2.1_腐蚀.md",
    "7.2.2_膨胀.md",
    "7.3_开运算与闭运算.md",
    "7.3.1_开运算.md",
    "7.3.2_闭运算.md",
    "7.4_贴标签.md",
    "7.4.1_连通域标签法.md",
    "7.4.2_轮廓标签法.md",
    "7.5_细线化方法.md",
    "7.x_习题.md",
]

REQUIRED_CHAPTER7_FIGURES = [
    "ch07_connectivity.png",
    "ch07_morphology_erosion_dilation.png",
    "ch07_opening_closing.png",
    "ch07_component_labeling.png",
    "ch07_thinning.png",
]

REQUIRED_CHAPTER7_CODE = [
    "erosion_dilation.py",
    "opening_closing.py",
    "connected_component_labeling.py",
    "contour_labeling.py",
    "thinning.py",
]

REQUIRED_CHAPTER8_WIKI = [
    "8.1_彩色的形成原理与基本概念.md",
    "8.2_表色系.md",
    "8.2.1_计算颜色模型系统.md",
    "8.2.2_视觉颜色模型系统.md",
    "8.2.3_工业颜色模型系统.md",
    "8.3_色彩平衡.md",
    "8.3.1_白平衡法.md",
    "8.3.2_灰色世界法.md",
    "8.4_彩色补偿.md",
    "8.x_习题.md",
]

REQUIRED_CHAPTER8_FIGURES = [
    "ch08_color_formation.png",
    "ch08_color_spaces.png",
    "ch08_white_balance.png",
    "ch08_gray_world.png",
    "ch08_color_compensation.png",
]

REQUIRED_CHAPTER8_CODE = [
    "color_spaces.py",
    "white_balance.py",
    "gray_world.py",
    "color_compensation.py",
]

REQUIRED_CHAPTER9_WIKI = [
    "9.1_图像的频域变换（傅里叶变换）.md",
    "9.1.1_一维傅里叶变换.md",
    "9.1.2_二维傅里叶变换.md",
    "9.1.3_快速傅里叶变换（FFT）.md",
    "9.1.4_图像的频谱分布特性.md",
    "9.2_小波变换.md",
    "9.2.1_连续小波变换.md",
    "9.2.2_离散小波变换.md",
    "9.2.3_小波的多尺度分解与重构.md",
    "9.3_小波变换在图像处理中的应用.md",
    "9.3.1_应用于图像压缩.md",
    "9.3.2_应用于图像融合.md",
    "9.3.3_应用于图像增强.md",
    "9.3.4_应用于图像去噪.md",
    "9.x_习题.md",
]

REQUIRED_CHAPTER9_FIGURES = [
    "ch09_fft_spectrum.png",
    "ch09_frequency_filtering.png",
    "ch09_wavelet_multiscale.png",
    "ch09_wavelet_applications.png",
]

REQUIRED_CHAPTER9_CODE = [
    "one_dimensional_fourier_transform.py",
    "two_dimensional_fft.py",
    "spectrum_visualization.py",
    "wavelet_decomposition.py",
    "wavelet_denoising.py",
]

REQUIRED_CHAPTER10_WIKI = [
    "10.1_图像冗余的概念.md",
    "10.1.1_冗余的概念.md",
    "10.1.2_图像中的冗余.md",
    "10.2_图像无损压缩编码.md",
    "10.2.1_行程编码（RLE）.md",
    "10.2.2_哈夫曼（Huffman）编码.md",
    "10.3_图像有损压缩编码.md",
    "10.3.1_彩色图像的有损编码.md",
    "10.3.2_小波变换编码.md",
    "10.x_习题.md",
]

REQUIRED_CHAPTER10_FIGURES = [
    "ch10_compression_pipeline.png",
    "ch10_rle_runs.png",
    "ch10_huffman_tree.png",
    "ch10_lossy_quantization.png",
    "ch10_wavelet_compression.png",
]

REQUIRED_CHAPTER10_CODE = [
    "rle_encoding.py",
    "huffman_encoding_demo.py",
    "jpeg_idea_demo.py",
    "wavelet_compression_demo.py",
]

REQUIRED_CHAPTER11_WIKI = [
    "11.1_深度卷积网络的基本结构.md",
    "11.1.1_卷积层.md",
    "11.1.2_激活层.md",
    "11.1.3_BN层（批数据归一化处理层）.md",
    "11.1.4_池化层.md",
    "11.2_超分辨率图像重建卷积网络.md",
    "11.2.1_SRCNN网络.md",
    "11.2.2_ESPCN网络.md",
    "11.3_图像分类深度卷积网络.md",
    "11.3.1_LeNet-5网络.md",
    "11.3.2_AlexNet网络.md",
    "11.4_图像目标检测深度卷积网络.md",
    "11.4.1_Faster-RCNN网络.md",
    "11.4.2_YOLO网络.md",
    "11.x_习题.md",
]

REQUIRED_CHAPTER11_FIGURES = [
    "ch11_cnn_layers.png",
    "ch11_super_resolution.png",
    "ch11_classification_networks.png",
    "ch11_detection_networks.png",
    "ch11_yolo_grid.png",
]

REQUIRED_CHAPTER11_CODE = [
    "cnn_layers_demo.py",
    "srcnn_structure_demo.py",
    "lenet5_structure_demo.py",
    "alexnet_structure_demo.py",
    "yolo_concept_demo.py",
]


def check_markdown_sections(chapter_dir: Path, files: list[str]) -> list[str]:
    errors: list[str] = []
    for filename in files:
        path = chapter_dir / filename
        if not path.exists():
            errors.append(f"missing wiki file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.relative_to(ROOT)} missing section {section}")
    return errors


def check_required_files(folder: Path, files: list[str], label: str) -> list[str]:
    return [
        f"missing {label}: {(folder / filename).relative_to(ROOT)}"
        for filename in files
        if not (folder / filename).exists()
    ]


def check_graph() -> list[str]:
    path = ROOT / "graph" / "knowledge_graph.json"
    if not path.exists():
        return ["missing graph/knowledge_graph.json"]
    graph = json.loads(path.read_text(encoding="utf-8"))
    if not graph.get("nodes") or not graph.get("edges"):
        return ["graph/knowledge_graph.json should contain non-empty nodes and edges"]
    required_relations = {
        "PREREQUISITE",
        "COMPARES_WITH",
        "GENERALIZES",
        "IMPLEMENTED_BY",
        "USES_FORMULA",
        "IMPROVES_OR_EXTENDS",
        "APPLIES_TO",
    }
    relations = {edge.get("type") for edge in graph.get("edges", [])}
    missing = sorted(required_relations - relations)
    return [f"missing semantic graph relation: {item}" for item in missing]


def check_public_boundaries() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    errors: list[str] = []
    for path in result.stdout.splitlines():
        normalized = path.replace("\\", "/")
        if normalized.endswith(".pdf"):
            errors.append(f"tracked PDF should not be public: {path}")
        if normalized.startswith("raw/books/") and normalized != "raw/books/README.md":
            errors.append(f"tracked raw book file should not be public: {path}")
        if normalized.startswith("raw/extracted_text/") and normalized != "raw/extracted_text/README.md":
            errors.append(f"tracked extracted text should not be public: {path}")
        if normalized.startswith("raw/temp/") and normalized != "raw/temp/README.md":
            errors.append(f"tracked temp file should not be public: {path}")
    return errors


def collect_errors() -> list[str]:
    errors: list[str] = []
    if not (ROOT / "coverage_report.md").exists():
        errors.append("missing coverage_report.md")
    errors.extend(check_markdown_sections(ROOT / "wiki" / "02_图像增强", REQUIRED_CHAPTER2_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "03_图像几何变换", REQUIRED_CHAPTER3_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "04_图像去噪", REQUIRED_CHAPTER4_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "05_图像锐化", REQUIRED_CHAPTER5_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "06_图像的分割", REQUIRED_CHAPTER6_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "07_二值图像处理", REQUIRED_CHAPTER7_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "08_彩色图像处理", REQUIRED_CHAPTER8_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "09_图像变换", REQUIRED_CHAPTER9_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "10_图像压缩编码", REQUIRED_CHAPTER10_WIKI))
    errors.extend(check_markdown_sections(ROOT / "wiki" / "11_深度学习与图像处理", REQUIRED_CHAPTER11_WIKI))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER3_FIGURES, "chapter 3 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER4_FIGURES, "chapter 4 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER5_FIGURES, "chapter 5 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER6_FIGURES, "chapter 6 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER7_FIGURES, "chapter 7 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER8_FIGURES, "chapter 8 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER9_FIGURES, "chapter 9 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER10_FIGURES, "chapter 10 figure"))
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER11_FIGURES, "chapter 11 figure"))
    errors.extend(check_required_files(ROOT / "examples" / "03_geometric_transform", REQUIRED_CHAPTER3_CODE, "chapter 3 code"))
    errors.extend(check_required_files(ROOT / "examples" / "04_image_denoising", REQUIRED_CHAPTER4_CODE, "chapter 4 code"))
    errors.extend(check_required_files(ROOT / "examples" / "05_image_sharpening", REQUIRED_CHAPTER5_CODE, "chapter 5 code"))
    errors.extend(check_required_files(ROOT / "examples" / "06_image_segmentation", REQUIRED_CHAPTER6_CODE, "chapter 6 code"))
    errors.extend(check_required_files(ROOT / "examples" / "07_binary_image_processing", REQUIRED_CHAPTER7_CODE, "chapter 7 code"))
    errors.extend(check_required_files(ROOT / "examples" / "08_color_image_processing", REQUIRED_CHAPTER8_CODE, "chapter 8 code"))
    errors.extend(check_required_files(ROOT / "examples" / "09_image_transform", REQUIRED_CHAPTER9_CODE, "chapter 9 code"))
    errors.extend(check_required_files(ROOT / "examples" / "10_image_compression", REQUIRED_CHAPTER10_CODE, "chapter 10 code"))
    errors.extend(check_required_files(ROOT / "examples" / "11_deep_learning_image_processing", REQUIRED_CHAPTER11_CODE, "chapter 11 code"))
    errors.extend(check_graph())
    errors.extend(check_public_boundaries())
    return errors


def main() -> int:
    errors = collect_errors()
    if errors:
        print("Coverage check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Coverage check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
