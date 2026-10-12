import math


def hexagon_vertices(
    cx: float,
    cy: float,
    radius: float,
) -> list[tuple[float, float]]:
    """Calculate the six vertices of a regular hexagon.

    Args:
        cx: X-coordinate of the hexagon's center.
        cy: Y-coordinate of the hexagon's center.
        radius: Distance from the center to each vertex.

    Returns:
        Six (x, y) vertex coordinates in counterclockwise
        mathematical angle order, starting from the right.

    Raises:
        ValueError: If radius is not positive.
    """
    if radius <= 0:
        raise ValueError("Radius must be positive.")

    vertices = []

    for i in range(6):
        angle = math.radians(i * 60)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vertices.append((x, y))

    return vertices
