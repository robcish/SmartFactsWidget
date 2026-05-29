#!/usr/bin/env python3
"""Plan three categories per calendar day with 2-day cooldown."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from content_lib import (
    CATEGORIES,
    CATEGORY_COOLDOWN_DAYS,
    FACTS_PER_DAY,
    iter_calendar_days,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "tools" / "category_plan.json"


def plan_year() -> dict[str, list[str]]:
    days = iter_calendar_days()
    plan: dict[str, list[str]] = {}
    recent: list[list[str]] = []

    for month, day in days:
        key = f"{month:02d}-{day:02d}"
        blocked = set()
        for prev in recent[-CATEGORY_COOLDOWN_DAYS:]:
            blocked.update(prev)

        chosen: list[str] = []
        start = (days.index((month, day)) * FACTS_PER_DAY) % len(CATEGORIES)
        idx = start
        attempts = 0
        while len(chosen) < FACTS_PER_DAY and attempts < len(CATEGORIES) * 4:
            cat = CATEGORIES[idx % len(CATEGORIES)]
            idx += 1
            attempts += 1
            if cat in blocked or cat in chosen:
                continue
            chosen.append(cat)
            blocked.add(cat)

        if len(chosen) < FACTS_PER_DAY:
            raise RuntimeError(f"Cannot plan categories for {key}")

        plan[key] = chosen
        recent.append(chosen)

    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan daily categories for the year")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    plan = plan_year()
    args.output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(plan)} days to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
