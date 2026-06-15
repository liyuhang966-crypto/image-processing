"""Chapter 11.3.2 AlexNet structure demo."""

from __future__ import annotations

import argparse

from _utils import add_output_argument, draw_blocks, print_result, save_image


def draw_alexnet_structure() -> object:
    return draw_blocks(["Input", "Conv\nstack", "ReLU", "Pool", "Dropout", "FC"], "AlexNet deeper CNN structure")


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw AlexNet structure.")
    add_output_argument(parser, "ch11_alexnet_structure.png")
    args = parser.parse_args()
    output = save_image(args.output, draw_alexnet_structure())
    print_result("draw_alexnet_structure", output)


if __name__ == "__main__":
    main()
