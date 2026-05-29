#!/usr/bin/env python3
"""Add sequence_index 2 template files using category_plan.json."""

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
    write_fact_md,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "tools" / "category_plan.json"


def template_body(month: int, day: int, sequence: int, locale: str) -> str:
    if locale == "pl-PL":
        return (
            f"<!-- TODO: fakt na {month:02d}-{day:02d}, slot {sequence} -->\n\n"
            "_Treść do uzupełnienia._"
        )
    return (
        f"<!-- TODO: fact for {month:02d}-{day:02d}, slot {sequence} -->\n\n"
        "_Content pending._"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Add MM-DD-2-{category}.md templates")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.plan.exists():
        print(f"Run plan_categories.py first (missing {args.plan})", file=sys.stderr)
        return 1

    plan: dict[str, list[str]] = json.loads(args.plan.read_text(encoding="utf-8"))
    created = 0

    for month, day in iter_calendar_days():
        key = f"{month:02d}-{day:02d}"
        categories = plan.get(key)
        if not categories or len(categories) < 3:
            print(f"Plan missing slot 2 for {key}", file=sys.stderr)
            return 1
        category = categories[2]
        fid = fact_id(month, day, 2, category)
        for locale in LOCALES:
            path = args.content_dir / locale / f"{fid}.md"
            if path.exists():
                continue
            created += 1
            if args.dry_run:
                print(f"Would create {path.relative_to(ROOT)}")
                continue
            write_fact_md(
                path,
                fact_id_value=fid,
                locale=locale,
                month=month,
                day=day,
                sequence=2,
                category=category,
                title="",
                teaser="",
                body=template_body(month, day, 2, locale),
                published=False,
                version=0,
            )

    print(f"{'Would create' if args.dry_run else 'Created'} {created} new file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
