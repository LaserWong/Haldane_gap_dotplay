#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage14');assert sha(old/'MANIFEST_SHA256.json')=='873769e3e99bf338a9b32548df20d89ecf7ce614aa3e68fad10035f91bf0d41e'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text()) if p.endswith('.json') else (ROOT/p).read_text()
pins={'bilayer_complete_H2_8x4_review':'a77330918068b2fcb60a6bdc11412546a4e3fd909a7b393e46c98b62236b654a','bilayer_residual_pencil_optimization_review':'9c6a17ceb920c20f323ccd27751b2d863f264566b0b1c8d46d5db4f2ea50c053','bilayer_split_H2_fixture_review':'7312565327e2b018b62051ddaf555a7f7c08f89376b897a95fc823d7a2a8a083','bilayer_complete_split_H2_8x4_review':'874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5'}
# Only final independently notified immutable seals belong here.
EXTRA_PINS={'uniform_second_thermal_partial_review':'3cfb6832485aa051ca37cf7e4a10dcda54f5bb3bcaeb4597ae65a33f0eee4dc3','bilayer_split_pencil_optimization_review':'fc205510f91902c1c9da6ba9bbdedefe69900a0fb1505fbd541aefe312417381'}
pins.update(EXTRA_PINS)
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','SEAL.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
data['stage15_review_pins']=pins;data['stage15_evidence']={}
def record(key,p):
 v=source(p);data['stage15_evidence'][key]=dict(primary_source=p,source_sha256=sources[p],verdict=v);return v
for key,directory in [('matrix43','bilayer_complete_H2_8x4_review'),('endpoints43','bilayer_residual_pencil_optimization_review'),('split_fixture','bilayer_split_H2_fixture_review'),('matrix57','bilayer_complete_split_H2_8x4_review')]:record(key,R+directory+'/ACCEPTANCE.json')
def signedfloor12(s):
 f=F(s);n=f.numerator*10**12//f.denominator;a=abs(n);return ('-' if n<0 else '')+f'{a//10**12}.{a%10**12:012d}'
data['bilayer_ground_endpoint_certificates']=[]
r=data['stage15_evidence']['endpoints43']
for i,a in enumerate(r['verdict']['physical_endpoints']):
 data['bilayer_ground_endpoint_certificates'].append(dict(id=f'stage15_ground_endpoint43_{i}',geometry=a['shape'],parameter_exact=a['g'],ground_search_dimension=a['basis_dimension'],physical_spin_count=2*a['shape'][0]*a['shape'][1],full_Hilbert_dimension=2**(2*a['shape'][0]*a['shape'][1]),shifted_ground_lower_exact=a['shifted_ground_lower'],downward12_decimal_lower_exact=a['downward12_decimal_lower'],shifted_ground_lower_decimal_down_12=signedfloor12(a['shifted_ground_lower']),unique_global_ground=True,complete_even_singlet_cutoff_required=True,new_all_size_gap=False,primary_source=r['primary_source'],primary_json_pointer=f'/physical_endpoints/{i}/shifted_ground_lower',primary_sha256=r['source_sha256']))
data['stage15_matrix_dimensions']=[dict(geometry=[4,4],physical_spin_count=32,full_Hilbert_dimension=2**32,unsplit_ground_trial_dimension=16,split_ground_trial_dimension=21,retained_denominator_states_in_existing_gap_pipeline=49,existing_gap_pipeline_total_trial_dimension=64,MPS_bond_dimension=None),dict(geometry=[8,4],physical_spin_count=64,full_Hilbert_dimension=2**64,unsplit_ground_trial_dimension=43,split_ground_trial_dimension=57,retained_denominator_states_in_existing_gap_pipeline=97,existing_gap_pipeline_total_trial_dimension=139,MPS_bond_dimension=None)]
data['stage15_scope']=dict(new_full8x4_43D_H2=True,new_full8x4_57D_H2=True,new_all_size_bilayer_gap=False,current_gap_pipeline_search_dimensions_changed=False,float_diagnostic_failures_are_certificates=False,float_diagnostic_failures_universal_nogo=False,conditional_uniform_gap_promoted=False,full18_physical_inputs_accepted=False,mutable_campaign_inputs_included=False,thermal_campaign_resume_authorized_by_snapshot=False)
data['stage15_endpoint57_included']='bilayer_split_pencil_optimization_review' in pins;data['stage15_partial_campaign_review_included']=False
if data['stage15_endpoint57_included']:
 p=R+'bilayer_split_pencil_optimization_review/ACCEPTANCE.json';v=record('endpoints57',p)
 for i,a in enumerate(v['physical_endpoints']):
  data['bilayer_ground_endpoint_certificates'].append(dict(id=f'stage15_ground_endpoint57_{i}',geometry=v['geometry'],parameter_exact=a['g'],ground_search_dimension=v['trial_dimension'],physical_spin_count=v['physical_spins'],full_Hilbert_dimension=int(v['physical_Hilbert_dimension']),shifted_ground_lower_exact=a['ground_lower'],downward12_decimal_lower_exact=a['downward12_decimal_lower'],shifted_ground_lower_decimal_down_12=signedfloor12(a['ground_lower']),gain_over43D_exact=a['gain_over43D'],unique_global_ground=v['unique_global_ground'],complete_even_singlet_cutoff_required=v['full_even_singlet_sector_r2_cutoff'],new_all_size_gap=False,primary_source=p,primary_json_pointer=f'/physical_endpoints/{i}/ground_lower',primary_sha256=sources[p]))
source(R+'bilayer_residual_pencil_optimization_review/snapshot/assessment/ASSESSMENT.md')
data['thermal_partial_cases']=[]
if 'uniform_second_thermal_partial_review' in pins:
 data['stage15_partial_campaign_review_included']=True
 p=R+'uniform_second_thermal_partial_review/CLAIM_VERDICTS.json';v=record('thermal_partial',p)
 record('thermal_partial_outcome',R+'uniform_second_thermal_partial_review/partial_outcome_results.json')
 p=R+'uniform_second_thermal_partial_review/progress_results.json';z=record('thermal_completed_cases',p)
 source(R+'uniform_second_thermal_partial_review/OUTCOME_REVIEW.md')
 for i,a in enumerate(z['cases']):
  case=a['case'];length=int(case.split('_')[0][1:]);seam=case.split('_')[1]
  data['thermal_partial_cases'].append(dict(case=case,length=length,seam=seam,beta_exact='49/4',full_physical_case_accepted=True,published_W_exact_match=a['exact_published_match'],W=a['W'],representatives=a['representatives'],batches=a['batches'],weighted_multiplicity=a['multiplicity'],physical_Hilbert_dimension=3**length,trace_lower_exact=a['lower'],trace_upper_exact=a['upper'],primary_source=p,primary_json_pointer=f'/cases/{i}',primary_sha256=sources[p]))
 for case in v['missing_cases']:
  data['thermal_partial_cases'].append(dict(case=case,length=12,seam=case.split('_')[1],beta_exact='49/4',full_physical_case_accepted=False,published_W_exact_match=False,W=None,representatives=None,batches=None,weighted_multiplicity=None,physical_Hilbert_dimension=3**12,trace_lower_exact=None,trace_upper_exact=None,primary_source=R+'uniform_second_thermal_partial_review/CLAIM_VERDICTS.json',primary_json_pointer='/missing_cases',primary_sha256=sources[R+'uniform_second_thermal_partial_review/CLAIM_VERDICTS.json']))
data['preserved_stage14_files']={R+'overview_stage14/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage14_files'][R+'overview_stage14/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage14/overview_data.json')
data.update(snapshot_label='stage15',schema_version=12,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All stage14 gap and conditional records unchanged. Newly accepted complete bilayer matrices and physical ground endpoints in separate datasets; no new all-size gap. Accepted16/18 partial physical thermal reproduction; conditional gap categories unchanged; no mutable campaign input.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
for name,rows in [('thermal_partial_cases.csv',data['thermal_partial_cases']),('bilayer_ground_endpoint_certificates.csv',data['bilayer_ground_endpoint_certificates']),('stage15_matrix_dimensions.csv',data['stage15_matrix_dimensions'])]:csv_write(name,rows)
print('PASS stage15',len(data['claims']),len(seals))
