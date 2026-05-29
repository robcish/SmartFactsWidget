#!/usr/bin/env python3
"""Shared helpers for Smart Facts content tools."""

from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
LOCALES = ("pl-PL", "en-US")

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
FILENAME_PATTERN = re.compile(r"^(\d{2})-(\d{2})-(\d+)-([a-z-]+)\.md$")
WIKI_LINK = re.compile(r"\[[^\]]*\]\((https?://[^)]+)\)")

CATEGORIES = [
    "general",
    "science",
    "history",
    "geography",
    "biology",
    "animals",
    "technology",
    "culture",
    "food",
    "sport",
    "psychology",
    "language",
    "philosophy",
    "society",
    "law",
    "finance",
    "environment",
    "astronomy",
    "math",
    "mythology",
    "myth-busting",
    "reflection",
]

FACTS_PER_DAY = 3
CATEGORY_COOLDOWN_DAYS = 2


def iter_calendar_days(year: int = 2024) -> list[tuple[int, int]]:
    """366 days for leap-year template (Jan 1 – Dec 31)."""
    days: list[tuple[int, int]] = []
    d = date(year, 1, 1)
    end = date(year, 12, 31)
    while d <= end:
        days.append((d.month, d.day))
        d += timedelta(days=1)
    return days


def day_index(month: int, day: int, days: list[tuple[int, int]] | None = None) -> int:
    if days is None:
        days = iter_calendar_days()
    return days.index((month, day))


def parse_frontmatter(raw: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_PATTERN.match(raw.strip() + "\n")
    if not match:
        raise ValueError("Missing YAML frontmatter")
    metadata: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.lower() in {"true", "false"}:
            metadata[key] = value.lower() == "true"
        elif value.isdigit():
            metadata[key] = int(value)
        else:
            metadata[key] = value
    return metadata, match.group(2).strip()


def load_fact_file(path: Path) -> dict[str, object]:
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    return {
        "path": path,
        "meta": meta,
        "body": body,
        "raw": raw,
    }


def slot_path(content_dir: Path, locale: str, month: int, day: int, sequence: int) -> Path | None:
    folder = content_dir / locale
    matches = sorted(folder.glob(f"{month:02d}-{day:02d}-{sequence}-*.md"))
    return matches[0] if matches else None


def iter_fact_files(content_dir: Path = CONTENT_DIR) -> list[Path]:
    paths: list[Path] = []
    for locale in LOCALES:
        folder = content_dir / locale
        if not folder.is_dir():
            continue
        paths.extend(sorted(folder.glob("*.md")))
    return paths


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"[*_#>`]", "", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fingerprint(meta: dict[str, object], body: str) -> str:
    teaser = normalize_text(str(meta.get("teaser", "")))
    body_n = normalize_text(body)[:120]
    return f"{teaser}|{body_n}"


def fact_id(month: int, day: int, sequence: int, category: str) -> str:
    return f"{month:02d}-{day:02d}-{sequence}-{category}"


def write_fact_md(
    path: Path,
    *,
    fact_id_value: str,
    locale: str,
    month: int,
    day: int,
    sequence: int,
    category: str,
    title: str,
    teaser: str,
    body: str,
    published: bool,
    version: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                f"id: {fact_id_value}",
                f"locale: {locale}",
                f"month: {month}",
                f"day: {day}",
                f"sequence_index: {sequence}",
                f"category: {category}",
                f"title: {title}",
                f"teaser: {teaser}",
                f"published: {'true' if published else 'false'}",
                f"version: {version}",
                "---",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )
