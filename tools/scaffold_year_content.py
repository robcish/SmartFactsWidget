#!/usr/bin/env python3
"""Scaffold 366 days × 2 facts × 2 locales; fill content from a start date onward."""

from __future__ import annotations

import shutil
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

LOCALES = ("pl-PL", "en-US")
FACTS_PER_DAY = 2

CATEGORIES = [
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

FILL_START = date(2026, 5, 29)
FILL_DAYS = 8


def iter_calendar_days() -> list[tuple[int, int]]:
    days: list[tuple[int, int]] = []
    d = date(2024, 1, 1)
    end = date(2024, 12, 31)
    while d <= end:
        days.append((d.month, d.day))
        d += timedelta(days=1)
    return days


def fact_id(month: int, day: int, sequence: int, category: str) -> str:
    return f"{month:02d}-{day:02d}-{sequence}-{category}"


def write_md(
    path: Path,
    *,
    fact_id_value: str,
    locale: str,
    month: int,
    day: int,
    sequence: int,
    category: str,
    title: str,
    teaser: str,
    body: str,
    published: bool,
    version: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                f"id: {fact_id_value}",
                f"locale: {locale}",
                f"month: {month}",
                f"day: {day}",
                f"sequence_index: {sequence}",
                f"category: {category}",
                f"title: {title}",
                f"teaser: {teaser}",
                f"published: {'true' if published else 'false'}",
                f"version: {version}",
                "---",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )


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


def main() -> None:
    rules_path = CONTENT / "FACT_GENERATION_RULES.md"
    rules_content = rules_path.read_text(encoding="utf-8") if rules_path.exists() else None

    for loc in LOCALES:
        folder = CONTENT / loc
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)

    from generate_facts_database import FACTS  # noqa: WPS433

    fill_end = FILL_START + timedelta(days=FILL_DAYS - 1)
    fill_ptr = 0
    filled_days = 0

    for day_index, (month, day) in enumerate(iter_calendar_days()):
        try:
            cal_date = date(2026, month, day)
        except ValueError:
            cal_date = None

        is_filled = cal_date is not None and FILL_START <= cal_date <= fill_end
        day_facts: list[tuple[str, str, str, str, str, str, str]] = []
        if is_filled and fill_ptr + 1 < len(FACTS):
            day_facts = [FACTS[fill_ptr], FACTS[fill_ptr + 1]]
            fill_ptr += 2
            filled_days += 1

        for sequence in range(FACTS_PER_DAY):
            if day_facts and sequence < len(day_facts):
                cat, pl_t, pl_te, pl_b, en_t, en_te, en_b = day_facts[sequence]
                category = cat
                fid = fact_id(month, day, sequence, category)
                write_md(
                    CONTENT / "pl-PL" / f"{fid}.md",
                    fact_id_value=fid,
                    locale="pl-PL",
                    month=month,
                    day=day,
                    sequence=sequence,
                    category=category,
                    title=pl_t,
                    teaser=pl_te,
                    body=pl_b,
                    published=True,
                    version=1,
                )
                write_md(
                    CONTENT / "en-US" / f"{fid}.md",
                    fact_id_value=fid,
                    locale="en-US",
                    month=month,
                    day=day,
                    sequence=sequence,
                    category=category,
                    title=en_t,
                    teaser=en_te,
                    body=en_b,
                    published=True,
                    version=1,
                )
            else:
                category = CATEGORIES[(day_index * FACTS_PER_DAY + sequence) % len(CATEGORIES)]
                fid = fact_id(month, day, sequence, category)
                for locale in LOCALES:
                    write_md(
                        CONTENT / locale / f"{fid}.md",
                        fact_id_value=fid,
                        locale=locale,
                        month=month,
                        day=day,
                        sequence=sequence,
                        category=category,
                        title="",
                        teaser="",
                        body=template_body(month, day, sequence, locale),
                        published=False,
                        version=0,
                    )

    if rules_content:
        rules_path.write_text(rules_content, encoding="utf-8")

    total_days = len(iter_calendar_days())
    print(
        f"Scaffolded {total_days} days × {FACTS_PER_DAY} slots × {len(LOCALES)} locales "
        f"= {total_days * FACTS_PER_DAY * len(LOCALES)} files"
    )
    print(f"Filled {filled_days} days from {FILL_START} through {fill_end}")


if __name__ == "__main__":
    main()
