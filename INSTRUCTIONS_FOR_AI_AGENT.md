# Smart Facts Widget — AI Agent Development Instructions

This document defines the concept, architecture, and implementation plan for the **Smart Facts Widget** project.  
It is intended as a guide for an AI coding assistant (Cursor, Copilot, Claude, etc.) responsible for generating, maintaining, or extending the project.

---

## 🎯 Project Goal

Build a minimalist Android app and **home screen widget** that shows a new **educational fact every day**.  
The app is non-commercial, ad-free, and serves as a **portfolio project** demonstrating modern Jetpack technologies and clean architecture.

> “No ads. No noise. Just knowledge.”

---

## 🧩 Key Features

- 🧠 Daily educational fact displayed in a home-screen widget  
- 💬 Tap the widget → open full explanation screen  
- 🔄 Auto-rotation every few hours via WorkManager  
- ☁️ Prefetch content from GitHub Pages manifest (built from `/content`)  
- 📴 Works offline using Room cache  
- 🕒 Future facts remain locked until release date  
- 🎨 Minimalist UI (Material 3, Compose)  
- 🧰 Widget-first architecture using Jetpack Glance  

---

## 🧱 Tech Stack

| Layer | Technology |
|--------|-------------|
| UI | Jetpack Compose (Material 3) |
| Widget | Jetpack Glance |
| Background | WorkManager |
| Local DB | Room |
| Remote | GitHub Pages (static JSON manifest) |
| DI | Hilt |
| Language | Kotlin |
| License | MIT |
| Min SDK | 23+ |

---

## 🧠 Topics for the Facts

Each fact is short (1–2 paragraphs), timeless, and written in an accessible tone.  
Main knowledge areas:

- Science & Technology  
- Psychology & Mind  
- Language & Etymology  
- History & Culture  
- Mythology & Symbols  
- Everyday Law & Finance  
- Society & Politics  
- Philosophy & Reflection  
- Myths vs. Truths  
- General “Did you know?” insights  

---

## 🗂️ Content & Manifest Model

Facts live as Markdown files under `content/{locale}/`.  
CI builds `docs/facts.json` (GitHub Pages) via `tools/build_manifest.py`.

```json
{
  "version": 1,
  "generated_at": "2026-05-29T12:00:00Z",
  "facts": [
    {
      "id": "2026-05-29-science-00",
      "locale": "pl-PL",
      "category": "science",
      "title": "Sharks are older than trees",
      "teaser": "Did you know sharks existed before trees?",
      "body_md": "Sharks have roamed the oceans for more than **400 million years**.",
      "release_epoch_ms": 1748506800000,
      "published": true,
      "version": 1
    }
  ]
}
```

### Release rules

- CI excludes `published: false` and future `release_epoch_ms` from the public manifest.
- The Android app applies the same filter when caching to Room.

---

## 💾 Room Entity

```kotlin
@Entity(tableName = "facts")
data class FactEntity(
    @PrimaryKey val id: String,
    val title: String,
    val teaser: String,
    val bodyMd: String,
    val category: String,
    val releaseEpochMs: Long,
    val published: Boolean,
    val version: Int,
    val updatedAt: Long,
    val isFavorite: Boolean = false,
)
```

---

## 🔄 Data Flow

1. On app startup → sync manifest from GitHub Pages.  
2. Store fetched items in Room.  
3. Every morning (07:00) → WorkManager syncs new data.  
4. After sync → Glance widget `updateAll`.  
5. Widget only shows facts with `releaseEpochMs ≤ now`.  
6. App UI and widget share the same repository.  

---

## 🧰 Glance Widget

**Structure:**

```kotlin
class SmartFactsWidget : GlanceAppWidget() {
    @Composable
    override fun Content() {
        val fact = remember { "Did you know sharks existed before trees?" }
        Box(
            modifier = GlanceModifier
                .background(Color.White)
                .padding(12.dp)
        ) {
            Text(text = fact, style = TextStyle(fontSize = 16.sp))
        }
    }
}
```

**Receiver:**
```kotlin
class SmartFactsWidgetReceiver : GlanceAppWidgetReceiver() {
    override val glanceAppWidget: GlanceAppWidget = SmartFactsWidget()
}
```

**Widget Info XML:**
```xml
<appwidget-provider
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="180dp"
    android:minHeight="110dp"
    android:updatePeriodMillis="0"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen" />
```

---

## 🧩 Compose UI Screens

| Screen | Description |
|---------|-------------|
| **Home** | Displays today's fact(s) |
| **Detail** | Full content with Markdown rendering |
| **Browse** | Facts history (past 7–14 days) |
| **Settings** | Widget refresh rate, theme, font size |
| **About** | Info about author, license, and tech stack |

---

## 🎨 Branding

| Element | Value |
|----------|--------|
| Name | Smart Facts Widget |
| Tagline | “A calm, daily dose of knowledge.” |
| Accent color | `#FFD54F` (warm yellow) |
| Icon | Use **card**, **wave**, **sun/moon**, or **leaf** motif – avoid lightbulb/brain symbols |
| Typography | Inter / Manrope / Nunito |
| Motto | “No ads. No noise. Just knowledge.” |

---

## 📦 Repository

- **Name:** `SmartFactsWidget`  
- **Visibility:** Public  
- **License:** MIT  
- **Topics:** `android`, `jetpack-compose`, `glance`, `widget`, `room`, `github-pages`, `workmanager`, `portfolio`, `kotlin`

### README should include:
- Overview & purpose  
- Screenshots (app + widget)  
- Architecture diagram  
- Build & setup instructions  
- License section  
- Future roadmap  

---

## ⚙️ Publishing Pipeline

Facts are generated by AI and stored as Markdown files in `/content`.

```markdown
---
id: 2025-10-27-math-93x95
locale: pl-PL
category: math
title: Quick mental math: 93×95
teaser: Did you know you can calculate 93×95 in your head?
release_epoch_ms: 1761523200000
published: true
---
Tip for numbers near 100:
93×95 = (100−7)(100−5) = 10000−1200+35 = **8835**.
```

A GitHub Action (`.github/workflows/publish.yml`) runs `tools/build_manifest.py`  
which validates frontmatter and writes `docs/facts.json` for GitHub Pages.

**Agent workflow:** add/edit Markdown in `content/`, commit, push to `main`.

---

## 🧩 MVP Tasks for AI Agent

1. Android project (Compose + Hilt + Ktor + Room + Glance).  
2. Implement Room schema + repository + manifest sync.  
3. Build Glance widget for fact teaser.  
4. Add WorkManager for daily sync.  
5. Implement Compose UI (Home, Detail — Browse/Settings in v0.2).  
6. Add offline caching and date filters.  
7. CMS pipeline: `content/` + `build_manifest.py` + GitHub Action.  
8. Verify build with minSdk 23, targetSdk 35.  

---

## 🔮 Optional Future Features

- Favorites list  
- Weekly notification  
- Quiz mode  
- Donate / Tip jar (Google Play Billing)  
- Multi-language content (`facts_en`, `facts_pl`)  
- Alternative widget layouts (small, medium, dark)  

---

## 🧭 Summary

**Smart Facts Widget** is a calm, educational Android app that demonstrates how to combine  
Jetpack Compose, Glance, WorkManager, Room, and GitHub-as-CMS into a clean, offline-first product.  

> Minimalism meets curiosity.  
> Built for learning, not distraction.
