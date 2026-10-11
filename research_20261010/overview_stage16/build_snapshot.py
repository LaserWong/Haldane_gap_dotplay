#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage15');assert sha(old/'MANIFEST_SHA256.json')=='2313a7d3eac7852710a24bec3547e1fe3595d281c2e93ee03c16465ebdd1be5f'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text()) if p.endswith('.json') else (ROOT/p).read_text()
pins={'bilayer_krylov_m4_fixture_review':'47d717c90a183afde52fcf9b6dcd92fa246d9fa7619821af8fd703dd8310a589','bilayer_next_residual_direction_review':'8cc778af3e672d6710b454c2b1d84df8d109bde43302081dc631b444bf056490','bilayer_square_symmetry_window_review':'890e942c8a7e37cbefc5b8de52f40f8d61cbfefe76e03f8a71f9dec8d66648cc','bilayer_square_symmetry_recurrence_review':'21577fcf285cc7e53c6c4acdbdfa1086f1b7dd88f6f30c4e87e0ebf5f0ac5e83','bilayer_g011_symmetry_scalar_review':'914b267d33635a576b591358c1b7e0e152b3b51111bbaeb18c7a0aa980f1f70a','bilayer_g0106_symmetry_point_review':'3cc265100d18353585289f677e3ba79a1bb79b6ec60ac43c0fcd7046cc113d68','uniform_second_thermal_repair_review':'74e56ac805d5f9f6e23c93171dcf1224b9c2ace62de05defbf5115101b64200c'}
EXTRA_PINS={'bilayer_g01065_optimized_point_review':'1b50b7645b0c6a9805dbac76a38d0eaf2e1e7eab7a435a78ce0c8d44e0c03964','bilayer_symmetry_interval_0106_review':'6260f3243dc94c3751b06f30bfbc4d03364d315f1c7447beb3bd291abb3ecfd6'}
NEXT_INTERVAL_PIN='f6328b280cad0963dd70aa90c71b12ca88fbbf6a2b808376d2948e6aeae77fe2'
if NEXT_INTERVAL_PIN:EXTRA_PINS['bilayer_symmetry_interval_01065_review']=NEXT_INTERVAL_PIN
pins.update(EXTRA_PINS)
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','ACCEPTANCE.json','CLAIM_VERDICTS.json','SEAL.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
data['stage16_review_pins']=pins;data['stage16_evidence']={}
def record(key,p):
 v=source(p);data['stage16_evidence'][key]=dict(primary_source=p,source_sha256=sources[p],verdict=v);return v
for key,directory in [('m4_fixture','bilayer_krylov_m4_fixture_review'),('envelope_barrier','bilayer_next_residual_direction_review'),('square_window','bilayer_square_symmetry_window_review'),('square_recurrence','bilayer_square_symmetry_recurrence_review'),('finite011','bilayer_g011_symmetry_scalar_review'),('point0106','bilayer_g0106_symmetry_point_review'),('repair','uniform_second_thermal_repair_review')]:
 f='ACCEPTANCE.json' if (ROOT/(R+directory+'/ACCEPTANCE.json')).exists() else 'CLAIM_VERDICTS.json';record(key,R+directory+'/'+f)
point=next(r for r in data['claims'] if r.get('certificate_route')=='stage13_actual_point')
def add(ident,p,gptr,pptr,route,lptr=None,plot=True):
 src=source(p);r=deepcopy(point);g=ptr(src,pptr);gap=ptr(src,gptr)
 r.update(id=ident,parameter_exact=g,parameter_decimal=float(F(g)),parameter_kind='closed_interval' if lptr else 'point',parameter_lower_exact=ptr(src,lptr) if lptr else None,gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),primary_source=p,primary_json_pointer=gptr,parameter_source_pointer=pptr,primary_sha256=sources[p],evidence_sources=[p],certificate_route=route,snapshot_stage='stage16',notes='Independent accepted square-symmetry exact scalar/physical-input certificate; all integer periodic square L>=2 and unique ground.',plotted_in_main_figure=plot,initial_beta_exact=None,asymptotic_base_size=None)
 if lptr:r['parameter_lower_source_pointer']=lptr
 data['claims'].append(r);return r
r=data['stage16_evidence']['point0106'];add('stage16_g0106',r['primary_source'],'/all_integer_L_ge2_gap','/g','stage16_symmetry_point')
r=data['stage16_evidence']['finite011'];v=r['verdict'];data['stage16_finite_bilayer_certificates']=[dict(id='stage16_g011_finite',model='ordinary_spinhalf_bilayer',parameter_exact=v['g'],gap_lower_exact=v['actual_gap_lower'],gap_lower_decimal_down_12=floor12(v['actual_gap_lower']),integer_size_min=2,integer_size_max=32,all_size_certificate=False,unique_full_Hilbert_ground=True,denominator_search_dimensions=v['denominator_ground_search_dimensions'],numerator_search_dimension=v['fresh_numerator_search_dimension'],retained_counts=[49,97,1],primary_source=r['primary_source'],primary_json_pointer='/actual_gap_lower',primary_sha256=r['source_sha256'])]
data['stage16_interval_included']=False
if 'bilayer_symmetry_interval_0106_review' in pins:
 data['stage16_interval_included']=True
 p=R+'bilayer_symmetry_interval_0106_review/ACCEPTANCE.json';v=record('interval0106',p)
 add('stage16_interval0106_piece',p,'/extension_uniform_gap_lower','/extension_interval/1','stage16_interval_piece','/extension_interval/0',False)
 add('stage16_interval0106_union',p,'/combined_uniform_gap_lower','/combined_interval/1','stage16_uniform_union','/combined_interval/0')
 data['current_ordinary_interval_piece_routes'].append('stage16_interval_piece');data['current_ordinary_interval_piece_count']=81;data['current_ordinary_interval_endpoint']='53/500';data['current_ordinary_interval_union_route']='stage16_uniform_union'
data['stage16_next_point_included']=False;data['stage16_next_interval_included']=False
if 'bilayer_g01065_optimized_point_review' in pins:
 data['stage16_next_point_included']=True
 p=R+'bilayer_g01065_optimized_point_review/ACCEPTANCE.json';v=record('point01065',p)
 add('stage16_g01065',p,'/all_integer_L_ge2_gap','/g','stage16_symmetry_point')
if NEXT_INTERVAL_PIN:
 data['stage16_next_interval_included']=True
 p=R+'bilayer_symmetry_interval_01065_review/ACCEPTANCE.json';v=record('interval01065',p)
 add('stage16_interval01065_piece',p,'/extension_uniform_gap_lower','/extension_interval/1','stage16_interval_piece','/extension_interval/0',False)
 add('stage16_interval01065_union',p,'/combined_uniform_gap_lower','/combined_interval/1','stage16_uniform_union','/combined_interval/0')
 data['current_ordinary_interval_piece_count']=82;data['current_ordinary_interval_endpoint']='213/2000'


data['stage16_scope']=dict(m4_small_shapes_only=True,physical8x4_m4_accepted=False,envelope_barrier_universal_nogo=False,geometry_square_isotropic_only=True,raw_canonical_coordinates_distinguished=True,g011_all_size_gap=False,g011_hypothetical_targets_are_physical=False,g0106_selected_ground_search_dimensions=[16,43],g0106_selected_numerator_search_dimension=43,g0106_ambient_matrix_dimensions=[21,57],g0106_retained_counts=[49,97,1],thermal_full18_accepted=False,conditional_uniform_gaps_promoted=False,repair_review_is_engineering_only=True,mutable_campaign_included=False)
data['stage16_gap_route_dimensions']=[]
for key,r in data['stage16_evidence'].items():
 v=r['verdict']
 if key=='finite011':gd=v['denominator_ground_search_dimensions'];nd=v['fresh_numerator_search_dimension'];ambient=None;scope='g=.11, only2<=L<=32'
 elif key=='point0106':gd=v['selected_ground_vector_search_dimensions'];nd=v['selected_numerator_search_dimension'];ambient=v['ambient_complete_matrix_dimensions'];scope='g=.106, allintegerL>=2'
 elif key=='point01065':gd=v['denominator_search_dimensions'];nd=v['numerator_search_dimension'];ambient=None;scope='g=.1065, allintegerL>=2'
 elif key=='interval01065':gd=v['selected_ground_search_dimensions'];nd=v['selected_numerator_search_dimension'];ambient=v.get('ambient_matrix_dimensions');scope='[.106,.1065], allintegerL>=2'
 elif key=='interval0106':gd=v['selected_ground_search_dimensions'];nd=v['selected_numerator_search_dimension'];ambient=v['ambient_matrix_dimensions'];scope='[.105,.106], allintegerL>=2'
 else:continue
 data['stage16_gap_route_dimensions'].append(dict(route=key,scope=scope,selected_denominator_search_dimensions=gd,selected_numerator_search_dimension=nd,ambient_denominator_matrix_dimensions=ambient,retained_states=[49,97,1],physical_Hilbert_dimensions=[2**32,2**64,2**128],primary_source=r['primary_source'],primary_sha256=r['source_sha256']))
data['preserved_stage15_files']={R+'overview_stage15/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage15_files'][R+'overview_stage15/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage15/overview_data.json')
data.update(snapshot_label='stage16',schema_version=13,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All stage15 rows preserved. New .106 all-size point and separate .11 L2..32 finite certificate; square-symmetry tools and engineering-only repair. No mutable campaign or full18-input promotion.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
(HERE/'historical_interval_pieces_stage15.csv').write_bytes((old/'ordinary_interval_pieces.csv').read_bytes())
for name,rows in [('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure'] and not any(a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'] and F(a['gap_lower_exact'])>F(r['gap_lower_exact']) for a in data['claims'])]),('stage16_gap_route_dimensions.csv',data['stage16_gap_route_dimensions']),('certified_bounds.csv',data['claims']),('stage16_finite_bilayer_certificates.csv',data['stage16_finite_bilayer_certificates']),('ordinary_interval_pieces.csv',[r for r in data['claims'] if r.get('certificate_route') in data['current_ordinary_interval_piece_routes']])]:csv_write(name,rows)
print('PASS stage16',len(data['claims']),len(seals))
