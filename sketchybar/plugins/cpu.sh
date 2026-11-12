#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
N="$(sysctl -n hw.ncpu)"
CPU="$(ps -A -o %cpu | awk -v n="$N" 'NR>1 {s+=$1} END {v=s/n; if (v>100) v=100; printf "%d", v}')"
COLOR=$FG
[ "$CPU" -ge 60 ] && COLOR=$YELLOW
[ "$CPU" -ge 85 ] && COLOR=$RED
sketchybar --set "$NAME" label="${CPU}%" label.color=$COLOR
