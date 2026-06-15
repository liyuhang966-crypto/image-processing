"""Chapter 6.1 threshold segmentation.

Run:
    python examples/06_image_segmentation/threshold_segmentation.py --threshold 128
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_gray, save_image


def threshold_segment(image: np.ndarray, threshold: int = 128, inverse: bool = False) -> np.ndarray:
    mode = cv2.THRESH_BINARY_INV if inverse else cv2.THRESH_BINARY
    _, binary = cv2.threshold(image, int(threshold), 255, mode)
    return binary


def main() -> None:
    parser = argparse.ArgumentParser(description="Global threshold segmentation.")
    add_common_arguments(parser, "ch06_threshold_segment.png")
    parser.add_argument("--threshold", type=int, default=128)
    parser.add_argument("--inverse", action="store_true")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = threshold_segment(image, threshold=args.threshold, inverse=args.inverse)
    output = save_image(args.output, result)
    print_result(source, "threshold_segment", output, float(args.threshold))


if __name__ == "__main__":
    main()
