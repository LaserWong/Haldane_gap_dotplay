#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage11');data=json.loads((old/'overview_data.json').read_text())
assert len(data['claims'])==228
sources=data['sources'];seals=data['review_seals']
def source(p):
 b=(ROOT/p).read_bytes();sources[p]=sha(ROOT/p);return json.loads(b) if p.endswith('.json') else b.decode()
for p,h in sources.items():assert sha(ROOT/p)==h,p
preserved={R+'overview_stage11/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())}
preserved[R+'overview_stage11/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json')
source(R+'overview_stage11/overview_data.json')
pins={'bilayer_direct_window_review':'8e2726b4925b752fed9789dc43b3486229a626e4d7d07b45c1d6b5171d23f8c7','bilayer_direct_window_continuation_review':'c9dadb17430a3523cda109599f3025ff62c7b9ebebacc2b9eb48acce2381e977','uniform_seed_frontier_review':'b71dfa41a851c509ec5bad6382f458ad6f51531934bbd90143ee9162779cbaf2'}
# Additional finalized review pins are deliberately added only after independent notification.
EXTRA_PINS={'bilayer_frontier_interval_0102_review':'45d651b0f68b840ed2c7a42978acd975d7789b69ad75acd3b4c21a9b74d2a7ed','bilayer_frontier_above_010_review':'d101b554ea00c044e148031ec4d073d10f6f757b78a019e5bc6502a67e086d05','uniform_source_license_supplement':'6d823ea723bd24e0536164e0f29fb8ad8023688049c9cb9c9498245dc97c1786','uniform_source_scope_review':'7c3ca3698dc82ace47e5c76482910404df1e1655e40ef6bc89f5775b2a5358c9'}
pins.update(EXTRA_PINS)
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','REVIEW_STATUS.json','ACCEPTANCE.json','CLAIM_VERDICTS.json','SEAL.json','PRODUCER_PROSE_ERRATUM.json','SOURCES.json','ATTRIBUTION.md','LICENSE','NOTICE_CHECKS.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
data['stage12_review_pins']=pins
p=R+'bilayer_direct_window_review/ACCEPTANCE.json';s=source(p);assert s['status']=='PASS'
def add(template,ident,p,gptr,pptr,route,lo=None,lptr=None,plot=True):
 src=source(p);r=deepcopy(template);g=ptr(src,pptr);gap=ptr(src,gptr)
 r.update(id=ident,parameter_exact=g,parameter_decimal=float(F(g)),parameter_kind='point' if lo is None else 'closed_interval',parameter_lower_exact=lo,gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),primary_source=p,primary_json_pointer=gptr,parameter_source_pointer=pptr,primary_sha256=sources[p],evidence_sources=[p],certificate_route=route,snapshot_stage='stage12',notes='Independent accepted analytic/exact scalar certificate; all integer square sides L>=2 and unique finite-volume ground state.',plotted_in_main_figure=plot,initial_beta_exact=None,asymptotic_base_size=None)
 if lptr:r['parameter_lower_source_pointer']=lptr
 data['claims'].append(r);return r
point=next(r for r in data['claims'] if r.get('certificate_route')=='complete_8x4_hardcore_residual')
r=add(point,'stage12_bilayer_direct_g010',p,'/gap_lower','/coupling','bilayer_direct_time_first_point');r.update(initial_beta_exact=s['initial_beta'],asymptotic_base_size=s['asymptotic_onset'])
def record(key,p):
 v=source(p);data[key]=dict(primary_source=p,source_sha256=sources[p],verdict=v);return v
record('stage12_bilayer_direct_acceptance',p)
record('stage12_bilayer_direct_erratum',R+'bilayer_direct_window_review/snapshot/PRODUCER_PROSE_ERRATUM.json')
p=R+'bilayer_direct_window_continuation_review/audit.json';s=record('stage12_bilayer_continuation',p)
template=next(r for r in data['claims'] if r.get('certificate_route')=='range010_interval_piece')
for i,a in enumerate(s['results']):
 r=add(template,f'stage12_direct_interval_{i}',p,f'/results/{i}/gap',f'/results/{i}/coupling_interval/1','stage12_direct_interval_piece',a['coupling_interval'][0],f'/results/{i}/coupling_interval/0',False);r.update(asymptotic_base_size=a['terminal_n'])
p=R+'bilayer_direct_window_continuation_review/ACCEPTANCE.json';record('stage12_bilayer_continuation_acceptance',p)
add(template,'stage12_direct_interval_union',p,'/uniform_gap_lower','/coupling_interval/1','stage12_uniform_interval_union','0','/coupling_interval/0',True)
data['current_ordinary_interval_piece_routes']=['stage12_direct_interval_piece'];data['current_ordinary_interval_endpoint']='1/10';data['current_ordinary_interval_piece_count']=66;data['current_ordinary_interval_union_route']='stage12_uniform_interval_union'
p=R+'uniform_seed_frontier_review/CLAIM_VERDICTS.json';s=record('stage12_uniform_n52',p);assert s['status'].startswith('ACCEPTED')
r=deepcopy(data['uniform_large_size_certificates'][-1]);r.update(id='stage12_uniform_n52',gap_lower_exact=s['gap'],gap_lower_decimal_down_12=floor12(s['gap']),integer_size_min=52,beta_exact=s['canonical_seed']['beta'],asymptotic_onset=s['asymptotic_from'],primary_source=p,primary_json_pointer='/gap',size_source_pointer='/all_integer_L_at_least',primary_sha256=sources[p],denominator_full_dimension_formula='3^52',numerator_full_dimension_formula='3^104');data['uniform_large_size_certificates'].append(r)
data['stage12_source_scope_included']='uniform_source_scope_review' in pins
if data['stage12_source_scope_included']:
 record('stage12_source_scope',R+'uniform_source_scope_review/results.json')
 for f in ['sources/transfer.tex','sources/model.tex','sources/introduction.tex']:source(R+'uniform_source_scope_review/'+f)
data['stage12_frontier_point_included']='bilayer_frontier_above_010_review' in pins
data['stage12_frontier_interval_included']=False
if data['stage12_frontier_point_included']:
 p=R+'bilayer_frontier_above_010_review/ACCEPTANCE.json';s=record('stage12_frontier_point',p)
 assert s['status']=='PASS_WITH_EXPLICIT_POINT_METADATA_ERRATUM'
 for i,a in enumerate(s['points']):
  r=add(point,f'stage12_frontier_point_{i}',p,f'/points/{i}/gap_lower',f'/points/{i}/g','bilayer_frontier_above010_point');r.update(asymptotic_base_size=a['onset'])
 record('stage12_frontier_metadata_erratum',R+'bilayer_frontier_above_010_review/snapshot/METADATA_ERRATUM.json')
if 'bilayer_frontier_interval_0102_review' in pins:
 data['stage12_frontier_interval_included']=True
 p=R+'bilayer_frontier_interval_0102_review/audit.json';s=record('stage12_frontier_interval',p)
 for i,a in enumerate(s['intervals']):
  r=add(template,f'stage12_frontier_interval_{i}',p,f'/intervals/{i}/gap',f'/intervals/{i}/coupling_interval/1','stage12_frontier_interval_piece',a['coupling_interval'][0],f'/intervals/{i}/coupling_interval/0',False);r.update(asymptotic_base_size=a['terminal_n'])
 add(template,'stage12_frontier_extension',p,'/extension_uniform_gap','/extension_interval/1','stage12_frontier_extension','1/10','/extension_interval/0',False)
 add(template,'stage12_frontier_whole_union',p,'/combined_uniform_gap','/combined_interval/1','stage12_uniform_interval_union','0','/combined_interval/0',True)
 data['current_ordinary_interval_piece_routes'].append('stage12_frontier_interval_piece');data['current_ordinary_interval_endpoint']='51/500';data['current_ordinary_interval_piece_count']=74

data.update(snapshot_label='stage12',schema_version=9,generated_utc=datetime.now(timezone.utc).isoformat(),preserved_stage11_files=preserved,claim_selection='All 228 stage11 M/L>=2 rows, finite chain record and three uniform large-size records preserved. New accepted 2D direct windows and n52 proof; exact current interval cover separate from historical alternatives.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',data['claims']),('finite_size_certificates.csv',data['finite_size_certificates']),('uniform_large_size_certificates.csv',data['uniform_large_size_certificates']),('unplotted_status.csv',data['unplotted_status']),('ordinary_interval_pieces.csv',[r for r in data['claims'] if r.get('certificate_route') in data['current_ordinary_interval_piece_routes']]),('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure'] and not any(a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'] and F(a['gap_lower_exact'])>F(r['gap_lower_exact']) for a in data['claims'])])]:csv_write(name,rows)
for name in ['trial_dimensions.csv','stage9_chain_dimensions.csv','stage10_bilayer_dimensions.csv','tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv','reference_certificates.csv','chain_candidate_routes.csv','recipe_upper_envelopes.csv','excited_witness_upper_envelopes.csv']:(HERE/name).write_bytes((old/name).read_bytes())
(HERE/'historical_interval_pieces_stage11.csv').write_bytes((old/'ordinary_interval_pieces.csv').read_bytes())
print('PASS: stage12 extracted',len(data['claims']),'M/L>=2 records,',len(data['uniform_large_size_certificates']),'uniform large-size records')
