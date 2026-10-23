
from collections.abc import Sequence
from pathlib import Path

from png2svg.conversion import convert_image_to_svg

Color = tuple[int, int, int]


class PNGToSVGConverter:
    """Convert images to SVG mosaics using reusable settings."""

    def __init__(
        self,
        radius: float = 10,
        shape: str = "hexagon",
        palette: Sequence[Color] | None = None,
    ) -> None:
        if radius <= 0:
            raise ValueError("Radius must be positive.")

        if shape not in {"hexagon", "triangle"}:
            raise ValueError("Invalid shape: choose 'hexagon' or 'triangle'.")

        if palette is not None and not palette:
            raise ValueError("Palette must contain at least one color.")

        self.radius = radius
        self.shape = shape
        self.palette = palette

    def convert(
        self,
        input_path: str | Path,
        output_path: str | Path,
    ) -> None:
        """Convert an image using the configured settings."""
        convert_image_to_svg(
            input_path,
            output_path,
            radius=self.radius,
            shape=self.shape,
            palette=self.palette,
        )
