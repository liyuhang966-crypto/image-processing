"""对应章节：3.1.3 图像的旋转

运行方式：
    python examples/03_geometric_transform/image_rotation.py --angle 30 --scale 1.0
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, interpolation_flag, print_result, read_gray, save_image


def rotate_image(
    image: np.ndarray,
    angle: float = 30,
    scale: float = 1.0,
    interpolation: int = cv2.INTER_LINEAR,
) -> np.ndarray:
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(image, matrix, (width, height), flags=interpolation)


def main() -> None:
    parser = argparse.ArgumentParser(description="3.1.3 图像旋转：围绕图像中心旋转。")
    add_common_arguments(parser)
    parser.add_argument("--angle", type=float, default=30, help="旋转角度，正值为逆时针。")
    parser.add_argument("--scale", type=float, default=1.0, help="旋转时的缩放因子。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = rotate_image(image, args.angle, args.scale, interpolation_flag(args.interpolation))
    output = save_image(result, args.output, "ch03_rotation")
    print_result(args.image, output, "rotate_image")


if __name__ == "__main__":
    main()
