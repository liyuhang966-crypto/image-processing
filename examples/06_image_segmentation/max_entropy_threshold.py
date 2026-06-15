"""Chapter 6.1.2 maximum entropy thresholding.

Run:
    python examples/06_image_segmentation/max_entropy_threshold.py
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_gray, save_image


def max_entropy_threshold(image: np.ndarray) -> tuple[int, np.ndarray]:
    hist = cv2.calcHist([image], [0], None, [256], [0, 256]).ravel().astype(float)
    probability = hist / max(hist.sum(), 1.0)
    cumulative = np.cumsum(probability)
    best_threshold = 0
    best_entropy = -np.inf
    eps = 1e-12
    for threshold in range(1, 255):
        p0 = cumulative[threshold]
        p1 = 1.0 - p0
        if p0 <= eps or p1 <= eps:
            continue
        background = probability[: threshold + 1] / p0
        foreground = probability[threshold + 1 :] / p1
        entropy = -np.sum(background * np.log(background + eps)) - np.sum(foreground * np.log(foreground + eps))
        if entropy > best_entropy:
            best_entropy = float(entropy)
            best_threshold = threshold
    _, binary = cv2.threshold(image, best_threshold, 255, cv2.THRESH_BINARY)
    return best_threshold, binary


def main() -> None:
    parser = argparse.ArgumentParser(description="Maximum entropy threshold segmentation.")
    add_common_arguments(parser, "ch06_max_entropy_threshold.png")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    threshold, result = max_entropy_threshold(image)
    output = save_image(args.output, result)
    print_result(source, "max_entropy_threshold", output, float(threshold))


if __name__ == "__main__":
    main()
