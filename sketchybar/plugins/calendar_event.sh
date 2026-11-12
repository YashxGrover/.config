#!/bin/bash
ICAL=/opt/homebrew/bin/icalBuddy
[ -x "$ICAL" ] || ICAL=/usr/local/bin/icalBuddy
OUT="$("$ICAL" -n -nc -b "" -nrd -ea -iep "title,datetime" -tf "%H:%M" -li 1 eventsToday+1 2>/dev/null)"
if [ -z "$OUT" ]; then
  sketchybar --set "$NAME" label="No events"; exit 0
fi
TITLE="$(echo "$OUT" | sed -n '1p' | sed 's/^ *//')"
[ ${#TITLE} -gt 24 ] && TITLE="${TITLE:0:23}…"
START="$(echo "$OUT" | sed -n '2,$p' | grep -oE '[0-9]{1,2}:[0-9]{2}' | head -1)"
LABEL="$TITLE"
if [ -n "$START" ]; then
  NOW=$(date +%s)
  TARGET=$(date -j -f "%H:%M" "$START" +%s 2>/dev/null)
  [ -n "$TARGET" ] && [ "$TARGET" -lt "$NOW" ] && TARGET=$((TARGET + 86400))
  if [ -n "$TARGET" ]; then
    MINS=$(( (TARGET - NOW) / 60 ))
    if [ "$MINS" -ge 60 ]; then LABEL="$TITLE · $((MINS/60))h $((MINS%60))m"
    else LABEL="$TITLE · ${MINS}m"; fi
  fi
fi
sketchybar --set "$NAME" label="$LABEL"
