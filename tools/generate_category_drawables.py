#!/usr/bin/env python3
"""Download official Material Symbols Outlined SVGs and emit Android vector drawables."""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "src" / "main" / "res" / "drawable"

# category slug -> Material Symbols name (https://github.com/google/material-design-icons)
SYMBOLS: dict[str, str] = {
    "science": "science",
    "math": "calculate",
    "biology": "biotech",
    "animals": "pets",
    "technology": "memory",
    "history": "history_edu",
    "geography": "public",
    "astronomy": "rocket_launch",
    "language": "translate",
    "psychology": "psychology",
    "philosophy": "menu_book",
    "society": "groups",
    "law": "gavel",
    "finance": "savings",
    "culture": "museum",
    "mythology": "auto_stories",
    "myth-busting": "fact_check",
    "general": "star",
    "reflection": "self_improvement",
    "sport": "sports_soccer",
    "food": "restaurant",
    "environment": "eco",
}

BASE_URL = (
    "https://github.com/google/material-design-icons/raw/master/"
    "symbols/web/{symbol}/materialsymbolsoutlined/{symbol}_24px.svg"
)

# Material SVGs use viewBox 0 -960 960 960. Glance/AppWidget rasterization needs a 24×24
# viewport (large viewports often render as blank). Scale paths via <group>.
SCALE = 24 / 960
# ~17% black watermark on yellow widget background (no runtime tint — Glance is flaky).
FILL_COLOR = "#2B121212"

VECTOR_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <group
        android:scaleX="{scale}"
        android:scaleY="{scale}"
        android:translateY="24">
{paths}
    </group>
</vector>
"""

PATH_TEMPLATE = (
    '        <path\n            android:fillColor="{fill}"\n'
    '            android:pathData="{path_data}" />'
)


def category_to_filename(category: str) -> str:
    return f"ic_cat_{category.replace('-', '_')}.xml"


def fetch_svg(symbol: str) -> str:
    url = BASE_URL.format(symbol=symbol)
    request = urllib.request.Request(url, headers={"User-Agent": "SmartFactsWidget/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def extract_paths(svg: str) -> list[str]:
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', svg)
    if not paths:
        raise ValueError("No <path> elements found in SVG")
    return paths


def to_vector_xml(path_data_list: list[str]) -> str:
    paths_block = "\n".join(
        PATH_TEMPLATE.format(fill=FILL_COLOR, path_data=p) for p in path_data_list
    )
    return VECTOR_TEMPLATE.format(scale=SCALE, paths=paths_block) + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    for category, symbol in SYMBOLS.items():
        outfile = OUT / category_to_filename(category)
        try:
            svg = fetch_svg(symbol)
            path_data = extract_paths(svg)
            outfile.write_text(to_vector_xml(path_data), encoding="utf-8")
            print(f"OK {outfile.name} <- {symbol}")
        except (urllib.error.URLError, ValueError) as error:
            failures.append(f"{category} ({symbol}): {error}")
            print(f"FAIL {category}: {error}", file=sys.stderr)

    if failures:
        print(f"\n{len(failures)} icon(s) failed.", file=sys.stderr)
        return 1

    print(f"\nGenerated {len(SYMBOLS)} icons from Google Material Symbols.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
