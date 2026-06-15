"""Chapter 11.2.1 SRCNN structure demo."""

from __future__ import annotations

import argparse

from _utils import add_output_argument, draw_blocks, print_result, save_image


def draw_srcnn_structure() -> object:
    return draw_blocks(["LR image", "Patch\nextract", "Nonlinear\nmap", "Reconstruct", "SR image"], "SRCNN super-resolution idea")


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw SRCNN structure.")
    add_output_argument(parser, "ch11_srcnn_structure.png")
    args = parser.parse_args()
    output = save_image(args.output, draw_srcnn_structure())
    print_result("draw_srcnn_structure", output)


if __name__ == "__main__":
    main()
