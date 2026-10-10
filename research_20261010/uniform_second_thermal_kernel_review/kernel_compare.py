#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,hashlib,resource,os,time
P=Path(__file__).resolve().parent;A=P.with_name('uniform_second_thermal_pilot');os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
manifest=A/'MANIFEST_SHA256.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='0b5ffdc303cd506a2946308c3ce33e7327e38eac6dae9a92413937fe735f0185'
for name,h in json.loads(manifest.read_text()).items():assert hashlib.sha256((A/name).read_bytes()).hexdigest()==h
for name in ['stream_second.cpp','coefficients.txt']:(P/name).write_bytes((A/name).read_bytes())
r=subprocess.run(['g++','-O2','-std=c++17',str(P/'stream_second.cpp'),'-lgmpxx','-lgmp','-o',str(P/'reviewed_kernel')],capture_output=True,text=True,timeout=90);assert r.returncode==0,r.stderr
# The sole authorized kernel invocation: all M=0 L5 twisted representatives.
st=time.process_time();r=subprocess.run([str(P/'reviewed_kernel'),'5','P','full','0','0','100000',str(P/'coefficients.txt'),'compute'],capture_output=True,text=True,timeout=30);assert r.returncode==0,r.stderr
rows=[tuple(map(int,line.split())) for line in r.stdout.splitlines()];fixtures=json.loads((P/'fixture_results.json').read_text());want=[(v['code'],v['multiplicity'],int(v['norm_squared'])) for v in fixtures['records'] if (v['n'],v['twist'],v['weight'])==(5,'P',0)];assert rows==want
(P/'kernel_stdout.txt').write_text(r.stdout);(P/'kernel_stderr.txt').write_text(r.stderr)
result={'status':'PASS','invocations':1,'case':'L5 P M0 full representatives','records_exactly_matched':len(rows),'source_sha256':hashlib.sha256((P/'stream_second.cpp').read_bytes()).hexdigest(),'binary_sha256':hashlib.sha256((P/'reviewed_kernel').read_bytes()).hexdigest(),'coefficient_sha256':hashlib.sha256((P/'coefficients.txt').read_bytes()).hexdigest(),'maxrss_children_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'CPU_children_seconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,'hard_memory_MiB':256,'CPU_affinity':5}
(P/'kernel_comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
