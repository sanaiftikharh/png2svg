import math
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


def average_triangle_color(
    image: Image.Image,
    cx: float,
    cy: float,
    radius: float,
    inverted: bool = False,
) -> tuple[int, int, int]:
    """Return the average RGB color of pixels inside an equilateral triangle."""
    if radius <= 0:
        raise ValueError("Radius must be positive.")

    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    start_angle = 90 if inverted else -90

    vertices = [
        (
            cx + radius * math.cos(math.radians(start_angle + index * 120)),
            cy + radius * math.sin(math.radians(start_angle + index * 120)),
        )
        for index in range(3)
    ]

    (ax, ay), (bx, by), (cx2, cy2) = vertices
    double_area = (bx - ax) * (cy2 - ay) - (by - ay) * (cx2 - ax)

    if double_area == 0:
        raise ValueError("Triangle has no area.")

    red_total = 0
    green_total = 0
    blue_total = 0
    pixel_count = 0

    min_x = max(0, int(cx - radius))
    max_x = min(width - 1, int(cx + radius))
    min_y = max(0, int(cy - radius))
    max_y = min(height - 1, int(cy + radius))

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            denominator = (by - cy2) * (ax - cx2) + (cx2 - bx) * (ay - cy2)

            w0 = ((by - cy2) * (x - cx2) + (cx2 - bx) * (y - cy2)) / denominator

            w1 = ((cy2 - ay) * (x - cx2) + (ax - cx2) * (y - cy2)) / denominator

            w2 = 1.0 - w0 - w1

            if min(w0, w1, w2) >= -1e-10:
                red, green, blue = cast(
                    tuple[int, int, int],
                    rgb_image.getpixel((x, y)),
                )
                red_total += red
                green_total += green
                blue_total += blue
                pixel_count += 1

    if pixel_count == 0:
        raise ValueError("No image pixels fall inside the triangle.")

    return (
        round(red_total / pixel_count),
        round(green_total / pixel_count),
        round(blue_total / pixel_count),
    )
