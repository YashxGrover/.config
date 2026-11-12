#!/bin/bash
source "$HOME/.config/sketchybar/colors.sh"
N="$(sysctl -n hw.ncpu)"
CPU="$(ps -A -o %cpu | awk -v n="$N" 'NR>1{s+=$1}END{v=s/n; if(v>100)v=100; printf "%d", v}')"
FREE="$(memory_pressure | awk '/free percentage/{gsub("%","",$5); print $5}')"
MEM=$((100 - ${FREE:-100}))
GPU="$(ioreg -r -d 1 -w0 -c IOAccelerator | grep -oE '"Device Utilization %" ?= ?[0-9]+' | head -1 | grep -oE '[0-9]+$')"
GPU="${GPU:-0}"
col() { if [ "$1" -ge 85 ]; then echo $RED; elif [ "$1" -ge 60 ]; then echo $YELLOW; else echo "$2"; fi; }
f() { awk "BEGIN{printf \"%.2f\", $1/100}"; }
sketchybar \
  --push cpu "$(f $CPU)" --set cpu label="${CPU}%" graph.color="$(col $CPU $GREEN)" \
  --push gpu "$(f $GPU)" --set gpu label="${GPU}%" graph.color="$(col $GPU $BLUE)" \
  --push mem "$(f $MEM)" --set mem label="${MEM}%" graph.color="$(col $MEM $PURPLE)"
