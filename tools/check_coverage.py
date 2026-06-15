"""Coverage checks for chapter 2 and chapter 3 refinement quality."""

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
    errors.extend(check_required_files(ROOT / "assets" / "extracted_figures", REQUIRED_CHAPTER3_FIGURES, "chapter 3 figure"))
    errors.extend(check_required_files(ROOT / "examples" / "03_geometric_transform", REQUIRED_CHAPTER3_CODE, "chapter 3 code"))
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
