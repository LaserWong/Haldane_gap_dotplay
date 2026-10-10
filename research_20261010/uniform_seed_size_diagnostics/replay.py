#!/usr/bin/env python3
"""Replay exact data only. Floating proposals are never needed for certification."""
import os,resource,subprocess,json,hashlib,time
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
for name,digest in json.loads((P/'INPUT_MANIFEST_SHA256.json').read_text()).items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
subprocess.run(['g++','-O2',str(P/'mps_lengths.cpp'),'-lgmpxx','-lgmp','-o',str(P/'mps_lengths')],check=True)
t0=time.time();a=resource.getrusage(resource.RUSAGE_CHILDREN)
with (P/'mps_lengths.out').open('w') as f,(P/'mps_lengths.log').open('w') as g:
 subprocess.run([str(P/'mps_lengths'),str(ROOT/'audit/mps/mps_blocks.txt')],stdout=f,stderr=g,check=True)
b=resource.getrusage(resource.RUSAGE_CHILDREN)
(P/'mps_resources.json').write_text(json.dumps({'seconds':time.time()-t0,'cpu_seconds':b.ru_utime+b.ru_stime-a.ru_utime-a.ru_stime,'child_peak_kb_including_compiler':b.ru_maxrss,'cpu_affinity_count':1,'address_space_limit_bytes':1024**3},indent=2)+'\n')
for script,log in [('verify_trials.py','exact_trial_verify.log'),('verify_scalar.py','exact_scalar_verify.log')]:
 with (P/log).open('w') as f:subprocess.run(['python',str(P/script)],stdout=f,stderr=subprocess.STDOUT,check=True)
print((P/'exact_scalar_verify.log').read_text())
print((P/'mps_resources.json').read_text())
