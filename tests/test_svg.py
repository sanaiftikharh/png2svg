from xml.etree import ElementTree as ET

import pytest

from png2svg.svg import generate_svg, save_svg


def test_generate_svg_has_correct_dimensions() -> None:
    svg = generate_svg(100, 80, [])

    root = ET.fromstring(svg)

    assert root.attrib["width"] == "100"
    assert root.attrib["height"] == "80"
    assert root.attrib["viewBox"] == "0 0 100 80"


def test_generate_svg_contains_hexagon_with_color() -> None:
    vertices = [
        (10, 0),
        (15, 5),
        (15, 15),
        (10, 20),
        (5, 15),
        (5, 5),
    ]
    hexagons = [(vertices, (255, 0, 0))]

    svg = generate_svg(100, 80, hexagons)
    root = ET.fromstring(svg)

    polygons = [element for element in root.iter() if element.tag.endswith("polygon")]

    assert len(polygons) == 1
    assert polygons[0].attrib["fill"] == "#ff0000"
    assert polygons[0].attrib["points"] == ("10,0 15,5 15,15 10,20 5,15 5,5")


def test_generate_svg_contains_multiple_hexagons() -> None:
    first_vertices = [
        (0, 0),
        (1, 0),
        (2, 1),
        (1, 2),
        (0, 2),
        (-1, 1),
    ]
    second_vertices = [
        (10, 10),
        (11, 10),
        (12, 11),
        (11, 12),
        (10, 12),
        (9, 11),
    ]

    hexagons = [
        (first_vertices, (255, 0, 0)),
        (second_vertices, (0, 255, 0)),
    ]

    svg = generate_svg(100, 80, hexagons)
    root = ET.fromstring(svg)

    polygons = [element for element in root.iter() if element.tag.endswith("polygon")]

    assert len(polygons) == 2
    assert polygons[0].attrib["fill"] == "#ff0000"
    assert polygons[1].attrib["fill"] == "#00ff00"


def test_generate_svg_rejects_non_positive_dimensions() -> None:
    with pytest.raises(ValueError):
        generate_svg(0, 80, [])

    with pytest.raises(ValueError):
        generate_svg(100, -1, [])


def test_generate_svg_rejects_invalid_color() -> None:
    vertices = [
        (10, 0),
        (15, 5),
        (15, 15),
        (10, 20),
        (5, 15),
        (5, 5),
    ]

    with pytest.raises(ValueError):
        generate_svg(100, 80, [(vertices, (256, 0, 0))])


def test_save_svg_writes_file(tmp_path) -> None:
    svg = generate_svg(100, 80, [])
    output_path = tmp_path / "output.svg"

    save_svg(svg, output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == svg
