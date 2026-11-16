#!/bin/bash
# A file lock prevents overlapping peeks and releases automatically on exit.
exec /usr/bin/python3 - <<'PY'
import fcntl
from pathlib import Path
import subprocess
root = Path.home() / '.config/sketchybar'
runtime = root / 'runtime'
runtime.mkdir(mode=0o700, exist_ok=True)
with (runtime / 'menubar-peek.lockfile').open('a') as lock:
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(0)
    helper = root / 'plugins/menubar_peek'
    if helper.is_file():
        subprocess.run([str(helper)], check=False)
    else:
        import time
        bar = '/opt/homebrew/bin/sketchybar'
        try:
            subprocess.run([bar, '--bar', 'hidden=on', 'topmost=off'], check=False)
            time.sleep(2)
        finally:
            subprocess.run([bar, '--bar', 'hidden=off', 'topmost=on'], check=False)
PY
