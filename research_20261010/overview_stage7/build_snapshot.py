#!/usr/bin/env python3
"""Explicit extension of immutable stage6. No mathematical research is run."""
import sys; sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: create a new stage instead'
old=R+'overview_stage6/overview_data.json'
data=json.loads((ROOT/old).read_text())
for p,h in data['sources'].items(): assert sha(ROOT/p)==h,p
sources=deepcopy(data['sources']); claims=deepcopy(data['claims']); dims=deepcopy(data['dimensions']); statuses=deepcopy(data['unplotted_status'])
seals=[];accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text())
def source(p):
 b=(ROOT/p).read_bytes();sources[p]=hashlib.sha256(b).hexdigest()
 return json.loads(b) if p.endswith('.json') else b.decode()
for p,h in accepted.items():
 assert sha(ROOT/p)==h,('Unaccepted or changed review seal',p)
 n=manifest_check(p);source(p)
 seals.append(dict(directory=str(Path(p).parent),manifest=p,sha256=h,verified_files=n))
source(old)
preserved={R+'overview_stage6/'+p:sha(ROOT/(R+'overview_stage6/'+p)) for p in json.loads((ROOT/(R+'overview_stage6/MANIFEST_SHA256.json')).read_text())}
preserved[R+'overview_stage6/MANIFEST_SHA256.json']=sha(ROOT/(R+'overview_stage6/MANIFEST_SHA256.json'))

def add(model,value,primary,pointer,proofs,route,kind='point',lo=None,beta=None,onset=None,note='',rank=None):
 gap=str(F(ptr(source(primary),pointer)))
 for p in proofs:source(p)
 r=deepcopy(claims[0]);r.update(id='stage7_'+primary.replace('/','_')+'__'+pointer.replace('/','_'),model=model,parameter='g',parameter_exact=str(F(value)),parameter_lower_exact=None if lo is None else str(F(lo)),parameter_decimal=float(F(value)),parameter_kind=kind,fixed_J_exact=None,unit_coupling='strong bond = 1' if model=='alternating_spin1_chain' else 'rung = 1',gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),size_variable='M (two-spin cells)' if model=='alternating_spin1_chain' else 'L (square side)',integer_size_min=2,unique_finite_volume_ground_state=True,boundary='periodic; positive-direction adjacency multiplicities retained at size 2',evidence_status='independent_review_passed',initial_beta_exact=beta,asymptotic_base_size=onset,primary_source=primary,primary_json_pointer=pointer,primary_sha256=sources[primary],evidence_sources=[primary]+proofs,notes=note,certificate_route=route,numerator_trial_rank=rank,largest_higher_moments_used=model=='ordinary_spinhalf_bilayer',snapshot_stage='stage7',tail_variant=None,bootstrap_order=None,plotted_in_main_figure=kind=='point',proof_family='thermal_bootstrap')
 if pointer.startswith('/results/'):
  r['parameter_source_pointer']=pointer.rsplit('/',1)[0]+'/g'
 elif pointer.startswith('/intervals/') or pointer.startswith('/regimes/'):
  prefix=pointer.rsplit('/',1)[0];r['parameter_source_pointer']=prefix+'/coupling_interval/1';r['parameter_lower_source_pointer']=prefix+'/coupling_interval/0'
 elif pointer=='/all_integer_L_ge2_gap':r['parameter_source_pointer']='/accepted_g'
 elif pointer.startswith('/combined_'):
  r['parameter_source_pointer']='/combined_coupling_interval/1';r['parameter_lower_source_pointer']='/combined_coupling_interval/0'
 elif pointer.startswith('/extension_'):
  r['parameter_source_pointer']='/extension_interval/1';r['parameter_lower_source_pointer']='/extension_interval/0'
 else:raise AssertionError(('Missing exact parameter provenance',pointer))
 claims.append(r);return r

def dimension(model,g,shape,n,proposal,p,pointer,scope,**kwargs):
 source(p)
 row={k:None for k in dims[0]};row.update(model=model,parameter_exact=g,seed_geometry=shape,full_Hilbert_dimension=(9**n if model=='alternating_spin1_chain' else 4**n),proposal_basis_dimension=proposal,support_scope=scope,evidence_source=p,evidence_json_pointer=pointer,evidence_sha256=sources[p],dimer_or_rung_count=n,physical_spin_count=2*n,notes='',numerator_trial_rank=None,implicit_filtered_space_dimension_upper=None,filtered_max_triplet_number=None,original_max_triplet_number=None,total_trial_space_dimension=None,odd_trial_space_dimension=None,fixed_witness_span_dimension=None,comparison_reference_dimension=None)
 row.update(kwargs);dims.append(row);return row

# Joint scalar theorem and discrete chain application, separated by their seals.
p=R+'joint_ratio_review/LEMMA_ACCEPTANCE.json';lemma=source(p);assert lemma['status'].startswith('PASS')
source(R+'joint_ratio_review/GENERAL_LEMMA.md')
p=R+'joint_ratio_review/results/chain_summary.json';summary=source(p);assert summary['status'].startswith('PASS')
candidates=[]
for i,a in enumerate(summary['results']):
 tag=a['g'].replace('/','d');q=R+f'joint_ratio_review/results/chain_review_{tag}.json';d=source(q);s=d['selected_path']
 add('alternating_spin1_chain',a['g'],p,f'/results/{i}/accepted_gap_lower',[q,R+'joint_ratio_review/CHAIN_REVIEW.md'],'joint_ratio_chain',beta=s['initial_beta'],onset=s['asymptotic_cells'],rank=1,note='Discrete certificate; every integer M>=2. Same-base joint-ratio propagation; earlier recipe obstructions retain their own scope.')
 for j,b in enumerate(d['all_paths']):
  gap=min(F(b['M_ge8_gap_lower']),F(d['minimum_short_gap']))
  candidates.append(dict(model='alternating_spin1_chain',g=a['g'],route='joint_ratio',gap_lower_exact=str(gap),gap_decimal_down_12=floor12(gap),initial_beta=b['initial_beta'],asymptotic_onset=b['asymptotic_cells'],time_cycles=b['time_cycles'],canonical_cycles=b['canonical_cycles'],primary_source=q,primary_path_pointer=f'/all_paths/{j}',short_gap_pointer='/minimum_short_gap',source_sha256=sources[q],derivation='minimum of M>=8 path bound and independently accepted M=2..7 minimum'))
p=R+'joint_ratio_review/results/chain_first_moments.json';d=source(p)
dimension('alternating_spin1_chain','7/40;9/50;181/1000;91/500','M=8',8,2,p,'/8','two-vector first-moment numerator combination',numerator_trial_rank=1,expanded_vector_support=d['8']['support'],notes='Two-dimensional first-moment combination on 43,294 physical configurations; the older coordinate search/support count is a separate object.')

# Counted chain comparison; does not presume separated physical low eigenband.
p=R+'chain_low_band_review/SUMMARY.json';summary=source(p);assert summary['status']=='PASS_INDEPENDENT_COUNTED_BAND_AND_ALL_SIZE_REVIEW'
for i,a in enumerate(summary['results']):
 q=R+f"chain_low_band_review/review_g{a['g'].replace('/','d')}.json";d=source(q);s=d['selected_path']
 add('alternating_spin1_chain',a['g'],p,f'/results/{i}/gap_lower',[q,R+'chain_low_band_review/COUNTED_BLOCK_THEOREM.md',R+'chain_low_band_review/README.md'],'counted_chain_low_band',beta=s['initial_beta'],onset=s['asymptotic_cells'],rank=1,note='Every integer M>=2. Counted 13-dimensional P/6548-dimensional Q reference. Does not assume 13 physical eigenvalues below the complement cutoff. Limiting window [8,16].')
 for j,b in enumerate(d['all_paths']):
  candidates.append(dict(model='alternating_spin1_chain',g=a['g'],route='counted_low_band',gap_lower_exact=b['all_M_ge2_gap_lower'],gap_decimal_down_12=floor12(b['all_M_ge2_gap_lower']),initial_beta=b['initial_beta'],asymptotic_onset=b['asymptotic_cells'],time_cycles=b['time_cycles'],canonical_cycles=b['canonical_cycles'],primary_source=q,primary_path_pointer=f'/all_paths/{j}',gap_pointer=f'/all_paths/{j}/all_M_ge2_gap_lower',source_sha256=sources[q],derivation='direct accepted all-integer path bound'))
 dimension('alternating_spin1_chain',a['g'],'M=4',4,1099,q,'/ground','ground search accompanying counted P/Q denominator',retained_low_band_count=1,expanded_vector_support=1099,full_H_applied_support=1107,comparison_reference_dimension=13,notes='One identified ground replaces the corresponding counted-reference term. Twelve comparison triplet terms plus 6548 complement terms complete the trace; they need not be an isolated physical eigenband.')
 dimension('alternating_spin1_chain',a['g'],'M=4',4,13,p,'/moment_review','bare-vacuum-plus-triplet comparison P',comparison_reference_dimension=13,expanded_vector_support=13,full_H_applied_support=173,shifted_H_action_union_support=172,residual_union_support=160,notes='P=13 and Q=6548. Trial-plus-action and unshifted action unions have 173 configurations; these are not the original 1099-dimensional ground search.')
 dimension('alternating_spin1_chain',a['g'],'M=8',8,2,R+'joint_ratio_review/results/chain_first_moments.json','/8','counted-chain largest first-moment numerator',numerator_trial_rank=1,expanded_vector_support=43294,notes='Two-vector combination on 43,294 configurations; no largest-patch complete residual is required.')

# Separate isolated polynomial frontier.
p=R+'bilayer_polynomial_frontier_review/results/SUMMARY.json';s=source(p);assert s['status'].startswith('PASS') and not s['g09_new_gap']
add('ordinary_spinhalf_bilayer',s['accepted_g'],p,'/all_integer_L_ge2_gap',[R+'bilayer_polynomial_frontier_review/PROOF.md',R+'bilayer_polynomial_frontier_review/REVIEW_STATUS.json'],'polynomial_frontier_full_band',beta='177/20',onset=s['asymptotic_onset'],rank=193,note='Isolated .085 full-band certificate; distinct from the full continuous interval certificate. No certified .09 gap.')
for k,(shape,n) in enumerate([('4x4',16),('8x4',32),('8x8',64)]):
 dimension('ordinary_spinhalf_bilayer','17/200',shape,n,s['ground_search_dimensions'][k],p,f'/retained_full_band_dimensions/{k}','discrete polynomial frontier full-band route',retained_low_band_count=s['retained_full_band_dimensions'][k],numerator_trial_rank=193 if k==2 else None,notes='Ground search, physical eigenband count and full Hilbert dimension are separate quantities.')

# Two successive entire-interval extensions and every exact adjacent piece.
for folder,route in [('interval_joint_review','joint_interval'),('interval_range_0085_review','range0085_interval')]:
 p=R+folder+'/results/SUMMARY.json';s=source(p);assert s['accepted'] and s['status'].startswith('PASS')
 proofs=[R+folder+'/REVIEW.md',R+folder+'/REVIEW_STATUS.json']
 add('ordinary_spinhalf_bilayer',s['extension_interval'][1],p,'/extension_all_integer_L_ge2_uniform_gap',proofs,route+'_extension',kind='closed_interval',lo=s['extension_interval'][0],rank=1,note='Uniform throughout the new extension; every integer L>=2.')
 add('ordinary_spinhalf_bilayer',s['combined_coupling_interval'][1],p,'/combined_all_integer_L_ge2_uniform_gap',proofs,'uniform_interval_union',kind='closed_interval',lo='0',rank=1,note='Exact adjacent union, not interpolation of isolated points.')
 for i,a in enumerate(s['intervals']):
  lo,hi=a['coupling_interval'];mode='ground_only' if F(hi)<=F('41/500') else 'denominator_low_band'
  r=add('ordinary_spinhalf_bilayer',hi,p,f'/intervals/{i}/all_integer_L_ge2_gap',proofs,route+'_piece',kind='closed_interval',lo=lo,beta=a['beta_initial'],onset=a['asymptotic_onset'],rank=1,note='One filtered largest numerator; '+mode+' denominator certificate.')
  r['denominator_regime']=mode
 if folder=='interval_range_0085_review':
  for j,a in enumerate(s['regimes']):
   add('ordinary_spinhalf_bilayer',a['coupling_interval'][1],p,f'/regimes/{j}/uniform_gap',proofs,'range0085_regime',kind='closed_interval',lo=a['coupling_interval'][0],rank=1,note='Regime-specific interval bound; not another disjoint piece.')
   for k,(shape,n) in enumerate([('4x4',16),('8x4',32),('8x8',64)]):
    dimension('ordinary_spinhalf_bilayer','<='.join(a['coupling_interval']),shape,n,s['ground_search_dimensions'][k],p,f'/regimes/{j}','continuous .085 pipeline: '+('ground-only denominators' if j==0 else 'complete smaller odd bands'),retained_low_band_count=a['denominator_retained_states'][k] if k<2 else None,numerator_trial_rank=1 if k==2 else None,total_trial_space_dimension=a['total_augmented_trial_dimensions'][k],odd_trial_space_dimension=([48,96,0][k] if j==1 else 0),fixed_witness_span_dimension=(a['denominator_retained_states'][k] if k<2 else 1),implicit_filtered_space_dimension_upper=30 if k==2 else None,filtered_max_triplet_number=6 if k==2 else None,original_max_triplet_number=4 if k==2 else None,notes='59/125 are total ground-search-plus-odd linear dimensions in the final regime. The largest numerator uses <=30; 30 is not a maximum over the whole pipeline.')

# Independently proved projector reference is not a thermal-bootstrap success.
p=R+'nonperturbative_mps_review/CLAIM_VERDICTS.json';s=source(p);assert s['verdict']=='PASS_WITH_EXPLICIT_SCOPE'
for name in ['REVIEW.md','aklt_independent_results.json','uniform_independent_results.json','d26_rebuild_results.json','SEAL.json']:source(R+'nonperturbative_mps_review/'+name)
refs=[dict(model='AKLT_spin1_projector_chain',hamiltonian='H=sum_i P_{total spin 2}(i,i+1)',boundary='periodic',gap_lower_exact='1/10',gap_lower_decimal_down_12='0.100000000000',integer_size_min=5,unique_ground_integer_size_min=3,proof_family='finite_size_projector_criterion',thermal_bootstrap_success=False,full_Hilbert_dimension_formula='3^L',omitted_state_count_formula='3^L-1',MPS_bond_dimension=2,retained_state_count=1,local_proof_matrix_dimension=81,largest_local_positivity_block_dimension=21,primary_source=p,primary_json_pointer='/accepted/2/conditions',source_sha256=sources[p],evidence_sources=[R+'nonperturbative_mps_review/REVIEW.md',R+'nonperturbative_mps_review/aklt_independent_results.json'],normalization_note='Projector coefficient one; bilinear-plus-biquadratic convention 2P2 doubles the gap.',scope_note='Current same-real-factor thermal-transfer sufficiency fails; not universal thermal-transfer impossibility. Periodic L=2 has four ground states and is excluded.')]
for model,status,scope in [('uniform_spin1_Heisenberg_chain','independently_reviewed_fixed_D26_recipe_exclusion','Fixed D26 one-Rayleigh numerator at L=12/16, denominator n=6/8, specified G updates and a one-off delayed canonical conversion after completed positive cycles. Not all MPS, all adaptive methods or physical gaplessness.'),('AKLT_spin1_projector_chain','current_thermal_transfer_sufficiency_fails','Negative realignment witness -1/3 in the current same-real-factor Cartesian construction. Separate projector gap certificate remains valid; universal transfer impossibility is not proved.'),('ordinary_spinhalf_bilayer','third_moment_43D_g009_unreviewed','New H^3/43-dimensional g=.09 proposal has no accepted independent seal in this snapshot and is excluded from certified figures. Frozen cutoff decision; do not auto-promote later work.')]:
 statuses.append(dict(model=model,parameter_exact='9/100' if model=='ordinary_spinhalf_bilayer' else None,status=status,gap_lower_exact=None,evidence_source=p if model!='ordinary_spinhalf_bilayer' else 'parent assignment: explicit unreviewed exclusion',evidence_sha256=sources[p] if model!='ordinary_spinhalf_bilayer' else None,scope=scope,plotted_as_zero_gap=False))

for r in claims:
 r.setdefault('proof_family','thermal_bootstrap')
 if r['parameter_kind']=='point':
  group=[a for a in claims if a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact']]
  r['plotted_in_main_figure']=r is max(group,key=lambda a:(F(a['gap_lower_exact']),a['id']))
 elif r['model']=='ordinary_spinhalf_bilayer':
  r['plotted_in_main_figure']=r['certificate_route']=='uniform_interval_union' and F(r['parameter_exact'])==F('17/200')
for d in dims:
 for k in ['numerator_trial_rank','implicit_filtered_space_dimension_upper','filtered_max_triplet_number','original_max_triplet_number','total_trial_space_dimension','odd_trial_space_dimension','fixed_witness_span_dimension','comparison_reference_dimension']:d.setdefault(k,None)
for s in statuses:
 if s.get('model')=='alternating_spin1_chain':s['scope']+=' Historical recipe/grid result; the counted-band route now certifies isolated g=.2.'
piece_routes=['uniform_interval_piece','filtered_interval_extension_piece','joint_interval_piece','range0085_interval_piece']
data.update(schema_version=4,snapshot_label='stage7',generated_utc=datetime.now(timezone.utc).isoformat(),claims=claims,dimensions=dims,unplotted_status=statuses,sources=sources,review_seals=seals,reference_certificates=refs,chain_candidate_routes=candidates,ordinary_interval_piece_routes=piece_routes,ordinary_interval_piece_count=49,ordinary_interval_endpoint='17/200',ground_only_interval_endpoint='41/500',previous_stage6_sha256=sha(ROOT/old),preserved_stage6_files=preserved,source_commit_reported_by_project='00593ba445c26b1da625c9afe618e85a2550f70e',git_checkout_verified=False,claim_selection='Explicit pinned review seals; stage6 preserved; unreviewed H^3 43D .09 excluded',root_note='Extracted tree has no .git metadata. Reported commit is parent-provided context, not a verified checkout.',joint_ratio_review_included=True,interval_range_0085_included=True,nonperturbative_mps_review_included=True)
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',claims),('trial_dimensions.csv',dims),('unplotted_status.csv',statuses),('ordinary_interval_pieces.csv',[r for r in claims if r.get('certificate_route') in piece_routes]),('latest_point_bounds.csv',[r for r in claims if r['parameter_kind']=='point' and r['plotted_in_main_figure']]),('reference_certificates.csv',refs),('chain_candidate_routes.csv',candidates)]:csv_write(name,rows)
for name in ['tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv']:
 (HERE/name).write_bytes((ROOT/(R+'overview_stage6')/name).read_bytes())
print(json.dumps(dict(status='PASS stage7 extraction',claims=len(claims),dimensions=len(dims),sources=len(sources),review_seals=len(seals),chain_candidate_routes=len(candidates))))
