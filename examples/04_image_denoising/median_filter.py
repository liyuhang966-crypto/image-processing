"""对应章节：4.3 中值滤波

运行方式：
    python examples/04_image_denoising/median_filter.py --kernel-size 5
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, odd_kernel, print_result, read_gray, save_image


def median_filter_image(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    return cv2.medianBlur(image, odd_kernel(kernel_size))


def main() -> None:
    parser = argparse.ArgumentParser(description="4.3 中值滤波：用邻域中位数抑制椒盐噪声。")
    add_common_arguments(parser)
    parser.add_argument("--kernel-size", type=int, default=5, help="滤波窗口尺寸，自动修正为奇数。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = median_filter_image(image, args.kernel_size)
    output = save_image(result, args.output, "ch04_median_filter")
    print_result(args.image, output, "median_filter_image")


if __name__ == "__main__":
    main()
