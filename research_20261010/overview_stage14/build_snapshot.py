#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage13');assert sha(old/'MANIFEST_SHA256.json')=='25c5663d046405f58899a205df1edaa1bd5b3a42b327919b8c9475294a4944fa'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text()) if p.endswith('.json') else (ROOT/p).read_text()
pins={'uniform_second_initialization_review':'3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b','uniform_second_moment_review':'dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de','bilayer_short_bridge_refinement_review':'49bc11944d411a6342f18b3661173fab47c4298d4932a1ce750befe244bc2d7a','bilayer_residual_pencil_review':'a4eec8140e891b53cc9bd4c237c95236dd32a7069180ed9bc9355df82e4060fb','uniform_second_thermal_kernel_review':'401d8d423025b397940aac33b6fc04f0ad59fd0bd046c4a42c9c48d5be3cf183','uniform_second_thermal_campaign_review':'0f1a4c69912e7f5fad566a6633d866dd1c6c563f7d6c532e19c9a96b18505e27'}
SUPERVISOR_PIN='797f9942024ae7d3da835538b044b6f64c154805865191bb070c2e4184f03464'
if SUPERVISOR_PIN:pins['uniform_second_thermal_supervisor_review']=SUPERVISOR_PIN
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;(n:=manifest_check(p));seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','SEAL.json','SOURCE_PROVENANCE.json','LICENSE.upstream']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
data['stage14_review_pins']=pins;data['stage14_evidence']={}
def record(key,p):
 v=source(p);data['stage14_evidence'][key]=dict(primary_source=p,source_sha256=sources[p],verdict=v);return v
for key,directory,f in [('second_initialization','uniform_second_initialization_review','CLAIM_VERDICTS.json'),('second_moment','uniform_second_moment_review','CLAIM_VERDICTS.json'),('short_bridge','bilayer_short_bridge_refinement_review','ACCEPTANCE.json'),('pencil','bilayer_residual_pencil_review','ACCEPTANCE.json'),('kernel','uniform_second_thermal_kernel_review','CLAIM_VERDICTS.json'),('data_plane','uniform_second_thermal_campaign_review','results.json')]:record(key,R+directory+'/'+f)
data['conditional_uniform_certificates']=[]
for key in ['second_initialization','second_moment']:
 r=data['stage14_evidence'][key];v=r['verdict'];data['conditional_uniform_certificates'].append(dict(id='stage14_'+key,model='uniform_periodic_spin1_Heisenberg',unit_bilinear_exchange=1,gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),integer_size_min=v['all_integer_L_at_least'],all_integers_including_odd=True,unique_ground_state=True,evidence_status='CONDITIONAL on eighteen published physical integer-total/error certificates',thermal_beta_exact='49/4',published_thermal_premise_count=18,full_local_physical_rerun=False,locally_recomputed_physical_gap=False,minimum_seed_claim=False,primary_source=r['primary_source'],primary_json_pointer='/gap',primary_sha256=r['source_sha256']))
r=data['stage14_evidence']['short_bridge'];v=r['verdict'];data['bilayer_short_size_certificates']=[]
for i,a in enumerate(v['continuous_positive_bounds']):data['bilayer_short_size_certificates'].append(dict(id=f'stage14_short_bridge_{i}',model='ordinary_spinhalf_bilayer',unit_rung_exchange=1,parameter_lower_exact=a['coupling_interval'][0],parameter_exact=a['coupling_interval'][1],gap_lower_exact=a['gap_lower'],gap_lower_decimal_down_12=floor12(a['gap_lower']),integer_size_min=2,integer_size_max=7,all_integers_including_odd=True,unique_ground_state=True,all_size_certificate=False,trial_dimension=2,primary_source=r['primary_source'],primary_json_pointer=f'/continuous_positive_bounds/{i}/gap_lower',parameter_source_pointer=f'/continuous_positive_bounds/{i}/coupling_interval/1',primary_sha256=r['source_sha256']))
data['stage14_supervisor_included']=bool(SUPERVISOR_PIN)
if SUPERVISOR_PIN:
 for f in ['CLAIM_VERDICTS.json','results.json','test_results.json']:
  if (ROOT/(R+'uniform_second_thermal_supervisor_review/'+f)).exists():record('supervisor_'+f,R+'uniform_second_thermal_supervisor_review/'+f)
data['stage14_scope']=dict(conditional_second_input_only=True,full18_local_physical_rerun=False,locally_accepted_uniform_bounds_replaced=False,all_size_bilayer_frontier_changed=False,complete4x4_H2_fixture=True,full8x4_matrix_included=False,new_pencil_gap=False,active_mutable_campaign_data_included=False,campaign_launched_in_this_snapshot=False,supervisor_finally_reviewed=bool(SUPERVISOR_PIN),original_first_initialization=60,original_second_initialization=36,first_dataset_new_initialization=52)
data['preserved_stage13_files']={R+'overview_stage13/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage13_files'][R+'overview_stage13/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage13/overview_data.json')
data.update(snapshot_label='stage14',schema_version=11,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All locally accepted stage13 records unchanged. Conditional published second-input gaps and finite L2..7 bounds kept in separate datasets; no active mutable campaign or8x4 matrix.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
for name,rows in [('conditional_uniform_certificates.csv',data['conditional_uniform_certificates']),('bilayer_short_size_certificates.csv',data['bilayer_short_size_certificates'])]:csv_write(name,rows)
print('PASS stage14',len(data['claims']),len(seals))
