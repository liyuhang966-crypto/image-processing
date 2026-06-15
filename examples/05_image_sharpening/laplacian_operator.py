"""Chapter 5.3.1 Laplacian differential operator.

Run:
    python examples/05_image_sharpening/laplacian_operator.py --amount 0.7 --kernel-size 3
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, odd_kernel, print_result, read_gray, save_image


def laplacian_sharpen(image: np.ndarray, amount: float = 0.7, kernel_size: int = 3) -> np.ndarray:
    """Sharpen by subtracting a scaled second derivative response from the image."""
    gray = image.astype(np.float32)
    laplacian = cv2.Laplacian(gray, cv2.CV_32F, ksize=odd_kernel(kernel_size))
    sharpened = gray - float(amount) * laplacian
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Laplacian image sharpening.")
    add_common_arguments(parser, "ch05_laplacian_sharpen.png")
    parser.add_argument("--amount", type=float, default=0.7, help="second-derivative sharpening amount")
    parser.add_argument("--kernel-size", type=int, default=3, help="odd Laplacian kernel size")
    args = parser.parse_args()

    image, source = read_gray(args.input)
    result = laplacian_sharpen(image, amount=args.amount, kernel_size=args.kernel_size)
    output = save_image(args.output, result)
    print_result(source, "laplacian_sharpen", output)


if __name__ == "__main__":
    main()
