from pathlib import Path
import json,hashlib
from fractions import Fraction as F
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ground=load(HERE/'results/ground_summary.json');scalar=load(HERE/'results/scalar_summary.json')
assert ground['patches']==ground['exact_negative_witnesses']==21 and ground['independent_inertias']==105
assert scalar['accepted_certificates']==14 and scalar['selected_failures']==7 and scalar['additional_baseline_beta_replays']==8
assert len(load(HERE/'results/dominance_review.json'))==14
assert len(load(HERE/'results/bounded_grid_samples.json'))==10521
assert len(load(HERE/'results/direct_witness_review.json'))==21
best=[]
for r in scalar['best']:
 row={k:r[k] for k in ['g','order','beta_initial','all_integer_L_ge2_gap','asymptotic_onset','accepted_beta']}
 row['status']='newly_replayed_certificate'
 if F(row['g'])==F(1,20):
  row['newly_replayed_endpoint']=row['all_integer_L_ge2_gap'];row['all_integer_L_ge2_gap']=str(F(171822115684,10**12));row['status']='retain_previous_stronger_sealed_certificate'
  row['source']='../tail_comparison_review/REVIEW_STATUS.json'
  row['newly_replayed_beta']=row['beta_initial'];row['beta_initial']='199/20';row['accepted_beta']='199/5';row['asymptotic_onset']=16
 row['gap_display']=f"{float(F(row['all_integer_L_ge2_gap'])):.12f}";best.append(row)
status=dict(status='PASS independent exact certificate review',generated_utc=datetime.now(timezone.utc).isoformat(),model='Ordinary spin-1/2 square bilayer, unit rung coupling, equal straight intralayer g, no crossed bonds',boundary='Periodic weighted positive-direction bonds; length-two parallel edges retained',scope='Every integer square side L>=2 at the listed discrete couplings; unique finite-volume ground state',best=best,
 alternative_g007_xty_gap=str(F(20459331271,10**12)),patches=21,ground_trial_dimensions=[11,29,29],physical_spin_counts=[32,64,128],full_hilbert_dimensions=[2**32,2**64,2**128],retained_ground_states_per_patch=1,retained_complete_bands=[49,97,193],
 exact_negative_witnesses=21,independent_rational_schur_inertias=105,accepted_scalar_records=14,additional_baseline_beta_replays=8,exact_selected_failures=7,same_beta_dominance_records=14,diagnostic_grid_samples=10521,
 new_physical_trial_families=0,new_higher_moments=0,external_even_sector_low_count=1,cutoff_eigenvalues_allowed=True,
 failed_grid_couplings=['2/25','1/10'],failure_scope='beta 5..30 step .05, xyt/xty/txy only; no all-beta or physical-gaplessness conclusion',continuous_coupling_claim=False,auxiliary_interval_export_audited=False,
 producer_freeze=load(HERE/'PRODUCER_FREEZE.json'),maximum_observed_rss_kib=max(ground['maximum_rss_kib'],scalar['maximum_rss_kib']),resource_limits=dict(cpu_affinity_count=1,blas_threads=1,address_space_bytes=1536*1024**2))
(HERE/'REVIEW_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST_SHA256.json' and '__pycache__' not in p.parts}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('SEALED',len(manifest),'files',sha(HERE/'MANIFEST_SHA256.json'))
for r in best:print(r['g'],r['gap_display'],r['status'])
