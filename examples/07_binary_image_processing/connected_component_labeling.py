"""Chapter 7.4.1 connected component labeling.

Run:
    python examples/07_binary_image_processing/connected_component_labeling.py --connectivity 8
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_binary, save_image


def label_connected_components(image: np.ndarray, connectivity: int = 8) -> np.ndarray:
    count, labels = cv2.connectedComponents((image > 0).astype(np.uint8), connectivity=int(connectivity))
    if count <= 1:
        return np.zeros_like(image)
    return cv2.applyColorMap(cv2.normalize(labels, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8), cv2.COLORMAP_TURBO)


def main() -> None:
    parser = argparse.ArgumentParser(description="Connected component labeling.")
    add_common_arguments(parser, "ch07_connected_components.png")
    parser.add_argument("--connectivity", choices=[4, 8], type=int, default=8)
    args = parser.parse_args()

    image, source = read_binary(args.input)
    result = label_connected_components(image, connectivity=args.connectivity)
    output = save_image(args.output, result)
    print_result(source, "label_connected_components", output)


if __name__ == "__main__":
    main()
