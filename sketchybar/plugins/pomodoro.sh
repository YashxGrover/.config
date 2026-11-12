#!/usr/bin/env sh

# Pomodoro Focus Timer (25min countdown with click start/pause/reset)
STATE_FILE="/tmp/sketchybar_pomodoro.txt"

if [ "$SENDER" = "mouse.clicked" ]; then
  if [ ! -f "$STATE_FILE" ]; then
    echo "running:1500" > "$STATE_FILE"
  else
    STATUS=$(cut -d: -f1 "$STATE_FILE")
    REMAINING=$(cut -d: -f2 "$STATE_FILE")
    if [ "$STATUS" = "running" ]; then
      echo "paused:$REMAINING" > "$STATE_FILE"
    elif [ "$STATUS" = "paused" ]; then
      echo "running:$REMAINING" > "$STATE_FILE"
    else
      echo "running:1500" > "$STATE_FILE"
    fi
  fi
fi

if [ -f "$STATE_FILE" ]; then
  STATUS=$(cut -d: -f1 "$STATE_FILE")
  REMAINING=$(cut -d: -f2 "$STATE_FILE")

  if [ "$STATUS" = "running" ]; then
    REMAINING=$((REMAINING - 1))
    if [ "$REMAINING" -le 0 ]; then
      echo "stopped:0" > "$STATE_FILE"
      afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &
      sketchybar --set "$NAME" icon="􀐫" icon.color=0xffff5f56 label="Done!"
      exit 0
    fi
    echo "running:$REMAINING" > "$STATE_FILE"
    MIN=$((REMAINING / 60))
    SEC=$((REMAINING % 60))
    LABEL=$(printf "%02d:%02d" "$MIN" "$SEC")
    sketchybar --set "$NAME" icon="􀐫" icon.color=0xff30d158 label="$LABEL"
  elif [ "$STATUS" = "paused" ]; then
    MIN=$((REMAINING / 60))
    SEC=$((REMAINING % 60))
    LABEL=$(printf "%02d:%02d" "$MIN" "$SEC")
    sketchybar --set "$NAME" icon="􀊆" icon.color=0xffffbd2e label="$LABEL (paused)"
  else
    sketchybar --set "$NAME" icon="􀐫" icon.color=0xff888888 label="25:00"
  fi
else
  sketchybar --set "$NAME" icon="􀐫" icon.color=0xff888888 label="25:00"
fi
