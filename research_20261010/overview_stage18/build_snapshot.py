#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage17');assert sha(old/'MANIFEST_SHA256.json')=='f4e281b0b923aca9996366f8d56730f88477bf0351e46282b8ea10e0ae4ceac0'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text())
pins={'bilayer_residual_direction_fixture_review':'3d3f16691dd1ce39d880b261f9f3fd46c3103c41dd9ee09b5e7e04c5794b0958','bilayer_residual_direction_outer_gate_review':'ec73cbd52f4e75627a02c258df18f0f00c0c01e1e3012c13372ac13dea4fdd22','bilayer_residual_direction_production_gate_review':'fca0225b1dd1c414b2bb8b42a0db8d799a31683de96296a91a38e7fb9d185ebb','bilayer_complete_residual_direction_58d_review':'13e12855678f844ce419319908087ad05a7de6d5dd547ee2060d4db7ccee1887'}
EXTRA_PINS={'bilayer_residual_direction_58d_algebra_review':'917c9c32ff4d7ca045153de2778bddfb65684335c6a0549b2682251a09f9e90b','uniform_second_thermal_full_review':'792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94'}
pins.update(EXTRA_PINS)
data['stage18_review_pins']=pins;data['stage18_evidence']={}
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','PROOF.md','REVIEW.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','RESULTS.json','audit.json','result.json']:
  p=R+directory+'/'+f
  if (ROOT/p).exists():sources[p]=sha(ROOT/p)
 f=next(f for f in ['ACCEPTANCE.json','CLAIM_VERDICTS.json','RESULTS.json','audit.json','result.json'] if (ROOT/(R+directory+'/'+f)).exists());p=R+directory+'/'+f;data['stage18_evidence'][directory]=dict(primary_source=p,source_sha256=sources[p],verdict=source(p))
p=R+'bilayer_complete_residual_direction_58d_review/FULL_INPUT_SHA256.json';inputs=source(p)
data['stage18_physical_input_hashes']={}
for rel,h in inputs.items():
 q=(ROOT/p).parent/rel;assert sha(q)==h;key=str(q.resolve().relative_to(ROOT));sources[key]=h;data['stage18_physical_input_hashes'][key]=h
data['stage18_producer_complete_row_manifest']='research_20261010/bilayer_residual_direction_production_run/MANIFEST_SHA256.json'
data['stage18_producer_complete_row_files']=manifest_check(data['stage18_producer_complete_row_manifest'])
data['stage18_locally_reproduced_uniform_certificates']=[]
data['stage18_thermal_provenance']={}
data['stage18_scope']=dict(bilayer_new_gap=False,complete58D_physical_matrix_accepted=True,full18_thermal_accepted=False,algebra_endpoint_engineering_PASS=False,mutable_campaign_included=False,prior_conditional_records_historical=True)
p=R+'uniform_second_thermal_full_review/provenance_results.json';provenance=source(p);data['stage18_thermal_provenance']=dict(primary_source=p,source_sha256=sources[p],verdict=provenance)
p=R+'uniform_second_thermal_full_review/progress_results.json';progress=source(p);data['stage18_thermal_cases']=deepcopy(progress['cases']);data['stage18_thermal_progress_source']=p
for f in ['PROVENANCE_INPUT_SHA256.json','INPUT_SHA256.json']:
 p=R+'uniform_second_thermal_full_review/'+f;deps=source(p)
 for q,h in deps.items():
  if '/.replay_snapshot/' not in q:assert sha(ROOT/q)==h;sources[q]=h
p=R+'uniform_second_thermal_full_review/SNAPSHOT_SHA256.json';data['stage18_snapshot_hashes']=source(p)
data['stage18_snapshot_archive']=R+'uniform_second_thermal_full_review/campaign_snapshot.zip';sources[data['stage18_snapshot_archive']]=sha(ROOT/data['stage18_snapshot_archive'])
v=data['stage18_evidence']['uniform_second_thermal_full_review']['verdict'];p=data['stage18_evidence']['uniform_second_thermal_full_review']['primary_source']
for i,c in enumerate(v['locally_discharged_claims']):
 r=deepcopy(data['conditional_uniform_certificates'][i]);r.update(id='stage18_local_uniform_'+str(i),evidence_status='ACCEPTED: all18 physical thermal premises independently reproduced and mapped to exact scalar proof',full_local_physical_rerun=True,locally_recomputed_physical_gap=False,physical_inputs_locally_reproduced=True,thermal_premises_discharged=True,scalar_proof_unchanged=True,primary_source=p,primary_json_pointer=f'/locally_discharged_claims/{i}/gap',primary_sha256=sources[p],historical_scalar_source=data['conditional_uniform_certificates'][i]['primary_source'],provenance_source=data['stage18_thermal_provenance']['primary_source'],MPS_anchor_sites=72,MPS_bond_dimension=26,new_MPS_contraction=False);r.pop('locally_recomputed_physical_gap',None);r['locally_certified_gap']=True;data['stage18_locally_reproduced_uniform_certificates'].append(r)
data['stage18_scope']['full18_thermal_accepted']=True
p=R+'bilayer_residual_direction_58d_algebra_review/ACCEPTANCE.json';v=source(p)
data['stage18_ground_endpoint_certificates']=[]
def signedfloor12(s):
 f=F(s);n=f.numerator*10**12//f.denominator;a=abs(n);return ('-' if n<0 else '')+f'{a//10**12}.{a%10**12:012d}'
for i,c in enumerate(v['results']):
 data['stage18_ground_endpoint_certificates'].append(dict(id='stage18_58D_endpoint_'+str(i),geometry=[8,4],physical_Hilbert_dimension=2**64,ground_search_dimension=58,parameter_exact=c['g'],shifted_ground_lower_exact=c['ground_lower'],shifted_ground_lower_decimal_down_12=signedfloor12(c['ground_lower']),gain_over_fresh57_exact=c['gain_over_fresh57'],unique_global_ground=c['global_ground_identified'],gap_claim=False,primary_source=p,primary_json_pointer=f'/results/{i}/ground_lower',primary_sha256=sources[p]))
data['stage18_algebra_resource_addendum']=R+'bilayer_residual_direction_58d_algebra/RESOURCE_ADDENDUM_SHA256.json';q=data['stage18_algebra_resource_addendum'];assert sha(ROOT/q)=='ecb288368cfc2d2f21a2f0d2ec21974ec203d7481fab8aae4e28d6a2bb23d119';src=source(q)
for name,h in src.items():
 pp=str((Path(q).parent/name));assert sha(ROOT/pp)==h;sources[pp]=h
data['preserved_stage17_files']={R+'overview_stage17/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage17_files'][R+'overview_stage17/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage17/overview_data.json')
data.update(snapshot_label='stage18',schema_version=15,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All stage17 rows preserved. Complete58D physical matrix and separately reviewed scope; both uniform theorems now have all physical inputs locally discharged by the final independent review and exact scalar/MPS72 provenance mapping.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
csv_write('stage18_local_uniform_certificates.csv',data['stage18_locally_reproduced_uniform_certificates'])
csv_write('stage18_thermal_cases.csv',data['stage18_thermal_cases'])
csv_write('stage18_ground_endpoint_certificates.csv',data['stage18_ground_endpoint_certificates'])
print('PASS stage18 preparation',len(data['claims']),len(seals))
