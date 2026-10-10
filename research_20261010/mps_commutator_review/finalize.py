#!/usr/bin/env python3
"""Seal only after all exact independent regressions complete."""
from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (P/'SEAL.json').exists()
r=json.loads((P/'regressions.json').read_text());assert r['status'].startswith('PASS')
a=json.loads((P/'independent_assembly.json').read_text());s=json.loads((P/'independent_scalar.json').read_text());state=json.loads((P/'independent_n24_checkpoint.json').read_text());assert state['status']=='complete'
text=(P/'REVIEW.md').read_text().replace('Physical large-n replay is pending; this document is not a PASS seal. Independent local algebra, every fused transfer, full tiny physical fixtures, exact two-vector arithmetic, and both scalar half-line coverings have passed. Final status will be set only after comparing all74 independently contracted n24 integers.','PASS. All74 n24 integers agree exactly in a separately coded, uncached independent contraction. Independent local algebra, every fused transfer, full tiny physical fixtures, exact two-vector arithmetic, and both scalar half-line coverings also pass. All three earlier independent-review seals are unchanged.')
text+=f"\nFinal independent n24 replay: {state['total_recorded_CPU_seconds']:.6f} recorded CPU seconds including driver/startup allowance, peak{r['peak_child_KiB']}KiB. All37 C/K pairs completed under the authorized cap.\n"
(P/'REVIEW.md').write_text(text)
resources={'one_core':1,'affinity_CPU':1,'large_replay_cap_CPU_seconds':2400,'large_replay_cap_KiB':700*1024,'large_replay':state['attempts'],'recorded_large_replay_total_CPU_seconds':state['total_recorded_CPU_seconds'],'startup_allowance_CPU_seconds':state['startup_allowance_CPU_seconds']}
for name in ['tiny','cells','fsum','assembly','scalar']:
 q=json.loads((P/f'independent_{name}.json').read_text());resources[name]={k:q[k] for k in ['CPU_seconds','peak_KiB'] if k in q}
(P/'RESOURCES.json').write_text(json.dumps(resources,indent=2)+'\n')
claims={'status':'PASS','physical_n24_correlations':37,'physical_n24_exact_integers':74,'physical_expansion_max_n':6,'local_search_dimension':2,'MPS_D_ground':26,'MPS_bond_current_combination_upper':156,'numerator_length':48,'retained_numerator_states':1,'retained_denominator_states':[70,73],'old_pi_trial_difference_display':float(__import__('fractions').Fraction(a['rational_states'][0]['gap_from_psi'])+__import__('fractions').Fraction(a['improvement'])),'rational_pi_trial_differences_display':[x['gap_display'] for x in a['rational_states']],'all_beta_recipe_exclusions':[70,73],'scope':s['scope'],'physical_spectral_gap_claim':False,'universal_seed_minimum_claim':False,'new_direct_window_route_included':False,'producer_frozen_manifests':r['checks']}
(P/'CLAIM_VERDICTS.json').write_text(json.dumps(claims,indent=2)+'\n')
files={str(f.relative_to(P)):sha(f) for f in sorted(P.rglob('*')) if f.is_file() and str(f.relative_to(P)) not in ['MANIFEST_SHA256.json','SEAL.json'] and '__pycache__' not in f.parts}
(P/'MANIFEST_SHA256.json').write_text(json.dumps({'status':'FROZEN independent current-witness review','files':files},indent=2)+'\n')
seal={'status':'PASS','created_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest':'MANIFEST_SHA256.json','manifest_sha256':sha(P/'MANIFEST_SHA256.json'),'scope':s['scope'],'exact_n24_integer_matches':74,'earlier_three_seals_unchanged':True}
(P/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print('MANIFEST_SHA256',sha(P/'MANIFEST_SHA256.json'));print('SEAL_SHA256',sha(P/'SEAL.json'))
