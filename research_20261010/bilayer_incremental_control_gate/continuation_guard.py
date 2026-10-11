import os,sys,json,fcntl
from pathlib import Path
import engine
from session_supervisor import supervise
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{6});ledger=P/'CONTINUATION_LEDGER.json';assert not ledger.exists()
rec=dict(authorized_cpu=10,soft_stop=10,supervisor_reserved=2,worker_reserved=8,charged=10,state='reserved',scope='metadata-only continuation; no physical contraction')
engine.atomic(ledger,rec);out=P/'runs/metadata_continuation';out.mkdir();lock=open(P/'RUN_LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
r=supervise([sys.executable,str(P/'engine.py'),str(out),str(P/'runs/full_metadata_fixed/data')],out,P/'CONTROL_SESSIONS.json',8,2,lock_fd=lock.fileno());rec.update(r,state='complete' if r['exit']==0 else 'stopped',source_sha256=engine.sha((P/'engine.py').read_bytes()));engine.atomic(ledger,rec);engine.atomic(out/'RESOURCES.json',rec);print(json.dumps(rec));assert r['exit']==0,'Unexpected stop: further retry requires root decision'
