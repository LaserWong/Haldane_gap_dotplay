#!/usr/bin/env python3
"""Bounded scheduling fault tests; only trivial Python fixtures, no thermal jobs."""
import os,sys,time,json,resource,importlib.util,signal
from pathlib import Path
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
spec=importlib.util.spec_from_file_location('supervisor',P/'supervisor.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);base=P/'test_states_seal';base.mkdir(exist_ok=True);tests=[]
def ledger(name,limit=1000,seconds=20):return s.Ledger(base/name,limit,time.time()+seconds,bindings={'fixture':name},test=True)
def deadgroup(pid):
 for _ in range(100):
  active=[]
  for f in Path('/proc').glob('[0-9]*/stat'):
   try:
    r=f.read_text();a=r[r.rfind(')')+2:].split()
    if int(a[2])==pid and a[0]!='Z':active.append(int(f.parent.name))
   except (FileNotFoundError,ProcessLookupError):pass
  if not active:return True
  time.sleep(.01)
 return False
# Reserved attempt survives crash before launch without refund.
l=ledger('after_reserve');a=l.reserve(20,'worker');deadline=l.deadline;l.close();l=s.Ledger(base/'after_reserve',1000,deadline,bindings={'fixture':'after_reserve'},test=True);l.reconcile();assert l.used()==20 and l.data['attempts'][0]['status']=='UNKNOWN_CHARGED';l.close();tests.append('crash after reserve retains full charge')
l=ledger('exhausted',limit=5);l.reserve(3,'worker')
try:l.reserve(3,'worker')
except AssertionError:pass
else:raise AssertionError('budget overflow')
l.close();tests.append('aggregate budget exhaustion rejects launch')
l=ledger('duplicate')
try:s.Ledger(base/'duplicate',1000,l.deadline,bindings={'fixture':'duplicate'},test=True)
except BlockingIOError:pass
else:raise AssertionError('second campaign lock accepted')
l.close();tests.append('duplicate active campaign lock rejected')
l=ledger('slots');l.reserve(10,'worker');l.reserve(10,'worker')
try:l.reserve(10,'worker')
except AssertionError:pass
else:raise AssertionError('third worker accepted')
l.close();tests.append('third worker reservation rejected')

def fixture(name,code,crash=None,deadline_seconds=15,expect_normal=False):
 l=ledger(name,seconds=deadline_seconds);a=l.reserve(100,'worker',{'fixture':name});pid=s.launch(l,a,[sys.executable,'-c',code],0,cap=2,test_crash=crash);active={pid:a};finish=time.time()+10
 while active and time.time()<finish:s.drain(l,active);time.sleep(.02)
 assert not active and deadgroup(pid),'unreaped/running process group'
 if expect_normal:assert a['status']=='COMPLETE' and a['charge']<100 and a['terminal_wait4_cpu']>=a['result']['child_cpu']>=.2
 else:assert a['status']=='UNKNOWN_CHARGED' and a['charge']==100
 l.close();tests.append(name)
fixture('normal durable completion refund','import subprocess,sys; subprocess.run([sys.executable,"-c",\'import time\\nend=time.process_time()+.2\\nwhile time.process_time()<end: pass\'],check=True)',expect_normal=True)
fixture('crash during child retains charge','import time; time.sleep(4)',crash='during')
fixture('crash before ledger commit retains charge','pass',crash='before_commit')
fixture('failed metadata attempt charged','raise SystemExit(3)')
fixture('deadline kills full process group','import subprocess,sys,time; subprocess.Popen([sys.executable,"-c","import time;time.sleep(8)"]);time.sleep(8)',deadline_seconds=.35)
# Guardian SIGKILL while runner/grandchild active: parent-death cascade plus drain cleanup.
l=ledger('watchdog_killed');a=l.reserve(100,'worker');pid=s.launch(l,a,[sys.executable,'-c','import subprocess,sys,time; subprocess.Popen([sys.executable,"-c","import time;time.sleep(8)"]);time.sleep(8)'],0,cap=2);time.sleep(.3);os.kill(pid,signal.SIGKILL);active={pid:a}
while active:s.drain(l,active);time.sleep(.01)
assert deadgroup(pid) and a['charge']==100;l.close();tests.append('watchdog killed leaves no live descendants')
# Ancestor crash: separate owner exits, guardian parent-death handler kills its group.
ready_r,ready_w=os.pipe();owner=os.fork()
if owner==0:
 os.close(ready_r);ll=ledger('supervisor_crash');aa=ll.reserve(100,'worker');gp=s.launch(ll,aa,[sys.executable,'-c','import subprocess,sys,time;subprocess.Popen([sys.executable,"-c","import time;time.sleep(8)"]);time.sleep(8)'],0,cap=2);os.write(ready_w,str(gp).encode());time.sleep(.3);os._exit(93)
os.close(ready_w);gp=int(os.read(ready_r,100));os.close(ready_r);os.waitpid(owner,0);assert deadgroup(gp);tests.append('supervisor crash parent-death cleanup')
# Terminal state and changed identity cannot reset/restart the ledger.
l=ledger('terminal');l.data['terminal_state']='BUDGET_RESERVATION_EXHAUSTED';l.save();dd=l.deadline;l.close()
try:s.Ledger(base/'terminal',1000,dd,bindings={'fixture':'different'},test=True)
except AssertionError:tests.append('source identity change rejected')
else:raise AssertionError('changed identity accepted')
# No thermal commands were dispatched.
out={'status':'PASS scheduling-only fixtures','tests':tests,'count':len(tests),'no_thermal_jobs':True,'campaign_deadline_utc':'2026-10-11T06:00:00Z','user_deadline_utc':'2026-10-14T00:00:00Z','reserve_rule':'122 CPU seconds per120-second-limited possible process','supervisor_source_sha256':s.sources()[str(P/'supervisor.py')],'resources':{'self_cpu':resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,'children_cpu':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,'maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}}
(P/'tests.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
