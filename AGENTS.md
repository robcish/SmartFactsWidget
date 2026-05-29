# Guide for AI agents (Cursor, Copilot, etc.)

**Start here** when adding or editing facts, content, or the manifest.

## Read first (in order)

1. **[content/FACT_GENERATION_RULES.md](content/FACT_GENERATION_RULES.md)** — calendar model, frontmatter, categories, quality, tools, examples, external sources.
2. **Published examples** — `content/en-US/05-29-0-animals.md` and `content/pl-PL/05-29-0-animals.md` (same `id`, different locale).
3. **[INSTRUCTIONS_FOR_AI_AGENT.md](INSTRUCTIONS_FOR_AI_AGENT.md)** — app architecture (Kotlin, Glance, Room). **Ignore** any `release_epoch_ms` mentions there; the app uses **calendar v2** (`month`, `day`, `sequence_index`).

## Typical task: add facts for a date range

Example user request:

> Add published facts for 2026-06-06 through 2026-06-15 (both pl-PL and en-US).

**Checklist:**

1. List template files: `content/en-US/06-06-*.md` … or run `grep -l "published: true" content/en-US/06-*.md`.
2. Respect **category cooldown** (same category not within 2 calendar days) — see rules file.
3. Write **both locales** per fact (`id`, `month`, `day`, `sequence_index`, `category` must match).
4. Set `published: true`, non-empty `title`, `teaser`, body; `version: 1`.
5. Run:
   ```bash
   python3 tools/verify_category_cooldown.py
   python3 tools/verify_fact_uniqueness.py --published-only
   python3 tools/build_manifest.py
   python3 tools/verify_wikipedia_links.py
   cp docs/facts.json app/src/main/assets/seed_facts.json
   ```
6. Commit `content/`, `docs/facts.json`, and `app/src/main/assets/seed_facts.json` if seed is updated in-repo.

**Users do not need a new APK** for facts-only changes after push to `main` (GitHub Pages deploys `docs/facts.json`). A new APK is only needed for app code changes or refreshing the bundled offline seed.

## Do not

- Copy long text verbatim from CC BY-SA sources without rewriting and checking license/attribution needs.
- Publish facts with empty `title` (omitted from manifest).
- Use a category not listed in `CategoryIcons.kt`.
- Change unrelated app code when the task is content-only.

## Tools reference

| Script | Purpose |
|--------|---------|
| `tools/build_manifest.py` | Build `docs/facts.json` |
| `tools/verify_category_cooldown.py` | 2-day category cooldown check (exit 1 on violation) |
| `tools/verify_fact_uniqueness.py` | Duplicate title/teaser/body detection |
| `tools/verify_wikipedia_links.py` | HTTP-check Wikipedia URLs in published facts |
| `tools/plan_categories.py` | Generate `tools/category_plan.json` (3 cats/day) |
| `tools/add_third_slot_templates.py` | Create `MM-DD-2-{category}.md` templates |
| `tools/populate_year_content.py` | Fill facts from science-facts + Wikipedia (batch by `--start`/`--end`) |
| `tools/rename_fact_category.py` | Rename fact when category slug changes |
| `tools/content_summary.py` | Category balance, coverage, cooldown — run for a status report |
| `tools/fix_pl_translations.py` | Rewrite pl-PL from en-US (translate + PL Wikipedia links) |
| `tools/fix_pl_missing_wiki_links.py` | Second pass: add PL wiki links where missing |
| `tools/strip_pl_category_fallback_links.py` | Remove generic category PL Wikipedia links |
| `tools/scaffold_year_content.py` | Generate year of template `.md` files (destructive — avoid on existing `content/`) |
| `tools/fill_past_week_may22_28.py` | Example batch-fill script (reference only) |
| `tools/generate_category_drawables.py` | Regenerate `ic_cat_*.xml` from Material Symbols |

## Valid categories

`science`, `math`, `biology`, `animals`, `technology`, `history`, `geography`, `astronomy`, `language`, `psychology`, `philosophy`, `society`, `law`, `finance`, `culture`, `mythology`, `myth-busting`, `general`, `reflection`, `sport`, `food`, `environment`

Defined in `app/src/main/java/com/robcish/smartfactswidget/ui/category/CategoryIcons.kt`.
