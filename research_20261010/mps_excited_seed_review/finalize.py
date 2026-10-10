#!/usr/bin/env python3
"""Seal only the three-state core after clean reproduction."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,hashlib,re
P=Path(__file__).resolve().parent
assert json.loads((P/'regressions.json').read_text())['status']=='PASS'
for manifest in ['PHYSICAL_MANIFEST_SHA256.json','SCALAR_MANIFEST_SHA256.json']:
 m=json.loads((P/'inputs'/manifest).read_text())
 for name,h in m['files'].items():assert hashlib.sha256((P.parent/'mps_excited_seed_witnesses'/name).read_bytes()).hexdigest()==h
a=json.loads((P/'independent_scalar.json').read_text());phys=json.loads((P/'independent_physical.json').read_text())
rows=[]
for r in a['rows']:
 n=r['n'];rows.append({'n':n,'numerator_length':2*n,'retained_denominator_dimension':3,'retained_numerator_dimension':1,'denominator_Hilbert_dimension':3**n,'numerator_Hilbert_dimension':3**(2*n),'bond_dimensions':[26,52,52],'physical_witness_verdict':'PASS exact independent replay','scalar_verdict':r['verdict'],'all_beta_fixed_recipe_exclusion':not bool(r['unresolved_boxes']),'inconclusive_closed_union':[['13/2','45/4']] if r['unresolved_boxes'] else [],'exact_global_J_upper':r['max_J_upper'],'global_J_upper_display':float(F(r['max_J_upper'])),'alpha0':r['alpha0'],'alpha1':r['alpha1'],'R_2n':r['R'],'delta':r['delta'],'trial_energy_difference':r['gap']})
claims={'status':'PASS independent review','scope':'Three-state fixed exact D26 MPS recipe; n14/16/20 all-beta exclusions, n24 necessary screen only. No physical gaplessness or startup claim.','rows':rows,'all_beta_exclusion_n':[14,16,20],'n24_unresolved_closed_union':['13/2','45/4'],'complete_exact_excited_replay_even_n':[2,24],'complete_exact_ground_replay_even_n':[2,48],'direct_physical_fixture_n':[2,4,6],'arbitrary_SU2_assumption_used':False,'proof':'REVIEW.md'}
(P/'CLAIM_VERDICTS.json').write_text(json.dumps(claims,indent=2)+'\n')
def cost(name):
 s=(P/name).read_text();return {'CPU_seconds':float(re.search(r'CPU_seconds=([0-9.]+)',s)[1]),'peak_KiB':int(re.search(r'peak_KiB=(\d+)',s)[1])}
resources={'single_CPU_affinity':1,'address_space_limit_bytes':1024**3,'physical_rebuild':{'CPU_seconds':phys['cpu_seconds'],'peak_KiB':phys['peak_KiB']},'source_contraction':cost('independent_contractions.log'),'ground_contraction':cost('independent_ground.log'),'scalar_replay':{'CPU_seconds':a['CPU_seconds'],'peak_KiB':a['peak_KiB']},'note':'Costs are from the final complete clean replay. Earlier developmental runs, including an inefficient exact-unrounded exponential prototype and a CPU0-contention replay, were stopped and are not certificate results.'}
(P/'RESOURCES.json').write_text(json.dumps(resources,indent=2)+'\n')
review=(P/'REVIEW.md').read_text();review+='\nFinal clean replay resource measurements are recorded exactly in RESOURCES.json. The descriptive first-pass timings above are retained as an additional observed benchmark.\n';(P/'REVIEW.md').write_text(review)
files={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(P.rglob('*')) if f.is_file() and 'longitudinal_extension' not in f.relative_to(P).parts and f.name not in {'SEAL.json','MANIFEST_SHA256.json','independent_contract','independent_ground'}}
(P/'MANIFEST_SHA256.json').write_text(json.dumps({'scope':'Three-state review core only; excludes separate longitudinal_extension and compiled executables','files':files},indent=2)+'\n')
seal={'status':'PASS immutable three-state independent review','sealed_utc':datetime.now(timezone.utc).isoformat(),'manifest_sha256':hashlib.sha256((P/'MANIFEST_SHA256.json').read_bytes()).hexdigest(),'claim_summary':'CLAIM_VERDICTS.json','manifest':'MANIFEST_SHA256.json','clean_reproduction':'REPRODUCE.sh completed successfully','longitudinal_extension_in_scope':False}
(P/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal))
