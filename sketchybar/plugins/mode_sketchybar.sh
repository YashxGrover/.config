#!/bin/bash
# SketchyBar on top; macOS menu bar auto-hides and can't show over the bar
/opt/homebrew/bin/sketchybar --bar hidden=off topmost=on
/usr/bin/osascript -e 'tell application "System Events" to tell dock preferences to set autohide menu bar to true'
