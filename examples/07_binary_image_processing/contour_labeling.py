"""Chapter 7.4.2 contour labeling.

Run:
    python examples/07_binary_image_processing/contour_labeling.py --min-area 30
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_binary, save_image


def label_contours(image: np.ndarray, min_area: float = 20.0) -> np.ndarray:
    contours, _ = cv2.findContours((image > 0).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    canvas = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    index = 1
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        color = ((37 * index) % 255, (91 * index) % 255, (151 * index) % 255)
        cv2.drawContours(canvas, [contour], -1, color, 2)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(canvas, str(index), (x, max(15, y - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        index += 1
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description="Contour labeling.")
    add_common_arguments(parser, "ch07_contour_labeling.png")
    parser.add_argument("--min-area", type=float, default=30.0)
    args = parser.parse_args()

    image, source = read_binary(args.input)
    result = label_contours(image, min_area=args.min_area)
    output = save_image(args.output, result)
    print_result(source, "label_contours", output)


if __name__ == "__main__":
    main()
