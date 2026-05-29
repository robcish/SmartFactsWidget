#!/usr/bin/env bash
# Install and launch Smart Facts on a connected device/emulator (no Android Studio Run needed).
set -euo pipefail
cd "$(dirname "$0")"
./gradlew installDebug
adb shell am start -n com.robcish.smartfactswidget/.MainActivity
