#!/usr/bin/env python3
import ctypes,json,os,resource,signal,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent;assert not(P/'scalar_retry1_resources.json').exists()
out=os.open(P/'scalar_retry1.out',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
err=os.open(P/'scalar_retry1.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
start=time.monotonic();ps=time.process_time();pid=os.fork()
if pid==0:
 os.setsid();os.dup2(out,1);os.dup2(err,2);os.close(out);os.close(err)
 resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));os.sched_setaffinity(0,{4})
 signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU});assert ctypes.CDLL(None).prctl(1,signal.SIGKILL)==0
 os.execv(sys.executable,[sys.executable,str(P/'certify_scalar_retry1.py')])
os.close(out);os.close(err);resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));os.sched_setaffinity(0,{4})
fired=None;polls=0;peak=0.;hz=os.sysconf('SC_CLK_TCK')
while True:
 got,status,u=os.wait4(pid,os.WNOHANG)
 if got:break
 try:
  a=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split();c=(int(a[11])+int(a[12]))/hz;peak=max(peak,c);polls+=1
 except FileNotFoundError:c=0.
 if time.monotonic()-start>15:fired='wall'
 if c>2.5:fired='active_CPU'
 if fired:os.killpg(pid,signal.SIGKILL);got,status,u=os.wait4(pid,0);break
 time.sleep(.02)
r={'status':'PASS' if os.waitstatus_to_exitcode(status)==0 and fired is None else 'FAILED_NO_AUTOMATIC_RETRY','exit_code':os.waitstatus_to_exitcode(status),'watchdog_fired':fired,'wait4_child_CPU_seconds':u.ru_utime+u.ru_stime,'parent_CPU_seconds':time.process_time()-ps,'wall_seconds':time.monotonic()-start,'wait4_peak_RSS_KiB':u.ru_maxrss,'hard_child_CPU_seconds':3,'hard_parent_CPU_seconds':1,'memory_MiB':256,'affinity':[4],'active_polls':polls,'max_polled_CPU_seconds':peak,'preserved_failed_scalar_charge':3,'physical_retry':False}
(P/'scalar_retry1_resources.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='PASS' else 1)
