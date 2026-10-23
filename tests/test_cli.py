import sys
from pathlib import Path

import pytest
from PIL import Image

from png2svg.cli import build_parser, main


def test_parser_accepts_input_and_output_paths() -> None:
    args = build_parser().parse_args(["input.png", "output.svg"])

    assert args.input_path == Path("input.png")
    assert args.output_path == Path("output.svg")


def test_parser_accepts_custom_radius() -> None:
    args = build_parser().parse_args(["input.png", "output.svg", "--radius", "5"])

    assert args.radius == 5.0


def test_parser_uses_default_radius() -> None:
    args = build_parser().parse_args(["input.png", "output.svg"])

    assert args.radius == 10.0


def test_main_creates_svg(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output" / "result.svg"

    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_path)

    monkeypatch.setattr(
        sys,
        "argv",
        ["png2svg", str(input_path), str(output_path)],
    )

    main()

    assert output_path.exists()
    assert "SVG saved to:" in capsys.readouterr().out


def test_main_rejects_missing_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_path = tmp_path / "output.svg"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "png2svg",
            str(tmp_path / "missing.png"),
            str(output_path),
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    assert not output_path.exists()


def test_main_rejects_non_positive_radius(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"

    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_path)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "png2svg",
            str(input_path),
            str(output_path),
            "--radius",
            "0",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    assert not output_path.exists()


def test_cli_grayscale_palette(tmp_path, monkeypatch):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.svg"
    Image.new("RGB", (20, 20), (120, 80, 40)).save(input_path)

    monkeypatch.setattr(
        "sys.argv",
        [
            "png2svg",
            str(input_path),
            str(output_path),
            "--palette",
            "grayscale",
        ],
    )

    main()

    assert output_path.exists()
    svg = output_path.read_text()
    assert "#000000" in svg or "#808080" in svg or "#FFFFFF" in svg


def test_cli_rejects_unknown_palette():
    import pytest

    from png2svg.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["input.png", "output.svg", "--palette", "unknown"])
