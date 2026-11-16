#!/bin/bash
# macOS menu bar permanently visible, SketchyBar hidden
/opt/homebrew/bin/sketchybar --bar hidden=on topmost=off
/usr/bin/osascript -e 'tell application "System Events" to tell dock preferences to set autohide menu bar to false'
