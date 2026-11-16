#!/usr/bin/env sh

# Handles click to switch KiwiDesk space
if [ "$SENDER" = "mouse.clicked" ]; then
  kiwidesk focus_space "$SID"
fi
