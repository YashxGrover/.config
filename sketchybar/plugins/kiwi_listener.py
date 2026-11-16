#!/usr/bin/python3
"""One event listener per user; coalesce KiwiDesk bursts into bar refreshes."""
import fcntl,queue,subprocess,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'runtime';RUNTIME.mkdir(parents=True,exist_ok=True)
def listen():
    with (RUNTIME/'kiwi-listener.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return
        process=subprocess.Popen(['/opt/homebrew/bin/kiwidesk','subscribe','--reconnect'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
        signals=queue.Queue(maxsize=1)
        def read():
            for line in process.stdout:
                if line.strip():
                    try:signals.put_nowait(True)
                    except queue.Full:pass
            signals.put(None)
        threading.Thread(target=read,daemon=True).start()
        try:
            while True:
                if signals.get() is None:break
                # Wait briefly to group a burst, bounded to avoid starving updates.
                for _ in range(3):
                    try:
                        if signals.get(timeout=.03) is None:return
                    except queue.Empty:break
                subprocess.run(['/opt/homebrew/bin/sketchybar','--trigger','kiwi_state'],timeout=5,check=False)
        finally:
            process.terminate()
            try:process.wait(timeout=2)
            except subprocess.TimeoutExpired:process.kill()
if __name__=='__main__':
    try:listen()
    except (OSError,subprocess.SubprocessError):pass
