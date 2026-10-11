import os,sys,time,signal,resource,ctypes
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from engine import atomic
from session_supervisor import snapshot
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(2,8));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2));assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
f=P/'TEST_LEDGER.json';assert not f.exists();r=dict(authorized=10,charged=10,child_tree_reserved=8,external_reserved=2,state='reserved');atomic(f,r)
pid=os.fork()
if pid==0:
 assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
 os.setsid();resource.setrlimit(resource.RLIMIT_CPU,(8,8));os.execv(sys.executable,[sys.executable,str(P/'test_observer.py')])
start=time.monotonic();peak=0;seen={pid};reason=None
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
  if rss>256*1024**2:reason='whole_tree_rss'
  if sum(rows[p]['cpu'] for p in members if p in rows)>=7.8:reason='tree_cpu'
  if time.process_time()>=1.8:reason='external_cpu'
  if time.monotonic()-start>30:reason='wall'
 except Exception:reason='accounting_failure'
 if reason:
  for p in seen:
   try:os.kill(p,signal.SIGKILL)
   except ProcessLookupError:pass
  w,st,u=os.wait4(pid,0);break
 time.sleep(.01)
cpu=u.ru_utime+u.ru_stime
while True:
 try:w2,s2,u2=os.wait4(-1,os.WNOHANG)
 except ChildProcessError:break
 if w2:cpu+=u2.ru_utime+u2.ru_stime
 else:
  for p in seen:
   try:os.kill(p,signal.SIGKILL)
   except ProcessLookupError:pass
  time.sleep(.005)
r.update(state='complete' if st==0 and reason is None else 'failed',exit=os.waitstatus_to_exitcode(st),reason=reason,wait4_tree_cpu=cpu,external_self_cpu=time.process_time(),combined_peak_rss_bytes=peak,wall=time.monotonic()-start);atomic(f,r);print(r);assert r['state']=='complete','No automatic retry'
