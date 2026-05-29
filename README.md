# Smart Facts Widget

A calm, minimalist Android app and widget that delivers short educational facts each day — directly to your home screen.

Built with **Jetpack Compose**, **Glance**, **Room**, and **WorkManager**.  
Content is managed in this repository (GitHub-as-CMS) — no separate backend to host.

> “No ads. No noise. Just knowledge.”

---

## Features

- **Three facts per day** (morning, midday, afternoon) in **Polish and English**
- Home screen **widget** (Jetpack Glance) with tap-to-read
- In-app reader with a **7-day timeline**
- **Offline-ready** — full-year seed bundled; Room cache for sync
- Auto-sync via WorkManager (daily + on app start)
- Ad-free, no account, no analytics SDKs

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Jetpack Compose, Material 3 |
| Widget | Jetpack Glance |
| Background sync | WorkManager |
| Local cache | Room |
| Remote content | GitHub Pages (`facts.json`) |
| HTTP client | Ktor |
| DI | Hilt |
| Language | Kotlin |
| Min SDK | 23 · Target SDK | 35 |

---

## Architecture

Facts live as Markdown under `content/pl-PL/` and `content/en-US/`. CI builds `docs/facts.json` and deploys the `docs/` folder to GitHub Pages.

```
content/{locale}/*.md
        │
        ▼  git push (main)
.github/workflows/publish.yml
        │
        ▼
docs/facts.json  +  docs/privacy.html
        │
        ▼  GitHub Pages
Android app  →  HTTPS  →  Room  →  widget + Compose UI
```

Calendar model: facts repeat every year on **month + day** with `sequence_index` 0, 1, 2. See [content/FACT_GENERATION_RULES.md](content/FACT_GENERATION_RULES.md).

---

## Build & run

### Prerequisites

- Android Studio (latest stable) with SDK 35
- JDK 17

### Run locally

```bash
git clone git@github.com:robcish/SmartFactsWidget.git
cd SmartFactsWidget
```

Open in Android Studio → Run `app`. Add the **Smart Facts** widget from the home screen (long-press → Widgets).

### Command line

```bash
./gradlew assembleDebug          # debug APK
./gradlew bundleRelease          # release AAB (signed if keystore.properties exists)
```

---

## Release (Google Play)

| Doc | Purpose |
|-----|---------|
| [docs/RELEASE.md](docs/RELEASE.md) | Checklist before upload |
| [docs/KEYSTORE.md](docs/KEYSTORE.md) | Sign release AAB (upload key) |
| [docs/CERTIFICATE_SHA256.md](docs/CERTIFICATE_SHA256.md) | SHA-256 from APK via `apksigner` (Method 1A) |
| [docs/PLAY_STORE_LISTING.md](docs/PLAY_STORE_LISTING.md) | Store title, descriptions (EN + PL) |
| [docs/privacy.html](docs/privacy.html) | Privacy policy (Pages URL below) |

**Privacy policy URL:** https://robcish.github.io/SmartFactsWidget/privacy.html

1. Copy `keystore.properties.example` → `keystore.properties` and create the JKS ([KEYSTORE.md](docs/KEYSTORE.md)).
2. Bump `versionCode` / `versionName` in `app/build.gradle.kts`.
3. `./gradlew bundleRelease` → upload `app/build/outputs/bundle/release/app-release.aab`.

Obfuscation (R8) is **not** required; it stays disabled.

---

## Content workflow

For agents and contributors, start at [AGENTS.md](AGENTS.md).

```bash
python3 tools/verify_category_cooldown.py
python3 tools/verify_fact_uniqueness.py --published-only
python3 tools/build_manifest.py
cp docs/facts.json app/src/main/assets/seed_facts.json   # when refreshing offline seed
```

Push to `main` — devices pick up new facts on the next sync. A new APK is only needed for app code changes or an updated bundled seed.

---

## Project status

**v1.0.0** — MVP ready for Play Store (widget, sync, full-year content).  
Planned later: browse history screen, settings, dedicated about screen.

---

## License

MIT License — see [LICENSE](LICENSE).

© 2025–2026 Robert Różański
