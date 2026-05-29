# Fact generation rules (for AI agents & humans)

These rules apply when creating facts in `content/`.  
Repo entry point for agents: **[AGENTS.md](../AGENTS.md)**.

## Calendar model (v2)

- Facts repeat **every year** on the same **month + day** (no year in the database).
- **Three facts per day** per locale: `sequence_index` `0`, `1`, and `2`.
- Slot times (local): **00:00:01**, **08:00**, **16:00** — see `DayScheduleResolver.kt`.
- **ID / filename:** `{MM}-{DD}-{sequence}-{category}.md`  
  Example: `05-29-0-animals.md`, `05-29-1-biology.md`, `05-29-2-science.md`

## Frontmatter

```yaml
id: 05-29-0-animals
locale: pl-PL
month: 5
day: 29
sequence_index: 0
category: animals
title: Krowy mają przyjaciół
teaser: Krowy tęsknią za swoimi ulubionymi kompanami.
published: true
version: 1
```

| Field | Notes |
|-------|--------|
| `published` | `false` = template; excluded from manifest |
| `title` | Required for manifest; must be non-empty |
| `teaser` | One short sentence for the home-screen widget |
| `category` | Must be one of the slugs in [Valid categories](#valid-categories) |

## Valid categories

`science`, `math`, `biology`, `animals`, `technology`, `history`, `geography`, `astronomy`, `language`, `psychology`, `philosophy`, `society`, `law`, `finance`, `culture`, `mythology`, `myth-busting`, `general`, `reflection`, `sport`, `food`, `environment`

## Category cooldown (2 days)

The **same category must not appear again within 2 calendar days** (by month/day in the annual calendar).

Before assigning a category to a new fact, check the previous two days in your batch (and existing published facts). If collisions exist, **swap categories** between days (keep the fact text) rather than forcing a mismatched label.

## Category must match the topic (icon in the app)

The `category` field controls the **icon** in the widget and detail screen. Assign it from the **subject** of the fact, not from the filename slot or batch plan alone.

| Topic belongs in | Examples |
|------------------|----------|
| `geography`, `environment`, `science` | Climate records, weather extremes, oceans, ice sheets |
| `math` | Proofs, algorithms, numbers—not temperature records |
| `mythology` | Gods, legends, folklore—not thermometer readings |
| `myth-busting` | Debunking a common false belief—not raw data tables |

**Do not** paste unrelated facts into a day’s planned categories just to fill slots. If three facts on one day would all cite the same Wikipedia list (e.g. weather records), either **spread them across nearby days** or **rewrite** them as distinct angles with the correct category.

**Titles and teasers** must be short, human-written sentences—not truncated scrapes ending in `…`.

## Uniqueness

Each published fact must be **unique across the whole year** (same topic/teaser should not repeat on another day). Before publishing a batch:

```bash
python3 tools/verify_fact_uniqueness.py --published-only
python3 tools/verify_category_cooldown.py
```

## Content quality

- **Tone:** calm, curious, accessible; portfolio/education app (not clickbait).
- **Teaser** (widget): one or two short sentences; the widget wraps the full teaser (no fixed line cap). Keep it concise so very small widgets are still readable.
- **Body** (detail): 1–3 short paragraphs, Markdown; optional `**bold**`; end with a Wikipedia link when possible.
- **Locales:** always create **both** `pl-PL` and `en-US` with the same `id`, `month`, `day`, `sequence_index`, `category`. **Translate**, do not paste English into PL files.
- **Wikipedia links:** use real article titles in the URL. Run `python3 tools/verify_wikipedia_links.py`. PL and EN titles often differ; if there is no sensible PL article for the topic, **omit the link** (do not use a generic category article).

## Example pair (en-US + pl-PL)

**`content/en-US/05-29-0-animals.md`**

```markdown
---
id: 05-29-0-animals
locale: en-US
month: 5
day: 29
sequence_index: 0
category: animals
title: Cows have best friends
teaser: Cows miss their favorite herd companions.
published: true
version: 1
---
Research shows cows **form strong bonds** with specific herd mates and experience significant stress when separated.

[More on cattle behavior (Wikipedia)](https://en.wikipedia.org/wiki/Cattle)
```

**`content/pl-PL/05-29-0-animals.md`** — same `id` / calendar fields, Polish copy:

```markdown
---
id: 05-29-0-animals
locale: pl-PL
month: 5
day: 29
sequence_index: 0
category: animals
title: Krowy mają przyjaciół
teaser: Krowy tęsknią za swoimi ulubionymi kompanami.
published: true
version: 1
---
Badania pokazują, że krowy **bardzo przywiązują się** do wybranych osób ze stada i odczuwają silny stres po rozłączeniu.

[Bydło (Wikipedia)](https://pl.wikipedia.org/wiki/Byd%C5%82o)
```

## What is already published?

Check before filling a date range:

```bash
python3 -c "
import json
from pathlib import Path
m = json.loads(Path('docs/facts.json').read_text())
days = sorted({(f['month'], f['day']) for f in m['facts']})
print(len(m['facts']), 'facts;', 'days', days[0], '…', days[-1] if days else 'none')
"
```

Or: `grep -l "published: true" content/en-US/MM-*.md`

As of last manifest build, published window may be limited (e.g. May–early June); most other `.md` files are `published: false` templates.

## Scaffolding & manifest

```bash
# Optional: generate template files for the year (edit FILL_START in script)
python3 tools/scaffold_year_content.py

# Quality checks (run before manifest)
python3 tools/verify_category_cooldown.py
python3 tools/verify_fact_uniqueness.py --published-only

# Build manifest (only published facts with non-empty title)
python3 tools/build_manifest.py

# Validate Wikipedia URLs
python3 tools/verify_wikipedia_links.py

# Optional: refresh offline bundle in the APK
cp docs/facts.json app/src/main/assets/seed_facts.json
```

## Publishing & delivery

1. Set `published: true` and fill `title`, `teaser`, body.
2. Push to `main` → GitHub Action (`.github/workflows/publish.yml`) builds and deploys `docs/facts.json` to GitHub Pages.
3. The app downloads the manifest (`FACTS_MANIFEST_URL`) and compares `manifest_version`; **no Play Store update required** for new facts only.
4. Update `seed_facts.json` in the repo when you want fresh installs / offline fallback to include the same facts.

---

## External sources (partial — agents must research beyond these)

The links below are **starting points only**. They cover a fraction of possible topics. Agents must **verify** claims, **rewrite** in our format (teaser + body), produce **both locales**, and find additional facts via Wikipedia, reputable references, and their own research. **Do not** bulk-import or copy text verbatim unless the license clearly allows it and attribution is handled.

| Source | URL | License (check before use) | Good for |
|--------|-----|------------------------------|----------|
| Science Facts dataset | https://github.com/Royal-lobster/science-facts-project | MIT | Obscure **science** facts; rewrite + link sources |
| Hugging Face mirror | https://huggingface.co/datasets/Royal-lobster/science-facts | MIT | Same dataset |
| Wikipedia **On this day** API | https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day | CC BY-SA | **History** aligned to month/day; summarize, link article |
| REST example (EN events) | `https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{MM}/{DD}` | CC BY-SA | Pick 1 event per slot; rewrite |
| Open Trivia DB | https://opentdb.com/ | CC BY-SA 4.0 | Quiz Q&A — poor fit; heavy rewrite; attribution if used |
| AtlasPI (historical geography) | https://huggingface.co/datasets/clirim911/atlaspi-historical-geography | Apache 2.0 | Geography/history structure; not ready-made teasers |
| CIA World Factbook (JSON) | https://github.com/iancoleman/cia_world_factbook_api (community JSON) | Public domain (factbook) | Country **geography** stats; rewrite |

### Using external material responsibly

1. **Prefer primary verification** — Wikipedia article, museum/university pages, papers.
2. **Rewrite** — teaser + body in our voice; never dump API JSON into `body_md`.
3. **PL + EN** — independent translations, same fact.
4. **Licenses** — MIT/Apache/Public domain: still rewrite; CC BY-SA: attribution may be required if derivative; when unsure, use facts you compose from reading sources.
5. **Timeless vs dated** — calendar model repeats yearly; avoid “in 2024 …” unless the hook is still valid every year.

### Agent workflow summary

```
1. Read AGENTS.md + this file
2. Confirm date range + published status of templates
3. Plan categories (2-day cooldown)
4. Write en-US + pl-PL pairs
5. build_manifest.py → verify_wikipedia_links.py
6. Optionally update seed_facts.json
7. Commit content/ + docs/facts.json (+ seed if changed)
```
