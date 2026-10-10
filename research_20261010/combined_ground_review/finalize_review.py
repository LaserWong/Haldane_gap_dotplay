"""Seal completed artifacts after all tests and live dependency checks pass."""
import json,hashlib,datetime,subprocess,sys,re
from pathlib import Path
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
summary=load(HERE/'results/summary.json');assert summary['patches']==42 and summary['selected_orders']==42 and summary['accepted_full_band']==30 and summary['accepted_ground_only']==11
assert summary['frozen_inputs']==len(load(HERE/'INPUT_SHA256.json'))==302
assert load(HERE/'results/bounded_grid_review.json')['total_samples']==21042
assert load(HERE/'results/comparison_review.json')['status'].startswith('PASS')
subprocess.run([sys.executable,str(HERE/'verify_seals.py'),'--live'],check=True)
rows=load(HERE/'results/accepted_certificates.json');ground=load(HERE/'results/ground_only_certificates.json');accepted=[]
from fractions import Fraction as F
for g in sorted({x['g'] for x in rows if x['variant']=='combined'},key=F):
 row=max([x for x in rows if x['g']==g and x['variant']=='combined'],key=lambda x:F(x['all_integer_L_ge2_gap']))
 gr=next(x for x in ground if x['g']==g and x['variant']=='combined')
 accepted.append(dict(g=g,order=row['order'],beta_initial=row['beta'],all_integer_L_ge2_gap=row['all_integer_L_ge2_gap'],gap_display=row['gap_display'],asymptotic_onset=row['onset'],largest_ground_only_gap=gr['all_integer_L_ge2_gap'],largest_ground_only_display=gr['gap_display']))
assert len(accepted)==6 and accepted[-1]['gap_display']==0.023243965748
now=datetime.datetime.now(datetime.timezone.utc);local=now.astimezone(ZoneInfo('America/New_York'))
for name in ['README.md','REVIEW.md']:
 p=HERE/name;s=p.read_text();s=re.sub(r'Updated 2026-10-10 .*? UTC\.',f'Updated {local:%Y-%m-%d %H:%M} America/New_York (EDT, UTC−4) / {now:%H:%M} UTC.',s,count=1);p.write_text(s)
status=dict(status='PASS independent physical-dependency, exact recombination, transport and all-integer-size review',sealed_utc=now.isoformat(),sealed_America_New_York=local.isoformat(),model='Ordinary spin-1/2 square bilayer; unit AF rung; equal straight intralayer g; no crossed bonds',boundary='Periodic positive-direction multiedges, including length-two parallel bonds',scope='Every integer square side L>=2, separately at six listed couplings',finite_volume_unique_ground=True,accepted=accepted,producer_manifest_sha256='452848690e6303fb768b1d48e90b3635a52e46c8f4c8c620f8906d956f0aa2bd',producer_frozen_files=67,checked_prior_review_seals=8,checked_prior_manifest_entries=850,frozen_snapshot_files=302,check_counts=dict(patches=42,selected_orders=42,successful_full_band=30,selected_exact_failures=12,successful_ground_only=11,grid_samples=21042),full_hilbert_dimensions=[str(4**n) for n in [16,32,64]],original_ground_trial_dimensions=[11,29,29],original_space_plus_residual_dimensions_upper=[12,30,30],implicit_filter_plane_dimension_upper=2,filtered_retained_ground_states=1,filtered_support_triplet_number_max=6,retained_low_band_dimensions=[49,97,193],largest_ground_only_still_uses_original_second_moments=True,new_filtered_residual_claim=False,all_beta_exclusion=False,continuous_coupling_claim=False,physical_gap_optimality_claim=False,proof_assistant_verified=False,scalar_independence='Fresh standard-library code, direct physical H-prime traces, exact rational operations and directed 512-bit exponentials; no producer or previous reviewer code imported',resource_limit=dict(cpu_count=1,address_space_bytes=1073741824),next='Parent may publish these sealed discrete-coupling certificates and their dimensional/input qualifications.')
save(HERE/'REVIEW_STATUS.json',status)
files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST_SHA256.json' and '__pycache__' not in str(p)}
# Nested prerequisite manifests are part of this review and must not be omitted.
for p in sorted((HERE/'snapshot').rglob('MANIFEST_SHA256.json')):files[str(p.relative_to(HERE))]=sha(p)
save(HERE/'MANIFEST_SHA256.json',dict(sorted(files.items())))
subprocess.run([sys.executable,str(HERE/'verify_seals.py'),'--live'],check=True)
print('MANIFEST_SHA256',sha(HERE/'MANIFEST_SHA256.json'))
print('REVIEW_STATUS_SHA256',sha(HERE/'REVIEW_STATUS.json'))
