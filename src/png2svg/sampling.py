from pathlib import Path
from typing import cast

from PIL import Image


def load_image(path: str | Path) -> Image.Image:
    """Load an image and convert it to RGB mode."""
    with Image.open(path) as source:
        return source.convert("RGB")


def average_hexagon_color(
    image: Image.Image,
    cx: float,
    cy: float,
    radius: float,
) -> tuple[int, int, int]:
    """Return the average RGB color of pixels inside a hexagon."""
    if radius <= 0:
        raise ValueError("Radius must be positive.")

    rgb_image = image.convert("RGB")
    width, height = rgb_image.size

    min_x = max(0, int(cx - radius))
    max_x = min(width - 1, int(cx + radius))
    min_y = max(0, int(cy - radius))
    max_y = min(height - 1, int(cy + radius))

    red_total = 0
    green_total = 0
    blue_total = 0
    pixel_count = 0

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dx = abs(x - cx)
            dy = abs(y - cy)

            # Pointy/flat-top regular hexagon boundary.

            if (
                dx <= radius
                and dy <= (3**0.5) * radius / 2
                and dx + dy / (3**0.5) <= radius
            ):
                pixel = cast(tuple[int, int, int], rgb_image.getpixel((x, y)))
                red, green, blue = pixel
                red_total += red
                green_total += green
                blue_total += blue
                pixel_count += 1

    if pixel_count == 0:
        raise ValueError("No image pixels fall inside the hexagon.")

    return (
        round(red_total / pixel_count),
        round(green_total / pixel_count),
        round(blue_total / pixel_count),
    )
