#!/usr/bin/python3
import subprocess
import sys
from pathlib import Path

kind, value = sys.argv[1:3]
command = {'desktop': 'focus_desktop', 'space': 'focus_space'}[kind]
result = subprocess.run(['/opt/homebrew/bin/kiwidesk', command, value], capture_output=True, text=True)
if result.returncode or 'cannot connect' in result.stdout.lower() or result.stdout.startswith('error:'):
    raise SystemExit(result.stderr or result.stdout)
parent = 'kiwi.desk' if kind == 'desktop' else 'kiwi.current'
subprocess.run(['/opt/homebrew/bin/sketchybar', '--set', parent, 'popup.drawing=off'], check=False)
subprocess.run(['/usr/bin/python3', str(Path(__file__).with_name('workspaces.py'))], check=False)
