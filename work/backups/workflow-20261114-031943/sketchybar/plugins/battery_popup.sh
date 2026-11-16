#!/bin/bash
INFO="$(pmset -g batt)"
PCT="$(echo "$INFO" | grep -Eo '[0-9]+%' | head -1)"
SRC="$(echo "$INFO" | head -1 | grep -o "'.*'" | tr -d "'")"
TIME="$(echo "$INFO" | grep -Eo '[0-9]+:[0-9]+ remaining' | head -1)"
[ -z "$TIME" ] && TIME="$(echo "$INFO" | grep -o 'charged\|charging\|finishing charge' | head -1)"
REG="$(ioreg -rc AppleSmartBattery)"
CYC="$(echo "$REG" | awk '/"CycleCount" =/ {print $3; exit}')"
MAXC="$(echo "$REG" | awk '/"AppleRawMaxCapacity" =/ {print $3; exit}')"
DES="$(echo "$REG" | awk '/"DesignCapacity" =/ {print $3; exit}')"
HEALTH=""
[ -n "$MAXC" ] && [ -n "$DES" ] && [ "$DES" -gt 0 ] && HEALTH="$((MAXC * 100 / DES))%"
sketchybar --set battery.p1 label="Charge: $PCT" \
           --set battery.p2 label="Source: $SRC" \
           --set battery.p3 label="Status: ${TIME:-n/a}" \
           --set battery.p4 label="Cycles: ${CYC:-n/a}   Health: ${HEALTH:-n/a}"
sketchybar --set battery popup.drawing=toggle
