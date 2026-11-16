#!/bin/bash
if [ "$BUTTON" = right ]; then
  exec "$HOME/.config/sketchybar/plugins/appearance.sh"
else
  exec "$HOME/.config/sketchybar/plugins/menubar_peek.sh"
fi
