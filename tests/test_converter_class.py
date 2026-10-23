from pathlib import Path

from PIL import Image

from png2svg.converter import PNGToSVGConverter


def test_converter_class_creates_svg(tmp_path: Path) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"
    Image.new("RGB", (20, 20), (255, 0, 0)).save(input_path)

    converter = PNGToSVGConverter(radius=5)
    converter.convert(input_path, output_path)

    assert output_path.exists()
    assert "<svg" in output_path.read_text(encoding="utf-8")


def test_converter_class_supports_triangle_shape(tmp_path: Path) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"
    Image.new("RGB", (20, 20), (255, 0, 0)).save(input_path)

    converter = PNGToSVGConverter(radius=5, shape="triangle")
    converter.convert(input_path, output_path)

    svg = output_path.read_text(encoding="utf-8")
    assert "<polygon" in svg


def test_converter_class_rejects_invalid_radius() -> None:
    import pytest

    with pytest.raises(ValueError, match="Radius"):
        PNGToSVGConverter(radius=0)
