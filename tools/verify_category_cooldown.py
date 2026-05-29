#!/usr/bin/env python3
"""Verify 2-day category cooldown across published facts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from content_lib import CONTENT_DIR, day_index, iter_calendar_days, iter_fact_files, load_fact_file

ROOT = Path(__file__).resolve().parents[1]


def collect_slots(
    content_dir: Path,
    *,
    published_only: bool,
    include_drafts: bool,
) -> list[dict[str, object]]:
    days = iter_calendar_days()
    slots: list[dict[str, object]] = []

    for path in iter_fact_files(content_dir):
        if path.parent.name not in {"pl-PL", "en-US"}:
            continue
        if path.parent.name != "pl-PL":
            continue
        try:
            loaded = load_fact_file(path)
        except ValueError:
            continue
        meta = loaded["meta"]
        published = bool(meta.get("published", False))
        if published_only and not published:
            continue
        if not published_only and not include_drafts and not published:
            continue
        month = int(meta["month"])
        day = int(meta["day"])
        category = str(meta["category"])
        slots.append(
            {
                "month": month,
                "day": day,
                "category": category,
                "id": str(meta.get("id", path.stem)),
                "path": path,
                "index": day_index(month, day, days),
            }
        )
    return slots


def find_violations(slots: list[dict[str, object]], cooldown: int = 2) -> list[str]:
    violations: list[str] = []
    by_index: dict[int, list[dict[str, object]]] = {}
    for slot in slots:
        by_index.setdefault(int(slot["index"]), []).append(slot)

    for idx, day_slots in sorted(by_index.items()):
        cats_today = {str(s["category"]) for s in day_slots}
        if len(cats_today) < len(day_slots):
            violations.append(
                f"Duplicate category on same day: "
                f"{day_slots[0]['month']:02d}-{day_slots[0]['day']:02d}"
            )
        for back in range(1, cooldown + 1):
            prev = by_index.get(idx - back)
            if not prev:
                continue
            for s in day_slots:
                for p in prev:
                    if s["category"] == p["category"]:
                        violations.append(
                            f"{s['month']:02d}-{s['day']:02d} "
                            f"({s['id']}, {s['category']}) conflicts with "
                            f"{p['month']:02d}-{p['day']:02d} "
                            f"({p['id']}, {p['category']}) — {back} day(s) apart"
                        )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Check category cooldown")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--month", type=int, help="Only report facts in this month (1-12)")
    parser.add_argument("--published-only", action="store_true", default=True)
    parser.add_argument("--include-drafts", action="store_true")
    args = parser.parse_args()

    slots = collect_slots(
        args.content_dir,
        published_only=args.published_only,
        include_drafts=args.include_drafts,
    )
    if args.month:
        slots = [s for s in slots if int(s["month"]) == args.month]

    violations = find_violations(slots)
    if violations:
        print(f"Found {len(violations)} cooldown violation(s):\n")
        for v in violations:
            print(f"  - {v}")
        return 1

    scope = f"month {args.month:02d}" if args.month else "all published days"
    print(f"No category cooldown violations ({scope}, {len(slots)} slots checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
