import sys,time,copy,json,ast
from pathlib import Path
import controller as c
import pencil24 as pen
import production_finalize as fin
import production_admission as pa
p=c.P;t=time.process_time();checks=[]
rowset=c.read(p/'runs/final_schema_smoke/pencils.json');sec=c.read(p/'runs/final_schema_smoke/sectors24.json')
for row in rowset['tests']:
 v=pen.pencil(sec,row['g_num'],row['g_den']);assert row['physical_K_denominator']==v['K_denominator'] and row['physical_J_denominator']==v['J_denominator'];assert row['K_numerators']==v['K_numerators'] and row['J_numerators']==v['J_numerators'];pen.validate_export(v)
checks.append('final_O2_explicit_denominator_schema_matches_consumer')
assert c.read(p/'runs/final_schema_smoke/result.json.accumulators.json')==c.read(p/'runs/localized4/result.json.accumulators.json');checks.append('O1_O2_all24_fixture_equivalent')
expected=dict(schema='accepted-fixed-witness-m012-v1',T_Q=200,T_A=11,**dict(zip(['m0','m1','m2'],rowset['G'])))
assert fin.assemble(sec,expected,False)['accepted_m012_matched'];wrong=copy.deepcopy(expected);wrong['m2']=str(int(wrong['m2'])+1)
try:fin.assemble(sec,wrong,False);raise RuntimeError('bad control survived')
except AssertionError:checks.append('accepted_low_moment_control_mismatch_rejected')
# Current sample adopts only after all exit hashes/schema/ranges verify.
for name in ['final_sample6','final_sample4']:
 d,job,v=c.adopt_completed(p/'runs'/name);assert len(v['values'])==24
try:c.finalize(d,job,{0:1,2:496,4:4495,6:169911});raise RuntimeError('sample survived full gate')
except AssertionError:checks.append('new24_sample_rejected_as_complete_moment')
# Generated production source demonstrably uses actual plan forecast, not zeros.
s=(p/'production_controller.py').read_text();ast.parse(s);assert 'forecast=production.forecast(ledger,args,cap,time.time()' in s;assert 'admit(ledger,cap,0,0,time.time())' not in s
assert "'admission_forecast':forecast" in s;checks.append('production_entrypoint_wires_nonzero_full_plan_forecast')
# No production authority or job has been created.
assert not (p/'UNAUTHORIZED_JOB').exists();checks.append('no_production_job_initialized')
# Variant pinning is historical, not rebound: old and new witness/rules identical,
# numerical source and executable differ and are preserved independently.
old=c.read(p/'PINNED_INPUTS_PRE_DENOMINATOR.json');new=c.read(p/'PINNED_INPUTS.json');assert old[str(p/'whole')]==c.digest((p/'whole_pre_denominator').read_bytes());assert old[str(p/'whole.cpp')]==c.digest((p/'whole_pre_denominator.cpp').read_bytes());assert new==c.identities();checks.append('both_kernel_epochs_preserved_and_hash_verified')
c.atomic(p/'FINAL_METADATA_TESTS.json',dict(checks=checks,controller_cpu=time.process_time()-t));print(checks)
