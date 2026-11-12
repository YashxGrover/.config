#!/bin/bash
# Hide SketchyBar briefly so the macOS menu bar can show, then restore it
sketchybar --bar hidden=on topmost=off
( sleep 5; sketchybar --bar hidden=off topmost=on ) >/dev/null 2>&1 &
