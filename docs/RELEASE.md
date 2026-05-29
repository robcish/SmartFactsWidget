# Release checklist (Google Play)

## Before upload

- [ ] Full year of facts published (`content/`, manifest on GitHub Pages)
- [ ] Signed AAB ready — [KEYSTORE.md](KEYSTORE.md) or Android Studio “Generate Signed Bundle”
- [ ] SHA-256 only? — [CERTIFICATE_SHA256.md](CERTIFICATE_SHA256.md) (Method 1A, no keystore file needed)
- [ ] `./gradlew bundleRelease` succeeds
- [ ] Smoke test on a real device (widget, offline, PL/EN, sync)
- [ ] Privacy policy live: https://robcish.github.io/SmartFactsWidget/privacy.html
- [ ] Store texts ready: [PLAY_STORE_LISTING.md](PLAY_STORE_LISTING.md)

## Play Console (manual)

- [ ] Create app → package `com.robcish.smartfactswidget`
- [ ] Upload AAB (internal testing track first is recommended)
- [ ] Store listing (EN + PL if targeting Poland)
- [ ] Privacy policy URL (link above)
- [ ] Data safety form: no account, no data sold, Internet for content sync
- [ ] Content rating questionnaire (IARC)
- [ ] Screenshots + 512×512 icon + 1024×500 feature graphic

## Version numbers

Update in `app/build.gradle.kts` before each Play upload:

- `versionCode` — integer, must increase every upload
- `versionName` — user-visible string (e.g. `1.0.0`)

## Content updates without a new APK

Push changes to `content/` on `main`. CI deploys `docs/facts.json`. Devices sync via WorkManager.

A new APK is needed for app code changes or refreshing `app/src/main/assets/seed_facts.json`.

## Obfuscation

R8/minify is **disabled** (`isMinifyEnabled = false`). Not required for Play.
