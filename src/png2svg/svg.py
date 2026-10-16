from collections.abc import Iterable, Sequence
from pathlib import Path

Point = tuple[float, float]
Color = tuple[int, int, int]
Hexagon = tuple[Sequence[Point], Color]


def generate_svg(
    width: int,
    height: int,
    hexagons: Iterable[Hexagon],
) -> str:
    """Generate an SVG document containing colored hexagons.

    Args:
        width: Width of the SVG image in pixels.
        height: Height of the SVG image in pixels.
        hexagons: An iterable of (vertices, RGB color) pairs.

    Returns:
        The complete SVG document as a string.

    Raises:
        ValueError: If dimensions, vertices, or RGB values are invalid.
    """
    if width <= 0 or height <= 0:
        raise ValueError("SVG width and height must be positive.")

    lines = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
        )
    ]

    for vertices, color in hexagons:
        if len(vertices) != 6:
            raise ValueError("Each hexagon must have exactly six vertices.")

        if len(color) != 3 or any(
            not isinstance(channel, int) or not 0 <= channel <= 255 for channel in color
        ):
            raise ValueError("RGB color values must be integers from 0 to 255.")

        points = " ".join(
            f"{format_coordinate(x)},{format_coordinate(y)}" for x, y in vertices
        )

        red, green, blue = color
        fill = f"#{red:02x}{green:02x}{blue:02x}"

        lines.append(f'<polygon points="{points}" fill="{fill}" />')

    lines.append("</svg>")

    return "\n".join(lines)


def format_coordinate(value: float) -> str:
    """Format a coordinate without unnecessary trailing zeros."""
    return f"{value:g}"


def save_svg(
    svg_content: str,
    output_path: str | Path,
) -> None:
    """Save SVG content to a file."""
    Path(output_path).write_text(svg_content, encoding="utf-8")
