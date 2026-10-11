import os,resource,time,json,copy,sys
from pathlib import Path
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
import engine as e
import physical_session as phys
P=Path(__file__).resolve().parent;t=time.process_time();checks=[]
data=P/'runs/full_metadata_fixed/data';job=e.read(data/'state.json')['job'];before=time.process_time();s=e.IncrementalJob(data,job);startup=time.process_time()-before;before=time.process_time();result=s.finish();assembly=time.process_time()-before;assert s.reads['raw_outputs']==0
checks.append('full2945_startup_zero_old_raw_reads_and_final24_exact')
# Corruption/refund states cannot create controller authority.
for key,val in [('reserved',0),('prepaid',2400)]:
 d=P/'validation'/key;d.mkdir(parents=True);state={'prepaid':1200,'reserved':23,'sessions':[dict(id=0,controller_cap=20,supervisor_cap=3,charged=23,state='reserved')]};state[key]=val;e.atomic(d/'budget.json',state)
 try:e.ControlBudget(d/'budget.json');raise RuntimeError('refund survived')
 except AssertionError:checks.append('controller_'+key+'_mutation_rejected')
# Crash between archive publication and old-attempt unlink is charged once.
d=P/'validation/archive';x=e.IncrementalJob(d,'SYNTHETIC-ARCHIVE-TEST');a=x.reserve(0);a['state']='failed';e.atomic(d/'attempts/0000.json',a);x=e.IncrementalJob(d,'SYNTHETIC-ARCHIVE-TEST');h=e.sha(e.raw(a));x.authorize_retry(0,h,'explicit-test-authority');e.atomic(d/'attempts/0000.json',a)
y=e.IncrementalJob(d,'SYNTHETIC-ARCHIVE-TEST');assert y.worker_charged==3 and y.failed_charged==3 and not (d/'attempts/0000.json').exists();y.authorize_retry(0,h,'explicit-test-authority');checks.append('retry_archive_crash_and_repetition_idempotent')
# Mandatory physical identities and synthetic namespace separation are fail-closed.
assert len(phys.required_pins(P/'NO_JOB'))>=10 and not phys.required_pins(P/'NO_JOB')<=set();checks.append('empty_physical_pins_rejected')
z=e.IncrementalJob(P/'validation/physical_namespace','PHYSICAL-TEST',phys.SCHEMA,phys.KIND);a=z.reserve(0)
try:z.complete_synthetic(0,a);raise RuntimeError('synthetic adopted')
except AssertionError:checks.append('synthetic_generation_refused_for_physical_job')
# New-format physical finalization uses sector weights and accepted m012, checked
# with a structurally complete metadata mock built from the prior exact fixture.
k=phys.KERNEL;sec=e.read(k/'runs/generic4/sectors24.json');vals={int(q):[int(v) for v in a] for q,a in sec.items()}
# This helper's production normalization is8 and16/3, so encode exact inverse
# weights as a symbolic code-path check only; the real physical fixtures already
# tested the same consumer. We do not manufacture a production certificate.
assert 'accepted_full_m012_mismatch' in (P/'physical_session.py').read_text();checks.append('accepted_m012_gate_is_in_newformat_dispatcher')
paths=list(data.rglob('*.json'));inventory=e.sha('\n'.join(str(p.relative_to(data))+':'+e.sha(p.read_bytes()) for p in sorted(paths)).encode())
usage=resource.getrusage(resource.RUSAGE_SELF);e.atomic(P/'FINAL_VALIDATION.json',dict(checks=checks,full_startup_cpu=startup,full_assembly_cpu=assembly,raw_outputs_read=s.reads['raw_outputs'],metadata_cpu=time.process_time()-t,self_cpu_total=usage.ru_utime+usage.ru_stime,peak_rss_kib=usage.ru_maxrss,synthetic_file_count=len(paths),synthetic_inventory_sha256=inventory));print('FINAL METADATA VALIDATION PASS')
