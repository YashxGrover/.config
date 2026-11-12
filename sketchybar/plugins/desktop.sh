#!/usr/bin/env sh

# Extract clean integer from $INFO (e.g. '{"display-1": 3}' -> '3')
if [ -n "$INFO" ]; then
  DESK_NUM=$(echo "$INFO" | grep -o '[0-9]\+' | head -n1)
fi

if [ -z "$DESK_NUM" ]; then
  DESK_NUM=$(sketchybar --query default_menu 2>/dev/null | grep -o '"space":[0-9]*' | head -n1 | cut -d: -f2)
fi

if [ -z "$DESK_NUM" ]; then
  DESK_NUM="1"
fi

sketchybar --set "$NAME" label="Desktop $DESK_NUM"
