#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage19');assert sha(old/'MANIFEST_SHA256.json')=='c3a433da85b34129895f86618e29c37e872f1ae8402521c2b329bda3f6109012'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text())
pins=json.loads((HERE/'stage20_review_pins.json').read_text());data['stage20_review_pins']=pins;data['stage20_evidence']={}
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','PROOF.md','REVIEW.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','RESULTS.json','STATUS.json','audit.json','result.json','results.json']:
  p=R+directory+'/'+f
  if (ROOT/p).exists():sources[p]=sha(ROOT/p)
 f=next(f for f in ['ACCEPTANCE.json','CLAIM_VERDICTS.json','RESULTS.json','STATUS.json','audit.json','result.json'] if (ROOT/(R+directory+'/'+f)).exists());p=R+directory+'/'+f;data['stage20_evidence'][directory]=dict(primary_source=p,source_sha256=sources[p],verdict=source(p))
p=R+'uniform_proof_guide/MANIFEST_SHA256.json';assert sha(ROOT/p)=='78514331ec4e434bc633dc2c16520e371bace16e1559e32520aa08ceb095dfd1';manifest_check(p);source(p)
for f in ['PROOF_GUIDE.md','DEPENDENCY_MAP.md','EXACT_DATA.json','SOURCE_PINS.json','SELF_CHECK.json','history/ATTEMPT1_NOTE.json','history/SELF_CHECK_ATTEMPT1.json']:
 p=R+'uniform_proof_guide/'+f;sources[p]=sha(ROOT/p)
p=R+'uniform_proof_guide_review/GUIDE_PACKAGE_RESULTS.json';v=source(p);data['stage20_guide_package']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
v=source(R+'uniform_proof_guide/SOURCE_PINS.json')
for p,h in v['consumed_file_sha256'].items():assert sha(ROOT/p)==h;sources[p]=h
for directory,h in {**v['accepted_review_manifests'],**v['producer_manifests']}.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;manifest_check(p);sources[p]=h

p=R+'uniform_alternating_robustness_review/CLAIM_VERDICTS.json';v=source(p);data['stage20_near_uniform_certificates']=[]
for i,c in enumerate(v['claims']):
 data['stage20_near_uniform_certificates'].append(dict(id='stage20_near_uniform_'+str(i),model='periodic_alternating_spin1_chain',Hamiltonian='sum_j[S_(2j-1).S_(2j)+g S_(2j).S_(2j+1)]',designated_first_bond_coefficient=1,parameter_lower_exact=c['g_closed_interval'][0],parameter_upper_exact=c['g_closed_interval'][1],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),eta_radius=c['eta_radius'],integer_cell_min=c['all_integer_cells_at_least'],physical_site_count='2M',physical_Hilbert_dimension='3^(2M)=9^M',all_integer_cells=True,unique_ground_state=c['unique_ground_state'],initialization_cells=16,initialization_physical_sites=32,physical_anchor_sites=64,physical_anchor_Hilbert_dimension=3**64,MPS_bond_dimension=26,trial_span_dimension=1,normalized_beta='49/4',physical_inverse_temperature='beta/c; c=(1+g)/2',finite_Weyl_bridge_cells=[2,15],terminal_cell_base=c['terminal_cell_base'],new_physical_computation=False,optimal_neighborhood_claim=False,primary_source=p,primary_json_pointer=f'/claims/{i}/gap',primary_sha256=sources[p]))
p=R+'uniform_alternating_robustness_review/results.json';v=source(p);data['stage20_near_uniform_scalar']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
p=R+'uniform_alternating_robustness_proposal/MANIFEST_SHA256.json';assert sha(ROOT/p)=='836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd';manifest_check(p);source(p)
p=R+'bilayer_whole_m4_pipeline/MANIFEST_SHA256.json';assert sha(ROOT/p)=='13010f1d1326fd2c76938036b01ce2e912d70f35714a2c473a529910a790a488';manifest_check(p);source(p)
for f in ['ALGEBRA.md','CHECKS.json','BUDGET_LEDGER.json','SOURCE_IDENTITY.json']:
 p=R+'bilayer_whole_m4_pipeline_review/'+f;sources[p]=sha(ROOT/p)
data['stage20_pipeline_scope']=[dict(status='accepted algebra and small fixtures; bounded sample provenance',coupling_exact='11/100',shifted_Hamiltonian='Hprime=Q+(g/2)(C+Cdagger+D)',integer_operator='T=200Hprime=200Q+11(C+Cdagger+D)',Q_meaning='sum of rung triplet projectors',moment_normalization='divide unnormalized T moments by norm_squared*200^k',complete_independent_small_fixtures=6,scalar_moment_orders=[0,1,2,3,4],signed_terms=15,producer_q6_targets_per_phase=512,producer_q4_targets_per_phase=128,independent_q6_exact_checkpoint_targets=64,independent_q4_aggregate_checkpoint_complete=False,independent_repeated_phase_completed=False,full8x4_moments_computed=False,new_energy_endpoint=False,new_gap=False,full_production_admitted=False,producer_general_process_tree_guard_verified=False,review_repaired_process_tree_guard_tests_pass=True,source=R+'bilayer_whole_m4_pipeline_review/STATUS.json')]
p=R+'bilayer_lazy_chunk_hardening_review/PARTIAL22_FINDING.md';sources[p]=sha(ROOT/p)
p=R+'uniform_alternating_positive_transfer_review/CLAIM_VERDICTS.json';v=source(p);data['stage20_positive_cell_certificates']=[]
for i,c in enumerate(v['claims']):
 r=dict(data['stage20_near_uniform_certificates'][0]);r.update(id='stage20_positive_cell_'+str(i),parameter_lower_exact=c['g_closed_interval'][0],parameter_upper_exact=c['g_closed_interval'][1],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),eta_radius=c['eta_radius'],integer_cell_min=c['all_integer_cells_at_least'],unique_ground_state=c['unique_ground_state'],initialization_cells=c['cell_seed'],initialization_physical_sites=c['physical_seed'],physical_anchor_sites=c['own_anchor_physical_length'],physical_anchor_Hilbert_dimension=3**c['own_anchor_physical_length'],finite_Weyl_bridge_cells=[2,c['cell_seed']-1],terminal_cell_base=c['terminal_cell'],positive_cell_interpolation='min(S sqrt(T),T)',main_cell16_frontier=i<4,primary_source=p,primary_json_pointer=f'/claims/{i}/gap',primary_sha256=sources[p]);data['stage20_positive_cell_certificates'].append(r)
p=R+'uniform_alternating_positive_transfer_review/results.json';v=source(p);data['stage20_positive_cell_scalar']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
p=R+'uniform_alternating_positive_transfer/MANIFEST_SHA256.json';assert sha(ROOT/p)=='ea050102bb50eea1a287e7e674de0f43aa091a4fcd17a3d8279870f5e26ab529';manifest_check(p);source(p)
data['preserved_stage19_files']={R+'overview_stage19/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage19_files'][R+'overview_stage19/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage19/overview_data.json')
data.update(snapshot_label='stage20',schema_version=17,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All stage19 scientific data preserved; independently accepted proof guide and final new review scopes only. New positive-cell intervals are independently accepted; cell/physical sizes and engineering-only limitations remain explicit.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
csv_write('stage20_positive_cell_certificates.csv',data['stage20_positive_cell_certificates'])
csv_write('stage20_pipeline_scope.csv',data['stage20_pipeline_scope'])
csv_write('stage20_near_uniform_certificates.csv',data['stage20_near_uniform_certificates'])
print('PASS stage20 preparation',len(data['claims']),len(seals))
