from pathlib import Path

from png2svg.geometry import hexagon_vertices, triangle_vertices
from png2svg.sampling import average_hexagon_color, load_image
from png2svg.svg import generate_svg, save_svg


def convert_image_to_svg(
    input_path: str | Path,
    output_path: str | Path,
    radius: float = 10,
    shape: str = "hexagon",
) -> None:
    """Convert an image into a hexagonal or triangular SVG mosaic."""
    if radius <= 0:
        raise ValueError("Radius must be positive.")

    if shape not in {"hexagon", "triangle"}:
        raise ValueError("Invalid shape: choose 'hexagon' or 'triangle'.")

    image = load_image(input_path)
    width, height = image.size
    polygons = []

    if shape == "hexagon":
        horizontal_step = 1.5 * radius
        vertical_step = 3**0.5 * radius

        column = 0
        cx = 0.0

        while cx < width:
            offset_y = (column % 2) * vertical_step / 2
            cy = offset_y

            while cy < height:
                vertices = hexagon_vertices(cx, cy, radius)
                color = average_hexagon_color(image, cx, cy, radius)
                polygons.append((vertices, color))
                cy += vertical_step

            cx += horizontal_step
            column += 1

    else:
        horizontal_step = 3**0.5 * radius
        vertical_step = 1.5 * radius

        row = 0
        cy = 0.0

        while cy < height:
            offset_x = (row % 2) * horizontal_step / 2
            cx = offset_x
            column = 0

            while cx < width:
                inverted = (row + column) % 2 == 1
                vertices = triangle_vertices(
                    cx,
                    cy,
                    radius,
                    inverted=inverted,
                )
                color = average_hexagon_color(image, cx, cy, radius)
                polygons.append((vertices, color))
                cx += horizontal_step
                column += 1

            cy += vertical_step
            row += 1

    svg_content = generate_svg(width, height, polygons)
    save_svg(svg_content, output_path)
