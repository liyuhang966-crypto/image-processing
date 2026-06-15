"""Chapter 8.3.2 gray world color balance.

Run:
    python examples/08_color_image_processing/gray_world.py
"""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, print_result, read_color, save_image


def gray_world_balance(image: np.ndarray) -> np.ndarray:
    image_float = image.astype(np.float32)
    channel_mean = np.mean(image_float, axis=(0, 1))
    target = float(np.mean(channel_mean))
    gain = target / (channel_mean + 1e-6)
    return np.clip(image_float * gain, 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gray world color balance.")
    add_common_arguments(parser, "ch08_gray_world.png")
    args = parser.parse_args()
    image, source = read_color(args.input)
    output = save_image(args.output, gray_world_balance(image))
    print_result(source, "gray_world_balance", output)


if __name__ == "__main__":
    main()
