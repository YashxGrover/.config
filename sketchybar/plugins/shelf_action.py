#!/usr/bin/python3
"""KiwiDesk actions from top-bar window icons; right click for moves/pocket."""
import json
import os
from pathlib import Path
import subprocess
import sys

KD='/opt/homebrew/bin/kiwidesk'
SB='/opt/homebrew/bin/sketchybar'
ROOT=Path(__file__).resolve().parents[1]


def run(*args):
    p=subprocess.run([KD,*map(str,args)],text=True,capture_output=True,timeout=10)
    if p.returncode or 'cannot connect' in p.stdout.lower() or p.stdout.startswith('error:'):
        raise RuntimeError(p.stderr or p.stdout)
    return p.stdout


def choose(options):
    script='''on run argv
set choice to choose from list argv with prompt "Window actions"
if choice is false then return ""
return item 1 of choice
end run'''
    return subprocess.run(['/usr/bin/osascript','-e',script,*options],text=True,capture_output=True).stdout.strip()


def choose_app_window(state,bundle,history):
    ids=[w['id'] for w in state.get('windows',[]) if w.get('bundle_id')==bundle]
    if not ids:return None
    focused=next((s.get('focused') for s in state.get('spaces',[]) if str(s['id'])==str(state.get('active_space'))),None)
    if focused in ids:return ids[(ids.index(focused)+1)%len(ids)]
    previous=history.get(bundle)
    return previous if previous in ids else ids[0]

def main():
    if sys.argv[1]=='pocket':
        run('pocket' if os.environ.get('BUTTON')=='right' else 'pocket.toggle_list')
        return
    if sys.argv[1]=='all':
        state=json.loads(run('get_state'))
        options={str(i+1)+' · '+(w.get('app','Window'))+' · '+(w.get('title') or ''):w['id'] for i,w in enumerate(state.get('windows',[]))}
        if not options:return
        selected=choose(list(options))
        if selected in options:run('focus_window',options[selected])
        return
    if sys.argv[1]=='app':
        bundle=sys.argv[2];state=json.loads(run('get_state'))
        history_path=ROOT/'runtime/app-history.json'
        try:history=json.loads(history_path.read_text())
        except (OSError,ValueError):history={}
        target=choose_app_window(state,bundle,history)
        if target is None:return
        run('focus_window',target)
        history[bundle]=target;history_path.parent.mkdir(parents=True,exist_ok=True)
        temporary=history_path.with_suffix('.tmp');temporary.write_text(json.dumps(history));temporary.replace(history_path)
        return
    wid=int(sys.argv[2])
    if os.environ.get('BUTTON')!='right':
        run('focus_window',wid)
    else:
        state=json.loads(run('get_state'))
        config=json.loads((ROOT/'workspaces.json').read_text())
        actions={'Focus this window':('focus_window',wid),'Pocket / restore this window':('pocket',wid)}
        for space in state.get('spaces',[]):
            sid=str(space['id']);actions['Move to Space '+sid]=('move_to_space',sid,wid)
        for d in config['desktops']:
            actions['Move to desktop · '+d['name']]=('move_to_desktop',d['number'],'1',wid)
        selected=choose(list(actions))
        if selected in actions:run(*actions[selected])
    subprocess.run([SB,'--set','front_app','popup.drawing=off'],check=False)
    subprocess.run(['/usr/bin/python3',str(ROOT/'plugins/workspaces.py')],check=False)


if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError,subprocess.TimeoutExpired) as e:
        print(str(e),file=sys.stderr);sys.exit(1)
