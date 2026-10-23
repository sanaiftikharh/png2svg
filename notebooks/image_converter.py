"""Interactive PNG-to-SVG Mosaic Studio.

Features:
- Input image selection and preview
- Hexagon and triangle geometries
- Adjustable shape radius
- Optional color palette mapping
- SVG generation and output preview
- Conversion status and output information
- Palette distribution demonstration
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from png2svg.conversion import convert_image_to_svg
    from png2svg.palette import distribute_palette

    return convert_image_to_svg, distribute_palette, mo


@app.cell
def _(mo):
    mo.md("""
    # PNG → SVG Mosaic Studio

    Turn an ordinary image into a scalable geometric mosaic.

    1. Select an image.
    2. Choose a shape and radius.
    3. Select an optional color palette.
    4. Generate and compare the original image with the SVG output.
    """)
    return


@app.cell
def _(mo):
    input_image = mo.ui.file_browser(
        initial_path=".",
        filetypes=[".png", ".jpg", ".jpeg", ".webp", ".bmp"],
        selection_mode="file",
        multiple=False,
        label="1. Select source image",
    )

    shape = mo.ui.dropdown(
        options=["hexagon", "triangle"],
        value="hexagon",
        label="2. Geometry",
    )

    radius = mo.ui.slider(
        start=2,
        stop=40,
        step=1,
        value=10,
        label="3. Shape radius",
        show_value=True,
    )

    palette_name = mo.ui.dropdown(
        options=["None", "Grayscale", "Sunset", "Ocean"],
        value="None",
        label="4. Color palette",
    )

    output_path = mo.ui.text(
        value="output/mosaic.svg",
        label="5. Output SVG path",
    )

    convert_button = mo.ui.run_button(
        label="Generate SVG mosaic",
    )

    mo.vstack(
        [
            input_image,
            mo.hstack(
                [shape, radius],
                justify="start",
                gap=2,
            ),
            palette_name,
            output_path,
            convert_button,
        ],
        gap=1,
    )
    return (
        convert_button,
        input_image,
        output_path,
        palette_name,
        radius,
        shape,
    )


@app.cell
def _(input_image):
    from pathlib import Path
    selected_path = input_image.path(index=0)

    if selected_path is not None:
        selected_path = Path(selected_path)
    return Path, selected_path


@app.cell
def _(
    Path,
    convert_button,
    convert_image_to_svg,
    mo,
    output_path,
    palette_name,
    radius,
    selected_path,
    shape,
):
    result_path = None

    result_message = mo.md(
        "Select an image and click **Generate SVG mosaic**."
    )

    if convert_button.value:
        if selected_path is None or not selected_path.is_file():
            result_message = mo.md(
                "**Input required:** Select an existing image."
            )

        elif not output_path.value.strip():
            result_message = mo.md(
                "**Output required:** Enter an output filename."
            )

        elif radius.value is None or radius.value <= 0:
            result_message = mo.md(
                "**Invalid radius:** Choose a positive value."
            )

        else:
            destination = Path(output_path.value.strip())

            try:
                if destination.suffix.lower() != ".svg":
                    raise ValueError(
                        "The output filename must end in .svg."
                    )

                if selected_path.resolve() == destination.resolve():
                    raise ValueError(
                        "The input and output paths must differ."
                    )

                if destination.exists() and destination.is_dir():
                    raise ValueError(
                        "The output path points to a directory."
                    )

                palettes = {
                    "Grayscale": [
                        (0, 0, 0),
                        (128, 128, 128),
                        (255, 255, 255),
                    ],
                    "Sunset": [
                        (75, 0, 130),
                        (220, 20, 60),
                        (255, 165, 0),
                    ],
                    "Ocean": [
                        (0, 0, 128),
                        (0, 128, 180),
                        (135, 206, 235),
                    ],
                }

                chosen_palette = (
                    None
                    if palette_name.value == "None"
                    else palettes[palette_name.value]
                )

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                convert_image_to_svg(
                    selected_path,
                    destination,
                    radius=float(radius.value),
                    shape=shape.value,
                    palette=chosen_palette,
                )

                if not destination.is_file():
                    raise ValueError(
                        "The converter did not create an output file."
                    )

                if destination.stat().st_size == 0:
                    raise ValueError(
                        "The generated SVG file is empty."
                    )

                result_path = destination

                result_message = mo.md(f"""
    ### Conversion successful!

    | Property | Value |
    |---|---|
    | Input | `{selected_path.name}` |
    | Output | `{destination}` |
    | Geometry | {shape.value} |
    | Radius | {radius.value} |
    | Palette | {palette_name.value} |
    | File size | {destination.stat().st_size:,} bytes |
    """)

            except (ValueError, OSError) as error:
                result_message = mo.md(
                    f"**Conversion failed:** {error}"
                )

    result_message
    return (result_path,)


@app.cell
def _(mo, result_path, selected_path):
    import base64
    # Input preview
    if selected_path is not None and selected_path.is_file():
        input_mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
        }

        input_mime = input_mime_types.get(
            selected_path.suffix.lower(),
            "image/png",
        )

        input_data = base64.b64encode(
            selected_path.read_bytes()
        ).decode("ascii")

        input_preview = mo.image(
            src=f"data:{input_mime};base64,{input_data}",
            alt="Original input image",
            width="100%",
        )
    else:
        input_preview = mo.md("Select an image above.")

    # Output preview
    if result_path is not None and result_path.is_file():
        svg_data = base64.b64encode(
            result_path.read_bytes()
        ).decode("ascii")

        output_preview = mo.image(
            src=f"data:image/svg+xml;base64,{svg_data}",
            alt="Generated SVG mosaic",
            width="100%",
        )
    else:
        output_preview = mo.md(
            "Click **Generate SVG mosaic** to create the output."
        )

    mo.vstack(
        [
            mo.md("---\n# Image Previews"),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("### Original Image"),
                            input_preview,
                        ],
                        gap=1,
                    ),
                    mo.vstack(
                        [
                            mo.md("### Generated SVG"),
                            output_preview,
                        ],
                        gap=1,
                    ),
                ],
                widths="equal",
                gap=2,
                align="start",
            ),
        ],
        gap=2,
    )
    return


@app.cell
def _(distribute_palette, mo):
    mo.md("""
    ---
    # Palette Distribution Utility

    This example demonstrates distributing colors according to weights.
    It is separate from the image-conversion process.
    """)

    palette_for_distribution = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]

    weights = [0.5, 0.3, 0.2]
    count = 10

    distribution = distribute_palette(
        palette_for_distribution,
        weights,
        count,
    )

    mo.md(f"""
    **Palette:** `{palette_for_distribution}`

    **Weights:** `{weights}`

    **Number of assignments:** `{count}`

    **Result:** `{distribution}`
    """)
    return


if __name__ == "__main__":
    app.run()
