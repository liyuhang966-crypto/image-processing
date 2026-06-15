"""Chapter 8.3.1 white balance.

Run:
    python examples/08_color_image_processing/white_balance.py --percentile 95
"""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, print_result, read_color, save_image


def white_balance(image: np.ndarray, percentile: float = 95.0) -> np.ndarray:
    image_float = image.astype(np.float32)
    reference = np.percentile(image_float.reshape(-1, 3), percentile, axis=0)
    target = float(np.mean(reference))
    gain = target / (reference + 1e-6)
    return np.clip(image_float * gain, 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Percentile white balance.")
    add_common_arguments(parser, "ch08_white_balance.png")
    parser.add_argument("--percentile", type=float, default=95.0)
    args = parser.parse_args()
    image, source = read_color(args.input)
    output = save_image(args.output, white_balance(image, percentile=args.percentile))
    print_result(source, "white_balance", output)


if __name__ == "__main__":
    main()
