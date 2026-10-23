import pytest

from png2svg.palette import distribute_palette, map_to_palette


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


def test_distribute_palette_respects_weights() -> None:
    palette = [(0, 0, 0), (255, 255, 255)]

    result = distribute_palette(palette, [3, 1], count=8)

    assert result.count((0, 0, 0)) == 6
    assert result.count((255, 255, 255)) == 2


def test_distribute_palette_returns_requested_count() -> None:
    palette = [(255, 0, 0), (0, 0, 255)]

    result = distribute_palette(palette, [1, 1], count=7)

    assert len(result) == 7


def test_distribute_palette_rejects_mismatched_weights() -> None:
    palette = [(0, 0, 0), (255, 255, 255)]

    with pytest.raises(ValueError, match="weight"):
        distribute_palette(palette, [1], count=4)


def test_distribute_palette_rejects_zero_total_weight() -> None:
    palette = [(0, 0, 0), (255, 255, 255)]

    with pytest.raises(ValueError, match="weight"):
        distribute_palette(palette, [0, 0], count=4)


def test_distribute_palette_rejects_negative_weights() -> None:
    palette = [(0, 0, 0), (255, 255, 255)]

    with pytest.raises(ValueError, match="weight"):
        distribute_palette(palette, [2, -1], count=4)


def test_distribute_palette_rejects_negative_count() -> None:
    palette = [(0, 0, 0)]

    with pytest.raises(ValueError, match="count"):
        distribute_palette(palette, [1], count=-1)
