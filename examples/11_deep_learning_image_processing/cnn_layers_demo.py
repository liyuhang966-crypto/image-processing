"""Chapter 11.1 CNN layers demo."""

from __future__ import annotations

import argparse

from _utils import add_output_argument, draw_blocks, print_result, save_image


def draw_cnn_layers() -> object:
    return draw_blocks(["Input", "Conv", "BN", "ReLU", "Pool", "Head"], "CNN basic layer pipeline")


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw CNN layer pipeline.")
    add_output_argument(parser, "ch11_cnn_layers_demo.png")
    args = parser.parse_args()
    output = save_image(args.output, draw_cnn_layers())
    print_result("draw_cnn_layers", output)


if __name__ == "__main__":
    main()
