"""对应章节：4.4.1 K近邻均值滤波

运行方式：
    python examples/04_image_denoising/k_nearest_mean_filter.py --kernel-size 5 --k 8
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, odd_kernel, print_result, read_gray, save_image


def k_nearest_mean_filter_image(image: np.ndarray, kernel_size: int = 5, k: int = 8) -> np.ndarray:
    window = odd_kernel(kernel_size)
    radius = window // 2
    padded = cv2.copyMakeBorder(image, radius, radius, radius, radius, cv2.BORDER_REFLECT)
    output = np.empty_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            patch = padded[y : y + window, x : x + window].astype(np.int16).ravel()
            center = int(padded[y + radius, x + radius])
            nearest = patch[np.argsort(np.abs(patch - center))[: max(1, min(k, patch.size))]]
            output[y, x] = np.uint8(np.mean(nearest))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="4.4.1 K近邻均值滤波：只平均与中心灰度接近的邻域像素。")
    add_common_arguments(parser)
    parser.add_argument("--kernel-size", type=int, default=5)
    parser.add_argument("--k", type=int, default=8, help="参与均值的近邻像素数量。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = k_nearest_mean_filter_image(image, args.kernel_size, args.k)
    output = save_image(result, args.output, "ch04_k_nearest_mean_filter")
    print_result(args.image, output, "k_nearest_mean_filter_image")


if __name__ == "__main__":
    main()
