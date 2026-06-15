"""Chapter 9.3.4 wavelet denoising."""

from __future__ import annotations

import argparse

import numpy as np
import pywt

from _utils import add_common_arguments, print_result, read_gray, save_image


def wavelet_denoise_image(image: np.ndarray, wavelet: str = "haar", threshold: float = 12.0) -> np.ndarray:
    coeffs = pywt.wavedec2(image.astype(np.float32), wavelet, level=2)
    filtered = [coeffs[0]]
    for detail in coeffs[1:]:
        filtered.append(tuple(pywt.threshold(part, threshold, mode="soft") for part in detail))
    reconstructed = pywt.waverec2(filtered, wavelet)
    return np.clip(reconstructed[: image.shape[0], : image.shape[1]], 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wavelet soft-threshold denoising.")
    add_common_arguments(parser, "ch09_wavelet_denoising.png")
    parser.add_argument("--wavelet", default="haar")
    parser.add_argument("--threshold", type=float, default=12.0)
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, wavelet_denoise_image(image, args.wavelet, args.threshold))
    print_result(source, "wavelet_denoise_image", output)


if __name__ == "__main__":
    main()
