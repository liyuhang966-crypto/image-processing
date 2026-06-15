"""Chapter 11.4.2 YOLO concept demo."""

from __future__ import annotations

import argparse

import cv2

from _utils import add_output_argument, canvas, print_result, save_image


def draw_yolo_concept() -> object:
    image = canvas(640, 360)
    cv2.putText(image, "YOLO: grid cells predict boxes and classes", (24, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 20), 2)
    for x in range(80, 561, 80):
        cv2.line(image, (x, 70), (x, 310), (210, 210, 210), 1)
    for y in range(70, 311, 60):
        cv2.line(image, (80, y), (560, y), (210, 210, 210), 1)
    cv2.rectangle(image, (185, 130), (315, 235), (37, 99, 235), 3)
    cv2.rectangle(image, (365, 105), (505, 250), (22, 163, 74), 3)
    cv2.putText(image, "box + class", (195, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (37, 99, 235), 1)
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw YOLO concept.")
    add_output_argument(parser, "ch11_yolo_concept.png")
    args = parser.parse_args()
    output = save_image(args.output, draw_yolo_concept())
    print_result("draw_yolo_concept", output)


if __name__ == "__main__":
    main()
