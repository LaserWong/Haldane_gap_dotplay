#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage10');data=json.loads((old/'overview_data.json').read_text())
assert len(data['claims'])==225
sources=data['sources'];seals=data['review_seals']
def source(p):
 b=(ROOT/p).read_bytes();sources[p]=sha(ROOT/p);return json.loads(b) if p.endswith('.json') else b.decode()
for p,h in sources.items():assert sha(ROOT/p)==h,p
preserved={R+'overview_stage10/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())}
preserved[R+'overview_stage10/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json')
source(R+'overview_stage10/overview_data.json')
for f in ['README.md','MANIFEST.json','materialize.py','VERIFICATION.json']:
 source('reproducibility/stage11_exact_evidence/'+f)
pins={'integer_window_refinement_review':'2bb3672253a96a570aef1afa41d086ec35db3b673d04e3fbc4d27f0a83bf5110','chain_numerator_pair_block_review':'e87cb666a153b3531ebf9654aacb0f20db726a8aa93f6a25375f74d7850629f1','uniform_transfer_moment_review':'aa19d8fd83ab4f094c07b9d047c2cfa3e1201785e82a0170e3c3b0a937a9e028','mps_commutator_review':'9e5b78e1a5ad8c77383773b83d086a5660f20cbe4c8d4df110c2d161490800e0','mps_direct_window_review':'67f8d45934ca4f7e44ca3e8e841615aabd1a27f645ce35311142bcf4bdee04b8','mps_seed_even_completion_review':'838ace735be490199875f759ee35527c68bf888b20c14bafc264a81ad3935b04'}
pins['uniform_cooled_seed_review']='a5b5f3b35d67f69f555455143e8e5c70beaff46aba2469705c3e22eb7c00a5d7'
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','REVIEW_STATUS.json','ACCEPTANCE.json','CLAIM_VERDICTS.json','SEAL.json','SYMMETRY_SCOPE_ERRATUM.md','PRODUCER_PROSE_ERRATUM.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
data['stage11_review_pins']=pins
p=R+'integer_window_refinement_review/ACCEPTANCE.json';s=source(p);assert s['status'].startswith('ACCEPTED_INDEPENDENT')
for i,a in enumerate(s['all_integer_M_ge_2']):
 r=deepcopy(next(r for r in data['claims'] if r['id']=='stage9_chain_above02_'+a['g']))
 r.update(id='stage11_direct_window_'+a['g'],gap_lower_exact=a['gap'],gap_lower_decimal_down_12=floor12(a['gap']),primary_source=p,primary_json_pointer=f'/all_integer_M_ge_2/{i}/gap',parameter_source_pointer=f'/all_integer_M_ge_2/{i}/g',primary_sha256=sources[p],evidence_sources=[p,R+'integer_window_refinement_review/PROOF.md'],certificate_route='direct_time_first_finite_windows',snapshot_stage='stage11',initial_beta_exact=None,asymptotic_base_size=a['onset'],notes='Independent analytic lemma and exact scalar paths; inherited reviewed physical inputs; all integer M>=2; isolated coupling.')
 data['claims'].append(r)
data['finite_size_certificates']=[dict(id='stage11_chain_g025_M2_M16',model='alternating_spin1_chain',parameter_exact='1/4',gap_lower_exact=s['g025']['gap'],gap_lower_decimal_down_12=floor12(s['g025']['gap']),integer_size_min=2,integer_size_max=16,size_variable='M (two-spin cells)',all_size_certificate=False,unique_finite_volume_ground_state=True,primary_source=p,primary_json_pointer='/g025/gap',source_sha256=sources[p],evidence_status='independent_analytic_and_exact_scalar_review',unit_coupling='strong bond = 1',boundary='periodic; positive-direction adjacency multiplicities retained at size 2')]
def record(key,p):
 s=source(p);data[key]=dict(primary_source=p,source_sha256=sources[p],verdict=s,gap_lower_exact=None,not_a_gap_bound=True);return data[key]
record('stage11_integer_window_acceptance',p)
data['stage11_integer_window_acceptance'].pop('not_a_gap_bound');data['stage11_integer_window_acceptance']['aggregate_acceptance_record']=True
record('stage11_producer_prose_erratum',R+'integer_window_refinement_review/PRODUCER_PROSE_ERRATUM.json')
record('stage11_pair_block',R+'chain_numerator_pair_block_review/ACCEPTANCE.json')
record('stage11_transfer_moments',R+'uniform_transfer_moment_review/independent_results.json')
record('stage11_transfer_verdicts',R+'uniform_transfer_moment_review/CLAIM_VERDICTS.json')
record('stage11_mps_current',R+'mps_commutator_review/CLAIM_VERDICTS.json')
record('stage11_mps_direct_window',R+'mps_direct_window_review/summary.json')
record('stage11_mps_even_completion',R+'mps_seed_even_completion_review/summary.json')
data['stage11_pair_block'].update(inherited_vectors_exact_symmetry=False,combined_spans_exact_symmetry=False,only_new_pair_directions_exact_singlets=True,old_route_exclusion_only=True)
data['stage11_transfer_moments'].update(trace_upper_bound_only=True,physical_gap_claim=False,cooling_scan_not_universal=True)
for r in data['unplotted_status']:
 if r['status'] in ['current_operator_branch_excluded','new_numerator_branch_excluded']:
  r['scope']='Historical stage10 exclusion; the explicitly pinned stage11 independent review is now included. Further mutable refinements remain excluded. '+r['scope'];r['historical_superseded']=True
for name in ['stage11_pair_block','stage11_transfer_moments','stage11_mps_current','stage11_mps_direct_window','stage11_mps_even_completion']:
 data['unplotted_status'].append(dict(model='alternating_spin1_chain' if name=='stage11_pair_block' else 'uniform_spin1_chain',status=name,scope='Accepted scoped physical input or fixed-recipe diagnostic; see typed verdict; no positive gap.',parameter_exact=None,gap_lower_exact=None,evidence_source=data[name]['primary_source'],plotted_as_zero_gap=False))
data['unplotted_status'].append(dict(model='uniform_spin1_chain',status='cooled_seed_candidates_excluded_stage11',scope='Ongoing cooled-seed optimization is excluded from this immutable extraction; no candidate is promoted.',parameter_exact=None,gap_lower_exact=None,evidence_source=None,plotted_as_zero_gap=False))
p=R+'uniform_cooled_seed_review/scalar_results.json';v=source(p)
assert v['status'].startswith('PASS')
data['stage11_cooled_review']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
record('stage11_cooled_acceptance',R+'uniform_cooled_seed_review/CLAIM_VERDICTS.json')
data['stage11_cooled_acceptance'].pop('not_a_gap_bound');data['stage11_cooled_acceptance']['aggregate_acceptance_record']=True
data['uniform_large_size_certificates']=[]
for i,a in enumerate(v['rows']):
 data['uniform_large_size_certificates'].append(dict(id='stage11_uniform_cooled_n'+str(a['seed_n']),model='uniform_spin1_heisenberg_chain',gap_lower_exact=a['gap'],gap_lower_decimal_down_12=floor12(a['gap']),integer_size_min=a['seed_n'],integer_size_max=None,size_variable='L (microscopic spins)',all_integers_including_odd=True,unique_finite_volume_ground_state=True,physical_coupling='unit nearest-neighbor bilinear exchange',boundary='periodic',beta_exact=a['beta'],asymptotic_onset=a['asymptotic_from'],primary_source=p,primary_json_pointer=f'/rows/{i}/gap',size_source_pointer=f'/rows/{i}/seed_n',primary_sha256=sources[p],evidence_status='independent_analytic_physical_and_exact_scalar_review',proof_family='thermal_bootstrap',MPS_bond_dimension=26,retained_numerator_states=1,denominator_full_dimension_formula='3^'+str(a['seed_n']),numerator_full_dimension_formula='3^'+str(2*a['seed_n']),claimed_below_minimum=False,minimum_seed_proven=False))
data['unplotted_status']=[r for r in data['unplotted_status'] if r['status']!='cooled_seed_candidates_excluded_stage11']
data.update(snapshot_label='stage11',schema_version=8,generated_utc=datetime.now(timezone.utc).isoformat(),preserved_stage10_files=preserved,claim_selection='All 225 stage10 rows preserved; three stronger all-size chain certificates added; finite M2..16 g=.25 separate; three accepted uniform L>=54/56/60 records separate; immutable independent reviews only.',cooled_seed_candidates_included=False,cooled_seed_independent_review_included=True,historical_mps_windows_superseded=True,main_figure_selection_rule='Strongest eligible isolated point per model/parameter; old row eligibility flags preserved unchanged.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',data['claims']),('finite_size_certificates.csv',data['finite_size_certificates']),('uniform_large_size_certificates.csv',data['uniform_large_size_certificates']),('unplotted_status.csv',data['unplotted_status']),('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure'] and not any(a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'] and F(a['gap_lower_exact'])>F(r['gap_lower_exact']) for a in data['claims'])])]:csv_write(name,rows)
for name in ['trial_dimensions.csv','stage9_chain_dimensions.csv','stage10_bilayer_dimensions.csv','ordinary_interval_pieces.csv','tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv','reference_certificates.csv','chain_candidate_routes.csv','recipe_upper_envelopes.csv','excited_witness_upper_envelopes.csv']:(HERE/name).write_bytes((old/name).read_bytes())
print('PASS: stage11 extracted',len(data['claims']),'all-size rows and one finite-size certificate')
