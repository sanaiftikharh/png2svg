import math

import pytest

from png2svg.geometry import hexagon_vertices, triangle_vertices


def test_returns_six_vertices():
    vertices = hexagon_vertices(cx=10, cy=20, radius=5)

    assert len(vertices) == 6


def test_first_vertex_is_to_the_right_of_center():
    vertices = hexagon_vertices(cx=10, cy=20, radius=5)

    assert vertices[0] == pytest.approx((15, 20))


def test_vertices_have_expected_coordinates():
    vertices = hexagon_vertices(cx=0, cy=0, radius=2)

    expected = [
        (2, 0),
        (1, math.sqrt(3)),
        (-1, math.sqrt(3)),
        (-2, 0),
        (-1, -math.sqrt(3)),
        (1, -math.sqrt(3)),
    ]

    for actual, expected_vertex in zip(vertices, expected):
        assert actual == pytest.approx(expected_vertex)


def test_every_vertex_is_radius_distance_from_center():
    cx, cy, radius = 10, 20, 5
    vertices = hexagon_vertices(cx=cx, cy=cy, radius=radius)

    for x, y in vertices:
        distance = math.hypot(x - cx, y - cy)
        assert distance == pytest.approx(radius)


def test_rejects_non_positive_radius():
    with pytest.raises(ValueError):
        hexagon_vertices(cx=0, cy=0, radius=0)

    with pytest.raises(ValueError):
        hexagon_vertices(cx=0, cy=0, radius=-1)


def test_triangle_vertices_returns_three_points() -> None:
    vertices = triangle_vertices(10, 20, 5)

    assert len(vertices) == 3


def test_triangle_vertices_are_equilateral() -> None:
    vertices = triangle_vertices(10, 20, 5)

    def distance(
        first: tuple[float, float],
        second: tuple[float, float],
    ) -> float:
        return ((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2) ** 0.5

    assert distance(vertices[0], vertices[1]) == pytest.approx(
        distance(vertices[1], vertices[2])
    )
    assert distance(vertices[1], vertices[2]) == pytest.approx(
        distance(vertices[2], vertices[0])
    )


def test_triangle_vertices_rejects_nonpositive_radius() -> None:
    with pytest.raises(ValueError, match="positive"):
        triangle_vertices(0, 0, 0)
