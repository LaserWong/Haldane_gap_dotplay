import os,sys,json,time,resource,signal,ctypes,math
from pathlib import Path
import engine
P=Path(__file__).resolve().parent
os.sched_setaffinity(0,{6});name,cap,mode=sys.argv[1:];cap=int(cap)
ledger_path=P/'GATE_LEDGER.json';l=engine.read(ledger_path) if ledger_path.exists() else dict(hard=30,soft=25,supervisor_reserved=3,charged=3,attempts=[])
assert l['charged']==3+sum(x['charged'] for x in l['attempts']) and l['charged']+cap<=25
out=P/'runs'/name;out.mkdir(parents=True,exist_ok=False);rec=dict(name=name,mode=mode,charged=cap,state='reserved');l['charged']+=cap;l['attempts'].append(rec);engine.atomic(ledger_path,l)
# Three supervisors at most, each has a separately prepaid one-CPU-second hard cap.
assert len(l['attempts'])<=3;resource.setrlimit(resource.RLIMIT_CPU,(1,1))
controller_cap=.2 if mode=='cpu_fault' else cap;rss_cap=80*1024**2 if mode=='memory_fault' else 256*1024**2
cb=engine.ControlBudget(P/'CONTROL_SESSIONS.json');session=cb.reserve(controller_cap,1)
libc=ctypes.CDLL(None);assert libc.prctl(36,1,0,0,0)==0;owner=os.getpid();started=time.monotonic();pid=os.fork()
if pid==0:
 assert libc.prctl(1,signal.SIGKILL,0,0,0)==0
 if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
 os.setsid();resource.setrlimit(resource.RLIMIT_CPU,(math.ceil(controller_cap),math.ceil(controller_cap)));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));fd=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(fd,1);os.dup2(fd,2);os.close(fd)
 if mode=='cpu_fault':
  while True:pass
 if mode=='memory_fault':
  hold=bytearray(128*1024**2)
  while True:time.sleep(.05)
 os.execv(sys.executable,[sys.executable,str(P/'engine.py'),str(out)])

def scan():
 rows={}
 for f in Path('/proc').iterdir():
  if not f.name.isdigit():continue
  try:s=(f/'stat').read_text()
  except FileNotFoundError:continue
  a=s[s.rfind(')')+2:].split();rows[int(f.name)]=dict(ppid=int(a[1]),pgrp=int(a[2]),cpu=(int(a[11])+int(a[12]))/os.sysconf('SC_CLK_TCK'),rss=int(a[21])*os.sysconf('SC_PAGE_SIZE'))
 return rows
reason=None;peak=0;lastcpu=0
while True:
 w,status,u=os.wait4(pid,os.WNOHANG)
 if w:break
 try:
  rows=scan();assert pid in rows and owner in rows,'missing_mandatory_accounting'
  members={pid};changed=True
  while changed:
   nxt=members|{p for p,v in rows.items() if v['ppid'] in members or v['pgrp']==pid};changed=nxt!=members;members=nxt
  combined=rows[owner]['rss']+sum(rows[p]['rss'] for p in members if p in rows);peak=max(peak,combined);lastcpu=rows[pid]['cpu']
  if lastcpu>=controller_cap-(.03 if controller_cap<1 else .1):reason='controller_session_cpu_guard'
  if combined>rss_cap:reason='combined_supervisor_controller_tree_memory_guard'
  if len(members)>1:reason='unexpected_benchmark_descendant'
 except Exception as e:reason='accounting_failure:'+str(e)
 own=resource.getrusage(resource.RUSAGE_SELF);owncpu=own.ru_utime+own.ru_stime
 if owncpu>.9:reason='supervisor_prepaid_cpu_guard'
 if time.monotonic()-started>max(30,3*cap+10):reason='external_wall_guard'
 if reason:
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  w,status,u=os.wait4(pid,0);break
 time.sleep(.01)
usage=u.ru_utime+u.ru_stime;own=resource.getrusage(resource.RUSAGE_SELF);owncpu=own.ru_utime+own.ru_stime
assert pid not in scan();cb.finish(session,usage,owncpu,'complete' if os.waitstatus_to_exitcode(status)==0 else 'fault_stopped')
rec.update(state='complete' if os.waitstatus_to_exitcode(status)==0 else 'stopped',exit=os.waitstatus_to_exitcode(status),reason=reason,controller_wait4_cpu=usage,supervisor_cpu=owncpu,combined_peak_rss_bytes=peak,rss_limit=rss_cap,wall=time.monotonic()-started,last_observed_controller_cpu=lastcpu,source_sha256=engine.sha((P/'engine.py').read_bytes()),guard_sha256=engine.sha(Path(__file__).read_bytes()))
engine.atomic(ledger_path,l);engine.atomic(out/'RESOURCES.json',rec);print(json.dumps(rec))
if mode=='benchmark':assert rec['state']=='complete','Unexpected failure; no automatic retry'
else:assert reason==('controller_session_cpu_guard' if mode=='cpu_fault' else 'combined_supervisor_controller_tree_memory_guard')
