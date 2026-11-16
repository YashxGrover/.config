#!/bin/bash
[ "$SENDER" = "mouse.exited.global" ] && { sketchybar --set "$NAME" popup.drawing=off; exit 0; }
sketchybar --set "$NAME" label="$(date '+%a %d %b · %H:%M')"
