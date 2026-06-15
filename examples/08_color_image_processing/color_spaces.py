"""Chapter 8.2 color space conversion.

Run:
    python examples/08_color_image_processing/color_spaces.py --space hsv
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_color, save_image


def convert_color_space(image: np.ndarray, space: str = "hsv") -> np.ndarray:
    if space == "hsv":
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return cv2.cvtColor(converted, cv2.COLOR_HSV2BGR)
    if space == "lab":
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        return cv2.cvtColor(converted, cv2.COLOR_LAB2BGR)
    if space == "ycrcb":
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        return cv2.cvtColor(converted, cv2.COLOR_YCrCb2BGR)
    raise ValueError(f"unsupported color space: {space}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Color space conversion demo.")
    add_common_arguments(parser, "ch08_color_space.png")
    parser.add_argument("--space", choices=["hsv", "lab", "ycrcb"], default="hsv")
    args = parser.parse_args()
    image, source = read_color(args.input)
    output = save_image(args.output, convert_color_space(image, args.space))
    print_result(source, f"convert_color_space:{args.space}", output)


if __name__ == "__main__":
    main()
