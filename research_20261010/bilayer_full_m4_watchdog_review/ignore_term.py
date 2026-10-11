"""Metadata-only watchdog fault: ignore TERM, await group KILL."""
import os,sys,time,signal,json,resource
from pathlib import Path
p=Path(sys.argv[1]);p.mkdir()
def term(*args):(p/'TERM_SEEN').write_text('TERM observed; deliberate ignore for KILL test\n')
signal.signal(signal.SIGTERM,term)
(p/'PID_LIMITS.json').write_text(json.dumps(dict(pid=os.getpid(),ppid=os.getppid(),cpu=resource.getrlimit(resource.RLIMIT_CPU),address_space=resource.getrlimit(resource.RLIMIT_AS),affinity=sorted(os.sched_getaffinity(0)))))
while True:time.sleep(.05)
