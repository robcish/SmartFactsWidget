#!/usr/bin/env python3
"""Remove generic category Wikipedia links from pl-PL facts (no link if no topic article)."""

from __future__ import annotations

import argparse
import urllib.parse
from pathlib import Path

from content_lib import CONTENT_DIR, WIKI_LINK, load_fact_file, write_fact_md


def strip_wiki(body: str) -> str:
    return WIKI_LINK.sub("", body).strip()

# Titles used by the former apply_pl_category_links.py pass
CATEGORY_FALLBACK_PL: dict[str, str] = {
    "general": "Wikipedia",
    "science": "Nauka",
    "history": "Historia",
    "geography": "Geografia",
    "biology": "Biologia",
    "animals": "Zwierzęta",
    "technology": "Technologia",
    "culture": "Kultura",
    "food": "Żywność",
    "sport": "Sport",
    "psychology": "Psychologia",
    "language": "Język",
    "philosophy": "Filozofia",
    "society": "Społeczeństwo",
    "law": "Prawo",
    "finance": "Finanse",
    "environment": "Środowisko naturalne",
    "astronomy": "Astronomia",
    "math": "Matematyka",
    "mythology": "Mitologia",
    "myth-busting": "Pseudonauka",
    "reflection": "Ciekawość",
}


def normalize_wiki_title(value: str) -> str:
    return urllib.parse.unquote(value.replace("_", " ")).strip().lower()


def is_category_fallback_link(url: str, category: str) -> bool:
    expected = CATEGORY_FALLBACK_PL.get(category)
    if not expected or "pl.wikipedia.org/wiki/" not in url:
        return False
    slug = url.split("/wiki/", 1)[-1].split("?", 1)[0]
    return normalize_wiki_title(slug) == normalize_wiki_title(expected)


def main() -> int:
    parser = argparse.ArgumentParser(description="Strip category-fallback PL Wikipedia links")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    pl_dir = args.content_dir / "pl-PL"
    stripped = kept = 0

    for path in sorted(pl_dir.glob("*.md")):
        fact = load_fact_file(path)
        meta = fact["meta"]
        if not bool(meta.get("published", False)):
            continue
        body = str(fact["body"])
        match = WIKI_LINK.search(body)
        if not match:
            continue
        url = match.group(1)
        category = str(meta.get("category", ""))
        if not is_category_fallback_link(url, category):
            kept += 1
            continue

        new_body = strip_wiki(body).strip()
        stripped += 1
        if args.dry_run:
            print(f"Would strip link: {meta['id']}")
            continue

        write_fact_md(
            path,
            fact_id_value=str(meta["id"]),
            locale="pl-PL",
            month=int(meta["month"]),
            day=int(meta["day"]),
            sequence=int(meta["sequence_index"]),
            category=category,
            title=str(meta["title"]),
            teaser=str(meta["teaser"]),
            body=new_body,
            published=True,
            version=int(meta.get("version", 1)),
        )

    print(f"Done: stripped={stripped}, kept_topic_links={kept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
