#!/bin/bash
APP="$(cat "$HOME/.config/sketchybar/runtime/media-player" 2>/dev/null)"
case "$APP" in Spotify|Music) ;; *) exit 0 ;; esac
/usr/bin/pgrep -x "$APP" >/dev/null || exit 0
ACTION=playpause
[ "$BUTTON" = right ] && ACTION='next track'
/usr/bin/osascript -e "tell application \"$APP\" to $ACTION" >/dev/null 2>&1
NAME=media "$HOME/.config/sketchybar/plugins/media.sh"
