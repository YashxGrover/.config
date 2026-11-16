#!/bin/bash
# Cover the native menu bar completely, including when auto-hide reveals it.
source "$HOME/.config/sketchybar/colors.sh"
/opt/homebrew/bin/sketchybar --bar hidden=off topmost=on color="0xff${BAR:4}" blur_radius=0
/usr/bin/osascript -e 'tell application "System Events" to tell dock preferences to set autohide menu bar to true'
