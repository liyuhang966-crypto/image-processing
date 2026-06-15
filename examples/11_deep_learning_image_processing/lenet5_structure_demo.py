"""Chapter 11.3.1 LeNet-5 structure demo."""

from __future__ import annotations

import argparse

from _utils import add_output_argument, draw_blocks, print_result, save_image


def draw_lenet5_structure() -> object:
    return draw_blocks(["Input", "C1", "S2", "C3", "S4", "FC"], "LeNet-5 classification structure")


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw LeNet-5 structure.")
    add_output_argument(parser, "ch11_lenet5_structure.png")
    args = parser.parse_args()
    output = save_image(args.output, draw_lenet5_structure())
    print_result("draw_lenet5_structure", output)


if __name__ == "__main__":
    main()
