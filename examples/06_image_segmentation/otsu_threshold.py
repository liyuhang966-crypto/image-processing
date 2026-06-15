"""Chapter 6.1.3 Otsu maximum between-class variance thresholding.

Run:
    python examples/06_image_segmentation/otsu_threshold.py
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_gray, save_image


def otsu_threshold(image: np.ndarray) -> tuple[float, np.ndarray]:
    threshold, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return float(threshold), binary


def main() -> None:
    parser = argparse.ArgumentParser(description="Otsu threshold segmentation.")
    add_common_arguments(parser, "ch06_otsu_threshold.png")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    threshold, result = otsu_threshold(image)
    output = save_image(args.output, result)
    print_result(source, "otsu_threshold", output, threshold)


if __name__ == "__main__":
    main()
