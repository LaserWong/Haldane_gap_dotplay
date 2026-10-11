"""Shared externally supervised controller-session primitive; no automatic retry."""
import os,time,signal,resource,ctypes,math
from pathlib import Path
from engine import ControlBudget

def snapshot():
 rows={}
 for f in Path('/proc').iterdir():
  if not f.name.isdigit():continue
  try:s=(f/'stat').read_text()
  except FileNotFoundError:continue
  a=s[s.rfind(')')+2:].split();rows[int(f.name)]=dict(ppid=int(a[1]),pgrp=int(a[2]),cpu=(int(a[11])+int(a[12]))/os.sysconf('SC_CLK_TCK'),rss=int(a[21])*os.sysconf('SC_PAGE_SIZE'),start=a[19])
 return rows

def supervise(command,out,budget_path,controller_cap,supervisor_cap=1,memory_bytes=256*1024**2,watch_cpu=None,max_descendants=1,lock_fd=None,supervisor_watch_cpu=None):
 assert isinstance(controller_cap,int) and isinstance(supervisor_cap,int)
 os.sched_setaffinity(0,{6});out=Path(out);cb=ControlBudget(budget_path);sid=cb.reserve(controller_cap,supervisor_cap)
 libc=ctypes.CDLL(None);assert libc.prctl(36,1,0,0,0)==0;owner=os.getpid();start=time.monotonic();pid=os.fork()
 if pid==0:
  assert libc.prctl(1,signal.SIGKILL,0,0,0)==0
  if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
  os.environ['CONTROLLER_CPU_CAP']=str(controller_cap)
  os.setsid();resource.setrlimit(resource.RLIMIT_CPU,(controller_cap,controller_cap));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
  if lock_fd is not None:os.set_inheritable(lock_fd,True);os.environ['BILAYER_LOCK_FD']=str(lock_fd)
  fd=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(fd,1);os.dup2(fd,2);os.close(fd);os.execv(command[0],command)
 # Crucial: setting this hard limit before fork prevents child-specific limits.
 resource.setrlimit(resource.RLIMIT_CPU,(supervisor_cap,supervisor_cap))
 limit=controller_cap if watch_cpu is None else watch_cpu;reason=None;peak=0;lastcpu=0;seen={pid};uses=[];lock_verified=False
 while True:
  w,status,u=os.wait4(pid,os.WNOHANG)
  if w:uses.append((w,status,u));break
  try:
   rows=snapshot();assert pid in rows and owner in rows,'mandatory_accounting_missing'
   if lock_fd is not None:
    childfd=os.stat(f'/proc/{pid}/fd/{lock_fd}');parentfd=os.fstat(lock_fd);assert (childfd.st_dev,childfd.st_ino)==(parentfd.st_dev,parentfd.st_ino),'inherited_lock_missing';lock_verified=True
   members={pid};changed=True
   while changed:
    new=members|{p for p,v in rows.items() if v['ppid'] in members or v['pgrp']==pid};changed=new!=members;members=new
   seen|=members;combined=rows[owner]['rss']+sum(rows[p]['rss'] for p in members if p in rows);peak=max(peak,combined);lastcpu=rows[pid]['cpu']
   if lastcpu>=limit-(.03 if limit<1 else .1):reason='controller_session_cpu_guard'
   if combined>memory_bytes:reason='combined_supervisor_controller_worker_memory_guard'
   if len(members)>max_descendants:reason='unexpected_descendant'
  except Exception as e:reason='accounting_failure:'+str(e)
  own=resource.getrusage(resource.RUSAGE_SELF);owncpu=own.ru_utime+own.ru_stime
  ownlimit=supervisor_cap if supervisor_watch_cpu is None else supervisor_watch_cpu
  if owncpu>=ownlimit-(.03 if ownlimit<1 else .1):reason='supervisor_prepaid_cpu_guard'
  if supervisor_watch_cpu is not None:
   for _ in range(20000):pass
  if time.monotonic()-start>max(30,3*controller_cap+10):reason='session_wall_guard'
  if reason:
   for child in seen:
    try:os.killpg(child,signal.SIGKILL)
    except ProcessLookupError:pass
    try:os.kill(child,signal.SIGKILL)
    except ProcessLookupError:pass
   w,status,u=os.wait4(pid,0);uses.append((w,status,u));break
  time.sleep(.01)
 until=time.monotonic()+2
 while True:
  try:w,st,u=os.wait4(-1,os.WNOHANG)
  except ChildProcessError:break
  if w:uses.append((w,st,u));continue
  for child,v in snapshot().items():
   if v['ppid']==owner:
    seen.add(child)
    try:os.kill(child,signal.SIGKILL)
    except ProcessLookupError:pass
  assert time.monotonic()<until,'orphan_cleanup_timeout';time.sleep(.005)
 assert not any(p in snapshot() for p in seen),'surviving_session_member'
 actual=sum(u.ru_utime+u.ru_stime for _,_,u in uses);own=resource.getrusage(resource.RUSAGE_SELF);owncpu=own.ru_utime+own.ru_stime
 # For a multi-process physical session wait4 can include waited-worker CPU.
 # Charge the whole controller reservation regardless; record own CPU only if
 # the successful session supplies its independently measured self-CPU receipt.
 controller_cpu=actual if max_descendants==1 else None
 if controller_cpu is None:
  receipt=out/'SESSION_SELF_CPU.json'
  if receipt.exists():
   import json
   controller_cpu=json.loads(receipt.read_text())['controller_self_cpu']
 if controller_cpu is not None:assert controller_cpu<=controller_cap
 assert owncpu<=supervisor_cap
 rec=cb.state['sessions'][sid];rec.update(state='complete' if os.waitstatus_to_exitcode(status)==0 else 'stopped',controller_cpu=controller_cpu,supervisor_cpu=owncpu)
 from engine import atomic
 atomic(cb.path,cb.state)
 return dict(exit=os.waitstatus_to_exitcode(status),reason=reason,wait4_tree_cpu=actual,controller_cpu=controller_cpu,controller_last_observed_cpu=lastcpu,supervisor_cpu=owncpu,combined_peak_rss_bytes=peak,memory_cap_bytes=memory_bytes,seen=sorted(seen),reaped=[w for w,_,_ in uses],wall=time.monotonic()-start,session_reserved=controller_cap+supervisor_cap,inherited_lock_verified=lock_verified)
