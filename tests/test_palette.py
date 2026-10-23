import pytest

from png2svg.palette import map_to_palette


def test_map_to_palette_returns_closest_color() -> None:
    palette = [(0, 0, 0), (255, 255, 255)]

    assert map_to_palette((20, 20, 20), palette) == (0, 0, 0)


def test_map_to_palette_returns_exact_palette_color() -> None:
    palette = [(255, 0, 0), (0, 0, 255)]

    assert map_to_palette((255, 0, 0), palette) == (255, 0, 0)


def test_map_to_palette_rejects_empty_palette() -> None:
    with pytest.raises(ValueError, match="palette"):
        map_to_palette((100, 100, 100), [])


def test_map_to_palette_rejects_invalid_rgb_color() -> None:
    with pytest.raises(ValueError):
        map_to_palette((300, 0, 0), [(0, 0, 0)])
