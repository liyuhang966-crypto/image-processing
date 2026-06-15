"""Chapter 5.2.2 Roberts cross differential operator.

Run:
    python examples/05_image_sharpening/roberts_operator.py --scale 1.0
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, normalize_to_uint8, print_result, read_gray, save_image


def roberts_edges(image: np.ndarray, scale: float = 1.0) -> np.ndarray:
    """Detect diagonal gray changes with the two 2x2 Roberts kernels."""
    gray = image.astype(np.float32)
    kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    gx = cv2.filter2D(gray, cv2.CV_32F, kernel_x)
    gy = cv2.filter2D(gray, cv2.CV_32F, kernel_y)
    magnitude = np.sqrt(gx * gx + gy * gy) * float(scale)
    return normalize_to_uint8(magnitude)


def main() -> None:
    parser = argparse.ArgumentParser(description="Roberts cross edge detection.")
    add_common_arguments(parser, "ch05_roberts_edges.png")
    parser.add_argument("--scale", type=float, default=1.0, help="edge magnitude scale")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = roberts_edges(image, scale=args.scale)
    output = save_image(args.output, result)
    print_result(source, "roberts_edges", output)


if __name__ == "__main__":
    main()
