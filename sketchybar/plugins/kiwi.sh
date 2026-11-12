#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
STATE=/tmp/kiwi_state
if [ "$SENDER" = "kiwi_update" ]; then
  echo "$DESKTOP|$ACTIVE|$COUNTS|$MODE" > $STATE
elif [ -f $STATE ]; then
  IFS='|' read -r DESKTOP ACTIVE COUNTS MODE < $STATE
else exit 0; fi

case "$NAME" in
  kiwi.desk) sketchybar --set $NAME label="Desk $DESKTOP" ;;
  kiwi.mode) sketchybar --set $NAME label="$MODE" ;;
  kiwi.space*)
    IDX="${NAME##*.space}"
    CNT="$(echo "$COUNTS" | cut -d, -f"$IDX")"
    if [ "$ACTIVE" = "$IDX" ]; then
      sketchybar --set $NAME label.color=$BG background.color=$ORANGE
    elif [ "${CNT:-0}" -gt 0 ]; then
      sketchybar --set $NAME label.color=$FG background.color=$PILL
    else
      sketchybar --set $NAME label.color=$DIM background.color=$PILL
    fi ;;
esac
