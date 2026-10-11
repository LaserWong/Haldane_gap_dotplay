#!/usr/bin/env python3
"""One-shot child, independent wall watchdog, wait4 accounting, no retries."""
import ctypes,os,resource,signal,time,json,sys,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];selftest=sys.argv[1:]==['--self-test'];cpu=30;memory=100*1024**2;parent=os.getpid();libc=ctypes.CDLL(None,use_errno=True);start=time.monotonic();out=P/('guard_selftest.out' if selftest else 'anchors.out');err=P/('guard_selftest.log' if selftest else 'anchors.log');record=P/('guard_selftest.json' if selftest else 'guard_resources.json')
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(memory,memory));resource.setrlimit(resource.RLIMIT_CPU,(30,30))
assert hashlib.sha256((P/'contract_sequential').read_bytes()).hexdigest()=='4dd3ef1afbb71df0e8e1af1f4287d16dc7cf06db8cf06fe9480f26b16cc3ca0a'
if not selftest:assert hashlib.sha256((P/'d26_blocks.txt').read_bytes()).hexdigest()=='26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa'
if not selftest and (P/'guard_resources.json').exists():raise RuntimeError('Refuse automatic retry of the physical batch')
pid=os.fork()
if pid==0:
 try:
  os.setsid();os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu));resource.setrlimit(resource.RLIMIT_AS,(memory,memory));signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU})
  if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:raise OSError(ctypes.get_errno(),'PR_SET_PDEATHSIG')
  death=ctypes.c_int();assert libc.prctl(2,ctypes.byref(death),0,0,0)==0 and death.value==signal.SIGKILL
  assert os.getppid()==parent and os.getsid(0)==os.getpid() and os.getpgrp()==os.getpid()
  assert resource.getrlimit(resource.RLIMIT_CPU)==(cpu,cpu) and resource.getrlimit(resource.RLIMIT_AS)==(memory,memory)
  assert os.sched_getaffinity(0)=={5} and signal.SIGXCPU not in signal.pthread_sigmask(signal.SIG_BLOCK,set()) and signal.getsignal(signal.SIGXCPU)==signal.SIG_DFL
  f=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600);os.dup2(f,1);os.close(f);f=os.open(err,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600);os.dup2(f,2);os.close(f)
  os.write(2,f'GUARD_VERIFIED cpu={cpu}/{cpu} AS={memory}/{memory} affinity=5 SIGXCPU=default_unblocked PDEATHSIG=9 SID=PID PGID=PID threads=1\n'.encode())
  if selftest:os._exit(0)
  exe=str(P/'contract_sequential');args=[exe,str(P/'d26_blocks.txt')]+[str(x) for x in range(26,34)];env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1');os.execve(exe,args,env)
 except BaseException as e:
  os.write(2,('GUARD_SETUP_FAILURE '+repr(e)+'\n').encode());os._exit(125)
watchdog=False;status=None;usage=None;observations=[];observed=False
try:
 while True:
  got,status,usage=os.wait4(pid,os.WNOHANG)
  if got:break
  if not observed:
   try:
    exe_now=os.readlink(f'/proc/{pid}/exe')
    if exe_now==str(P/'contract_sequential'):
     limits=Path(f'/proc/{pid}/limits').read_text();stat=Path(f'/proc/{pid}/status').read_text()
     observations.append({'executable':exe_now,'limits':limits,'status_fields':[s for s in stat.splitlines() if s.startswith(('Threads:','Cpus_allowed_list:','Uid:','Gid:'))]});observed=True
   except (FileNotFoundError,ProcessLookupError):pass
  if time.monotonic()-start>=25:
   watchdog=True
   try:os.killpg(pid,signal.SIGKILL)
   except ProcessLookupError:pass
   _,status,usage=os.wait4(pid,0);break
  time.sleep(.01)
finally:
 # C++ is single-process; remove any unexpected remaining group member as well.
 try:os.killpg(pid,signal.SIGKILL)
 except ProcessLookupError:pass
elapsed=time.monotonic()-start;exitcode=os.waitstatus_to_exitcode(status);r={'postexec_observations':observations,'selftest':selftest,'exit_code':exitcode,'wall_watchdog_fired':watchdog,'wall_seconds':elapsed,'wait4_user_cpu_seconds':usage.ru_utime,'wait4_system_cpu_seconds':usage.ru_stime,'wait4_total_cpu_seconds':usage.ru_utime+usage.ru_stime,'wait4_maxrss_kib':usage.ru_maxrss,'requested_cpu_soft_hard':[30,30],'requested_AS_soft_hard':[memory,memory],'external_wall_limit_seconds':25,'CPU_affinity':[5],'no_retry':True,'program_timer':'See anchors.log separately; not equated to wait4 accounting'};record.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if exitcode==0 and not watchdog else 1)
