from pathlib import Path
import os,resource,subprocess,time,json
H=Path(__file__).resolve().parent
def limits():
 os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(25,25));resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2))
rows=[]
for tag,geom,limit in [('fixture4x4',H.parent/'bilayer_residual_pencil_review/snapshot/geometry_4x4.txt',0),('sample8x4',H/'snapshot/geometry_8x4.txt',1000)]:
 t=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN)
 with (H/(tag+'.log')).open('w') as log:subprocess.run([str(H/'independent_matrix'),str(geom),str(H/(tag+'.json')),str(limit)],preexec_fn=limits,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=30)
 u=resource.getrusage(resource.RUSAGE_CHILDREN);row=dict(tag=tag,cpu_seconds=u.ru_utime+u.ru_stime-before.ru_utime-before.ru_stime,seconds=time.monotonic()-t,peak_rss_kib=u.ru_maxrss);rows.append(row);print(row,flush=True)
out=dict(runs=rows);(H/'matrix_benchmark_resources.json').write_text(json.dumps(out,indent=2)+'\n')
