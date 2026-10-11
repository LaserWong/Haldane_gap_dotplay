"""Persistent physical dispatcher using the benchmarked incremental store.
No production authority is included; this entrypoint has not executed physics.
"""
import os,sys,time,json,signal,resource,ctypes,math
from pathlib import Path
from engine import IncrementalJob,atomic,read,sha,raw
from session_supervisor import snapshot
ROOT=Path(__file__).resolve().parent;KERNEL=ROOT.parent/'bilayer_variable_g_control_gate';SCHEMA='bilayer-moment24-v1';KIND='PHYSICAL-FIXED-WITNESS24'
import datetime
DEADLINE=datetime.datetime(2026,10,14,tzinfo=datetime.timezone.utc).timestamp()

def verify_output(out,receipt,row,identity):
 assert receipt['identity']==identity and receipt['exit']==0
 required={'result.json','result.json.schema.json','result.json.accumulators.json','chunk.json','targets.jsonl'};assert required<=set(receipt['output_sha256'])
 for name,h in receipt['output_sha256'].items():assert Path(name).name==name and sha((out/name).read_bytes())==h
 assert read(out/'result.json.schema.json')==dict(schema=SCHEMA,fields=24)
 meta=read(out/'chunk.json');q=row['q'];stride=65536 if q==6 else 1024 if q==4 else 127 if q==2 else 1
 assert (meta['q'],meta['begin'],meta['end'],meta['N'],meta['stride'])==(q,row['begin'],row['end'],row['N'],stride)
 targets=[json.loads(x) for x in (out/'targets.jsonl').read_text().splitlines()];assert [x['id'] for x in targets]==list(range(row['begin'],row['end']));assert all(x['rank']==stride*x['id']%row['N'] for x in targets)
 val=read(out/'result.json.accumulators.json');r=read(out/'result.json');assert len(val)==24 and r['complete'] and list(r['terms'].values())==val[:15];v=list(map(int,val));m=[v[15],v[16],v[17]+121*v[20],v[18]+193600*v[20]+1331*sum(v[:4])+v[21],v[19]+sum(v[4:10])+14641*sum(v[10:15])];assert m==list(map(int,r['moments']));return val

def worker(out,row,identity,lockfd):
 out.mkdir(parents=True,exist_ok=False);owner=os.getpid();libc=ctypes.CDLL(None);pid=os.fork()
 if pid==0:
  assert libc.prctl(1,signal.SIGKILL,0,0,0)==0
  if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
  os.setsid();os.set_inheritable(lockfd,True);os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(row['cap'],row['cap']));resource.setrlimit(resource.RLIMIT_AS,(128*1024**2,128*1024**2));fd=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(fd,1);os.dup2(fd,2);os.close(fd)
  args=[str(KERNEL/'whole'),'chunk','sample',str(out),str(ROOT.parent/'bilayer_whole_m4_pipeline'),str(ROOT.parent/'bilayer_brauer_rule_compiler/run'),str(row['cap']),'8',str(row['q']),str(row['begin']),str(row['end']-row['begin'])];os.execv(args[0],args)
 start=time.monotonic();why=None
 while True:
  w,st,u=os.wait4(pid,os.WNOHANG)
  if w:break
  try:
   ss=snapshot();assert pid in ss;assert not any(x['ppid']==pid for x in ss.values()),'unexpected_numerical_descendant'
   if ss[pid]['cpu']>=row['cap']-.1:why='worker_cpu_guard'
  except Exception:why='worker_accounting_failure'
  if time.monotonic()-start>2*row['cap']+10 or time.time()>=DEADLINE:why='worker_wall_or_absolute_deadline'
  if why:os.killpg(pid,signal.SIGKILL);w,st,u=os.wait4(pid,0);break
  time.sleep(.01)
 rec=dict(identity=identity,exit=os.waitstatus_to_exitcode(st),reason=why,wait4_cpu=u.ru_utime+u.ru_stime,output_sha256={f.name:sha(f.read_bytes()) for f in out.iterdir() if f.is_file()});assert rec['wait4_cpu']<=row['cap'];atomic(out/'receipt.json',rec);return rec

STOP=False
def stop_after_chunk(signum,frame):
 global STOP;STOP=True

def required_pins(jobdir):
 return {str(p.resolve()) for p in [KERNEL/'whole',KERNEL/'whole.cpp',KERNEL/'pencil24.py',ROOT/'engine.py',ROOT/'physical_session.py',ROOT/'session_supervisor.py',ROOT/'production_supervisor.py',jobdir/'EXPECTED_M012.json',ROOT.parent/'bilayer_whole_m4_pipeline/witness57.txt',ROOT.parent/'bilayer_whole_m4_pipeline/geometry_8x4.txt',*[ROOT.parent/'bilayer_brauer_rule_compiler/run'/('diagrams_'+x+'.bin') for x in ['N','F','L']]]}

def finalize_physical(store,jobdir,identity):
 store.finish();sector={q:[0]*24 for q in [0,2,4,6]}
 for v in store.committed.values():
  q=v['range']['q']
  for j,x in enumerate(v['values']):sector[q][j]+=int(x)
 sys.path.insert(0,str(KERNEL));import pencil24
 controls=read(jobdir/'EXPECTED_M012.json');assert controls['schema']=='accepted-fixed-witness-m012-v1' and controls['T_Q']==200 and controls['T_A']==11
 assert controls['witness_sha256']==identity[str((ROOT.parent/'bilayer_whole_m4_pipeline/witness57.txt').resolve())]
 assert controls['geometry_sha256']==identity[str((ROOT.parent/'bilayer_whole_m4_pipeline/geometry_8x4.txt').resolve())]
 v=pencil24.pencil(sector,11,100,True);assert v['G_numerators']==[str(int(controls[k])) for k in ['m0','m1','m2']],'accepted_full_m012_mismatch'
 mats=pencil24.validate_export(v);m3=200*mats['K'][2];m4=40000*mats['J'][2];assert m3.denominator==m4.denominator==1
 atomic(jobdir/'FULL_MOMENTS.json',dict(schema=SCHEMA,job=store.job,complete=True,accepted_m012=True,m3=str(int(m3)),m4=str(int(m4)),raw_sector_accumulators={q:list(map(str,a)) for q,a in sector.items()},pencil_at_11_over_100=v))

def run(jobdir,outdir):
 jobdir=Path(jobdir);outdir=Path(outdir);authority=read(jobdir/'PRODUCTION_AUTHORITY.json');assert authority['explicit_authorization'] is True and authority['hard_cap']==21600 and authority['deadline_utc']=='2026-10-14T00:00:00Z'
 identity=read(jobdir/'PINNED_INPUTS.json');assert required_pins(jobdir)<=set(identity),'mandatory_pins_missing';assert all(sha(Path(f).read_bytes())==h for f,h in identity.items());lockfd=int(os.environ['BILAYER_LOCK_FD']);assert os.fstat(lockfd).st_ino==os.stat(jobdir/'LOCK').st_ino
 signal.signal(signal.SIGUSR1,stop_after_chunk);completed=0;session_limit=authority.get('session_chunk_limit',100);assert 1<=session_limit<=100
 job=sha(raw(dict(kind=KIND,schema=SCHEMA,identity=identity)));store=IncrementalJob(jobdir/'store',job,SCHEMA,KIND)
 for i in list(store.pending):
  if STOP or completed>=session_limit:break
  row=store.rows[i];retry_remaining=3600-store.failed_charged;assert retry_remaining>=0
  assert 1200+store.worker_charged+store.pending_reserved+retry_remaining<=21600
  assert 1200+store.worker_charged+row['cap']<=20000
  control=read(jobdir/'CONTROL_SESSIONS.json');session_slots=(1200-control['reserved'])//23+1;assert math.ceil(len(store.pending)/session_limit)<=session_slots,'controller_session_reserve_cannot_cover_pending_chunks'
  review_reserve=authority.get('independent_review_wall_reserve',86400);assert review_reserve>=86400
  remaining_wall=2*(store.pending_reserved+retry_remaining)+10*(len(store.pending)+math.ceil(retry_remaining/3))+1200+60*session_slots+review_reserve
  assert time.time()+remaining_wall<DEADLINE,'complete_work_and_review_deadline_forecast'
  prior=store.path/'attempts'/f'{i:04d}.json'
  if prior.exists():
   a=read(prior);assert a['state'] in ('failed','abandoned')
   token=authority.get('authorized_retry_receipts',{}).get(str(i));assert token==sha(raw(a)),'specific_retry_authority_required';store.authorize_retry(i,token,sha(raw(authority)))
  a=store.reserve(i);attempt_tag=str(store.worker_charged);out=jobdir/'raw_outputs'/f'{i:04d}_{attempt_tag}';rec=worker(out,row,identity,lockfd)
  if rec['exit']!=0:
   a.update(state='failed',worker_receipt_sha256=sha(raw(rec)));atomic(store.path/'attempts'/f'{i:04d}.json',a);raise RuntimeError('worker_failed_no_automatic_retry')
  val=verify_output(out,rec,row,identity);payload=dict(schema=SCHEMA,kind=KIND,job=job,id=i,range=row,values=val,worker_receipt_sha256=sha(raw(rec)))
  normalized=store.path/'outputs'/f'{i:04d}.json';atomic(normalized,payload);a.update(state='complete',output_sha256=sha(normalized.read_bytes()));atomic(store.path/'attempts'/f'{i:04d}.json',a);store.adopt_one(i,a);completed+=1
 if not store.pending:finalize_physical(store,jobdir,identity)
 atomic(outdir/'SESSION_SELF_CPU.json',dict(controller_self_cpu=time.process_time(),completed_this_session=completed,pending_chunks=len(store.pending),graceful_boundary_stop=bool(store.pending)))
if __name__=='__main__':run(sys.argv[1],sys.argv[2])
