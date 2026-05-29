#!/usr/bin/env python3
"""Fill calendar facts from MIT science-facts + Wikipedia summaries (EN + PL)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from content_lib import (
    CONTENT_DIR,
    LOCALES,
    fact_id,
    iter_calendar_days,
    load_fact_file,
    normalize_text,
    slot_path,
    write_fact_md,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "tools" / "category_plan.json"
CACHE_DIR = ROOT / "tools" / "cache"
USED_FACTS_CACHE = CACHE_DIR / "used_fact_texts.txt"
SCIENCE_FACTS_URL = (
    "https://raw.githubusercontent.com/Royal-lobster/science-facts-project/main/facts.json"
)

SOURCE_TO_CATEGORY = {
    "botany": "biology",
    "zoology": "animals",
    "animals": "animals",
    "physics": "science",
    "chemistry": "science",
    "astronomy": "astronomy",
    "math": "math",
    "mathematics": "math",
    "history": "history",
    "geography": "geography",
    "technology": "technology",
    "psychology": "psychology",
    "language": "language",
    "food": "food",
    "medicine": "biology",
    "environment": "environment",
    "marine": "biology",
    "space": "astronomy",
}

BLOCKLIST = re.compile(
    r"\b(death|suicide|murder|rape|porn|nazi|genocide|torture|abortion)\b",
    re.I,
)


def map_category(source_file: str, raw_category: str) -> str:
    key = source_file.replace(".json", "").split("_")[0].lower()
    if key in SOURCE_TO_CATEGORY:
        return SOURCE_TO_CATEGORY[key]
    for part in raw_category.lower().split("_"):
        if part in SOURCE_TO_CATEGORY:
            return SOURCE_TO_CATEGORY[part]
    return "science"


def load_science_facts(cache: Path) -> list[dict[str, str]]:
    cache.parent.mkdir(parents=True, exist_ok=True)
    if not cache.exists():
        print(f"Downloading {SCIENCE_FACTS_URL} …")
        with urllib.request.urlopen(SCIENCE_FACTS_URL, timeout=120) as resp:
            cache.write_bytes(resp.read())
    data = json.loads(cache.read_text(encoding="utf-8"))
    return data


def first_sentence(text: str, max_len: int = 120) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    for sep in (". ", "? ", "! "):
        if sep in text:
            sent = text.split(sep, 1)[0] + sep.strip()
            if len(sent) <= max_len:
                return sent.rstrip(".") + "."
    if len(text) > max_len:
        return text[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return text if text.endswith(".") else text + "."


def title_from_text(text: str) -> str:
    sent = first_sentence(text, 90)
    sent = re.sub(r"^(The|A|An)\s+", "", sent, flags=re.I)
    if len(sent) > 70:
        sent = sent[:67].rsplit(" ", 1)[0] + "…"
    return sent.rstrip(".")


def teaser_from_text(text: str) -> str:
    return first_sentence(text, 100)


def body_en(text: str, wiki_url: str) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=2)
    para = parts[0]
    if len(parts) > 1 and len(para) < 200:
        para = " ".join(parts[:2])
    if len(para) > 320:
        para = para[:317].rsplit(" ", 1)[0] + "…"
    bold = re.sub(
        r"\b(\d+[\d,.]*\s*(?:million|billion|meters|feet|km|years|percent|%)?)\b",
        r"**\1**",
        para,
        count=1,
    )
    article = wiki_url.split("/wiki/")[-1] if "/wiki/" in wiki_url else "Article"
    article = urllib.parse.unquote(article.replace("_", " "))
    return (
        f"{bold}\n\n"
        f"[{article} (Wikipedia)]({wiki_url})"
    )


_WIKI_CACHE: dict[tuple[str, str], dict[str, str] | None] = {}


def wiki_summary(lang: str, title: str) -> dict[str, str] | None:
    key = (lang, title.lower())
    if key in _WIKI_CACHE:
        return _WIKI_CACHE[key]
    encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": "SmartFactsPopulate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        _WIKI_CACHE[key] = None
        return None
    extract = data.get("extract", "")
    if not extract or len(extract) < 40:
        return None
    page_title = data.get("title", title)
    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
    result = {"title": page_title, "extract": extract, "url": page_url}
    _WIKI_CACHE[key] = result
    return result


def pl_wiki_title_from_en_url(wiki_url: str) -> str | None:
    article = urllib.parse.unquote(wiki_url.split("/wiki/")[-1].replace("_", " "))
    api = (
        "https://en.wikipedia.org/w/api.php?"
        + urllib.parse.urlencode(
            {
                "action": "query",
                "titles": article,
                "prop": "langlinks",
                "lllang": "pl",
                "format": "json",
            }
        )
    )
    req = urllib.request.Request(api, headers={"User-Agent": "SmartFactsPopulate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            links = page.get("langlinks") or []
            if links:
                return str(links[0]["title"])
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError):
        pass
    return None


def translate_en_pl(text: str) -> str:
    if len(text) > 450:
        text = text[:447] + "…"
    url = (
        "https://api.mymemory.translated.net/get?"
        + urllib.parse.urlencode({"q": text, "langpair": "en|pl"})
    )
    req = urllib.request.Request(url, headers={"User-Agent": "SmartFactsPopulate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        out = data.get("responseData", {}).get("translatedText", "")
        if out and "MYMEMORY WARNING" not in out.upper():
            return out
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass
    return text


def pl_from_science_text(text: str, wiki_url: str, used_pl: set[str]) -> tuple[str, str, str]:
    """One MT request per fact when PL Wikipedia extract is unavailable or duplicate."""
    para = text if len(text) < 280 else text[:277].rsplit(" ", 1)[0] + "…"
    block = translate_en_pl(f"{title_from_text(text)}. {teaser_from_text(text)} {para}")
    parts = re.split(r"(?<=[.!?])\s+", block.strip(), maxsplit=2)
    pl_title = parts[0].rstrip(".") if parts else title_from_text(text)
    if len(pl_title) > 70:
        pl_title = pl_title[:67] + "…"
    pl_teaser = parts[1] if len(parts) > 1 else teaser_from_text(block)
    pl_para = parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else block)
    pl_link_title = pl_wiki_title_from_en_url(wiki_url) or pl_title
    pl_wiki = f"https://pl.wikipedia.org/wiki/{urllib.parse.quote(pl_link_title.replace(' ', '_'))}"
    pl_body = f"{pl_para}\n\n[{pl_link_title} (Wikipedia)]({pl_wiki})"
    fp = normalize_text(f"{pl_title}|{pl_teaser[:60]}")
    used_pl.add(fp)
    return pl_title, pl_teaser, pl_body


def pl_from_en(
    text: str,
    en_title: str,
    en_teaser: str,
    en_body: str,
    wiki_url: str,
    used_pl: set[str],
) -> tuple[str, str, str, str]:
    pl_title = pl_wiki_title_from_en_url(wiki_url)
    pl_article = pl_title or urllib.parse.unquote(wiki_url.split("/wiki/")[-1].replace("_", " "))
    pl = wiki_summary("pl", pl_article)
    if pl:
        title = pl["title"]
        if len(title) > 70:
            title = title[:67] + "…"
        teaser = first_sentence(pl["extract"], 100)
        extract = pl["extract"]
        if len(extract) > 300:
            extract = extract[:297].rsplit(" ", 1)[0] + "…"
        body = f"{extract}\n\n[{title} (Wikipedia)]({pl['url']})"
        fp = normalize_text(f"{title}|{teaser[:60]}|{extract[:80]}")
        if fp not in used_pl:
            used_pl.add(fp)
            return title, teaser, body, pl["url"]
    return (*pl_from_science_text(text, wiki_url, used_pl), wiki_url.replace("en.wikipedia", "pl.wikipedia"))


def pool_facts(raw: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_cat: dict[str, list[dict[str, str]]] = {}
    seen: set[str] = set()
    for item in raw:
        text = item.get("text", "").strip()
        if len(text) < 60 or len(text) > 450:
            continue
        if BLOCKLIST.search(text):
            continue
        norm = normalize_text(text)
        if norm in seen:
            continue
        seen.add(norm)
        cat = map_category(item.get("source_file", ""), item.get("category", ""))
        url = item.get("source_url", "")
        if not url.startswith("http"):
            continue
        by_cat.setdefault(cat, []).append(
            {"text": text, "url": url, "category": cat}
        )
    return by_cat


def should_skip(path: Path, force: bool) -> bool:
    if not path.exists():
        return False
    if force:
        return False
    try:
        loaded = load_fact_file(path)
    except ValueError:
        return False
    meta = loaded["meta"]
    if not bool(meta.get("published", False)):
        return False
    title = str(meta.get("title", "")).strip()
    body = str(loaded["body"]).strip()
    if title and not body.startswith("<!--") and "_Treść do uzupełnienia_" not in body:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Populate year content from science-facts")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--start", default="01-01", help="MM-DD inclusive")
    parser.add_argument("--end", default="12-31", help="MM-DD inclusive")
    parser.add_argument("--force", action="store_true", help="Overwrite published facts")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.plan.exists():
        print("Run: python3 tools/plan_categories.py", file=sys.stderr)
        return 1

    plan: dict[str, list[str]] = json.loads(args.plan.read_text(encoding="utf-8"))
    raw = load_science_facts(CACHE_DIR / "science_facts.json")
    by_cat = pool_facts(raw)
    top = sorted(by_cat.items(), key=lambda x: len(x[1]), reverse=True)[:8]
    print("Pool sizes:", {k: len(v) for k, v in top}, "…")

    cursors: dict[str, int] = {k: 0 for k in by_cat}
    used_global: set[str] = set()
    used_pl: set[str] = set()
    if USED_FACTS_CACHE.exists() and not args.force:
        used_global = {
            line.strip()
            for line in USED_FACTS_CACHE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    def next_fact(category: str) -> dict[str, str] | None:
        search_order = [category, "science", "general", "biology", "geography"]
        seen_orders: list[str] = []
        for cat in search_order:
            if cat in seen_orders:
                continue
            seen_orders.append(cat)
            queue = by_cat.get(cat) or []
            if not queue:
                continue
            start = cursors.get(cat, 0)
            for offset in range(len(queue)):
                idx = (start + offset) % len(queue)
                item = queue[idx]
                norm = normalize_text(item["text"])
                if norm in used_global:
                    continue
                used_global.add(norm)
                cursors[cat] = (idx + 1) % len(queue)
                return item
        for cat, queue in by_cat.items():
            if not queue:
                continue
            start = cursors.get(cat, 0)
            for offset in range(len(queue)):
                idx = (start + offset) % len(queue)
                item = queue[idx]
                norm = normalize_text(item["text"])
                if norm in used_global:
                    continue
                used_global.add(norm)
                cursors[cat] = (idx + 1) % len(queue)
                return item
        return None

    sm, sd = map(int, args.start.split("-"))
    em, ed = map(int, args.end.split("-"))
    in_range = False
    written = 0
    skipped = 0

    for month, day in iter_calendar_days():
        key = f"{month:02d}-{day:02d}"
        if key == f"{sm:02d}-{sd:02d}":
            in_range = True
        if not in_range:
            continue
        cats = plan.get(key, [])
        if len(cats) < 3:
            print(f"Missing plan for {key}", file=sys.stderr)
            return 1
        for sequence in range(3):
            category = cats[sequence]
            fid = fact_id(month, day, sequence, category)
            paths: dict[str, Path] = {}
            for loc in LOCALES:
                existing = slot_path(args.content_dir, loc, month, day, sequence)
                target = args.content_dir / loc / f"{fid}.md"
                if (
                    existing
                    and existing != target
                    and not args.dry_run
                    and not should_skip(existing, args.force)
                ):
                    if target.exists() and not should_skip(target, args.force):
                        existing.unlink()
                    elif not target.exists():
                        existing.rename(target)
                paths[loc] = target
            if all(should_skip(p, args.force) for p in paths.values()):
                skipped += 1
                continue
            item = next_fact(category)
            if item is None:
                print(f"No fact available for {fid}", file=sys.stderr)
                return 1
            text = item["text"]
            url = item["url"]
            en_title = title_from_text(text)
            if len(en_title) < 12:
                en_title = first_sentence(text, 70).rstrip(".")
            if len(en_title) < 12:
                continue
            en_teaser = teaser_from_text(text)
            en_body = body_en(text, url)
            pl_title, pl_teaser, pl_body, _ = pl_from_en(
                text, en_title, en_teaser, en_body, url, used_pl
            )
            blocks = {
                "en-US": {"title": en_title, "teaser": en_teaser, "body": en_body},
                "pl-PL": {"title": pl_title, "teaser": pl_teaser, "body": pl_body},
            }
            for locale in LOCALES:
                path = paths[locale]
                if should_skip(path, args.force):
                    continue
                block = blocks[locale]
                if args.dry_run:
                    print(f"Would write {path.name} [{locale}]")
                    continue
                write_fact_md(
                    path,
                    fact_id_value=fid,
                    locale=locale,
                    month=month,
                    day=day,
                    sequence=sequence,
                    category=category,
                    title=block["title"],
                    teaser=block["teaser"],
                    body=block["body"],
                    published=True,
                    version=1,
                )
                written += 1
        if key == f"{em:02d}-{ed:02d}":
            break

    if not args.dry_run:
        USED_FACTS_CACHE.parent.mkdir(parents=True, exist_ok=True)
        USED_FACTS_CACHE.write_text(
            "\n".join(sorted(used_global)) + "\n",
            encoding="utf-8",
        )

    print(f"{'Would write' if args.dry_run else 'Wrote'} {written} file(s); skipped {skipped} already-published.")
    print(f"Unique facts used: {len(used_global)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
