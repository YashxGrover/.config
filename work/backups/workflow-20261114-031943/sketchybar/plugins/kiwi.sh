#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
STATE=/tmp/kiwi_state
if [ "$SENDER" = "kiwi_update" ]; then
  echo "$DESKTOP|$ACTIVE|$COUNTS|$MODE" > $STATE
elif [ -f $STATE ]; then
  IFS='|' read -r DESKTOP ACTIVE COUNTS MODE < $STATE
else exit 0; fi

case "$NAME" in
  kiwi.desk) sketchybar --set $NAME label="Desktop $DESKTOP" ;;
  kiwi.current) sketchybar --set "$NAME" label="Space $ACTIVE" ;;
  kiwi.mode) sketchybar --set $NAME label="$MODE" ;;
  kiwi.space*)
    IDX="${NAME##*.space}"
    CNT="$(echo "$COUNTS" | cut -d, -f"$IDX")"
    if [ -z "$CNT" ]; then
      sketchybar --set "$NAME" drawing=off
      exit 0
    fi
    sketchybar --set "$NAME" drawing=on
    if [ "$ACTIVE" = "$IDX" ]; then
      sketchybar --set $NAME label.color=$ORANGE background.drawing=on background.color=$PILL background.corner_radius=3 background.border_width=0
    elif [ "${CNT:-0}" -gt 0 ]; then
      sketchybar --set $NAME label.color=$FG background.drawing=off
    else
      sketchybar --set $NAME label.color=$DIM background.drawing=off
    fi ;;
esac
