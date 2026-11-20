from pathlib import Path

import pytest
from PIL import Image

from png2svg.sampling import average_hexagon_color, average_triangle_color, load_image


def test_load_image_returns_rgb_image(tmp_path):
    path = tmp_path / "test.png"
    Image.new("RGBA", (10, 10), (255, 0, 0, 128)).save(path)

    image = load_image(path)

    assert image.mode == "RGB"
    assert image.size == (10, 10)
    assert image.getpixel((0, 0)) == (255, 0, 0)


def test_load_real_png_image():
    image_path = Path("examples/sample.jpg")
    image = load_image(image_path)
    assert image.mode == "RGB"
    assert image.width > 0
    assert image.height > 0


def test_average_color_of_uniform_hexagon():
    image = Image.new("RGB", (20, 20), (100, 150, 200))

    color = average_hexagon_color(image, cx=10, cy=10, radius=5)

    assert color == (100, 150, 200)


def test_average_color_ignores_pixels_outside_hexagon():
    image = Image.new("RGB", (5, 5), (255, 255, 255))
    image.putpixel((0, 0), (0, 0, 0))

    color = average_hexagon_color(image, cx=2, cy=2, radius=2)

    assert color == (255, 255, 255)


def test_average_color_rejects_non_positive_radius():
    image = Image.new("RGB", (10, 10), (100, 100, 100))

    with pytest.raises(ValueError):
        average_hexagon_color(image, cx=5, cy=5, radius=0)

    with pytest.raises(ValueError):
        average_hexagon_color(image, cx=5, cy=5, radius=-1)


def test_average_color_rejects_hexagon_with_no_pixels():
    image = Image.new("RGB", (10, 10), (100, 100, 100))

    with pytest.raises(ValueError):
        average_hexagon_color(image, cx=100, cy=100, radius=2)


def test_average_triangle_color_samples_only_triangle_pixels():
    image = Image.new("RGB", (10, 10), (255, 255, 255))

    for y in range(10):
        for x in range(5):
            image.putpixel((x, y), (0, 0, 0))

    color = average_triangle_color(
        image,
        cx=5,
        cy=5,
        radius=4,
    )

    assert color != (255, 255, 255)


def test_average_triangle_color_rejects_zero_radius():
    image = Image.new("RGB", (10, 10), (100, 100, 100))

    with pytest.raises(ValueError, match="positive"):
        average_triangle_color(image, 5, 5, 0)


def test_average_triangle_rejects_shape_outside_image():
    image = Image.new("RGB", (10, 10), (100, 100, 100))

    with pytest.raises(
        ValueError,
        match="No image pixels fall inside the triangle",
    ):
        average_triangle_color(
            image,
            cx=-20,
            cy=-20,
            radius=2,
        )
