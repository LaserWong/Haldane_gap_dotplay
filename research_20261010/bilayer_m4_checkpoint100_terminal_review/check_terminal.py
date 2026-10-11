import os,sys,json,hashlib,resource,fcntl,copy,collections,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent;PKG=ROOT/'bilayer_m4_checkpoint100_terminal';D=PKG/'snapshot';OLD=ROOT/'bilayer_m4_checkpoint100';LIVE=ROOT/'bilayer_full_m4_production_run_checksum';SRC=ROOT/'bilayer_stable_observer_checksum_fix'
assert os.sched_getaffinity(0)=={7} and resource.getrlimit(resource.RLIMIT_CPU)==(6,6)
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(32768),b''):h.update(b)
 return h.hexdigest()
locks=[]
for name in ['LOCK','OUTER_LOCK']:
 f=(LIVE/name).open('r');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);locks.append(f)
assert digest(PKG/'MANIFEST_SHA256.json')=='2d89c43b510c5fd40f8032c827ea21f8739a06dc3064ad3e4c89a7ff3d992c44'
mp=read(PKG/'MANIFEST_SHA256.json')
for name,h in mp.items():
 assert digest(PKG/name)==h
 dest=P/'evidence'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/name,dest)
shutil.copyfile(PKG/'MANIFEST_SHA256.json',P/'evidence/MANIFEST_SHA256.json')
assert digest(OLD/'MANIFEST_SHA256.json')=='737e312e7c1f1f057cd567a088eeb7be53d30aff87e8fc25f50e138634523318'
prior=read(OLD/'MANIFEST_SHA256.json');unchanged=[]
for name,h in prior.items():
 if name.startswith(('snapshot/store/','snapshot/raw_outputs/','snapshot/sessions/','snapshot/LIMIT_EVENTS/')) or name in ['snapshot/PINNED_INPUTS.json','snapshot/CHECKPOINT_READY_100.json','snapshot/PRODUCTION_AUTHORITY.json','snapshot/OUTER_PROGRESS.json','snapshot/OUTER_STARTED_5.json']:
  assert mp[name]==h;unchanged.append(name)
for prefix in ['snapshot/store/','snapshot/raw_outputs/','snapshot/sessions/']:
 assert {k for k in mp if k.startswith(prefix)}=={k for k in prior if k.startswith(prefix)}
pins=read(D/'PINNED_INPUTS.json');assert digest(D/'PINNED_INPUTS.json')=='4c9c17ece2714710b83c8f4e975b027dc057da3a51bb9d44671ba869b124f6da' and all(digest(f)==h for f,h in pins.items())
job=sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins)));assert job=='c2c9f79a9d55bbc0867f3ef38103d54cb98fc44c185adc280360ca25a969fd01'
state=read(D/'store/state.json');ready=read(D/'CHECKPOINT_READY_100.json');token=read(D/'CONTINUE_AFTER_100.json');assert state==read(LIVE/'store/state.json')==ready['state'] and state['committed_count']==100 and state['worker_charged']==492
assert ready['checkpoint_sha256']==sha(raw(state))=='01d7a5098422a5dcb210fff8c77782e57099ff439e9e49b4b323cba06aea2418'
assert token==read(LIVE/'CONTINUE_AFTER_100.json')==dict(job_id=job,checkpoint_sha256=ready['checkpoint_sha256'],explicit_root_approval=True,max_completed_chunks=400)
assert not(D/'CONTINUE_AFTER_400.json').exists() and not(D/'CHECKPOINT_READY_400.json').exists() and not(D/'FULL_MOMENTS.json').exists()
assert sorted(f.name for f in (D/'store/attempts').glob('*.json'))==[f'{i:04d}.json' for i in range(100)] and all(read(f)['state']=='complete' for f in (D/'store/attempts').glob('*.json'))
control=read(D/'CONTROL_SESSIONS.json');assert control==read(LIVE/'CONTROL_SESSIONS.json') and control['prepaid']==1600 and control['reserved']==716==sum(r['charged'] for r in control['sessions'])
assert [r['charged'] for r in control['sessions']]==[120,100,120,100,23,120,100,23,5,5] and [r['id'] for r in control['sessions']]==list(range(10))
assert control['sessions'][5]['state']=='stopped' and control['sessions'][9]['state']=='complete' and control['sessions'][9]['charged']==5
terminal=read(D/'OUTER_RESULT_5.json');assert terminal['job_id']==job and terminal['reason']=='outer_accounting_or_resource_failure' and terminal['sessions']==1 and terminal['reserved']==120 and terminal['watchdog_reserved']==100
assert terminal['self_cpu']>=read(D/'OUTER_PROGRESS.json')['self_cpu'] and terminal['combined_peak_rss_bytes']<=256*1024**2
assert 'LimitMismatch: unexpected_stable_executable_or_command' in (D/'launch.log').read_text()
new_events={k for k in mp if k.startswith('snapshot/LIMIT_EVENTS/')} - {k for k in prior if k.startswith('snapshot/LIMIT_EVENTS/')};assert new_events=={'snapshot/LIMIT_EVENTS/6edab5e1bf540b7e5cd6e9899204e294fab492211965c57edffbdb48224d5291.json'}
event=read(PKG/next(iter(new_events)));assert sha(raw(event))=='6edab5e1bf540b7e5cd6e9899204e294fab492211965c57edffbdb48224d5291'
assert event['outcome']=='mismatch' and event['reason']=='unexpected_stable_executable_or_command' and event['expected_role']=='supervisor' and event['pid']==112
assert event['before']==event['after'] and event['after']['argv']==[] and event['after']['ppid']==read(D/'OUTER_STARTED_5.json')['pid']==9
assert event['cpu']==[3,20] and event['address_space']==[64*1024**2,128*1024**2] and event['affinity']=='6'
sys.path.insert(0,str(SRC));import limit_observer
config=dict(python='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3',native=str(ROOT/'bilayer_variable_g_control_gate/whole'),scripts=dict(outer=str(SRC/'outer.py'),supervisor=str(SRC/'production_supervisor.py'),controller=str(SRC/'physical_session.py')))
assert limit_observer.classify(copy.deepcopy(event),config)==event
roles=collections.Counter();native_ids=[]
for key,v in terminal['post_exec_limit_observations'].items():
 if v.get('role')=='external_watchdog':assert v['cpu']==[100,100] and v['address_space']==[64*1024**2,128*1024**2];roles['external_watchdog']+=1;continue
 assert v['outcome']=='verified_post_exec' and v['before']==v['after'] and key==str(v['pid'])+':'+v['after']['start']
 assert limit_observer.classify(copy.deepcopy(v),config)==v;role=v['expected_role'];roles[role]+=1
 if role=='native':
  args=v['after']['argv'];chunk=int(Path(args[3]).name.split('_')[0]);assert 0<=chunk<100;row=read(D/'store/attempts'/f'{chunk:04d}.json')['range']
  assert args==[str(ROOT/'bilayer_variable_g_control_gate/whole'),'chunk','sample',str(LIVE/'raw_outputs'/f'{chunk:04d}_{192+3*(chunk+1)}'),str(ROOT/'bilayer_whole_m4_pipeline'),str(ROOT/'bilayer_brauer_rule_compiler/run'),'3','8',str(row['q']),str(row['begin']),str(row['end']-row['begin'])]
  native_ids.append(chunk)
assert len(native_ids)==len(set(native_ids)) and roles['supervisor']==roles['controller']==roles['external_watchdog']==1
assert 492+716==1208 and 716+29*23==1383 and 1383+220==1603>1600
# Newly authorized partition is design-only here; old job/source stays terminal.
assert 16800+1800+3000==21600 and 3000-492==2508 and 716+220+30*23==1626 and 1800-1626==174
assert read(LIVE/'store/state.json')==state and read(LIVE/'CONTROL_SESSIONS.json')==control
for f in locks:fcntl.flock(f,fcntl.LOCK_UN);f.close()
for name in ['limit_observer.py','outer.py']:shutil.copyfile(SRC/name,P/name)
result=dict(status='PASS_TERMINAL_EVIDENCE_GATE_FAIL_PENDING_INCOMPLETE_IDENTITY_REPAIR',producer_manifest=digest(PKG/'MANIFEST_SHA256.json'),files=len(mp),unchanged_scientific_and_checkpoint_files=len(unchanged),job=job,checkpoint=ready['checkpoint_sha256'],authorized_token_cap=400,actual_committed=100,no_new_scientific_receipts=True,coverage={'q0':1,'q2':496,'q4':1456,'q6':0},worker_charge=492,control_charge=716,total_charge=1208,both_locks_available_and_held=True,namespace_caveat='No cross-namespace empty process-scan assertion.',terminal_self_CPU=terminal['self_cpu'],terminal_tree_CPU=terminal['wait4_tree_cpu'],terminal_wall=terminal['wall'],peak_RSS=terminal['combined_peak_rss_bytes'],verified_roles=dict(roles),verified_native_chunk_ids=sorted(native_ids),failed_tuple=event,interpretation='The frozen classifier deterministically rejects an empty command line although all role limits match. Equal samples with incomplete argv do not prove an unexpected executable. Cause of empty argv is not established.',old_control_forecast_without_new_launcher=1383,old_control_forecast_with_new_launcher=1603,old_control_pool=1600,proposed_new_partition={'standard':16800,'control':1800,'retry':3000,'retired_workers':492,'remaining_retry':2508,'control_forecast':1626,'control_spare':174},no_new_physics_or_fork_tests=True,new_launch_authorized_by_review=False)
(P/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['verified_native_chunk_ids','failed_tuple']},indent=2))
