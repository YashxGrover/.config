#!/usr/bin/python3
"""Sample byte counters only while the Wi-Fi popup is open."""
import json,os,subprocess,time
from pathlib import Path
SB='/opt/homebrew/bin/sketchybar'
CACHE=Path.home()/'.config/sketchybar/runtime/network.json'
OPEN=CACHE.with_name('network-open')
def sb(*args):subprocess.run([SB,*args],timeout=5,check=False)
def output(*args):return subprocess.run(args,capture_output=True,text=True,timeout=5,check=True).stdout
def sample():
    route=output('/sbin/route','-n','get','default')
    interface=next((line.split(':',1)[1].strip() for line in route.splitlines() if line.strip().startswith('interface:')),'en0')
    rows=output('/usr/sbin/netstat','-ibn').splitlines();header=next(line.split() for line in rows if 'Ibytes' in line)
    row=next(line.split() for line in rows if line.split() and line.split()[0]==interface and '<Link#' in line)
    return {'interface':interface,'time':time.monotonic(),'in':int(row[header.index('Ibytes')]),'out':int(row[header.index('Obytes')])}
def main():
    sender=os.environ.get('SENDER','')
    if sender=='mouse.exited.global':
        OPEN.unlink(missing_ok=True);sb('--set','wifi','popup.drawing=off','update_freq=0');return
    if sender=='mouse.clicked':
        if OPEN.exists():
            OPEN.unlink();sb('--set','wifi','popup.drawing=off','update_freq=0');return
        OPEN.parent.mkdir(parents=True,exist_ok=True);OPEN.touch()
        CACHE.parent.mkdir(parents=True,exist_ok=True)
        try:CACHE.write_text(json.dumps(sample()))
        except (OSError,ValueError,StopIteration,subprocess.SubprocessError):pass
        sb('--set','wifi','popup.drawing=toggle','update_freq=1','--set','wifi.down','label=Download · sampling…','--set','wifi.up','label=Upload · sampling…');return
    if not OPEN.exists():return
    try:
        current=sample();previous=json.loads(CACHE.read_text()) if CACHE.exists() else current
        dt=current['time']-previous['time'];valid=0<dt<10 and current['interface']==previous['interface']
        down=max(0,current['in']-previous['in'])*8/dt/1e6 if valid else 0
        up=max(0,current['out']-previous['out'])*8/dt/1e6 if valid else 0
        CACHE.parent.mkdir(parents=True,exist_ok=True);temp=CACHE.with_suffix('.tmp');temp.write_text(json.dumps(current));temp.replace(CACHE)
        sb('--set','wifi.down',f'label=↓  {down:.2f} Mbps','--set','wifi.up',f'label=↑  {up:.2f} Mbps','--set','wifi.interface','label='+current['interface'])
    except (OSError,ValueError,StopIteration,subprocess.SubprocessError):
        sb('--set','wifi.down','label=No active network','--set','wifi.up','label=—')
if __name__=='__main__':main()
