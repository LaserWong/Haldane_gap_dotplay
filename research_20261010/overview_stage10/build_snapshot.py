#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage9');data=json.loads((old/'overview_data.json').read_text())
assert len(data['claims'])==212
sources=data['sources'];seals=data['review_seals']
def source(p):
 b=(ROOT/p).read_bytes();sources[p]=sha(ROOT/p);return json.loads(b) if p.endswith('.json') else b.decode()
for p,h in sources.items():assert sha(ROOT/p)==h,p
preserved={R+'overview_stage9/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())}
preserved[R+'overview_stage9/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json')
source(R+'overview_stage9/overview_data.json')
pins={'bilayer_complete_residual_8x4_review':'47ca2166342038a845f45d774bd9e2d91429496235df6e6d0fc39fb678a2b081','chain_frontier_rank195_review':'1365bd8c7fe06acf5c4c8bdaf264d1638c17bad5df72c8d753a8ee6ac615c959'}
interval_manifest=ROOT/(R+'interval_range_010_review/MANIFEST_SHA256.json')
if interval_manifest.exists():
 assert sha(interval_manifest)=='d6eb3e4ce912086fe66dc1eb2917c3ae7381bc6a527a939b99229b97b863f3e5'
 pins['interval_range_010_review']=sha(interval_manifest)
for directory,h in pins.items():
 p=R+directory+'/MANIFEST_SHA256.json';assert sha(ROOT/p)==h;n=manifest_check(p);seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n));source(p)
 for f in ['README.md','REVIEW.md','PROOF.md','REVIEW_STATUS.json','ACCEPTANCE.json','DECIMAL_DISPLAY_CHECK.json']:
  if (ROOT/(R+directory)/f).exists():source(R+directory+'/'+f)
def add(template,ident,p,gptr,pptr,route,lo=None,lptr=None,plot=True):
 src=source(p);r=deepcopy(template);g=ptr(src,pptr);gap=ptr(src,gptr)
 r.update(id=ident,parameter_exact=g,parameter_decimal=float(F(g)),parameter_kind='point' if lo is None else 'closed_interval',parameter_lower_exact=lo,gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),primary_source=p,primary_json_pointer=gptr,parameter_source_pointer=pptr,primary_sha256=sources[p],evidence_sources=[p],certificate_route=route,snapshot_stage='stage10',notes='Independently sealed all-integer L>=2 certificate; unique finite-volume ground state; one retained largest numerator.',plotted_in_main_figure=plot,initial_beta_exact=None,asymptotic_base_size=None)
 if lptr:r['parameter_lower_source_pointer']=lptr
 data['claims'].append(r);return r
point=next(r for r in data['claims'] if r.get('certificate_route')=='third_moment_enlarged_numerator')
p=R+'bilayer_complete_residual_8x4_review/REVIEW_STATUS.json';s=source(p);assert s['status']=='PASS'
r=add(point,'stage10_bilayer_complete_residual_g010',p,'/all_integer_L_ge2_gap','/coupling','complete_8x4_hardcore_residual');r.update(initial_beta_exact='47/5',asymptotic_base_size=64)
for f in ['assembly_result.json','scalar_result.json','polynomial_result.json']:source(R+'bilayer_complete_residual_8x4_review/'+f)
data['complete_residual_review']=dict(primary_source=p,source_sha256=sources[p],verdict=s,largest_residual_computed=False,production_q8_enumerated=False,hardcore_signed_commutator=True,coherent_sector_interference_preserved=True,complete_denominator_tail_retained=True)
data['stage10_bilayer_dimensions']=[dict(seed_geometry=shape,physical_spin_count=n,full_Hilbert_dimension=2**n,ground_search_dimension=search,total_trial_space_dimension=total,retained_denominator_states=retained,retained_numerator_states=1 if shape=='8x8' else None,MPS_bond_dimension=None) for shape,n,search,total,retained in [('4x4',32,11,59,49),('8x4',64,43,139,97),('8x8',128,43,43,None)]]
p=R+'chain_frontier_rank195_review/ACCEPTANCE.json';s=source(p);assert s['status'].startswith('ACCEPTED_EXACT') and not s['new_positive_gap_certificate']
data['rank195_obstruction']=dict(primary_source=p,source_sha256=sources[p],verdict=s,gap_lower_exact=None,fixed_early_window_only=True,not_physical_gaplessness=True,necessary_improvement_strict_lower_decimal='0.000426143856861',rounded_approximation_only='0.000426143856862')
for r in data['unplotted_status']:
 if r['status'] in ['rank195_independent_review_pending','hardcore_pair_commutator_proposed_only']:r['scope']='Historical stage9 status; superseded by independently sealed stage10 review. '+r['scope'];r['historical_superseded']=True
for model,status,scope in [('alternating_spin1_chain','rank195_fixed_early_window_obstruction','g=1/4, all beta>=0, exact M4 trace allowed and every vector in old M8 span; specified first [8,16] window only; no positive gap or universal exclusion.'),('ordinary_spinhalf_bilayer','interval_range010_pending','Candidate extension [0.09,0.1] remains pending unless final independent immutable seal is included.'),('uniform_spin1_chain','current_operator_branch_excluded','Ongoing MPS pi-current branch excluded regardless of producer claims.'),('alternating_spin1_chain','new_numerator_branch_excluded','Ongoing new numerator refinements excluded regardless of producer claims.')]:
 data['unplotted_status'].append(dict(model=model,status=status,scope=scope,parameter_exact=None,gap_lower_exact=None,evidence_source=None,plotted_as_zero_gap=False))
data['interval_range_010_included']='interval_range_010_review' in pins
if data['interval_range_010_included']:
 p=R+'interval_range_010_review/results/SUMMARY.json';s=source(p);assert s['accepted'] and s['status'].startswith('PASS')
 data['interval_range_010_review']=dict(primary_source=p,source_sha256=sources[p],verdict=s)
 template=next(r for r in data['claims'] if r.get('certificate_route')=='range009_interval_piece')
 for i,a in enumerate(s['intervals']):
  r=add(template,f'stage10_range010_piece_{i}',p,f'/intervals/{i}/all_integer_L_ge2_gap',f'/intervals/{i}/coupling_interval/1','range010_interval_piece',a['coupling_interval'][0],f'/intervals/{i}/coupling_interval/0',False);r.update(initial_beta_exact=a['beta_initial'],asymptotic_base_size=a['asymptotic_onset'])
 add(template,'stage10_range010_extension',p,'/extension_all_integer_L_ge2_uniform_gap','/extension_interval/1','range010_interval_extension','9/100','/extension_interval/0',False)
 add(template,'stage10_range010_union',p,'/combined_all_integer_L_ge2_uniform_gap','/combined_coupling_interval/1','uniform_interval_union','0','/combined_coupling_interval/0',True)
 data['ordinary_interval_piece_routes'].append('range010_interval_piece');data['ordinary_interval_piece_count']=66;data['ordinary_interval_endpoint']='1/10'
 data['unplotted_status']=[r for r in data['unplotted_status'] if r['status']!='interval_range010_pending']
data.update(snapshot_label='stage10',schema_version=7,generated_utc=datetime.now(timezone.utc).isoformat(),preserved_stage9_files=preserved,claim_selection='All 212 stage9 rows preserved; immutable independent PASS only; fixed-recipe obstructions are not gaps.',rank195_review_included=True,ongoing_complete_residual_and_current_operator_branches_excluded=False,ongoing_current_operator_and_chain_numerator_branches_excluded=True)
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in seals},indent=2)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',data['claims']),('trial_dimensions.csv',data['dimensions']),('unplotted_status.csv',data['unplotted_status']),('latest_point_bounds.csv',[r for r in data['claims'] if r['parameter_kind']=='point' and r['plotted_in_main_figure']]),('stage9_chain_dimensions.csv',[data['stage9_chain_dimensions']]),('stage10_bilayer_dimensions.csv',data['stage10_bilayer_dimensions'])]:csv_write(name,rows)
for name in ['ordinary_interval_pieces.csv','tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv','reference_certificates.csv','chain_candidate_routes.csv','recipe_upper_envelopes.csv','excited_witness_upper_envelopes.csv']:(HERE/name).write_bytes((old/name).read_bytes())
if data['interval_range_010_included']:csv_write('ordinary_interval_pieces.csv',[r for r in data['claims'] if r.get('certificate_route') in data['ordinary_interval_piece_routes']])
print('PASS: stage10 extracted',len(data['claims']),'gap rows; interval included:',data['interval_range_010_included'])
