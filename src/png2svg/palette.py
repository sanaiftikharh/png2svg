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


def distribute_palette(
    palette: Sequence[Color],
    weights: Sequence[float],
    count: int,
) -> list[Color]:
    """Distribute palette colors according to their relative weights."""
    if not palette:
        raise ValueError("Palette must contain at least one color.")

    if len(palette) != len(weights):
        raise ValueError("The number of weights must match the palette.")

    if count < 0:
        raise ValueError("count must not be negative.")

    if any(not _is_valid_color(color) for color in palette):
        raise ValueError("Palette colors must contain valid RGB values.")

    if any(weight < 0 for weight in weights):
        raise ValueError("weights must be non-negative.")

    total_weight = sum(weights)

    if total_weight <= 0:
        raise ValueError("The total weight must be positive.")

    exact_counts = [count * weight / total_weight for weight in weights]
    allocated_counts = [int(value) for value in exact_counts]
    remaining = count - sum(allocated_counts)

    order = sorted(
        range(len(palette)),
        key=lambda index: exact_counts[index] - allocated_counts[index],
        reverse=True,
    )

    for index in order[:remaining]:
        allocated_counts[index] += 1

    return [
        color
        for color, allocated_count in zip(palette, allocated_counts)
        for _ in range(allocated_count)
    ]
