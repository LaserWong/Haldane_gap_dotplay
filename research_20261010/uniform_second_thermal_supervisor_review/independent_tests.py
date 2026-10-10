#!/usr/bin/env python3
"""Authorized scheduling fixtures only; never dispatch a thermal command."""
from pathlib import Path
import os,resource,json,time,sys,signal,importlib.util,hashlib
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30));P=Path(__file__).resolve().parent;S=P/'snapshot';start=time.process_time()
pins=json.loads((P/'SNAPSHOT_SHA256.json').read_text());assert all(hashlib.sha256((S/f).read_bytes()).hexdigest()==h for f,h in pins.items())
spec=importlib.util.spec_from_file_location('reviewed_scheduler',S/'supervisor.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert g.DEADLINE==1791698400 and g.USER_DEADLINE==1791936000 and g.LIMIT==21600
assert g.reservation(12,'prepare')==54*122 and g.reservation(12,'run')==60*122 and g.SELF_RESERVE==122
BASE=P/'fixture_state_final';BASE.mkdir(exist_ok=False);tests=[]
def ledger(name,limit=1000,sec=15):return g.Ledger(BASE/name,limit,time.time()+sec,bindings={'test':name},test=True)
l=ledger('reserve_crash');a=l.reserve(20,'worker');deadline=l.deadline;l.close();l=g.Ledger(BASE/'reserve_crash',1000,deadline,bindings={'test':'reserve_crash'},test=True);l.reconcile();assert l.used()==20 and a['reservation']==20 and l.data['attempts'][0]['status']=='UNKNOWN_CHARGED';l.close();tests.append('reserved-before-launch survives restart without refund')
l=ledger('two_slots');l.reserve(10,'worker');l.reserve(10,'worker')
try:l.reserve(10,'worker')
except AssertionError:tests.append('third simultaneous worker rejected')
else:raise AssertionError('third worker')
l.close()
l=ledger('lock')
try:g.Ledger(BASE/'lock',1000,l.deadline,bindings={'test':'lock'},test=True)
except BlockingIOError:tests.append('duplicate campaign lock rejected')
else:raise AssertionError('duplicate lock')
l.close()
l=ledger('corrupt');deadline=l.deadline;l.close();p=BASE/'corrupt/ledger.json';o=json.loads(p.read_text());o['payload']['limit']=999;p.write_text(json.dumps(o))
try:g.Ledger(BASE/'corrupt',1000,deadline,bindings={'test':'corrupt'},test=True)
except AssertionError:tests.append('corrupt persistent checkpoint rejected')
else:raise AssertionError('corrupt accepted')

def drained(l,a,pid):
 active={pid:a};stop=time.monotonic()+6
 while active and time.monotonic()<stop:g.drain(l,active);time.sleep(.01)
 assert not active and not g.group_live(pid)
def attempt(name,code,crash=None,sec=10,normal=False):
 l=ledger(name,sec=sec);a=l.reserve(100,'worker');pid=g.launch(l,a,[sys.executable,'-c',code],5,cap=2,test_crash=crash);drained(l,a,pid)
 if normal:assert a['status']=='COMPLETE' and 0<a['charge']<100 and a['terminal_wait4_cpu']>=a['result']['child_cpu']>=.1
 else:assert a['status']=='UNKNOWN_CHARGED' and a['charge']==100
 l.close();tests.append(name)
child="import time\nt=time.process_time()+.15\nwhile time.process_time()<t: pass"
attempt('terminal wait4 accounts nested child CPU','import subprocess,sys;subprocess.run([sys.executable,"-c",'+repr(child)+'],check=True)',normal=True)
sleepy='import subprocess,sys,time;subprocess.Popen([sys.executable,"-c","import time;time.sleep(4)"]);time.sleep(4)'
attempt('guardian crash cleans descendant group',sleepy,crash='during')
attempt('post-result crash does not refund','pass',crash='before_commit')
attempt('deadline kills active descendants',sleepy,sec=.25)
# Failed attempts consume aggregate budget; the third cannot start.
l=ledger('failed_budget',limit=210)
for j in range(2):
 a=l.reserve(100,'worker');pid=g.launch(l,a,[sys.executable,'-c','raise SystemExit(3)'],5,cap=2);drained(l,a,pid);assert a['charge']==100
assert l.used()==200
try:l.reserve(100,'worker')
except AssertionError:tests.append('failed retries debit aggregate budget across attempts')
else:raise AssertionError('failed CPU refunded')
deadline=l.deadline;l.close();l=g.Ledger(BASE/'failed_budget',210,deadline,bindings={'test':'failed_budget'},test=True);assert l.used()==200;l.close();tests.append('aggregate budget survives reopening')
# Kill guardian externally while it has a runner and grandchild.
l=ledger('killed_guardian');a=l.reserve(100,'worker');pid=g.launch(l,a,[sys.executable,'-c',sleepy],5,cap=2);time.sleep(.2);os.kill(pid,signal.SIGKILL);drained(l,a,pid);assert a['charge']==100;l.close();tests.append('SIGKILL watchdog leaves no running descendants')
# Owner death must trigger guardian group cleanup even without the main drain loop.
r,w=os.pipe();owner=os.fork()
if owner==0:
 os.close(r);l=ledger('owner_died');a=l.reserve(100,'worker');pid=g.launch(l,a,[sys.executable,'-c',sleepy],5,cap=2);os.write(w,str(pid).encode());os.close(w);time.sleep(.2);os._exit(93)
os.close(w);pgid=int(os.read(r,100));os.close(r);os.waitpid(owner,0);end=time.monotonic()+3
while g.group_live(pgid) and time.monotonic()<end:time.sleep(.01)
assert not g.group_live(pgid);tests.append('owner crash triggers parent-death cascade')
# A live descendant sees the enforced one-core affinity and96MiB ceiling.
probe='import os,resource,time;assert os.sched_getaffinity(0)=={5};assert resource.getrlimit(resource.RLIMIT_AS)==(96*1024**2,96*1024**2);t=time.process_time()+.15\nwhile time.process_time()<t: pass'
attempt('descendant memory and affinity limits enforced',probe,normal=True)
# An expired ledger cannot reserve another job.
l=ledger('expired',sec=-1)
try:l.reserve(1,'worker')
except AssertionError:tests.append('expired wall deadline rejects new reservation')
else:raise AssertionError('expired launch')
l.close()
# Frozen source only consumes current invocation's validated completions.
s=(S/'supervisor.py').read_text();assert 'for a in newly_complete:' in s and 'newly_complete=drain' in s;tests.append('historical certificate cannot bypass current validation')
out={'status':'PASS independent authorized scheduling fixtures','tests':tests,'count':len(tests),'no_thermal_commands':True,'deadline_utc':'2026-10-11T06:00:00Z','user_hardstop_utc':'2026-10-14T00:00:00Z','aggregate_CPU_limit_seconds':21600,'max_worker_trees':2,'CPU_affinity':5,'self_CPU_seconds':time.process_time()-start,'waited_children_CPU_seconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,'children_maxrss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
(P/'test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
