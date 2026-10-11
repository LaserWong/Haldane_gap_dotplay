"""Validate finished numerical receipts and commit exact chunks without rerunning them."""
import json,math,copy,time
import controller as c
p=c.P;t=time.process_time();c.verify_inputs();ledger=c.read(p/'BUDGET_LEDGER.json');c.validate_budget(ledger)
wrong=copy.deepcopy(ledger);wrong['charged']-=3
try:c.validate_budget(wrong);raise RuntimeError('budget mutation survived')
except AssertionError:pass
ident=c.identities();core={k:v for k,v in ident.items() if not k.endswith('/controller.py')};committed=[]
for name in ['chunk4_q0','chunk4_q2','chunk4_q4','resumed_q6','sample6_a','sample6_b','sample4_a','sample4_b']:
 r=p/'runs'/name;receipt=c.read(r/'receipt.json');assert receipt['state']=='complete'
 assert {k:v for k,v in receipt['identity'].items() if not k.endswith('/controller.py')}==core
 args=receipt['args'];assert args[0]=='chunk';kind=args[1];nx,q,begin,count=map(int,args[2:]);large=kind=='sample';n=nx*(4 if large else 2);origin=large and q in (4,6);N=math.comb(n-1,q-1) if origin else math.comb(n,q)
 m=c.read(r/'chunk.json');assert (m['q'],m['begin'],m['end'],m['N'])==(q,begin,begin+count,N)
 rows=[json.loads(x) for x in (r/'targets.jsonl').read_text().splitlines()];assert [x['id'] for x in rows]==list(range(begin,begin+count));assert all(x['rank']==m['stride']*x['id']%N for x in rows)
 result=c.read(r/'result.json');assert result['complete'];values=c.read(r/'result.json.accumulators.json');assert list(result['terms'].values())==values[:15]
 job=c.digest(json.dumps({'identity':core,'kind':kind,'nx':nx},sort_keys=True).encode());payload=dict(job=job,sector=q,begin=begin,end=begin+count,N=N,values=values)
 d=p/'adopted'/job;c.commit(d,payload,job);committed.append(dict(name=name,job=job,sector=q,begin=begin,end=begin+count,directory=str(d)))
small=committed[0];sums=c.finalize(small['directory'],small['job'],{0:1,2:28,4:70,6:28});full=[sum(sums[q][i] for q in sums) for i in range(22)];assert full==list(map(int,c.read(p/'runs/generic4/result.json.accumulators.json')))
# Sparse sample cannot pass the complete-coverage gate.
large=committed[4]
try:c.finalize(large['directory'],large['job'],{4:4495,6:169911});raise RuntimeError('partial sample accepted as full')
except AssertionError:pass
c.atomic(p/'ADOPTION.json',{'committed':committed,'small_full22_equal':True,'partial_large_rejected':True,'budget_refund_mutation_rejected':True,'metadata_cpu':time.process_time()-t});print('ADOPTION PASS')
