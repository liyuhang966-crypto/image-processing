from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "extracted_figures"


def savefig(name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=160)
    plt.close()


def gamma_curve() -> None:
    x = np.linspace(0, 1, 256)
    plt.figure(figsize=(6, 4))
    for gamma, label in [(0.45, "gamma < 1 brightens"), (1.0, "identity"), (2.2, "gamma > 1 darkens")]:
        plt.plot(x, x**gamma, label=label)
    plt.title("Gamma correction transfer curves")
    plt.xlabel("input gray level")
    plt.ylabel("output gray level")
    plt.grid(True, alpha=0.3)
    plt.legend()
    savefig("ch02_gamma_curves.png")


def contrast_stretching() -> None:
    x = np.arange(256)
    y = np.interp(x, [0, 70, 180, 255], [0, 25, 235, 255])
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, color="#1f77b4")
    plt.scatter([70, 180], [25, 235], color="#d62728", zorder=3)
    plt.title("Piecewise linear contrast stretching")
    plt.xlabel("input gray level")
    plt.ylabel("output gray level")
    plt.grid(True, alpha=0.3)
    savefig("ch02_contrast_stretching.png")


def gray_window() -> None:
    x = np.arange(256)
    window = ((x >= 90) & (x <= 170)).astype(float)
    highlight = np.where(window > 0, 255, 30)
    slice_only = np.where(window > 0, 255, 0)
    plt.figure(figsize=(7, 4))
    plt.plot(x, highlight, label="gray-level window")
    plt.plot(x, slice_only, label="window slicing", linestyle="--")
    plt.axvspan(90, 170, color="#ffcc66", alpha=0.25)
    plt.title("Gray-level window and slicing")
    plt.xlabel("input gray level")
    plt.ylabel("output gray level")
    plt.ylim(-10, 270)
    plt.grid(True, alpha=0.3)
    plt.legend()
    savefig("ch02_gray_window_slicing.png")


def synthetic_gray() -> np.ndarray:
    yy, xx = np.mgrid[0:256, 0:256]
    img = (60 + 80 * (xx / 255) + 45 * np.sin(yy / 22)).astype(np.float32)
    cv2.circle(img, (92, 96), 42, 185, -1)
    cv2.rectangle(img, (145, 140), (220, 210), 105, -1)
    noise = np.random.default_rng(42).normal(0, 6, img.shape)
    return np.clip(img + noise, 0, 255).astype(np.uint8)


def histogram_equalization() -> None:
    img = synthetic_gray()
    eq = cv2.equalizeHist(img)
    plt.figure(figsize=(8, 5))
    for i, (title, data) in enumerate([("before", img), ("after", eq)], 1):
        plt.subplot(2, 2, i)
        plt.imshow(data, cmap="gray", vmin=0, vmax=255)
        plt.title(title)
        plt.axis("off")
        plt.subplot(2, 2, i + 2)
        plt.hist(data.ravel(), bins=64, range=(0, 255), color="#4c78a8")
        plt.xlim(0, 255)
        plt.title(f"histogram {title}")
    savefig("ch02_histogram_equalization.png")


def adaptive_histogram_equalization() -> None:
    img = synthetic_gray()
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(img)
    plt.figure(figsize=(7, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray", vmin=0, vmax=255)
    plt.title("global input")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(clahe, cmap="gray", vmin=0, vmax=255)
    plt.title("local equalization")
    plt.axis("off")
    savefig("ch02_adaptive_histogram_equalization.png")


def retinex() -> None:
    img = synthetic_gray().astype(np.float32) + 1
    illumination = cv2.GaussianBlur(img, (0, 0), 18) + 1
    reflectance = np.log(img) - np.log(illumination)
    out = cv2.normalize(reflectance, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    plt.figure(figsize=(8, 4))
    for i, (title, data) in enumerate([("observed image", img), ("estimated illumination", illumination), ("retinex output", out)], 1):
        plt.subplot(1, 3, i)
        plt.imshow(data, cmap="gray")
        plt.title(title)
        plt.axis("off")
    savefig("ch02_retinex_decomposition.png")


def pseudo_color() -> None:
    ramp = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (40, 1))
    color = cv2.applyColorMap(ramp, cv2.COLORMAP_JET)
    plt.figure(figsize=(6, 2.2))
    plt.imshow(cv2.cvtColor(color, cv2.COLOR_BGR2RGB))
    plt.title("Pseudo-color lookup table")
    plt.axis("off")
    savefig("ch02_pseudo_color_lut.png")


def write_readme() -> None:
    text = """# 第 2 章原创教学示意图

这些图片是为知识库重新绘制的教学示意图，不是从原书批量裁剪得到的页面图片。

| 文件 | 用途 |
|---|---|
| `ch02_gamma_curves.png` | γ 校正曲线 |
| `ch02_contrast_stretching.png` | 分段线性对比度展宽 |
| `ch02_gray_window_slicing.png` | 灰级窗与灰级窗切片 |
| `ch02_histogram_equalization.png` | 直方图均衡化前后对比 |
| `ch02_adaptive_histogram_equalization.png` | 自适应直方图均衡化效果 |
| `ch02_pseudo_color_lut.png` | 伪彩色查找表 |
| `ch02_retinex_decomposition.png` | Retinex 光照/反射分解示意 |
"""
    (OUT / "README.md").write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    gamma_curve()
    contrast_stretching()
    gray_window()
    histogram_equalization()
    adaptive_histogram_equalization()
    pseudo_color()
    retinex()
    write_readme()
    print({"figures": 7, "output": str(OUT)})


if __name__ == "__main__":
    main()
