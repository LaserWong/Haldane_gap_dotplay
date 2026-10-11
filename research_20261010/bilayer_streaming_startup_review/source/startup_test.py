"""Authorized metadata fixture: each actual startup stops after final pin hashes."""
import os,sys,resource,json,ast,builtins
from pathlib import Path
P=Path(__file__).resolve().parent;JOB=P.parent/'bilayer_full_m4_production_run_streaming';sys.path.insert(0,str(P))
import engine,outer,production_supervisor,physical_session
from engine import atomic,read,verify_pins
class StopBeforeDispatch(Exception):pass
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(99,100));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2))
# A separate observer enforces3 aggregate child CPU seconds. The99/100 inherited
# profile is the ACTUAL outer startup profile, not the metadata gate budget.
pins=read(JOB/'PINNED_INPUTS.json');results=[];max_read=0;calls=0
orig_open=builtins.open
class BoundedStream:
 def __init__(self,s):self.s=s
 def __enter__(self):return self
 def __exit__(self,*a):return self.s.__exit__(*a)
 def read(self,n):
  global max_read,calls
  assert n==65536;max_read=max(max_read,n);calls+=1;return self.s.read(n)
def bounded_open(*a,**k):return BoundedStream(orig_open(*a,**k))
def profile():
 d={}
 for line in Path('/proc/self/status').read_text().splitlines():
  if line.startswith(('VmPeak:','VmSize:','VmRSS:')):k,v=line.split(':');d[k]=int(v.split()[0])*1024
 return dict(status=d,cpu_limits=list(resource.getrlimit(resource.RLIMIT_CPU)),as_limits=list(resource.getrlimit(resource.RLIMIT_AS)),affinity=sorted(os.sched_getaffinity(0)))
def nofork(*a,**k):raise AssertionError('No worker or process dispatch permitted in metadata test')
os.fork=nofork
for name,module,entry,args in [('outer',outer,outer.run,()),('production_supervisor',production_supervisor,production_supervisor.launch,(JOB,)),('physical_session',physical_session,physical_session.run,(JOB,P/'test_output'))]:
 assert module.verify_pins is verify_pins
 tree=ast.parse((P/(name+'.py')).read_text());assert any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='verify_pins' for n in ast.walk(tree))
 def fixture_read(path):
  if Path(path)==JOB/'PRODUCTION_AUTHORITY.json':return dict(explicit_authorization=True,hard_cap=21600,deadline_utc='2026-10-14T00:00:00Z',session_chunk_limit=100)
  return read(path)
 module.read=fixture_read
 def stop_after_hash(actual):
  assert actual==pins
  global max_read
  builtins.open=bounded_open
  try:verify_pins(actual)
  finally:builtins.open=orig_open
  results.append(dict(entrypoint=name,all_final_pins_verified=len(actual),**profile()));raise StopBeforeDispatch()
 module.verify_pins=stop_after_hash
 try:entry(*args)
 except StopBeforeDispatch:pass
 else:raise AssertionError('Entry did not stop at actual startup pin boundary')
 module.verify_pins=verify_pins;module.read=read
bad=dict(pins);big='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3';bad[big]='0'*64
try:verify_pins(bad)
except AssertionError:mutation=True
else:raise AssertionError('Pin mutation survived')
assert not (JOB/'PRODUCTION_AUTHORITY.json').exists() and not (JOB/'CONTROL_SESSIONS.json').exists() and not (JOB/'store').exists()
atomic(P/'STARTUP_TEST.json',dict(actual_startups=results,mutation_rejected=mutation,max_hash_read_request=max_read,hash_read_calls=calls,workers_dispatched=0,in_memory_fixture_authority_only=True,stopped_before_any_dispatch=True))
