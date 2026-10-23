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


def triangle_vertices(
    cx: float,
    cy: float,
    radius: float,
    inverted: bool = False,
) -> list[tuple[float, float]]:
    """Calculate the three vertices of an equilateral triangle.

    Args:
        cx: X-coordinate of the triangle's center.
        cy: Y-coordinate of the triangle's center.
        radius: Distance from the center to each vertex.
        inverted: Whether the triangle points downward.

    Returns:
        Three (x, y) vertex coordinates.

    Raises:
        ValueError: If radius is not positive.
    """
    if radius <= 0:
        raise ValueError("Radius must be positive.")

    start_angle = 90 if inverted else -90

    return [
        (
            cx + radius * math.cos(math.radians(start_angle + i * 120)),
            cy + radius * math.sin(math.radians(start_angle + i * 120)),
        )
        for i in range(3)
    ]
