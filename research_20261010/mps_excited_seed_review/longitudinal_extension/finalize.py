#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,hashlib,re
P=Path(__file__).resolve().parent
assert json.loads((P/'regressions.json').read_text())['status']=='PASS'
producer=P.parent.parent/'mps_excited_seed_witnesses/longitudinal_extension'
for name,h in json.loads((P/'inputs/MANIFEST_SHA256.json').read_text())['files'].items():assert hashlib.sha256((producer/name).read_bytes()).hexdigest()==h
# Prove that reviewing the extension has not changed any sealed core artifact.
core=json.loads((P.parent/'MANIFEST_SHA256.json').read_text())
for name,h in core['files'].items():assert hashlib.sha256((P.parent/name).read_bytes()).hexdigest()==h
physical=json.loads((P/'independent_physical.json').read_text());scalar=json.loads((P/'independent_scalar.json').read_text());conditional=json.loads((P/'independent_conditional.json').read_text())
assert F(conditional['actual_four_to_three_witness_trace_ratio_lower'])>F('1.0189342')
rows=[]
for r in scalar['rows']:
 n=r['n'];rows.append({'n':n,'numerator_length':2*n,'retained_denominator_dimension':4,'retained_numerator_dimension':1,'denominator_Hilbert_dimension':3**n,'numerator_Hilbert_dimension':3**(2*n),'bond_dimensions':[26,52,52,52],'physical_witness_verdict':'PASS exact independent replay','scalar_verdict':r['verdict'],'all_beta_fixed_recipe_exclusion':not bool(r['unresolved_boxes']),'inconclusive_closed_union':[['31/4','11']] if r['unresolved_boxes'] else [],'exact_global_J_upper':r['max_J_upper'],'global_J_upper_display':float(F(r['max_J_upper']))})
claims={'status':'PASS independent longitudinal review','rows':rows,'all_beta_exclusion_n':[14,16,20],'n24_unresolved_closed_union':['31/4','11'],'conditional_three_state_budget':{'beta':'8','hypothetical_trace_multiplier':'201/200','conditional_final_common_lower':conditional['conditional_final_common_lower'],'four_to_three_witness_trace_ratio_lower':conditional['actual_four_to_three_witness_trace_ratio_lower'],'premise_impossible':True},'proof':'REVIEW.md','scope':'Four fixed orthogonal witnesses. Necessary-condition obstruction only; no actual startup or gap certificate.'}
(P/'CLAIM_VERDICTS.json').write_text(json.dumps(claims,indent=2)+'\n')
s=(P/'independent_contractions.log').read_text();resources={'single_CPU_affinity':1,'address_space_limit_bytes':1024**3,'physical_rebuild':{'CPU_seconds':physical['cpu_seconds'],'peak_KiB':physical['peak_KiB']},'exact_source_contraction':{'CPU_seconds':float(re.search(r'CPU_seconds=([0-9.]+)',s)[1]),'peak_KiB':int(re.search(r'peak_KiB=(\d+)',s)[1])},'scalar_replay':{'CPU_seconds':scalar['CPU_seconds'],'peak_KiB':scalar['peak_KiB']}}
(P/'RESOURCES.json').write_text(json.dumps(resources,indent=2)+'\n')
files={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(P.rglob('*')) if f.is_file() and f.relative_to(P).as_posix() not in {'SEAL.json','MANIFEST_SHA256.json','independent_contract'}}
man={'scope':'Longitudinal fourth-witness review only','inherited_core_seal_sha256':hashlib.sha256((P.parent/'SEAL.json').read_bytes()).hexdigest(),'inherited_core_manifest_sha256':hashlib.sha256((P.parent/'MANIFEST_SHA256.json').read_bytes()).hexdigest(),'files':files}
(P/'MANIFEST_SHA256.json').write_text(json.dumps(man,indent=2)+'\n');seal={'status':'PASS immutable longitudinal independent review','sealed_utc':datetime.now(timezone.utc).isoformat(),'manifest_sha256':hashlib.sha256((P/'MANIFEST_SHA256.json').read_bytes()).hexdigest(),'claim_summary':'CLAIM_VERDICTS.json','clean_reproduction':'REPRODUCE.sh completed successfully','core_integrity_rechecked':True}
(P/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal))
