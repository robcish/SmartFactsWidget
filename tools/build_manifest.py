#!/usr/bin/env python3
"""Build facts.json manifest from Markdown content files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
DEFAULT_OUTPUT = ROOT / "docs" / "facts.json"

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(raw: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_PATTERN.match(raw.strip() + "\n")
    if not match:
        raise ValueError("Missing YAML frontmatter delimiters (---)")

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

    body = match.group(2).strip()
    return metadata, body


def load_facts(content_dir: Path, include_future: bool) -> list[dict[str, object]]:
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    facts: list[dict[str, object]] = []

    for locale_dir in sorted(content_dir.iterdir()):
        if not locale_dir.is_dir():
            continue
        for md_file in sorted(locale_dir.glob("*.md")):
            metadata, body = parse_frontmatter(md_file.read_text(encoding="utf-8"))

            published = bool(metadata.get("published", False))
            release_epoch_ms = int(metadata["release_epoch_ms"])

            if not published:
                continue
            if not include_future and release_epoch_ms > now_ms:
                continue

            facts.append(
                {
                    "id": metadata["id"],
                    "locale": metadata.get("locale", locale_dir.name),
                    "category": metadata["category"],
                    "title": metadata["title"],
                    "teaser": metadata["teaser"],
                    "body_md": body,
                    "release_epoch_ms": release_epoch_ms,
                    "published": published,
                    "version": int(metadata.get("version", 1)),
                }
            )

    facts.sort(key=lambda item: (item["locale"], item["release_epoch_ms"]))
    return facts


def build_manifest(content_dir: Path, output: Path, include_future: bool) -> dict[str, object]:
    facts = load_facts(content_dir, include_future=include_future)
    manifest = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "facts": facts,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Smart Facts JSON manifest")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--include-future",
        action="store_true",
        help="Include facts with a future release_epoch_ms (for local inspection only)",
    )
    args = parser.parse_args()

    if not args.content_dir.exists():
        print(f"Content directory not found: {args.content_dir}", file=sys.stderr)
        return 1

    manifest = build_manifest(args.content_dir, args.output, args.include_future)
    print(f"Wrote {len(manifest['facts'])} facts to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
