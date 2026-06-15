"""对应章节：3.1.2 图像的镜像

运行方式：
    python examples/03_geometric_transform/image_mirror.py --axis horizontal
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, print_result, read_gray, save_image


def mirror_image(image: np.ndarray, axis: str = "horizontal") -> np.ndarray:
    flip_code = {"horizontal": 1, "vertical": 0, "both": -1}[axis]
    return cv2.flip(image, flip_code)


def main() -> None:
    parser = argparse.ArgumentParser(description="3.1.2 图像镜像：沿水平、垂直或双轴翻转。")
    add_common_arguments(parser)
    parser.add_argument("--axis", choices=["horizontal", "vertical", "both"], default="horizontal")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = mirror_image(image, args.axis)
    output = save_image(result, args.output, "ch03_mirror")
    print_result(args.image, output, "mirror_image")


if __name__ == "__main__":
    main()
