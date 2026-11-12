#!/usr/bin/env sh

# Listens to KiwiDesk real-time JSON event stream and updates SketchyBar
kiwidesk subscribe space_change layout_change 2>/dev/null | while read -r line; do
  # Extract space and mode
  SPACE=$(echo "$line" | sed -n 's/.*"space"[ :]*"\([^"]*\)".*/\1/p')
  MODE=$(echo "$line" | sed -n 's/.*"mode"[ :]*"\([^"]*\)".*/\1/p')

  # Update active space pill
  if [ -n "$SPACE" ]; then
    for i in 1 2 3 4 5 6 7; do
      if [ "$i" = "$SPACE" ]; then
        sketchybar --set "space.$i" background.drawing=on \
                                    background.color=0x3330d158 \
                                    background.border_color=0x8830d158 \
                                    icon.color=0xff30d158 \
                                    label.color=0xffffffff
      else
        sketchybar --set "space.$i" background.drawing=on \
                                    background.color=0x15ffffff \
                                    background.border_color=0x15ffffff \
                                    icon.color=0x99ffffff \
                                    label.color=0x77ffffff
      fi
    done
  fi

  # Update layout badge if mode changed
  if [ -n "$MODE" ]; then
    case "$MODE" in
      "monocle") ICON="􀢊"; LABEL="Monocle" ;;
      "bsp") ICON="􀏚"; LABEL="BSP" ;;
      "scrolling") ICON="􀢤"; LABEL="Scroll" ;;
      "stack") ICON="􀏞"; LABEL="Stack" ;;
      "grid") ICON="􀏟"; LABEL="Grid" ;;
      "floating") ICON="􀏠"; LABEL="Floating" ;;
      "track") ICON="􀏝"; LABEL="Track" ;;
      *) ICON="􀏚"; LABEL="$MODE" ;;
    esac
    sketchybar --set "layout" icon="$ICON" label="$LABEL"
  fi
done
