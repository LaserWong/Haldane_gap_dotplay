#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage18');assert sha(old/'MANIFEST_SHA256.json')=='9bee857d7ffd20440048adef790f9b564b3a81d76673c206ed3ef80d1d4475c1'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text())
pins={'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f','uniform_n28_second_initialization_review':'e22c642a814744fed23e45e799b58be4d31da7c4e1b341e2d4c39b95bb474ead','uniform_n26_second_coverage_review':'b4e4bc246acb27b63bb51745c23cbd28b7b0928d5d45ad19ddfb3ffe5d6d077d','uniform_n24_second_coverage_review':'9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282','bilayer_connected_rule_compiler_review':'615e4dc7c33f40a65865b66bb395cae8a127c971f1ab1793ef704f8435908a2a','bilayer_cartesian_indexed_review':'8778764242be53f587f68b7416d7cf114cb0182b505089fbd85a7ffe224c1979'}
EXTRA_PINS={'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf','bilayer_brauer_rule_review':'2433ba51a63cba8ade95874f3244dea39a7f1acf0bcfe1a327bfb34c1789cfdb','uniform_small_lengths_completion_review':'b5225681662482e5ed219fe85d0cc9247703b21b183f6e6441dd081b7bc9d984','uniform_direct25_coverage_review':'a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9'}
pins.update(EXTRA_PINS)
data['stage19_review_pins']=pins;data['stage19_evidence']={}
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','PROOF.md','REVIEW.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','RESULTS.json','STATUS.json','audit.json','result.json','results.json']:
  p=R+directory+'/'+f
  if (ROOT/p).exists():sources[p]=sha(ROOT/p)
 f=next(f for f in ['ACCEPTANCE.json','CLAIM_VERDICTS.json','RESULTS.json','STATUS.json','audit.json','result.json'] if (ROOT/(R+directory+'/'+f)).exists());p=R+directory+'/'+f;data['stage19_evidence'][directory]=dict(primary_source=p,source_sha256=sources[p],verdict=source(p))
data['stage19_uniform_initializations']=[];data['stage19_uniform_coverage']=[];data['stage19_uniform_isolated']=[]
p=R+'uniform_smaller_second_initialization_review/CLAIM_VERDICTS.json';v=source(p)
for i,c in enumerate(v['claims']):
 data['stage19_uniform_initializations'].append(dict(id='stage19_init'+str(c['n']),model='untwisted_periodic_uniform_spin1_Heisenberg',unit_bilinear_exchange=1,bootstrap_initialization=c['n'],integer_size_min=c['all_integer_L_at_least'],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),unique_ground_state=c['unique_ground_state'],all_integer_lengths=True,anchor_length=c['anchor_length'],MPS_bond_dimension=26,trial_span_dimension=1,physical_anchor_Hilbert_dimension=3**c['anchor_length'],anchor_energy_convention='H0 is TOTAL energy; shifted H0/N0+aL, no extra factor L',thermal_beta='49/4',minimum_seed_claim=False,primary_source=p,primary_json_pointer=f'/claims/{i}/gap',primary_sha256=sources[p]))
for n in [28,26]:
 p=R+('uniform_n28_second_initialization_review' if n==28 else 'uniform_n26_second_coverage_review')+'/CLAIM_VERDICTS.json';v=source(p)
 data['stage19_uniform_coverage'].append(dict(id='stage19_coverage'+str(n),model='untwisted_periodic_uniform_spin1_Heisenberg',unit_bilinear_exchange=1,bootstrap_initialization=v['bootstrap_initialization'],integer_size_min=v['all_integer_L_at_least'],gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),unique_ground_state=v['unique_ground_state'],all_integer_lengths=True,coverage_only=True,minimum_seed_claim=False,primary_source=p,primary_json_pointer='/gap',primary_sha256=sources[p]))
p=R+'uniform_n24_second_coverage_review/CLAIM_VERDICTS.json';v=source(p);data['stage19_uniform_isolated'].append(dict(id='stage19_isolated24',model='untwisted_periodic_uniform_spin1_Heisenberg',certified_lengths=v['certified_lengths'],gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),unique_ground_state=True,all_integer_tail_claim=False,bootstrap_initialization=30,primary_source=p,primary_json_pointer='/gap',primary_sha256=sources[p]))
p=R+'uniform_direct25_coverage_review/CLAIM_VERDICTS.json';v=source(p)
data['stage19_uniform_coverage'].append(dict(id='stage19_coverage24',model='untwisted_periodic_uniform_spin1_Heisenberg',unit_bilinear_exchange=1,bootstrap_initialization=30,integer_size_min=24,gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),unique_ground_state=True,all_integer_lengths=True,coverage_only=True,minimum_seed_claim=False,primary_source=p,primary_json_pointer='/gap',primary_sha256=sources[p]))
p=R+'uniform_direct25_coverage_review/results.json';v=source(p);data['stage19_direct25_physical']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
p=R+'uniform_direct25_coverage_review/RESOURCE_ANOMALY.json';v=source(p);data['stage19_direct25_resource']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
p=R+'uniform_small_lengths_completion_review/CLAIM_VERDICTS.json';v=source(p)
data['stage19_uniform_coverage'].append(dict(id='stage19_coverage2_0023',model='untwisted_periodic_uniform_spin1_Heisenberg',unit_bilinear_exchange=1,bootstrap_initialization=30,integer_size_min=2,gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),unique_ground_state=True,all_integer_lengths=True,coverage_only=True,minimum_seed_claim=False,primary_source=p,primary_json_pointer='/gap',primary_sha256=sources[p]))
data['stage19_uniform_finite_certificates']=[]
for n,c in v['analytic_small_lengths'].items():
 data['stage19_uniform_finite_certificates'].append(dict(id='stage19_analytic'+n,certified_lengths=[int(n)],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),unique_ground_state=True,proof_kind='exact total-spin decomposition; periodic multiedges retained',all_integer_tail_claim=False,primary_source=p,primary_json_pointer=f'/analytic_small_lengths/{n}/gap',primary_sha256=sources[p]))
p=R+'uniform_small_lengths_completion_review/results.json';v=source(p);data['stage19_small_lengths_physical']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
for i,c in enumerate(v['rows']):
 data['stage19_uniform_finite_certificates'].append(dict(id='stage19_direct'+str(c['L']),certified_lengths=[c['L']],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),unique_ground_state=True,proof_kind='direct physical trial thermal numerator and certified trace upper bound',all_integer_tail_claim=False,MPS_bond_dimension=26,trial_span_dimension=1,physical_Hilbert_dimension=3**c['L'],shifted_total_Rayleigh=c['shifted_total_Rayleigh'],primary_source=p,primary_json_pointer=f'/rows/{i}/gap',length_source_pointer=f'/rows/{i}/L',primary_sha256=sources[p]))
p=R+'uniform_gap_0248_all_sizes_review/CLAIM_VERDICTS.json';v=source(p)
data['stage19_uniform_coverage'].append(dict(id='stage19_coverage2_0248',model='untwisted_periodic_uniform_spin1_Heisenberg',unit_bilinear_exchange=1,bootstrap_initialization=34,integer_size_min=2,gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),unique_ground_state=True,all_integer_lengths=True,coverage_only=True,minimum_seed_claim=False,primary_source=p,primary_json_pointer='/gap',primary_sha256=sources[p]))
p=R+'uniform_gap_0248_all_sizes_review/results.json';v=source(p);data['stage19_strong_all_size']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
for key in ['cached_prefix_4_to25','new_direct26_to33']:
 for i,c in enumerate(v[key]):
  data['stage19_uniform_finite_certificates'].append(dict(id='stage19_strong_direct'+str(c['L']),certified_lengths=[c['L']],gap_lower_exact=v['gap'],gap_lower_decimal_down_12=floor12(v['gap']),unique_ground_state=True,proof_kind='exact stronger physical purity inequality; '+key,all_integer_tail_claim=False,MPS_bond_dimension=26,trial_span_dimension=1,physical_Hilbert_dimension=3**c['L'],primary_source=p,primary_json_pointer='/gap',length_source_pointer=f'/{key}/{i}/L',primary_sha256=sources[p]))
for r in data['stage19_uniform_finite_certificates']:
 if r['certified_lengths'][0]>=4:
  L=r['certified_lengths'][0];r['anchor_length']=48 if r['id']=='stage19_strong_direct24' else L;r['physical_anchor_Hilbert_dimension']=3**r['anchor_length']
  if L==24:
   r['id']='stage19_strong_parity24';r['proof_kind']='inherited parity-resolved thermal purity with physical MPS48 anchor; cached_prefix_4_to25'
data['stage19_uniform_isolated'][0].update(proof_kind='parity-resolved thermal purity',anchor_length=48,physical_target_Hilbert_dimension=3**24,physical_anchor_Hilbert_dimension=3**48)
data['stage19_scope']=dict(smallest_accepted_initialization=30,strongest_global_gap='31/1250',strongest_global_gap_tail_initialization=34,uniform_contiguous_coverage_onset=2,isolated24=True,isolated24_alone_proves_uniform_onset=False,direct25_resource_compliance_accepted=False,no_minimum_claim=True,bilayer_new_gap=False,full8x4_m4_accepted=False,compiler_scope='local algebra and512-target samples only',old180_second_production_gate_passed=False,failed_cost_gate_is_universal_nogo=False,active_compiler_included=False)
data['preserved_stage18_files']={R+'overview_stage18/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage18_files'][R+'overview_stage18/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage18/overview_data.json')
data.update(snapshot_label='stage19',schema_version=16,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All stage18 rows preserved; new genuine initializations distinguished from finite coverage and isolated certificates. Final .0248 all-integer L>=2 proof uses n34 tail; smallest genuine initialization30 remains .0179. All source reviews are final; active implementation and proof-guide work excluded.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
for key in ['stage19_uniform_initializations','stage19_uniform_coverage','stage19_uniform_isolated','stage19_uniform_finite_certificates']:csv_write(key+'.csv',data[key])
print('PASS stage19 preparation',len(data['claims']),len(seals))
