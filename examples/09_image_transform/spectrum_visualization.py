"""Chapter 9.1.4 spectrum visualization."""

from __future__ import annotations

import argparse

import cv2
import numpy as np

from _utils import add_common_arguments, normalize_uint8, print_result, read_gray, save_image


def visualize_spectrum(image: np.ndarray, gamma: float = 0.4) -> np.ndarray:
    spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image.astype(np.float32)))))
    normalized = normalize_uint8(spectrum)
    table = np.array([(i / 255) ** gamma * 255 for i in range(256)], dtype=np.uint8)
    return cv2.applyColorMap(cv2.LUT(normalized, table), cv2.COLORMAP_TURBO)


def main() -> None:
    parser = argparse.ArgumentParser(description="Colorized FFT spectrum visualization.")
    add_common_arguments(parser, "ch09_spectrum_visualization.png")
    parser.add_argument("--gamma", type=float, default=0.4)
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, visualize_spectrum(image, args.gamma))
    print_result(source, "visualize_spectrum", output)


if __name__ == "__main__":
    main()
