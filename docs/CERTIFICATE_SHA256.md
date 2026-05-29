# SHA-256 certificate fingerprint

The **SHA-256 fingerprint** identifies your app’s signing certificate (Firebase, Google APIs, App Links, Play Console, etc.).

It is **not** the same as creating a release keystore:

| Goal | What you need |
|------|----------------|
| **Publish to Google Play** | A signed **AAB** (upload key or Play-managed signing) — see [KEYSTORE.md](KEYSTORE.md) |
| **Learn the SHA-256** of an already signed APK | **Method 1A** below — no keystore file or password required |

---

## Method 1A — `apksigner` on a signed APK (recommended)

Use this when you have a signed APK (debug or release) and only need the fingerprint.

### Step 1 — Build an APK

```bash
# Debug (uses ~/.android/debug.keystore automatically)
./gradlew assembleDebug

# Release (only if you already configured keystore.properties)
./gradlew assembleRelease
```

### Step 2 — Find `apksigner`

Usually under the Android SDK build-tools, for example:

```text
~/Library/Android/sdk/build-tools/35.0.0/apksigner
```

List installed versions:

```bash
ls "$ANDROID_HOME/build-tools"
# or on macOS with default SDK path:
ls ~/Library/Android/sdk/build-tools
```

### Step 3 — Print certificates

```bash
apksigner verify --print-certs app/build/outputs/apk/debug/app-debug.apk
```

For a release APK:

```bash
apksigner verify --print-certs app/build/outputs/apk/release/app-release.apk
```

### Step 4 — Copy SHA-256

In the output, find:

```text
Signer #1 certificate SHA-256 digest:
a32a43cd459f7ce6b82c552f5d876989d53e6af1c0b2d35fb677b51a1dc4f0e5
```

That hex string is the **SHA-256 fingerprint** (Play Console and some Google consoles accept it with or without `:` separators).

### Helper script (this repo)

```bash
./tools/print_apk_sha256.sh
# or
./tools/print_apk_sha256.sh path/to/your.apk
```

---

## Method 1B — `keytool` on APK

```bash
keytool -printcert -jarfile app/build/outputs/apk/debug/app-debug.apk
```

Look under **Certificate fingerprints** → **SHA-256**.

---

## Method 2 — `keytool` on keystore (only if you have the `.jks`)

If you manage the upload keystore and know its password:

```bash
keytool -list -v -keystore release/smart-facts-upload.jks -alias upload
```

See [KEYSTORE.md](KEYSTORE.md).

---

## Which certificate matters?

| Situation | Certificate to use |
|-----------|-------------------|
| Local dev, Firebase debug | SHA-256 from **debug** APK (Method 1A on `app-debug.apk`) |
| App on Play with **Play App Signing** | **App signing key** SHA-256 from Play Console → **Setup → App signing** (after first upload) |
| You sign releases locally | SHA-256 from **release** APK (Method 1A) or Method 2 on your `.jks` |

Debug and release fingerprints **differ**. Use the one that matches how users install the app.

---

## Play Store without creating `release/*.jks` first?

You still must upload a **signed** AAB. Common paths:

1. **Android Studio** → Build → Generate Signed App Bundle → wizard can create a new keystore once (you may never open `keytool` yourself).
2. **Play App Signing** — after the first upload, Google shows the **app signing** SHA-256 in the console; you do not need Method 1A for that copy-paste.

Method 1A is for when you already have an APK on disk and want the fingerprint without opening the keystore file.
