"""Generate original teaching figures for chapter 8 color image processing."""

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


def color_formation() -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_title("RGB additive color formation")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)
    ax.axis("off")
    circles = [(2.4, 2.7, "#ef4444", "R"), (3.6, 2.7, "#22c55e", "G"), (3.0, 1.8, "#3b82f6", "B")]
    for x, y, color, label in circles:
        ax.add_patch(plt.Circle((x, y), 1.05, color=color, alpha=0.45))
        ax.text(x, y, label, ha="center", va="center", fontsize=16)
    ax.text(3, 0.45, "Different channel mixtures produce perceived color", ha="center")
    save(fig, "ch08_color_formation.png")


def color_spaces() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))
    labels = [("RGB", "device channels"), ("HSV", "hue + saturation + value"), ("Lab", "lightness + opponent colors")]
    colors = ["#ef4444", "#f59e0b", "#6366f1"]
    for ax, (title, subtitle), color in zip(axes, labels, colors):
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0.15, 0.25), 0.7, 0.45, fill=False, linewidth=2, color=color))
        ax.text(0.5, 0.55, title, ha="center", va="center", fontsize=15)
        ax.text(0.5, 0.32, subtitle, ha="center", va="center", fontsize=9)
    save(fig, "ch08_color_spaces.png")


def white_balance() -> None:
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    channels = ["B", "G", "R"]
    before = [1.35, 1.0, 0.72]
    after = [1.0, 1.0, 1.0]
    x = np.arange(3)
    ax.bar(x - 0.18, before, width=0.34, label="before", color="#93c5fd")
    ax.bar(x + 0.18, after, width=0.34, label="after", color="#34d399")
    ax.set_xticks(x, channels)
    ax.set_title("White balance equalizes neutral channel responses")
    ax.set_ylabel("relative gain")
    ax.legend()
    save(fig, "ch08_white_balance.png")


def gray_world() -> None:
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.set_title("Gray world assumption")
    ax.plot([0, 1], [0.2, 0.8], color="#64748b")
    ax.scatter([0.2, 0.48, 0.78], [0.65, 0.5, 0.28], s=90, c=["#60a5fa", "#9ca3af", "#f87171"])
    ax.text(0.5, 0.12, "average scene color should be neutral gray", ha="center")
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, "ch08_gray_world.png")


def color_compensation() -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    ax.set_title("Color compensation applies channel gains")
    gains = [0.95, 1.00, 1.08]
    ax.bar(["B gain", "G gain", "R gain"], gains, color=["#3b82f6", "#22c55e", "#ef4444"])
    ax.axhline(1.0, color="#111827", linewidth=1)
    ax.set_ylim(0.8, 1.2)
    save(fig, "ch08_color_compensation.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 8 章原创教学示意图" in previous:
        previous = previous.split("## 第 8 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 8 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch08_color_formation.png` | 8.1 彩色的形成原理与基本概念 | 展示 RGB 加色成色思想 | 是 | `8.1_彩色的形成原理与基本概念.md` |
| `ch08_color_spaces.png` | 8.2 表色系 | 对比 RGB、HSV、Lab 的表达侧重点 | 是 | `8.2_表色系.md`, `8.2.1_计算颜色模型系统.md`, `8.2.2_视觉颜色模型系统.md`, `8.2.3_工业颜色模型系统.md` |
| `ch08_white_balance.png` | 8.3.1 白平衡法 | 展示中性参考的通道增益校正 | 是 | `8.3_色彩平衡.md`, `8.3.1_白平衡法.md` |
| `ch08_gray_world.png` | 8.3.2 灰色世界法 | 展示平均颜色趋向中性灰的假设 | 是 | `8.3.2_灰色世界法.md` |
| `ch08_color_compensation.png` | 8.4 彩色补偿 | 展示手动通道增益补偿 | 是 | `8.4_彩色补偿.md`, `8.x_习题.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    color_formation()
    color_spaces()
    white_balance()
    gray_world()
    color_compensation()
    update_readme()
    print({"figures": 5, "output": str(OUT)})


if __name__ == "__main__":
    main()
