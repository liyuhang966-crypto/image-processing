"""Chapter 10.2.1 run-length encoding."""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, print_result, read_gray, save_image


def run_length_encode(values: np.ndarray) -> list[tuple[int, int]]:
    flat = values.ravel().astype(int)
    if flat.size == 0:
        return []
    runs: list[tuple[int, int]] = []
    current = int(flat[0])
    count = 1
    for value in flat[1:]:
        value = int(value)
        if value == current:
            count += 1
        else:
            runs.append((current, count))
            current, count = value, 1
    runs.append((current, count))
    return runs


def main() -> None:
    parser = argparse.ArgumentParser(description="RLE demo on a thresholded image.")
    add_common_arguments(parser, "ch10_rle_binary.png")
    parser.add_argument("--threshold", type=int, default=128)
    args = parser.parse_args()
    image, source = read_gray(args.input)
    binary = (image >= args.threshold).astype(np.uint8) * 255
    runs = run_length_encode(binary)
    output = save_image(args.output, binary)
    ratio = binary.size / max(len(runs) * 2, 1)
    print_result(source, "run_length_encode", output, f"runs={len(runs)} approx_ratio={ratio:.2f}")


if __name__ == "__main__":
    main()
