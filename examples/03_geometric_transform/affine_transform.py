"""对应章节：3.3 齐次坐标与图像的仿射变换

运行方式：
    python examples/03_geometric_transform/affine_transform.py --dx 18 --dy 12 --angle 12 --scale 0.95 --shear-x 0.15
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import add_common_arguments, interpolation_flag, print_result, read_gray, save_image


def affine_transform_image(
    image: np.ndarray,
    dx: float = 18,
    dy: float = 12,
    angle: float = 12,
    scale: float = 0.95,
    shear_x: float = 0.15,
    interpolation: int = cv2.INTER_LINEAR,
) -> np.ndarray:
    height, width = image.shape[:2]
    theta = np.deg2rad(angle)
    cos_t = np.cos(theta) * scale
    sin_t = np.sin(theta) * scale
    matrix = np.float32(
        [
            [cos_t, -sin_t + shear_x, dx],
            [sin_t, cos_t, dy],
        ]
    )
    return cv2.warpAffine(image, matrix, (width, height), flags=interpolation)


def main() -> None:
    parser = argparse.ArgumentParser(description="3.3 仿射变换：组合平移、旋转、缩放和错切。")
    add_common_arguments(parser)
    parser.add_argument("--dx", type=float, default=18)
    parser.add_argument("--dy", type=float, default=12)
    parser.add_argument("--angle", type=float, default=12)
    parser.add_argument("--scale", type=float, default=0.95)
    parser.add_argument("--shear-x", type=float, default=0.15)
    args = parser.parse_args()

    image = read_gray(args.image)
    result = affine_transform_image(
        image,
        dx=args.dx,
        dy=args.dy,
        angle=args.angle,
        scale=args.scale,
        shear_x=args.shear_x,
        interpolation=interpolation_flag(args.interpolation),
    )
    output = save_image(result, args.output, "ch03_affine")
    print_result(args.image, output, "affine_transform_image")


if __name__ == "__main__":
    main()
