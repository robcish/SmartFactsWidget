#!/usr/bin/env python3
"""Second pass: add PL Wikipedia links to pl-PL facts that lack a valid one."""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from content_lib import CONTENT_DIR, WIKI_LINK, load_fact_file, write_fact_md
from fix_pl_translations import (
    build_pl_body,
    en_article_title,
    extract_wiki_url,
    is_pl_already_ok,
    resolve_pl_wiki,
    strip_wiki,
)

ROOT = Path(__file__).resolve().parents[1]


def has_valid_pl_link(body: str) -> bool:
    match = WIKI_LINK.search(body)
    if not match:
        return False
    url = match.group(1)
    if "pl.wikipedia.org" not in url:
        return False
    slug = url.split("/wiki/")[-1]
    if len(slug) > 80 or "%E2%80%A6" in url or "designed_in" in slug:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--delay", type=float, default=0.35)
    args = parser.parse_args()

    caches: dict = {}
    added = skipped = 0
    pl_dir = args.content_dir / "pl-PL"
    en_dir = args.content_dir / "en-US"

    for pl_path in sorted(pl_dir.glob("*.md")):
        pl = load_fact_file(pl_path)
        meta = pl["meta"]
        if not bool(meta.get("published", False)):
            continue
        body = str(pl["body"])
        if has_valid_pl_link(body):
            skipped += 1
            continue

        fact_id = str(meta["id"])
        en_path = en_dir / f"{fact_id}.md"
        if not en_path.exists():
            continue
        en = load_fact_file(en_path)
        en_wiki = extract_wiki_url(str(en["body"]))
        en_title = str(en["meta"].get("title", ""))

        time.sleep(args.delay)
        link = resolve_pl_wiki(en_wiki, en_title, caches)
        core = strip_wiki(body)
        new_body = build_pl_body(core, link)
        write_fact_md(
            pl_path,
            fact_id_value=fact_id,
            locale="pl-PL",
            month=int(meta["month"]),
            day=int(meta["day"]),
            sequence=int(meta["sequence_index"]),
            category=str(meta["category"]),
            title=str(meta.get("title", "")),
            teaser=str(meta.get("teaser", "")),
            body=new_body,
            published=True,
            version=int(meta.get("version", 1)),
        )
        if link:
            added += 1
        if (added + skipped) % 50 == 0:
            print(f"  … added={added} skipped={skipped}", flush=True)

    print(f"Done: links_added={added}, already_ok={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
