#!/bin/bash
source "$HOME/.config/sketchybar/icons.sh"
[ "$SENDER" = "mouse.exited.global" ] && { sketchybar --set "$NAME" popup.drawing=off; exit 0; }
S="$(osascript -e 'set v to get volume settings
return (output volume of v as string) & "," & (output muted of v as string)')"
VOL="${S%%,*}"; MUTED="${S##*,}"
if [ "$MUTED" = "true" ] || [ "$VOL" = "0" ]; then
  sketchybar --set "$NAME" icon="$ICON_VOL_OFF" label="Muted"
else
  if [ "$VOL" -gt 50 ]; then ICON=$ICON_VOL_UP; else ICON=$ICON_VOL_DOWN; fi
  sketchybar --set "$NAME" icon="$ICON" label="${VOL}%"
fi
sketchybar --set volume.slider slider.percentage="$VOL"
