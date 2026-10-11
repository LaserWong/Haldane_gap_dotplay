#!/usr/bin/env python3
import os,sys,resource,time,signal,ctypes,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
mode=sys.argv[1];assert mode in ['compile','fixture']
result_path=P/(mode+'_resources.json')
assert not result_path.exists(), 'No automatic retry: prior attempt exists'
assert 4 in os.sched_getaffinity(0)
if mode=='compile':cmd=['g++','-O2','-std=c++17',str(P/'fixture.cpp'),'-lgmpxx','-lgmp','-o',str(P/'fixture')];cpu=30;mem=512*1024**2;wall=90
else:
 assert hashlib.sha256((ROOT/'audit/mps/mps_blocks.txt').read_bytes()).hexdigest()=='26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa'
 cmd=[str(P/'fixture'),str(ROOT/'audit/mps/mps_blocks.txt'),str(P/'b2_blocks.txt')];cpu=14;mem=256*1024**2;wall=60
out=os.open(P/(mode+'.out'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);err=os.open(P/(mode+'.log'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
start=time.monotonic();pid=os.fork()
if pid==0:
 os.setsid();os.dup2(out,1);os.dup2(err,2);os.close(out);os.close(err)
 resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu));resource.setrlimit(resource.RLIMIT_AS,(mem,mem));os.sched_setaffinity(0,{4})
 signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU});assert ctypes.CDLL(None).prctl(1,signal.SIGKILL)==0
 os.execvp(cmd[0],cmd)
os.close(out);os.close(err);resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
fired=False
while True:
 got,status,usage=os.wait4(pid,os.WNOHANG)
 if got:break
 if time.monotonic()-start>wall:
  fired=True;os.killpg(pid,signal.SIGKILL);got,status,usage=os.wait4(pid,0);break
 time.sleep(.02)
result={'mode':mode,'exit_code':os.waitstatus_to_exitcode(status),'wall_watchdog_fired':fired,'wall_seconds':time.monotonic()-start,'wait4_user_cpu_seconds':usage.ru_utime,'wait4_system_cpu_seconds':usage.ru_stime,'wait4_total_cpu_seconds':usage.ru_utime+usage.ru_stime,'wait4_peak_rss_kib':usage.ru_maxrss,'child_hard_cpu_seconds':cpu,'child_hard_address_space_mib':mem//1024**2,'parent_hard_cpu_seconds':1,'aggregate_fixture_cpu_ceiling_seconds':15 if mode=='fixture' else None,'affinity':[4],'automatic_retry':False,'requested_physical_lengths':[4,6] if mode=='fixture' else []}
result_path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(0 if result['exit_code']==0 and not fired else 1)
