"""Chapter 5.2.4 Prewitt differential operator.

Run:
    python examples/05_image_sharpening/prewitt_operator.py --direction both
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, normalize_to_uint8, print_result, read_gray, save_image


def prewitt_edges(image: np.ndarray, direction: str = "both") -> np.ndarray:
    """Compute Prewitt edge response with uniform smoothing in the perpendicular direction."""
    gray = image.astype(np.float32)
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_y = kernel_x.T
    gx = cv2.filter2D(gray, cv2.CV_32F, kernel_x)
    gy = cv2.filter2D(gray, cv2.CV_32F, kernel_y)
    if direction == "x":
        return normalize_to_uint8(np.abs(gx))
    if direction == "y":
        return normalize_to_uint8(np.abs(gy))
    return normalize_to_uint8(np.sqrt(gx * gx + gy * gy))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prewitt edge detection.")
    add_common_arguments(parser, "ch05_prewitt_edges.png")
    parser.add_argument("--direction", choices=["x", "y", "both"], default="both")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = prewitt_edges(image, direction=args.direction)
    output = save_image(args.output, result)
    print_result(source, "prewitt_edges", output)


if __name__ == "__main__":
    main()
