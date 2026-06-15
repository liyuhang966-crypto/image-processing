from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"

sys.path.insert(0, str(ROOT / "examples"))
from _common import SAMPLE_GRAY, ensure_samples


INTERPOLATION = {
    "nearest": cv2.INTER_NEAREST,
    "linear": cv2.INTER_LINEAR,
    "cubic": cv2.INTER_CUBIC,
    "area": cv2.INTER_AREA,
}


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--image", default=str(SAMPLE_GRAY), help="输入图片路径，默认使用合成灰度样例。")
    parser.add_argument("--output", default=None, help="输出图片路径，默认写入 examples/output/。")
    parser.add_argument(
        "--interpolation",
        choices=sorted(INTERPOLATION),
        default="linear",
        help="重采样插值方式。",
    )


def read_gray(path: str | Path) -> np.ndarray:
    ensure_samples()
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(path)
    return image


def save_image(image: np.ndarray, output: str | Path | None, name: str) -> Path:
    output_path = Path(output) if output else OUTPUT_DIR / f"{name}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)
    return output_path


def interpolation_flag(name: str) -> int:
    return INTERPOLATION[name]


def print_result(source: str | Path, output: Path, operation: str) -> None:
    print(f"source={source}")
    print(f"operation={operation}")
    print(f"output={output}")
