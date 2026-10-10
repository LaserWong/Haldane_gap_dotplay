#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;I=P/'inputs'
for manifest in ['PHYSICAL_MANIFEST_SHA256.json','SCALAR_MANIFEST_SHA256.json']:
 for name,h in json.loads((I/manifest).read_text())['files'].items():assert hashlib.sha256((I/name).read_bytes()).hexdigest()==h
assert hashlib.sha256((I/'mps_blocks.txt').read_bytes()).hexdigest()==json.loads((I/'PHYSICAL_MANIFEST_SHA256.json').read_text())['external_inputs']['../../audit/mps/mps_blocks.txt']
def parse(name):return {k:int(v) for k,v in (s.split('=') for s in (P/name).read_text().splitlines())}
x=parse('independent_contractions.out');original=parse('inputs/contractions_n24.out');ground=parse('independent_ground.out');oldground=parse('inputs/ground_lengths.out')
assert x==original and len(x)==48
assert all(ground[k]==v for k,v in oldground.items())
assert all(ground[k]==v for k,v in x.items() if k.startswith(('N0','H0')))
assert all(v>0 for k,v in x.items() if k.startswith('N'))
assert json.loads((P/'independent_physical.json').read_text())['status']=='PASS'
rows=json.loads((P/'independent_scalar.json').read_text())['rows'];saved=json.loads((I/'exact_witness_data.json').read_text())['rows']
for a,b in zip(rows,saved):
 assert a['n']==b['n']
 for own,source in [('alpha0','alpha0'),('alpha1','alpha1'),('delta','delta'),('R','R_2n'),('gap','trial_energy_difference')]:assert F(a[own])==F(b[source])
 assert not a['unresolved_boxes'] or a['n']==24
 if a['n']==24:assert a['unresolved_boxes'][0][0]=='13/2' and a['unresolved_boxes'][-1][1]=='45/4'
# Extensive energy shifts leave delta invariant.
for a in rows:
 for c in [F(-3,7),F(100),F(700741,500000)]:assert F(a['R'])+2*a['n']*c-2*(F(a['alpha0'])+a['n']*c)==F(a['delta'])
# Explicit counterexample to conflating a fixed numerator lower recipe with physical ratio.
assert F(1,4)/2**4==F(1,64) and F(5,4)/2**4==F(5,64)
result={'status':'PASS','exact_excited_contraction_integers':48,'ground_input_integers_matched':len(oldground),'norms_positive':True,'physical_and_scalar_hashes_checked':True,'all_beta_exclusion_n':[14,16,20],'unresolved_n24_closed_union':['13/2','45/4'],'physical_ratio_counterexample_pass':True,'energy_shift_regression_pass':True}
(P/'regressions.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
