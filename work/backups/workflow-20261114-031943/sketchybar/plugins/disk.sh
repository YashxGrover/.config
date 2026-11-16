#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
read -r size available < <(df -k / | awk 'NR==2 {print $2,$4}')
[[ "$size" =~ ^[0-9]+$ && "$available" =~ ^[0-9]+$ ]] || exit 0
[ "$size" -gt 0 ] || exit 0
percent=$(( (size-available)*100/size ))
color=$DIM
[ "$percent" -ge 75 ] && color=$YELLOW
[ "$percent" -ge 90 ] && color=$RED
sketchybar --set "${NAME:-disk}" label="${percent}%" label.color="$color"
