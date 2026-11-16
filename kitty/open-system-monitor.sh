#!/bin/bash
set -euo pipefail

KITTY_BIN="$(command -v kitty || true)"
if [[ -z "$KITTY_BIN" ]]; then
  echo "Kitty was not found. Install or launch Kitty, then run this helper again." >&2
  exit 127
fi

if command -v btop >/dev/null 2>&1; then
  exec "$KITTY_BIN" --title "Mac System Monitor" btop
fi

# Keep the dashboard useful before btop is installed; the launcher automatically
# switches to btop once it becomes available on PATH.
exec "$KITTY_BIN" --title "Mac System Monitor" /usr/bin/python3 "$HOME/.config/kitty/system_monitor.py"
