from pathlib import Path
import json,hashlib
from fractions import Fraction as F
P=Path(__file__).resolve().parent
m=json.loads((P/'inputs/MANIFEST_SHA256.json').read_text())
for name,h in m['files'].items():assert hashlib.sha256((P/'inputs'/name).read_bytes()).hexdigest()==h
assert (P/'inputs/local_tensors.json').read_bytes()==(P.parent/'inputs/local_tensors.json').read_bytes()
def parse(name):return {k:int(v) for k,v in (s.split('=') for s in (P/name).read_text().splitlines())}
a=parse('independent_contractions.out');b=parse('inputs/contractions_n24.out');c=parse('../independent_contractions.out')
assert a==b==c and len(a)==48
assert json.loads((P/'independent_physical.json').read_text())['status']=='PASS'
rows=json.loads((P/'independent_scalar.json').read_text())['rows'];saved=json.loads((P/'inputs/exact_witness_data.json').read_text())['rows']
for a,b in zip(rows,saved):
 assert a['n']==b['n'] and b['retained_denominator_span_dimension']==4
 assert F(a['alpha1'])==F(b['alpha_z'])==F(b['alpha1'])
 if a['n']<24:assert not a['unresolved_boxes']
 else:assert a['unresolved_boxes'][0][0]=='31/4' and a['unresolved_boxes'][-1][1]=='11'
conditional=json.loads((P/'independent_conditional.json').read_text());assert conditional['premise_is_impossible']
assert F(conditional['conditional_final_common_lower'])>F(99,100)
assert F(conditional['actual_four_to_three_witness_trace_ratio_lower'])>F(201,200)
out={'status':'PASS','longitudinal_exact_integer_equality_checks':48,'full_physical_fixtures':[2,4,6],'orthogonality':'Sz0, momentum pi versus psi momentum0; all other states disjoint Sz','all_beta_fixed_recipe_exclusion_n':[14,16,20],'n24_inconclusive_closed_union':['31/4','11'],'conditional_budget_premise_disproved':True}
(P/'regressions.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
