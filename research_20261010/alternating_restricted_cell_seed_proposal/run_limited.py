import os,sys,time,resource,json,math,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
ledger=P/'RESOURCE_LEDGER.json'
hist=json.loads(ledger.read_text()) if ledger.exists() else []
used=sum(x['charged_cpu_seconds'] for x in hist);budget=float(sys.argv[1]);assert used+budget+0.1<=30,(used,budget)
source_hashes={str(x.relative_to(P)):hashlib.sha256(x.read_bytes()).hexdigest() for x in P.glob('*.py')}
aff=min(os.sched_getaffinity(0));start=time.monotonic();pid=os.fork()
if pid==0:
 os.sched_setaffinity(0,{aff});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(int(budget),int(budget)))
 os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
 os.execv(sys.executable,[sys.executable]+sys.argv[2:])
_,status,r= os.wait4(pid,0);cpu=r.ru_utime+r.ru_stime
rec={'command':sys.argv[2:],'source_sha256_before_execution':source_hashes,'requested_cap_cpu_seconds':budget,'hard_cpu_limit_seconds':int(budget),'hard_address_space_bytes':256*1024**2,'affinity':[aff],'wait4_user_cpu_seconds':r.ru_utime,'wait4_system_cpu_seconds':r.ru_stime,'charged_cpu_seconds':cpu+0.05,'supervisor_overhead_reserve_seconds':0.05,'wall_seconds':time.monotonic()-start,'peak_rss_kib':r.ru_maxrss,'wait_status':status}
hist.append(rec);ledger.write_text(json.dumps(hist,indent=2)+'\n');print(rec);sys.exit(os.waitstatus_to_exitcode(status))
