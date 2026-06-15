"""对应章节：4.5 非局部均值滤波

运行方式：
    python examples/04_image_denoising/non_local_means_filter.py --h 10 --template-window-size 7 --search-window-size 21
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, odd_kernel, print_result, read_gray, save_image


def non_local_means_filter_image(
    image: np.ndarray,
    h: float = 10,
    template_window_size: int = 7,
    search_window_size: int = 21,
) -> np.ndarray:
    return cv2.fastNlMeansDenoising(
        image,
        None,
        h=float(h),
        templateWindowSize=odd_kernel(template_window_size),
        searchWindowSize=odd_kernel(search_window_size),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="4.5 非局部均值滤波：按相似块加权平均进行去噪。")
    add_common_arguments(parser)
    parser.add_argument("--h", type=float, default=10, help="滤波强度，越大越平滑。")
    parser.add_argument("--template-window-size", type=int, default=7)
    parser.add_argument("--search-window-size", type=int, default=21)
    args = parser.parse_args()

    image = read_gray(args.image)
    result = non_local_means_filter_image(image, args.h, args.template_window_size, args.search_window_size)
    output = save_image(result, args.output, "ch04_non_local_means_filter")
    print_result(args.image, output, "non_local_means_filter_image")


if __name__ == "__main__":
    main()
