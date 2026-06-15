"""Shared helpers for chapter 6 segmentation examples."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_SEGMENTS = ROOT / "assets" / "sample_images" / "sample_segments.png"
DEFAULT_OUTPUT_DIR = ROOT / "examples" / "output"


def ensure_sample() -> None:
    if SAMPLE_SEGMENTS.exists():
        return
    SAMPLE_SEGMENTS.parent.mkdir(parents=True, exist_ok=True)
    image = np.full((256, 256), 45, dtype=np.uint8)
    cv2.circle(image, (85, 120), 45, 165, -1)
    cv2.rectangle(image, (145, 70), (220, 170), 220, -1)
    cv2.ellipse(image, (145, 190), (55, 22), 0, 0, 360, 110, -1)
    rng = np.random.default_rng(6)
    noise = rng.normal(0, 8, image.shape)
    cv2.imwrite(str(SAMPLE_SEGMENTS), np.clip(image.astype(float) + noise, 0, 255).astype(np.uint8))


def add_common_arguments(parser: argparse.ArgumentParser, output_name: str) -> None:
    parser.add_argument("--input", type=Path, default=SAMPLE_SEGMENTS, help="input image path")
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


def save_image(path: Path, image: np.ndarray) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    return path


def print_result(source: Path, operation: str, output: Path, threshold: float | None = None) -> None:
    print(f"source={source}")
    print(f"operation={operation}")
    if threshold is not None:
        print(f"threshold={threshold:.3f}")
    print(f"output={output}")
