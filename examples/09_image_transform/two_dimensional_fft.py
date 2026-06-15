"""Chapter 9.1.2 two-dimensional FFT."""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, normalize_uint8, print_result, read_gray, save_image


def two_dimensional_spectrum(image: np.ndarray) -> np.ndarray:
    spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image.astype(np.float32)))))
    return normalize_uint8(spectrum)


def main() -> None:
    parser = argparse.ArgumentParser(description="2D FFT magnitude spectrum.")
    add_common_arguments(parser, "ch09_two_dimensional_fft.png")
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, two_dimensional_spectrum(image))
    print_result(source, "two_dimensional_spectrum", output)


if __name__ == "__main__":
    main()
