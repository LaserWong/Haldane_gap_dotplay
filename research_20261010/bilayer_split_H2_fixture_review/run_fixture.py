from pathlib import Path
import os,resource,subprocess,time,json
H=Path(__file__).resolve().parent
out={}
for name,command,mem,cpu in [('compile',['g++','-O3','-UNDEBUG',str(H/'independent_split.cpp'),'-o',str(H/'independent_split')],512,40),('physical',[str(H/'independent_split'),str(H/'snapshot/geometry_4x4.txt'),str(H/'independent_result.json'),'0'],100,30)]:
 def limits():
  os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(mem*1024**2,mem*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu))
 t=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN)
 with (H/(name+'.log')).open('w') as log:p=subprocess.run(command,preexec_fn=limits,stdout=log,stderr=subprocess.STDOUT,timeout=50)
 u=resource.getrusage(resource.RUSAGE_CHILDREN);out[name]=dict(exit_code=p.returncode,cpu_seconds=u.ru_utime+u.ru_stime-before.ru_utime-before.ru_stime,seconds=time.monotonic()-t,cumulative_children_peak_rss_kib=u.ru_maxrss,address_limit_mib=mem,cpu_limit=cpu);print(name,out[name],flush=True);assert p.returncode==0
out['physical']['measured_process_peak_rss_kib']=json.loads((H/'independent_result.json').read_text())['peak_rss_kib']
(H/'resources.json').write_text(json.dumps(out,indent=2)+'\n')
