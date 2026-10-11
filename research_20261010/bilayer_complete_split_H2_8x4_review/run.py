from pathlib import Path
import sys,resource,os,subprocess,time,json
H=Path(__file__).resolve().parent;sample='sample' in sys.argv;tag='sample' if sample else 'full';cap=20 if sample else 90
def limits():
 os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
t=time.monotonic()
with (H/(tag+'.log')).open('w') as log:p=subprocess.run([str(H/'independent_split'),str(H/'snapshot/geometry_8x4.txt'),str(H/(tag+'.json')),'1000' if sample else '0'],preexec_fn=limits,stdout=log,stderr=subprocess.STDOUT,timeout=cap+15)
u=resource.getrusage(resource.RUSAGE_CHILDREN);x=dict(exit_code=p.returncode,cpu_seconds=u.ru_utime+u.ru_stime,seconds=time.monotonic()-t,peak_rss_kib=u.ru_maxrss,cpu_cap=cap,address_cap_mib=100);assert p.returncode==0
if sample:
 a=json.loads((H/'sample.json').read_text());x['projected_full_seconds']=a['cache_seconds']+a['q4_seconds']*4495/a['q4_processed']+a['q6_seconds']*169911/a['q6_processed']
(H/(tag+'_resources.json')).write_text(json.dumps(x,indent=2)+'\n');print(x)
