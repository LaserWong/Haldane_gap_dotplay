import os,sys,json,hashlib,ast,copy,types,time,signal,resource,ctypes,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent;SRC=ROOT/'bilayer_stable_observer_checksum_fix';JOB=ROOT/'bilayer_full_m4_production_run_checksum';BASE=ROOT/'bilayer_streaming_hash_revision'
assert os.sched_getaffinity(0)=={7} and resource.getrlimit(resource.RLIMIT_CPU)==(6,6) and resource.getrlimit(resource.RLIMIT_AS)==(64*1024**2,128*1024**2)
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(32768),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def emit(name,x):(P/name).write_text(json.dumps(x,indent=2)+'\n')
assert digest(SRC/'MANIFEST_SHA256.json')=='6b810258d0d4f593d6d19308b5d19690dedde8d69ac721e9554b6dff66cc9d5a'
assert all(digest(SRC/f)==h for f,h in read(SRC/'MANIFEST_SHA256.json').items())
shutil.copytree(SRC,P/'source')
pins=read(JOB/'PINNED_INPUTS.json');assert digest(JOB/'PINNED_INPUTS.json')=='4c9c17ece2714710b83c8f4e975b027dc057da3a51bb9d44671ba869b124f6da' and len(pins)==27
assert all(digest(f)==h for f,h in pins.items())
job=hashlib.sha256(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins))).hexdigest();assert job=='c2c9f79a9d55bbc0867f3ef38103d54cb98fc44c185adc280360ca25a969fd01'
for name in ['PINNED_INPUTS.json','PROPOSED_JOB_ID.json','PREDECESSOR.json','CONTROL_SESSIONS_CARRY_FORWARD.json','EXPECTED_M012.json']:shutil.copy2(JOB/name,P/name)
assert not(JOB/'PRODUCTION_AUTHORITY.json').exists() and not(JOB/'CONTROL_SESSIONS.json').exists() and not(JOB/'store').exists()
def funcs(p):
 s=Path(p).read_text();return {n.name:(ast.get_source_segment(s,n),n) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
old=funcs(BASE/'physical_session.py');new=funcs(SRC/'physical_session.py')
science=['verify_output','worker','stop_after_chunk','required_pins','finalize_physical']
assert all(old[k][0]==new[k][0] for k in science)
class RestoreBudgets(ast.NodeTransformer):
 def visit_Name(self,n):return ast.copy_location(ast.Constant(value={'CONTROL_POOL':1200,'RETRY_POOL':3600}[n.id]),n) if n.id in ['CONTROL_POOL','RETRY_POOL'] else n
assert ast.dump(RestoreBudgets().visit(copy.deepcopy(new['run'][1])),include_attributes=False)==ast.dump(old['run'][1],include_attributes=False)
assert funcs(BASE/'engine.py')['plan'][0]==funcs(SRC/'engine.py')['plan'][0]
assert all(digest(SRC/n)==digest(BASE/n) for n in ['production_supervisor.py','session_supervisor.py'])
oldpins=read(ROOT/'bilayer_full_m4_production_run_streaming/PINNED_INPUTS.json')
for name in ['whole','whole.cpp','pencil24.py']:
 f=str(ROOT/'bilayer_variable_g_control_gate'/name);assert pins[f]==oldpins[f]==digest(f)
assert digest(SRC/'limit_observer.py')==digest(ROOT/'bilayer_stable_observer_revision/limit_observer.py')
sys.path.insert(0,str(SRC));import engine,physical_session,production_supervisor
# Carry accounting uses the actual frozen predecessor, not a reset ledger.
pred=read(JOB/'PREDECESSOR.json');carry=read(JOB/'CONTROL_SESSIONS_CARRY_FORWARD.json');prior=ROOT/'bilayer_full_m4_production_run_streaming'
assert carry==read(prior/'CONTROL_SESSIONS.json') and carry['reserved']==463 and pred['charged_control']==463 and pred['charged_workers']==192 and pred['no_refund']
assert pred['failed_manifest_sha256']==digest(prior/'FAILED_OBSERVER_MANIFEST_SHA256.json')=='552153e60e66c147e6384cca5f6b878e6a7cfac271cc35d4e0d66a0ed2e17b73'
assert (engine.CONTROL_POOL,engine.RETRY_POOL,engine.RETIRED_WORKER_RESERVATIONS)==(1600,3200,192)
budget=dict(carry,prepaid=1600);engine.atomic(P/'control_fixture.json',budget);cb=engine.ControlBudget(P/'control_fixture.json');assert cb.reserve(100,20)==5 and cb.reserve(99,1)==6 and cb.state['reserved']==683
assert cb.state['sessions'][:5]==carry['sessions'] and 683+30*23==1373 and 1600-1373==227
store=engine.IncrementalJob(P/'fixture_store','REVIEW-NONPRODUCTION-CARRY192',physical_session.SCHEMA,physical_session.KIND)
assert store.worker_charged==store.failed_charged==192 and store.pending_reserved==16800
assert store.reserve(0)['forecast']==21600
store2=engine.IncrementalJob(P/'fixture_store','REVIEW-NONPRODUCTION-CARRY192',physical_session.SCHEMA,physical_session.KIND);assert store2.worker_charged==store2.failed_charged==195 and 3200-192==3008
# Existing physical receipt with nonzero n8 exercises the restored coefficient.
selected=None
for f in sorted((prior/'store/committed').glob('*.json')):
 v=read(f)['payload']
 if int(v['values'][20]):selected=v;break
assert selected is not None
idx=selected['id'];rawdir=prior/'raw_outputs'/f'{idx:04d}_{3*(idx+1)}';rec=read(rawdir/'receipt.json')
assert physical_session.verify_output(rawdir,rec,selected['range'],rec['identity'])==selected['values']
bad=P/'bad_193200';shutil.copytree(rawdir,bad);r=read(bad/'result.json');r['moments'][3]=str(int(r['moments'][3])-400*int(selected['values'][20]));(bad/'result.json').write_bytes(raw(r));badrec=copy.deepcopy(rec);badrec['output_sha256']['result.json']=digest(bad/'result.json')
try:physical_session.verify_output(bad,badrec,selected['range'],rec['identity'])
except AssertionError:pass
else:raise AssertionError('193200 checksum corruption accepted')
emit('SOURCE_CARRY_CHECKS.json',dict(scientific_functions_byte_identical=science,run_AST_budget_only=True,nonzero_n8_chunk=idx,n8=selected['values'][20],bad193200_rejected=True,control_carry=463,worker_carry=192,control_forecast=1373,retry_remaining=3008,initial_forecast=21600))
# Exact helper, with only the expected affinity6 changed to reviewer CPU7.
obs=types.ModuleType('review_limit_observer');obs.__file__=str(SRC/'limit_observer.py');code=(SRC/'limit_observer.py').read_text();assert code.count("record['affinity']!='6'")==1
adapt=code.replace("record['affinity']!='6'","record['affinity']!='7'");(P/'limit_observer_cpu7.py').write_text(adapt);exec(compile(adapt,str(SRC/'limit_observer.py'),'exec'),obs.__dict__)
config=dict(python=sys.executable,native='/usr/bin/sleep',scripts=dict(outer='/review/outer.py',supervisor='/review/supervisor.py',controller=str(Path(__file__).resolve())))
assert [obs.topology_role(x,10,{10:{'ppid':1},11:{'ppid':10},12:{'ppid':11},13:{'ppid':2}}) for x in [10,11,12,13]]==['supervisor','controller','native','unexpected']
results=[]
def must_reject(record,label):
 try:obs.enforce(record,P/'events'/label)
 except obs.LimitMismatch:pass
 else:raise AssertionError('genuine mismatch survived '+label)
 assert any(read(f)==record for f in (P/'events'/label).glob('*.json'))
for label,cap,mem in [('good',3,128),('bad_cpu',2,128),('bad_AS',3,96)]:
 pr,cw=os.pipe();cr,pw=os.pipe();owner=os.getpid();pid=os.fork()
 if pid==0:
  assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
  if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
  os.close(pr);os.close(pw);os.write(cw,b'B');assert os.read(cr,1)==b'L'
  resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));resource.setrlimit(resource.RLIMIT_AS,(mem*1024**2,mem*1024**2));os.write(cw,b'C');assert os.read(cr,1)==b'E'
  os.execv('/usr/bin/sleep',['/usr/bin/sleep','5'])
 os.close(cr);os.close(cw)
 try:
  assert os.read(pr,1)==b'B';before=obs.sample(pid,'native',config);assert before['outcome']=='fork_before_exec';obs.enforce(before,P/'events'/label)
  os.write(pw,b'L');assert os.read(pr,1)==b'C';changed=obs.sample(pid,'native',config);assert changed['outcome']=='fork_before_exec' and changed['cpu']==[cap,cap] and changed['address_space']==[mem*1024**2]*2;obs.enforce(changed,P/'events'/label)
  os.write(pw,b'E');until=time.monotonic()+2
  while True:
   post=obs.sample(pid,'native',config)
   if post['outcome'] in ['verified_post_exec','mismatch']:break
   obs.enforce(post,P/'events'/label);assert time.monotonic()<until;time.sleep(.002)
  if label!='good':must_reject(post,label)
  else:
   assert post['outcome']=='verified_post_exec' and post['after']['start']==before['after']['start'];obs.enforce(post,P/'events'/label)
   wrong=copy.deepcopy(post);wrong['affinity']='6';obs.classify(wrong,config);must_reject(wrong,'injected_bad_affinity')
   wrongexe=copy.deepcopy(post);wrongexe['after']['exe']='/definitely/not/expected';wrongexe['before']=copy.deepcopy(wrongexe['after']);obs.classify(wrongexe,config);must_reject(wrongexe,'injected_unexpected_image')
   prioridentity=copy.deepcopy(before['before']);lateridentity=copy.deepcopy(post['after'])
   for x in [prioridentity,lateridentity]:x['argv']=[s.encode() for s in x['argv']]
   realidentity=obs.identity;identities=iter([prioridentity,lateridentity]);obs.identity=lambda _:next(identities)
   try:cross=obs.sample(pid,'native',config)
   finally:obs.identity=realidentity
   assert cross['outcome']=='exec_or_identity_transition';obs.enforce(cross,P/'events/crossing')
   # Same PID/starttime must be rechecked after a genuine post-exec limit change.
   resource.prlimit(pid,resource.RLIMIT_CPU,(2,2));rechecked=obs.sample(pid,'native',config);assert rechecked['after']==post['after'];must_reject(rechecked,'same_identity_limit_change')
  results.append(dict(case=label,before=before,after_limits=changed,post_exec=post))
 finally:
  try:os.kill(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  w,st,u=os.wait4(pid,0);assert w==pid
  os.close(pr);os.close(pw)
 afterexit=obs.sample(pid,'native',config);assert afterexit['outcome']=='exited_during_observation';obs.enforce(afterexit,P/'events'/label)
 results[-1].update(killed_reaped=True,wait4_CPU=u.ru_utime+u.ru_stime,exit_status=os.waitstatus_to_exitcode(st))
emit('OBSERVER_CASES.json',results)
# Repeat the final27-pin startup cutpoints under realAS64, before any dispatch.
outer=types.ModuleType('review_outer');outer.__file__=str(SRC/'outer.py');outer.__name__='review_outer';source=(SRC/'outer.py').read_text();assert 'if child in limit_observations:continue' not in source and "key=str(child)+':'+observation['after']['start']" in source
adapt=source.replace('=={6}','=={7}').replace('==(99,100)','==(6,6)');(P/'outer_cpu7.py').write_text(adapt);exec(compile(adapt,str(SRC/'outer.py'),'exec'),outer.__dict__)
class Cutpoint(BaseException):pass
realverify=engine.verify_pins;authority=dict(explicit_authorization=True,hard_cap=21600,deadline_utc='2026-10-14T00:00:00Z',session_chunk_limit=100,job_id=job);cuts=[]
def nofork(*a,**k):raise AssertionError('scientific_fork_forbidden')
os.fork=nofork
for name,mod,call in [('outer',outer,lambda:outer.run()),('supervisor',production_supervisor,lambda:production_supervisor.launch(JOB)),('controller',physical_session,lambda:physical_session.run(JOB,P/'no_dispatch'))]:
 original_read=mod.read;original_verify=mod.verify_pins
 def fixture_read(path):return dict(authority) if Path(path)==JOB/'PRODUCTION_AUTHORITY.json' else original_read(path)
 mod.read=fixture_read
 if name=='outer':
  def fixture_lock(path,*args,**kw):
   assert Path(path)==JOB/'OUTER_LOCK';return open(P/'review_outer.lock',*args,**kw)
  mod.open=fixture_lock
 def verify_cut(actual):
  assert actual==pins;realverify(actual);cuts.append(name);raise Cutpoint()
 mod.verify_pins=verify_cut
 try:call()
 except Cutpoint:pass
 else:raise AssertionError('actual verifier not reached')
 finally:mod.read=original_read;mod.verify_pins=original_verify
assert cuts==['outer','supervisor','controller'];assert not(JOB/'PRODUCTION_AUTHORITY.json').exists() and not(JOB/'CONTROL_SESSIONS.json').exists() and not(JOB/'store').exists()
vm={k:int(v.split()[0])*1024 for k,v in (line.split(':',1) for line in Path('/proc/self/status').read_text().splitlines() if line.startswith(('VmPeak:','VmSize:','VmRSS:')))}
emit('CHECKS.json',dict(status='PASS_OBSERVER_CORRECTION_AND_SCOPED_BUDGET_DELTA',source_seal='6b810258d0d4f593d6d19308b5d19690dedde8d69ac721e9554b6dff66cc9d5a',job=job,pins=27,actual_startup_cutpoints=cuts,actual_AS=resource.getrlimit(resource.RLIMIT_AS),memory=vm,barrier_cases=3,true_bad_CPU_rejected=True,true_bad_AS_rejected=True,injected_bad_affinity_rejected=True,read_crossing_exec_deferred=True,same_identity_limit_change_rechecked=True,mismatch_diagnostics_persisted=True,all_test_children_reaped=True,restored193600_nonzero_n8_checked=True,control_carry=463,worker_carry=192,global_cap=21600,control_pool=1600,retry_pool=3200,control_forecast=1373,retry_remaining=3008,no_physical_worker=True,production_authority_created=False));print('PASS stable observer and exact science/budget scope')
