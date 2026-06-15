"""Generate original teaching figures for chapter 10 image compression."""

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


def pipeline() -> None:
    fig, ax = plt.subplots(figsize=(7, 2.4))
    ax.axis("off")
    steps = ["image", "transform /\npredict", "quantize /\ncode", "bitstream"]
    for i, label in enumerate(steps):
        x = 0.08 + i * 0.23
        ax.add_patch(plt.Rectangle((x, 0.42), 0.16, 0.25, fill=False, linewidth=2, color="#2563eb"))
        ax.text(x + 0.08, 0.545, label, ha="center", va="center")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.21, 0.545), xytext=(x + 0.17, 0.545), arrowprops=dict(arrowstyle="->"))
    ax.set_title("Compression removes redundancy before storing bits")
    save(fig, "ch10_compression_pipeline.png")


def rle_runs() -> None:
    sequence = [0, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 1]
    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.imshow([sequence], cmap="tab20", aspect="auto")
    ax.set_title("RLE stores value + run length")
    ax.set_yticks([])
    ax.set_xticks(range(len(sequence)))
    save(fig, "ch10_rle_runs.png")


def huffman_tree() -> None:
    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.axis("off")
    ax.set_title("Frequent symbols get shorter Huffman codes")
    ax.text(0.2, 0.75, "A: 0", fontsize=12)
    ax.text(0.55, 0.75, "B: 10", fontsize=12)
    ax.text(0.55, 0.48, "C: 110", fontsize=12)
    ax.text(0.55, 0.22, "D: 111", fontsize=12)
    ax.text(0.22, 0.38, "shorter code\nfor higher probability", color="#2563eb")
    save(fig, "ch10_huffman_tree.png")


def lossy_quantization() -> None:
    x = np.arange(64)
    coeff = np.exp(-x / 13) * np.cos(x / 3)
    quant = np.round(coeff / 0.18) * 0.18
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x, coeff, label="original coefficient")
    ax.step(x, quant, where="mid", label="quantized")
    ax.set_title("Lossy coding coarsens transform coefficients")
    ax.legend()
    ax.grid(True, color="#e5e7eb")
    save(fig, "ch10_lossy_quantization.png")


def wavelet_compression() -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3))
    ax.axis("off")
    ax.set_title("Wavelet compression keeps important coefficients")
    for i, label in enumerate(["LL keep", "details threshold", "entropy code"]):
        ax.add_patch(plt.Rectangle((0.12 + 0.28 * i, 0.42), 0.2, 0.22, fill=False, linewidth=2, color="#16a34a"))
        ax.text(0.22 + 0.28 * i, 0.53, label, ha="center", va="center", fontsize=9)
    save(fig, "ch10_wavelet_compression.png")


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 10 章原创教学示意图" in previous:
        previous = previous.split("## 第 10 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 10 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch10_compression_pipeline.png` | 10.1 图像冗余 | 展示压缩基本流程 | 是 | `10.1_图像冗余的概念.md`, `10.1.1_冗余的概念.md`, `10.1.2_图像中的冗余.md` |
| `ch10_rle_runs.png` | 10.2.1 RLE | 展示行程编码 | 是 | `10.2_图像无损压缩编码.md`, `10.2.1_行程编码（RLE）.md` |
| `ch10_huffman_tree.png` | 10.2.2 Huffman | 展示高概率短码思想 | 是 | `10.2.2_哈夫曼（Huffman）编码.md` |
| `ch10_lossy_quantization.png` | 10.3 有损压缩 | 展示量化带来的近似 | 是 | `10.3_图像有损压缩编码.md`, `10.3.1_彩色图像的有损编码.md` |
| `ch10_wavelet_compression.png` | 10.3.2 小波变换编码 | 展示保留重要小波系数 | 是 | `10.3.2_小波变换编码.md`, `10.x_习题.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    pipeline()
    rle_runs()
    huffman_tree()
    lossy_quantization()
    wavelet_compression()
    update_readme()
    print({"figures": 5, "output": str(OUT)})


if __name__ == "__main__":
    main()
