from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
SAMPLE_NOISY = ROOT / "assets" / "sample_images" / "sample_noisy.png"

sys.path.insert(0, str(ROOT / "examples"))
from _common import SAMPLE_GRAY, ensure_samples


def ensure_noisy_sample() -> None:
    ensure_samples()
    SAMPLE_NOISY.parent.mkdir(parents=True, exist_ok=True)
    if SAMPLE_NOISY.exists():
        return
    image = cv2.imread(str(SAMPLE_GRAY), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(SAMPLE_GRAY)
    rng = np.random.default_rng(42)
    gaussian = rng.normal(0, 18, image.shape).astype(np.float32)
    noisy = np.clip(image.astype(np.float32) + gaussian, 0, 255).astype(np.uint8)
    salt_pepper = rng.random(image.shape)
    noisy[salt_pepper < 0.015] = 0
    noisy[salt_pepper > 0.985] = 255
    cv2.imwrite(str(SAMPLE_NOISY), noisy)


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--image", default=str(SAMPLE_NOISY), help="输入图片路径，默认使用合成噪声图。")
    parser.add_argument("--output", default=None, help="输出图片路径，默认写入 examples/output/。")


def read_gray(path: str | Path) -> np.ndarray:
    ensure_noisy_sample()
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(path)
    return image


def save_image(image: np.ndarray, output: str | Path | None, name: str) -> Path:
    output_path = Path(output) if output else OUTPUT_DIR / f"{name}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)
    return output_path


def odd_kernel(value: int) -> int:
    value = max(1, int(value))
    return value if value % 2 == 1 else value + 1


def print_result(source: str | Path, output: Path, operation: str) -> None:
    print(f"source={source}")
    print(f"operation={operation}")
    print(f"output={output}")
