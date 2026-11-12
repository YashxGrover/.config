#!/bin/bash
APP=""
pgrep -x Spotify >/dev/null && APP="Spotify"
[ -z "$APP" ] && pgrep -x Music >/dev/null && APP="Music"
if [ -z "$APP" ]; then sketchybar --set "$NAME" drawing=off; exit 0; fi
STATE="$(osascript -e "tell application \"$APP\" to player state as string" 2>/dev/null)"
if [ "$STATE" = "playing" ]; then
  T="$(osascript -e "tell application \"$APP\" to (name of current track) & \" - \" & (artist of current track)" 2>/dev/null)"
  [ ${#T} -gt 32 ] && T="${T:0:31}…"
  sketchybar --set "$NAME" label="$T" drawing=on
else
  sketchybar --set "$NAME" drawing=off
fi
