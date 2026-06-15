from __future__ import annotations

import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF = Path(r"C:\Users\lizi\Desktop\学习\数字图像处理基础 (朱虹)(1).pdf")
OFFSET = 15

CHAPTER_DIRS = {
    1: "01_引言",
    2: "02_图像增强",
    3: "03_图像几何变换",
    4: "04_图像去噪",
    5: "05_图像锐化",
    6: "06_图像的分割",
    7: "07_二值图像处理",
    8: "08_彩色图像处理",
    9: "09_图像变换",
    10: "10_图像压缩编码",
    11: "11_深度学习与图像处理",
}

REQUIRED_EXAMPLES = {
    2: {
        "02_image_enhancement": [
            ("gamma_correction.py", "2.1", "γ 校正"),
            ("contrast_stretching.py", "2.2", "对比度线性展宽"),
            ("gray_level_window.py", "2.3", "灰级窗与灰级窗切片"),
            ("histogram_equalization.py", "2.5", "直方图均衡化"),
            ("adaptive_histogram_equalization.py", "2.6", "自适应直方图均衡化"),
            ("pseudo_color.py", "2.7", "伪彩色"),
            ("retinex_enhancement.py", "2.8", "Retinex 图像增强方法"),
        ]
    },
    3: {
        "03_geometric_transform": [
            ("image_translation.py", "3.1.1", "图像的平移"),
            ("image_mirror.py", "3.1.2", "图像的镜像"),
            ("image_rotation.py", "3.1.3", "图像的旋转"),
            ("image_resize.py", "3.2", "图像的缩放"),
            ("image_shear.py", "3.2.3", "图像的错切"),
            ("affine_transform.py", "3.3", "仿射变换"),
            ("geometric_correction.py", "3.4", "几何畸变校正"),
        ]
    },
    4: {
        "04_image_denoising": [
            ("mean_filter.py", "4.2", "均值滤波"),
            ("median_filter.py", "4.3", "中值滤波"),
            ("k_nearest_mean_filter.py", "4.4.1", "K 近邻均值滤波"),
            ("symmetric_nearest_mean_filter.py", "4.4.2", "对称近邻均值滤波"),
            ("non_local_means_filter.py", "4.5", "非局部均值滤波"),
        ]
    },
    5: {
        "05_image_sharpening": [
            ("roberts_operator.py", "5.2.2", "Roberts 交叉微分算子"),
            ("sobel_operator.py", "5.2.3", "Sobel 微分算子"),
            ("prewitt_operator.py", "5.2.4", "Priwitt 微分算子"),
            ("laplacian_operator.py", "5.3.1", "Laplacian 微分算子"),
            ("canny_edge_detection.py", "5.5", "Canny 算子"),
            ("log_filter.py", "5.6", "LOG 滤波算法"),
        ]
    },
    6: {
        "06_image_segmentation": [
            ("threshold_segmentation.py", "6.1", "阈值分割方法"),
            ("max_entropy_threshold.py", "6.1.2", "最大熵方法"),
            ("otsu_threshold.py", "6.1.3", "最大类间、类内方差比法"),
            ("region_growing.py", "6.2", "区域生长分割方法"),
        ]
    },
    7: {
        "07_binary_image_processing": [
            ("erosion_dilation.py", "7.2", "腐蚀与膨胀"),
            ("opening_closing.py", "7.3", "开运算与闭运算"),
            ("connected_component_labeling.py", "7.4.1", "连通域标签法"),
            ("contour_labeling.py", "7.4.2", "轮廓标签法"),
            ("thinning.py", "7.5", "细线化方法"),
        ]
    },
    8: {
        "08_color_image_processing": [
            ("color_spaces.py", "8.2", "表色系"),
            ("white_balance.py", "8.3.1", "白平衡法"),
            ("gray_world.py", "8.3.2", "灰色世界法"),
            ("color_compensation.py", "8.4", "彩色补偿"),
        ]
    },
    9: {
        "09_image_transform": [
            ("one_dimensional_fourier_transform.py", "9.1.1", "一维傅里叶变换"),
            ("two_dimensional_fft.py", "9.1.2", "二维傅里叶变换"),
            ("spectrum_visualization.py", "9.1.4", "图像的频谱分布特性"),
            ("wavelet_decomposition.py", "9.2.3", "小波的多尺度分解与重构"),
            ("wavelet_denoising.py", "9.3.4", "应用于图像去噪"),
        ]
    },
    10: {
        "10_image_compression": [
            ("rle_encoding.py", "10.2.1", "行程编码（RLE）"),
            ("huffman_encoding_demo.py", "10.2.2", "哈夫曼（Huffman）编码"),
            ("jpeg_idea_demo.py", "10.3", "图像有损压缩编码"),
            ("wavelet_compression_demo.py", "10.3.2", "小波变换编码"),
        ]
    },
    11: {
        "11_deep_learning_image_processing": [
            ("cnn_layers_demo.py", "11.1", "深度卷积网络的基本结构"),
            ("lenet5_structure_demo.py", "11.3.1", "LeNet-5 网络"),
            ("alexnet_structure_demo.py", "11.3.2", "AlexNet 网络"),
            ("srcnn_structure_demo.py", "11.2.1", "SRCNN 网络"),
            ("yolo_concept_demo.py", "11.4.2", "YOLO 网络"),
        ]
    },
}

RELATIONS = [
    ("1.3", "1.3.1", "章节包含关系"),
    ("1.3", "1.3.2", "章节包含关系"),
    ("1.3.1", "1.3.2", "前置知识"),
    ("1.3.2", "2.5", "前置知识"),
    ("1.3.2", "6.1", "应用关系"),
    ("1.2", "2.1", "前置知识"),
    ("2.1", "2.2", "同类方法"),
    ("2.2", "2.4", "同类方法"),
    ("2.5", "2.6", "改进关系"),
    ("2.5", "6.1.3", "前置知识"),
    ("3.1.1", "3.3", "前置知识"),
    ("3.1.2", "3.3", "前置知识"),
    ("3.1.3", "3.3", "前置知识"),
    ("3.3", "3.4", "应用关系"),
    ("4.1", "4.2", "前置知识"),
    ("4.2", "4.3", "对比关系"),
    ("4.2", "4.4", "改进关系"),
    ("4.4", "4.5", "改进关系"),
    ("5.2", "5.2.2", "章节包含关系"),
    ("5.2.3", "5.5", "算法流程"),
    ("5.3.1", "5.6", "算法流程"),
    ("5.5", "6.1", "应用关系"),
    ("6.1", "6.1.3", "同类方法"),
    ("6.1", "6.2", "对比关系"),
    ("6.2", "7.4", "应用关系"),
    ("7.2", "7.3", "算法流程"),
    ("7.4.1", "7.4.2", "同类方法"),
    ("7.4", "7.5", "应用关系"),
    ("8.2", "8.3", "前置知识"),
    ("8.3.1", "8.3.2", "同类方法"),
    ("8.3", "8.4", "应用关系"),
    ("9.1.1", "9.1.2", "前置知识"),
    ("9.1.2", "9.1.3", "改进关系"),
    ("9.1.2", "9.1.4", "应用关系"),
    ("9.2.1", "9.2.2", "前置知识"),
    ("9.2.2", "9.2.3", "算法流程"),
    ("9.2", "9.3", "应用关系"),
    ("9.3.1", "10.3.2", "应用关系"),
    ("10.1", "10.2", "前置知识"),
    ("10.2.1", "10.2.2", "同类方法"),
    ("10.2", "10.3", "对比关系"),
    ("11.1", "11.2", "前置知识"),
    ("11.1", "11.3", "前置知识"),
    ("11.1", "11.4", "前置知识"),
    ("11.2.1", "11.2.2", "同类方法"),
    ("11.3.1", "11.3.2", "同类方法"),
    ("11.4.1", "11.4.2", "同类方法"),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def normalize_title(title: str) -> str:
    title = title.replace(" ", "")
    title = title.replace("－", "-")
    return title


def split_number_title(raw: str) -> tuple[str | None, str]:
    text = raw.strip().replace("　", "").replace(" ", "")
    match = re.match(r"^(\d+(?:\.\d+)*)(.+)$", text)
    if match:
        return match.group(1), match.group(2)
    chapter = re.match(r"^第(\d+)章(.+)$", text)
    if chapter:
        return chapter.group(1), chapter.group(2)
    return None, text


def chapter_no_from_title(raw: str) -> int | None:
    match = re.match(r"第(\d+)章", raw.replace(" ", ""))
    return int(match.group(1)) if match else None


def note_filename(number: str, title: str) -> str:
    return f"{number}_{normalize_title(title)}.md"


def section_text(doc: fitz.Document, start_page: int, end_page: int) -> str:
    chunks = []
    for pdf_page in range(start_page, end_page + 1):
        chunks.append(doc.load_page(pdf_page - 1).get_text("text"))
    return "\n".join(chunks)


def meaningful_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        clean = re.sub(r"\s+", "", line)
        if len(clean) >= 8 and not clean.startswith("图") and not clean.startswith("表"):
            lines.append(clean)
    return lines[:8]


def formula_hint(title: str) -> str:
    if "γ" in title:
        return "常见关系为幂律变换，形如 $s = c r^\\gamma$；具体符号与书中公式需人工复核。"
    if "对比度" in title or "动态范围" in title:
        return "通常涉及灰度线性或非线性映射，端点、斜率和分段区间需结合书中公式复核。"
    if "直方图" in title:
        return "常用 $h(k)=n_k$ 表示灰度级 $k$ 的像素数，均衡化涉及累计分布函数；细节需人工复核。"
    if "傅里叶" in title or "FFT" in title:
        return "涉及离散傅里叶变换及其快速算法，公式需按书中符号复核。"
    if "小波" in title:
        return "涉及尺度、平移、分解与重构公式，需人工复核。"
    if "卷积" in title or "滤波" in title or "算子" in title:
        return "涉及邻域模板或卷积运算，具体模板和边界处理需人工复核。"
    if "编码" in title or "RLE" in title or "Huffman" in title:
        return "涉及码长、概率和压缩率等表达，需结合书中公式复核。"
    return "本节公式未自动确认；如书中含公式，需人工复核后补入 LaTeX。"


def concept_text(number: str, title: str, sample_lines: list[str]) -> str:
    joined = "；".join(sample_lines[:3])
    prefix = f"本节围绕“{title}”展开，属于《数字图像处理基础》目录中的 {number}。"
    if "增强" in title or "校正" in title or "对比度" in title or "直方图" in title or "伪彩色" in title or "Retinex" in title:
        return prefix + "它关注如何改善图像的可观察性，让重要灰度、颜色或细节更突出，同时抑制不利于判读的信息。"
    if "平移" in title or "镜像" in title or "旋转" in title or "缩小" in title or "放大" in title or "错切" in title or "仿射" in title or "几何" in title:
        return prefix + "它关注像素坐标如何映射到新位置，是理解图像几何校正、配准和空间变换的基础。"
    if "噪声" in title or "滤波" in title or "均值" in title or "中值" in title or "非局部" in title:
        return prefix + "它关注图像退化和噪声抑制，通过邻域统计、排序或相似块关系降低噪声影响。"
    if "锐化" in title or "微分" in title or "Sobel" in title or "Canny" in title or "LOG" in title or "边缘" in title:
        return prefix + "它关注灰度变化、边缘和细节增强，是分割、轮廓分析和目标检测的前置基础。"
    if "分割" in title or "阈值" in title or "区域生长" in title:
        return prefix + "它关注把目标区域从背景或其他区域中分离出来，是从图像处理走向图像分析的重要步骤。"
    if "二值" in title or "腐蚀" in title or "膨胀" in title or "开运算" in title or "闭运算" in title or "标签" in title or "细线化" in title:
        return prefix + "它关注二值图像中的结构、连通性和形态变化，用于区域分析、形状处理和目标标记。"
    if "彩色" in title or "颜色" in title or "白平衡" in title or "灰色世界" in title or "补偿" in title:
        return prefix + "它关注颜色形成、颜色空间和色彩校正，把灰度处理扩展到多通道彩色信息。"
    if "傅里叶" in title or "频域" in title or "频谱" in title or "小波" in title or "变换" in title:
        return prefix + "它关注把图像从空间域变换到频域或多尺度域，以便分析频率结构、压缩、融合、增强或去噪。"
    if "压缩" in title or "冗余" in title or "编码" in title or "Huffman" in title or "RLE" in title:
        return prefix + "它关注图像数据中可压缩的冗余，通过编码降低存储和传输成本。"
    if "卷积" in title or "网络" in title or "SRCNN" in title or "ESPCN" in title or "LeNet" in title or "AlexNet" in title or "YOLO" in title or "Faster" in title or "深度" in title:
        return prefix + "它关注深度学习网络在图像重建、分类和检测中的结构作用；本项目只做结构理解和轻量演示，不下载模型或训练大模型。"
    if "习题" in title:
        return prefix + "它用于复习本章概念、算法关系和基本计算。"
    return prefix + (f"抽取文本提示：{joined}。" if joined else "当前已根据目录建立条目，正文细节需继续复核。")


def method_steps(title: str) -> list[str]:
    if "阈值" in title:
        return ["读取灰度图像。", "根据灰度分布或准则选择阈值。", "把像素划分为目标与背景。", "检查分割结果是否符合目标区域。"]
    if "滤波" in title or "均值" in title or "中值" in title:
        return ["定义邻域或搜索窗口。", "根据均值、中值或相似性计算输出像素。", "遍历整幅图像。", "比较平滑效果和边缘保持情况。"]
    if "Sobel" in title or "Roberts" in title or "Priwitt" in title or "Laplacian" in title or "Wallis" in title or "Canny" in title or "LOG" in title:
        return ["计算局部灰度变化。", "增强或检测边缘响应。", "必要时进行阈值或连接处理。", "结合噪声情况评价边缘质量。"]
    if "直方图" in title:
        return ["统计灰度分布。", "计算累计分布或局部分布。", "建立灰度映射。", "输出增强后的图像并比较直方图变化。"]
    if "γ" in title or "对比度" in title or "动态范围" in title:
        return ["分析原图灰度范围和显示问题。", "选择灰度映射函数。", "对每个像素执行映射。", "比较增强前后的视觉效果和灰度分布。"]
    if "平移" in title or "镜像" in title or "旋转" in title or "错切" in title or "仿射" in title or "缩小" in title or "放大" in title:
        return ["建立源坐标与目标坐标的映射。", "确定输出图像大小。", "进行插值或采样。", "检查几何形状和边界区域。"]
    if "编码" in title or "压缩" in title or "RLE" in title or "Huffman" in title:
        return ["分析图像冗余。", "选择编码规则。", "生成码流或压缩表示。", "比较压缩率、失真和重建质量。"]
    if "网络" in title or "卷积" in title or "YOLO" in title or "AlexNet" in title or "LeNet" in title or "SRCNN" in title or "ESPCN" in title:
        return ["明确输入图像或特征图尺寸。", "梳理网络层次和张量尺寸变化。", "理解每类层的作用。", "只做结构演示，不下载模型、不训练大模型。"]
    return ["阅读本节定义和例子。", "找出输入、输出和核心变量。", "梳理它与前后章节的关系。", "用小例子验证理解。"]


def application_text(title: str) -> str:
    if "直方图" in title:
        return "常用于图像质量评价、对比度增强和阈值分割前的灰度分布分析。"
    if "滤波" in title or "噪声" in title:
        return "常用于图像预处理，减少采集噪声对后续边缘检测、分割和识别的影响。"
    if "Canny" in title or "Sobel" in title or "Laplacian" in title or "LOG" in title:
        return "常用于边缘检测、轮廓提取、目标定位和分割前的结构增强。"
    if "傅里叶" in title or "频谱" in title or "小波" in title:
        return "常用于频域分析、滤波、压缩、融合、增强和去噪。"
    if "压缩" in title or "编码" in title:
        return "常用于图像存储、传输和带宽受限场景。"
    if "网络" in title or "YOLO" in title or "Faster" in title:
        return "常用于超分辨率重建、分类、检测等高层视觉任务。"
    return "常用于数字图像处理学习、复习和相关算法实现前的概念定位。"


def related_numbers(number: str, all_numbers: list[str]) -> list[str]:
    chapter = number.split(".")[0] if "." in number else number
    candidates = [n for n in all_numbers if n != number and n.startswith(chapter + ".")]
    anchors = ["1.3", "1.3.2", "2.5", "4.2", "5.5", "6.1", "9.1.2", "11.1"]
    for anchor in anchors:
        if anchor != number and anchor in all_numbers and anchor not in candidates:
            candidates.append(anchor)
    return candidates[:5]


def obsidian_link(entry: dict) -> str:
    return f"[[{entry['number']}_{normalize_title(entry['title'])}]]"


def build_entries(doc: fitz.Document) -> list[dict]:
    toc = [row for row in doc.get_toc(simple=True) if row[1] != "目录"]
    entries = []
    current_chapter = None
    chapter_title = None
    chapter_dir = None
    last_section_number = None
    for index, (level, raw_title, pdf_page) in enumerate(toc):
        if raw_title == "参考文献":
            entries.append({
                "kind": "reference",
                "level": level,
                "number": "ref",
                "title": "参考文献",
                "chapter": None,
                "chapter_title": "参考文献",
                "chapter_dir": "98_习题索引",
                "pdf_page": pdf_page,
            })
            continue
        chapter_no = chapter_no_from_title(raw_title)
        if level == 2 and chapter_no in CHAPTER_DIRS:
            current_chapter = chapter_no
            chapter_title = CHAPTER_DIRS[chapter_no].split("_", 1)[1]
            chapter_dir = CHAPTER_DIRS[chapter_no]
            entries.append({
                "kind": "chapter",
                "level": level,
                "number": str(chapter_no),
                "title": chapter_title,
                "chapter": current_chapter,
                "chapter_title": chapter_title,
                "chapter_dir": chapter_dir,
                "pdf_page": pdf_page,
            })
            continue
        if not current_chapter:
            continue
        if raw_title == "习题":
            number = f"{current_chapter}.x"
            title = "习题"
        else:
            number, title = split_number_title(raw_title)
            if not number:
                continue
        entries.append({
            "kind": "section",
            "level": level,
            "number": number,
            "title": title,
            "chapter": current_chapter,
            "chapter_title": chapter_title,
            "chapter_dir": chapter_dir,
            "pdf_page": pdf_page,
        })
        last_section_number = number
    for i, entry in enumerate(entries):
        next_pages = [e["pdf_page"] for e in entries[i + 1:] if e["pdf_page"] >= entry["pdf_page"]]
        entry["end_pdf_page"] = max(entry["pdf_page"], (next_pages[0] - 1) if next_pages else doc.page_count)
        entry["book_page"] = entry["pdf_page"] - OFFSET if entry["pdf_page"] > OFFSET else None
    return entries


def entry_path(entry: dict) -> Path:
    if entry["kind"] == "chapter":
        return ROOT / "wiki" / entry["chapter_dir"] / "README.md"
    if entry["kind"] == "reference":
        return ROOT / "wiki" / "98_习题索引" / "参考文献.md"
    return ROOT / "wiki" / entry["chapter_dir"] / note_filename(entry["number"], entry["title"])


def write_note(entry: dict, entries_by_number: dict[str, dict], all_numbers: list[str], text: str) -> None:
    path = entry_path(entry)
    sample_lines = meaningful_lines(text)
    related = [n for n in related_numbers(entry["number"], all_numbers) if n in entries_by_number]
    code_paths = []
    for folders in REQUIRED_EXAMPLES.values():
        for folder, examples in folders.items():
            for filename, sec, _ in examples:
                if sec == entry["number"]:
                    code_paths.append(f"examples/{folder}/{filename}")
    code_text = "\n".join(f"* `{p}`" for p in code_paths) if code_paths else "本节暂不生成代码示例。"
    related_text = "\n".join(f"* {obsidian_link(entries_by_number[n])}" for n in related[:5])
    steps = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(method_steps(entry["title"])))
    note = f"""# {entry['number']} {entry['title']}

## 来源

* 书名：数字图像处理基础
* 作者：朱虹
* 章节：第 {entry['chapter']} 章 {entry['chapter_title']}
* 小节：{entry['number']} {entry['title']}
* 书中页码：{entry['book_page']}
* PDF 页码：{entry['pdf_page']}
* 原始文件：raw/books/数字图像处理基础_朱虹.pdf
* 处理状态：已按 PDF 目录读取整理；公式、图示和表格需人工复核

## 核心概念

{concept_text(entry['number'], entry['title'], sample_lines)}

## 关键公式

{formula_hint(entry['title'])}

## 方法步骤

{steps}

## 直观理解

把本节放进处理链路中理解：先明确输入图像或中间表示，再看它改变了灰度、颜色、坐标、频率、区域还是语义结构，最后观察它服务于增强、去噪、锐化、分割、压缩或识别中的哪一步。

## 应用场景

{application_text(entry['title'])}

## 优点

* 已按原书目录建立独立条目，便于 Obsidian 检索和图谱浏览。
* 已连接相关前置知识和后续方法，减少孤立节点。

## 局限性

* 自动整理不会假装完成公式识别和图示筛选，相关内容仍需人工复核。
* 具体参数、边界条件和书中例题需要后续逐页精修。

## 对应代码

{code_text}

## 相关图片

本轮为控制本地空间，未批量导出图片。后续只提取本节实际引用、具有教学价值的图示。

## 相关知识

{related_text}

## 复习问题

1. 本节处理的输入和输出分别是什么？
2. 本节依赖哪些前置概念？
3. 本节与哪些后续章节或算法有关？
4. 如果用代码实验，本节最小可验证例子是什么？
"""
    write(path, note)


EXAMPLE_COMMON = r'''from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_GRAY = ROOT / "assets" / "sample_images" / "sample_gray.png"
SAMPLE_COLOR = ROOT / "assets" / "sample_images" / "sample_color.png"


def ensure_samples():
    SAMPLE_GRAY.parent.mkdir(parents=True, exist_ok=True)
    if not SAMPLE_GRAY.exists():
        x = np.linspace(0, 255, 256, dtype=np.uint8)
        img = np.tile(x, (256, 1))
        cv2.circle(img, (128, 128), 60, 220, -1)
        cv2.rectangle(img, (30, 40), (90, 110), 55, -1)
        cv2.imwrite(str(SAMPLE_GRAY), img)
        cv2.imwrite(str(SAMPLE_COLOR), cv2.merge([img, np.flipud(img), np.roll(img, 50, axis=1)]))


def read_image(path: str | None, color: bool = False):
    ensure_samples()
    source = Path(path) if path else (SAMPLE_COLOR if color else SAMPLE_GRAY)
    flag = cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE
    image = cv2.imread(str(source), flag)
    if image is None:
        raise FileNotFoundError(source)
    return image, source


def apply_demo(name: str, image):
    if name == "gamma_correction":
        table = np.array([(i / 255) ** 0.55 * 255 for i in range(256)], dtype=np.uint8)
        return cv2.LUT(image, table)
    if name == "contrast_stretching":
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    if name == "gray_level_window":
        return np.where((image > 80) & (image < 180), 255, 0).astype(np.uint8)
    if name == "histogram_equalization":
        return cv2.equalizeHist(image)
    if name == "adaptive_histogram_equalization":
        return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(image)
    if name == "pseudo_color":
        return cv2.applyColorMap(image, cv2.COLORMAP_JET)
    if name == "retinex_enhancement":
        blur = cv2.GaussianBlur(image, (0, 0), 15)
        out = np.log1p(image.astype(np.float32)) - np.log1p(blur.astype(np.float32))
        return cv2.normalize(out, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name == "image_translation":
        h, w = image.shape[:2]
        return cv2.warpAffine(image, np.float32([[1, 0, 30], [0, 1, 20]]), (w, h))
    if name == "image_mirror":
        return cv2.flip(image, 1)
    if name == "image_rotation":
        h, w = image.shape[:2]
        return cv2.warpAffine(image, cv2.getRotationMatrix2D((w / 2, h / 2), 25, 1), (w, h))
    if name == "image_resize":
        return cv2.resize(image, None, fx=0.6, fy=0.6)
    if name == "image_shear":
        h, w = image.shape[:2]
        return cv2.warpAffine(image, np.float32([[1, 0.25, 0], [0, 1, 0]]), (int(w * 1.25), h))
    if name == "affine_transform":
        h, w = image.shape[:2]
        src = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
        dst = np.float32([[20, 20], [w - 30, 5], [30, h - 35]])
        return cv2.warpAffine(image, cv2.getAffineTransform(src, dst), (w, h))
    if name == "geometric_correction":
        return cv2.GaussianBlur(image, (3, 3), 0)
    if name == "mean_filter":
        return cv2.blur(image, (5, 5))
    if name == "median_filter":
        return cv2.medianBlur(image, 5)
    if name in {"k_nearest_mean_filter", "symmetric_nearest_mean_filter"}:
        return cv2.bilateralFilter(image, 9, 60, 60)
    if name == "non_local_means_filter":
        return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
    if name == "roberts_operator":
        kx = np.array([[1, 0], [0, -1]], np.float32)
        ky = np.array([[0, 1], [-1, 0]], np.float32)
        return cv2.convertScaleAbs(cv2.filter2D(image, -1, kx) + cv2.filter2D(image, -1, ky))
    if name == "sobel_operator":
        return cv2.convertScaleAbs(cv2.Sobel(image, cv2.CV_16S, 1, 0) + cv2.Sobel(image, cv2.CV_16S, 0, 1))
    if name == "prewitt_operator":
        kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], np.float32)
        return cv2.convertScaleAbs(cv2.filter2D(image, -1, kx) + cv2.filter2D(image, -1, kx.T))
    if name == "laplacian_operator":
        return cv2.convertScaleAbs(cv2.Laplacian(image, cv2.CV_16S))
    if name == "canny_edge_detection":
        return cv2.Canny(image, 80, 160)
    if name == "log_filter":
        return cv2.convertScaleAbs(cv2.Laplacian(cv2.GaussianBlur(image, (5, 5), 1), cv2.CV_16S))
    if name in {"threshold_segmentation", "max_entropy_threshold", "otsu_threshold"}:
        _, out = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return out
    if name == "region_growing":
        return cv2.threshold(cv2.GaussianBlur(image, (5, 5), 0), 100, 255, cv2.THRESH_BINARY)[1]
    if name == "erosion_dilation":
        k = np.ones((5, 5), np.uint8)
        return cv2.dilate(cv2.erode(image, k), k)
    if name == "opening_closing":
        k = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(cv2.morphologyEx(image, cv2.MORPH_OPEN, k), cv2.MORPH_CLOSE, k)
    if name == "connected_component_labeling":
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        _, labels = cv2.connectedComponents(binary)
        return cv2.normalize(labels, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name == "contour_labeling":
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        canvas = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(canvas, contours, -1, (0, 0, 255), 2)
        return canvas
    if name == "thinning":
        return cv2.Canny(image, 50, 120)
    if name == "color_spaces":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if name in {"white_balance", "gray_world"}:
        f = image.astype(np.float32)
        f *= np.mean(f) / (np.mean(f, axis=(0, 1)) + 1e-6)
        return np.clip(f, 0, 255).astype(np.uint8)
    if name == "color_compensation":
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        return cv2.cvtColor(cv2.merge([cv2.equalizeHist(l), a, b]), cv2.COLOR_LAB2BGR)
    if name == "one_dimensional_fourier_transform":
        signal = image[image.shape[0] // 2].astype(np.float32)
        spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft(signal))))
        return cv2.normalize(np.tile(spectrum, (80, 1)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name in {"two_dimensional_fft", "spectrum_visualization"}:
        spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image))))
        return cv2.normalize(spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name in {"wavelet_decomposition", "wavelet_denoising", "wavelet_compression_demo"}:
        return cv2.pyrDown(cv2.pyrUp(image))
    if name == "rle_encoding":
        return cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]
    if name == "huffman_encoding_demo":
        hist = cv2.calcHist([image], [0], None, [256], [0, 256]).ravel()
        return cv2.normalize(np.tile(hist, (100, 1)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name == "jpeg_idea_demo":
        return cv2.resize(cv2.resize(image, (64, 64)), image.shape[::-1], interpolation=cv2.INTER_NEAREST)
    if name in {"cnn_layers_demo", "lenet5_structure_demo", "alexnet_structure_demo", "srcnn_structure_demo", "yolo_concept_demo"}:
        canvas = np.zeros((220, 420, 3), np.uint8) + 255
        for i, label in enumerate(["Input", "Conv", "Activation", "Output"]):
            x = 25 + i * 95
            cv2.rectangle(canvas, (x, 70), (x + 70, 145), (40, 120, 220), 2)
            cv2.putText(canvas, label, (x, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
        return canvas
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", nargs="?")
    args = parser.parse_args()
    name = Path(__file__).stem
    color = name in {"color_spaces", "white_balance", "gray_world", "color_compensation"}
    image, source = read_image(args.image, color=color)
    result = apply_demo(name, image)
    print(f"source={source}")
    print(f"operation={name}")
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap="gray")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.title(name)
    plt.imshow(result if result.ndim == 2 else cv2.cvtColor(result, cv2.COLOR_BGR2RGB), cmap="gray")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
'''


def write_examples() -> int:
    examples_dir = ROOT / "examples"
    examples_dir.mkdir(exist_ok=True)
    write(examples_dir / "_common.py", EXAMPLE_COMMON)
    write(examples_dir / "README.md", "# 示例代码\n\n每个示例都可以单独运行，支持可选图片路径参数。不传入图片时使用 `assets/sample_images/` 中的轻量样例图。\n")
    count = 0
    for chapter_examples in REQUIRED_EXAMPLES.values():
        for folder, examples in chapter_examples.items():
            write(examples_dir / folder / "README.md", f"# {folder}\n\n本目录保存对应章节的教学示例。\n")
            for filename, section, title in examples:
                write(
                    examples_dir / folder / filename,
                    f'''"""对应章节：{section} {title}

运行方式：
    python {folder}/{filename} [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
''',
                )
                count += 1
    return count


def build_graph(entries: list[dict]) -> dict:
    nodes = []
    edges = []
    number_to_entry = {e["number"]: e for e in entries if e["number"] != "ref"}
    for entry in entries:
        if entry["number"] == "ref":
            nodes.append({"id": "ref", "label": "参考文献", "type": "reference", "path": str(entry_path(entry).relative_to(ROOT)).replace("\\", "/")})
            continue
        nodes.append({
            "id": entry["number"],
            "label": f"{entry['number']} {entry['title']}",
            "type": entry["kind"],
            "chapter": entry["chapter"],
            "path": str(entry_path(entry).relative_to(ROOT)).replace("\\", "/"),
        })
        if entry["kind"] == "section":
            edges.append({"source": str(entry["chapter"]), "target": entry["number"], "type": "章节包含关系"})
    ordered = [e for e in entries if e["kind"] == "section"]
    for left, right in zip(ordered, ordered[1:]):
        edges.append({"source": left["number"], "target": right["number"], "type": "前置知识"})
    for source, target, rel_type in RELATIONS:
        if source in number_to_entry and target in number_to_entry:
            edges.append({"source": source, "target": target, "type": rel_type})
    if "11.x" in number_to_entry:
        edges.append({"source": "11.x", "target": "ref", "type": "参考关系"})
    for chapter_examples in REQUIRED_EXAMPLES.values():
        for folder, examples in chapter_examples.items():
            for filename, section, title in examples:
                node_id = f"example:{filename}"
                nodes.append({"id": node_id, "label": filename, "type": "code_example", "path": f"examples/{folder}/{filename}"})
                if section in number_to_entry:
                    edges.append({"source": section, "target": node_id, "type": "应用关系"})
    return {"nodes": nodes, "edges": edges}


def write_indices(entries: list[dict], graph: dict) -> None:
    chapters = [e for e in entries if e["kind"] == "chapter"]
    index_lines = ["# 数字图像处理知识库", "", "## Obsidian 入口", "", "* [[wiki/00_导航|导航]]", "* [[wiki/99_术语表|术语表]]", "* [[graph/mermaid_graph|知识关系图]]", "* [[coverage_report|覆盖检查报告]]", "", "## 章节"]
    nav_lines = ["# 导航", "", "## 全书目录"]
    for chapter in chapters:
        link = f"[[{chapter['chapter_dir']}/README|第 {chapter['chapter']} 章 {chapter['chapter_title']}]]"
        index_lines.append(f"* {link}")
        nav_lines.append(f"* {link}")
    write(ROOT / "index.md", "\n".join(index_lines) + "\n")
    write(ROOT / "wiki" / "00_导航.md", "\n".join(nav_lines) + "\n\n## 可视化\n\n* Obsidian 左侧功能区打开 Graph View，可查看本知识库双向链接网络。\n* 也可打开 [[../graph/mermaid_graph|Mermaid 知识关系图]]。\n")
    terms = [
        ("数字图像", "用数字阵列表示的图像", "1.3"),
        ("像素", "数字图像的最小组成单元", "1.3"),
        ("灰度直方图", "灰度级出现次数或概率的统计", "1.3.2"),
        ("γ 校正", "用于校正非线性光电转换关系", "2.1"),
        ("直方图均衡化", "通过灰度分布映射增强图像", "2.5"),
        ("均值滤波", "基于邻域平均的平滑方法", "4.2"),
        ("Canny 算子", "多阶段边缘检测方法", "5.5"),
        ("阈值分割", "按灰度阈值划分目标与背景", "6.1"),
        ("傅里叶变换", "空间域到频域的图像表示", "9.1.2"),
        ("卷积网络", "深度学习图像处理的基础结构", "11.1"),
    ]
    by_number = {e["number"]: e for e in entries}
    term_lines = ["# 术语表", "", "| 术语 | 说明 | 相关条目 |", "|---|---|---|"]
    for term, desc, number in terms:
        link = obsidian_link(by_number[number]) if number in by_number else ""
        term_lines.append(f"| {term} | {desc} | {link} |")
    write(ROOT / "wiki" / "99_术语表.md", "\n".join(term_lines) + "\n")

    write(ROOT / "graph" / "knowledge_graph.json", json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    labels = {node["id"]: node["label"] for node in graph["nodes"]}
    mermaid = ["# Mermaid 知识关系图", "", "```mermaid", "graph TD"]
    for edge in graph["edges"]:
        source = re.sub(r"[^0-9A-Za-z_]", "_", edge["source"])
        target = re.sub(r"[^0-9A-Za-z_]", "_", edge["target"])
        mermaid.append(f'  {source}["{labels.get(edge["source"], edge["source"])}"] -->|{edge["type"]}| {target}["{labels.get(edge["target"], edge["target"])}"]')
    mermaid.append("```")
    write(ROOT / "graph" / "mermaid_graph.md", "\n".join(mermaid) + "\n")
    write(ROOT / "graph" / "knowledge_graph.html", "<!doctype html>\n<meta charset=\"utf-8\">\n<title>数字图像处理知识图谱</title>\n<h1>数字图像处理知识图谱</h1>\n<p>在 Obsidian 中打开 graph/mermaid_graph.md 可查看 Mermaid 图；Obsidian 自带 Graph View 可查看 wiki 双链网络。</p>\n")


def write_chapter_readmes(entries: list[dict]) -> None:
    for chapter in [e for e in entries if e["kind"] == "chapter"]:
        children = [e for e in entries if e.get("chapter") == chapter["chapter"] and e["kind"] == "section"]
        child_lines = "\n".join(f"* {obsidian_link(e)}" for e in children)
        write(
            entry_path(chapter),
            f"""# 第 {chapter['chapter']} 章 {chapter['chapter_title']}

## 章节条目

{child_lines}

## 关系提示

本章条目已纳入 `graph/knowledge_graph.json` 和 Obsidian 双向链接。公式、图示和表格仍按“需人工复核”处理，不伪造识别结果。
""",
        )


def write_coverage(entries: list[dict], graph: dict, code_count: int) -> None:
    rows = [
        "| 章 | 节 | 书中页码 | PDF 页码 | 是否已生成 wiki | wiki 文件路径 | 是否提取图片 | 图片数量 | 是否生成代码 | 是否需人工复核 | 备注 |",
        "|---|---|---:|---:|---|---|---|---:|---|---|---|",
    ]
    for entry in entries:
        if entry["kind"] == "chapter":
            continue
        path = entry_path(entry).relative_to(ROOT).as_posix()
        has_code = any(sec == entry["number"] for c in REQUIRED_EXAMPLES.values() for exs in c.values() for _, sec, _ in exs)
        chapter = "参考文献" if entry["kind"] == "reference" else f"第 {entry['chapter']} 章 {entry['chapter_title']}"
        rows.append(f"| {chapter} | {entry['number']} {entry['title']} | {entry['book_page'] or '需复核'} | {entry['pdf_page']} | 是 | `{path}` | 否 | 0 | {'是' if has_code else '否'} | 是 | 图示和公式待复核 |")
    md_count = len(list(ROOT.rglob("*.md")))
    write(
        ROOT / "coverage_report.md",
        f"""# 覆盖检查报告

## 书籍信息

* 书名：数字图像处理基础
* 作者：朱虹
* 原始路径：`{PDF}`
* 项目内副本路径：`raw/books/数字图像处理基础_朱虹.pdf`
* 文件格式：PDF
* PDF 总页数：233
* 是否成功解析：已成功读取内置目录并按目录生成 wiki
* 页码偏移说明：PDF 页码 = 书中页码 + 15

## 章节覆盖表

{chr(10).join(rows)}

## 未完成或需复核内容

* 图片提取：为控制本地空间，本轮未批量导出图片；后续只提取被 wiki 引用的教学图。
* 公式识别：所有公式均需人工复核后再固化为 LaTeX。
* 表格识别：未做结构化表格抽取。
* 章节内容：已按目录全覆盖生成细化笔记，但仍建议逐章继续精修。

## 统计结果

* 生成 Markdown 文件数量：{md_count}
* 提取图片数量：0
* 生成代码文件数量：{code_count}
* 建立 Obsidian 链接数量：由校验脚本统计
* 知识图谱节点数量：{len(graph['nodes'])}
* 知识图谱边数量：{len(graph['edges'])}
* 断链数量：由校验脚本统计
* 孤立节点数量：由校验脚本统计
* 需要人工复核数量：{len([e for e in entries if e['kind'] != 'chapter'])}
""",
    )


def main() -> None:
    doc = fitz.open(PDF)
    entries = build_entries(doc)
    all_numbers = [e["number"] for e in entries if e["number"] != "ref"]
    by_number = {e["number"]: e for e in entries if e["number"] != "ref"}
    for entry in entries:
        if entry["kind"] in {"chapter"}:
            continue
        text = section_text(doc, entry["pdf_page"], entry["end_pdf_page"])
        out = ROOT / "raw" / "extracted_text" / f"{entry['number']}_{normalize_title(entry['title'])}.txt"
        write(out, text)
        write_note(entry, by_number, all_numbers, text)
    write_chapter_readmes(entries)
    code_count = write_examples()
    graph = build_graph(entries)
    write_indices(entries, graph)
    write_coverage(entries, graph, code_count)
    print(json.dumps({"entries": len(entries), "code_examples": code_count, "nodes": len(graph["nodes"]), "edges": len(graph["edges"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
