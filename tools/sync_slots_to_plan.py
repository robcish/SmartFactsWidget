#!/usr/bin/env python3
"""Align each day's three slot files with category_plan.json (rename + fix frontmatter)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from content_lib import (
    CONTENT_DIR,
    LOCALES,
    fact_id,
    iter_calendar_days,
    load_fact_file,
    slot_path,
    write_fact_md,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "tools" / "category_plan.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync slot files to category plan")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan: dict[str, list[str]] = json.loads(args.plan.read_text(encoding="utf-8"))
    fixed = 0

    for month, day in iter_calendar_days():
        key = f"{month:02d}-{day:02d}"
        cats = plan[key]
        for sequence, category in enumerate(cats):
            fid = fact_id(month, day, sequence, category)
            for locale in LOCALES:
                target = args.content_dir / locale / f"{fid}.md"
                existing = slot_path(args.content_dir, locale, month, day, sequence)
                if existing is None:
                    continue
                if existing == target:
                    loaded = load_fact_file(target)
                    meta = loaded["meta"]
                    if str(meta.get("category")) != category or str(meta.get("id")) != fid:
                        if args.dry_run:
                            print(f"Would fix meta {target.name}")
                        else:
                            write_fact_md(
                                target,
                                fact_id_value=fid,
                                locale=locale,
                                month=month,
                                day=day,
                                sequence=sequence,
                                category=category,
                                title=str(meta.get("title", "")),
                                teaser=str(meta.get("teaser", "")),
                                body=str(loaded["body"]),
                                published=bool(meta.get("published", False)),
                                version=int(meta.get("version", 1)),
                            )
                            fixed += 1
                    continue
                loaded = load_fact_file(existing)
                meta = loaded["meta"]
                if args.dry_run:
                    print(f"Would move {existing.name} -> {fid}.md [{locale}]")
                else:
                    write_fact_md(
                        target,
                        fact_id_value=fid,
                        locale=locale,
                        month=month,
                        day=day,
                        sequence=sequence,
                        category=category,
                        title=str(meta.get("title", "")),
                        teaser=str(meta.get("teaser", "")),
                        body=str(loaded["body"]),
                        published=bool(meta.get("published", False)),
                        version=int(meta.get("version", 1)),
                    )
                    existing.unlink()
                    fixed += 1

    print(f"{'Would fix' if args.dry_run else 'Fixed'} {fixed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
