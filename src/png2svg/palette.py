from collections.abc import Sequence

Color = tuple[int, int, int]


def map_to_palette(
    color: Color,
    palette: Sequence[Color],
) -> Color:
    """Map an RGB color to the closest color in a palette."""
    if not _is_valid_color(color):
        raise ValueError("Color must contain three RGB integers from 0 to 255.")

    if not palette:
        raise ValueError("palette must contain at least one color.")

    if any(not _is_valid_color(candidate) for candidate in palette):
        raise ValueError(
            "Palette colors must contain three RGB integers from 0 to 255."
        )

    return min(
        palette,
        key=lambda candidate: sum(
            (channel - palette_channel) ** 2
            for channel, palette_channel in zip(color, candidate)
        ),
    )


def _is_valid_color(color: tuple[int, ...]) -> bool:
    """Return whether a color contains three valid RGB channels."""
    return len(color) == 3 and all(
        isinstance(channel, int)
        and not isinstance(channel, bool)
        and 0 <= channel <= 255
        for channel in color
    )
