#!/bin/bash
CAL="$(cal)"
for i in 1 2 3 4 5 6 7 8; do
  sketchybar --set clock.cal$i label="$(echo "$CAL" | sed -n "${i}p")"
done
ICAL=/opt/homebrew/bin/icalBuddy; [ -x "$ICAL" ] || ICAL=/usr/local/bin/icalBuddy
EV="$("$ICAL" -n -nc -b "" -nrd -ea -iep "title,datetime" -ps "| · |" -tf "%H:%M" eventsToday+2 2>/dev/null | head -5)"
for i in 1 2 3 4 5; do
  L="$(echo "$EV" | sed -n "${i}p" | sed 's/^ *//')"
  [ -z "$L" ] && [ "$i" = 1 ] && L="No upcoming events"
  [ ${#L} -gt 40 ] && L="${L:0:39}…"
  sketchybar --set clock.ev$i label="$L"
done
sketchybar --set clock popup.drawing=toggle
