#!/usr/bin/env python3
"""Build facts.json manifest from Markdown content files."""

from __future__ import annotations

import argparse
import hashlib
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


def load_facts(content_dir: Path) -> list[dict[str, object]]:
    facts: list[dict[str, object]] = []

    for locale_dir in sorted(content_dir.iterdir()):
        if not locale_dir.is_dir() or locale_dir.name.startswith("."):
            continue
        if locale_dir.name.endswith(".md"):
            continue
        for md_file in sorted(locale_dir.glob("*.md")):
            metadata, body = parse_frontmatter(md_file.read_text(encoding="utf-8"))

            published = bool(metadata.get("published", False))
            if not published:
                continue

            title = str(metadata.get("title", "")).strip()
            if not title:
                continue

            facts.append(
                {
                    "id": metadata["id"],
                    "locale": metadata.get("locale", locale_dir.name),
                    "category": metadata["category"],
                    "title": title,
                    "teaser": metadata["teaser"],
                    "body_md": body,
                    "month": int(metadata["month"]),
                    "day": int(metadata["day"]),
                    "sequence_index": int(metadata["sequence_index"]),
                    "published": published,
                    "version": int(metadata.get("version", 1)),
                }
            )

    facts.sort(
        key=lambda item: (
            item["locale"],
            item["month"],
            item["day"],
            item["sequence_index"],
        )
    )
    return facts


def build_manifest(content_dir: Path, output: Path) -> dict[str, object]:
    facts = load_facts(content_dir)
    payload = json.dumps(facts, ensure_ascii=False, sort_keys=True)
    content_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    manifest = {
        "manifest_version": f"v2-{content_hash}",
        "version": 2,
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
    args = parser.parse_args()

    if not args.content_dir.exists():
        print(f"Content directory not found: {args.content_dir}", file=sys.stderr)
        return 1

    manifest = build_manifest(args.content_dir, args.output)
    print(f"Wrote {len(manifest['facts'])} facts to {args.output}")
    print(f"manifest_version={manifest['manifest_version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
