from pathlib import Path
import subprocess,os,resource,time,json
H=Path(__file__).resolve().parent;t=time.monotonic()
def limits():
 os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(40,40));resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2))
rows=[]
for ids in [(0,),(13,),(3,10)]:
 tag='_'.join(map(str,ids));c=[0]*42
 for i in ids:c[28+i]=1
 path=H/'polarization'/('coeff_'+tag+'.txt');path.write_text('400 21\n'+' '.join(map(str,c))+'\n');start=time.monotonic();u=resource.getrusage(resource.RUSAGE_CHILDREN)
 with (H/'polarization'/('run_'+tag+'.log')).open('w') as log:subprocess.run([str(H/'independent_residual'),str(H/'snapshot/geometry_8x4.txt'),str(path),str(H/'polarization'/('result_'+tag+'.json')),'origin'],preexec_fn=limits,timeout=45,check=True,stdout=log,stderr=subprocess.STDOUT)
 v=resource.getrusage(resource.RUSAGE_CHILDREN);row=dict(indices=list(ids),cpu_seconds=v.ru_utime+v.ru_stime-u.ru_utime-u.ru_stime,seconds=time.monotonic()-start,peak_rss_kib=v.ru_maxrss);rows.append(row);print(row,flush=True)
u=resource.getrusage(resource.RUSAGE_CHILDREN);assert u.ru_utime+u.ru_stime<40
out=dict(runs=rows,cpu_seconds=u.ru_utime+u.ru_stime,peak_rss_kib=u.ru_maxrss,projection105_cpu_seconds=max(r['cpu_seconds'] for r in rows)*105)
(H/'benchmark.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
