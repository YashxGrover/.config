#!/bin/bash
APP="$INFO"
if [ -z "$APP" ]; then
  APP="$(/usr/bin/osascript -l JavaScript -e 'ObjC.import("AppKit"); $.NSWorkspace.sharedWorkspace.frontmostApplication.localizedName.js' 2>/dev/null)"
fi
[ -n "$APP" ] && sketchybar --set "$NAME" label="$APP" icon="" icon.drawing=on icon.width=24 icon.background.image="app.$APP" icon.background.image.drawing=on icon.background.image.scale=0.65
