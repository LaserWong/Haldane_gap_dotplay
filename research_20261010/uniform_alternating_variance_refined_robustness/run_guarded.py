#!/usr/bin/env python3
"""Independent wall/active CPU/wait4 guard for the separately authorized scalar gate."""
import ctypes,hashlib,json,os,resource,signal,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent
assert not (P/'resources.json').exists(), 'No automatic retry'
assert 4 in os.sched_getaffinity(0)
out=os.open(P/'check.out',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
err=os.open(P/'check.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
start=time.monotonic();parent_start=time.process_time();pid=os.fork()
if pid==0:
 os.setsid();os.dup2(out,1);os.dup2(err,2);os.close(out);os.close(err)
 resource.setrlimit(resource.RLIMIT_CPU,(28,28));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));os.sched_setaffinity(0,{4})
 signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU})
 assert ctypes.CDLL(None).prctl(1,signal.SIGKILL)==0
 os.execv(sys.executable,[sys.executable,str(P/'check_scalar.py')])
os.close(out);os.close(err);os.sched_setaffinity(0,{4})
resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
fired=None;polls=0;max_polled=0.;hz=os.sysconf('SC_CLK_TCK')
while True:
 got,status,usage=os.wait4(pid,os.WNOHANG)
 if got:break
 try:
  fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
  child_cpu=(int(fields[11])+int(fields[12]))/hz
  max_polled=max(max_polled,child_cpu);polls+=1
 except FileNotFoundError:child_cpu=0.
 if time.monotonic()-start>90:fired='wall_90_seconds'
 if child_cpu>27:fired='active_child_cpu_27_seconds'
 if fired:
  os.killpg(pid,signal.SIGKILL);got,status,usage=os.wait4(pid,0);break
 time.sleep(.02)
r={'status':'PASS' if os.waitstatus_to_exitcode(status)==0 and fired is None else 'FAILED_NO_AUTOMATIC_RETRY','exit_code':os.waitstatus_to_exitcode(status),'watchdog_fired':fired,'wait4_user_cpu_seconds':usage.ru_utime,'wait4_system_cpu_seconds':usage.ru_stime,'wait4_total_cpu_seconds':usage.ru_utime+usage.ru_stime,'wait4_peak_rss_kib':usage.ru_maxrss,'wall_seconds':time.monotonic()-start,'parent_cpu_seconds':time.process_time()-parent_start,'child_hard_cpu_seconds':28,'parent_hard_cpu_seconds':1,'aggregate_authorized_cpu_seconds':30,'child_active_cpu_kill_threshold':27,'active_poll_count':polls,'max_polled_cpu_seconds':max_polled,'hard_address_space_mib':256,'CPU_affinity':[4],'separately_authorized_new_gate':True,'physical_contractions':False,'automatic_retry':False}
(P/'resources.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='PASS' else 1)
