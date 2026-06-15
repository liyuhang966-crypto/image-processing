"""Chapter 6.2 region growing segmentation.

Run:
    python examples/06_image_segmentation/region_growing.py --seed-x 85 --seed-y 120 --tolerance 28
"""

from __future__ import annotations

import argparse
from collections import deque

import numpy as np

from _utils import add_common_arguments, print_result, read_gray, save_image


def region_growing_segment(image: np.ndarray, seed: tuple[int, int], tolerance: int = 25) -> np.ndarray:
    height, width = image.shape
    seed_x = min(max(seed[0], 0), width - 1)
    seed_y = min(max(seed[1], 0), height - 1)
    seed_value = int(image[seed_y, seed_x])
    visited = np.zeros_like(image, dtype=bool)
    mask = np.zeros_like(image, dtype=np.uint8)
    queue: deque[tuple[int, int]] = deque([(seed_x, seed_y)])
    visited[seed_y, seed_x] = True
    while queue:
        x, y = queue.popleft()
        if abs(int(image[y, x]) - seed_value) <= tolerance:
            mask[y, x] = 255
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((nx, ny))
    return mask


def main() -> None:
    parser = argparse.ArgumentParser(description="Region growing segmentation.")
    add_common_arguments(parser, "ch06_region_growing.png")
    parser.add_argument("--seed-x", type=int, default=85)
    parser.add_argument("--seed-y", type=int, default=120)
    parser.add_argument("--tolerance", type=int, default=28)
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = region_growing_segment(image, seed=(args.seed_x, args.seed_y), tolerance=args.tolerance)
    output = save_image(args.output, result)
    print_result(source, "region_growing_segment", output, float(args.tolerance))


if __name__ == "__main__":
    main()
