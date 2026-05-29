#!/usr/bin/env python3
"""Verify Wikipedia URLs in published Markdown facts (HTTP 200)."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\((https?://[^)]+)\)")


def is_published(raw: str) -> bool:
    if not raw.startswith("---"):
        return False
    parts = raw.split("---", 2)
    if len(parts) < 2:
        return False
    return "published: true" in parts[1]


def check_url(url: str) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "SmartFactsLinkCheck/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                return True, "200"
            return False, f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        if error.code in {403, 405}:
            return check_url_get(url)
        return False, f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001
        return False, str(error)


def check_url_get(url: str) -> tuple[bool, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "SmartFactsLinkCheck/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.status == 200, "200"
    except urllib.error.HTTPError as error:
        return False, f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001
        return False, str(error)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Wikipedia links in published facts")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    args = parser.parse_args()

    failures: list[str] = []
    checked = 0

    for md_file in sorted(args.content_dir.rglob("*.md")):
        if md_file.name == "FACT_GENERATION_RULES.md":
            continue
        raw = md_file.read_text(encoding="utf-8")
        if not is_published(raw):
            continue
        for url in MARKDOWN_LINK.findall(raw):
            checked += 1
            ok, detail = check_url(url)
            if not ok:
                rel = md_file.relative_to(ROOT)
                failures.append(f"{rel}: {url} ({detail})")

    if failures:
        print(f"FAILED {len(failures)} / {checked} Wikipedia URLs:", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"OK — {checked} Wikipedia URLs in published facts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
