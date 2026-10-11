import sys,fcntl
from pathlib import Path
P=Path(__file__).resolve().parent;BASE=P.parent/'bilayer_incremental_control_receipt_fix';sys.path.insert(0,str(BASE))
from engine import atomic
from session_supervisor import supervise
phase=int(sys.argv[1]);out=P/'sessions'/str(phase);out.mkdir(parents=True,exist_ok=False)
lock=open(P/'job/LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
r=supervise([sys.executable,str(P/'adapter.py'),str(phase)],out,P/'job/CONTROL_SESSIONS.json',3,2,max_descendants=2,lock_fd=lock.fileno(),wall_limit=100,controller_address_space=64*1024**2,supervisor_address_space=32*1024**2,descendant_address_space=160*1024**2)
atomic(out/'RESOURCES.json',r);assert r['exit']==0,'Unexpected failure; no retry authorized'
