"""Command-line interface for png2svg."""

import argparse
from pathlib import Path

from png2svg.conversion import convert_image_to_svg


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="png2svg",
        description="Convert an image into a hexagonal or triangular SVG mosaic.",
    )

    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the input image.",
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="Path for the generated SVG file.",
    )
    parser.add_argument(
        "--radius",
        type=float,
        default=10.0,
        help="Radius of each shape (default: 10).",
    )
    parser.add_argument(
        "--shape",
        choices=("hexagon", "triangle"),
        default="hexagon",
        help="Mosaic shape: hexagon (default) or triangle.",
    )

    return parser


def main() -> None:
    """Parse arguments and convert the input image to SVG."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.input_path.is_file():
        parser.error(f"Input image does not exist: {args.input_path}")

    if args.radius <= 0:
        parser.error("--radius must be positive.")

    try:
        args.output_path.parent.mkdir(parents=True, exist_ok=True)
        convert_image_to_svg(
            args.input_path,
            args.output_path,
            radius=args.radius,
            shape=args.shape,
        )
    except (ValueError, OSError) as error:
        parser.error(str(error))

    print(f"SVG saved to: {args.output_path}")


if __name__ == "__main__":
    main()
