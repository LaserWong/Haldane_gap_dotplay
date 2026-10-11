#!/usr/bin/env python3
"""Design-only fixture tests: never opens production ledger for writing."""
from pathlib import Path
import os,sys,time,json,hashlib,resource,subprocess,importlib.util,copy,fcntl,shutil
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));sp=importlib.util.spec_from_file_location('extension',P/'supervisor.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
root=P.parent;original=root/'uniform_second_thermal_campaign_partial_outcome/terminal_ledger_snapshot.json';raw=original.read_bytes();assert hashlib.sha256(raw).hexdigest()==s.OLD_TERMINAL_SHA
fixture=P/'ledger_extension_fixture_final';fixture.mkdir(exist_ok=True);(fixture/'ledger.json').write_bytes(raw)
# Explicit test-only object bypasses production sole-path constructor; it never launches.
l=s.Ledger.__new__(s.Ledger);l.folder=fixture;l.path=fixture/'ledger.json';l.limit=s.LIMIT;l.deadline=s.DEADLINE;l.data=s.read(l.path);l.lock=open(fixture/'campaign.lock','a+');fcntl.flock(l.lock,fcntl.LOCK_EX|fcntl.LOCK_NB);old=copy.deepcopy(l.data);l.extend(s.sources());l.validate_prefix();assert l.used()==16207 and l.data['limit']==43200 and l.data['attempts']==old['attempts'] and l.data['bindings']==old['bindings'];assert (fixture/'history'/('original_terminal_'+s.OLD_TERMINAL_SHA+'.json')).read_bytes()==raw
extension=l.data['extensions'][0];assert extension['old_limit']==21600 and extension['additional_budget']==21600 and extension['retained_charge']==16207
try:l.extend(s.sources())
except AssertionError:duplicate_rejected=True
else:raise AssertionError('duplicate extension accepted')
l.data['attempts'][0]['charge']-=1
try:l.validate_prefix()
except AssertionError:refund_rejected=True
else:raise AssertionError('old refund mutation accepted')
l.data['attempts']=copy.deepcopy(old['attempts']);l.validate_prefix();l.close()
# Test bounded configuration for EVERY allowed base, not a grid of observed timings.
assert s.INTERNAL_ALLOWANCE>s.BATCHES*(s.CPU_CAP+2)+(s.CPU_CAP+2)+120+2
reservations={str(n):{a:s.reservation(n,a) for a in ['prepare','run','validate']} for n in range(4,13)};assert reservations['12']['run']==552
# Scaled legacy integration regression: mathematical floor(remaining)-1 and capped child.
def sequence(label,budget,max_batches,cap,work):
 folder=P/label;folder.mkdir(exist_ok=True);start=resource.getrusage(resource.RUSAGE_CHILDREN);selfstart=time.process_time();rows=[]
 code='import time\nt=time.process_time()+'+str(work)+'\nwhile time.process_time()<t: pass\n'
 for j in range(max_batches):
  r=resource.getrusage(resource.RUSAGE_CHILDREN);used=time.process_time()-selfstart+r.ru_utime+r.ru_stime-start.ru_utime-start.ru_stime;remaining=int(budget-used)-1
  if remaining<1:rows.append({'yield_before_launch':True,'remaining':remaining});break
  allowance=min(cap,remaining)
  def limits():resource.setrlimit(resource.RLIMIT_CPU,(allowance,allowance));resource.setrlimit(resource.RLIMIT_AS,(96*1024**2,96*1024**2))
  b=resource.getrusage(resource.RUSAGE_CHILDREN);rr=subprocess.run([sys.executable,'-c',code],preexec_fn=limits,timeout=6);a=resource.getrusage(resource.RUSAGE_CHILDREN);row={'index':j,'remaining':remaining,'allowance':allowance,'exitcode':rr.returncode,'cpu':a.ru_utime+a.ru_stime-b.ru_utime-b.ru_stime};rows.append(row)
  if rr.returncode:break
  (folder/f'checkpoint{j}.json').write_text(json.dumps(row))
 return rows
unsafe=sequence('legacy_boundary_fixture_final',7,3,3,2.2);assert unsafe[-1]['exitcode']==-9
safe=sequence('bounded_invocation_fixture_final',30,3,3,2.2);assert len(safe)==3 and all(x['exitcode']==0 and x['allowance']==3 for x in safe)
# Frozen wrapper/kernel pins remain unchanged; actual partial checkpoints keep old identities.
gp=root/'uniform_second_thermal_campaign_gate/campaign.py';spec=importlib.util.spec_from_file_location('gate',gp);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
for twist in ['I','P']:
 folder=root/'uniform_second_thermal_campaign_run/cases'/('L12_'+twist);case=g.loadcase(folder/'case.json',12,twist,16,g.pins())
 for sec,start,count,name in g.batches(case):
  f=folder/name
  if f.exists():g.verify_batch(json.loads(f.read_text()),g.identity(case,sec,start,count),sec['representatives'][start:start+count])
# Metadata-only integration uses a copied single-case fixture, not a campaign/alternative ledger.
case=root/'uniform_second_thermal_extension_metadata_fixture';shutil.copytree(root/'uniform_second_thermal_campaign_run/cases/L4_I',case)
led=s.Ledger(P/'metadata_integration_ledger',10000,time.time()+30,bindings={'fixture':'metadata-only'},test=True);a=led.reserve(s.reservation(4,'validate'),'worker');cmd=[sys.executable,str(s.RUNNER/'campaign.py'),'--action','validate','--length','4','--twist','I','--output',str(case),'--max-new-batches',str(s.BATCHES),'--cpu-budget',str(s.INTERNAL_ALLOWANCE)];pid=s.launch(led,a,cmd,0);active={pid:a}
while active:s.drain(led,active);time.sleep(.02)
assert a['status']=='COMPLETE';led.close()
# Production ledger remains byte-for-byte immutable.
assert (root/'uniform_second_thermal_campaign_run/ledger.json').read_bytes()==raw
out={'status':'PASS design-only extension/short-boundary tests','production_ledger_unchanged':True,'historical_attempt_prefix_preserved':True,'original_terminal_bytes_preserved':True,'old_charge':16207,'new_cap':43200,'remaining_after_extension':26993,'duplicate_extension_rejected':duplicate_rejected,'old_refund_mutation_rejected':refund_rejected,'unsafe_scaled_sequence':unsafe,'safe_bounded_sequence':safe,'configuration_invariant':{'internal_allowance':s.INTERNAL_ALLOWANCE,'maximum_phase_charge_including_slack':s.BATCHES*(s.CPU_CAP+2)+(s.CPU_CAP+2),'full_legacy_request':120,'strict_safe':True},'reservations':reservations,'metadata_integration_cpu':a['terminal_wait4_cpu'],'no_thermal_jobs':True,'resources':{'self_cpu':resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,'children_cpu':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime},'source_sha256':s.sources()};(P/'tests.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
