#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
FREE="$(memory_pressure | awk '/free percentage/ {gsub("%","",$5); print $5}')"
[ -z "$FREE" ] && exit 0
USED=$((100 - FREE))
COLOR=$FG
[ "$USED" -ge 75 ] && COLOR=$YELLOW
[ "$USED" -ge 90 ] && COLOR=$RED
sketchybar --set "$NAME" label="${USED}%" label.color=$COLOR
