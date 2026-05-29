#!/usr/bin/env python3
"""Print a human-readable summary of Smart Facts content (for agents and maintainers)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
MANIFEST = ROOT / "docs" / "facts.json"
LOCALES = ("pl-PL", "en-US")
ALL_CATEGORIES = [
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


def iter_calendar_days(year: int = 2024) -> list[tuple[int, int]]:
    days: list[tuple[int, int]] = []
    d = date(year, 1, 1)
    end = date(year, 12, 31)
    while d <= end:
        days.append((d.month, d.day))
        d += timedelta(days=1)
    return days


def load_manifest(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("facts", [])


def scan_markdown(content_dir: Path) -> dict[str, object]:
    files_by_locale: dict[str, int] = {}
    published_by_locale: dict[str, int] = {}
    days_per_locale: dict[str, Counter[int]] = defaultdict(Counter)

    for locale in LOCALES:
        folder = content_dir / locale
        if not folder.is_dir():
            continue
        paths = list(folder.glob("*.md"))
        files_by_locale[locale] = len(paths)
        pub = 0
        for path in paths:
            raw = path.read_text(encoding="utf-8")
            if "published: true" in raw and "title:" in raw:
                parts = raw.split("---", 2)
                if len(parts) >= 2 and "title: " in parts[1]:
                    title_line = [
                        ln for ln in parts[1].splitlines() if ln.strip().startswith("title:")
                    ]
                    if title_line and len(title_line[0].split(":", 1)[1].strip()) > 0:
                        pub += 1
            # month from filename MM-DD-...
            name = path.stem
            if len(name) >= 5:
                month = int(name[:2])
                days_per_locale[locale][month] += 1
        published_by_locale[locale] = pub

    return {
        "files_by_locale": files_by_locale,
        "published_by_locale": published_by_locale,
        "days_per_locale": days_per_locale,
    }


def analyze_facts(facts: list[dict], locale: str) -> dict[str, object]:
    subset = [f for f in facts if f.get("locale") == locale]
    by_day: dict[tuple[int, int], list[str]] = defaultdict(list)
    by_month: dict[int, list[str]] = defaultdict(list)
    categories = Counter(f["category"] for f in subset)

    for f in subset:
        key = (int(f["month"]), int(f["day"]))
        by_day[key].append(str(f["category"]))
        by_month[int(f["month"])].append(str(f["category"]))

    per_day_counts = Counter(len(v) for v in by_day.values())
    dup_same_day = sum(1 for cats in by_day.values() if len(cats) != len(set(cats)))

    days_order = iter_calendar_days()
    pos = {md: i for i, md in enumerate(days_order)}
    cooldown_violations = 0
    for md, cats in by_day.items():
        i = pos.get(md)
        if i is None:
            continue
        for back in (1, 2):
            prev_md = days_order[i - back]
            prev_cats = by_day.get(prev_md, [])
            for c in cats:
                if c in prev_cats:
                    cooldown_violations += 1

    total = sum(categories.values()) or 1
    expected = total / max(len(categories), 1)
    deviations = {
        cat: {
            "count": categories[cat],
            "pct": 100 * categories[cat] / total,
            "vs_even_pct": 100 * (categories[cat] - expected) / expected if expected else 0,
        }
        for cat in ALL_CATEGORIES
    }
    unused = [c for c in ALL_CATEGORIES if categories[c] == 0]
    missing_in_manifest = [c for c in ALL_CATEGORIES if categories[c] == 0]

    return {
        "total": len(subset),
        "days_with_facts": len(by_day),
        "facts_per_day_distribution": dict(sorted(per_day_counts.items())),
        "duplicate_category_same_day": dup_same_day,
        "cooldown_violations_2d": cooldown_violations,
        "categories": dict(categories.most_common()),
        "category_deviations": deviations,
        "unused_categories": unused,
        "by_month_counts": {m: len(v) for m, v in sorted(by_month.items())},
    }


def print_report(
    *,
    md_scan: dict[str, object],
    en_stats: dict[str, object],
    pl_stats: dict[str, object],
    manifest_path: Path,
) -> None:
    print("=" * 60)
    print("Smart Facts — content summary")
    print("=" * 60)

    print("\n## Files on disk")
    for loc in LOCALES:
        files = md_scan["files_by_locale"].get(loc, 0)
        pub = md_scan["published_by_locale"].get(loc, 0)
        print(f"  {loc}: {files} markdown files, ~{pub} published with title")

    print("\n## Manifest")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"  Path: {manifest_path.relative_to(ROOT)}")
        print(f"  manifest_version: {manifest.get('manifest_version')}")
        print(f"  facts in JSON: {len(manifest.get('facts', []))}")
    else:
        print("  (no manifest — run tools/build_manifest.py)")

    for label, stats in ("en-US", en_stats), ("pl-PL", pl_stats):
        print(f"\n## Calendar stats ({label})")
        print(f"  Published facts: {stats['total']}")
        print(f"  Days covered: {stats['days_with_facts']}")
        print(f"  Facts per day: {stats['facts_per_day_distribution']}")
        print(f"  Same category twice on one day: {stats['duplicate_category_same_day']}")
        print(f"  2-day category cooldown violations: {stats['cooldown_violations_2d']}")

    print("\n## Category balance (en-US, vs perfectly even split)")
    en_cats = en_stats["categories"]
    total = en_stats["total"] or 1
    n_cats = len([c for c in ALL_CATEGORIES if en_cats.get(c, 0) > 0])
    expected = total / n_cats if n_cats else 0
    print(f"  Categories used: {n_cats} / {len(ALL_CATEGORIES)}")
    if en_stats["unused_categories"]:
        print(f"  Unused: {', '.join(en_stats['unused_categories'])}")
    print(f"  Expected ~{expected:.1f} facts per category if perfectly even")
    print()
    print(f"  {'category':<16} {'count':>5} {'share':>7} {'vs even':>8}")
    print("  " + "-" * 40)
    for cat in ALL_CATEGORIES:
        n = en_cats.get(cat, 0)
        if n == 0 and cat not in en_stats["unused_categories"]:
            continue
        pct = 100 * n / total
        dev = 100 * (n - expected) / expected if expected else 0
        flag = " !" if abs(dev) > 15 else ""
        print(f"  {cat:<16} {n:>5} {pct:>6.1f}% {dev:>+7.0f}%{flag}")

    print("\n## Suggested agent commands")
    print("  python3 tools/content_summary.py")
    print("  python3 tools/verify_category_cooldown.py")
    print("  python3 tools/verify_fact_uniqueness.py --published-only")
    print("  python3 tools/build_manifest.py")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Smart Facts content")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    facts = load_manifest(args.manifest)
    md_scan = scan_markdown(args.content_dir)
    en_stats = analyze_facts(facts, "en-US")
    pl_stats = analyze_facts(facts, "pl-PL")

    if args.json:
        json.dump(
            {"markdown": md_scan, "en-US": en_stats, "pl-PL": pl_stats},
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        print()
        return 0

    print_report(
        md_scan=md_scan,
        en_stats=en_stats,
        pl_stats=pl_stats,
        manifest_path=args.manifest,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
