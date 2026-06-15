"""Chapter 7.5 thinning.

Run:
    python examples/07_binary_image_processing/thinning.py --max-iterations 80
"""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, print_result, read_binary, save_image


def _transitions(neighbors: list[int]) -> int:
    return sum((neighbors[i] == 0 and neighbors[(i + 1) % 8] == 1) for i in range(8))


def thin_binary(image: np.ndarray, max_iterations: int = 80) -> np.ndarray:
    binary = (image > 0).astype(np.uint8)
    for _ in range(int(max_iterations)):
        changed = False
        for step in (0, 1):
            remove: list[tuple[int, int]] = []
            for y in range(1, binary.shape[0] - 1):
                for x in range(1, binary.shape[1] - 1):
                    if binary[y, x] == 0:
                        continue
                    p2 = binary[y - 1, x]
                    p3 = binary[y - 1, x + 1]
                    p4 = binary[y, x + 1]
                    p5 = binary[y + 1, x + 1]
                    p6 = binary[y + 1, x]
                    p7 = binary[y + 1, x - 1]
                    p8 = binary[y, x - 1]
                    p9 = binary[y - 1, x - 1]
                    neighbors = [p2, p3, p4, p5, p6, p7, p8, p9]
                    count = int(sum(neighbors))
                    if not (2 <= count <= 6) or _transitions(neighbors) != 1:
                        continue
                    if step == 0 and p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0:
                        remove.append((x, y))
                    if step == 1 and p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0:
                        remove.append((x, y))
            if remove:
                changed = True
                for x, y in remove:
                    binary[y, x] = 0
        if not changed:
            break
    return (binary * 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Zhang-Suen style binary thinning.")
    add_common_arguments(parser, "ch07_thinning.png")
    parser.add_argument("--max-iterations", type=int, default=80)
    args = parser.parse_args()

    image, source = read_binary(args.input)
    result = thin_binary(image, max_iterations=args.max_iterations)
    output = save_image(args.output, result)
    print_result(source, "thin_binary", output)


if __name__ == "__main__":
    main()
