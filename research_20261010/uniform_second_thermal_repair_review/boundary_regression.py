#!/usr/bin/env python3
"""Independent scaled nonthermal reproduction of invocation-budget boundary."""
from pathlib import Path
import os,resource,subprocess,sys,json,time
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30))
work='import time\ns=time.process_time()\nwhile time.process_time()-s<1.3: pass\nprint("completed fixed batch",flush=True)'
def child(cap):
 def limits():
  os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,64*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap))
 before=resource.getrusage(resource.RUSAGE_CHILDREN);r=subprocess.run([sys.executable,'-c',work],capture_output=True,text=True,preexec_fn=limits,timeout=5);after=resource.getrusage(resource.RUSAGE_CHILDREN)
 return {'cap_seconds':cap,'returncode':r.returncode,'CPU_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'stdout':r.stdout}
def loop(fixed):
 records=[];used=0;budget=5;guard=1
 for _ in range(5):
  remaining=int(budget-used)-guard
  if remaining<1:return {'records':records,'yielded':True,'used':used,'remaining':remaining}
  if fixed and remaining<2:return {'records':records,'yielded':True,'used':used,'remaining':remaining}
  cap=2 if fixed else min(120,remaining)
  r=child(cap);records.append(r);used+=r['CPU_seconds']
  if r['returncode']!=0:return {'records':records,'yielded':False,'used':used,'remaining':remaining}
 raise AssertionError('unbounded fixture')
old=loop(False);new=loop(True)
assert len(old['records'])==3 and [r['returncode'] for r in old['records']]==[0,0,-9] and old['records'][-1]['cap_seconds']==1
assert new['yielded'] and len(new['records'])==2 and all(r['returncode']==0 and r['cap_seconds']==2 for r in new['records']) and new['remaining']<2
out={'status':'PASS independent actual-process boundary regression','old_shrinking_allowance':old,'fixed_allowance_graceful_yield':new,'no_thermal_commands':True,'CPU_affinity':5,'total_waited_child_CPU_seconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime}
(P/'boundary_regression_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
