from pathlib import Path
import os,resource,subprocess,json,time,sys,hashlib
P=Path(__file__).resolve().parent
start=time.monotonic()
shape=json.loads((P/'snapshot/producer/physical_result.json').read_text())['geometry'];tag='x'.join(map(str,shape))
engine=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else P/'independent_residual'
def limits():
 os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
with (P/'independent_run.log').open('w') as log:
 p=subprocess.run([str(engine),str(P/f'snapshot/geometry_{tag}.txt'),str(P/'snapshot/producer/coefficients.txt'),str(P/'independent_result.json'),'origin'],stdout=log,stderr=subprocess.STDOUT,preexec_fn=limits,timeout=55)
u=resource.getrusage(resource.RUSAGE_CHILDREN);r=dict(exit_code=p.returncode,seconds=time.monotonic()-start,cpu_seconds=u.ru_utime+u.ru_stime,peak_rss_kib=u.ru_maxrss,cpu_affinity=[4],address_space_limit_mib=250,cpu_seconds_limit=40,engine_sha256=hashlib.sha256(engine.read_bytes()).hexdigest())
(P/'independent_resources.json').write_text(json.dumps(r,indent=2)+'\n');print(r);assert p.returncode==0
