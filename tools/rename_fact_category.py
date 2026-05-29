#!/usr/bin/env python3
"""Rename fact files when category slug changes (both locales, updates frontmatter id)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from content_lib import CONTENT_DIR, LOCALES, load_fact_file, write_fact_md

ROOT = Path(__file__).resolve().parents[1]


def rename_pair(old_id: str, new_id: str, content_dir: Path) -> None:
    old_month = int(old_id[0:2])
    old_day = int(old_id[3:5])
    old_seq = int(old_id[6])
    new_month = int(new_id[0:2])
    new_day = int(new_id[3:5])
    new_seq = int(new_id[6])
    new_category = new_id.split("-", 3)[3]

    for locale in LOCALES:
        old_path = content_dir / locale / f"{old_id}.md"
        if not old_path.exists():
            print(f"Missing {old_path}", file=sys.stderr)
            continue
        loaded = load_fact_file(old_path)
        meta = loaded["meta"]
        write_fact_md(
            content_dir / locale / f"{new_id}.md",
            fact_id_value=new_id,
            locale=locale,
            month=new_month,
            day=new_day,
            sequence=new_seq,
            category=new_category,
            title=str(meta.get("title", "")),
            teaser=str(meta.get("teaser", "")),
            body=str(loaded["body"]),
            published=bool(meta.get("published", False)),
            version=int(meta.get("version", 1)),
        )
        old_path.unlink()
        print(f"Renamed {locale}/{old_id}.md → {new_id}.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rename fact id/category")
    parser.add_argument("old_id", help="e.g. 05-30-0-animals")
    parser.add_argument("new_id", help="e.g. 05-30-0-biology")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    args = parser.parse_args()
    rename_pair(args.old_id, args.new_id, args.content_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
