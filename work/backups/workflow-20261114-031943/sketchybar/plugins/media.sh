#!/bin/bash
# Prefer whichever supported player is playing; retain paused tracks for resuming.
APP=""; PAUSED=""
for candidate in Spotify Music; do
  /usr/bin/pgrep -x "$candidate" >/dev/null || continue
  state="$(/usr/bin/osascript -e "tell application \"$candidate\" to player state as string" 2>/dev/null)"
  if [ "$state" = playing ]; then APP="$candidate"; break; fi
  [ "$state" = paused ] && [ -z "$PAUSED" ] && PAUSED="$candidate"
done
[ -z "$APP" ] && APP="$PAUSED"
if [ -z "$APP" ]; then
  sketchybar --set "${NAME:-media}" drawing=off
  exit 0
fi
track="$(/usr/bin/osascript -e "tell application \"$APP\" to (name of current track) & \" · \" & (artist of current track)" 2>/dev/null)"
[ -z "$track" ] && track="$APP"
RUNTIME="$HOME/.config/sketchybar/runtime"
mkdir -p "$RUNTIME"
printf '%s\n' "$APP" > "$RUNTIME/media-player"
case "$APP" in Spotify) bundle=com.spotify.client ;; Music) bundle=com.apple.Music ;; esac
sketchybar --set "${NAME:-media}" drawing=on label="$track" icon="" icon.width=20 \
  icon.background.image="app.$bundle" icon.background.image.drawing=on icon.background.image.scale=0.5
