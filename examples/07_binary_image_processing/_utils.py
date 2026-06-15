"""Shared helpers for chapter 7 binary image processing examples."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_BINARY = ROOT / "assets" / "sample_images" / "sample_binary.png"
DEFAULT_OUTPUT_DIR = ROOT / "examples" / "output"


def ensure_sample() -> None:
    if SAMPLE_BINARY.exists():
        return
    SAMPLE_BINARY.parent.mkdir(parents=True, exist_ok=True)
    image = np.zeros((256, 256), dtype=np.uint8)
    cv2.rectangle(image, (35, 45), (110, 140), 255, -1)
    cv2.circle(image, (170, 95), 42, 255, -1)
    cv2.ellipse(image, (135, 185), (70, 24), 0, 0, 360, 255, -1)
    image[58:66, 58:66] = 0
    image[90:104, 85:99] = 0
    for x, y in [(25, 210), (45, 205), (225, 55), (220, 205), (72, 23)]:
        cv2.circle(image, (x, y), 3, 255, -1)
    cv2.imwrite(str(SAMPLE_BINARY), image)


def add_common_arguments(parser: argparse.ArgumentParser, output_name: str) -> None:
    parser.add_argument("--input", type=Path, default=SAMPLE_BINARY, help="input binary image path")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / output_name,
        help="output image path",
    )


def read_binary(path: Path) -> tuple[np.ndarray, Path]:
    ensure_sample()
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(path)
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary, path


def kernel(size: int) -> np.ndarray:
    size = max(1, int(size))
    if size % 2 == 0:
        size += 1
    return np.ones((size, size), dtype=np.uint8)


def save_image(path: Path, image: np.ndarray) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    return path


def print_result(source: Path, operation: str, output: Path) -> None:
    print(f"source={source}")
    print(f"operation={operation}")
    print(f"output={output}")
