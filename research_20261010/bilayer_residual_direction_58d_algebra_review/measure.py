import json,resource,subprocess,sys,os,time
out,mem,cap,*cmd=sys.argv[1:];os.sched_setaffinity(0,{4})
def limit():
 resource.setrlimit(resource.RLIMIT_AS,(int(mem)*1024**2,)*2);resource.setrlimit(resource.RLIMIT_CPU,(int(cap),)*2)
t=time.monotonic();p=subprocess.run(cmd,preexec_fn=limit);r=resource.getrusage(resource.RUSAGE_CHILDREN)
open(out,'w').write(json.dumps(dict(command=cmd,exit_code=p.returncode,cpu_seconds=r.ru_utime+r.ru_stime,peak_rss_kib=r.ru_maxrss,wall_seconds=time.monotonic()-t),indent=2)+'\n');assert p.returncode==0
