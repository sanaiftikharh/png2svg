"""Convert raster images into SVG wallpapers."""

from png2svg.conversion import convert_image_to_svg
from png2svg.converter import PNGToSVGConverter

__version__ = "0.1.0"
__all__ = [
    "PNGToSVGConverter",
    "convert_image_to_svg",
]
