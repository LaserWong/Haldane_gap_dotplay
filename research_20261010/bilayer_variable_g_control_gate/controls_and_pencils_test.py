import os,json,time,copy,shutil,math
from pathlib import Path
from fractions import Fraction as F
import controller as c
import production_admission as a
p=c.P;t=time.process_time();checks=[];childcpu=0

def reject(fn,label):
 try:fn()
 except (AssertionError,ValueError,KeyError,FileNotFoundError,RuntimeError):checks.append(label);return
 raise AssertionError('mutation survived:'+label)

# Strict exit-time output digest verification, including both new weighted fields.
for filename,index in [('result.json.accumulators.json',15),('result.json.accumulators.json',22),('result.json.accumulators.json',23),('chunk.json',None),('targets.jsonl',None),('result.json.schema.json',None)]:
 d=p/'mutations'/f'digest_{len(checks)}';shutil.copytree(p/'runs/chunk_q0',d)
 if index is None:(d/filename).write_text('{}')
 else:
  vals=c.read(d/filename);vals[index]=str(int(vals[index])+1);(d/filename).write_text(json.dumps(vals))
 reject(lambda:c.adopt_completed(d),'digest_reject_'+filename+'_'+str(index))
d=p/'mutations/forged_receipt';shutil.copytree(p/'runs/chunk_q0',d);r=c.read(d/'receipt.json');r['output_sha256']['chunk.json']='0'*64;(d/'receipt.json').write_text(json.dumps(r));reject(lambda:c.adopt_completed(d),'receipt_not_matching_ledger')

# All four independently executed sectors reconstruct both new fields and the prior22.
rows=[]
for name in ['chunk_q0','chunk_q2','chunk_q4','resumed_q6']:
 d,job,v=c.adopt_completed(p/'runs'/name);rows.append(v)
expected={0:1,2:28,4:70,6:28};sums=c.finalize(d,job,expected);full=[sum(sums[q][i] for q in sums) for i in range(24)]
assert full==list(map(int,c.read(p/'runs/generic4/result.json.accumulators.json')))
sectors=c.read(p/'runs/generic4/sectors24.json');assert all(sums[q]==list(map(int,sectors[str(q)])) for q in sums);checks.append('serialized_full24_and_each_sector_exact')
for name,old in [('generic4','generic4'),('generic5','generic5'),('localized4','localized4'),('localized5','localized5'),('symmetrized4','symmetrized4'),('symmetrized5','symmetrized5')]:
 new=c.read(p/'runs'/name/'result.json.accumulators.json');prior=c.read(p.parent/'bilayer_lazy_chunk_hardening/runs'/old/'result.json.accumulators.json');assert new[:22]==prior
checks.append('all_six_prior22_unchanged')

# Reconstruct the physical pencil solely from checkpointed sector integers.
m0,m1,m2low,m3low,m4low,n8,cross,uz,wz=full[15:];m2=m2low+121*n8;m3=m3low+193600*n8+1331*sum(full[:4])+cross;m4=m4low+sum(full[4:10])+14641*sum(full[10:15])
weighted=lambda col,power:sum(q**power*sums[q][col] for q in sums)
pu=weighted(15,1);uu=weighted(15,2);uc=weighted(16,1);uw=weighted(16,2);cw=weighted(17,1)+968*n8;ww=weighted(17,2)+7744*n8
ref=c.read(p/'runs/generic4/pencils.json');assert list(map(int,ref['G']))==[m0,m1,m2]
for row in ref['tests']:
 num,den=row['g_num'],row['g_den'];alpha=F(1)-F(200*num,22*den);beta=F(num,22*den)
 K=[alpha*pu+beta*m1,alpha*uc+beta*m2,alpha*cw+beta*m3];J=[alpha**2*uu+2*alpha*beta*uc+beta**2*m2,alpha**2*uw+alpha*beta*(uz+cw)+beta**2*m3,alpha**2*ww+2*alpha*beta*wz+beta**2*m4]
 assert K==[F(int(x),22*den) for x in row['K_scaled_11']];assert J==[F(int(x),(22*den)**2) for x in row['J_scaled_121']]
checks.append('five_physical_pencils_from_serialized24')

# Versioned schema prohibits silently reading old22 checkpoints.
old=copy.deepcopy(rows[0]);old['schema']='bilayer-moment22-v1';old['values']=old['values'][:22];reject(lambda:c.validate_payload(old,job),'old22_schema_rejected')
old=copy.deepcopy(rows[0]);old['values']=old['values'][:22];reject(lambda:c.validate_payload(old,job),'short24_payload_rejected')
for stage in ['before_write','partial_write','after_rename']:
 dest=p/'recovery'/stage
 for v in rows:
  pid=os.fork()
  if pid==0:c.commit(dest,v,job,stage);os._exit(73)
  _,st,u=os.wait4(pid,0);childcpu+=u.ru_utime+u.ru_stime;assert os.waitstatus_to_exitcode(st)==73;c.commit(dest,v,job);assert c.commit(dest,v,job)=='identical_duplicate'
 assert c.finalize(dest,job,expected)==sums;checks.append(stage+'_process_resume24')
base=p/'recovery/after_rename'
d=p/'mutations/gap';shutil.copytree(base,d);(d/'q2_0_28.json').unlink();reject(lambda:c.finalize(d,job,expected),'coverage_gap')
d=p/'mutations/overlap';shutil.copytree(base,d);v=copy.deepcopy(rows[1]);v['begin']=1;c.commit(d,v,job);reject(lambda:c.finalize(d,job,expected),'coverage_overlap')
d=p/'mutations/truncated';shutil.copytree(base,d);(d/'q0_0_1.json').write_text('{');reject(lambda:c.finalize(d,job,expected),'checkpoint_truncation')
v=copy.deepcopy(rows[0]);v['values'][23]=str(int(v['values'][23])+1);reject(lambda:c.commit(base,v,job),'conflicting_duplicate24')

# Production admission prices the COMPLETE remaining disjoint plan.
L={'hard_cap':21600,'soft_stop':20000,'charged':1200,'controller_reserved':1200,'attempts':[]};args=['chunk','sample','8','6','0','64'];now=time.time();fore=a.forecast(L,args,6,now);assert fore['total_reserved_forecast']==21600 and fore['pending_reserved']==16794
reject(lambda:a.forecast(L,args,6,a.DEADLINE-100),'deadline_full_plan_rejected')
wrong=copy.deepcopy(L);wrong['charged']=1199;reject(lambda:a.forecast(wrong,args,6,now),'budget_refund_rejected')
failed=copy.deepcopy(L);failed['attempts']=[dict(name='failed',args=args,state='abandoned_charged',charged=6,reserved=6)];failed['charged']=1206
reject(lambda:a.forecast(failed,args,6,now),'unexpected_retry_without_authority')
assert a.forecast(failed,args,6,now,True)['total_reserved_forecast']==21600;checks.append('authorized_retry_charged_and_forecasted')
done=copy.deepcopy(failed);done['attempts'][0]['state']='complete';reject(lambda:a.forecast(done,args,6,now),'completed_range_not_readmitted')
plan=a.plan()
for q in [0,2,4,6]:
 pos=0
 for r in [x for x in plan if x['q']==q]:assert r['begin']==pos;pos+=r['count']
 assert pos==next(x['N'] for x in plan if x['q']==q)
checks.append('all2945_plan_ranges_complete_without_support_evaluation')
assert not (p/'UNAUTHORIZED_JOB/PRODUCTION_AUTHORITY.json').exists();checks.append('production_authorization_absent_no_launch')
# Controller death leaves charged reservation and reconciliation records abandonment.
ledger=c.read(p/'BUDGET_LEDGER.json');dead=next(x for x in ledger['attempts'] if x['name']=='death_q6');assert dead['state']=='abandoned_charged' and dead['charged']==3 and dead['reconciled_no_refund'];checks.append('controller_death_stale_reservation_reconciled_no_refund')
c.atomic(p/'CONTROLS_AND_PENCILS_TESTS.json',dict(checks=checks,count=len(checks),controller_cpu=time.process_time()-t,children_wait4_cpu=childcpu,production_forecast=fore));print(json.dumps({'checks':len(checks),'status':'PASS'}))
