#!/usr/bin/env python3
"""Extend sealed stage7; optional new sources require an explicitly pinned PASS seal."""
import sys;sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=R+'overview_stage7/overview_data.json';data=json.loads((ROOT/old).read_text())
claims=deepcopy(data['claims']);dims=deepcopy(data['dimensions']);statuses=deepcopy(data['unplotted_status']);sources=deepcopy(data['sources'])
def source(p):
 b=(ROOT/p).read_bytes();sources[p]=hashlib.sha256(b).hexdigest();return json.loads(b) if p.endswith('.json') else b.decode()
for p,h in sources.items():assert sha(ROOT/p)==h,p
accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text());seals=[]
for p,h in accepted.items():
 assert sha(ROOT/p)==h;seals.append(dict(directory=str(Path(p).parent),manifest=p,sha256=h,verified_files=manifest_check(p)));source(p)
source(old)
preserved={R+'overview_stage7/'+p:sha(ROOT/(R+'overview_stage7/'+p)) for p in json.loads((ROOT/(R+'overview_stage7/MANIFEST_SHA256.json')).read_text())}
preserved[R+'overview_stage7/MANIFEST_SHA256.json']=sha(ROOT/(R+'overview_stage7/MANIFEST_SHA256.json'))
def add(g,p,pointer,route,kind='point',lo=None,beta=None,onset=None):
 d=source(p);r=deepcopy(next(r for r in claims if r['model']=='ordinary_spinhalf_bilayer' and r['parameter_kind']=='point'))
 r.update(id='stage8_'+route+'_'+pointer.replace('/','_'),parameter_exact=str(F(g)),parameter_decimal=float(F(g)),parameter_lower_exact=lo,parameter_kind=kind,gap_lower_exact=str(F(ptr(d,pointer))),gap_lower_decimal_down_12=floor12(ptr(d,pointer)),primary_source=p,primary_json_pointer=pointer,primary_sha256=sources[p],evidence_sources=[p],evidence_status='independent_review_passed',certificate_route=route,snapshot_stage='stage8',initial_beta_exact=beta,asymptotic_base_size=onset,numerator_trial_rank=1,notes='Every integer L>=2; unique finite-volume ground state. One retained largest numerator.',largest_higher_moments_used=True,proof_family='thermal_bootstrap',plotted_in_main_figure=kind=='point')
 if kind=='point':r['parameter_source_pointer']='/coupling'
 elif pointer.startswith('/intervals/'):
  root=pointer.rsplit('/',1)[0];r['parameter_source_pointer']=root+'/coupling_interval/1';r['parameter_lower_source_pointer']=root+'/coupling_interval/0'
 else:
  stem='combined_coupling_interval' if pointer.startswith('/combined') else 'extension_interval';r['parameter_source_pointer']='/'+stem+'/1';r['parameter_lower_source_pointer']='/'+stem+'/0'
 claims.append(r);return r
p=R+'third_moment_review/REVIEW_STATUS.json';d=source(p);assert d['status'].startswith('PASS')
for f in ['PROOF.md','REVIEW.md','results/scalar_summary.json','results/scalar_and_all_size_replay.json']:source(R+'third_moment_review/'+f)
for field,route in [('best_all_integer_gap','third_moment_enlarged_numerator'),('two_vector_all_integer_gap','third_moment_two_vector_numerator')]:
 r=add(d['coupling'],p,'/'+field,route);r['evidence_sources'] += [R+'third_moment_review/PROOF.md',R+'third_moment_review/REVIEW.md'];r['notes']+=' Isolated g=.09; no continuous interval inferred. Smaller denominators unchanged.'
for i,(shape,n) in enumerate([('4x4',16),('8x4',32),('8x8',64)]):
 r={k:None for k in dims[0]};r.update(model='ordinary_spinhalf_bilayer',parameter_exact='9/100',seed_geometry=shape,dimer_or_rung_count=n,physical_spin_count=2*n,full_Hilbert_dimension=4**n,proposal_basis_dimension=d['enlarged_exact_search_ranks'][i],support_scope='independently checked exact enlarged search; scalar use only at largest seed',numerator_trial_rank=1 if i==2 else None,evidence_source=p,evidence_json_pointer='/enlarged_exact_search_ranks/'+str(i),evidence_sha256=sources[p],notes='Exact enlarged rank, not retained band count or MPS bond. Smaller 16/43 searches are checked but not substituted into denominators. The used denominator totals remain 59/125 and trace counts 49/97.')
 dims.append(r)
# Preserve historical unreviewed-at-stage7 entry as history, clearly superseded.
for r in statuses:
 if r['status']=='third_moment_43D_g009_unreviewed':r['scope']+=' Historical stage7 cutoff only; superseded by the independently sealed stage8 discrete .09 certificate.'
recipe=[]
p=R+'uniform_seed_size_review/CLAIM_VERDICTS.json';v=source(p);assert v['status'].startswith('PASS')
for f in ['SEAL.json','REVIEW.md','independent_trials.json']:source(R+'uniform_seed_size_review/'+f)
source(R+'uniform_seed_size_diagnostics/uniform_seed_size_diagnostics.json')
p=R+'uniform_seed_size_review/independent_scalar.json';s=source(p)
for i,r in enumerate(s['rows']):
 n=r['n'];scope=('All legal completed time-first delays then specified joint-aware canonical conversion' if n<10 else 'First-G obstruction with four orthogonal denominator witnesses')
 recipe.append(dict(model='uniform_spin1_Heisenberg_chain',denominator_length=n,numerator_length=2*n,MPS_bond_dimension=26,retained_numerator_states=1,physical_denominator_dimension=3**n,physical_numerator_dimension=3**(2*n),quantity='upper cap on attainable certified lower ratio J_lower',upper_cap_exact=r['J_cap'],gap_lower_exact=None,beta_domain='all beta>=0',scope=scope,not_a_physical_purity_upper_bound=True,not_a_gap_bound=True,no_all_method_seed_minimum=True,primary_source=p,primary_json_pointer=f'/rows/{i}/J_cap',source_sha256=sources[p]))
 statuses.append(dict(model='uniform_spin1_Heisenberg_chain',parameter_exact=None,status='independently_sealed_fixed_D26_recipe_exclusion_n'+str(n),gap_lower_exact=None,evidence_source=p,evidence_sha256=sources[p],scope=scope+'. Fixed archived D26 one-Rayleigh numerator at 2n, any valid denominator upper traces. Not all MPS, adaptive schemes or physical gaplessness; no successful minimum seed.',plotted_as_zero_gap=False))
p=R+'joint_small_seed_review/ACCEPTANCE.json';s=source(p);assert s['status'].startswith('PASS');source(R+'joint_small_seed_review/PROOF.md')
for g in s['couplings']:
 statuses.append(dict(model='ordinary_spinhalf_bilayer',parameter_exact=g,status='independently_sealed_synchronous_mixed_cube_recipe_no_go',gap_lower_exact=None,evidence_source=p,evidence_sha256=sources[p],scope=s['accepted_scope']+' All finite beta>=0, seeds 2x2/4x2/4x4 and mirror. Excludes neither fresh trace injections, asynchronous other-base updates, stronger simultaneous optimizers nor all methods; not a gap bound.',plotted_as_zero_gap=False))
endpoint='17/200';piece_routes=deepcopy(data['ordinary_interval_piece_routes']);interval=False
p=R+'interval_range_009_review/results/SUMMARY.json'
if R+'interval_range_009_review/MANIFEST_SHA256.json' in accepted:
 s=source(p);assert s['accepted'] and s['status'].startswith('PASS');interval=True;endpoint='9/100'
 for f in ['REVIEW.md','REVIEW_STATUS.json']:source(R+'interval_range_009_review/'+f)
 add(s['extension_interval'][1],p,'/extension_all_integer_L_ge2_uniform_gap','range009_interval_extension','closed_interval',s['extension_interval'][0])
 add(s['combined_coupling_interval'][1],p,'/combined_all_integer_L_ge2_uniform_gap','uniform_interval_union','closed_interval','0')
 for i,a in enumerate(s['intervals']):
  r=add(a['coupling_interval'][1],p,f'/intervals/{i}/all_integer_L_ge2_gap','range009_interval_piece','closed_interval',a['coupling_interval'][0],a['beta_initial'],a['asymptotic_onset']);r['denominator_regime']='denominator_low_band'
 piece_routes.append('range009_interval_piece')
excited=[];excited_included=False;excited_text=None
if R+'mps_excited_seed_review/MANIFEST_SHA256.json' in accepted:
 excited_included=True
 for f in ['CLAIM_VERDICTS.json','SEAL.json','REVIEW.md','independent_physical.json']:source(R+'mps_excited_seed_review/'+f)
 p=R+'mps_excited_seed_review/independent_scalar.json';s=source(p);assert s['status'].startswith('PASS')
 for i,a in enumerate(s['rows']):
  n=a['n'];excited.append(dict(model='uniform_spin1_Heisenberg_chain',denominator_length=n,numerator_length=2*n,MPS_bond_dimension=26,excited_MPS_bond_dimension_upper=52,denominator_orthogonal_witnesses=3,retained_numerator_states=1,physical_denominator_dimension=3**n,physical_numerator_dimension=3**(2*n),quantity='upper envelope on attainable certified lower ratio J_lower',upper_cap_exact=a['max_J_upper'],gap_lower_exact=None,unresolved_boxes=a['unresolved_boxes'],all_beta_recipe_excluded=not a['unresolved_boxes'],no_successful_startup_claim=True,not_a_gap_bound=True,not_a_physical_purity_upper_bound=True,no_all_method_seed_minimum=True,primary_source=p,primary_json_pointer=f'/rows/{i}',source_sha256=sources[p]))
  statuses.append(dict(model='uniform_spin1_Heisenberg_chain',parameter_exact=None,status='independently_sealed_three_witness_'+('all_beta_recipe_exclusion' if n<24 else 'bounded_inconclusive_warm_window')+'_n'+str(n),gap_lower_exact=None,evidence_source=p,evidence_sha256=sources[p],scope='Archived D26 one-Rayleigh numerator; three orthogonal denominator witnesses, specified whole time-first delays and joint-aware conversion. No physical-purity upper bound, gap bound, all-method minimum seed or actual startup. n24 unresolved closed-box union [13/2,45/4].',plotted_as_zero_gap=False))
 excited_text='The [sealed core three-state review](../mps_excited_seed_review/REVIEW.md) independently verifies exact staggered source contractions and excludes the fixed one-Rayleigh D26 recipe for every beta≥0 at denominator lengths **n=14,16,20**. At **n=24**, the unresolved closed-box union is **[13/2,45/4] = [6.5,11.25]**; outside it the specified recipe is excluded. An optimistic upper orbit surviving inside the window does not certify realizable denominator bounds, actual startup or a physical gap. The three denominator witnesses have Sz=0,+1,−1 and are orthogonal fixed trials, not certified eigenvectors or a certified triplet. Ground MPS bond D=26 and single-source bond upper bound 52 are distinct from three linear witnesses and full Hilbert dimensions 3^n / 3^(2n). Exact physical tests through n6, source contractions through n24 and ground contractions through n48 are sealed. The separate longitudinal/momentum extensions are outside this snapshot. [Exact upper-envelope rows](excited_witness_upper_envelopes.csv).'
for r in claims:
 if r['parameter_kind']=='point':
  group=[a for a in claims if a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact']];r['plotted_in_main_figure']=r is max(group,key=lambda a:(F(a['gap_lower_exact']),a['id']))
 elif r['model']=='ordinary_spinhalf_bilayer':r['plotted_in_main_figure']=r['certificate_route']=='uniform_interval_union' and F(r['parameter_exact'])==F(endpoint)
data.update(snapshot_label='stage8',schema_version=5,generated_utc=datetime.now(timezone.utc).isoformat(),claims=claims,dimensions=dims,unplotted_status=statuses,sources=sources,review_seals=seals,preserved_stage7_files=preserved,ordinary_interval_endpoint=endpoint,ordinary_interval_piece_routes=piece_routes,ordinary_interval_piece_count=56 if interval else 49,interval_range_009_included=interval,third_moment_review_included=True,uniform_seed_size_review_included=True,joint_small_seed_review_included=True,recipe_upper_envelopes=recipe,claim_selection='Explicit immutable PASS review pins only; 198 inherited certificate rows retained; recipe upper envelopes kept separate from gap lower bounds',mps_excited_seed_review_included=excited_included,excited_witness_upper_envelopes=excited)
if excited_text:data['excited_witness_readme']=excited_text
data['stage7_publication']={'commit':'fb38f57548c86d9dda19450e68cbbedbafd6765a','tree':'de52aaf8e91dad68ccdc9e74f2fce0368be78212','evidence':'parent reported verified remote main publication; not a local Git checkout claim'}
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',claims),('trial_dimensions.csv',dims),('unplotted_status.csv',statuses),('ordinary_interval_pieces.csv',[r for r in claims if r.get('certificate_route') in piece_routes]),('latest_point_bounds.csv',[r for r in claims if r['parameter_kind']=='point' and r['plotted_in_main_figure']]),('recipe_upper_envelopes.csv',recipe),('excited_witness_upper_envelopes.csv',excited)]:csv_write(name,rows)
for name in ['tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv','reference_certificates.csv','chain_candidate_routes.csv']:(HERE/name).write_bytes((ROOT/(R+'overview_stage7')/name).read_bytes())
print(json.dumps(dict(status='PASS stage8 extraction',claims=len(claims),dimensions=len(dims),sources=len(sources),review_seals=len(seals),interval_included=interval)))
