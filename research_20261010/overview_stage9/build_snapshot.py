#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage8');data=json.loads((old/'overview_data.json').read_text())
assert len(data['claims'])==209
sources=data['sources'];seals=data['review_seals']
def source(p):
 b=(ROOT/p).read_bytes();sources[p]=sha(ROOT/p);return json.loads(b) if p.endswith('.json') else b.decode()
for p,h in sources.items():assert sha(ROOT/p)==h,p
preserved={R+'overview_stage8/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())}
preserved[R+'overview_stage8/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json')
source(R+'overview_stage8/overview_data.json')
newdirs=['chain_frontier_above_02_review','mps_excited_seed_review/longitudinal_extension','mps_excited_seed_review/momentum_extension','bilayer_g010_diagnostics_review']
for directory in newdirs:
 p=R+directory+'/MANIFEST_SHA256.json';n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=sha(ROOT/p),verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','SEAL.json','CLAIM_VERDICTS.json','REVIEW_STATUS.json','ACCEPTANCE.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
p=R+'chain_frontier_above_02_review/SUMMARY.json';s=source(p);assert s['status'].startswith('PASS')
for i,a in enumerate(s['results']):
 r=deepcopy(data['claims'][0]);r.update(id='stage9_chain_above02_'+a['g'],parameter_exact=a['g'],parameter_decimal=float(F(a['g'])),gap_lower_exact=a['gap_lower'],gap_lower_decimal_down_12=floor12(a['gap_lower']),primary_source=p,primary_json_pointer=f'/results/{i}/gap_lower',parameter_source_pointer=f'/results/{i}/g',primary_sha256=sources[p],evidence_sources=[p,R+'chain_frontier_above_02_review/PROOF.md'],certificate_route='counted_Schur_reference67',snapshot_stage='stage9',initial_beta_exact={'21/100':'83/10','11/50':'171/20','9/40':'87/10'}[a['g']],asymptotic_base_size={'21/100':64,'11/50':128,'9/40':256}[a['g']],notes='Isolated coupling; all integer M>=2; reference67 at M4; unchanged M8 two-vector Rayleigh numerator; no continuous chain interval.',plotted_in_main_figure=True)
 data['claims'].append(r)
p=R+'chain_frontier_above_02_review/physical_premises.json';s=source(p)
data['stage9_chain_dimensions']=dict(source=p,reference_M=4,reference_dimension=s['reference_dimension'],omitted_count=s['omitted_count'],physical_spin_count=8,full_Hilbert_dimension=s['full_dimension'],ground_trial_dimension=1099,full_ground_action_support=1107,weak_action_union=s['full_action_union'],residual_union=s['residual_union'],largest_M=8,largest_physical_spin_count=16,largest_full_Hilbert_dimension=9**8,largest_search_dimension=2,largest_trial_support=43294,largest_retained_numerator_states=1,largest_physical_input_unchanged=True,MPS_bond_dimension=None)
data['mps_extensions']=[]
for extension in ['longitudinal_extension','momentum_extension']:
 p=R+'mps_excited_seed_review/'+extension+'/CLAIM_VERDICTS.json';s=source(p);assert s['status'].startswith('PASS')
 data['mps_extensions'].append(dict(extension=extension,primary_source=p,source_sha256=sources[p],verdict=s,gap_lower_exact=None,not_a_gap_bound=True,necessary_screen_only=True))
p=R+'bilayer_g010_diagnostics_review/REVIEW_STATUS.json';s=source(p);assert s['status']=='PASS'
data['bilayer_g010_diagnostics']=dict(primary_source=p,source_sha256=sources[p],verdict=s,gap_lower_exact=None,new_gap_proof=False,conditional_sensitivity_only=True,unrestricted_M0_M5_optimality=False)
for f in ['exact_result.json','scan_result.json']:source(R+'bilayer_g010_diagnostics_review/'+f)
for model,status,scope,p in [
 ('alternating_spin1_chain','rank195_independent_review_pending','Independent immutable PASS absent at extraction; no scientific promotion.',''),
 ('ordinary_spinhalf_bilayer','g010_scoped_diagnostics_only','8x4 denominator uncertainty; restricted degree-five moment brackets; conditional bounded input sensitivities. No new gap proof.',R+'bilayer_g010_diagnostics_review/REVIEW_STATUS.json'),
 ('ordinary_spinhalf_bilayer','hardcore_pair_commutator_proposed_only','Proposed exact construction awaiting full residual review; no accepted gap extension.','')]:
 data['unplotted_status'].append(dict(model=model,status=status,scope=scope,parameter_exact='1/10' if model=='ordinary_spinhalf_bilayer' else None,gap_lower_exact=None,evidence_source=p or None,plotted_as_zero_gap=False))
data['excited_witness_readme']=data.get('excited_witness_readme','').replace('The separate longitudinal/momentum extensions are outside this snapshot.','Historical core retained; both sealed extensions are included separately in stage9.')
data.update(snapshot_label='stage9',schema_version=6,generated_utc=datetime.now(timezone.utc).isoformat(),preserved_stage8_files=preserved,claim_selection='All209 stage8 rows retained; new immutable independent PASS reviews only; diagnostic recipe bounds separate.',rank195_review_included=False,ongoing_complete_residual_and_current_operator_branches_excluded=True)
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',data['claims']),('trial_dimensions.csv',data['dimensions']),('unplotted_status.csv',data['unplotted_status']),('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure']]),('stage9_chain_dimensions.csv',[data['stage9_chain_dimensions']])]:csv_write(name,rows)
for name in ['ordinary_interval_pieces.csv','tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv','reference_certificates.csv','chain_candidate_routes.csv','recipe_upper_envelopes.csv','excited_witness_upper_envelopes.csv']:(HERE/name).write_bytes((old/name).read_bytes())
print('PASS: stage9 extracted',len(data['claims']),'gap rows')
