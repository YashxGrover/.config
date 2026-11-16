#!/usr/bin/env sh

# High-precision RAM usage with dynamic color alerting
MEM_TOTAL=$(sysctl -n hw.memsize 2>/dev/null)
PAGESIZE=$(pagesize 2>/dev/null)
VM_STAT=$(vm_stat 2>/dev/null)

ACTIVE=$(echo "$VM_STAT" | awk '/Pages active/ {print $3}' | tr -d '.')
WIRED=$(echo "$VM_STAT" | awk '/Pages wired/ {print $4}' | tr -d '.')
COMPRESSED=$(echo "$VM_STAT" | awk '/Pages occupied by compressor/ {print $5}' | tr -d '.')

if [ -n "$MEM_TOTAL" ] && [ -n "$ACTIVE" ] && [ -n "$WIRED" ]; then
  USED=$(( (ACTIVE + WIRED + COMPRESSED) * PAGESIZE ))
  PERCENT=$(( USED * 100 / MEM_TOTAL ))

  if [ "$PERCENT" -ge 85 ]; then
    COLOR=0xffff5f56 # Red (Heavy pressure)
  elif [ "$PERCENT" -ge 65 ]; then
    COLOR=0xffffbd2e # Yellow (Moderate pressure)
  else
    COLOR=0xffffd60a # Clean Yellow
  fi

  sketchybar --set "$NAME" icon="􀍛" icon.color=$COLOR label="${PERCENT}%" label.color=$COLOR
else
  sketchybar --set "$NAME" label="--"
fi
