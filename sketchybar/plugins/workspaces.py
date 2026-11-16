#!/usr/bin/python3
"""Profile-aware desktop/Space navigation and native app/window icons."""
import json
import fcntl
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
KD = '/opt/homebrew/bin/kiwidesk'
SB = '/opt/homebrew/bin/sketchybar'


def query(command):
    p = subprocess.run([KD, command], capture_output=True, text=True, timeout=5)
    if p.returncode:
        raise ValueError(p.stderr)
    return json.loads(p.stdout)


def colors():
    values = {}
    for line in (ROOT / 'colors.sh').read_text().splitlines():
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            values[key] = value.strip()
    return values


def render(state, profile, config, palette):
    args = [SB]
    active = str(state.get('active_space', ''))
    desktop = str(state.get('desktop', ''))
    spaces = state.get('spaces', [])
    windows = state.get('windows', [])
    labels = config.get('space_labels', {}).get(profile, {})
    desktop_windows = windows + state.get('away_windows', [])
    by_id = {w['id']: w for w in desktop_windows}

    def set_item(name, *properties):
        args.extend(['--set', name, *properties])

    def app_icon(item, app, scale=0.6):
        set_item(item, 'icon=', 'icon.drawing=on', 'icon.background.image=app.'+app,
                 'icon.background.image.drawing=on', 'icon.background.image.scale='+str(scale))

    for entry in config['desktops']:
        number = str(entry['number'])
        selected = number == desktop
        item = 'desktop.tab'+number
        image=ROOT/'runtime/icons'/('active' if selected else 'inactive')/('desktop'+number+'.png')
        set_item(item, 'label='+(entry['name'] if selected else ''),
                 'width='+('92' if selected else '36'), 'icon.width=28',
                 'label.padding_left=0', 'label.width=dynamic',
                 'label.y_offset=0', 'icon.y_offset=0',
                 'label.color='+palette['ORANGE' if selected else 'DIM'],
                 'icon='+('' if image.exists() else entry['icon']),
                 'icon.font=SF Pro:Regular:19.0',
                 'icon.color='+palette['ORANGE' if selected else 'DIM'],
                 'icon.background.image='+str(image),
                 'icon.background.image.scale=0.65',
                 'icon.background.image.drawing='+('on' if image.exists() else 'off'),
                 'background.drawing=off')

    set_item('kiwi.current', 'drawing=on', 'label='+active)
    for index in range(10):
        tab, option = 'kiwi.tab'+str(index+1), 'workspace.option'+str(index+1)
        if index >= len(spaces):
            set_item(tab, 'drawing=off'); set_item(option, 'drawing=off'); continue
        space = spaces[index]
        sid = str(space['id'])
        selected = sid == active
        target = next((by_id[wid] for wid in space.get('windows', []) if wid in by_id and by_id[wid].get('bundle_id')), {})
        click = shlex.join(['/usr/bin/python3', str(ROOT/'plugins/workspace_select.py'), 'space', sid])
        # The active Space is indicated by number and a flat highlight, without layout text.
        set_item(tab, 'drawing=off', 'label='+sid, 'label.color='+palette['ORANGE' if selected else 'DIM'],
                 'background.drawing='+('on' if selected else 'off'), 'background.color='+palette['PILL'],
                 'click_script='+click)
        set_item(option, 'drawing=on', 'label='+labels.get(sid, 'Space '+sid),
                 'label.color='+palette['ORANGE' if selected else 'FG'], 'click_script='+click)
        if target:
            app_icon(tab, target['bundle_id'], 0.48)
            app_icon(option, target['bundle_id'], 0.55)
        else:
            set_item(tab, 'icon=', 'icon.drawing=on', 'icon.background.image.drawing=off')
            set_item(option, 'icon=', 'icon.drawing=off')
    set_item('workspace.header', 'label='+profile+' · KiwiDesk Spaces')

    # One compact tab per app on this desktop; complete window list stays in the popup.
    groups = {}
    for window in windows:
        if window.get('bundle_id'):
            groups.setdefault(window['bundle_id'], []).append(window)
    for index in range(12):
        item = 'window.tab'+str(index+1)
        if index >= min(len(groups), 5):
            set_item(item, 'drawing=off'); continue
        bundle, group = list(groups.items())[index]
        representative = next((w for w in group if w.get('id') in next((s.get('windows', []) for s in spaces if str(s['id']) == active), [])), group[0])
        click = shlex.join(['/usr/bin/python3', str(ROOT/'plugins/shelf_action.py'), 'app', bundle])
        set_item(item, 'drawing=on', 'label=',
                 'icon.width=24', 'click_script='+click)
        app_icon(item, bundle, 0.7)
    set_item('app.overflow', 'drawing='+('on' if len(groups)>5 else 'off'),
             'label=+'+str(max(0,len(groups)-5)))
    for index in range(24):
        item = 'window.option'+str(index+1)
        if index >= len(windows):
            set_item(item, 'drawing=off'); continue
        window = windows[index]
        title = window.get('title') or window.get('app') or 'Window'
        title = ''.join(c for c in title if c.isprintable())
        click = shlex.join(['/usr/bin/python3', str(ROOT/'plugins/shelf_action.py'), 'window', str(window['id'])])
        sid = next((str(s['id']) for s in spaces if window['id'] in s.get('windows', [])), '?')
        set_item(item, 'drawing=on', 'label='+title+' · '+sid, 'click_script='+click)
        app_icon(item, window.get('bundle_id', window.get('app','')), 0.55)
    return args


def main():
    runtime=ROOT/'runtime';runtime.mkdir(parents=True,exist_ok=True)
    with (runtime/'workspace-poll.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return
        try:
            catalog=ROOT.parent/'workflow/config.json'
            config=json.loads((catalog if catalog.exists() else ROOT/'workspaces.json').read_text())
            state=query('get_state')
            profile=next((d['profile'] for d in config['desktops'] if str(d['number'])==str(state.get('desktop'))),'')
            focused=next((s.get('focused') for s in state.get('spaces',[]) if str(s['id'])==str(state.get('active_space'))),None)
            front=next((w for w in state.get('windows',[]) if w['id']==focused),None)
            if front and front.get('bundle_id'):
                history_path=runtime/'app-history.json'
                try:history=json.loads(history_path.read_text())
                except (OSError,ValueError):history={}
                if history.get(front['bundle_id'])!=focused:
                    history[front['bundle_id']]=focused
                    temporary=history_path.with_suffix('.poll.tmp');temporary.write_text(json.dumps(history));temporary.replace(history_path)
            args=render(state,profile,config,colors())
            cache=runtime/'workspace-render.json';previous=json.loads(cache.read_text()) if cache.exists() else None
            if args!=previous:
                subprocess.run(args,check=True,timeout=5)
                cache.write_text(json.dumps(args))
        except (OSError,ValueError,subprocess.SubprocessError) as error:
            print('Workspace update unavailable: '+str(error),file=sys.stderr)

if __name__=='__main__':main()
