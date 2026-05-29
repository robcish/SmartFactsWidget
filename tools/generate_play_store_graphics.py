#!/usr/bin/env python3
"""Generate Play Store icon (512) and feature graphic (1024x500) from launcher icon artwork."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from launcher_icon_render import render_launcher_icon  # noqa: E402

OUT = ROOT / "docs" / "play-store"

CREAM = (255, 251, 245)  # #FFFBF5
YELLOW = (255, 213, 79)  # #FFD54F
TEXT = (33, 33, 33)
SUBTEXT = (66, 66, 66)

COPY = {
    "pl": {
        "subtitle": "Spokojna, codzienna dawka wiedzy.",
        "tagline": "Widget · Bez reklam",
    },
    "en": {
        "subtitle": "A calm, daily dose of knowledge.",
        "tagline": "Widget · No ads",
    },
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def _draw_background(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    for x in range(w):
        t = x / max(w - 1, 1)
        r = int(CREAM[0] + (YELLOW[0] - CREAM[0]) * t * 0.25)
        g = int(CREAM[1] + (YELLOW[1] - CREAM[1]) * t * 0.25)
        b = int(CREAM[2] + (YELLOW[2] - CREAM[2]) * t * 0.25)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))
    return img


def render_feature_graphic(locale: str = "en") -> Image.Image:
    w, h = 1024, 500
    img = _draw_background(w, h)
    draw = ImageDraw.Draw(img)
    strings = COPY[locale]

    icon_size = 200
    icon = render_launcher_icon(icon_size)
    margin_x = 72
    gap = 48
    icon_y = (h - icon_size) // 2
    img.paste(icon, (margin_x, icon_y), icon)

    title_font = _font(58, bold=True)
    sub_font = _font(30, bold=False)
    tag_font = _font(26, bold=False)

    text_x = margin_x + icon_size + gap
    title = "Smart Facts"
    subtitle = strings["subtitle"]
    tagline = strings["tagline"]

    title_h = _text_size(draw, title, title_font)[1]
    sub_h = _text_size(draw, subtitle, sub_font)[1]
    tag_h = _text_size(draw, tagline, tag_font)[1]
    line_gap = 18
    block_h = title_h + line_gap + sub_h + line_gap + tag_h
    y = (h - block_h) // 2

    draw.text((text_x, y), title, fill=TEXT, font=title_font)
    y += title_h + line_gap
    draw.text((text_x, y), subtitle, fill=SUBTEXT, font=sub_font)
    y += sub_h + line_gap
    draw.text((text_x, y), tagline, fill=SUBTEXT, font=tag_font)

    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    render_launcher_icon(512).save(OUT / "icon-512.png", "PNG", optimize=True)
    render_feature_graphic("en").save(OUT / "feature-graphic-1024x500.png", "PNG", optimize=True)
    render_feature_graphic("pl").save(OUT / "feature-graphic-1024x500-pl.png", "PNG", optimize=True)
    print(f"Wrote {OUT / 'icon-512.png'} (same as ic_launcher)")
    print(f"Wrote {OUT / 'feature-graphic-1024x500.png'}")
    print(f"Wrote {OUT / 'feature-graphic-1024x500-pl.png'}")


if __name__ == "__main__":
    main()
