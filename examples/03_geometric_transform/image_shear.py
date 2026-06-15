"""对应章节：3.2.3 图像的错切

运行方式：
    python examples/03_geometric_transform/image_shear.py --shear-x 0.25 --shear-y 0
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, interpolation_flag, print_result, read_gray, save_image


def shear_image(
    image: np.ndarray,
    shear_x: float = 0.25,
    shear_y: float = 0.0,
    interpolation: int = cv2.INTER_LINEAR,
) -> np.ndarray:
    height, width = image.shape[:2]
    matrix = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])
    out_width = max(1, int(width + abs(shear_x) * height))
    out_height = max(1, int(height + abs(shear_y) * width))
    return cv2.warpAffine(image, matrix, (out_width, out_height), flags=interpolation)


def main() -> None:
    parser = argparse.ArgumentParser(description="3.2.3 图像错切：按 x/y 错切系数倾斜图像。")
    add_common_arguments(parser)
    parser.add_argument("--shear-x", type=float, default=0.25, help="x 方向错切系数。")
    parser.add_argument("--shear-y", type=float, default=0.0, help="y 方向错切系数。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = shear_image(image, args.shear_x, args.shear_y, interpolation_flag(args.interpolation))
    output = save_image(result, args.output, "ch03_shear")
    print_result(args.image, output, "shear_image")


if __name__ == "__main__":
    main()
