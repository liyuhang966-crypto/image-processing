"""Generate original teaching figures for chapter 6 image segmentation."""

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


def threshold_histogram() -> None:
    rng = np.random.default_rng(6)
    bg = rng.normal(60, 12, 3000)
    fg = rng.normal(170, 18, 1800)
    values = np.clip(np.concatenate([bg, fg]), 0, 255)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.hist(values, bins=48, color="#60a5fa", edgecolor="#1e3a8a")
    ax.axvline(115, color="#dc2626", linewidth=2, label="threshold T")
    ax.set_title("Global threshold separates histogram modes")
    ax.set_xlabel("gray value")
    ax.set_ylabel("count")
    ax.legend()
    save(fig, "ch06_threshold_histogram.png")


def p_parameter() -> None:
    x = np.arange(256)
    hist = np.exp(-((x - 55) ** 2) / 500) + 0.65 * np.exp(-((x - 170) ** 2) / 900)
    cdf = np.cumsum(hist) / np.sum(hist)
    p = 0.72
    threshold = int(np.searchsorted(cdf, p))
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(x, cdf, label="cumulative probability")
    ax.axhline(p, color="#16a34a", linestyle="--", label=f"p={p}")
    ax.axvline(threshold, color="#dc2626", label=f"T={threshold}")
    ax.set_title("p-parameter threshold from cumulative histogram")
    ax.set_xlabel("gray value")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch06_p_parameter_threshold.png")


def max_entropy() -> None:
    x = np.arange(256)
    score = 3.2 - ((x - 118) ** 2) / 4500 + 0.12 * np.sin(x / 13)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(x, score, color="#7c3aed")
    best = int(x[np.argmax(score)])
    ax.axvline(best, color="#dc2626", label=f"max entropy T={best}")
    ax.set_title("Maximum entropy picks threshold with richest two-class information")
    ax.set_xlabel("threshold")
    ax.set_ylabel("entropy score")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch06_max_entropy_threshold.png")


def otsu_variance() -> None:
    x = np.arange(256)
    between = np.exp(-((x - 122) ** 2) / 1200)
    within = 1.0 - 0.75 * between
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(x, between, label="between-class variance")
    ax.plot(x, within, label="within-class variance")
    ax.axvline(122, color="#dc2626", label="Otsu threshold")
    ax.set_title("Otsu maximizes between-class variance")
    ax.set_xlabel("threshold")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch06_otsu_variance.png")


def region_growing() -> None:
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.set_title("Region growing expands from a seed")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.grid(True, color="#e5e7eb")
    circle = plt.Circle((4.5, 4), 2.1, fill=False, linewidth=2.5, color="#2563eb")
    ax.add_patch(circle)
    ax.scatter([4.5], [4], color="#dc2626", s=70, label="seed")
    for angle in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        ax.annotate("", xy=(4.5 + 1.7 * np.cos(angle), 4 + 1.7 * np.sin(angle)), xytext=(4.5, 4), arrowprops=dict(arrowstyle="->", color="#16a34a"))
    ax.text(5.5, 6.5, "similar gray values join", color="#16a34a")
    ax.legend(loc="lower left")
    save(fig, "ch06_region_growing.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 6 章原创教学示意图" in previous:
        previous = previous.split("## 第 6 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 6 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch06_threshold_histogram.png` | 6.1 阈值分割方法 | 展示直方图双峰和阈值分割思想 | 是 | `6.1_阈值分割方法.md` |
| `ch06_p_parameter_threshold.png` | 6.1.1 p-参数法 | 展示由累计概率确定阈值 | 是 | `6.1.1_p-参数法.md` |
| `ch06_max_entropy_threshold.png` | 6.1.2 最大熵方法 | 展示熵准则随阈值变化 | 是 | `6.1.2_最大熵方法.md` |
| `ch06_otsu_variance.png` | 6.1.3 最大类间、类内方差比法 | 展示 Otsu 类间方差最大化 | 是 | `6.1.3_最大类间、类内方差比法.md` |
| `ch06_region_growing.png` | 6.2 区域生长分割方法 | 展示从种子点按相似性扩张 | 是 | `6.2_区域生长分割方法.md`, `6.x_习题.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    threshold_histogram()
    p_parameter()
    max_entropy()
    otsu_variance()
    region_growing()
    update_readme()
    print({"figures": 5, "output": str(OUT)})


if __name__ == "__main__":
    main()
