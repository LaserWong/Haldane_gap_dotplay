import json,time,copy,shutil,math
from pathlib import Path
import controller as c
p=Path(__file__).resolve().parent;start=time.process_time();job='generic4:'+c.digest((p/'whole').read_bytes());expected={0:1,2:28,4:70,6:28};payload=[];checks=[]
for q,N in expected.items():
 r=p/'runs'/f'chunk4_q{q}';m=c.read(r/'chunk.json');v=c.read(r/'result.json.accumulators.json');assert m['N']==N
 rows=[json.loads(x) for x in (r/'targets.jsonl').read_text().splitlines()];assert sorted(x['rank'] for x in rows)==list(range(N))
 payload.append(dict(job=job,sector=q,begin=0,end=N,N=N,values=v))
assert c.read(p/'runs/resumed_q6/result.json.accumulators.json')==payload[-1]['values']
assert not (p/'runs/interrupted_q6/result.json.accumulators.json').exists()
truth=[sum(int(v['values'][i]) for v in payload) for i in range(22)];assert truth==list(map(int,c.read(p/'runs/generic4/result.json.accumulators.json')))
def rejected(f,label):
 try:f()
 except (AssertionError,ValueError,KeyError,FileNotFoundError):checks.append(label);return
 raise AssertionError('mutation survived:'+label)
for stage in ['before_write','partial_write','after_rename','normal']:
 d=p/'checkpoints'/stage
 for v in payload:
  c.commit(d,v,job,stage if stage!='normal' else None)
  c.commit(d,v,job) # recovery replay of already computed exact payload
  assert c.commit(d,v,job)=='identical_duplicate'
 got=c.finalize(d,job,expected);assert [sum(got[q][i] for q in got) for i in range(22)]==truth;checks.append(stage+'_recovery_exact22')
base=p/'checkpoints/normal'
def clone(name):
 d=p/'mutations'/name;shutil.copytree(base,d);return d
wrong=copy.deepcopy(payload[0]);wrong['job']='wrong';rejected(lambda:c.commit(clone('wrong_job'),wrong,job),'wrong_job')
wrong=copy.deepcopy(payload[0]);wrong['values'][0]='1.5';rejected(lambda:c.commit(clone('malformed_integer'),wrong,job),'malformed_integer')
wrong=copy.deepcopy(payload[0]);wrong['values'][0]=str(int(wrong['values'][0])+1);rejected(lambda:c.commit(clone('conflicting_duplicate'),wrong,job),'conflicting_duplicate')
d=clone('corruption');f=d/'q0_0_1.json';v=c.read(f);v['values'][0]=str(int(v['values'][0])+1);f.write_text(json.dumps(v));rejected(lambda:c.finalize(d,job,expected),'valid_json_corruption')
d=clone('truncation');(d/'q0_0_1.json').write_text('{');rejected(lambda:c.finalize(d,job,expected),'truncation')
d=clone('gap');(d/'q2_0_28.json').unlink();rejected(lambda:c.finalize(d,job,expected),'missing_range')
d=clone('overlap');v=copy.deepcopy(payload[1]);v['begin']=1;c.commit(d,v,job);rejected(lambda:c.finalize(d,job,expected),'overlap')
d=clone('wrong_size');rejected(lambda:c.finalize(d,job,{0:1,2:29,4:70,6:28}),'wrong_sector_size')
# Partial files are diagnostic only; complete union still determines all scalar output.
(base/'orphan.partial').write_text('999999');assert c.finalize(base,job,expected)==c.finalize(p/'checkpoints/normal',job,expected)
# Prove large arithmetic schedules without constructing/evaluating support arrays.
for N,a in [(169911,65536),(4495,1024),(496,127)]:
 assert math.gcd(N,a)==1;inv=pow(a,-1,N)
 for i in [0,1,N//2,N-2,N-1]:assert (inv*((a*i)%N))%N==i
checks+=['small_complete_rank_bijection','large_modular_inverse_boundaries','resumed_numeric_chunk_exact22','incomplete_numeric_chunk_not_committed']
ledger=c.read(p/'BUDGET_LEDGER.json');assert ledger['charged']==10+sum(x['charged'] for x in ledger['attempts']);assert next(x for x in ledger['attempts'] if x['name']=='interrupted_q6')['charged']==3
checks+=['interruption_and_resume_separately_charged','no_refund_ledger']
out={'checks':checks,'count':len(checks),'all22_equal':True,'metadata_cpu':time.process_time()-start,'checkpoint_bytes':sum(x.stat().st_size for x in (p/'checkpoints').rglob('*') if x.is_file())};c.atomic(p/'CHECKPOINT_TESTS.json',out);print(json.dumps(out))
