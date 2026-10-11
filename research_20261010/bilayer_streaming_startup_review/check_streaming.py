import os,sys,resource,json,hashlib,builtins,types,time
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent;SRC=ROOT/'bilayer_streaming_hash_revision';JOB=ROOT/'bilayer_full_m4_production_run_streaming'
sys.path.insert(0,str(SRC));import engine,physical_session,production_supervisor
assert os.sched_getaffinity(0)=={7} and resource.getrlimit(resource.RLIMIT_CPU)==(8,8) and resource.getrlimit(resource.RLIMIT_AS)==(64*1024**2,128*1024**2)
def digest(path):
 h=hashlib.sha256()
 with builtins.open(path,'rb') as f:
  while True:
   b=f.read(32768)
   if not b:return h.hexdigest()
   h.update(b)
def load(path):return json.loads(Path(path).read_text())
pins=load(JOB/'PINNED_INPUTS.json');proposed=load(JOB/'PROPOSED_JOB_ID.json');assert digest(JOB/'PINNED_INPUTS.json')==proposed['pins_sha256']=='227f433eb8a01923d217b7dc2d407e257bd1f7a438845432269364702da44be5'
assert engine.sha(engine.raw(dict(kind=physical_session.KIND,schema=physical_session.SCHEMA,identity=pins)))==proposed['job_id']=='845b55d815552ca70bb870f0efd6be20a94850f952e63a87dc7a0338553e8a0e'
assert all(digest(f)==h for f,h in pins.items())
pythonpin='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3';assert Path(pythonpin).stat().st_size==30894944 and pythonpin in pins and len(pins)==26
assert digest(JOB/'EXPECTED_M012.json')=='f528834efae7b875b4dfa665ab991f4bfd7db73d54507ac681c8402e1a6f19ec'
failed=ROOT/'bilayer_full_m4_production_run';assert digest(failed/'FAILED_START_MANIFEST_SHA256.json')=='0dd76472806a818c4489fac4b093b7636468dc33771bbb0c8fa6ae3b9875aa32'
carry=load(JOB/'CONTROL_SESSIONS_CARRY_FORWARD.json');pred=load(JOB/'PREDECESSOR.json');assert carry==load(failed/'CONTROL_SESSIONS.json') and carry['reserved']==220 and pred['charged_control']==220 and pred['no_refund']
assert pred['original_total_cpu_authority']==pred['successor_total_cpu_authority']==21600 and pred['control_pool']==carry['prepaid']==1200
assert [x['charged'] for x in carry['sessions']]==[120,100] and all(x['no_refund'] and x['state']=='FAILED_PREINNER' for x in carry['sessions'])
assert 220+220+30*23==1130 and 1200-1130==70
assert not(JOB/'PRODUCTION_AUTHORITY.json').exists() and not(JOB/'CONTROL_SESSIONS.json').exists() and not(JOB/'store').exists()
# Engine delta is only the bounded file-digest helpers; no scheduling/recovery change.
old=(ROOT/'bilayer_control_memory_revision/engine.py').read_text();new=(SRC/'engine.py').read_text();stripped=new[:new.index('def file_sha256')]+new[new.index('def atomic'):];assert stripped==old
assert digest(SRC/'session_supervisor.py')==digest(ROOT/'bilayer_control_memory_revision/session_supervisor.py')
outer=types.ModuleType('review_actual_outer');outer.__file__=str(SRC/'outer.py');outer.__name__='review_actual_outer';exec(compile((P/'outer_cpu7_review.py').read_text(),str(SRC/'outer.py'),'exec'),outer.__dict__)
# Real entries, real complete pin maps and real helper. Only a memory-only fixture
# authority, redirected lock and a stop immediately after successful verification.
realopen=builtins.open;realverify=engine.verify_pins;results=[];sizes=[];paths=set()
class ReadBound:
 def __init__(self,path,*args,**kw):self.f=realopen(path,*args,**kw);self.path=str(path)
 def __enter__(self):return self
 def __exit__(self,*args):self.f.close()
 def read(self,n=-1):
  assert 0<n<=65536,'whole_file_hash_read';sizes.append(n);paths.add(self.path);return self.f.read(n)
class VerifiedStop(BaseException):pass
def forbid_fork(*args,**kw):raise AssertionError('review_forbids_dispatch')
os.fork=forbid_fork
authority=dict(explicit_authorization=True,hard_cap=21600,deadline_utc='2026-10-14T00:00:00Z',session_chunk_limit=100,job_id=proposed['job_id'])
for name,module,call in [('outer',outer,lambda:outer.run()),('supervisor',production_supervisor,lambda:production_supervisor.launch(JOB)),('controller',physical_session,lambda:physical_session.run(JOB,P/'no_controller_output'))]:
 assert module.verify_pins is realverify
 original_read=module.read;original_verify=module.verify_pins
 def read_fixture(path):
  if Path(path)==JOB/'PRODUCTION_AUTHORITY.json':return dict(authority)
  return original_read(path)
 module.read=read_fixture
 if name=='outer':
  def lock_only(path,*a,**kw):
   assert Path(path)==JOB/'OUTER_LOCK';return realopen(P/'review_outer.lock',*a,**kw)
  module.open=lock_only
 def checked(actual):
  assert actual==pins
  before=len(sizes);builtins.open=ReadBound
  try:realverify(actual)
  finally:builtins.open=realopen
  vm={k:int(v.split()[0])*1024 for k,v in (line.split(':',1) for line in Path('/proc/self/status').read_text().splitlines() if line.startswith(('VmPeak:','VmSize:','VmRSS:')))}
  results.append(dict(entry=name,pins=len(actual),hash_reads=len(sizes)-before,limits=dict(cpu=resource.getrlimit(resource.RLIMIT_CPU),address_space=resource.getrlimit(resource.RLIMIT_AS)),memory=vm))
  raise VerifiedStop()
 module.verify_pins=checked
 try:call()
 except VerifiedStop:pass
 else:raise AssertionError('entry did not reach actual full-pin verifier')
 finally:module.read=original_read;module.verify_pins=original_verify
assert len(results)==3 and pythonpin in paths and len(paths)==26 and max(sizes)==65536
bad=dict(pins);bad[pythonpin]='0'*64
try:realverify(bad)
except AssertionError:pass
else:raise AssertionError('large-binary hash mutation accepted')
report=dict(status='PASS_ALL_THREE_REAL_STARTUPS_FINAL26_PINS_AS64',source_manifest='88aa9e771ab91a958d43a339a9bbd96e627240f2ca82cdc0d4234ddf0908fbee',job_id=proposed['job_id'],contexts=results,python_binary_bytes=30894944,read_block_bytes=65536,total_hash_reads=len(sizes),large_pin_mutation_rejected=True,old_failed_control_charge=220,successor_standard_control_total=1130,remaining_control_margin=70,unchanged_global_CPU_cap=21600,test_only_CPU_affinity_adaptation='CPU7 and8hard; actualAS64soft/128hard before imports',no_physical_workers=True,no_real_authority_or_ledger_created=True)
(P/'CHECKS.json').write_text(json.dumps(report,indent=2)+'\n');print('STREAMING ACTUAL STARTUP PASS')
