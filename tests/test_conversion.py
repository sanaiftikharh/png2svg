
from xml.etree import ElementTree as ET

import pytest
from PIL import Image

from png2svg.conversion import convert_image_to_svg


def test_conversion_creates_svg_file(tmp_path) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"

    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_path)

    convert_image_to_svg(input_path, output_path, radius=5)

    assert output_path.exists()

    root = ET.parse(output_path).getroot()
    assert root.attrib["width"] == "30"
    assert root.attrib["height"] == "30"


def test_conversion_generates_colored_hexagons(tmp_path) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"

    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_path)

    convert_image_to_svg(input_path, output_path, radius=5)

    root = ET.parse(output_path).getroot()
    polygons = [
        element
        for element in root.iter()
        if element.tag.endswith("polygon")
    ]

    assert len(polygons) > 0
    assert all(polygon.attrib["fill"] == "#ff0000" for polygon in polygons)


def test_conversion_rejects_invalid_radius(tmp_path) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"

    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_path)

    with pytest.raises(ValueError):
        convert_image_to_svg(input_path, output_path, radius=0)


def test_conversion_rejects_missing_input(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        convert_image_to_svg(
            tmp_path / "missing.png",
            tmp_path / "output.svg",
            radius=5,
        )
