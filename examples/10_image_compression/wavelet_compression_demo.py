"""Chapter 10.3.2 wavelet compression demo."""

from __future__ import annotations

import argparse

import numpy as np
import pywt

from _utils import add_common_arguments, print_result, read_gray, save_image


def wavelet_compress_demo(image: np.ndarray, wavelet: str = "haar", keep_ratio: float = 0.15) -> np.ndarray:
    coeffs = pywt.wavedec2(image.astype(np.float32), wavelet, level=2)
    array, slices = pywt.coeffs_to_array(coeffs)
    threshold = np.quantile(np.abs(array), 1 - float(keep_ratio))
    compressed = np.where(np.abs(array) >= threshold, array, 0)
    restored = pywt.waverec2(pywt.array_to_coeffs(compressed, slices, output_format="wavedec2"), wavelet)
    return np.clip(restored[: image.shape[0], : image.shape[1]], 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wavelet coefficient threshold compression.")
    add_common_arguments(parser, "ch10_wavelet_compression.png")
    parser.add_argument("--wavelet", default="haar")
    parser.add_argument("--keep-ratio", type=float, default=0.15)
    args = parser.parse_args()
    image, source = read_gray(args.input)
    output = save_image(args.output, wavelet_compress_demo(image, args.wavelet, args.keep_ratio))
    print_result(source, "wavelet_compress_demo", output)


if __name__ == "__main__":
    main()
