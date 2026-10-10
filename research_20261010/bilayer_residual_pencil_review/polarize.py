from pathlib import Path
import subprocess,os,resource,time,json,itertools
P=Path(__file__).resolve().parent;start=time.monotonic()
def limits():
 os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(remaining,remaining));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
labels=[(i,) for i in range(5)]+list(itertools.combinations(range(5),2));out=[]
for ids in labels:
 used=resource.getrusage(resource.RUSAGE_CHILDREN);remaining=max(1,int(30-used.ru_utime-used.ru_stime));assert used.ru_utime+used.ru_stime<29
 tag='_'.join(map(str,ids));coeff=P/'polarization'/('coeff_'+tag+'.txt');dest=P/'polarization'/('result_'+tag+'.json')
 c=[0]*15
 for i in ids:c[10+i]=1
 coeff.write_text('400 21\n'+' '.join(map(str,c))+'\n')
 with (P/'polarization'/('run_'+tag+'.log')).open('w') as log:
  subprocess.run([str(P/'independent_residual'),str(P/'snapshot/geometry_4x4.txt'),str(coeff),str(dest),'origin'],preexec_fn=limits,stdout=log,stderr=subprocess.STDOUT,timeout=45,check=True)
 out.append(dict(indices=list(ids),file=str(dest.relative_to(P))));print('PASS',tag,flush=True)
u=resource.getrusage(resource.RUSAGE_CHILDREN);assert u.ru_utime+u.ru_stime<=30
(P/'polarization_runs.json').write_text(json.dumps(dict(runs=out,cpu_seconds=u.ru_utime+u.ru_stime,seconds=time.monotonic()-start,peak_rss_kib=u.ru_maxrss,scope='4x4 only; 15 exact independent scalar polarizations; no8x4 support contraction'),indent=2)+'\n')
