"""对应章节：3.2.1/3.2.2 图像缩小与放大

运行方式：
    python examples/03_geometric_transform/image_resize.py --scale-x 0.75 --scale-y 0.75 --interpolation area
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, interpolation_flag, print_result, read_gray, save_image


def resize_image(
    image: np.ndarray,
    scale_x: float = 0.75,
    scale_y: float = 0.75,
    interpolation: int = cv2.INTER_AREA,
) -> np.ndarray:
    if scale_x <= 0 or scale_y <= 0:
        raise ValueError("scale_x and scale_y must be positive")
    return cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=interpolation)


def main() -> None:
    parser = argparse.ArgumentParser(description="3.2 图像缩放：按比例缩小或放大图像。")
    add_common_arguments(parser)
    parser.set_defaults(interpolation="area")
    parser.add_argument("--scale-x", type=float, default=0.75, help="x 方向缩放比例。")
    parser.add_argument("--scale-y", type=float, default=0.75, help="y 方向缩放比例。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = resize_image(image, args.scale_x, args.scale_y, interpolation_flag(args.interpolation))
    output = save_image(result, args.output, "ch03_resize")
    print_result(args.image, output, "resize_image")


if __name__ == "__main__":
    main()
