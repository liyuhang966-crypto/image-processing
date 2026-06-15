"""Generate original teaching figures for chapter 4 image denoising."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "extracted_figures"


def synthetic_image(size: int = 96) -> np.ndarray:
    y, x = np.indices((size, size))
    image = (80 + 120 * ((x > 22) & (x < 74) & (y > 22) & (y < 74))).astype(float)
    image += 40 * np.exp(-((x - 48) ** 2 + (y - 48) ** 2) / 500)
    return np.clip(image, 0, 255).astype(float)


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160)
    plt.close(fig)


def noise_models() -> None:
    image = synthetic_image()
    rng = np.random.default_rng(4)
    gaussian = np.clip(image + rng.normal(0, 22, image.shape), 0, 255)
    sp = image.copy()
    mask = rng.random(image.shape)
    sp[mask < 0.03] = 0
    sp[mask > 0.97] = 255
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.6))
    for ax, data, title in zip(axes, [image, gaussian, sp], ["clean", "Gaussian noise", "salt-pepper noise"]):
        ax.imshow(data, cmap="gray", vmin=0, vmax=255)
        ax.set_title(title)
        ax.axis("off")
    save(fig, "ch04_noise_models.png")


def mean_filter_kernel() -> None:
    kernel = np.ones((5, 5)) / 25
    fig, ax = plt.subplots(figsize=(4, 3.6))
    im = ax.imshow(kernel, cmap="Blues")
    for (y, x), value in np.ndenumerate(kernel):
        ax.text(x, y, f"{value:.2f}", ha="center", va="center", color="#111827")
    ax.set_title("Mean filter: equal weights")
    ax.set_xticks([])
    ax.set_yticks([])
    fig.colorbar(im, ax=ax, fraction=0.046)
    save(fig, "ch04_mean_filter_kernel.png")


def median_filter_window() -> None:
    patch = np.array([[52, 54, 250], [55, 58, 57], [0, 60, 61]])
    fig, ax = plt.subplots(figsize=(4, 3.6))
    ax.imshow(patch, cmap="gray", vmin=0, vmax=255)
    for (y, x), value in np.ndenumerate(patch):
        ax.text(x, y, str(value), ha="center", va="center", color="#ef4444" if value in {0, 250} else "#ffffff")
    ax.set_title("Median suppresses impulse outliers")
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, "ch04_median_filter_window.png")


def edge_preserving_filters() -> None:
    x = np.linspace(0, 1, 160)
    clean = (x > 0.5).astype(float)
    rng = np.random.default_rng(8)
    noisy = np.clip(clean + rng.normal(0, 0.18, x.shape), 0, 1)
    mean = np.convolve(noisy, np.ones(11) / 11, mode="same")
    bilateral_like = noisy.copy()
    bilateral_like[x < 0.48] = np.convolve(noisy[x < 0.48], np.ones(9) / 9, mode="same")
    bilateral_like[x > 0.52] = np.convolve(noisy[x > 0.52], np.ones(9) / 9, mode="same")
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(x, noisy, color="#94a3b8", label="noisy")
    ax.plot(x, mean, color="#dc2626", label="mean blur")
    ax.plot(x, bilateral_like, color="#16a34a", label="edge-preserving idea")
    ax.set_title("Edge preserving filters avoid averaging across edges")
    ax.set_xlabel("position")
    ax.set_ylabel("intensity")
    ax.grid(True, color="#d6d3ca")
    ax.legend()
    save(fig, "ch04_edge_preserving_filters.png")


def non_local_means() -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_title("Non-local means: similar patches vote together")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.grid(True, color="#e5e7eb")
    patches = [(2, 5), (6, 5.5), (7.2, 2.2), (2.5, 2), (4.5, 3.7)]
    for i, (x, y) in enumerate(patches):
        color = "#2563eb" if i == 0 else "#16a34a"
        rect = plt.Rectangle((x, y), 1.2, 1.2, fill=False, linewidth=2, color=color)
        ax.add_patch(rect)
        if i > 0:
            ax.annotate("", xy=(x + 0.6, y + 0.6), xytext=(2.6, 5.6), arrowprops=dict(arrowstyle="->", color="#64748b"))
    ax.text(1.8, 6.4, "reference patch", color="#2563eb")
    ax.text(5.6, 6.6, "similar patches", color="#16a34a")
    save(fig, "ch04_non_local_means.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 4 章原创教学示意图" in previous:
        previous = previous.split("## 第 4 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """\n## 第 4 章原创教学示意图\n\n这些图片为本仓库重新绘制的原创教学图，不是原书截图。\n\n| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |\n|---|---|---|---|---|\n| `ch04_noise_models.png` | 4.1 图像噪声 | 对比干净图、高斯噪声、椒盐噪声 | 是 | `4.1_图像噪声.md` |\n| `ch04_mean_filter_kernel.png` | 4.2 均值滤波 | 展示均值滤波核权重 | 是 | `4.2_均值滤波.md`, `4.2.1_均值滤波的原理.md`, `4.2.2_均值滤波方法.md` |\n| `ch04_median_filter_window.png` | 4.3 中值滤波 | 展示中值抑制脉冲噪声 | 是 | `4.3_中值滤波.md`, `4.3.1_中值滤波的原理.md`, `4.3.2_中值滤波方法.md` |\n| `ch04_edge_preserving_filters.png` | 4.4 边界保持类平滑滤波 | 对比跨边界平均和边界保持思想 | 是 | `4.4_边界保持类平滑滤波.md`, `4.4.1_K近邻均值滤波.md`, `4.4.2_对称近邻均值滤波.md` |\n| `ch04_non_local_means.png` | 4.5 非局部均值滤波 | 展示相似块加权平均 | 是 | `4.5_非局部均值滤波.md` |\n"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    noise_models()
    mean_filter_kernel()
    median_filter_window()
    edge_preserving_filters()
    non_local_means()
    update_readme()
    print({"figures": 5, "output": str(OUT)})


if __name__ == "__main__":
    main()
