"""Chapter 5.2.3 Sobel differential operator.

Run:
    python examples/05_image_sharpening/sobel_operator.py --kernel-size 3 --direction both
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, normalize_to_uint8, odd_kernel, print_result, read_gray, save_image


def sobel_edges(image: np.ndarray, kernel_size: int = 3, direction: str = "both") -> np.ndarray:
    """Compute Sobel edge magnitude or a single directional derivative."""
    ksize = odd_kernel(kernel_size)
    gray = image.astype(np.float32)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=ksize)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=ksize)
    if direction == "x":
        return normalize_to_uint8(np.abs(gx))
    if direction == "y":
        return normalize_to_uint8(np.abs(gy))
    return normalize_to_uint8(np.sqrt(gx * gx + gy * gy))


def main() -> None:
    parser = argparse.ArgumentParser(description="Sobel edge detection.")
    add_common_arguments(parser, "ch05_sobel_edges.png")
    parser.add_argument("--kernel-size", type=int, default=3, help="odd Sobel kernel size")
    parser.add_argument("--direction", choices=["x", "y", "both"], default="both")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = sobel_edges(image, kernel_size=args.kernel_size, direction=args.direction)
    output = save_image(args.output, result)
    print_result(source, "sobel_edges", output)


if __name__ == "__main__":
    main()
