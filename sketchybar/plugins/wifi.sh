#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
if [ -n "$(ipconfig getifaddr en0 2>/dev/null)" ]; then
  sketchybar --set "$NAME" label="Online" icon.color=$PURPLE
else
  sketchybar --set "$NAME" label="Offline" icon.color=$RED
fi
