#!/usr/bin/env python3
"""Authorized fixture-only extension audit, never writes production ledger."""
from pathlib import Path
import os,resource,hashlib,json,copy,importlib.util,fcntl,sys,time
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,40));start=time.process_time()
for f,h in json.loads((P/'SNAPSHOT_SHA256.json').read_text()).items():assert hashlib.sha256((P/'snapshot'/f).read_bytes()).hexdigest()==h
spec=importlib.util.spec_from_file_location('extension',P/'snapshot/supervisor.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
assert (s.LIMIT,s.CPU_CAP,s.METADATA_CAP,s.BATCHES,s.INTERNAL_ALLOWANCE,s.DEADLINE)==(43200,35,5,8,600,1791698400)
assert str(s.CANONICAL)=='/workspace/shared/haldane_active/research_20261010/uniform_second_thermal_campaign_run'
raw=(P/'original_terminal.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==s.OLD_TERMINAL_SHA
# Production ledger is read only before/after, for a non-mutation assertion.
production=s.CANONICAL/'ledger.json';before=production.read_bytes();assert before==raw
folder=P/'extension_fixture_verified';folder.mkdir(exist_ok=False);(folder/'ledger.json').write_bytes(raw)
l=s.Ledger.__new__(s.Ledger);l.folder=folder;l.path=folder/'ledger.json';l.limit=s.LIMIT;l.deadline=s.DEADLINE;l.data=s.read(l.path);l.lock=open(folder/'campaign.lock','a+');fcntl.flock(l.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
old=copy.deepcopy(l.data);bindings={'fixture_source_sha256':hashlib.sha256((P/'snapshot/supervisor.py').read_bytes()).hexdigest()};l.extend(bindings);l.validate_prefix();l.validate();good=copy.deepcopy(l.data)
assert l.used()==16207 and l.limit-l.used()==26993 and l.data['limit']==43200 and l.data['attempts']==old['attempts'] and l.data['bindings']==old['bindings'] and len(l.data['extensions'])==1
assert (folder/'history'/('original_terminal_'+s.OLD_TERMINAL_SHA+'.json')).read_bytes()==raw
tests=['exact original bytes/history/attempt prefix and16207 retained','append-only21600 budget extension leaves26993']
try:l.extend(bindings)
except AssertionError:tests.append('duplicate extension rejected')
else:raise AssertionError('duplicate')
def bad(name,fn):
 l.data=copy.deepcopy(good);fn(l.data)
 try:l.validate_prefix()
 except (AssertionError,KeyError):tests.append(name);return
 raise AssertionError('accepted '+name)
for key,val in [('authorization_id','wrong'),('old_limit',0),('new_limit',99999),('additional_budget',99999),('retained_charge',0),('deadline',s.DEADLINE+1),('original_terminal_sha256','0'*64),('original_attempt_count',60),('original_bindings_sha256','0'*64)]:bad('reject modified event '+key,lambda o,k=key,v=val:o['extensions'][0].update({k:v}))
bad('reject second event',lambda o:o['extensions'].append(copy.deepcopy(o['extensions'][0])))
bad('reject retroactive refund',lambda o:o['attempts'][0].update(charge=0))
bad('reject historical source rewrite',lambda o:o['bindings'].update(unreviewed='x'))
l.data=copy.deepcopy(good);a=l.reserve(s.reservation(12,'run'),'worker');assert a['reservation']==552 and l.used()==16759 and l.data['attempts'][:61]==old['attempts'];l.validate_prefix();l.close();tests.append('new552 reservation appends without modifying historical attempts')
# Whole process bounds for every allowed size and every prefix of an8-batch attempt.
for n in range(4,13):
 assert s.reservation(n,'prepare')==4*(n+1)*7+2*37
 assert s.reservation(n,'run')==2*(n+1)*7+10*37
 assert s.reservation(n,'validate')==2*(n+1)*7+2*37
for k in range(9):
 used_max=37*k+37;remaining_min=600-used_max-2;assert remaining_min>120
assert s.reservation(12,'run')==552 and 2*552<26993;tests.append('all invocation prefixes retain full legacy120 request')
# Actual private hook on trivial Python subprocesses verifies fixed mode-specific caps.
child="import os,resource,sys;mode=sys.argv[-1];assert os.sched_getaffinity(0)=={5};assert resource.getrlimit(resource.RLIMIT_AS)==(96*1024**2,96*1024**2);assert resource.getrlimit(resource.RLIMIT_CPU)==((5,5) if mode in ('list','matrix') else (35,35));print(mode,flush=True)"
runner="import subprocess,sys,resource\ndef limits(): resource.setrlimit(resource.RLIMIT_CPU,(120,120)); resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))\n"+"\n".join("subprocess.run([sys.executable,'-c',"+repr(child)+","+repr(mode)+"],check=True,preexec_fn=limits)" for mode in ['list','matrix','compute'])
l=s.Ledger(P/'hook_fixture_verified',2000,time.time()+15,bindings={'fixture':'mode-caps'},test=True);a=l.reserve(552,'worker');pid=s.launch(l,a,[sys.executable,'-c',runner],5);active={pid:a};stop=time.time()+10
while active and time.time()<stop:s.drain(l,active);time.sleep(.01)
assert not active and not s.group_live(pid) and a['status']=='COMPLETE';l.close();tests.append('live hook enforces5CPU metadata35CPU compute96MiB singlecore')
assert production.read_bytes()==before;tests.append('production ledger unchanged')
out={'status':'PASS independent design/fixture extension gate','tests':tests,'count':len(tests),'retained_charge':16207,'new_cap':43200,'remaining_before_new_work':26993,'max_run_reservation':552,'no_production_write':True,'no_thermal_command':True,'internal_budget600_prevents_shrinking_branch':True,'CPU_seconds_self':time.process_time()-start,'CPU_seconds_children':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime}
(P/'extension_test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
