"""Chapter 7.3 opening and closing.

Run:
    python examples/07_binary_image_processing/opening_closing.py --operation both --kernel-size 5
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, kernel, print_result, read_binary, save_image


def open_binary(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel(kernel_size))


def close_binary(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel(kernel_size))


def main() -> None:
    parser = argparse.ArgumentParser(description="Binary opening and closing.")
    add_common_arguments(parser, "ch07_opening_closing.png")
    parser.add_argument("--operation", choices=["open", "close", "both"], default="both")
    parser.add_argument("--kernel-size", type=int, default=5)
    args = parser.parse_args()

    image, source = read_binary(args.input)
    if args.operation == "open":
        result = open_binary(image, args.kernel_size)
    elif args.operation == "close":
        result = close_binary(image, args.kernel_size)
    else:
        result = np.hstack([open_binary(image, args.kernel_size), close_binary(image, args.kernel_size)])
    output = save_image(args.output, result)
    print_result(source, f"{args.operation}_binary", output)


if __name__ == "__main__":
    main()
