"""Linear startup and constant-record incremental control. Synthetic benchmark only."""
import os,json,time,hashlib,math,tempfile
from pathlib import Path
SCHEMA='synthetic-metadata24-v1';KIND='SYNTHETIC-NONPHYSICAL-NOT-ADOPTABLE'

def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic(path,x):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix=path.name+'.tmp.',dir=path.parent)
 with os.fdopen(fd,'wb') as f:f.write(raw(x));f.flush();os.fsync(f.fileno())
 os.replace(tmp,path);fd=os.open(path.parent,os.O_DIRECTORY|os.O_RDONLY);os.fsync(fd);os.close(fd)
def read(path):return json.loads(Path(path).read_text())
def plan():
 rows=[]
 for q,N,w,cap in [(0,1,1,3),(2,496,64,3),(4,4495,16,3),(6,169911,64,6)]:
  for b in range(0,N,w):rows.append(dict(q=q,begin=b,end=min(b+w,N),N=N,cap=cap))
 assert len(rows)==2945 and sum(x['cap'] for x in rows)==16800
 return rows

class ControlBudget:
 def __init__(self,path):
  self.path=Path(path);self.state=read(path) if self.path.exists() else dict(prepaid=1200,reserved=0,sessions=[])
  self.validate()
 def validate(self):
  s=self.state;assert s['prepaid']==1200 and isinstance(s['reserved'],int) and s['reserved']>=0
  assert s['reserved']==sum(r['charged'] for r in s['sessions']) and s['reserved']<=1200
  assert [r['id'] for r in s['sessions']]==list(range(len(s['sessions'])))
  assert all(isinstance(r[k],int) and r[k]>0 for r in s['sessions'] for k in ['controller_cap','supervisor_cap','charged'])
  assert all(r['charged']==r['controller_cap']+r['supervisor_cap'] for r in s['sessions'])
  assert all(r.get('controller_cpu') is None or 0<=r['controller_cpu']<=r['controller_cap'] for r in s['sessions'])
  assert all(r.get('supervisor_cpu') is None or 0<=r['supervisor_cpu']<=r['supervisor_cap'] for r in s['sessions'])
 def reserve(self,controller_cap,supervisor_cap):
  self.validate()
  assert isinstance(controller_cap,int) and isinstance(supervisor_cap,int) and controller_cap>0 and supervisor_cap>0
  cap=controller_cap+supervisor_cap;assert self.state['reserved']+cap<=self.state['prepaid'],'controller_prepaid_exhausted'
  rec=dict(id=len(self.state['sessions']),controller_cap=controller_cap,supervisor_cap=supervisor_cap,state='reserved',charged=cap)
  self.state['sessions'].append(rec);self.state['reserved']+=cap;atomic(self.path,self.state);return rec['id']
 def finish(self,i,controller_cpu,supervisor_cpu,state):
  rec=self.state['sessions'][i];assert 0<=controller_cpu<=rec['controller_cap'] and 0<=supervisor_cpu<=rec['supervisor_cap'],'controller_or_supervisor_cpu_cap_exceeded'
  rec.update(state=state,controller_cpu=controller_cpu,supervisor_cpu=supervisor_cpu);atomic(self.path,self.state)

class IncrementalJob:
 def __init__(self,path,job,schema=SCHEMA,kind=KIND):
  self.schema=schema;self.kind=kind
  self.path=Path(path);self.path.mkdir(parents=True,exist_ok=True);self.job=job;self.rows=plan();self.pending={i:r for i,r in enumerate(self.rows)};self.committed={};self.worker_charged=0;self.failed_charged=0;self.reads=dict(startup_attempts=0,startup_commits=0,raw_outputs=0,new_adoptions=0);self.startup_reconciliations=1
  statepath=self.path/'state.json';state=read(statepath) if statepath.exists() else {'job':job,'kind':self.kind,'worker_charged':0}
  assert state['job']==job and state['kind']==self.kind and type(state['worker_charged']) is int and state['worker_charged']>=0
  attempts={};archived={}
  for f in sorted((self.path/'attempt_history').glob('*.json')):
   a=read(f);assert a['job']==job and a['kind']==self.kind and a['state'] in ('failed','abandoned') and isinstance(a['charged'],int) and a['charged']>0
   assert a['archive_original_sha256'] not in archived;archived[a['archive_original_sha256']]=a
   self.worker_charged+=a['charged'];self.failed_charged+=a['charged']
  for f in sorted((self.path/'attempts').glob('*.json')):
   a=read(f);self.reads['startup_attempts']+=1
   if sha(raw(a)) in archived:
    f.unlink();continue # Idempotent recovery after archive publication, before unlink.
   assert a['job']==job and a['kind']==self.kind;assert a['id'] not in attempts and a['id'] in self.pending and a['range']==self.rows[a['id']] and a['state'] in ('reserved','complete','failed','abandoned') and isinstance(a['charged'],int) and a['charged']>=a['range']['cap'];
   if a['state']=='reserved':a['state']='abandoned';a['reconciled_no_refund']=True;atomic(f,a)
   attempts[a['id']]=a;self.worker_charged+=a['charged']
  self.worker_charged=max(self.worker_charged,state['worker_charged']) # No refund after interrupted state publication.
  for f in sorted((self.path/'committed').glob('*.json')):
   e=read(f);self.reads['startup_commits']+=1;v=e['payload'];assert sha(raw(v))==e['sha256'] and v['job']==job and v['schema']==self.schema
   i=v['id'];assert i not in self.committed and i in attempts;assert e['receipt_sha256']==sha(raw(attempts[i]));self.committed[i]=v;self.pending.pop(i)
  # Only complete-but-not-committed outputs are adopted, once at startup.
  for i,a in attempts.items():
   if i not in self.committed and a['state']=='complete':self.adopt_one(i,a)
   elif a['state']!='complete':self.failed_charged+=a['charged']
  self.pending_reserved=sum(r['cap'] for r in self.pending.values());self.persist()
 def persist(self):atomic(self.path/'state.json',dict(job=self.job,kind=self.kind,worker_charged=self.worker_charged,committed_count=len(self.committed)))
 def reserve(self,i):
  assert i in self.pending and not (self.path/'attempts'/f'{i:04d}.json').exists(),'no_implicit_retry'
  r=self.pending[i];retry=3600-self.failed_charged;assert retry>=0
  forecast=1200+self.worker_charged+self.pending_reserved+retry;assert forecast<=21600
  a=dict(id=i,job=self.job,kind=self.kind,state='reserved',charged=r['cap'],range=r,forecast=forecast)
  atomic(self.path/'attempts'/f'{i:04d}.json',a);self.worker_charged+=r['cap'];self.persist();return a
 def complete_synthetic(self,i,a):
  assert self.kind==KIND and self.schema==SCHEMA,'synthetic_cannot_enter_physical_job'
  r=self.rows[i];v=dict(schema=self.schema,kind=self.kind,job=self.job,id=i,range=r,values=[str((i+1)*(j-12)) for j in range(24)])
  out=self.path/'outputs'/f'{i:04d}.json';atomic(out,v);a=dict(a,state='complete',output_sha256=sha(out.read_bytes()));atomic(self.path/'attempts'/f'{i:04d}.json',a);return a
 def adopt_one(self,i,a):
  assert a['job']==self.job and a['kind']==self.kind and a['state']=='complete' and i in self.pending
  out=self.path/'outputs'/f'{i:04d}.json';b=out.read_bytes();self.reads['raw_outputs']+=1;assert sha(b)==a['output_sha256'],'output_digest_mismatch'
  v=json.loads(b);assert v['schema']==self.schema and v['kind']==self.kind and v['job']==self.job and v['id']==i and v['range']==self.rows[i] and len(v['values'])==24
  assert all(str(int(x))==x for x in v['values'])
  atomic(self.path/'committed'/f'{i:04d}.json',dict(payload=v,sha256=sha(raw(v)),receipt_sha256=sha(raw(a))))
  self.committed[i]=v;self.pending.pop(i)
  if hasattr(self,'pending_reserved'):self.pending_reserved-=self.rows[i]['cap']
  self.reads['new_adoptions']+=1;self.persist()
 def authorize_retry(self,i,expected_attempt_hash,authority_hash):
  path=self.path/'attempts'/f'{i:04d}.json';dest=self.path/'attempt_history'/f'{i:04d}_{expected_attempt_hash}.json'
  if not path.exists():
   old=read(dest);assert old['archive_original_sha256']==expected_attempt_hash and old['retry_authority_sha256']==authority_hash;return
  a=read(path);assert sha(raw(a))==expected_attempt_hash and a['state'] in ('failed','abandoned')
  a['archive_original_sha256']=expected_attempt_hash;a['retry_authority_sha256']=authority_hash
  if dest.exists():assert read(dest)==a
  else:atomic(dest,a)
  path.unlink()
  # Prior reservation stays in worker_charged and failed_charged, no refund.
 def finish(self):
  assert not self.pending and len(self.committed)==2945
  vals=[sum(int(self.committed[i]['values'][j]) for i in self.committed) for j in range(24)]
  if self.kind==KIND:assert vals==[(2945*2946//2)*(j-12) for j in range(24)]
  return vals

def benchmark(root,prior=None):
 p=Path(root);import resource
 limits=dict(cpu=list(resource.getrlimit(resource.RLIMIT_CPU)),address_space=list(resource.getrlimit(resource.RLIMIT_AS)),affinity=sorted(os.sched_getaffinity(0)));assert limits['cpu']==[int(os.environ['CONTROLLER_CPU_CAP'])]*2 and limits['address_space']==[256*1024**2]*2 and limits['affinity']==[7];atomic(p/'INHERITED_LIMITS.json',limits)
 start=time.process_time();wall=time.monotonic();data=Path(prior) if prior else p/'data';job=read(data/'state.json')['job'] if prior else KIND+':'+sha(Path(__file__).read_bytes());atomic(p/'RESUME_FRONTIER.json',read(data/'state.json')) if prior else None;obj=IncrementalJob(data,job);cold_start=time.process_time()-start;initial_count=len(obj.committed)
 # Exercise every synthetic chunk; leave exactly one complete receipt uncommitted.
 for i in list(obj.pending):
  a=obj.reserve(i);a=obj.complete_synthetic(i,a)
  if i!=2944:obj.adopt_one(i,a)
 generation_cpu=time.process_time()-start
 before=time.process_time();rest=IncrementalJob(data,job);restart_cpu=time.process_time()-before;assert rest.reads['raw_outputs']==1 and rest.reads['new_adoptions']==1;rest.finish()
 # A fully committed restart reads no historical raw output and adopts nothing.
 before=time.process_time();near=IncrementalJob(data,job);full_restart_cpu=time.process_time()-before;assert near.reads['raw_outputs']==0 and near.reads['new_adoptions']==0;near.finish()
 # Preserve representative corruption evidence, not thousands of raw files.
 evidence=p/'evidence';evidence.mkdir();f=data/'outputs/0000.json';bad=json.loads(f.read_text());bad['values'][23]=str(int(bad['values'][23])+1);atomic(evidence/'bad_output.json',bad);receipt=read(data/'attempts/0000.json');assert sha((evidence/'bad_output.json').read_bytes())!=receipt['output_sha256'];atomic(evidence/'receipt_0000.json',receipt);atomic(evidence/'valid_output_0000.json',read(f));atomic(evidence/'valid_commit_0000.json',read(data/'committed/0000.json'))
 # Production schemas must reject the clearly distinct synthetic identity.
 assert read(f)['schema']!='bilayer-moment24-v1' and read(f)['kind']==KIND
 ctrl=ControlBudget(p/'controller_budget_test.json');a=ctrl.reserve(20,3);ctrl.finish(a,.2,.01,'complete');b=ctrl.reserve(20,3);ctrl.finish(b,.1,.01,'fault_stopped');assert ctrl.state['reserved']==46
 try:ctrl.reserve(1200,3);raise RuntimeError('controller refund/cap mutation survived')
 except AssertionError:pass
 result=dict(kind=KIND,records=2945,resumed_from_committed=initial_count,cold_start_cpu=cold_start,generation_cpu=generation_cpu,startup_reconciliation_cpu=restart_cpu,full_near_end_restart_cpu=full_restart_cpu,generation_reads=obj.reads,restart_reads=rest.reads,fully_committed_restart_reads=near.reads,total_cpu=time.process_time()-start,wall=time.monotonic()-wall,final24=list(map(str,near.finish())),serialized_bytes=sum(f.stat().st_size for f in data.rglob('*.json')),controller_sessions_reserved=46,old_outputs_read_per_ordinary_commit=0)
 atomic(p/'BENCHMARK.json',result);print(json.dumps(result));return result
if __name__=='__main__':
 import sys
 benchmark(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
