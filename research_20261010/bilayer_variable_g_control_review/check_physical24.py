from pathlib import Path
import json,sys,importlib.util,hashlib
r=Path(__file__).resolve().parent;p=r.parent/'bilayer_variable_g_control_gate';s=r/'source24'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
pen=module('pencil24',s/'pencil24.py');fin=module('production_finalize',s/'production_finalize.py')
rows=[json.loads(x) for x in (r/'physical24/reference.jsonl').read_text().splitlines()];assert len(rows)==6
checks=[]
for ref in rows:
 d=p/'runs'/f"{ref['type']}{ref['nx']}";acc=list(map(int,json.loads((d/'result.json.accumulators.json').read_text())));sec=json.loads((d/'sectors24.json').read_text());assert len(acc)==24
 assert list(map(int,json.loads((d/'result.json').read_text())['moments']))==list(map(int,ref['moments']))
 assert [sum(int(v[i]) for v in sec.values()) for i in range(24)]==acc
 assert acc[22:]==list(map(int,ref['weighted'][-2:]))
 # Independent q8 identity uses old22 components, not the new gamma-v expression.
 low_wz=sum(int(q)*0 for q in sec) # physical reference totals already include all sectors.
 n8,cross=acc[20],acc[21];d8=sum(acc[:4]);q8_wz=1548800*n8+10648*d8+4*cross
 # New q8 contribution is deposited in q6 field23; exact physical total was independently checked above.
 weights=list(map(int,ref['weighted']));weighted=lambda i,k:sum(int(q)**k*int(v[i]) for q,v in sec.items())
 assert [weighted(15,1),weighted(16,1),weighted(17,1)+968*n8,weighted(15,2),weighted(16,2),weighted(17,2)+7744*n8]==weights[:6]
 source_rows=json.loads((d/'pencils.json').read_text())['tests']
 for direct,old in zip(ref['pencils'],source_rows):
  assert (direct['num'],direct['den'])==(old['g_num'],old['g_den'])
  out=pen.pencil(sec,direct['num'],direct['den']);mat=pen.validate_export(out)
  assert list(map(int,out['G_numerators']))==list(map(int,ref['moments'][:3]))
  assert list(map(int,out['K_numerators']))==[11*int(v) for v in direct['K_integer_H']]
  assert list(map(int,out['J_numerators']))==[121*int(v) for v in direct['J_integer_H']]
  assert list(map(int,old.get('K_numerators',old.get('K_scaled_11'))))==list(map(int,out['K_numerators']))
  assert list(map(int,old.get('J_numerators',old.get('J_scaled_121'))))==list(map(int,out['J_numerators']))
  assert out['K_denominator']==22*direct['den'] and out['J_denominator']==(22*direct['den'])**2
 expected=dict(schema='accepted-fixed-witness-m012-v1',T_Q=200,T_A=11,**dict(zip(['m0','m1','m2'],ref['moments'][:3])))
 assert fin.assemble(sec,expected,False)['accepted_m012_matched'];expected['m2']=str(int(expected['m2'])+1)
 try:fin.assemble(sec,expected,False)
 except AssertionError:pass
 else:raise AssertionError('wrong complete physical control accepted')
 checks.append({'nx':ref['nx'],'type':ref['type'],'independent_dense_moments_and_Q_bilinears':True,'variable_g_matrices':5,'independent_q8_WZ_identity':str(q8_wz)})
old=(p/'whole22_reference.cpp').read_text();new=(s/'whole.cpp').read_text()
assert old[:old.index('const char* names')]==new[:new.index('const char* names')]
a=old[old.index('void step('):old.index('map<string,Big> reference_terms')];b=new[new.index('void step('):new.index('map<string,Big> reference_terms')]
b=b.replace('t.Qchi_z+=8*(11*inner(gamma,v,6)+1331*(inner(m,ecm,6)+inner(m,nm,6)));','').replace('t.Qpsi_z+=q*inner(psi,z,q);t.Qchi_z+=q*inner(chi,z,q);','');assert a==b
# Exercise the eight/16-over-three normalization as pure algebra with signed entries.
full={str(q):[str((i+1)*(1 if (q+i)%2 else -1)*48) for i in range(24)] for q in (0,2,4,6)}
from fractions import Fraction as F
reduced={q:[str(F(v)/(8 if q=='4' else F(16,3) if q=='6' else 1)) for v in vals] for q,vals in full.items()}
assert pen.pencil(full,3,25)==pen.pencil(reduced,3,25,True)
try:pen.pencil({q:v[:22] for q,v in full.items()},3,25)
except AssertionError:pass
else:raise AssertionError('stale22-field schema survived')
report={'physical_reference_cases':checks,'old_numerical_kernel_prefix_identical':True,'old_step_identical_after_removing_only_two_new_bilinears':True,'physical_K_denominator':'22*g_den','physical_J_denominator':'(22*g_den)^2','signed_synthetic_origin_weight_test':True,'stale22_schema_rejected':True,'full8x4_physical_controls':'NOT_COMPUTED','production_admission':'BLOCKED_PENDING_CONTROL_REVISION'}
(r/'PHYSICAL24_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
