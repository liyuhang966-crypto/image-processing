"""Chapter 9.2.3 wavelet decomposition and reconstruction."""

from __future__ import annotations

import argparse

import numpy as np
import pywt

from _utils import add_common_arguments, normalize_uint8, print_result, read_gray, save_image


def wavelet_decompose_image(image: np.ndarray, wavelet: str = "haar") -> np.ndarray:
    coeffs = pywt.dwt2(image.astype(np.float32), wavelet)
    ll, (lh, hl, hh) = coeffs
    top = np.hstack([normalize_uint8(ll), normalize_uint8(lh)])
    bottom = np.hstack([normalize_uint8(hl), normalize_uint8(hh)])
    return np.vstack([top, bottom])


def main() -> None:
    parser = argparse.ArgumentParser(description="Single-level 2D wavelet decomposition.")
    add_common_arguments(parser, "ch09_wavelet_decomposition.png")
    parser.add_argument("--wavelet", default="haar")
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, wavelet_decompose_image(image, args.wavelet))
    print_result(source, "wavelet_decompose_image", output)


if __name__ == "__main__":
    main()
