import os,time,fcntl,json,copy,math
from pathlib import Path
import controller as c
p=c.P;t=time.process_time();job='process_recovery';truth=c.read(p/'runs/generic4/result.json.accumulators.json');v={'job':job,'sector':0,'begin':0,'end':1,'N':1,'values':truth};checks=[];children_cpu=0
for stage in ['before_write','partial_write','after_rename']:
 d=p/'process_recovery'/stage;pid=os.fork()
 if pid==0:
  c.commit(d,v,job,stage);os._exit(73)
 _,status,u=os.wait4(pid,0);children_cpu+=u.ru_utime+u.ru_stime;assert os.waitstatus_to_exitcode(status)==73
 c.commit(d,v,job);assert c.finalize(d,job,{0:1})[0]==list(map(int,truth));checks.append(stage+'_separate_process_recovery')
# Atomic replace must tolerate abandoned temporary files left by a crash.
d=p/'process_recovery/stale';d.mkdir();(d/'ledger.json.tmp.abandoned').write_text('{');c.atomic(d/'ledger.json',{'reserved':3});assert c.read(d/'ledger.json')=={'reserved':3};checks.append('stale_temporary_does_not_block_atomic_replace')
# Exact job input checks fail before numerical reservation or fork.
c.verify_inputs();old=c.identities;c.identities=lambda:dict(old(),bad='wrong')
try:c.verify_inputs();raise RuntimeError('mutation survived')
except AssertionError:checks.append('pinned_input_mismatch_rejected')
finally:c.identities=old
lock=open(p/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);pid=os.fork()
if pid==0:
 other=open(p/'LOCK','a+')
 try:fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB);os._exit(1)
 except BlockingIOError:os._exit(0)
_,st,u=os.wait4(pid,0);children_cpu+=u.ru_utime+u.ru_stime;assert os.waitstatus_to_exitcode(st)==0;lock.close();checks.append('second_controller_lock_rejected')
# Original interrupted range was reserved and never refunded; resume is a distinct attempt.
l=c.read(p/'BUDGET_LEDGER.json');a={x['name']:x for x in l['attempts']};assert a['interrupted_q6']['charged']==a['resumed_q6']['charged']==3;checks.append('failed_and_resumed_reservations_both_retained')
# Normalize exact22 sector accumulators using rational arithmetic; small full chunks use weight1.
from fractions import Fraction
sums=c.finalize(p/'checkpoints/normal','generic4:'+c.digest((p/'whole').read_bytes()),{0:1,2:28,4:70,6:28})
assert [sum(Fraction(sums[q][i]) for q in sums) for i in range(22)]==list(map(int,truth));checks.append('serialized_final_exact22_equals_physical_fixture')
# Sample rank coverage excludes duplicates and includes the final sequence index.
for q,names,N in [(6,['sample6_a','sample6_b'],169911),(4,['sample4_a','sample4_b'],4495)]:
 rows=[json.loads(x) for name in names for x in (p/'runs'/name/'targets.jsonl').read_text().splitlines()];assert len(set(x['id'] for x in rows))==len(rows)==len(set(x['rank'] for x in rows));assert rows[-1]['id']==N-1
checks.append('sample_unique_ranks_and_final_boundaries')
c.atomic(p/'RECOVERY_PROCESS_TESTS.json',dict(checks=checks,count=len(checks),controller_cpu=time.process_time()-t,children_wait4_cpu=children_cpu));print(checks)
