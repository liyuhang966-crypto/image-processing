"""Chapter 9.1.1 one-dimensional Fourier transform."""

from __future__ import annotations

import argparse

import numpy as np

from _utils import add_common_arguments, normalize_uint8, print_result, read_gray, save_image


def one_dimensional_spectrum(image: np.ndarray, row: int | None = None) -> np.ndarray:
    row_index = image.shape[0] // 2 if row is None else min(max(row, 0), image.shape[0] - 1)
    signal = image[row_index].astype(np.float32)
    spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft(signal))))
    return normalize_uint8(np.tile(spectrum, (96, 1)))


def main() -> None:
    parser = argparse.ArgumentParser(description="1D Fourier spectrum from one image row.")
    add_common_arguments(parser, "ch09_one_dimensional_spectrum.png")
    parser.add_argument("--row", type=int)
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, one_dimensional_spectrum(image, args.row))
    print_result(source, "one_dimensional_spectrum", output)


if __name__ == "__main__":
    main()
