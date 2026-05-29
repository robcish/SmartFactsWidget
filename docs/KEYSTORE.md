# Upload keystore (Google Play)

The release AAB must be signed with your **upload key**. Google Play App Signing can hold the app signing key; you keep the upload key locally.

> **Only need SHA-256?** You do not need this file. Use [CERTIFICATE_SHA256.md](CERTIFICATE_SHA256.md) — **Method 1A** (`apksigner verify --print-certs`) on a signed APK, or copy the fingerprint from Play Console after your first upload.

## 1. Create the keystore (one time)

From the project root, create a `release/` folder and run:

```bash
mkdir -p release
keytool -genkeypair -v \
  -keystore release/smart-facts-upload.jks \
  -alias upload \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storetype JKS
```

You will be prompted for:

| Prompt | Suggestion |
|--------|------------|
| Keystore password | Strong password — store in a password manager |
| Key password | Same as keystore password (press Enter when asked to reuse) |
| Name / org | Your name or “Robert Rozanski” |
| Country code | e.g. `PL` |

**Back up** `release/smart-facts-upload.jks` and the passwords somewhere safe (encrypted backup, password manager). If you lose them, you cannot upload updates for the same app id without going through Google’s key reset process.

## 2. Configure Gradle

```bash
cp keystore.properties.example keystore.properties
```

Edit `keystore.properties`:

```properties
storeFile=release/smart-facts-upload.jks
storePassword=your_store_password
keyAlias=upload
keyPassword=your_key_password
```

`keystore.properties` and `*.jks` are gitignored.

## 3. Build a signed App Bundle

```bash
./gradlew bundleRelease
```

Output:

`app/build/outputs/bundle/release/app-release.aab`

Upload this file in [Google Play Console](https://play.google.com/console) → your app → **Release** → **Production** (or internal testing first).

## 4. Play App Signing

On first upload, Google will ask you to opt in to **Play App Signing**. Recommended: let Google manage the app signing key; you only use the upload key above.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `keystore.properties` missing | Release builds are unsigned until you create the file; signing block is skipped. |
| Wrong password | Check `storePassword` / `keyPassword` in `keystore.properties`. |
| `keytool` not found | Use JDK 17+ (`java -version`); Android Studio bundles keytool in its JBR. |

See also [docs/RELEASE.md](RELEASE.md) for the full Play checklist.
