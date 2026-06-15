"""Chapter 8.4 color compensation.

Run:
    python examples/08_color_image_processing/color_compensation.py --red-gain 1.05 --blue-gain 0.95
"""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, print_result, read_color, save_image


def color_compensation(image: np.ndarray, red_gain: float = 1.05, green_gain: float = 1.0, blue_gain: float = 0.95) -> np.ndarray:
    gains = np.array([blue_gain, green_gain, red_gain], dtype=np.float32)
    return np.clip(image.astype(np.float32) * gains, 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manual color gain compensation.")
    add_common_arguments(parser, "ch08_color_compensation.png")
    parser.add_argument("--red-gain", type=float, default=1.05)
    parser.add_argument("--green-gain", type=float, default=1.0)
    parser.add_argument("--blue-gain", type=float, default=0.95)
    args = parser.parse_args()
    image, source = read_color(args.input)
    output = save_image(args.output, color_compensation(image, args.red_gain, args.green_gain, args.blue_gain))
    print_result(source, "color_compensation", output)


if __name__ == "__main__":
    main()
