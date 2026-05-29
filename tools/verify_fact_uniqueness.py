#!/usr/bin/env python3
"""Detect duplicate or near-duplicate published facts."""

from __future__ import annotations

import argparse
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import unquote, urlparse

from content_lib import CONTENT_DIR, iter_fact_files, load_fact_file, normalize_text

WIKI_LINK = re.compile(r"\[[^\]]*\]\((https?://[^)]+)\)")


def wiki_article(url: str) -> str | None:
    parsed = urlparse(url)
    if "wikipedia.org" not in parsed.netloc:
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return None
    return unquote(parts[-1]).lower()


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()


def teaser_bucket(teaser: str) -> str:
    words = teaser.split()[:6]
    return " ".join(words)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check fact uniqueness in content/")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--published-only", action="store_true", default=True)
    parser.add_argument("--strict", action="store_true", help="Stricter similarity thresholds")
    parser.add_argument("--stdin-title", type=str, help="Check one title against the database")
    args = parser.parse_args()

    teaser_thresh = 0.92 if args.strict else 0.85
    body_thresh = 0.88 if args.strict else 0.80

    facts: list[dict[str, object]] = []
    for path in iter_fact_files(args.content_dir):
        try:
            loaded = load_fact_file(path)
        except ValueError:
            continue
        meta = loaded["meta"]
        if args.published_only and not bool(meta.get("published", False)):
            continue
        locale = str(meta.get("locale", path.parent.name))
        title = str(meta.get("title", "")).strip()
        teaser = str(meta.get("teaser", "")).strip()
        body = str(loaded["body"])
        if args.stdin_title and locale == "en-US":
            if similarity(normalize_text(title), normalize_text(args.stdin_title)) >= 0.9:
                print(f"Title match: {meta.get('id')} — {title}")
                return 1
        if not title and args.published_only:
            continue
        wiki_urls = [wiki_article(m.group(1)) for m in WIKI_LINK.finditer(body)]
        facts.append(
            {
                "id": str(meta.get("id", path.stem)),
                "locale": locale,
                "title": title,
                "title_norm": normalize_text(title),
                "teaser_norm": normalize_text(teaser),
                "body_norm": normalize_text(body),
                "teaser_bucket": teaser_bucket(normalize_text(teaser)),
                "wiki": [w for w in wiki_urls if w],
            }
        )

    if args.stdin_title:
        print("No close title match found.")
        return 0

    errors: list[str] = []
    warnings: list[str] = []

    from collections import Counter

    id_counts = Counter(str(f["id"]) for f in facts)
    for fact_id, count in id_counts.items():
        if count > 2:
            errors.append(f"Fact id {fact_id} appears {count} times (expected at most 2 locales)")

    by_locale: dict[str, list[dict[str, object]]] = {}
    for fact in facts:
        by_locale.setdefault(str(fact["locale"]), []).append(fact)

    for locale, group in by_locale.items():
        title_map: dict[str, str] = {}
        fingerprint_map: dict[str, str] = {}
        wiki_map: dict[str, str] = {}
        teaser_buckets: dict[str, list[dict[str, object]]] = {}

        for fact in group:
            if fact["title_norm"] and len(str(fact["title_norm"])) >= 12:
                prev = title_map.get(str(fact["title_norm"]))
                if prev:
                    errors.append(
                        f"[{locale}] Exact title duplicate: {prev} vs {fact['id']} — {fact['title']}"
                    )
                else:
                    title_map[str(fact["title_norm"])] = str(fact["id"])

            fp = f"{fact['teaser_norm']}|{str(fact['body_norm'])[:80]}"
            if fact["teaser_norm"]:
                prev = fingerprint_map.get(fp)
                if prev:
                    errors.append(f"[{locale}] Fingerprint duplicate: {prev} vs {fact['id']}")
                else:
                    fingerprint_map[fp] = str(fact["id"])

            for w in fact["wiki"]:
                prev = wiki_map.get(w)
                if prev and prev != fact["id"]:
                    warnings.append(
                        f"Same Wikipedia article ({w}): {prev} vs {fact['id']}"
                    )
                else:
                    wiki_map[w] = str(fact["id"])

            bucket = str(fact["teaser_bucket"])
            if len(bucket) > 10:
                teaser_buckets.setdefault(bucket, []).append(fact)

        for bucket, candidates in teaser_buckets.items():
            if len(candidates) < 2:
                continue
            for i, a in enumerate(candidates):
                for b in candidates[i + 1 :]:
                    t_sim = similarity(str(a["teaser_norm"]), str(b["teaser_norm"]))
                    if t_sim >= teaser_thresh:
                        errors.append(
                            f"[{locale}] Similar teaser ({t_sim:.2f}): {a['id']} vs {b['id']}"
                        )
                    b_sim = similarity(str(a["body_norm"]), str(b["body_norm"]))
                    if b_sim >= body_thresh:
                        errors.append(
                            f"[{locale}] Similar body ({b_sim:.2f}): {a['id']} vs {b['id']}"
                        )

    if warnings:
        print(f"{len(warnings)} warning(s) (showing up to 15):")
        for w in warnings[:15]:
            print(f"  ! {w}")

    if errors:
        print(f"{len(errors)} error(s) (showing up to 40):")
        for e in errors[:40]:
            print(f"  ✗ {e}")
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more")
        return 1

    print(f"No uniqueness issues in {len(facts)} fact file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
