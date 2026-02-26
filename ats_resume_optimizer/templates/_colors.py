"""Color manipulation utilities for template rendering."""


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def lighten(hex_color: str, factor: float = 0.85) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(
        int(r + (255 - r) * factor),
        int(g + (255 - g) * factor),
        int(b + (255 - b) * factor),
    )


def darken(hex_color: str, factor: float = 0.3) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(
        int(r * (1 - factor)),
        int(g * (1 - factor)),
        int(b * (1 - factor)),
    )
