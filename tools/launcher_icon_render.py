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
LINES = (33, 33, 33)  # #212121

VIEWPORT = 108.0

# ic_launcher_foreground.xml — dark bars on yellow (M x,y hW v5)
_TEXT_LINES = (
    (28, 38, 80, 43),
    (28, 50, 72, 55),
    (28, 62, 64, 67),
    (28, 74, 76, 79),
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
    """Bitmap match for @mipmap/ic_launcher (yellow + four text lines)."""
    img = Image.new("RGBA", (size, size), BACKGROUND + (255,))
    draw = ImageDraw.Draw(img)
    for line in _TEXT_LINES:
        draw.rectangle(_scale_rect(*line, out_size=size), fill=LINES)
    return img


def write_mipmap_pngs(res_dir: str = "app/src/main/res") -> None:
    """Legacy mipmaps for API 23–25 (adaptive XML is v26+ only)."""
    from pathlib import Path

    sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    root = Path(__file__).resolve().parents[1] / res_dir
    for folder, px in sizes.items():
        out_dir = root / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in ("ic_launcher.png", "ic_launcher_round.png"):
            render_launcher_icon(px).save(out_dir / name, "PNG")
        print(f"Wrote {folder} ({px}px)")


if __name__ == "__main__":
    write_mipmap_pngs()
