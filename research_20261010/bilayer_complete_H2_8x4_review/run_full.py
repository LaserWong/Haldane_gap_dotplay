from pathlib import Path
import os,resource,subprocess,json,time,hashlib
H=Path(__file__).resolve().parent
def limits():
 os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2))
t=time.monotonic()
with (H/'full_run.log').open('w') as log:p=subprocess.run([str(H/'independent_matrix'),str(H/'snapshot/geometry_8x4.txt'),str(H/'independent_matrix_8x4.json'),'0'],preexec_fn=limits,stdout=log,stderr=subprocess.STDOUT,timeout=75)
u=resource.getrusage(resource.RUSAGE_CHILDREN);r=dict(exit_code=p.returncode,cpu_seconds=u.ru_utime+u.ru_stime,seconds=time.monotonic()-t,peak_rss_kib=u.ru_maxrss,cpu_limit=60,address_space_limit_mib=250,engine_sha256=hashlib.sha256((H/'independent_matrix').read_bytes()).hexdigest());(H/'full_run_resources.json').write_text(json.dumps(r,indent=2)+'\n');print(r);assert p.returncode==0
