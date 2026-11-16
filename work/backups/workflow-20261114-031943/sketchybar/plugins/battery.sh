#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
source "$HOME/.config/sketchybar/icons.sh"
[ "$SENDER" = "mouse.exited.global" ] && { sketchybar --set "$NAME" popup.drawing=off; exit 0; }
INFO="$(pmset -g batt)"
PCT="$(echo "$INFO" | grep -Eo '[0-9]+%' | head -1 | tr -d '%')"
[ -z "$PCT" ] && exit 0
if   [ "$PCT" -gt 75 ]; then ICON=$ICON_BAT_100
elif [ "$PCT" -gt 50 ]; then ICON=$ICON_BAT_75
elif [ "$PCT" -gt 25 ]; then ICON=$ICON_BAT_50
elif [ "$PCT" -gt 10 ]; then ICON=$ICON_BAT_25
else ICON=$ICON_BAT_0; fi
COLOR=$GREEN
[ "$PCT" -le 40 ] && COLOR=$YELLOW
[ "$PCT" -le 20 ] && COLOR=$RED
echo "$INFO" | grep -q 'AC Power' && ICON="$ICON_BOLT"
sketchybar --set "$NAME" icon="$ICON" icon.color=$COLOR label.color=$COLOR label="${PCT}%"
