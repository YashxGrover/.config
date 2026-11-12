#!/bin/bash
KD=/opt/homebrew/bin/kiwidesk
J="$($KD get_state 2>/dev/null)"
[ -z "$J" ] && J="$($KD run get_state 2>/dev/null)"
[ -z "$J" ] && exit 0
OUT="$(printf '%s' "$J" | /usr/bin/python3 -c '
import sys, json
t = sys.stdin.read()
try:
    d = json.loads(t[t.find("{"):t.rfind("}")+1])
except Exception:
    sys.exit(1)
act = str(d.get("active_space", ""))
mode, counts = "", []
for s in d.get("spaces", []):
    counts.append(str(len(s.get("windows", []))))
    if str(s.get("id")) == act:
        mode = s.get("mode", "")
print("%s|%s|%s|%s" % (d.get("desktop", ""), act, ",".join(counts), mode))
')"
[ -z "$OUT" ] && exit 0
[ "$OUT" = "$(cat /tmp/kiwi_state 2>/dev/null)" ] && exit 0
IFS='|' read -r DESKTOP ACTIVE COUNTS MODE <<< "$OUT"
/opt/homebrew/bin/sketchybar --trigger kiwi_update DESKTOP=$DESKTOP ACTIVE=$ACTIVE COUNTS=$COUNTS MODE=$MODE
