"""Deterministic pre-reservation startup failure; cannot launch physics."""
import os,sys,json,time,resource
from pathlib import Path
job=Path(sys.argv[1]);(job/'STUB_LIMITS.json').write_text(json.dumps(dict(pid=os.getpid(),affinity=sorted(os.sched_getaffinity(0)),cpu=list(resource.getrlimit(resource.RLIMIT_CPU)),address_space=list(resource.getrlimit(resource.RLIMIT_AS)),no_physical=True)))
time.sleep(.25)
raise SystemExit(7)
