#!/usr/bin/env python3
"""One-shot separately authorized length64 H² gate, no automatic retry."""
import ctypes,hashlib,json,os,resource,signal,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
mode=sys.argv[1];assert mode in ['compile','pilot'];assert 4 in os.sched_getaffinity(0)
result_path=P/(mode+'_resources.json');assert not result_path.exists(),'No automatic retry'
pins=json.loads((P/'INPUT_SHA256.json').read_text())
for rel,h in pins.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
if mode=='compile':
 cmd=['g++','-O2','-std=c++17',str(P/'pilot.cpp'),'-lgmpxx','-lgmp','-o',str(P/'pilot')];cpu=29;mem=512*1024**2;wall=90
else:
 cmd=[str(P/'pilot'),str(ROOT/'research_20261010/uniform_alternating_b2_fixture/b2_blocks.txt'),str(ROOT/'research_20261010/uniform_smaller_second_initialization_review/anchors.out'),str(P/'expected64.txt'),str(P)];cpu=39;mem=256*1024**2;wall=120
out=os.open(P/(mode+'.out'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
err=os.open(P/(mode+'.log'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
start=time.monotonic();parent_start=time.process_time();pid=os.fork()
if pid==0:
 os.setsid();os.dup2(out,1);os.dup2(err,2);os.close(out);os.close(err)
 resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu));resource.setrlimit(resource.RLIMIT_AS,(mem,mem));os.sched_setaffinity(0,{4})
 signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU});assert ctypes.CDLL(None).prctl(1,signal.SIGKILL)==0
 os.execvp(cmd[0],cmd)
os.close(out);os.close(err);os.sched_setaffinity(0,{4})
# Lower parent memory only after fork: the compiler retains its512MiB hard cap.
resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
fired=None;polls=0;max_polled=0.;hz=os.sysconf('SC_CLK_TCK')
while True:
 got,status,usage=os.wait4(pid,os.WNOHANG)
 if got:break
 try:
  fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
  child_cpu=(int(fields[11])+int(fields[12]))/hz;max_polled=max(max_polled,child_cpu);polls+=1
 except FileNotFoundError:child_cpu=0.
 if time.monotonic()-start>wall:fired='external_wall_watchdog'
 if child_cpu>cpu-1:fired='active_CPU_guard'
 if fired:
  os.killpg(pid,signal.SIGKILL);got,status,usage=os.wait4(pid,0);break
 time.sleep(.04)
r={'mode':mode,'status':'PASS' if os.waitstatus_to_exitcode(status)==0 and fired is None else 'FAILED_NO_AUTOMATIC_RETRY','exit_code':os.waitstatus_to_exitcode(status),'watchdog_fired':fired,'wait4_user_cpu_seconds':usage.ru_utime,'wait4_system_cpu_seconds':usage.ru_stime,'wait4_total_cpu_seconds':usage.ru_utime+usage.ru_stime,'wait4_peak_rss_kib':usage.ru_maxrss,'wall_seconds':time.monotonic()-start,'parent_CPU_seconds':time.process_time()-parent_start,'child_hard_CPU_seconds':cpu,'parent_hard_CPU_seconds':1,'aggregate_authorized_CPU_seconds':30 if mode=='compile' else 40,'active_CPU_kill_threshold':cpu-1,'active_poll_count':polls,'max_polled_CPU_seconds':max_polled,'child_memory_MiB':mem//1024**2,'CPU_affinity':[4],'wall_limit_seconds':wall,'requested_physical_lengths':[] if mode=='compile' else [64],'automatic_retry':False}
result_path.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='PASS' else 1)
