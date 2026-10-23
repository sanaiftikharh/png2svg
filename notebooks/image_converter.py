"""Interactive notebook for converting images into hexagonal SVG mosaics."""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import marimo as mo

    from png2svg.conversion import convert_image_to_svg

    return Path, convert_image_to_svg, mo


@app.cell
def _(mo):
    mo.md("""
    # PNG to SVG Mosaic Converter

    Convert an image into a scalable hexagonal mosaic.

    **How to use this notebook**
    1. Select an input image.
    2. Choose an output SVG path.
    3. Set the hexagon radius.
    4. Click **Convert image**.
    5. Compare the original image with the generated SVG.
    """)


@app.cell
def _(mo):
    input_image = mo.ui.file_browser(
        initial_path=".",
        filetypes=[".png", ".jpg", ".jpeg", ".webp", ".bmp"],
        selection_mode="file",
        multiple=False,
        label="Select an input image",
    )

    output_svg = mo.ui.text(
        value="output/mosaic.svg",
        label="Output SVG path",
    )

    radius = mo.ui.number(
        start=1,
        stop=100,
        step=1,
        value=10,
        label="Hexagon radius",
    )

    convert_button = mo.ui.run_button(label="Convert image")

    mo.vstack(
        [
            input_image,
            output_svg,
            radius,
            convert_button,
        ],
        gap=1,
    )
    return convert_button, input_image, output_svg, radius


@app.cell
def _(
    Path,
    convert_button,
    convert_image_to_svg,
    input_image,
    mo,
    output_svg,
    radius,
):
    status = mo.md("Select an image and click **Convert image**.")
    comparison = None

    if convert_button.value:
        input_path = input_image.path(index=0)

        if input_path is None:
            status = mo.md("Please select an input image.")
        elif not output_svg.value.strip():
            status = mo.md("Please enter an output SVG path.")
        elif radius.value is None or radius.value <= 0:
            status = mo.md("The hexagon radius must be positive.")
        else:
            output_path = Path(output_svg.value.strip())

            try:
                if not input_path.is_file():
                    raise ValueError("The selected input file does not exist.")

                if input_path.resolve() == output_path.resolve():
                    raise ValueError(
                        "The output path must be different from the input path."
                    )

                output_path.parent.mkdir(parents=True, exist_ok=True)

                convert_image_to_svg(
                    input_path,
                    output_path,
                    radius=float(radius.value),
                )

                if not output_path.is_file():
                    raise ValueError(
                        "The conversion finished without creating the SVG file."
                    )

                status = mo.md(
                    f"**Conversion successful!**\n\n"
                    f"- Input: `{input_path}`\n"
                    f"- Output: `{output_path}`\n"
                    f"- Hexagon radius: `{radius.value}`"
                )

                comparison = mo.image_compare(
                    before_image=str(input_path),
                    after_image=str(output_path),
                    width="100%",
                    height=450,
                )

            except (ValueError, OSError) as error:
                status = mo.md(f"**Conversion failed:** {error}")

    output_items = [status]

    if comparison is not None:
        output_items.append(comparison)

    mo.vstack(output_items, gap=2)


if __name__ == "__main__":
    app.run()
