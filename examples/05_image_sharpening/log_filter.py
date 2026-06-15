"""Chapter 5.6 Laplacian of Gaussian filter.

Run:
    python examples/05_image_sharpening/log_filter.py --sigma 1.2 --kernel-size 5
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, normalize_to_uint8, odd_kernel, print_result, read_gray, save_image


def log_edges(image: np.ndarray, sigma: float = 1.2, kernel_size: int = 5) -> np.ndarray:
    """Smooth with Gaussian first, then use Laplacian to highlight zero-crossing neighborhoods."""
    ksize = odd_kernel(kernel_size)
    blurred = cv2.GaussianBlur(image, (ksize, ksize), float(sigma))
    laplacian = cv2.Laplacian(blurred.astype(np.float32), cv2.CV_32F, ksize=3)
    return normalize_to_uint8(np.abs(laplacian))


def main() -> None:
    parser = argparse.ArgumentParser(description="LoG edge detection.")
    add_common_arguments(parser, "ch05_log_edges.png")
    parser.add_argument("--sigma", type=float, default=1.2, help="Gaussian sigma before Laplacian")
    parser.add_argument("--kernel-size", type=int, default=5, help="odd Gaussian kernel size")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = log_edges(image, sigma=args.sigma, kernel_size=args.kernel_size)
    output = save_image(args.output, result)
    print_result(source, "log_edges", output)


if __name__ == "__main__":
    main()
