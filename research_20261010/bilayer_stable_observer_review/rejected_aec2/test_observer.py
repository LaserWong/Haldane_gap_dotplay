import os,sys,time,signal,resource,ctypes,json,copy
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import limit_observer as obs
from engine import atomic,ControlBudget,IncrementalJob
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(8,8));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2))
config=dict(python=sys.executable,native='/usr/bin/sleep',scripts=dict(outer='/fixture/outer.py',supervisor='/fixture/supervisor.py',controller=str(Path(__file__).resolve())))
assert obs.topology_role(10,10,{10:{'ppid':1}})=='supervisor'
assert obs.topology_role(11,10,{10:{'ppid':1},11:{'ppid':10}})=='controller'
assert obs.topology_role(12,10,{10:{'ppid':1},11:{'ppid':10},12:{'ppid':11}})=='native'
results=[]
for label,cpu,as_mb in [('good',3,128),('bad_cpu',2,128),('bad_as',3,96)]:
 parentread,childwrite=os.pipe();childread,parentwrite=os.pipe();owner=os.getpid();pid=os.fork()
 if pid==0:
  assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
  if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
  os.close(parentread);os.close(parentwrite);os.write(childwrite,b'B');assert os.read(childread,1)==b'S'
  resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu));resource.setrlimit(resource.RLIMIT_AS,(as_mb*1024**2,as_mb*1024**2));os.write(childwrite,b'L');assert os.read(childread,1)==b'E'
  os.execv('/usr/bin/sleep',['/usr/bin/sleep','5'])
 os.close(childread);os.close(childwrite);assert os.read(parentread,1)==b'B'
 before=obs.sample(pid,'native',config);assert before['outcome']=='fork_before_exec';obs.enforce(before,P/'events'/label)
 os.write(parentwrite,b'S');assert os.read(parentread,1)==b'L';changed=obs.sample(pid,'native',config);assert changed['outcome']=='fork_before_exec';obs.enforce(changed,P/'events'/label)
 assert changed['cpu']==[cpu,cpu] and changed['address_space']==[as_mb*1024**2]*2
 os.write(parentwrite,b'E');until=time.monotonic()+2
 while True:
  record=obs.sample(pid,'native',config)
  if record['outcome'] in ('verified_post_exec','mismatch'):break
  obs.enforce(record,P/'events'/label);assert time.monotonic()<until;time.sleep(.005)
 rejected=False
 try:obs.enforce(record,P/'events'/label)
 except obs.LimitMismatch:rejected=True
 assert rejected==(label!='good')
 if label=='good':
  assert record['outcome']=='verified_post_exec' and record['after']['start']==before['after']['start']
  assert record['after']['exe']!=before['after']['exe']
  # Affinity fault is injected into an otherwise genuine stable observation;
  # no process is actually scheduled on an unauthorized CPU.
  affinity=copy.deepcopy(record);affinity['affinity']='7';obs.classify(affinity,config)
  try:obs.enforce(affinity,P/'events/bad_affinity');raise AssertionError('bad affinity survived')
  except obs.LimitMismatch:pass
  # Force a read-straddling-exec observation, with both identities retained.
  original_identity=obs.identity;calls=[0]
  def crossing(p):
   calls[0]+=1
   return before['before'] if calls[0]==1 else record['after']
  # Convert fixture serialized argv to the byte identity API.
  before_copy=copy.deepcopy(before['before']);before_copy['argv']=[x.encode() for x in before_copy['argv']]
  after_copy=copy.deepcopy(record['after']);after_copy['argv']=[x.encode() for x in after_copy['argv']]
  def crossing(p):
   calls[0]+=1;return before_copy if calls[0]==1 else after_copy
  obs.identity=crossing
  crossed=obs.sample(pid,'native',config);obs.identity=original_identity
  assert crossed['outcome']=='exec_or_identity_transition';obs.enforce(crossed,P/'events/crossing')
 os.kill(pid,signal.SIGKILL);w,st,u=os.wait4(pid,0);assert w==pid and os.waitstatus_to_exitcode(st)==-signal.SIGKILL
 os.close(parentread);os.close(parentwrite)
 # Every genuine mismatch was serialized before enforce raised.
 if rejected:
  saved=[json.loads(f.read_text()) for f in (P/'events'/label).glob('*.json')];assert any(x==record for x in saved)
 results.append(dict(case=label,before=before,after_limits=changed,post_exec=record,rejected=rejected,wait4_cpu=u.ru_utime+u.ru_stime,killed_reaped=True))
# Repartition and retired-reservation proof, without any scientific worker.
b=ControlBudget(P/'metadata_budget.json');assert b.state['prepaid']==1600
s=IncrementalJob(P/'metadata_store','NONPRODUCTION-RETIRED192-TEST','bilayer-moment24-v1','PHYSICAL-FIXED-WITNESS24');assert s.worker_charged==s.failed_charged==192 and s.pending_reserved==16800
r=s.reserve(0);assert r['forecast']==21600 and s.worker_charged==195
again=IncrementalJob(P/'metadata_store','NONPRODUCTION-RETIRED192-TEST','bilayer-moment24-v1','PHYSICAL-FIXED-WITNESS24');assert again.worker_charged==again.failed_charged==195
atomic(P/'TEST_RESULT.json',dict(cases=results,crossing_deferred=True,injected_affinity_rejected=True,topology_roles_pass=True,retired192_no_refund_pass=True,initial_forecast=21600,workers_dispatched=0,native_fixture_only='/usr/bin/sleep',self_cpu=time.process_time(),as_limits=list(resource.getrlimit(resource.RLIMIT_AS))))
