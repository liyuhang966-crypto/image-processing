"""Generate original teaching figures for chapter 3 geometric transforms."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "extracted_figures"


def setup_axis(ax, title: str) -> None:
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 7)
    ax.grid(True, color="#d6d3ca", linewidth=0.8)
    ax.set_xticks(range(0, 7))
    ax.set_yticks(range(0, 7))


def square_points() -> np.ndarray:
    return np.array([[1, 1], [4, 1], [4, 4], [1, 4], [1, 1]], dtype=float)


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160)
    plt.close(fig)


def translation_grid() -> None:
    pts = square_points()
    shifted = pts + np.array([1.5, 1.0])
    fig, ax = plt.subplots(figsize=(5, 4))
    setup_axis(ax, "Translation: (x, y) -> (x+dx, y+dy)")
    ax.plot(pts[:, 0], pts[:, 1], "o-", label="original", color="#2563eb")
    ax.plot(shifted[:, 0], shifted[:, 1], "o-", label="translated", color="#dc2626")
    ax.arrow(4.2, 4.2, 1.2, 0.8, head_width=0.18, color="#111827")
    ax.legend()
    save(fig, "ch03_translation_grid.png")


def mirror_transform() -> None:
    pts = square_points() + np.array([0.5, 0])
    mirrored = np.column_stack([6 - pts[:, 0], pts[:, 1]])
    fig, ax = plt.subplots(figsize=(5, 4))
    setup_axis(ax, "Mirror transform around vertical axis")
    ax.axvline(3, color="#111827", linestyle="--", label="mirror axis")
    ax.plot(pts[:, 0], pts[:, 1], "o-", label="original", color="#2563eb")
    ax.plot(mirrored[:, 0], mirrored[:, 1], "o-", label="mirrored", color="#16a34a")
    ax.legend()
    save(fig, "ch03_mirror_transform.png")


def rotation_center() -> None:
    pts = square_points()
    center = np.array([2.5, 2.5])
    theta = np.deg2rad(35)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotated = (pts - center) @ rot.T + center
    fig, ax = plt.subplots(figsize=(5, 4))
    setup_axis(ax, "Rotation around image center")
    ax.plot(pts[:, 0], pts[:, 1], "o-", label="original", color="#2563eb")
    ax.plot(rotated[:, 0], rotated[:, 1], "o-", label="rotated", color="#dc2626")
    ax.scatter([center[0]], [center[1]], color="#111827", s=50, label="center")
    ax.legend()
    save(fig, "ch03_rotation_center.png")


def resize_interpolation() -> None:
    x = np.arange(6)
    y = np.array([1, 1, 4, 4, 2, 2], dtype=float)
    xq = np.linspace(0, 5, 60)
    yq = np.interp(xq, x, y)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.set_title("Resize needs resampling")
    ax.plot(x, y, "o", label="known pixels", color="#2563eb")
    ax.step(x, y, where="mid", label="nearest", color="#dc2626", alpha=0.75)
    ax.plot(xq, yq, label="linear", color="#16a34a")
    ax.set_xlabel("source coordinate")
    ax.set_ylabel("gray value")
    ax.grid(True, color="#d6d3ca")
    ax.legend()
    save(fig, "ch03_resize_interpolation.png")


def shear_transform() -> None:
    pts = square_points()
    shear = np.array([[1, 0.45], [0, 1]])
    sheared = pts @ shear.T
    fig, ax = plt.subplots(figsize=(5, 4))
    setup_axis(ax, "Shear transform")
    ax.plot(pts[:, 0], pts[:, 1], "o-", label="original", color="#2563eb")
    ax.plot(sheared[:, 0], sheared[:, 1], "o-", label="sheared", color="#f59e0b")
    ax.legend()
    save(fig, "ch03_shear_transform.png")


def affine_transform() -> None:
    pts = square_points()
    matrix = np.array([[0.85, -0.28], [0.35, 0.95]])
    transformed = pts @ matrix.T + np.array([1.0, 0.2])
    fig, ax = plt.subplots(figsize=(5, 4))
    setup_axis(ax, "Affine = linear transform + translation")
    ax.plot(pts[:, 0], pts[:, 1], "o-", label="original", color="#2563eb")
    ax.plot(transformed[:, 0], transformed[:, 1], "o-", label="affine", color="#7c3aed")
    ax.legend()
    save(fig, "ch03_affine_transform.png")


def geometric_correction() -> None:
    t = np.linspace(0, 2 * np.pi, 200)
    r = 2.0 * (1 + 0.18 * np.cos(4 * t))
    distorted_x = 3 + r * np.cos(t)
    distorted_y = 3 + r * np.sin(t)
    corrected_x = 3 + 2 * np.cos(t)
    corrected_y = 3 + 2 * np.sin(t)
    fig, ax = plt.subplots(figsize=(5, 4))
    setup_axis(ax, "Geometric correction maps distorted coordinates back")
    ax.plot(distorted_x, distorted_y, label="distorted grid cue", color="#dc2626")
    ax.plot(corrected_x, corrected_y, label="corrected target", color="#16a34a")
    ax.legend()
    save(fig, "ch03_geometric_correction.png")


def update_readme() -> None:
    readme = OUT / "README.md"
    previous = readme.read_text(encoding="utf-8") if readme.exists() else ""
    chapter3 = """\n## 第 3 章原创教学示意图\n\n这些图片为本仓库重新绘制的原创教学图，不是原书截图。\n\n| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |\n|---|---|---|---|---|\n| `ch03_translation_grid.png` | 3.1.1 图像的平移 | 展示坐标整体偏移 | 是 | `3.1_图像的位置变换.md`, `3.1.1_图像的平移.md` |\n| `ch03_mirror_transform.png` | 3.1.2 图像的镜像 | 展示镜像轴和左右翻转 | 是 | `3.1.2_图像的镜像.md` |\n| `ch03_rotation_center.png` | 3.1.3 图像的旋转 | 展示旋转中心和旋转后位置 | 是 | `3.1.3_图像的旋转.md` |\n| `ch03_resize_interpolation.png` | 3.2.1/3.2.2 缩小与放大 | 对比最近邻和线性插值 | 是 | `3.2_图像的形状变换.md`, `3.2.1_图像的缩小.md`, `3.2.2_图像的放大.md` |\n| `ch03_shear_transform.png` | 3.2.3 图像的错切 | 展示错切造成的倾斜 | 是 | `3.2.3_图像的错切.md` |\n| `ch03_affine_transform.png` | 3.3 齐次坐标与仿射变换 | 展示仿射组合变换 | 是 | `3.3_齐次坐标与图像的仿射变换.md` |\n| `ch03_geometric_correction.png` | 3.4 图像几何畸变校正 | 展示畸变到校正的坐标映射 | 是 | `3.4_图像几何畸变的校正.md` |\n"""
    if "## 第 3 章原创教学示意图" in previous:
        previous = previous.split("## 第 3 章原创教学示意图", 1)[0].rstrip() + "\n"
    readme.write_text(previous.rstrip() + "\n" + chapter3.lstrip(), encoding="utf-8")


def main() -> None:
    translation_grid()
    mirror_transform()
    rotation_center()
    resize_interpolation()
    shear_transform()
    affine_transform()
    geometric_correction()
    update_readme()
    print({"figures": 7, "output": str(OUT)})


if __name__ == "__main__":
    main()
