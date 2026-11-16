#!/usr/bin/python3
"""Wall-clock timer: click start/pause/resume; right-click resets."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import time


def transition(state, now, click=False, reset=False):
    if reset:
        return {'status': 'idle', 'remaining': 1500}
    state = state.copy()
    if state.get('status') == 'running':
        remaining = max(0, state['deadline'] - now)
        if remaining == 0:
            state = {'status': 'done', 'remaining': 0}
        elif click:
            state = {'status': 'paused', 'remaining': remaining}
    elif click:
        remaining = state.get('remaining', 1500) if state.get('status') == 'paused' else 1500
        state = {'status': 'running', 'deadline': now + remaining}
    return state


def main():
    directory = Path.home() / '.config/sketchybar/runtime'
    directory.mkdir(mode=0o700, exist_ok=True)
    with (directory / 'focus.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = directory / 'focus.json'
        try:
            old = json.loads(path.read_text())
        except (OSError, ValueError):
            old = {'status': 'idle', 'remaining': 1500}
        now = time.time()
        click = os.environ.get('SENDER') == 'mouse.clicked'
        state = transition(old, now, click, click and os.environ.get('BUTTON') == 'right')
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(state))
        temporary.replace(path)
        status = state['status']
        seconds = int(max(0, state.get('deadline', now) - now)) if status == 'running' else int(state.get('remaining', 1500))
        label = 'Focus' if status == 'idle' else 'Done' if status == 'done' else '{}{:02d}:{:02d}'.format('Ⅱ ' if status == 'paused' else '', seconds // 60, seconds % 60)
        subprocess.run(['/opt/homebrew/bin/sketchybar', '--set', os.environ.get('NAME', 'focus'), 'label=' + label], check=False)
        if status == 'done' and old.get('status') != 'done':
            subprocess.Popen(['/usr/bin/afplay', '/System/Library/Sounds/Glass.aiff'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    main()
