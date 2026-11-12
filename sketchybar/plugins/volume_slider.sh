#!/bin/bash
osascript -e "set volume output volume $PERCENTAGE"
sketchybar --set "$NAME" slider.percentage="$PERCENTAGE"
