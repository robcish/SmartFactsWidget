#!/usr/bin/env python3
"""Rewrite pl-PL facts from en-US sources with Polish text and valid Wikipedia links."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from content_lib import CONTENT_DIR, WIKI_LINK, load_fact_file, write_fact_md

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "tools" / "cache"
UA = "SmartFactsFixPl/1.0"

POLISH_CHARS = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")


def has_polish(text: str) -> bool:
    return any(c in text for c in POLISH_CHARS)


def strip_wiki(body: str) -> str:
    return WIKI_LINK.sub("", body).strip()


def extract_wiki_url(body: str) -> str | None:
    match = WIKI_LINK.search(body)
    return match.group(1) if match else None


def en_article_title(url: str) -> str:
    return urllib.parse.unquote(url.split("/wiki/")[-1].replace("_", " "))


def wiki_page_url(lang: str, title: str) -> str:
    encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
    return f"https://{lang}.wikipedia.org/wiki/{encoded}"


def http_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def pl_title_from_en(en_url: str, cache: dict[str, str | None]) -> str | None:
    if en_url in cache:
        return cache[en_url]
    en_title = en_article_title(en_url)
    api = (
        "https://en.wikipedia.org/w/api.php?"
        + urllib.parse.urlencode(
            {
                "action": "query",
                "titles": en_title,
                "prop": "langlinks",
                "lllang": "pl",
                "format": "json",
            }
        )
    )
    data = http_json(api)
    pl_title = None
    if data:
        for page in data.get("query", {}).get("pages", {}).values():
            for link in page.get("langlinks") or []:
                if link.get("lang") == "pl":
                    pl_title = str(link.get("title") or link.get("*") or "")
                    break
    cache[en_url] = pl_title
    return pl_title


def wiki_summary(lang: str, title: str, cache: dict[tuple[str, str], dict | None]) -> dict | None:
    key = (lang, title)
    if key in cache:
        return cache[key]
    encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    data = http_json(url)
    if not data or data.get("type") == "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
        cache[key] = None
        return None
    extract = (data.get("extract") or "").strip()
    if len(extract) < 20:
        cache[key] = None
        return None
    result = {
        "title": data.get("title", title),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", wiki_page_url(lang, title)),
        "extract": extract,
    }
    cache[key] = result
    return result


def pl_search_title(query: str, cache: dict[str, str | None]) -> str | None:
    if query in cache:
        return cache[query]
    api = (
        "https://pl.wikipedia.org/w/api.php?"
        + urllib.parse.urlencode(
            {
                "action": "opensearch",
                "search": query[:80],
                "limit": 3,
                "namespace": 0,
                "format": "json",
            }
        )
    )
    data = http_json(api)
    title = None
    if data and len(data) >= 2 and data[1]:
        title = str(data[1][0])
    cache[query] = title
    return title


def resolve_pl_wiki(
    en_wiki: str | None,
    en_title: str,
    caches: dict,
) -> tuple[str, str] | None:
    """Return (link_label, pl_wiki_url) or None."""
    ll_cache: dict[str, str | None] = caches.setdefault("langlinks", {})
    sum_cache: dict[tuple[str, str], dict | None] = caches.setdefault("summary", {})
    search_cache: dict[str, str | None] = caches.setdefault("search", {})

    candidates: list[str] = []
    if en_wiki:
        pl_from_en = pl_title_from_en(en_wiki, ll_cache)
        if pl_from_en:
            candidates.append(pl_from_en)
        candidates.append(en_article_title(en_wiki))

    # Shorten EN title for search (first few words)
    short = re.split(r"[,.:;—–-]", en_title)[0].strip()
    words = short.split()[:5]
    if words:
        candidates.append(" ".join(words))

    seen: set[str] = set()
    for cand in candidates:
        cand = cand.strip()
        if not cand or cand.lower() in seen:
            continue
        seen.add(cand.lower())
        summary = wiki_summary("pl", cand, sum_cache)
        if summary:
            title = str(summary["title"])
            url = str(summary["url"])
            if "pl.wikipedia.org/wiki/" in url and len(title) < 120:
                return title, url

        found = pl_search_title(cand, search_cache)
        if found and found.lower() not in seen:
            seen.add(found.lower())
            summary = wiki_summary("pl", found, sum_cache)
            if summary:
                return str(summary["title"]), str(summary["url"])

    return None


def is_pl_already_ok(title: str, teaser: str, body: str) -> bool:
    if not has_polish(title) or not has_polish(teaser):
        return False
    if not has_polish(strip_wiki(body)[:300]):
        return False
    match = WIKI_LINK.search(body)
    if not match:
        return True
    url = match.group(1)
    if "pl.wikipedia.org" not in url:
        return False
    slug = urllib.parse.unquote(url.split("/wiki/")[-1])
    if len(slug) > 80 or "…" in url or "%E2%80%A6" in slug:
        return False
    if slug.count("_") > 12 and len(slug) > 40:
        return False
    return True


def first_sentence(text: str, max_len: int = 110) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    for sep in (". ", "? ", "! ", "… "):
        if sep in text:
            s = text.split(sep, 1)[0] + sep.strip()
            if len(s) <= max_len:
                return s if s.endswith((".", "?", "!")) else s + "."
    if len(text) > max_len:
        return text[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return text if text.endswith((".", "?", "!", "…")) else text + "."


def shorten_title(text: str, max_len: int = 68) -> str:
    text = text.strip().rstrip(".")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rsplit(" ", 1)[0] + "…"


def translate_batch(translator, texts: list[str], delay: float) -> list[str]:
    from deep_translator import GoogleTranslator

    out: list[str] = []
    for text in texts:
        if not text.strip():
            out.append(text)
            continue
        try:
            translated = translator.translate(text[:4500])
            out.append(translated or text)
        except Exception:
            out.append(text)
        time.sleep(delay)
    return out


def build_pl_body(text: str, link: tuple[str, str] | None) -> str:
    text = text.strip()
    if link:
        label, url = link
        return f"{text}\n\n[{label} (Wikipedia)]({url})"
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix pl-PL translations and Wikipedia links")
    parser.add_argument("--content-dir", type=Path, default=CONTENT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Rewrite even if PL looks OK")
    parser.add_argument("--delay", type=float, default=0.12, help="Delay between translate calls")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Install: pip install deep-translator", file=sys.stderr)
        return 1

    translator = GoogleTranslator(source="en", target="pl")
    pl_dir = args.content_dir / "pl-PL"
    en_dir = args.content_dir / "en-US"
    paths = sorted(pl_dir.glob("*.md"))
    if args.limit:
        paths = paths[: args.limit]

    caches: dict = {}
    fixed = skipped = no_link = 0

    for i, pl_path in enumerate(paths, 1):
        pl = load_fact_file(pl_path)
        meta = pl["meta"]
        if not bool(meta.get("published", False)):
            continue
        fact_id = str(meta["id"])
        en_path = en_dir / f"{fact_id}.md"
        if not en_path.exists():
            print(f"Missing EN: {fact_id}", file=sys.stderr)
            continue

        en = load_fact_file(en_path)
        en_meta = en["meta"]
        en_body_raw = str(en["body"])
        en_wiki = extract_wiki_url(en_body_raw)
        en_body = strip_wiki(en_body_raw)
        en_title = str(en_meta.get("title", "")).strip()
        en_teaser = str(en_meta.get("teaser", "")).strip()

        if not args.force and is_pl_already_ok(
            str(meta.get("title", "")),
            str(meta.get("teaser", "")),
            str(pl["body"]),
        ):
            skipped += 1
            continue

        link = resolve_pl_wiki(en_wiki, en_title, caches)
        if link is None:
            no_link += 1

        pl_title, pl_teaser, pl_body_core = translate_batch(
            translator, [en_title, en_teaser, en_body], args.delay
        )
        pl_title = shorten_title(pl_title)
        pl_teaser = first_sentence(pl_teaser, 100)
        if not has_polish(pl_title):
            pl_title = shorten_title(en_title)

        body = build_pl_body(pl_body_core, link)

        if args.dry_run:
            print(f"Would fix {fact_id} link={'yes' if link else 'no'}")
            fixed += 1
            continue

        write_fact_md(
            pl_path,
            fact_id_value=fact_id,
            locale="pl-PL",
            month=int(meta["month"]),
            day=int(meta["day"]),
            sequence=int(meta["sequence_index"]),
            category=str(meta["category"]),
            title=pl_title,
            teaser=pl_teaser,
            body=body,
            published=True,
            version=int(meta.get("version", 1)),
        )
        fixed += 1
        if i % 25 == 0:
            print(f"  … {i}/{len(paths)} fixed={fixed} skipped={skipped} no_link={no_link}", flush=True)

    print(
        f"Done: fixed={fixed}, skipped_ok={skipped}, without_wiki_link={no_link}, "
        f"total_scanned={len(paths)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
