"""Generate original teaching figures for chapter 9 image transforms."""

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


def fft_spectrum() -> None:
    x = np.linspace(0, 1, 256)
    signal = np.sin(2 * np.pi * 8 * x) + 0.45 * np.sin(2 * np.pi * 28 * x)
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(signal)))
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))
    axes[0].plot(x, signal)
    axes[0].set_title("spatial signal")
    axes[1].plot(np.linspace(-0.5, 0.5, len(spectrum)), spectrum)
    axes[1].set_title("frequency spectrum")
    for ax in axes:
        ax.grid(True, color="#e5e7eb")
    save(fig, "ch09_fft_spectrum.png")


def frequency_filtering() -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    radius = np.linspace(0, 1, 120)
    low = np.exp(-(radius / 0.35) ** 2)
    high = 1 - low
    ax.plot(radius, low, label="low-pass keeps smooth structure")
    ax.plot(radius, high, label="high-pass keeps detail")
    ax.set_title("Frequency filters choose which bands to keep")
    ax.set_xlabel("normalized frequency radius")
    ax.grid(True, color="#e5e7eb")
    ax.legend()
    save(fig, "ch09_frequency_filtering.png")


def wavelet_multiscale() -> None:
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.axis("off")
    labels = [("LL", 0.08, 0.48, 0.38, 0.38), ("LH", 0.5, 0.48, 0.18, 0.18), ("HL", 0.08, 0.14, 0.18, 0.18), ("HH", 0.5, 0.14, 0.18, 0.18)]
    for label, x, y, w, h in labels:
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, linewidth=2, color="#2563eb"))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=13)
    ax.text(0.5, 0.93, "Wavelet decomposition separates approximation and details", ha="center")
    save(fig, "ch09_wavelet_multiscale.png")


def wavelet_applications() -> None:
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.axis("off")
    items = ["compression", "fusion", "enhancement", "denoising"]
    for i, label in enumerate(items):
        x = 0.1 + i * 0.22
        ax.add_patch(plt.Rectangle((x, 0.35), 0.16, 0.22, fill=False, linewidth=2, color="#16a34a"))
        ax.text(x + 0.08, 0.46, label, ha="center", va="center", fontsize=9)
    ax.text(0.5, 0.76, "Wavelet coefficients can be selected, fused or thresholded", ha="center")
    save(fig, "ch09_wavelet_applications.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 9 章原创教学示意图" in previous:
        previous = previous.split("## 第 9 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 9 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch09_fft_spectrum.png` | 9.1 傅里叶变换 | 展示空间信号和频谱峰值 | 是 | `9.1_图像的频域变换（傅里叶变换）.md`, `9.1.1_一维傅里叶变换.md`, `9.1.2_二维傅里叶变换.md` |
| `ch09_frequency_filtering.png` | 9.1.4 频谱分布特性 | 展示低通和高通保留的频段 | 是 | `9.1.3_快速傅里叶变换（FFT）.md`, `9.1.4_图像的频谱分布特性.md` |
| `ch09_wavelet_multiscale.png` | 9.2 小波变换 | 展示 LL/LH/HL/HH 多尺度分解 | 是 | `9.2_小波变换.md`, `9.2.1_连续小波变换.md`, `9.2.2_离散小波变换.md`, `9.2.3_小波的多尺度分解与重构.md` |
| `ch09_wavelet_applications.png` | 9.3 小波应用 | 展示压缩、融合、增强和去噪的系数操作 | 是 | `9.3_小波变换在图像处理中的应用.md`, `9.3.1_应用于图像压缩.md`, `9.3.2_应用于图像融合.md`, `9.3.3_应用于图像增强.md`, `9.3.4_应用于图像去噪.md`, `9.x_习题.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    fft_spectrum()
    frequency_filtering()
    wavelet_multiscale()
    wavelet_applications()
    update_readme()
    print({"figures": 4, "output": str(OUT)})


if __name__ == "__main__":
    main()
