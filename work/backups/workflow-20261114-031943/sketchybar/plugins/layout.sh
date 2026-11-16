#!/usr/bin/env sh

# Live layout indicator for KiwiDesk
MODE=$(kiwidesk get_state 2>/dev/null | grep -o '"mode":"[^"]*' | head -n1 | cut -d'"' -f4)

case "$MODE" in
  "monocle") ICON="􀢊"; LABEL="Monocle" ;;
  "bsp") ICON="􀏚"; LABEL="BSP" ;;
  "scrolling") ICON="􀢤"; LABEL="Scroll" ;;
  "stack") ICON="􀏞"; LABEL="Stack" ;;
  "grid") ICON="􀏟"; LABEL="Grid" ;;
  "floating") ICON="􀏠"; LABEL="Floating" ;;
  "track") ICON="􀏝"; LABEL="Track" ;;
  *) ICON="􀏚"; LABEL="Tiling" ;;
esac

sketchybar --set "$NAME" icon="$ICON" label="$LABEL"
