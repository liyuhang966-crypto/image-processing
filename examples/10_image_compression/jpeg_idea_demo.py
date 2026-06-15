"""Chapter 10.3 JPEG-style lossy compression idea."""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, print_result, read_gray, save_image


def jpeg_block_demo(image: np.ndarray, block_size: int = 8, quality: int = 24) -> np.ndarray:
    h, w = image.shape
    out = np.zeros_like(image, dtype=np.float32)
    q = max(1, int(quality))
    for y in range(0, h - block_size + 1, block_size):
        for x in range(0, w - block_size + 1, block_size):
            block = image[y : y + block_size, x : x + block_size].astype(np.float32) - 128
            coeff = cv2.dct(block)
            quantized = np.round(coeff / q) * q
            out[y : y + block_size, x : x + block_size] = cv2.idct(quantized) + 128
    return np.clip(out, 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="JPEG block DCT quantization idea.")
    add_common_arguments(parser, "ch10_jpeg_idea.png")
    parser.add_argument("--quality", type=int, default=24)
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, jpeg_block_demo(image, quality=args.quality))
    print_result(source, "jpeg_block_demo", output)


if __name__ == "__main__":
    main()
