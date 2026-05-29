# Fact generation rules (for AI agents & humans)

These rules apply when creating facts in `content/`.

## Calendar model (v2)

- Facts repeat **every year** on the same **month + day** (no year in the database).
- **Two facts per day** per locale: `sequence_index` `0` (from 00:00:01) and `1` (from 12:00).
- The app computes exact slot times from the count of facts that day (see `DayScheduleResolver` in the Android app).
- **ID / filename:** `{MM}-{DD}-{sequence}-{category}.md`  
  Example: `05-29-0-animals.md`, `05-29-1-biology.md`

## Frontmatter

```yaml
id: 05-29-0-animals
locale: pl-PL
month: 5
day: 29
sequence_index: 0
category: animals
title: ...
teaser: ...
published: true   # false = template placeholder, omitted from manifest
version: 1
```

## Category cooldown (2 days)

The **same category must not appear again within 2 calendar days** (by month/day in the annual calendar).

## Content quality

- **Teaser** (widget): 1 short hook sentence.
- **Body** (detail): 2–4 short paragraphs, Markdown, optional Wikipedia link.
- **Wikipedia links:** use the real article title in the URL (check in browser or run `python3 tools/verify_wikipedia_links.py`). PL and EN titles often differ; there may be no PL article — then link to the closest related PL page or the EN article.
- **Locales:** always create **both** `pl-PL` and `en-US` with the same `id`, `month`, `day`, `sequence_index`, `category`.

## Scaffolding & manifest

```bash
# Create 366×2×2 templates + fill window from 29 May (edit FILL_START in script)
python3 tools/scaffold_year_content.py

# Build manifest (only published facts with non-empty title)
python3 tools/build_manifest.py
cp docs/facts.json app/src/main/assets/seed_facts.json
```

## Publishing

1. Set `published: true` and fill title/teaser/body for facts ready to go live.
2. Push — GitHub Action runs `build_manifest.py` and deploys `docs/facts.json`.
3. The app downloads the **full manifest** and uses `manifest_version` to skip redundant updates.
