"""对应章节：3.4 图像几何畸变的校正

运行方式：
    python examples/03_geometric_transform/geometric_correction.py --strength 0.18
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, interpolation_flag, print_result, read_gray, save_image


def correct_geometric_distortion(
    image: np.ndarray,
    strength: float = 0.18,
    interpolation: int = cv2.INTER_LINEAR,
) -> np.ndarray:
    height, width = image.shape[:2]
    y, x = np.indices((height, width), dtype=np.float32)
    cx, cy = width / 2.0, height / 2.0
    xn = (x - cx) / cx
    yn = (y - cy) / cy
    r2 = xn * xn + yn * yn
    factor = 1 + strength * r2
    map_x = (cx + xn * cx * factor).astype(np.float32)
    map_y = (cy + yn * cy * factor).astype(np.float32)
    return cv2.remap(image, map_x, map_y, interpolation=interpolation, borderMode=cv2.BORDER_CONSTANT)


def main() -> None:
    parser = argparse.ArgumentParser(description="3.4 几何畸变校正：用径向映射演示校正思想。")
    add_common_arguments(parser)
    parser.add_argument("--strength", type=float, default=0.18, help="径向校正强度，正负值对应不同畸变方向。")
    args = parser.parse_args()

    image = read_gray(args.image)
    result = correct_geometric_distortion(
        image,
        strength=args.strength,
        interpolation=interpolation_flag(args.interpolation),
    )
    output = save_image(result, args.output, "ch03_geometric_correction")
    print_result(args.image, output, "correct_geometric_distortion")


if __name__ == "__main__":
    main()
