"""Cross-check finished audit records, summarize scope, and seal this review."""
from independent_math import *
from verify_inputs import check_hashes
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent;R=HERE/'results';SRC=HERE/'snapshot/low_band/frontier_g007_g010'
load=lambda p:json.loads(p.read_text())
check_hashes()
ground=load(R/'ground_replay.json');translation=load(R/'translation_replay.json');patch=load(R/'patch_review.json');accepted=load(R/'accepted_certificates.json');failed=load(R/'selected_failures.json');grid=load(R/'bounded_grid_diagnostic.json');small=load(R/'short_size_review.json')
assert len(ground)==len(translation)==len(patch)==len(grid)==9 and len(accepted)==2 and len(failed)==7
assert load(R/'scalar_summary.json')['status']=='PASS independent exact frontier audit'
assert all(r['ground_width_after_clipping'] for r in patch)
feas=load(SRC/'feasibility_summary.json');assert len(feas)==9
for g in map(F,['7/100','2/25','1/10']):
 tag='g'+str(g).replace('/','d');path=SRC/tag
 selected=[r for r in feas if F(r['g'])==g];assert selected==load(path/'feasibility.json')
 for row in selected:
  nx,ny=row['nx'],row['ny'];gr=load(path/f'block1_{nx}x{ny}_{tag}.json');fr=load(path/f'translated_{nx}x{ny}_{tag}_fourier.json');bins=load(path/f'quadratic_bins_{nx}x{ny}_{tag}.json')
  rho=F(gr['exact_rayleigh'])-F(gr['E00']);r2=F(gr['exact_residual_squared']);a1=F(bins['bins'][1]['lower']);a2=F(bins['bins'][2]['lower'])
  assert F(row['ground_rayleigh_shifted'])==rho and F(row['ground_residual_squared'])==r2
  assert F(row['all_excited_cutoff'])==a1 and F(row['omitted_band_cutoff'])==a2
  assert F(row['ritz_max_upper'])==F(fr['ritz_max_upper'])==max(F(m['theta_upper']) for m in fr['modes'])
  assert F(row['triplet_residual_squared_max'])==F(fr['residual_squared_bound'])==max(F(m['residual_squared_upper']) for m in fr['modes'])
  assert row['ground_identified'] and row['band_separated'] and rho<a1 and F(row['ritz_max_upper'])<a2
  assert F(row['ground_Temple_width'])==r2/(a2-rho)
assert load(SRC/'frontier_summary.json')==[load(SRC/tag/'frontier_results.json') for tag in ['g7d100','g2d25','g1d10']]
assert {r['order']:F(r['all_integer_L_ge2_gap']) for r in accepted}=={'xty':F(9272103501,10**12),'txy':F(24790852531,10**12)}
assert sum(r['sample_count'] for r in grid)==4509 and all(r['accepted_float_proposals']==0 for r in grid if F(r['g'])>F(7,100))
assert F(small['gap'])>F(307810466553,10**12)
(R/'metadata_consistency.json').write_text(json.dumps(dict(status='PASS',feasibility_records=9,global_summary_equal=True,ritz_and_residual_extrema_exact=True),indent=2)+'\n')
now=datetime.now(timezone.utc)
status=dict(status='PASS independent physical, exact arithmetic and all-integer-size review',sealed_utc=now.isoformat(),sealed_local=now.astimezone(ZoneInfo('America/New_York')).isoformat(),model='Ordinary spin-1/2 square bilayer; unit rung exchange; equal straight intralayer g in both directions and layers; no crossed bonds',boundary='Periodic positive-direction multiplicity, including side-two parallel bonds',accepted_g='7/100',scope='Every integer square side L>=2',finite_volume_unique_ground=True,accepted=[{k:r[k] for k in ['g','order','beta_initial','accepted_beta','asymptotic_onset','all_integer_L_ge2_gap','gap_display']} for r in accepted],max_physical_spins=128,max_full_hilbert_dimension=str(4**64),max_ground_trial_dimension=29,max_retained_full_band_dimension=193,check_counts=dict(ground=9,translation=9,complete_band=9,exact_all_size_certificates=2,selected_exact_failures=7,float_grid_samples=4509),uniform_short_size_g_interval=['0','1/10'],uniform_short_size_sides=[2,3,4,5,6,7],new_ground_and_full_translated_moments_independently_replayed=True,geometry_reused_by_verified_prior_source_hash=True,new_endpoints_traces_transport_and_bridges_recomputed=True,floor_clipping_independently_verified=True,physical_and_bosonic_reference_multiplicities_kept_separate=True,producer_manifest_sha256='55b0ddf8e317c6953d0487a26880b075231d7fcc37c5a91a475a83b5a71dcb47',producer_frozen_file_count=70,proof_assistant_verified=False,bounded_diagnostics=dict(couplings=['2/25','1/10'],beta_min='5',beta_max='30',beta_step='1/20',orders=['xyt','xty','txy'],successful_proposals=0,all_beta_exclusion=False,physical_gaplessness_claim=False),qualifications=['No continuous-coupling global gap claim','No arbitrary-aspect-ratio or infinite-volume uniqueness claim','No all-beta exclusion or optimality claim','Floating scan is diagnostic only; g=.07 acceptance is exact-arithmetic and analytic'])
(HERE/'REVIEW_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
files={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST_SHA256.json' and '__pycache__' not in p.parts}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(files,indent=2)+'\n')
print('PASS review sealed',len(files),'files',hashlib.sha256((HERE/'MANIFEST_SHA256.json').read_bytes()).hexdigest())
