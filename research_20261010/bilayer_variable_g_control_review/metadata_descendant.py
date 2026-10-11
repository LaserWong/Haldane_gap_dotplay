"""Planned controller-death fixture, no numerical kernel."""
import os,sys,time,signal,ctypes,json
from pathlib import Path
out=Path(sys.argv[1]);owner=os.getpid();pid=os.fork()
if not pid:
 assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
 if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
 os.setsid()
 while True:time.sleep(.02)
(out/'PIDS.json').write_text(json.dumps(dict(controller=owner,worker=pid)))
while True:time.sleep(.02)
