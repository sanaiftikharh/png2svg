# png2svg

**Convert images into scalable SVG mosaics using geometric shapes and color palettes.**

`png2svg` is a Python package that transforms raster images into SVG artwork by sampling image colors and representing them with geometric shapes. The generated SVG can be scaled without losing quality, making it useful for wallpapers, illustrations, and creative image transformations.

## Features

- **Geometric mosaics:** Convert images into hexagonal or triangular patterns.
- **Adjustable shape radius:** Control the size and density of the mosaic.
- **Custom color palettes:** Map image colors to a selected palette.
- **Python API:** Use the conversion functionality in your own Python projects.
- **Command-line interface:** Convert images from the terminal.
- **Interactive notebook:** Explore image conversion through a Marimo interface.
- **Automated testing:** Run the test suite to verify functionality.

## Example

Convert an ordinary raster image into a geometric SVG mosaic and open the resulting SVG in a browser or vector graphics editor.

<!-- Add before-and-after screenshots or sample images here. -->

## Installation

Install the package from PyPI:

```bash
python -m pip install png2svg
```

Alternatively, if you use `uv`:

```bash
uv add png2svg
```

## Quick Start

### Python API

```python
from png2svg.conversion import convert_image_to_svg

convert_image_to_svg(
    input_path="input.png",
    output_path="output.svg",
    radius=10,
    shape="hexagon",
)
```

To generate a triangular mosaic:

```python
from png2svg.conversion import convert_image_to_svg

convert_image_to_svg(
    input_path="input.png",
    output_path="triangles.svg",
    radius=10,
    shape="triangle",
)
```

### Custom Color Palette

Pass a list of RGB colors to use a custom palette:

```python
from png2svg.conversion import convert_image_to_svg

palette = [
    (0, 0, 0),
    (128, 128, 128),
    (255, 255, 255),
]

convert_image_to_svg(
    input_path="input.png",
    output_path="grayscale.svg",
    radius=10,
    shape="hexagon",
    palette=palette,
)
```

## Interactive Notebook

The project includes a Marimo notebook for experimenting with the conversion process interactively.

The notebook provides controls for:

- Selecting an input image
- Choosing hexagonal or triangular geometry
- Adjusting the shape radius
- Selecting a predefined color palette
- Choosing an output SVG path
- Previewing the input and generated output
- Exploring the palette distribution utility

### Run Locally

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/sanaiftikharh/png2svg
cd png2svg
```

Install the project dependencies:

```bash
uv sync --all-groups
```

Launch the notebook:

```bash
uv run marimo edit notebooks/image_converter.py
```

## Command-Line Interface

The package provides a `png2svg` command-line entry point.

To inspect the available commands and options:

```bash
png2svg --help
```

Refer to the CLI help output for the exact argument names and supported options.

## Development

This project uses `uv` for dependency management and development workflows.

Install the development dependencies:

```bash
uv sync --all-groups
```

Run the tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=png2svg
```

Check code formatting and linting:

```bash
uv run ruff format --check .
uv run ruff check .
```

Run static type checking:

```bash
uv run mypy src
```

## Project Structure

```text
## Project Structure
png2svg/
├── .github/
│   └── workflows/
├── notebooks/
│   └── image_converter.py
├── src/
│   └── png2svg/
│       ├── __init__.py
│       ├── cli.py
│       ├── conversion.py
│       ├── converter.py
│       ├── geometry.py
│       ├── palette.py
│       ├── sampling.py
│       └── svg.py
├── tests/
├── pyproject.toml
├── README.md
└── uv.lock

```

## Technologies

- Python
- Pillow
- Marimo
- pytest and pytest-cov
- Ruff
- mypy
- uv
- GitHub Actions

## Contributing

Contributions, bug reports, and suggestions are welcome. For proposed changes, create a dedicated branch, add or update tests, and submit a pull request.

## License

Add the license applicable to this project before distributing it under an open-source license.

## Author

**Sana Iftikhar**

GitHub: [@sanaiftikharh](https://github.com/sanaiftikharh)
