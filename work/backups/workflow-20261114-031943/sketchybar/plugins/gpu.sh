#!/usr/bin/env sh

# Live Apple Silicon GPU utilization with dynamic colors
GPU_LOAD=$(ioreg -r -c IOAccelerator 2>/dev/null | grep -m1 -o '"Device Utilization %"=[0-9]*' | cut -d'=' -f2)

if [ -z "$GPU_LOAD" ]; then
  GPU_LOAD="0"
fi

if [ "$GPU_LOAD" -ge 75 ]; then
  COLOR=0xffff5f56 # Red (High GPU load)
elif [ "$GPU_LOAD" -ge 40 ]; then
  COLOR=0xffffbd2e # Yellow
else
  COLOR=0xffd38aea # Purple (Normal)
fi

sketchybar --set "$NAME" icon="􀤆" icon.color=$COLOR label="${GPU_LOAD}%" label.color=$COLOR
