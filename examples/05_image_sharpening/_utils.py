"""Shared helpers for chapter 5 sharpening examples."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_GRAY = ROOT / "assets" / "sample_images" / "sample_gray.png"
DEFAULT_OUTPUT_DIR = ROOT / "examples" / "output"


def ensure_sample() -> None:
    if SAMPLE_GRAY.exists():
        return
    SAMPLE_GRAY.parent.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0, 255, 256, dtype=np.uint8)
    image = np.tile(x, (256, 1))
    cv2.circle(image, (128, 128), 60, 220, -1)
    cv2.rectangle(image, (30, 40), (90, 110), 55, -1)
    cv2.imwrite(str(SAMPLE_GRAY), image)


def add_common_arguments(parser: argparse.ArgumentParser, output_name: str) -> None:
    parser.add_argument("--input", type=Path, default=SAMPLE_GRAY, help="input image path")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / output_name,
        help="output image path",
    )


def read_gray(path: Path) -> tuple[np.ndarray, Path]:
    ensure_sample()
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(path)
    return image, path


def normalize_to_uint8(image: np.ndarray) -> np.ndarray:
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def odd_kernel(value: int) -> int:
    value = max(1, int(value))
    return value if value % 2 else value + 1


def save_image(path: Path, image: np.ndarray) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    return path


def print_result(source: Path, operation: str, output: Path) -> None:
    print(f"source={source}")
    print(f"operation={operation}")
    print(f"output={output}")
