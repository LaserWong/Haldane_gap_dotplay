from pathlib import Path
import subprocess,os,resource,time,json
P=Path(__file__).resolve().parent
st=time.monotonic();b=resource.getrusage(resource.RUSAGE_CHILDREN)
def limits():
 os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
r=subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra',str(P/'kernel.cpp'),'-lgmpxx','-lgmp','-o',str(P/'kernel')],capture_output=True,text=True,preexec_fn=limits);a=resource.getrusage(resource.RUSAGE_CHILDREN);(P/'compile.log').write_text(r.stdout+r.stderr);(P/'compile_resources.json').write_text(json.dumps({'returncode':r.returncode,'wall_seconds':time.monotonic()-st,'cpu_seconds':a.ru_utime+a.ru_stime-b.ru_utime-b.ru_stime,'maxrss_kib':a.ru_maxrss},indent=2));assert r.returncode==0
