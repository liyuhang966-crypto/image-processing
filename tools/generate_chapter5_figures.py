"""Generate original teaching figures for chapter 5 image sharpening."""

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


def detail_profiles() -> None:
    x = np.linspace(0, 1, 240)
    ramp = x
    step = (x > 0.45).astype(float)
    line = np.zeros_like(x)
    line[(x > 0.48) & (x < 0.52)] = 1
    point = np.exp(-((x - 0.5) ** 2) / 0.00035)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.plot(x, ramp, label="slow gray change")
    ax.plot(x, step, label="edge / step")
    ax.plot(x, line, label="thin line")
    ax.plot(x, point, label="point detail")
    ax.set_title("Image details as gray-level changes")
    ax.set_xlabel("position")
    ax.set_ylabel("gray value")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch05_detail_profiles.png")


def first_derivative_kernels() -> None:
    kernels = {
        "Roberts x": np.array([[1, 0], [0, -1]]),
        "Prewitt x": np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
        "Sobel x": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
    }
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))
    for ax, (title, kernel) in zip(axes, kernels.items()):
        ax.imshow(kernel, cmap="coolwarm", vmin=-2, vmax=2)
        for (y, x), value in np.ndenumerate(kernel):
            ax.text(x, y, str(value), ha="center", va="center", color="#111827")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "ch05_first_derivative_kernels.png")


def operator_comparison() -> None:
    x = np.linspace(0, 1, 160)
    signal = (x > 0.5).astype(float)
    roberts = np.abs(np.diff(signal, prepend=signal[0]))
    prewitt = np.convolve(signal, [-1, 0, 1], mode="same")
    sobel = np.convolve(signal, [-1, 0, 1], mode="same")
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.plot(x, signal, color="#111827", label="gray step")
    ax.plot(x, roberts, label="Roberts response")
    ax.plot(x, np.abs(prewitt), label="Prewitt response")
    ax.plot(x, np.abs(sobel), "--", label="Sobel response")
    ax.set_title("First derivative operators respond at gray transitions")
    ax.set_xlabel("position")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch05_roberts_sobel_prewitt.png")


def laplacian_sharpening() -> None:
    x = np.linspace(0, 1, 180)
    signal = 0.25 + 0.5 * (x > 0.5).astype(float)
    lap = np.convolve(signal, [1, -2, 1], mode="same")
    sharpened = np.clip(signal - 0.8 * lap, 0, 1)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.plot(x, signal, label="original profile")
    ax.plot(x, lap, label="second derivative")
    ax.plot(x, sharpened, label="sharpened")
    ax.set_title("Laplacian sharpening emphasizes rapid changes")
    ax.set_xlabel("position")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch05_laplacian_sharpening.png")


def canny_pipeline() -> None:
    steps = ["Gaussian\nsmooth", "Gradient\nmagnitude", "Non-max\nsuppression", "Double\nthreshold", "Edge\ntracking"]
    fig, ax = plt.subplots(figsize=(8, 2.4))
    ax.axis("off")
    for i, label in enumerate(steps):
        x = i * 1.8
        rect = plt.Rectangle((x, 0.5), 1.35, 0.7, fill=False, linewidth=2, color="#2563eb")
        ax.add_patch(rect)
        ax.text(x + 0.675, 0.85, label, ha="center", va="center")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 1.65, 0.85), xytext=(x + 1.36, 0.85), arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(-0.2, 8.8)
    ax.set_ylim(0.25, 1.45)
    ax.set_title("Canny edge detection pipeline")
    save(fig, "ch05_canny_pipeline.png")


def log_filter() -> None:
    x = np.linspace(-3, 3, 220)
    gaussian = np.exp(-(x**2) / 2)
    log = (x**2 - 1) * gaussian
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.plot(x, gaussian, label="Gaussian smoothing")
    ax.plot(x, log, label="Laplacian of Gaussian")
    ax.axhline(0, color="#64748b", linewidth=1)
    ax.set_title("LoG smooths first, then finds second-derivative structure")
    ax.set_xlabel("position")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch05_log_filter.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 5 章原创教学示意图" in previous:
        previous = previous.split("## 第 5 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 5 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch05_detail_profiles.png` | 5.1 图像细节的基本特征 | 展示点、线、边缘和缓慢灰度变化的剖面差异 | 是 | `5.1_图像细节的基本特征.md` |
| `ch05_first_derivative_kernels.png` | 5.2 一阶微分算子 | 对比 Roberts、Prewitt、Sobel 的核结构 | 是 | `5.2_一阶微分算子.md`, `5.2.1_具有方向性的一阶微分算子.md` |
| `ch05_roberts_sobel_prewitt.png` | 5.2.2-5.2.4 | 对比一阶算子对阶跃边缘的响应 | 是 | `5.2.2_Roberts交叉微分算子.md`, `5.2.3_Sobel微分算子.md`, `5.2.4_Priwitt微分算子.md` |
| `ch05_laplacian_sharpening.png` | 5.3 二阶微分算子 | 展示二阶导数与锐化结果的关系 | 是 | `5.3_二阶微分算子.md`, `5.3.1_Laplacian微分算子.md`, `5.3.2_Wallis微分算子.md` |
| `ch05_canny_pipeline.png` | 5.5 Canny 算子 | 展示 Canny 的多阶段边缘检测流程 | 是 | `5.4_微分算子在边缘检测中的应用.md`, `5.5_Canny算子.md` |
| `ch05_log_filter.png` | 5.6 LOG 滤波算法 | 展示高斯平滑与二阶微分结合的思想 | 是 | `5.6_LOG滤波算法.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    detail_profiles()
    first_derivative_kernels()
    operator_comparison()
    laplacian_sharpening()
    canny_pipeline()
    log_filter()
    update_readme()
    print({"figures": 6, "output": str(OUT)})


if __name__ == "__main__":
    main()
