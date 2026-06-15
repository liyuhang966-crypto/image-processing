"""Shared helpers for chapter 8 color image processing examples."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_COLOR = ROOT / "assets" / "sample_images" / "sample_color.png"
DEFAULT_OUTPUT_DIR = ROOT / "examples" / "output"


def ensure_sample() -> None:
    if SAMPLE_COLOR.exists():
        return
    SAMPLE_COLOR.parent.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0, 255, 256, dtype=np.uint8)
    gray = np.tile(x, (256, 1))
    cv2.circle(gray, (128, 128), 60, 220, -1)
    cv2.rectangle(gray, (30, 40), (90, 110), 55, -1)
    color = cv2.merge([gray, np.flipud(gray), np.roll(gray, 50, axis=1)])
    cv2.imwrite(str(SAMPLE_COLOR), color)


def add_common_arguments(parser: argparse.ArgumentParser, output_name: str) -> None:
    parser.add_argument("--input", type=Path, default=SAMPLE_COLOR, help="input color image path")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / output_name,
        help="output image path",
    )


def read_color(path: Path) -> tuple[np.ndarray, Path]:
    ensure_sample()
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(path)
    return image, path


def save_image(path: Path, image: np.ndarray) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    return path


def print_result(source: Path, operation: str, output: Path) -> None:
    print(f"source={source}")
    print(f"operation={operation}")
    print(f"output={output}")
