"""Chapter 7.2 erosion and dilation.

Run:
    python examples/07_binary_image_processing/erosion_dilation.py --operation both --kernel-size 5
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, kernel, print_result, read_binary, save_image


def erode_binary(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    return cv2.erode(image, kernel(kernel_size), iterations=int(iterations))


def dilate_binary(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    return cv2.dilate(image, kernel(kernel_size), iterations=int(iterations))


def main() -> None:
    parser = argparse.ArgumentParser(description="Binary erosion and dilation.")
    add_common_arguments(parser, "ch07_erosion_dilation.png")
    parser.add_argument("--operation", choices=["erode", "dilate", "both"], default="both")
    parser.add_argument("--kernel-size", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=1)
    args = parser.parse_args()

    image, source = read_binary(args.input)
    if args.operation == "erode":
        result = erode_binary(image, args.kernel_size, args.iterations)
    elif args.operation == "dilate":
        result = dilate_binary(image, args.kernel_size, args.iterations)
    else:
        result = np.hstack([erode_binary(image, args.kernel_size, args.iterations), dilate_binary(image, args.kernel_size, args.iterations)])
    output = save_image(args.output, result)
    print_result(source, f"{args.operation}_binary", output)


if __name__ == "__main__":
    main()
