import os,sys,time,signal,resource,ctypes,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent/'bilayer_incremental_control_receipt_fix';sys.path.insert(0,str(B));from engine import atomic,read,sha
K=P.parent/'bilayer_variable_g_control_gate'
def status(pid):
 d={}
 for line in Path('/proc/%d/status'%pid).read_text().splitlines():
  k,_,v=line.partition(':')
  if k in ('VmPeak','VmSize','VmRSS'):d[k]=int(v.split()[0])*1024
 return d
def cleanup(pid):
 # Fixed known child: no directory scan or memory-proportional enumeration.
 try:os.kill(pid,signal.SIGKILL)
 except ProcessLookupError:pass
 return os.wait4(pid,0)
def observe():
 resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2))
 out=P/'sample';out.mkdir();pid=os.fork()
 if pid==0:
  libc=ctypes.CDLL(None);assert libc.prctl(1,signal.SIGKILL,0,0,0)==0
  resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(128*1024**2,128*1024**2));fd=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT,0o600);os.dup2(fd,1);os.dup2(fd,2)
  args=[str(K/'whole'),'chunk','sample',str(out),str(P.parent/'bilayer_whole_m4_pipeline'),str(P.parent/'bilayer_brauer_rule_compiler/run'),'3','8','6','0','64'];os.execv(args[0],args)
 atomic(P/'NATIVE_PID.json',dict(pid=pid));start=time.monotonic();peak={};reason=None
 while True:
  w,st,u=os.wait4(pid,os.WNOHANG)
  if w:break
  try:
   for k,v in status(pid).items():peak[k]=max(peak.get(k,0),v)
   own=resource.getrusage(resource.RUSAGE_SELF)
   if own.ru_utime+own.ru_stime>1.8:raise RuntimeError('observer_cpu_guard')
   if time.monotonic()-start>30:raise RuntimeError('worker_wall_guard')
  except Exception as e:reason=repr(e);w,st,u=cleanup(pid);break
  time.sleep(.01)
 result=dict(exit=os.waitstatus_to_exitcode(st),reason=reason,wait4_cpu=u.ru_utime+u.ru_stime,observed_native_status_maxima=peak,worker_as_bytes=128*1024**2,observer_as_bytes=64*1024**2,wall=time.monotonic()-start)
 atomic(P/'NATIVE_RESOURCES.json',result);assert result['exit']==0 and reason is None
 a=out/'result.json.accumulators.json';b=K/'runs/final_sample6/result.json.accumulators.json';assert read(a)==read(b)
 result['all24_equal']=True;result['accepted_accumulator_sha256']=sha(b.read_bytes());atomic(P/'NATIVE_RESOURCES.json',result)
 # Deliberate MemoryError path: one sleeping child, known PID only. Its one
 # second no-refund reservation is part of the three-second observer bundle.
 fault=os.fork()
 if fault==0:
  assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
  resource.setrlimit(resource.RLIMIT_CPU,(1,1));time.sleep(30);os._exit(0)
 try:raise MemoryError('planned allocation-failure injection')
 except MemoryError:w,st,u=cleanup(fault)
 assert os.waitstatus_to_exitcode(st)==-signal.SIGKILL
 atomic(P/'ENOMEM_CLEANUP.json',dict(injected=True,killed_and_reaped=w==fault,exit=os.waitstatus_to_exitcode(st),wait4_cpu=u.ru_utime+u.ru_stime,enumeration_required=False))
 atomic(P/'OBSERVER_STATUS.json',dict(status=status(os.getpid()),self_cpu=time.process_time()))
if __name__=='__main__':
 if len(sys.argv)>1:observe();sys.exit(0)
 os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(2,3));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2));assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
 ledger=P/'LEDGER.json';assert not ledger.exists();rec=dict(authorized=8,charged=8,breakdown=dict(native=3,observer_self=2,observer_fault_child=1,outer=2),state='reserved');atomic(ledger,rec)
 pid=os.fork()
 if pid==0:
  assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
  os.setsid();os.execv(sys.executable,[sys.executable,str(P/'profile.py'),'observe'])
 start=time.monotonic();peak=0;reason=None
 while True:
  w,st,u=os.wait4(pid,os.WNOHANG)
  if w:break
  try:
   rss=status(os.getpid()).get('VmRSS',0)+status(pid).get('VmRSS',0)
   f=P/'NATIVE_PID.json'
   if f.exists():
    try:rss+=status(read(f)['pid']).get('VmRSS',0)
    except FileNotFoundError:pass
   peak=max(peak,rss);own=resource.getrusage(resource.RUSAGE_SELF)
   if rss>256*1024**2:raise RuntimeError('combined_memory')
   if own.ru_utime+own.ru_stime>1.8:raise RuntimeError('outer_cpu')
   if time.monotonic()-start>40:raise RuntimeError('outer_wall')
  except Exception as e:
   reason=repr(e)
   try:os.killpg(pid,signal.SIGKILL)
   except ProcessLookupError:pass
   w,st,u=os.wait4(pid,0);break
  time.sleep(.02)
 children_cpu=u.ru_utime+u.ru_stime
 while True:
  try:w2,s2,u2=os.wait4(-1,os.WNOHANG)
  except ChildProcessError:break
  if w2:children_cpu+=u2.ru_utime+u2.ru_stime
  else:
   try:os.killpg(pid,signal.SIGKILL)
   except ProcessLookupError:pass
   time.sleep(.01)
 own=resource.getrusage(resource.RUSAGE_SELF);rec.update(state='complete' if st==0 and reason is None else 'failed',exit=os.waitstatus_to_exitcode(st),reason=reason,wait4_tree_cpu=children_cpu,outer_self_cpu=own.ru_utime+own.ru_stime,combined_peak_rss_bytes=peak,wall=time.monotonic()-start);atomic(ledger,rec);print(rec);assert rec['state']=='complete','No automatic retry'
