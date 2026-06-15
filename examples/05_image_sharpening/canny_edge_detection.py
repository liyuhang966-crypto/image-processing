"""Chapter 5.5 Canny edge detector.

Run:
    python examples/05_image_sharpening/canny_edge_detection.py --low 60 --high 160
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, odd_kernel, print_result, read_gray, save_image


def canny_edges(image: np.ndarray, low: int = 60, high: int = 160, blur_size: int = 5) -> np.ndarray:
    """Run Gaussian smoothing, gradient thinning and hysteresis thresholding via Canny."""
    blurred = cv2.GaussianBlur(image, (odd_kernel(blur_size), odd_kernel(blur_size)), 0)
    return cv2.Canny(blurred, int(low), int(high))


def main() -> None:
    parser = argparse.ArgumentParser(description="Canny edge detection.")
    add_common_arguments(parser, "ch05_canny_edges.png")
    parser.add_argument("--low", type=int, default=60, help="low hysteresis threshold")
    parser.add_argument("--high", type=int, default=160, help="high hysteresis threshold")
    parser.add_argument("--blur-size", type=int, default=5, help="odd Gaussian blur kernel size")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = canny_edges(image, low=args.low, high=args.high, blur_size=args.blur_size)
    output = save_image(args.output, result)
    print_result(source, "canny_edges", output)


if __name__ == "__main__":
    main()
