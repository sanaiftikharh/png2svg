
import math

import pytest

from png2svg.geometry import hexagon_vertices


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