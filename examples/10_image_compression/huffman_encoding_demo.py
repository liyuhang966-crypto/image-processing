"""Chapter 10.2.2 Huffman encoding demo."""

from __future__ import annotations

import argparse
import heapq
from collections import Counter

import cv2
import numpy as np

from _utils import add_common_arguments, normalize_uint8, print_result, read_gray, save_image


def huffman_code_lengths(values: np.ndarray) -> dict[int, int]:
    counts = Counter(values.ravel().astype(int))
    heap: list[tuple[int, int, tuple[int, ...]]] = [(count, index, (value,)) for index, (value, count) in enumerate(counts.items())]
    heapq.heapify(heap)
    lengths = {value: 0 for value in counts}
    index = len(heap)
    while len(heap) > 1:
        c1, _, symbols1 = heapq.heappop(heap)
        c2, _, symbols2 = heapq.heappop(heap)
        for symbol in symbols1 + symbols2:
            lengths[symbol] += 1
        heapq.heappush(heap, (c1 + c2, index, symbols1 + symbols2))
        index += 1
    return lengths


def main() -> None:
    parser = argparse.ArgumentParser(description="Huffman code length visualization.")
    add_common_arguments(parser, "ch10_huffman_lengths.png")
    args = parser.parse_args()
    image, source = read_gray(args.input)
    quantized = (image // 16).astype(np.uint8)
    lengths = huffman_code_lengths(quantized)
    lut = np.array([lengths.get(i, 0) for i in range(16)], dtype=np.float32)
    visual = normalize_uint8(lut[quantized])
    output = save_image(args.output, visual)
    avg = sum(Counter(quantized.ravel()).get(k, 0) * v for k, v in lengths.items()) / quantized.size
    print_result(source, "huffman_code_lengths", output, f"avg_bits={avg:.2f}")


if __name__ == "__main__":
    main()
