#!/usr/bin/env python3
"""Durable conservative scheduler. Definition is not launch authorization."""
import os,sys,json,hashlib,time,math,signal,resource,fcntl,argparse,uuid,ctypes
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent;RUNNER=P.parent/'uniform_second_thermal_campaign_gate';USER_DEADLINE=1791936000;DEADLINE=1791698400 # campaign2026-10-11T06:00:00Z
assert datetime.fromtimestamp(USER_DEADLINE,timezone.utc).isoformat()=='2026-10-14T00:00:00+00:00'
assert datetime.fromtimestamp(DEADLINE,timezone.utc).isoformat()=='2026-10-11T06:00:00+00:00' and DEADLINE<USER_DEADLINE
LIMIT=43200;CPU_CAP=35;BATCHES=8;SELF_RESERVE=122;INTERNAL_ALLOWANCE=600;METADATA_CAP=5
CANONICAL=Path("/workspace/shared/haldane_active/research_20261010/uniform_second_thermal_campaign_run")
OLD_TERMINAL_SHA="9a6b8fe6944c06544247c07b04344e2258784cbfc722f902b3cc2b979d57f288"
AUTHORIZATION_ID="root-20261011-cap-extension-21600-to-43200"
assert INTERNAL_ALLOWANCE>BATCHES*(CPU_CAP+2)+(CPU_CAP+2)+120+2

def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def atomic(path,obj):
 tmp=path.with_name(path.name+'.tmp-'+str(os.getpid()));raw=json.dumps({'payload':obj,'sha256':digest(obj)},indent=2)+'\n'
 with open(tmp,'x') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path);fd=os.open(path.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
def read(path):
 o=json.loads(path.read_text());assert set(o)=={'payload','sha256'} and o['sha256']==digest(o['payload']);return o['payload']
def stamp(pid):
 try:
  raw=Path(f'/proc/{pid}/stat').read_text();rest=raw[raw.rfind(')')+2:].split();return {'pid':pid,'start_ticks':int(rest[19]),'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
 except FileNotFoundError:return None
def alive(identity):return identity is not None and stamp(identity['pid'])==identity

def sources():
 files=[P/'supervisor.py',P/'hooks/sitecustomize.py',RUNNER/'campaign.py',RUNNER/'kernel',RUNNER/'kernel.cpp',RUNNER/'coefficients.txt',RUNNER/'MANIFEST_SHA256.json'];return {str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}

def reservation(n,action,max_batches=BATCHES,cap=CPU_CAP):
 assert action in ('prepare','run','validate')
 metadata=4*(n+1) if action=='prepare' else 2*(n+1)
 compute=max_batches if action=='run' else 0
 return metadata*(METADATA_CAP+2)+(compute+2)*(cap+2)

class Ledger:
 def __init__(self,folder,limit=LIMIT,deadline=DEADLINE,bindings=None,test=False):
  self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
  if not test:assert self.folder.resolve()==CANONICAL,'sole authorized ledger path required'
  self.lock=open(self.folder/'campaign.lock','a+');fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB);self.path=self.folder/'ledger.json';self.limit=limit;self.deadline=deadline
  expected=bindings if bindings is not None else sources()
  if test and not self.path.exists():
   self.data={'version':1,'limit':limit,'deadline':deadline,'bindings':expected,'test_mode':True,'attempts':[],'events':[],'terminal_state':'READY'};self.save()
  else:
   self.data=read(self.path)
   if self.data['limit']==21600:
    assert not test,'use extend_fixture explicitly for historical ledger test'
    self.extend(expected)
   else:
    assert self.data['limit']==limit and self.data['deadline']==deadline
    if not test:
     assert self.data['active_extension_bindings']==expected
     assert self.data['extensions'][-1]['authorization_id']==AUTHORIZATION_ID
     self.validate_prefix()
    else:assert self.data['bindings']==expected and self.data['test_mode']
  self.validate()
  if not test:assert self.data['terminal_state'] in ('EXTENSION_READY','RUNNING'),'terminal campaign cannot automatically restart'
 def extend(self,new_bindings):
  assert time.time()<DEADLINE,'extension deadline reached before any write'
  oldraw=self.path.read_bytes();assert hashlib.sha256(oldraw).hexdigest()==OLD_TERMINAL_SHA,'old terminal ledger changed'
  old=self.data;assert old['limit']==21600 and old['deadline']==DEADLINE and old['terminal_state']=='BUDGET_RESERVATION_EXHAUSTED' and sum(a['charge'] for a in old['attempts'])==16207
  assert not any(a['status'] in ('ACTIVE','RESERVED') for a in old['attempts'])
  history=self.folder/'history';history.mkdir(exist_ok=True);snap=history/('original_terminal_'+OLD_TERMINAL_SHA+'.json')
  if snap.exists():assert snap.read_bytes()==oldraw
  else:
   fd=os.open(snap,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.write(fd,oldraw);os.fsync(fd);os.close(fd);hd=os.open(history,os.O_DIRECTORY);os.fsync(hd);os.close(hd)
  event={'authorization_id':AUTHORIZATION_ID,'old_limit':21600,'additional_budget':21600,'new_limit':43200,'retained_charge':16207,'old_terminal_state':old['terminal_state'],'original_terminal_sha256':OLD_TERMINAL_SHA,'original_attempt_count':len(old['attempts']),'original_attempts_sha256':digest(old['attempts']),'original_bindings_sha256':digest(old['bindings']),'new_bindings':new_bindings,'deadline':DEADLINE,'recorded_utc':time.time()}
  old['extensions']=[event];old['active_extension_bindings']=new_bindings;old['limit']=43200;old['terminal_state']='EXTENSION_READY';self.data=old;self.save();self.validate_prefix()
 def validate_prefix(self):
  assert len(self.data['extensions'])==1
  event=self.data['extensions'][0]
  assert event['authorization_id']==AUTHORIZATION_ID and event['original_terminal_sha256']==OLD_TERMINAL_SHA
  assert (event['old_limit'],event['additional_budget'],event['new_limit'],event['retained_charge'],event['deadline'])==(21600,21600,43200,16207,DEADLINE)
  assert event['old_terminal_state']=='BUDGET_RESERVATION_EXHAUSTED'
  assert event['new_bindings']==self.data['active_extension_bindings'] and self.data['limit']==43200 and self.data['deadline']==DEADLINE
  assert 0<event['recorded_utc']<DEADLINE
  snap=self.folder/'history'/('original_terminal_'+event['original_terminal_sha256']+'.json');raw=snap.read_bytes();assert hashlib.sha256(raw).hexdigest()==event['original_terminal_sha256'];old=read(snap);count=event['original_attempt_count']
  assert self.data['attempts'][:count]==old['attempts'] and self.data['bindings']==old['bindings']
  assert event['original_bindings_sha256']==digest(old['bindings']) and old['test_mode'] is False and self.data['test_mode'] is False
  assert digest(self.data['attempts'][:count])==event['original_attempts_sha256'] and old['limit']==21600 and sum(a['charge'] for a in old['attempts'])==16207

 def save(self):atomic(self.path,self.data)
 def validate(self):
  ids=[a['id'] for a in self.data['attempts']];assert len(ids)==len(set(ids));assert self.used()<=self.limit
  for a in self.data['attempts']:assert 0<=a['charge']<=a['reservation'] and a['status'] in ('RESERVED','ACTIVE','COMPLETE','UNKNOWN_CHARGED','OVERHEAD','DEADLINE_CHARGED')
 def used(self):return sum(a['charge'] for a in self.data['attempts'])
 def reserve(self,amount,kind,details=None):
  assert time.time()<self.deadline,'deadline reached';assert amount>0 and self.used()+amount<=self.limit,'aggregate budget exhausted'
  if kind=='worker':assert sum(a['status'] in ('RESERVED','ACTIVE') and a['kind']=='worker' for a in self.data['attempts'])<2,'two-worker limit'
  a={'id':uuid.uuid4().hex,'kind':kind,'details':details or {},'reservation':amount,'charge':amount,'status':'RESERVED','reserved_utc':time.time(),'identity':None};self.data['attempts'].append(a);self.save();return a
 def activate(self,a,identity):a['identity']=identity;a['status']='ACTIVE';self.save()
 def reconcile(self):
  # An interrupted parent never refunds an unknown attempt, even if a result file exists.
  for a in self.data['attempts']:
   if a['status'] not in ('ACTIVE','RESERVED'):continue
   assert not alive(a['identity']),'duplicate live campaign attempt; wait for watchdog cleanup'
   a['status']='UNKNOWN_CHARGED';a['charge']=a['reservation'];a['reconciled_utc']=time.time()
  self.save()
 def complete(self,a,result,terminal_cpu):
  assert a['status']=='ACTIVE';assert result['attempt_id']==a['id'] and result['identity']==a['identity'];assert result['verified_wait4'] and result['runner_reaped'];assert result['child_cpu']>=0 and result['watchdog_cpu']>=0
  # Parent wait4 occurs after watchdog exit and includes its waited descendants.
  assert terminal_cpu>=result['child_cpu'] and terminal_cpu<=a['reservation']
  charged=min(a['reservation'],math.ceil(terminal_cpu)+2)
  assert result['child_cpu']+result['watchdog_cpu']<=a['reservation'],'measured usage exceeds analytical cap'
  a.update(status='COMPLETE',charge=charged,result=result,terminal_wait4_cpu=terminal_cpu,completed_utc=time.time());self.save()
 def close(self):self.lock.close()

def guardian(command,gate_fd,result_path,attempt_id,parent_identity,cpu,deadline,cap=CPU_CAP,test_crash=None):
 """One process group; watchdog remains able to kill its runner and descendants."""
 os.setsid();os.sched_setaffinity(0,{cpu});resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));identity=stamp(os.getpid())
 def stop(signum=None,frame=None):
  try:os.killpg(os.getpgrp(),signal.SIGKILL)
  finally:os._exit(137)
 signal.signal(signal.SIGALRM,stop);signal.signal(signal.SIGTERM,stop)
 if ctypes.CDLL(None,use_errno=True).prctl(1,signal.SIGTERM,0,0,0)!=0:os._exit(98)
 if os.getppid()!=parent_identity['pid']:stop()
 signal.setitimer(signal.ITIMER_REAL,max(.001,deadline-time.time()))
 if os.read(gate_fd,1)!=b'G':os._exit(125)
 os.close(gate_fd)
 child=os.fork()
 if child==0:
  signal.signal(signal.SIGALRM,signal.SIG_DFL);signal.setitimer(signal.ITIMER_REAL,max(.001,deadline-time.time()))
  if ctypes.CDLL(None,use_errno=True).prctl(1,signal.SIGKILL,0,0,0)!=0:os._exit(98)
  if os.getppid()!=identity['pid']:os._exit(97)
  resource.setrlimit(resource.RLIMIT_AS,(96*1024**2,96*1024**2))
  os.environ['PYTHONPATH']=str(P/'hooks');os.environ['HALDANE_CAMPAIGN_DEADLINE']=str(deadline)
  resource.setrlimit(resource.RLIMIT_CPU,(cap,cap))
  # Runner uses the same process group and one CPU. All its children inherit it.
  logfd=os.open(result_path.with_suffix('.log'),os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600);os.dup2(logfd,1);os.dup2(logfd,2);os.close(logfd)
  os.execv(command[0],command)
 if test_crash=='during':time.sleep(.1);os._exit(91)
 while True:
  if time.time()>=deadline or not alive(parent_identity):stop()
  pid,status,usage=os.wait4(child,os.WNOHANG)
  if pid:break
  time.sleep(.05)
 # The frozen runner waits every ordinary child. Kill remaining group members if it failed.
 # Killing them conservatively prevents an unaccounted orphan; failed status retains full reservation.
 if not os.WIFEXITED(status) or os.WEXITSTATUS(status)!=0:stop()
 own=resource.getrusage(resource.RUSAGE_SELF)
 result={'attempt_id':attempt_id,'identity':identity,'runner_reaped':True,'verified_wait4':True,'wait_status':status,'child_cpu':usage.ru_utime+usage.ru_stime,'watchdog_cpu':own.ru_utime+own.ru_stime,'maxrss_kib':usage.ru_maxrss,'finished_utc':time.time()}
 atomic(result_path,result)
 if test_crash=='before_commit':os._exit(92)
 os._exit(0)

def launch(ledger,a,command,cpu,cap=CPU_CAP,test_crash=None):
 r,w=os.pipe();parent=stamp(os.getpid());pid=os.fork()
 if pid==0:
  os.close(w)
  try:guardian(command,r,ledger.folder/(a['id']+'.completion.json'),a['id'],parent,cpu,ledger.deadline,cap,test_crash)
  except BaseException:
   try:os.killpg(os.getpgrp(),signal.SIGKILL)
   finally:os._exit(99)
 os.close(r)
 # Child waits on gate; no runner starts until pid identity is durably committed.
 identity=stamp(pid);assert identity;ledger.activate(a,identity);os.write(w,b'G');os.close(w);return pid

def group_live(pgid):
 for f in Path('/proc').glob('[0-9]*/stat'):
  try:
   raw=f.read_text();fields=raw[raw.rfind(')')+2:].split()
   if int(fields[2])==pgid and fields[0]!='Z':return True
  except (FileNotFoundError,ProcessLookupError):pass
 return False

def drain(ledger,active,block=False):
 completed=[]
 for pid,a in list(active.items()):
  got,status,usage=os.wait4(pid,0 if block else os.WNOHANG)
  if not got:continue
  # Parent-death hooks kill descendants; also enforce group cleanup before slot reuse.
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  end=time.monotonic()+5
  while group_live(pid) and time.monotonic()<end:time.sleep(.01)
  assert not group_live(pid),'process-group cleanup incomplete; no slot reuse'
  result=ledger.folder/(a['id']+'.completion.json')
  if os.WIFEXITED(status) and os.WEXITSTATUS(status)==0 and result.exists():ledger.complete(a,read(result),usage.ru_utime+usage.ru_stime);completed.append(a)
  else:
   # No trusted complete measurement: full original charge retained.
   a['status']='UNKNOWN_CHARGED';a['charge']=a['reservation'];a['wait_status']=status;ledger.save()
  del active[pid]
 return completed

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--state-dir',type=Path,required=True);ap.add_argument('--launch',action='store_true');args=ap.parse_args();assert args.launch,'explicit --launch required; root authorization is external'
 os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));led=Ledger(args.state_dir);led.reconcile();overhead=led.reserve(SELF_RESERVE,'supervisor');overhead['status']='OVERHEAD';led.data['terminal_state']='RUNNING';led.save();active={};cases=[(n,t) for n in range(4,13) for t in ('I','P')];state_root=args.state_dir.resolve()/'cases';state_root.mkdir(exist_ok=True)
 def terminate(signum=None,frame=None):
  for pid,a in active.items():
   if alive(a['identity']):
    try:os.killpg(pid,signal.SIGKILL)
    except ProcessLookupError:pass
   a['status']='DEADLINE_CHARGED';a['charge']=a['reservation']
  led.data['terminal_state']='DEADLINE_OR_SIGNAL_STOP';led.save();os._exit(128+(signum or 0))
 signal.signal(signal.SIGALRM,terminate);signal.signal(signal.SIGTERM,terminate);signal.signal(signal.SIGINT,terminate);signal.setitimer(signal.ITIMER_REAL,max(.001,DEADLINE-time.time()))
 completed=set()
 # Existing completion markers require a bounded validate attempt, never blind trust.
 for n,t in cases:
  folder=state_root/f'L{n}_{t}'
  if (folder/'certificate.json').exists():pass
 while True:
  newly_complete=drain(led,active)
  if time.time()>=DEADLINE:terminate()
  busy={(a['details']['n'],a['details']['twist']) for a in active.values()}
  for a in newly_complete:
   if a['status']=='COMPLETE' and a['kind']=='worker' and a['details']['action'] in ('run','validate'):
    key=(a['details']['n'],a['details']['twist']);folder=state_root/f'L{key[0]}_{key[1]}'
    if (folder/'certificate.json').exists():completed.add(key)
  if len(completed)==len(cases) and not active:led.data['terminal_state']='ALL_CASES_COMPLETE_PRODUCER_REVIEW_REQUIRED';led.save();break
  launched=False
  for n,t in cases:
   if len(active)>=2:break
   if (n,t) in busy or (n,t) in completed:continue
   folder=state_root/f'L{n}_{t}';action='prepare' if not (folder/'case.json').exists() else ('validate' if (folder/'certificate.json').exists() else 'run');amount=reservation(n,action)
   if led.used()+amount>LIMIT:continue
   occupied={a['details']['cpu'] for a in active.values()};cpu=next(c for c in (0,1) if c not in occupied)
   details={'n':n,'twist':t,'action':action,'cpu':cpu,'max_new_batches':BATCHES};attempt=led.reserve(amount,'worker',details)
   cmd=[sys.executable,str(RUNNER/'campaign.py'),'--action',action,'--length',str(n),'--twist',t,'--output',str(folder),'--batch-size','16','--max-new-batches',str(BATCHES),'--cpu',str(cpu),'--cpu-budget',str(INTERNAL_ALLOWANCE)]
   # With at most8 compute children each<=35CPU and runner<=35, used<315.
   # Internal600 allowance therefore never shrinks a child's requested120 cap.
   # Private hook gives each complete compute child its full fixed35-second allowance.
   active[launch(led,attempt,cmd,cpu)]=attempt;launched=True
  if not active and not launched:led.data['terminal_state']='BUDGET_RESERVATION_EXHAUSTED';led.save();break
  time.sleep(.05)
 signal.setitimer(signal.ITIMER_REAL,0);print(json.dumps({'state':led.data['terminal_state'],'charged_cpu_seconds':led.used(),'limit':LIMIT}));led.close()
if __name__=='__main__':main()
