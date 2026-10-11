#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage16');assert sha(old/'MANIFEST_SHA256.json')=='911fce0e47b5bff696187ac31524fbcb75096068ef2846e40472f5228ac36a7e'
data=json.loads((old/'overview_data.json').read_text());sources=data['sources'];seals=data['review_seals']
def source(p):
 sources[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text())
pins={'bilayer_symmetry_frontier_010675_0108_review':'4cdc6d5b68c95082a0d48369e46b984cea303e0f8f774d048cf2bcf55f367136','bilayer_symmetry_interval_0108_review':'61283a4637b0906e2c059e25023933003ba9a4815771ec0b52a680a0bb713f0b','bilayer_symmetry_frontier_010825_review':'e9b6f4f3451a71a44b9644f02c759512550b21d13325f2a7cc2ef4484f2501e4'}
NEXT_INTERVAL_PIN='8a4e274d06b2d8aa0c63a02af978a0820fe3110105ccc27da869a8183786827a'
if NEXT_INTERVAL_PIN:pins['bilayer_symmetry_interval_010825_review']=NEXT_INTERVAL_PIN
EXTRA_PINS={'bilayer_pair_product_review':'2da9636ae7a2053736ae5aca3aaea8a39a5c75ce4b0d342d8b7beb5ababd16f3'}
pins.update(EXTRA_PINS)
data['stage17_review_pins']=pins;data['stage17_evidence']={}
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','PROOF.md','REVIEW.md','ACCEPTANCE.json','RESULTS.json','audit.json']:
  p=R+directory+'/'+f
  if (ROOT/p).exists():sources[p]=sha(ROOT/p)
 p=R+directory+('/RESULTS.json' if directory=='bilayer_pair_product_review' else '/ACCEPTANCE.json');data['stage17_evidence'][directory]=dict(primary_source=p,source_sha256=sources[p],verdict=source(p))
point=next(r for r in data['claims'] if r.get('certificate_route')=='stage13_actual_point')
def add(ident,p,gptr,pptr,route,lptr=None,plot=True):
 src=source(p);r=deepcopy(point);g=ptr(src,pptr);gap=ptr(src,gptr)
 r.update(id=ident,parameter_exact=g,parameter_decimal=float(F(g)),parameter_kind='closed_interval' if lptr else 'point',parameter_lower_exact=ptr(src,lptr) if lptr else None,gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),primary_source=p,primary_json_pointer=gptr,parameter_source_pointer=pptr,primary_sha256=sources[p],evidence_sources=[p],certificate_route=route,snapshot_stage='stage17',notes='Independent physical and exact scalar certificate; every integer periodic square L>=2, unique full-Hilbert ground.',plotted_in_main_figure=plot,initial_beta_exact=None,asymptotic_base_size=None)
 if lptr:r['parameter_lower_source_pointer']=lptr
 data['claims'].append(r);return r
p=R+'bilayer_symmetry_frontier_010675_0108_review/ACCEPTANCE.json'
for i in range(4):add('stage17_point_'+str(i),p,f'/points/{i}/gap_lower',f'/points/{i}/g','stage17_symmetry_point')
p=R+'bilayer_symmetry_frontier_010825_review/ACCEPTANCE.json';add('stage17_point010825',p,'/all_integer_L_ge2_gap','/g','stage17_symmetry_point')
for suffix in ['0108']+(['010825'] if NEXT_INTERVAL_PIN else []):
 p=R+'bilayer_symmetry_interval_'+suffix+'_review/audit.json';v=source(p)
 for i in range(len(v['certificates'])):add('stage17_piece_'+suffix+'_'+str(i),p,f'/certificates/{i}/gap',f'/certificates/{i}/interval/1','stage17_interval_piece',f'/certificates/{i}/interval/0',False)
 p=R+'bilayer_symmetry_interval_'+suffix+'_review/ACCEPTANCE.json';add('stage17_union_'+suffix,p,'/combined_uniform_gap_lower','/combined_interval/1','stage17_uniform_union','/combined_interval/0')
data['current_ordinary_interval_piece_routes'].append('stage17_interval_piece');data['current_ordinary_interval_piece_count']=88 if NEXT_INTERVAL_PIN else 86;data['current_ordinary_interval_endpoint']='433/4000' if NEXT_INTERVAL_PIN else '27/250';data['current_ordinary_interval_union_route']='stage17_uniform_union'
data['stage17_nested_covers']=[dict(endpoint='27/250',closed_pieces=86,gap_lower='4499695659/1000000000000')]+([dict(endpoint='433/4000',closed_pieces=88,gap_lower='293202989/500000000000')] if NEXT_INTERVAL_PIN else [])
data['stage17_scope']=dict(selected_ground_dimensions=[21,57],selected_numerator_dimension=43,retained_counts=[49,97,1],physical_Hilbert_dimensions=[2**32,2**64,2**128],g01085_failure_universal_nogo=False,g0109_tested=False,full18_thermal_accepted=False,conditional_uniform_promoted=False,mutable_campaign_included=False)
data['preserved_stage16_files']={R+'overview_stage16/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())};data['preserved_stage16_files'][R+'overview_stage16/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json');source(R+'overview_stage16/overview_data.json')
data.update(snapshot_label='stage17',schema_version=14,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='All stage16 rows preserved; exact new frontier points and nested closed covers. Uniform conditional category unchanged.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2)+'\n');(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
(HERE/'historical_interval_pieces_stage16.csv').write_bytes((old/'ordinary_interval_pieces.csv').read_bytes())
for name,rows in [('certified_bounds.csv',data['claims']),('ordinary_interval_pieces.csv',[r for r in data['claims'] if r.get('certificate_route') in data['current_ordinary_interval_piece_routes']]),('stage17_nested_covers.csv',data['stage17_nested_covers']),('stage17_route_dimensions.csv',[data['stage17_scope']]),('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure'] and not any(a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'] and F(a['gap_lower_exact'])>F(r['gap_lower_exact']) for a in data['claims'])])]:csv_write(name,rows)
print('PASS stage17',len(data['claims']),len(seals))
