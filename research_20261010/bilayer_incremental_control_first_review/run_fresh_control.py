import os,sys,json,fcntl
from pathlib import Path
P=Path(__file__).resolve().parent;S=P/'control_sandbox';sys.path.insert(0,str(S))
from session_supervisor import supervise
from engine import atomic
out=P/'control_fresh';out.mkdir();lock=open(out/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
r=supervise([sys.executable,str(S/'engine.py'),str(out)],out,out/'CONTROL_SESSIONS.json',15,2,lock_fd=lock.fileno())
atomic(out/'RESOURCES.json',r)
assert r['exit']==0 and r['reason'] is None and r['inherited_lock_verified']
b=json.loads((out/'BENCHMARK.json').read_text());assert b['records']==2945 and b['resumed_from_committed']==0
assert b['restart_reads']['new_adoptions']==1 and b['restart_reads']['raw_outputs']==1
assert b['fully_committed_restart_reads']['new_adoptions']==b['fully_committed_restart_reads']['raw_outputs']==0
print('FRESH2945 COMPONENT BENCHMARK PASS',json.dumps(r))
