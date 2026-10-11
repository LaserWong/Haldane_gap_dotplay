import os,json,hashlib,math,resource,fcntl,time,datetime,collections,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent;PKG=ROOT/'bilayer_m4_checkpoint100';D=PKG/'snapshot';LIVE=ROOT/'bilayer_full_m4_production_run_checksum';SRC=ROOT/'bilayer_stable_observer_checksum_fix';E=P/'evidence'
assert os.sched_getaffinity(0)=={7} and resource.getrlimit(resource.RLIMIT_CPU)==(3,3)
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(32768),b''):h.update(b)
 return h.hexdigest()
# Existing lifetime lock is shared across namespaces; no misleading empty /proc proof.
lock=(LIVE/'LOCK').open('r');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert not list(LIVE.glob('CONTINUE_AFTER_*.json'))
manifest=PKG/'MANIFEST_SHA256.json';assert digest(manifest)=='737e312e7c1f1f057cd567a088eeb7be53d30aff87e8fc25f50e138634523318';mp=read(manifest)
for name,h in mp.items():
 assert digest(PKG/name)==h
 dest=E/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/name,dest)
shutil.copyfile(manifest,E/'MANIFEST_SHA256.json')
pins=read(D/'PINNED_INPUTS.json');assert digest(D/'PINNED_INPUTS.json')=='4c9c17ece2714710b83c8f4e975b027dc057da3a51bb9d44671ba869b124f6da' and all(digest(f)==h for f,h in pins.items())
job=sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins)));assert job=='c2c9f79a9d55bbc0867f3ef38103d54cb98fc44c185adc280360ca25a969fd01'
checkpoint=read(D/'CHECKPOINT_READY_100.json');state=read(D/'store/state.json');assert checkpoint==read(LIVE/'CHECKPOINT_READY_100.json') and state==read(LIVE/'store/state.json')
assert state==dict(committed_count=100,job=job,kind='PHYSICAL-FIXED-WITNESS24',worker_charged=492)
assert checkpoint==dict(authorized_cap=100,checkpoint_sha256=sha(raw(state)),job_id=job,requires_root_continuation=True,state=state) and checkpoint['checkpoint_sha256']=='01d7a5098422a5dcb210fff8c77782e57099ff439e9e49b4b323cba06aea2418'
rows=[]
for q,n,w,cap in [(0,1,1,3),(2,496,64,3),(4,4495,16,3),(6,169911,64,6)]:
 for b in range(0,n,w):rows.append(dict(q=q,N=n,begin=b,end=min(n,b+w),cap=cap))
assert len(rows)==2945 and sum(r['cap'] for r in rows)==16800
for dirname in ['attempts','committed','outputs']:assert sorted(f.name for f in (D/'store'/dirname).glob('*.json'))==[f'{i:04d}.json' for i in range(100)]
assert not list((D/'store/attempt_history').glob('*'))
sector={q:[0]*24 for q in [0,2,4,6]};targets={q:[] for q in sector};timing={q:dict(wait4=0.,setup=0.,body=0.,GMP=0.,chunks=0,max_wait4=0.) for q in sector};old=ROOT/'bilayer_streaming_observer_failure_review/evidence'
for i in range(100):
 a=read(D/'store/attempts'/f'{i:04d}.json');e=read(D/'store/committed'/f'{i:04d}.json');v=e['payload'];out=D/'store/outputs'/f'{i:04d}.json'
 assert a['id']==i and a['job']==job and a['state']=='complete' and a['charged']==3 and a['range']==rows[i] and a['forecast']==21600
 assert v['id']==i and v['job']==job and v['kind']=='PHYSICAL-FIXED-WITNESS24' and v['schema']=='bilayer-moment24-v1' and v['range']==rows[i]
 assert out.read_bytes()==raw(v) and sha(raw(v))==e['sha256']==a['output_sha256'] and e['receipt_sha256']==sha(raw(a))
 val=v['values'];assert len(val)==24 and all(type(x) is str and str(int(x))==x for x in val)
 if i<63:assert read(old/'store/committed'/f'{i:04d}.json')['payload']['values']==val
 rdir=D/'raw_outputs'/f'{i:04d}_{192+3*(i+1)}';receipt=read(rdir/'receipt.json');assert receipt['identity']==pins and receipt['exit']==0 and receipt['reason'] is None and sha(raw(receipt))==v['worker_receipt_sha256']
 assert 0<=receipt['wait4_cpu']<=rows[i]['cap']
 required={'result.json','result.json.schema.json','result.json.accumulators.json','chunk.json','targets.jsonl'};assert required<=set(receipt['output_sha256'])
 assert all(Path(name).name==name and digest(rdir/name)==h for name,h in receipt['output_sha256'].items())
 assert read(rdir/'result.json.accumulators.json')==val and read(rdir/'result.json.schema.json')==dict(schema='bilayer-moment24-v1',fields=24)
 q=rows[i]['q'];stride={0:1,2:127,4:1024,6:65536}[q];meta=read(rdir/'chunk.json');assert all(meta[k]==rows[i][k] for k in ['q','N','begin','end']) and meta['stride']==stride
 t=[json.loads(x) for x in (rdir/'targets.jsonl').read_text().splitlines()];assert [x['id'] for x in t]==list(range(rows[i]['begin'],rows[i]['end'])) and all(x['rank']==stride*x['id']%rows[i]['N'] for x in t);targets[q]+=t
 z=list(map(int,val));r=read(rdir/'result.json');assert r['complete'] and list(r['terms'].values())==val[:15]
 assert list(map(int,r['moments']))==[z[15],z[16],z[17]+121*z[20],z[18]+193600*z[20]+1331*sum(z[:4])+z[21],z[19]+sum(z[4:10])+14641*sum(z[10:15])]
 for j,x in enumerate(z):sector[q][j]+=x
 tt=timing[q];tt['wait4']+=receipt['wait4_cpu'];tt['setup']+=meta['setup_cpu'];tt['body']+=meta['body_cpu'];tt['GMP']+=r['GMP_cpu_seconds'];tt['chunks']+=1;tt['max_wait4']=max(tt['max_wait4'],receipt['wait4_cpu'])
coverage={q:len(t) for q,t in targets.items()};assert coverage=={0:1,2:496,4:1456,6:0}
for q,t in targets.items():assert len(set(x['rank'] for x in t))==len(t) and [x['id'] for x in t]==list(range(len(t)))
report=read(PKG/'CHECKPOINT_REPORT.json');assert report['partial24_raw_by_sector']=={str(q):list(map(str,a)) for q,a in sector.items()} and report['coverage']=={str(q):v for q,v in coverage.items()}
assert all(abs(report['worker_wait4_by_sector'][str(q)]-timing[q]['wait4'])<1e-9 for q in timing)
control=read(D/'CONTROL_SESSIONS.json');assert control==read(LIVE/'CONTROL_SESSIONS.json') and control['prepaid']==1600 and control['reserved']==711==sum(r['charged'] for r in control['sessions'])
assert [r['id'] for r in control['sessions']]==list(range(9)) and [r['charged'] for r in control['sessions']]==[120,100,120,100,23,120,100,23,5]
assert control['sessions'][:5]==read(D/'CONTROL_SESSIONS_CARRY_FORWARD.json')['sessions'] and control['sessions'][7]['state']==control['sessions'][8]['state']=='complete'
assert read(D/'RETIRED_WORKER_CHARGES.json')['total']==192 and state['worker_charged']==192+100*3
inner=read(D/'sessions/7/RESOURCES.json');outer=read(D/'OUTER_PROGRESS.json');assert inner==report['inner_resources'] and outer==report['outer_progress']
assert inner['exit']==0 and inner['reason'] is None and inner['inherited_lock_verified'] and inner['reaped'] and inner['controller_cpu']<=20 and inner['supervisor_cpu']<=3
assert read(D/'sessions/7/SESSION_SELF_CPU.json')['completed_this_session']==100
assert outer['sessions']==1 and outer['job_id']==job and outer['combined_peak_rss_bytes']<=256*1024**2 and outer['wait4_tree_cpu']>=inner['wait4_tree_cpu']>=sum(t['wait4'] for t in timing.values())
assert 'Traceback' not in (D/'launch.log').read_text()
events=[]
for f in (D/'LIMIT_EVENTS').glob('*.json'):
 r=read(f);assert f.stem==sha(raw(r)) and r['outcome'] in ['fork_before_exec','exec_or_identity_transition','exited_during_observation']
 if r['outcome']=='fork_before_exec':
  assert r['before']==r['after'] and r['expected_role']=='controller' and r['after']['argv'][1]==str(SRC/'production_supervisor.py')
 events.append(r)
assert len(events)==report['observer_transition_records']==12
assert not list(D.glob('CONTINUE_AFTER_*.json')) and not(D/'FULL_MOMENTS.json').exists()
# Entire remaining plan, not a three-operator extrapolation.
remaining_standard=sum(r['cap'] for r in rows[100:]);retry_remaining=3200-192;remaining_sessions=math.ceil((len(rows)-100)/100);future_control=remaining_sessions*23;planned_control=711+future_control
assert (remaining_standard,retry_remaining,remaining_sessions,future_control,planned_control)==(16500,3008,29,667,1378)
assert 1600+492+remaining_standard+retry_remaining==21600 and 711+492==1203 and 1600-planned_control==222
slots=(1600-711)//23+1;remaining_wall=2*(remaining_standard+retry_remaining)+10*(2845+math.ceil(retry_remaining/3))+1600+60*slots+86400
outer_full_wall=2*(16800+3200)+10*(2945+math.ceil(3200/3))+1600+60*70+86400;deadline=datetime.datetime(2026,10,14,tzinfo=datetime.timezone.utc).timestamp();now=time.time();assert now+max(remaining_wall,outer_full_wall)<deadline
assert read(LIVE/'CHECKPOINT_READY_100.json')==checkpoint and read(LIVE/'store/state.json')==state and not list(LIVE.glob('CONTINUE_AFTER_*.json'))
fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
result=dict(status='PASS_INITIAL100_CHECKPOINT_FOR_ROOT_CONTINUATION_DECISION',producer_manifest=digest(manifest),producer_files=len(mp),job=job,checkpoint_digest=checkpoint['checkpoint_sha256'],committed=100,coverage=coverage,all24_signed_chains_verified=True,first63_values_equal_preserved_prior_generation=True,worker_charged=492,control_charged=711,total_charged=1203,retired_worker_charges=192,observer_events=dict(collections.Counter(x['outcome'] for x in events)),verified_role_map_available=False,idle_evidence='Exclusive lifetime LOCK acquired throughout audit, complete100 attempts, reaped inner receipt, unchanged stage state and absent continuation; no cross-namespace process-scan claim.',whole_worker_timing=timing,outer_progress=outer,remaining_standard=remaining_standard,retry_remaining=retry_remaining,remaining_controller_reservations=future_control,planned_control=planned_control,control_spare=222,remaining_wall_forecast=remaining_wall,outer_full_wall_forecast=outer_full_wall,deadline_headroom_seconds=deadline-now-max(remaining_wall,outer_full_wall),no_q6_cost_sample=True,full_moments=False,token_written=False,scientific_workers_launched=0)
(P/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
