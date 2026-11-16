#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export CLANG_MODULE_CACHE_PATH="${TMPDIR:-/tmp}/workflow-clang-cache"
/usr/bin/xcrun swiftc "$ROOT/sketchybar/plugins/audio_devices.swift" -o "$ROOT/sketchybar/plugins/audio_devices" -framework CoreAudio
/usr/bin/xcrun swiftc "$ROOT/sketchybar/plugins/symbol_icons.swift" -o "$ROOT/sketchybar/plugins/symbol_icons" -framework AppKit
source "$ROOT/sketchybar/colors.sh"
"$ROOT/sketchybar/plugins/symbol_icons" "$ROOT/sketchybar/runtime/icons/active" "$ORANGE" "$ORANGE"
"$ROOT/sketchybar/plugins/symbol_icons" "$ROOT/sketchybar/runtime/icons/inactive" "$DIM" "$DIM"
