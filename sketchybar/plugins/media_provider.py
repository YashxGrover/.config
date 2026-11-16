#!/usr/bin/python3
"""Spotify now playing, with an optional future provider using JSON over stdout."""
import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SB='/opt/homebrew/bin/sketchybar'

def command(argv):
    return subprocess.run(argv,capture_output=True,text=True,check=True,timeout=5).stdout.strip()

def metadata(config):
    if config.get('source')=='external':
        argv=config.get('external',{}).get('metadata_argv',[])
        if not argv:return None
        value=json.loads(command(argv))
        return value if isinstance(value,dict) and value.get('title') and value.get('state') in ['playing','paused'] else None
    script='''const app = Application('com.spotify.client');
if (!app.running()) { JSON.stringify(null); }
else {
 const state = app.playerState();
 if (state !== 'playing' && state !== 'paused') { JSON.stringify(null); }
 else { JSON.stringify({title: app.currentTrack.name(), state: state, app: 'Spotify'}); }
}'''
    return json.loads(command(['/usr/bin/osascript','-l','JavaScript','-e',script]))

def main():
    config=json.loads((ROOT/'media.json').read_text())
    info=metadata(config)
    if len(sys.argv)>1 and sys.argv[1]=='control':
        if not info:return
        if config.get('source')=='external':
            argv=config.get('external',{}).get('play_pause_argv',[])
            if argv:command(argv)
        else:
            command(['/usr/bin/osascript','-e','tell application id "com.spotify.client" to playpause'])
        return
    name=os.environ.get('NAME','media')
    args=[SB,'--set',name]
    if not info:args+=['drawing=off']
    else:
        title=' '.join(str(info['title']).split())
        args+=['drawing=on','label='+title,'icon='+('Ⅱ' if info.get('state')=='paused' else '♪'),'icon.background.image.drawing=off']
    subprocess.run(args,check=True,timeout=5)

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,subprocess.SubprocessError):
        # Fail quietly when Spotify is closed or macOS has not allowed automation.
        if len(sys.argv)==1:
            subprocess.run([SB,'--set',os.environ.get('NAME','media'),'drawing=off'],check=False,timeout=5)
