#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
P=Path(__file__).resolve().parent
assert json.loads((P/'regressions.json').read_text())['status'].startswith('PASS')
for local,manifest,producer in [('inputs','PHYSICAL_MANIFEST_SHA256.json','momentum_extension'),('inputs','SCALAR_MANIFEST_SHA256.json','momentum_extension'),('inputs70','MANIFEST_SHA256.json','singlet_completion')]:
 for name,h in json.loads((P/local/manifest).read_text())['files'].items():assert hashlib.sha256((P.parent.parent/'mps_excited_seed_witnesses'/producer/name).read_bytes()).hexdigest()==h
claims={'status':'PASS independent review','n':24,'numerator_length':48,'full_Hilbert_dimension_denominator':3**24,'full_Hilbert_dimension_numerator':3**48,'retained_numerator_states':1,'transverse_translation_orbit_generators':24,'transverse_Gram_rank':23,'individual_MPS_bond_max':52,'zero_global_raising_norm_exact':True,'finite_n24_ground_singlet_derived':True,'H_eigenstate_assumption_used':False,'independent_H_contraction':'Three single-site channels with separately evaluated periodic seam; no producer two-site insertion tensors read by the contraction engine.','Fourier_unnormalized_norm_factor':24,'Fourier_translation_eigenvalue':'exp(-2 pi i k/24) for positive phase in the vector definition','rows':[],'actual_seed_startup_certified':False,'spectral_gap_claim':False,'scope':'Fixed one-Rayleigh numerator and specified thermal-first whole-cycle delays followed by accepted joint-aware canonical conversion. Remaining intervals are necessary-condition screens, not feasibility certificates.','proof':'REVIEW.md'}
for mode in [48,70]:
 a=json.loads((P/f'independent_scalar{mode}.json').read_text());claims['rows'].append({'retained_denominator_span_dimension':mode,'all_beta_fixed_recipe_exclusion':a['all_beta_exclusion'],'inconclusive_closed_unions':a['inconclusive_closed_unions'],'all_other_beta_nonnegative_excluded':True,'arithmetic':'Independent exact rational outward enclosures'})
(P/'CLAIM_VERDICTS.json').write_text(json.dumps(claims,indent=2)+'\n')
def cost(name):
 s=(P/name).read_text();m=re.search(r'FINAL CPU_seconds=([0-9.]+) peak_KiB=(\d+)',s);assert m;return {'CPU_seconds':float(m[1]),'peak_KiB':int(m[2])}
build=json.loads((P/'independent_build.json').read_text());benchmark=cost('independent_n24_benchmark.log');remaining=cost('independent_n24_remaining.log');actual=benchmark['CPU_seconds']+remaining['CPU_seconds'];assert actual<600
resources={'single_CPU_affinity':1,'physical_and_channel_address_space_limit_MiB':700,'scalar_address_space_limit_MiB':1024,'n24_contraction_CPU_seconds':actual,'n24_contraction_peak_KiB':max(benchmark['peak_KiB'],remaining['peak_KiB']),'independent_build':{k:build[k] for k in ['CPU_seconds','peak_KiB']},'tiny_contractions':{str(n):cost(f'independent_n{n}.log') for n in [2,4,6]},'other_verifiers':{}}
for name in ['independent_fourier','independent_singlet','independent_scalar48','independent_scalar70']:
 a=json.loads((P/(name+'.json')).read_text());resources['other_verifiers'][name]={k:a[k] for k in ['CPU_seconds','peak_KiB']}
(P/'RESOURCES.json').write_text(json.dumps(resources,indent=2)+'\n')
inherit={}
for parent in [P.parent,P.parent/'longitudinal_extension']:
 for name,h in json.loads((parent/'MANIFEST_SHA256.json').read_text())['files'].items():assert hashlib.sha256((parent/name).read_bytes()).hexdigest()==h
 inherit[str(parent.relative_to(P.parent.parent))]={'seal_sha256':hashlib.sha256((parent/'SEAL.json').read_bytes()).hexdigest(),'manifest_sha256':hashlib.sha256((parent/'MANIFEST_SHA256.json').read_bytes()).hexdigest()}
files={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(P.rglob('*')) if f.is_file() and f.relative_to(P).as_posix() not in {'MANIFEST_SHA256.json','SEAL.json','independent_channels'}}
(P/'MANIFEST_SHA256.json').write_text(json.dumps({'scope':'Independent momentum displacement, 48-state screen, derived singlet completion and 70-state screen','inherited_reviews':inherit,'files':files},indent=2)+'\n')
seal={'status':'PASS immutable momentum and spin-completion independent review','sealed_utc':datetime.now(timezone.utc).isoformat(),'manifest_sha256':hashlib.sha256((P/'MANIFEST_SHA256.json').read_bytes()).hexdigest(),'claim_summary':'CLAIM_VERDICTS.json','all_independent_n24_displacements_replayed':True,'earlier_review_integrity_rechecked':True,'all_beta_exclusion':False,'strongest_remaining_closed_window':['539/64','339/32']}
(P/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal))
