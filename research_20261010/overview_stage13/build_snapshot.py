#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage12');data=json.loads((old/'overview_data.json').read_text());assert len(data['claims'])==311
assert sha(old/'MANIFEST_SHA256.json')=='39c5b539217441e82c36186411f6604cb2ff260a9ebac47962fb4a0b8c203803'
sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text()) if p.endswith('.json') else (ROOT/p).read_text()
pins={'bilayer_seed_error_budget_review':'a52450baf76b0a3fb17addec8e784da7c2e19de0c49ef56efb79d2d2e0391361','bilayer_optimized_residual_g0105_review':'6c19485312d08ad0cca2fc76367d5c9172d3aab8ea843d0a740324b69837b331','bilayer_16d_4x4_residual_g0105_review':'928f1e61cee6a273c7d3af70d3caed60628373435b3b0985ae3005e9de70ac90','bilayer_g0105_actual_point_review':'02cdd689b9bf4608b540a95316672708eb4691b56057ad8fb23082a930185c12','uniform_moment_optimality_review':'60bb3811a98e6335d5054ff2c87c80656da8f47e5ab7e556a7a720714748525a','uniform_anchor96_100_review':'99317ea99db7892f33852e6a0b12b9aa4d3825527852ff605d7d86f22d3f22d7','uniform_seed_recipe_minimum_review':'ff6500e7dacf713d601053c1abcaa0bf1d974bce1c895e96f1c1f2e62d923c56'}
# Only final independently notified interval seal may be added here.
INTERVAL_PIN='0c19177fdb91be54ba1892e5e3960e18a90e0ace9f11018018445368333eea9d'
BRIDGE_PIN='1f94ecf80d9674416d07b5ed47b2aa28642b62c8f235ec0a792c96c499c5ae17'
if BRIDGE_PIN:pins['uniform_n48_direct_window_review']=BRIDGE_PIN
if INTERVAL_PIN:pins['bilayer_interval_0102_0105_review']=INTERVAL_PIN
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h,(p,sha(ROOT/p));n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','SEAL.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
data['stage13_review_pins']=pins;data['stage13_evidence']={}
def record(key,p):
 v=source(p);data['stage13_evidence'][key]=dict(primary_source=p,source_sha256=sources[p],verdict=v);return v
for key,directory,f in [('budget','bilayer_seed_error_budget_review','ACCEPTANCE.json'),('residual32','bilayer_optimized_residual_g0105_review','ACCEPTANCE.json'),('residual16','bilayer_16d_4x4_residual_g0105_review','ACCEPTANCE.json'),('point','bilayer_g0105_actual_point_review','ACCEPTANCE.json'),('optimality','uniform_moment_optimality_review','CLAIM_VERDICTS.json'),('anchors','uniform_anchor96_100_review','CLAIM_VERDICTS.json'),('recipe','uniform_seed_recipe_minimum_review','CLAIM_VERDICTS.json')]:record(key,R+directory+'/'+f)
point=next(r for r in data['claims'] if r.get('certificate_route')=='bilayer_direct_time_first_point')
def add(ident,p,gptr,pptr,route,lptr=None,plot=True):
 src=source(p);r=deepcopy(point);g=ptr(src,pptr);gap=ptr(src,gptr)
 r.update(id=ident,parameter_exact=g,parameter_decimal=float(F(g)),parameter_kind='closed_interval' if lptr else 'point',parameter_lower_exact=ptr(src,lptr) if lptr else None,gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),primary_source=p,primary_json_pointer=gptr,parameter_source_pointer=pptr,primary_sha256=sources[p],evidence_sources=[p],certificate_route=route,snapshot_stage='stage13',notes='Independent accepted exact physical/scalar proof; all integer periodic square L>=2, unique ground.',plotted_in_main_figure=plot,initial_beta_exact=None,asymptotic_base_size=None)
 if lptr:r['parameter_lower_source_pointer']=lptr
 data['claims'].append(r);return r
r=add('stage13_g0105_actual',R+'bilayer_g0105_actual_point_review/ACCEPTANCE.json','/gap','/coupling','stage13_actual_point');r.update(initial_beta_exact='47/5',asymptotic_base_size=2048)
data['stage13_interval_included']=bool(INTERVAL_PIN)
if INTERVAL_PIN:
 p=R+'bilayer_interval_0102_0105_review/audit.json';v=record('interval',p)
 for i,a in enumerate(v['results']):add(f'stage13_piece_{i}',p,f'/results/{i}/gap',f'/results/{i}/coupling_interval/1','stage13_interval_piece',f'/results/{i}/coupling_interval/0',False)
 add('stage13_extension',p,'/extension_uniform_gap','/extension_interval/1','stage13_extension','/extension_interval/0',False)
 add('stage13_union',p,'/combined_uniform_gap','/combined_interval/1','stage13_union','/combined_interval/0')
 data['current_ordinary_interval_piece_routes'].append('stage13_interval_piece');data['current_ordinary_interval_piece_count']=80;data['current_ordinary_interval_endpoint']='21/200';data['current_ordinary_interval_union_route']='stage13_union'
data['stage13_n48_bridge_included']=bool(BRIDGE_PIN)
data['uniform_coverage_certificates']=[];data['uniform_finite_windows']=[]
if BRIDGE_PIN:
 p=R+'uniform_n48_direct_window_review/results.json';v=record('n48_bridge',p)
 data['uniform_coverage_certificates']=[dict(id='stage13_uniform_coverage48',model='uniform_spin1_heisenberg_chain',integer_size_min=v['all_integer_L_at_least'],bootstrap_initialization_size=v['bootstrap_initialization_remains'],gap_lower_exact=v['combined_gap'],gap_lower_decimal_down_12=floor12(v['combined_gap']),all_integers_including_odd=True,unique_ground_state=True,minimum_seed_proven=False,primary_source=p,primary_json_pointer='/combined_gap',primary_sha256=sources[p],evidence_sources=[p,R+'uniform_seed_frontier_review/CLAIM_VERDICTS.json'],proof='Finite48..96 window overlaps independently proved all-integerL>=52 theorem')]
 data['uniform_finite_windows']=[dict(id='stage13_uniform_finite48_96',model='uniform_spin1_heisenberg_chain',integer_size_min=v['finite_window'][0],integer_size_max=v['finite_window'][1],gap_lower_exact=v['finite_gap'],gap_lower_decimal_down_12=floor12(v['finite_gap']),all_integers_including_odd=True,unique_ground_state=True,primary_source=p,primary_json_pointer='/finite_gap',primary_sha256=sources[p],new50site_anchor_used=False)]
data['stage13_scope']=dict(error_budget_physical_gap=False,optimality_physical_realization=False,optimality_minimum_seed=False,anchors_gap=False,recipe_minimum_seed=False,recipe_adaptive_orders_excluded=False,active_adaptive_and_tensor_assessments_excluded=True)
data['stage13_bilayer_dimensions']=[dict(seed_geometry=g,physical_spin_count=s,full_Hilbert_dimension=2**s,ground_search_dimension=d,total_trial_space_dimension=t,retained_low_band_count=r,numerator_trial_rank=1 if g=='8x8' else None,MPS_bond_dimension=None) for g,s,d,t,r in [('4x4',32,16,64,49),('8x4',64,43,139,97),('8x8',128,43,43,1)]]
data['preserved_stage12_files']={R+'overview_stage12/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage12_files'][R+'overview_stage12/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage12/overview_data.json')
data.update(snapshot_label='stage13',schema_version=10,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All311 stage12 rows unchanged; accepted actual .105 point and separately finalized interval; scoped information-only studies.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
(HERE/'historical_interval_pieces_stage12.csv').write_bytes((old/'ordinary_interval_pieces.csv').read_bytes())
for name,rows in [('uniform_coverage_certificates.csv',data['uniform_coverage_certificates']),('uniform_finite_windows.csv',data['uniform_finite_windows']),('certified_bounds.csv',data['claims']),('stage13_bilayer_dimensions.csv',data['stage13_bilayer_dimensions']),('ordinary_interval_pieces.csv',[r for r in data['claims'] if r.get('certificate_route') in data['current_ordinary_interval_piece_routes']]),('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure'] and not any(a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'] and F(a['gap_lower_exact'])>F(r['gap_lower_exact']) for a in data['claims'])])]:csv_write(name,rows)
print('PASS stage13',len(data['claims']),len(seals))
