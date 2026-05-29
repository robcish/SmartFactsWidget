# Smart Facts Widget

A calm, minimalist Android app and widget that delivers short educational facts each day — directly to your home screen.

Built with **Jetpack Compose**, **Glance**, **Room**, and **WorkManager**.  
Content is managed in this repository (GitHub-as-CMS) — no separate backend to host.

> “No ads. No noise. Just knowledge.”

---

## Features

- Daily educational facts across multiple topics (PL + EN)
- Home screen widget (Jetpack Glance) with tap-to-read
- Offline-ready — facts cached locally in Room
- Auto-sync via WorkManager (daily + on app start)
- Future facts stay hidden until their release date
- Ad-free, non-commercial portfolio project

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Jetpack Compose, Material 3 |
| Widget | Jetpack Glance |
| Background sync | WorkManager |
| Local cache | Room |
| Remote content | GitHub Pages (static JSON manifest) |
| HTTP client | Ktor |
| DI | Hilt |
| Language | Kotlin |
| Min SDK | 23 |

---

## Architecture

Content lives in this repo as Markdown files. A GitHub Action builds a JSON manifest and deploys it to GitHub Pages. The Android app pulls the manifest, caches facts in Room, and serves both the widget and in-app UI from the same repository layer.

```
content/pl-PL/*.md  +  content/en-US/*.md
        │
        ▼  git push
.github/workflows/publish.yml
        │
        ▼  tools/build_manifest.py
docs/facts.json
        │
        ▼  GitHub Pages
Android app  →  Ktor GET  →  Room  →  Glance widget + Compose UI
```

---

## Content Format

Facts are stored as Markdown with YAML frontmatter:

```markdown
---
id: 2025-05-22-science-sharks
locale: pl-PL
category: science
title: Sharks are older than trees
teaser: Did you know sharks existed before trees?
release_epoch_ms: 1747897200000
published: true
---
Sharks have been around for over 400 million years...
```

Directory layout:

```
content/
  pl-PL/
    2025-05-22-science-sharks.md
  en-US/
    2025-05-22-science-sharks.md
```

To publish a new fact: add or edit a `.md` file, commit, and push to `main`. CI rebuilds `docs/facts.json` and deploys to GitHub Pages. Devices pick up changes on the next sync.

---

## Build & Setup

### Prerequisites

- Android Studio (latest stable) with SDK 35
- JDK 17
- GitHub Pages enabled on this repo (Settings → Pages → GitHub Actions)

### Run the app

1. Clone the repository:
   ```bash
   git clone git@github.com:robcish/SmartFactsWidget.git
   cd SmartFactsWidget
   ```
2. Open the project in Android Studio.
3. Sync Gradle and run on an emulator or device (`app` configuration).
4. Add the **Smart Facts** widget to your home screen.

### Build from command line

```bash
./gradlew assembleDebug
```

---

## Publishing Workflow (for contributors / AI agents)

1. Create a Markdown file in `content/pl-PL/` or `content/en-US/`.
2. Set `release_epoch_ms` to the fact's go-live timestamp (milliseconds since epoch).
3. Set `published: true` when ready.
4. Push to `main` — GitHub Action runs `tools/build_manifest.py` and updates `docs/facts.json`.
5. GitHub Pages serves the updated manifest; apps sync on next WorkManager run.

---

## Project Status

**Early development / MVP in progress.**

Planned for v0.2: Browse history, Settings, About screen.

---

## License

MIT License — see [LICENSE](LICENSE).

© 2025 Robert Rozanski
