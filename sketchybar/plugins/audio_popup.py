#!/usr/bin/python3
"""Populate the output selector on click, without a background audio poller."""
import json,os,shlex,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SB='/opt/homebrew/bin/sketchybar'
def set_items(*args):subprocess.run([SB,*args],check=True,timeout=5)
def main():
    if len(sys.argv)>1:
        subprocess.run([str(ROOT/'audio_devices'),'select',sys.argv[1]],check=True,timeout=5)
        set_items('--set','volume','popup.drawing=off');return
    try:
        result=subprocess.run([str(ROOT/'audio_devices')],capture_output=True,text=True,check=True,timeout=5)
        devices=json.loads(result.stdout)
        args=[]
        for i in range(12):
            name=f'volume.device{i}'
            if i>=len(devices):args+=['--set',name,'drawing=off'];continue
            device=devices[i]
            click=shlex.join(['/usr/bin/python3',str(Path(__file__).resolve()),device['uid']])
            args+=['--set',name,'drawing=on','label='+('✓  ' if device['selected'] else '    ')+device['name'],'click_script='+click]
        args+=['--set','volume.note','drawing=off','--set','volume','popup.drawing=toggle']
        set_items(*args)
    except (OSError,ValueError,subprocess.SubprocessError):
        set_items('--set','volume.note','drawing=on','label=Audio helper unavailable — run workflow/build_helpers.sh','--set','volume','popup.drawing=toggle')
if __name__=='__main__':main()
