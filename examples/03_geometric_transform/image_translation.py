"""对应章节：3.1.1 图像的平移

运行方式：
    python examples/03_geometric_transform/image_translation.py --dx 30 --dy 20
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, interpolation_flag, print_result, read_gray, save_image


def translate_image(
    image: np.ndarray,
    dx: float = 30,
    dy: float = 20,
    interpolation: int = cv2.INTER_LINEAR,
    border_value: int = 0,
) -> np.ndarray:
    height, width = image.shape[:2]
    matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=interpolation,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="3.1.1 图像平移：按 dx、dy 移动图像。")
    add_common_arguments(parser)
    parser.add_argument("--dx", type=float, default=30, help="x 方向平移量，正值向右。")
    parser.add_argument("--dy", type=float, default=20, help="y 方向平移量，正值向下。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = translate_image(image, args.dx, args.dy, interpolation_flag(args.interpolation))
    output = save_image(result, args.output, "ch03_translation")
    print_result(args.image, output, "translate_image")


if __name__ == "__main__":
    main()
