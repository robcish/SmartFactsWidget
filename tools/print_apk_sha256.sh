#!/usr/bin/env bash
# Print SHA-256 certificate digest(s) from a signed APK (apksigner method 1A).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APK="${1:-$ROOT/app/build/outputs/apk/debug/app-debug.apk}"

if [[ ! -f "$APK" ]]; then
  echo "APK not found: $APK" >&2
  echo "Build one first, e.g.: ./gradlew assembleDebug" >&2
  exit 1
fi

find_apksigner() {
  if [[ -n "${ANDROID_HOME:-}" && -d "$ANDROID_HOME/build-tools" ]]; then
    local latest
    latest="$(ls -1 "$ANDROID_HOME/build-tools" 2>/dev/null | sort -V | tail -1)"
    if [[ -n "$latest" && -x "$ANDROID_HOME/build-tools/$latest/apksigner" ]]; then
      echo "$ANDROID_HOME/build-tools/$latest/apksigner"
      return 0
    fi
  fi
  local mac_sdk="$HOME/Library/Android/sdk/build-tools"
  if [[ -d "$mac_sdk" ]]; then
    local latest
    latest="$(ls -1 "$mac_sdk" 2>/dev/null | sort -V | tail -1)"
    if [[ -n "$latest" && -x "$mac_sdk/$latest/apksigner" ]]; then
      echo "$mac_sdk/$latest/apksigner"
      return 0
    fi
  fi
  if command -v apksigner >/dev/null 2>&1; then
    command -v apksigner
    return 0
  fi
  return 1
}

APKSIGNER="$(find_apksigner)" || {
  echo "apksigner not found. Set ANDROID_HOME or install Android SDK build-tools." >&2
  exit 1
}

echo "Using: $APKSIGNER"
echo "APK:    $APK"
echo ""
"$APKSIGNER" verify --print-certs "$APK"
