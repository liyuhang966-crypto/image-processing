"""Generate original teaching figures for chapter 7 binary image processing."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "extracted_figures"


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160)
    plt.close(fig)


def connectivity() -> None:
    grid = np.zeros((5, 5))
    grid[2, 2] = 1
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(grid, cmap="Greys", vmin=0, vmax=1)
    for y in range(5):
        for x in range(5):
            label = "P" if (x, y) == (2, 2) else ""
            ax.text(x, y, label, ha="center", va="center", color="#dc2626", fontsize=14)
    for x, y in [(2, 1), (3, 2), (2, 3), (1, 2)]:
        ax.text(x, y, "4", ha="center", va="center", color="#2563eb")
    for x, y in [(1, 1), (3, 1), (1, 3), (3, 3)]:
        ax.text(x, y, "8", ha="center", va="center", color="#16a34a")
    ax.set_title("4-neighborhood and 8-neighborhood")
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, "ch07_connectivity.png")


def morphology_erosion_dilation() -> None:
    base = np.zeros((9, 9))
    base[2:7, 2:7] = 1
    eroded = np.zeros_like(base)
    eroded[3:6, 3:6] = 1
    dilated = np.zeros_like(base)
    dilated[1:8, 1:8] = 1
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.5))
    for ax, data, title in zip(axes, [base, eroded, dilated], ["original", "erosion", "dilation"]):
        ax.imshow(data, cmap="gray_r")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "ch07_morphology_erosion_dilation.png")


def opening_closing() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.8))
    for ax, title, note in zip(axes, ["Opening", "Closing"], ["removes small foreground noise", "fills small holes / gaps"]):
        ax.axis("off")
        ax.set_title(title)
        ax.text(0.5, 0.65, "erosion -> dilation" if title == "Opening" else "dilation -> erosion", ha="center", fontsize=12)
        ax.text(0.5, 0.35, note, ha="center", color="#2563eb")
    save(fig, "ch07_opening_closing.png")


def component_labeling() -> None:
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ax.set_title("Connected components receive separate labels")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    shapes = [plt.Circle((2.2, 5.2), 1.0, color="#60a5fa"), plt.Rectangle((5.2, 4.4), 2.0, 1.7, color="#34d399"), plt.Circle((6.5, 2.0), 0.9, color="#f59e0b")]
    for i, shape in enumerate(shapes, 1):
        ax.add_patch(shape)
        ax.text(shape.get_center()[0] if hasattr(shape, "get_center") else 6.2, shape.get_center()[1] if hasattr(shape, "get_center") else 5.2, str(i), ha="center", va="center", fontsize=14)
    ax.axis("off")
    save(fig, "ch07_component_labeling.png")


def thinning() -> None:
    x = np.linspace(0, 1, 100)
    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    ax.plot(x, 0.5 + 0.22 * np.sin(2 * np.pi * x), linewidth=14, color="#93c5fd", label="thick stroke")
    ax.plot(x, 0.5 + 0.22 * np.sin(2 * np.pi * x), linewidth=2.5, color="#dc2626", label="skeleton")
    ax.set_title("Thinning preserves topology while reducing width")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend()
    save(fig, "ch07_thinning.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 7 章原创教学示意图" in previous:
        previous = previous.split("## 第 7 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 7 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch07_connectivity.png` | 7.1 基本概念 | 展示 4 邻域和 8 邻域 | 是 | `7.1_二值图像中的基本概念.md`, `7.1.1_连接与点特性.md` |
| `ch07_morphology_erosion_dilation.png` | 7.2 腐蚀与膨胀 | 展示目标收缩和扩张 | 是 | `7.2_腐蚀与膨胀.md`, `7.2.1_腐蚀.md`, `7.2.2_膨胀.md` |
| `ch07_opening_closing.png` | 7.3 开运算与闭运算 | 展示组合形态学顺序和作用 | 是 | `7.3_开运算与闭运算.md`, `7.3.1_开运算.md`, `7.3.2_闭运算.md` |
| `ch07_component_labeling.png` | 7.4 贴标签 | 展示不同连通区域的标签 | 是 | `7.4_贴标签.md`, `7.4.1_连通域标签法.md`, `7.4.2_轮廓标签法.md` |
| `ch07_thinning.png` | 7.5 细线化方法 | 展示粗笔画到骨架的变化 | 是 | `7.5_细线化方法.md`, `7.x_习题.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    connectivity()
    morphology_erosion_dilation()
    opening_closing()
    component_labeling()
    thinning()
    update_readme()
    print({"figures": 5, "output": str(OUT)})


if __name__ == "__main__":
    main()
