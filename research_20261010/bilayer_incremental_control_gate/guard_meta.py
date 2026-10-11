import os,sys,json,fcntl
from pathlib import Path
import engine
from session_supervisor import supervise
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{6});name,cap,mode=sys.argv[1:];cap=int(cap)
path=P/'GATE_LEDGER.json';l=engine.read(path)
assert l['charged']==l['supervisor_reserved']+sum(x['charged'] for x in l['attempts']) and l['charged']+cap<=l['soft']
out=P/'runs'/name;out.mkdir(parents=True,exist_ok=False);rec=dict(name=name,mode=mode,charged=cap,state='reserved');l['charged']+=cap;l['attempts'].append(rec);engine.atomic(path,l)
command=[sys.executable,str(P/'engine.py'),str(out)];watch=None;superwatch=None;mem=256*1024**2
if mode=='cpu_fault':command=[sys.executable,'-c','import resource,os,json; print(json.dumps({"cpu":resource.getrlimit(resource.RLIMIT_CPU),"as":resource.getrlimit(resource.RLIMIT_AS),"affinity":list(os.sched_getaffinity(0))}),flush=True); exec("while True: pass")'];watch=.2
if mode=='memory_fault':command=[sys.executable,'-c','import resource,os,json,time; print(json.dumps({"cpu":resource.getrlimit(resource.RLIMIT_CPU),"as":resource.getrlimit(resource.RLIMIT_AS),"affinity":list(os.sched_getaffinity(0))}),flush=True); x=bytearray(128*1024**2); time.sleep(20)'];mem=80*1024**2
if mode=='supervisor_fault':command=[sys.executable,'-c','import resource,os,json,time; print(json.dumps({"cpu":resource.getrlimit(resource.RLIMIT_CPU),"as":resource.getrlimit(resource.RLIMIT_AS),"affinity":list(os.sched_getaffinity(0))}),flush=True); time.sleep(20)'];superwatch=.2
lock=open(P/'RUN_LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
r=supervise(command,out,P/'CONTROL_SESSIONS.json',cap,1,mem,watch,lock_fd=lock.fileno(),supervisor_watch_cpu=superwatch);rec.update(r,state='complete' if r['exit']==0 else 'stopped',source_sha256=engine.sha((P/'engine.py').read_bytes()),guard_sha256=engine.sha(Path(__file__).read_bytes()))
engine.atomic(path,l);engine.atomic(out/'RESOURCES.json',rec);print(json.dumps(rec))
if mode=='benchmark':assert rec['state']=='complete','Unexpected failure; no automatic retry'
else:assert r['reason']=={'cpu_fault':'controller_session_cpu_guard','memory_fault':'combined_supervisor_controller_worker_memory_guard','supervisor_fault':'supervisor_prepaid_cpu_guard'}[mode]
