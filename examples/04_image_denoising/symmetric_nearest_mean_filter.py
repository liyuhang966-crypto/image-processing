"""对应章节：4.4.2 对称近邻均值滤波

运行方式：
    python examples/04_image_denoising/symmetric_nearest_mean_filter.py --kernel-size 5
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, odd_kernel, print_result, read_gray, save_image


def symmetric_nearest_mean_filter_image(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    window = odd_kernel(kernel_size)
    radius = window // 2
    padded = cv2.copyMakeBorder(image, radius, radius, radius, radius, cv2.BORDER_REFLECT)
    output = np.empty_like(image)
    offsets = [(dy, dx) for dy in range(-radius, radius + 1) for dx in range(-radius, radius + 1)]
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            center_y, center_x = y + radius, x + radius
            values = [int(padded[center_y, center_x])]
            for dy, dx in offsets:
                if dy < 0 or (dy == 0 and dx <= 0):
                    continue
                a = int(padded[center_y + dy, center_x + dx])
                b = int(padded[center_y - dy, center_x - dx])
                center = int(padded[center_y, center_x])
                values.append(a if abs(a - center) <= abs(b - center) else b)
            output[y, x] = np.uint8(np.mean(values))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="4.4.2 对称近邻均值滤波：从对称像素对中选择更接近中心的值。")
    add_common_arguments(parser)
    parser.add_argument("--kernel-size", type=int, default=5)
    args = parser.parse_args()

    image = read_gray(args.image)
    result = symmetric_nearest_mean_filter_image(image, args.kernel_size)
    output = save_image(result, args.output, "ch04_symmetric_nearest_mean_filter")
    print_result(args.image, output, "symmetric_nearest_mean_filter_image")


if __name__ == "__main__":
    main()
