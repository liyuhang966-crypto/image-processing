"""Generate original teaching figures for chapter 11 deep learning."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "extracted_figures"


def canvas(width: int = 760, height: int = 320) -> np.ndarray:
    return np.full((height, width, 3), 255, dtype=np.uint8)


def save(name: str, image: np.ndarray) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT / name), image)


def blocks(name: str, title: str, labels: list[str]) -> None:
    image = canvas()
    cv2.putText(image, title, (24, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (20, 20, 20), 2)
    step = 650 // max(len(labels), 1)
    for i, label in enumerate(labels):
        x = 45 + i * step
        cv2.rectangle(image, (x, 130), (x + 90, 205), (37, 99, 235), 2)
        cv2.putText(image, label, (x + 8, 174), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (20, 20, 20), 1)
        if i < len(labels) - 1:
            cv2.arrowedLine(image, (x + 96, 168), (x + step - 8, 168), (90, 90, 90), 2)
    save(name, image)


def yolo_grid() -> None:
    image = canvas(640, 360)
    cv2.putText(image, "YOLO grid prediction", (24, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (20, 20, 20), 2)
    for x in range(80, 561, 80):
        cv2.line(image, (x, 70), (x, 310), (210, 210, 210), 1)
    for y in range(70, 311, 60):
        cv2.line(image, (80, y), (560, y), (210, 210, 210), 1)
    cv2.rectangle(image, (185, 130), (315, 235), (37, 99, 235), 3)
    cv2.rectangle(image, (365, 105), (505, 250), (22, 163, 74), 3)
    save("ch11_yolo_grid.png", image)


def update_readme() -> None:
    path = OUT / "README.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else ""
    if "## 第 11 章原创教学示意图" in previous:
        previous = previous.split("## 第 11 章原创教学示意图", 1)[0].rstrip() + "\n"
    block = """
## 第 11 章原创教学示意图

这些图片为本仓库重新绘制的原创教学图，不是原书截图，也不依赖外部模型。

| 文件 | 对应小节 | 用途 | 是否原创 | 被引用的 wiki |
|---|---|---|---|---|
| `ch11_cnn_layers.png` | 11.1 深度卷积网络基本结构 | 展示卷积、BN、激活、池化和任务头 | 是 | `11.1_深度卷积网络的基本结构.md`, `11.1.1_卷积层.md`, `11.1.2_激活层.md`, `11.1.3_BN层（批数据归一化处理层）.md`, `11.1.4_池化层.md` |
| `ch11_super_resolution.png` | 11.2 超分辨率网络 | 展示 LR 到 SR 的映射流程 | 是 | `11.2_超分辨率图像重建卷积网络.md`, `11.2.1_SRCNN网络.md`, `11.2.2_ESPCN网络.md` |
| `ch11_classification_networks.png` | 11.3 分类网络 | 展示 LeNet/AlexNet 分类结构 | 是 | `11.3_图像分类深度卷积网络.md`, `11.3.1_LeNet-5网络.md`, `11.3.2_AlexNet网络.md` |
| `ch11_detection_networks.png` | 11.4 目标检测网络 | 展示候选框与检测头思路 | 是 | `11.4_图像目标检测深度卷积网络.md`, `11.4.1_Faster-RCNN网络.md` |
| `ch11_yolo_grid.png` | 11.4.2 YOLO 网络 | 展示网格预测框思想 | 是 | `11.4.2_YOLO网络.md`, `11.x_习题.md` |
"""
    path.write_text(previous.rstrip() + "\n" + block.lstrip(), encoding="utf-8")


def main() -> None:
    blocks("ch11_cnn_layers.png", "CNN layers", ["Input", "Conv", "BN", "ReLU", "Pool", "Head"])
    blocks("ch11_super_resolution.png", "Super-resolution CNN", ["LR", "Features", "Mapping", "Upscale", "SR"])
    blocks("ch11_classification_networks.png", "Classification CNNs", ["Image", "Conv", "Pool", "FC", "Class"])
    blocks("ch11_detection_networks.png", "Detection CNNs", ["Image", "Backbone", "Proposal", "ROI", "Boxes"])
    yolo_grid()
    update_readme()
    print({"figures": 5, "output": str(OUT)})


if __name__ == "__main__":
    main()
