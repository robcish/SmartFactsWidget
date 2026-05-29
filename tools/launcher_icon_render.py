#!/usr/bin/env python3
"""
Renders ic_launcher_foreground.xml 1:1 (108dp viewport) onto a square PNG.

Source of truth: app/src/main/res/drawable/ic_launcher_foreground.xml
+ @color/ic_launcher_background (#FFD54F). Do not change geometry here without
updating the vector drawable.

Regenerate: python3 tools/generate_play_store_graphics.py
"""

from __future__ import annotations

from PIL import Image, ImageDraw

BACKGROUND = (255, 213, 79)  # #FFD54F ic_launcher_background
FOREGROUND = (33, 33, 33)  # #212121
LINES = (255, 255, 255)

VIEWPORT = 108.0

# ic_launcher_foreground.xml — card bounds (19,19)+(70,70), corner radius 10
_CARD = (19, 19, 89, 89)
_CARD_RADIUS = 10

# pathData white bars: Mx,y hW v4 → (x1, y1, x2, y2)
_TEXT_LINES = (
    (27, 37, 79, 41),  # h52
    (27, 49, 71, 53),  # h44
    (27, 61, 63, 65),  # h36
    (27, 73, 75, 77),  # h48
)


def _scale(value: float, out_size: int) -> int:
    return int(round(value * out_size / VIEWPORT))


def _scale_rect(x1: float, y1: float, x2: float, y2: float, out_size: int) -> tuple[int, int, int, int]:
    return (
        _scale(x1, out_size),
        _scale(y1, out_size),
        _scale(x2, out_size),
        _scale(y2, out_size),
    )


def render_launcher_icon(size: int) -> Image.Image:
    """Bitmap match for @drawable/ic_launcher (yellow bg + foreground vector)."""
    img = Image.new("RGBA", (size, size), BACKGROUND + (255,))
    draw = ImageDraw.Draw(img)

    card = _scale_rect(*_CARD, out_size=size)
    radius = max(1, _scale(_CARD_RADIUS, size))
    draw.rounded_rectangle(card, radius=radius, fill=FOREGROUND)

    for line in _TEXT_LINES:
        draw.rectangle(_scale_rect(*line, out_size=size), fill=LINES)

    return img
