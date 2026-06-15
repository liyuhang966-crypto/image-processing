"""Shared drawing helpers for chapter 11 deep learning demos."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "examples" / "output"


def add_output_argument(parser: argparse.ArgumentParser, output_name: str) -> None:
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR / output_name)


def canvas(width: int = 760, height: int = 320) -> np.ndarray:
    return np.full((height, width, 3), 255, dtype=np.uint8)


def draw_blocks(labels: list[str], title: str, width: int = 760, height: int = 320) -> np.ndarray:
    image = canvas(width, height)
    cv2.putText(image, title, (24, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2)
    step = (width - 80) // max(len(labels), 1)
    y = height // 2 - 40
    for index, label in enumerate(labels):
        x = 38 + index * step
        cv2.rectangle(image, (x, y), (x + 95, y + 80), (37, 99, 235), 2)
        cv2.putText(image, label, (x + 8, y + 46), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (20, 20, 20), 1)
        if index < len(labels) - 1:
            cv2.arrowedLine(image, (x + 102, y + 40), (x + step - 8, y + 40), (80, 80, 80), 2)
    return image


def save_image(path: Path, image: np.ndarray) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    return path


def print_result(operation: str, output: Path) -> None:
    print(f"operation={operation}")
    print(f"output={output}")
