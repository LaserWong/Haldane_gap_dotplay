#!/usr/bin/env python3
"""Explicitly select sealed mathematical claims. Does not run spectral research."""
from common import *
from copy import deepcopy
import argparse
from datetime import datetime,timezone
ap=argparse.ArgumentParser();ap.add_argument('--include-combined',action='store_true');ap.add_argument('--include-interval-extension',action='store_true');args=ap.parse_args()
old=R+'overview/overview_data.json'
data=json.loads((ROOT/old).read_text())
for p,h in data['sources'].items():assert sha(ROOT/p)==h,p
sources=deepcopy(data['sources']);claims=deepcopy(data['claims']);dims=deepcopy(data['dimensions']);statuses=deepcopy(data['unplotted_status']);seals=[]
def source(path):
    b=(ROOT/path).read_bytes();sources[path]=hashlib.sha256(b).hexdigest()
    return json.loads(b) if path.endswith('.json') else b.decode()
def seal(folder,manifest='MANIFEST_SHA256.json'):
    p=R+folder+'/'+manifest
    accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text())
    assert p in accepted and sha(ROOT/p)==accepted[p],('Unaccepted or changed review seal',p)
    n=manifest_check(p);source(p)
    seals.append({'directory':R+folder,'manifest':p,'sha256':sources[p],'verified_files':n})
seal('overview','SHA256SUMS.json');source(old)
for folder in ['reduced_input_review','bilayer_frontier_review','ordinary_interval_review','ground_moment_review','variational_filter_review']:
    seal(folder)
seal('chain_temperature_review','SHA256SUMS.json')
for row in claims:row['snapshot_stage']='previous_sealed_overview'

def add(model,param,value,primary,pointer,proofs,kind='point',lo=None,beta=None,onset=None,route=None,note='',rank=None,higher=None):
    gap=str(F(ptr(source(primary),pointer)))
    for p in proofs:source(p)
    row=dict(id='stage6_'+primary.replace('/','_')+'__'+pointer.replace('/','_'),model=model,parameter=param,parameter_exact=str(F(value)),parameter_lower_exact=None if lo is None else str(F(lo)),parameter_decimal=float(F(value)),parameter_kind=kind,fixed_J_exact='3/10' if model=='fully_frustrated_bilayer' else None,unit_coupling='strong bond = 1' if model=='alternating_spin1_chain' else 'rung = 1',gap_lower_exact=gap,gap_lower_decimal_down_12=floor12(gap),size_variable='M (two-spin cells)' if model=='alternating_spin1_chain' else 'L (square side)',integer_size_min=2,unique_finite_volume_ground_state=True,boundary='periodic; positive-direction adjacency multiplicities retained at size 2',evidence_status='independent_review_passed',initial_beta_exact=beta,asymptotic_base_size=onset,primary_source=primary,primary_json_pointer=pointer,primary_sha256=sources[primary],evidence_sources=[primary]+proofs,notes=note,certificate_route=route,numerator_trial_rank=rank,largest_higher_moments_used=higher,snapshot_stage='stage6',tail_variant=None,bootstrap_order=None,plotted_in_main_figure=True)
    claims.append(row);return row

def dim(model,g,shape,full,proposal,p,pointer,route,retained=None,rank=None,upper=None,q=None,note='',expanded=None,reached=None):
    source(p)
    n=int(shape[2:]) if shape.startswith('M=') else __import__('math').prod(map(int,shape.split('x')))
    a=dict(model=model,parameter_exact=g,seed_geometry=shape,full_Hilbert_dimension=full,retained_low_band_count=retained,proposal_basis_dimension=proposal,expanded_vector_support=expanded,full_H_applied_support=reached,MPS_bond_dimension=None,support_scope=route,support_depth=None,evidence_source=p,evidence_json_pointer=pointer,evidence_sha256=sources[p],notes=note,dimer_or_rung_count=n,physical_spin_count=2*n,numerator_trial_rank=rank,implicit_filtered_space_dimension_upper=upper,filtered_max_triplet_number=q)
    dims.append(a);return a

# Exact temperature-first chain certificates. Historical obstruction rows retain their recipe scope.
p=R+'chain_temperature_review/SUMMARY.json';s=source(p);assert s['status']=='PASS'
for i,a in enumerate(s['results']):
    if a['gap'] is None:
        statuses.append(dict(model='alternating_spin1_chain',parameter_exact=a['g'],status='temperature_first_bounded_grid_no_success',gap_lower_exact=None,evidence_source=p,evidence_sha256=sources[p],scope='Recorded finite beta grid only. Neither an all-temperature obstruction nor physical gaplessness.'))
        continue
    tag={'323/2000':'g323d2000','13/80':'g13d80','7/40':'g7d40'}[a['g']]
    q=R+f'chain_temperature_review/review_{tag}.json';d=source(q)
    add('alternating_spin1_chain','g',a['g'],p,f'/results/{i}/gap',[R+'chain_temperature_review/REVIEW.md',q],beta=a['beta'],onset=a['asymptotic_from'],route='temperature_first_Rayleigh_numerator',rank=1,higher=False,note='Every integer M>=2. Largest M=8 input uses only a Rayleigh quotient. Older order-specific obstruction remains valid for its different recipe.')
    x=d['largest_Rayleigh_only'];dim('alternating_spin1_chain',a['g'],'M=8',x['full_dimension'],x['dimension'],q,'/largest_Rayleigh_only','largest numerator Rayleigh-only trial',rank=1,note='One numerator vector from the indicated search space. No retained eigenstate count or largest full residual is required.')
    x=d['small_physical_input']['check'];dim('alternating_spin1_chain',a['g'],'M=4',x['full_dimension'],x['trial_dimension'],q,'/small_physical_input/check','smaller denominator complete trace',retained=1,expanded=x['trial_dimension'],reached=x['full_Hv_support'])

# Largest-patch first-moment reduction, keeping all eight compared accepted choices.
p=R+'reduced_input_review/results/all_size_replay.json';s=source(p)
for i,a in enumerate(s):
    assert a['all_integer_square_L_ge']==2
    row=add('ordinary_spinhalf_bilayer','g',a['g'],p,f'/{i}/gap',[R+'reduced_input_review/REVIEW.md',R+'reduced_input_review/REVIEW_STATUS.json'],beta=a['beta_initial'],onset=a['asymptotic_onset'],route='reduced_first_moment_'+a['mode'],rank=a['numerator_trial_rank'],higher=False,note='At the largest 8x8 patch only G/K (plus G/A for the optional 193-direction numerator) is needed. Numerator directions are trials, not an asserted complete eigenband.')
    row['bootstrap_order']='txy';row['tail_variant']='quadratic'
p=R+'reduced_input_review/REVIEW_STATUS.json'
dim('ordinary_spinhalf_bilayer','3/100;1/25;1/20;3/50','8x8',2**128,29,p,'','reduced largest first-moment numerator',rank=1,note='One trial optimized in a 29-dimensional space. Complete upper-trace certification ends at 8x4 rungs.')

# Independently reviewed old full-band frontier, retained even when superseded.
p=R+'bilayer_frontier_review/results/accepted_certificates.json';s=source(p)
for i,a in enumerate(s):
    row=add('ordinary_spinhalf_bilayer','g',a['g'],p,f'/{i}/all_integer_L_ge2_gap',[R+'bilayer_frontier_review/REVIEW_STATUS.json',R+'bilayer_frontier_review/REVIEW.md'],beta=a['beta_initial'],onset=a['asymptotic_onset'],route='full_band_frontier',note='Independently accepted isolated g=.07 point. Not a continuous interval by itself.')
    row['bootstrap_order']=a['order'];row['tail_variant']=a['variant']

# Whole interval and every closed subinterval are both available as exact rows.
p=R+'ordinary_interval_review/results/SUMMARY.json';s=source(p);assert s['closed_intervals']==16
add('ordinary_spinhalf_bilayer','g','7/100',p,'/all_integer_L_ge2_uniform_gap',[R+'ordinary_interval_review/REVIEW_STATUS.json',R+'ordinary_interval_review/REVIEW.md'],kind='closed_interval',lo='0',route='uniform_interval_union',rank=1,higher=False,note='Union of 16 independently audited adjacent closed pieces. Uniform across every 0<=g<=.07 and every integer L>=2.')
for i,a in enumerate(s['intervals']):
    lo,hi=a['coupling_interval']
    r=add('ordinary_spinhalf_bilayer','g',hi,p,f'/intervals/{i}/all_integer_L_ge2_gap',[R+'ordinary_interval_review/REVIEW.md'],kind='closed_interval',lo=lo,beta=a['beta_initial'],onset=a['asymptotic_onset'],route='uniform_interval_piece',rank=1,higher=False,note='This exact closed piece is part of the 16-piece interval theorem. Three fixed vectors are used, one per physical geometry. The largest numerator is G/K-only.')
    r['plotted_in_main_figure']=False
for shape,k in [('4x4',0),('8x4',1),('8x8',2)]:
    n=__import__('math').prod(map(int,shape.split('x')))
    dim('ordinary_spinhalf_bilayer','0<=g<=7/100',shape,4**n,s['trial_dimensions'][k],p,f'/trial_dimensions/{k}','continuous interval fixed-vector construction',retained=1 if k<2 else None,rank=1 if k==2 else None,note='Search dimensions 11/29/29. Smaller denominators retain one certified ground level. Largest numerator is one trial, with no required eigenstate identification or higher moment.')

# Ground inverse-moment improvement has its own independent all-size seal.
p=R+'ground_moment_review/REVIEW_STATUS.json';st=source(p);assert st['status']=='PASS independent exact certificate review'
p=R+'ground_moment_review/results/accepted_certificates.json';s=source(p)
for i,a in enumerate(s):
    r=add('ordinary_spinhalf_bilayer','g',a['g'],p,f'/{i}/all_integer_L_ge2_gap',[R+'ground_moment_review/REVIEW_STATUS.json',R+'ground_moment_review/REVIEW.md'],beta=a['beta_initial'],onset=a['asymptotic_onset'],route='full_ground_inverse_moment',higher=True,note='Same existing ground search and higher moments. Complete retained physical band and exact all-size bridge independently reviewed.')
    r['bootstrap_order']=a['order'];r['tail_variant']=a['variant']
for g in st['failed_grid_couplings']:
    statuses.append(dict(model='ordinary_spinhalf_bilayer',parameter_exact=g,status='ground_moment_only_bounded_grid_no_success',gap_lower_exact=None,evidence_source=R+'ground_moment_review/REVIEW_STATUS.json',evidence_sha256=sources[R+'ground_moment_review/REVIEW_STATUS.json'],scope=st['failure_scope']+' Different filtered-numerator routes must be judged separately.'))

# Dimension accounting is certified by the filter audit; it alone proves no new gap.
p=R+'variational_filter_review/REVIEW_STATUS.json';s=source(p);assert s['status']=='independent_review_pass'
for q in sorted((ROOT/(R+'variational_filter_review/snapshot/reviewed_filter_final')).glob('filtered_*.json')):
    p=str(q.relative_to(ROOT));a=source(p)
    d=dim('ordinary_spinhalf_bilayer',a['coupling'],f"{a['nx']}x{a['ny']}",a['full_dimension'],a['original_trial_dimension'],p,'','filtered implicit numerator span',rank=1,upper=a['original_space_plus_residual_dimension_upper'],q=a['filtered_trial_max_triplet_number'],note='The original 11/29/29 search plus a single residual direction lies in dimension <=12/30/30. Rank-one numerator is not a one-dimensional search. Existing G/K/J and q<=6 leakage are used. No filtered residual or eigenvalue isolation is claimed here.')
    d['original_max_triplet_number']=a['original_trial_max_triplet_number'];d['additional_evidence_sources']=[R+'variational_filter_review/REVIEW.md',R+'variational_filter_review/REVIEW_STATUS.json']
source(R+'variational_filter_review/REVIEW.md')

# Combined branch is admitted only after the independent review has been sealed.
if args.include_combined:
    from combined_selection import add_combined
    add_combined(globals())

if args.include_interval_extension:
    from interval_extension_selection import add_interval_extension
    add_interval_extension(globals())

# Isolated point selection never interpolates or assumes monotonicity.
for row in claims:
    if row['parameter_kind']=='point':
        group=[r for r in claims if r['model']==row['model'] and r['parameter_kind']=='point' and r['parameter_exact']==row['parameter_exact']]
        best=max(group,key=lambda r:(F(r['gap_lower_exact']),r['id']))
        row['plotted_in_main_figure']=row is best
# Mark old method failures as local even when the same coupling now succeeds.
for s in statuses:
    s['plotted_as_zero_gap']=False
    if s['model']=='alternating_spin1_chain' and s['status']=='independently_reviewed_recipe_obstruction':
        s['scope']+=' A different temperature-first, Rayleigh-only-largest route is independently successful at this same coupling in stage6.'
for r in dims:
    for k in ['numerator_trial_rank','implicit_filtered_space_dimension_upper','filtered_max_triplet_number','original_max_triplet_number']:r.setdefault(k,None)
now=datetime.now(timezone.utc).isoformat()
out=dict(schema_version=3,snapshot_label='stage6',generated_utc=now,claim_selection='Explicit sealed reviews selected by build_snapshot.py',source_commit_reported_by_project=data['source_commit_reported_by_project'],git_checkout_verified=False,root_note='Materialized tree has no .git metadata. Provenance is by immutable file hashes.',claims=claims,dimensions=dims,unplotted_status=statuses,analytic_reference=data['analytic_reference'],sources=sources,review_seals=seals,recombination_comparisons=data['recombination_comparisons'],previous_overview_sha256=sha(ROOT/old),combined_review_included=args.include_combined,interval_extension_included=args.include_interval_extension,combined_route_comparisons=globals().get('COMBINED_COMPARISONS'))
(HERE/'overview_data.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(seals,indent=2)+'\n')
for name,rows in [('certified_bounds.csv',claims),('trial_dimensions.csv',dims),('unplotted_status.csv',statuses),('ordinary_interval_pieces.csv',[r for r in claims if r.get('certificate_route') in ['uniform_interval_piece','filtered_interval_extension_piece']]),('latest_point_bounds.csv',[r for r in claims if r['parameter_kind']=='point' and r['plotted_in_main_figure']])]:csv_write(name,rows)
for name in ['tail_order_comparison.csv','fixed_order_tail_gains.csv']:
    (HERE/name).write_bytes((ROOT/(R+'overview')/name).read_bytes())
print(json.dumps({'status':'PASS extraction','claims':len(claims),'dimensions':len(dims),'sources':len(sources),'sealed_reviews':len(seals),'combined_included':args.include_combined}))
