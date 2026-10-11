import os,sys,time,resource,signal,ctypes
from pathlib import Path
P=Path(__file__).resolve().parent;BASE=P.parent/'bilayer_control_memory_revision';sys.path.insert(0,str(BASE))
from engine import atomic,read,sha
from session_supervisor import snapshot
import physical_session as phys
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(2,6));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,256*1024**2))
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
ledger=P/'GATE_LEDGER.json';assert not ledger.exists()
rec=dict(hard_cpu=30,charged=30,breakdown=dict(reference_workers=6,singleton_workers=12,controllers=6,supervisors=4,outer=2),state='reserved',physical_scope='four singleton targets and accepted 64q6+16q4 aggregate controls only')
atomic(ledger,rec);job=P/'job';job.mkdir()
authority=dict(explicit_authorization=True,hard_cap=21600,deadline_utc='2026-10-14T00:00:00Z',session_chunk_limit=2,scope='TEST-ONLY-30-CPU-GATE-NOT-PRODUCTION-AUTHORITY')
atomic(job/'PRODUCTION_AUTHORITY.json',authority);atomic(job/'EXPECTED_M012.json',dict(schema='TEST-ONLY-NO-FULL-MOMENT-CONTROLS',scope='must never reach full accepted-control comparison'))
atomic(job/'CONTROL_SESSIONS.json',dict(prepaid=1200,reserved=0,sessions=[]))
pins={p:sha(Path(p).read_bytes()) for p in phys.required_pins(job)}
for p in [P/'adapter.py',P/'session.py',P/'outer.py']:pins[str(p.resolve())]=sha(p.read_bytes())
atomic(job/'PINNED_INPUTS.json',pins)
start=time.monotonic();charged_actual=0;peak=0;uses=[]
for phase in (0,1):
 pid=os.fork()
 if pid==0:
  libc=ctypes.CDLL(None);assert libc.prctl(1,signal.SIGKILL,0,0,0)==0
  os.setsid();resource.setrlimit(resource.RLIMIT_CPU,(6,6));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));os.execv(sys.executable,[sys.executable,str(P/'session.py'),str(phase)])
 reason=None;seen={pid}
 while True:
  w,st,u=os.wait4(pid,os.WNOHANG)
  if w:break
  try:
   rows=snapshot();members={pid}
   while True:
    more=members|{p for p,v in rows.items() if v['ppid'] in members or v['pgrp']==pid}
    if more==members:break
    members=more
   seen|=members;rss=rows[os.getpid()]['rss']+sum(rows[p]['rss'] for p in members if p in rows);peak=max(peak,rss)
   own=resource.getrusage(resource.RUSAGE_SELF);cpu=own.ru_utime+own.ru_stime
   if rss>256*1024**2:reason='whole_tree_memory'
   if cpu>1.8:reason='outer_cpu'
   if charged_actual+sum(rows[p]['cpu'] for p in members if p in rows)+cpu>29.8:reason='aggregate_cpu'
   if time.monotonic()-start>180:reason='wall_deadline'
  except Exception as e:reason='mandatory_accounting:'+str(e)
  if reason:
   for p in seen:
    try:os.kill(p,signal.SIGKILL)
    except ProcessLookupError:pass
   w,st,u=os.wait4(pid,0);break
  time.sleep(.025)
 charged_actual+=u.ru_utime+u.ru_stime;uses.append(dict(phase=phase,exit=os.waitstatus_to_exitcode(st),wait4_tree_cpu=u.ru_utime+u.ru_stime,reason=reason))
 atomic(P/'OUTER_PROGRESS.json',dict(sessions=uses,combined_peak_rss_bytes=peak))
 if st or reason:
  rec.update(state='failed',sessions=uses);atomic(ledger,rec);raise RuntimeError('Unexpected failure: all reservations remain charged; no retry')
 assert not any(p in snapshot() for p in seen),'surviving descendant'
 own=resource.getrusage(resource.RUSAGE_SELF)
rec.update(state='complete',sessions=uses,wait4_cpu=charged_actual,outer_cpu=own.ru_utime+own.ru_stime,wall=time.monotonic()-start,combined_peak_rss_bytes=peak)
atomic(ledger,rec);print(rec)
