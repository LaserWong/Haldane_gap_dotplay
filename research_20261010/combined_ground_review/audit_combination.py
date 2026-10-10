"""Independent direct-physical-trace audit of frozen combined certificates.
Consumes only frozen JSON. No producer/reviewer modules are imported.
"""
from independent_math import *
import json,hashlib,time,copy
from pathlib import Path
HERE=Path(__file__).resolve().parent;S=HERE/'snapshot';R=S/'research_20261010';C=R/'low_band/combined_ground_bounds';OUT=Path(os.environ.get('COMBINED_REVIEW_OUTPUT',str(HERE/'results')));OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(n,d):(OUT/n).write_text(json.dumps(d,indent=2)+'\n')

def verify_inputs():
 entries=load(HERE/'INPUT_SHA256.json')
 for p,h in entries.items():assert sha(S/p)==h,p
 return len(entries)

def seals():
 rows=[];allseals=load(HERE/'PRIOR_REVIEW_SHA256.json')
 for name,entry in allseals.items():
  p=R/name/'MANIFEST_SHA256.json';assert sha(p)==entry['manifest_sha256']
  assert load(p)==entry['files'];status=load(R/name/'REVIEW_STATUS.json');assert 'pass' in status['status'].lower()
  rows.append(dict(review=name,manifest_sha256=sha(p),sealed_files=len(entry['files']),status=status['status']))
 save('dependency_seals.json',rows)
 return {name:set(entry['files'].values()) for name,entry in allseals.items()}

def audit_bins(r):
 nx,ny=r['nx'],r['ny'];n=nx*ny;g=F(r['g']);bins=r['number_sector_bins'];ed=edges(nx,ny)
 assert r['N']==n and r['full_hilbert_dimension']==4**n and r['retained_full_band_dimension']==1+3*n
 assert F(r['energy_shift'])==-F(3*n,4)
 deg=[0]*n
 for (i,j),w in ed.items():deg[i]+=w;deg[j]+=w
 assert deg==[4]*n and bins['weighted_edges']==[[i,j,w] for (i,j),w in sorted(ed.items())]
 v=F(3,4)*g*g*sum(w*w for w in ed.values());alpha=1-2*g;delta=F(bins['delta_lower']);du=F(bins['delta_upper'])
 assert 0<delta<du and delta*delta<=1-4*g<du*du
 assert F(bins['alpha'])==alpha and F(bins['vacuum_creation_norm_squared'])==v and F(bins['creation_matrix_norm_squared_upper'])==4*g*g
 assert F(bins['delta_squared'])==1-4*g and bins['bosonic_modes']==3*n and bins['physical_hilbert_dimension']==4**n
 energy=-v/(alpha+delta);assert energy==F(bins['bosonic_ground_lower'])
 first=1;assert len(bins['bins'])==n+1
 for q,z in enumerate(bins['bins']):
  mult=math.comb(3*n+q-1,q)
  assert z['q']==q and z['multiplicity']==mult and z['first_ordered_index']==first and F(z['lower'])==energy+q*delta
  first+=mult
 assert first-1==math.comb(4*n,n)>=4**n and bins['bins'][2]['first_ordered_index']==2+3*n
 assert [F(r[k]) for k in ['global_ground_lower','all_excited_global_lower','global_lambda_kplus1_lower']]==[energy,energy+delta,energy+2*delta]
 return dict(physical_dimension=4**n,reference_count=first-1,oscillator_count_preserved=True)

def audit_patch(p,sealed):
 rec=load(p);variant=rec['combination_variant'];assert variant==p.parent.name;g=F(rec['g']);nx,ny=rec['nx'],rec['ny'];n=nx*ny
 src=rec['recombination_source_sha256'];assert len(src)==2
 basep=R/next(s for s in src if Path(s).name.startswith('temple_'));fp=R/next(s for s in src if Path(s).name.startswith('filtered_'))
 for q in [basep,fp]:assert sha(q)==src[str(q.relative_to(R))]
 b=load(basep);f=load(fp)
 assert sha(fp) in sealed['variational_filter_review']
 assert sha(basep) in sealed['ground_moment_review' if variant=='combined' else 'tail_comparison_review' if g<=F(3,50) else 'bilayer_frontier_review']
 # Byte-accepted base, unchanged in every substantive field except ground upper/width.
 expected=copy.deepcopy(b);expected['status']=rec['status'];expected['combination_variant']=variant;expected['new_trial_residual_claim']=False;expected['recombination_source_sha256']=src
 expected['blocks'][0]['unfiltered_eigen_upper']=b['blocks'][0]['eigen_upper'][:]
 expected['blocks'][0]['eigen_upper']=[f['shifted_rayleigh_upper']]
 expected['blocks'][0]['upper_endpoint_meaning']=rec['blocks'][0]['upper_endpoint_meaning']
 expected['ground_width']=str(F(f['shifted_rayleigh_upper'])-F(b['blocks'][0]['eigen_lower'][0]))
 assert rec==expected,p
 assert F(f['coupling'])==g and [f['nx'],f['ny']]==[nx,ny] and f['energy_shift']==rec['energy_shift']
 assert F(f['exact_original_shifted_rayleigh'])==F(b['blocks'][0]['eigen_upper'][0])
 assert f['physical_spins']==2*n and f['full_dimension']==4**n and f['original_trial_dimension']==(11 if n==16 else 29)
 assert f['implicit_filtered_trial_states']==1 and f['local_filter_plane_dimension_upper']==2 and f['residual_parity']=='even'
 grpath=S/f['source'];assert sha(grpath)==f['source_sha256'];assert f['source'].removeprefix('research_20261010/') in rec['source_sha256']
 gr=load(grpath);c=list(map(int,gr['coefficients']));den=gr['integer_matrix_denominator']
 quad=lambda key:sum(c[i]*int(gr[key][i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
 norm,first,second=[quad(k) for k in ['gram','shifted_hamiltonian_numerator','shifted_H2_numerator']]
 rho=F(first,den*norm);variance=F(second,den*den*norm)-rho*rho
 assert rho==F(f['exact_original_shifted_rayleigh']) and variance==F(f['exact_original_variance']) and variance>0
 low,upper=map(F,[rec['blocks'][0]['eigen_lower'][0],rec['blocks'][0]['eigen_upper'][0]])
 assert low<=upper<rho and F(rec['ground_width'])==upper-low
 if variant=='combined':
  endpoint=R/'low_band/ground_moment_pencil'/rec['ground_moment_pencil_source'];assert sha(endpoint)==rec['ground_moment_pencil_source_sha256']
  assert sha(endpoint) in sealed['ground_moment_review'];e=load(endpoint)
  assert low==F(e['ground_lower']) and rho==F(e['ground_upper']) and e['ground_trial_dimension']==len(c)
 counts=audit_bins(rec)
 assert rec['blocks'][0]['k']==rec['blocks'][0]['multiplicity']==1
 assert rec['blocks'][1]['k']==n and rec['blocks'][1]['multiplicity']==3
 return dict(variant=variant,g=str(g),shape=[nx,ny],ground_lower=str(low),filtered_upper=str(upper),original_upper=str(rho),ground_width=str(upper-low),original_trial_dimension=len(c),physical_spins=2*n,retained_low_band=1+3*n,filtered_states=1,filter_plane_dimension_at_most=2,unchanged_triplet_tail=True,physical_dependency_hashes_matched=True,**counts)

def short_sizes():
 # Exact g=.06 occupancy/Jacobi comparison for every L=2,...,7.
 bridge=load(R/'low_band/frontier_g006/all_size_bridges.json')[0]['small_sizes'];small=[]
 for item in bridge:
  side=item['side'];b=load(R/'low_band/frontier_g006'/item['number_file']);n=side*side;g=F(3,50)
  assert b['N']==n and F(b['g'])==g and b['nx']==b['ny']==side
  occupied=[]
  for q in range(n+1):
   h=min(q,n-q);root=math.isqrt(4*h);root+=root*root<4*h;z=2*q-min(root,side)
   if side>=4 and side%2==0:z=min(z,2*q,q*q//4,4*q-2*n+min(2*(n-q),(n-q)**2//4))
   occupied.append(z)
  empty=[2*n-4*q+z for q,z in enumerate(occupied)]
  assert occupied==b['graph_counts']['occupied_edge_max'] and empty==b['graph_counts']['empty_edge_max']
  diagonal=[(1-2*g)*q for q in range(n+1)];off=[F(3,4)*g*g*empty[q]*occupied[q+2] for q in range(n-1)]
  assert diagonal==list(map(F,b['diagonal'])) and off==list(map(F,b['offdiagonal_squared']))
  # For the first excited index only q=0,1 monotonization enters. Replay every bin as an extra check.
  previous=None;first=1;count=0
  for q,z in enumerate(b['bins']):
   assert z['q']==q and z['first_ordered_index']==first and z['multiplicity']==math.comb(n,q)*3**q
   first+=z['multiplicity'];values=[]
   for part,start in zip(z['parity_compressions'],range(q,min(q+2,n+1))):
    ids=list(range(start,n+1,2));assert part['number_indices']==ids;l=F(part['lower']);piv=[]
    for j,i in enumerate(ids):
     p=diagonal[i]-l-(off[ids[j-1]]/piv[-1] if j else 0);assert p>0;piv.append(p);count+=1
    assert piv==list(map(F,part['ldl_positive_pivots']));values.append(l)
   val=min(values);val=max(val,previous) if previous is not None else val;assert val==F(z['lower']);previous=val
  assert first==4**n+1 and F(b['bins'][1]['lower'])==F(item['gap_lower'])>0
  small.append(dict(side=side,gap=item['gap_lower'],strictly_positive_pivots=count,comparison_uniform_g=['0','3/50']))
 short06=min(F(x['gap']) for x in small)
 # Uniform .10 quadratic comparison, including period-two multiplicities.
 d=load(R/'low_band/frontier_g007_g010/short_sizes/uniform_short_sizes.json');sums=[sum(w*w for w in edges(k,k).values()) for k in range(2,8)]
 assert sums==d['weighted_edge_square_sums']==[16,18,32,50,72,98]
 delta=F(d['delta_lower']);alpha=F(d['alpha_lower']);v=F(d['vacuum_creation_norm_squared_upper'])
 assert alpha==F(4,5) and 0<delta*delta<=F(3,5) and v==F(147,200)
 short10=delta-v/(alpha+delta);assert short10==F(d['gap_lower'])>0
 save('short_size_review.json',dict(small_006=small,minimum_006=str(short06),uniform_010=dict(sides=list(range(2,8)),weighted_edge_square_sums=sums,gap=str(short10),gap_display=float(short10),comparison_uniform_g=['0','1/10']),gap_monotonicity_assumed=False))
 return short06,short10

def symbolic():
 def add(*dicts):
  out=Counter()
  for d in dicts:
   for k,v in d.items():out[k]+=v
  return {k:v for k,v in out.items() if v}
 def mult(d,n):return {k:v*n for k,v in d.items()}
 def purity(p,axis):
  q=list(p);q[axis]+=1;q=tuple(q);return {q:1,p:-2},q
 ledger=[]
 for order in ['txy','xty','xyt']:
  p=(0,0,0);points=[p];qs=[]
  for c in order:q,p=purity(p,'xyt'.index(c));qs.append(q);points.append(p)
  assert add(mult(qs[0],4),mult(qs[1],2),qs[2])=={points[3]:1,points[0]:-8}
  assert add(mult(qs[1],4),mult(qs[2],2))=={points[3]:2,points[1]:-8}
  swaps=[] if order=='xyt' else [('t','y')] if order=='xty' else [('t','x'),('t','y')]
  for i,j in swaps:
   a,pi=purity((2,3,4),'xyt'.index(i));b,_=purity(pi,'xyt'.index(j));c,pj=purity((2,3,4),'xyt'.index(j));e,_=purity(pj,'xyt'.index(i))
   assert add(e,mult(c,2))==add(b,mult(a,2))
  ledger.append(dict(order=order,path=points,swaps=swaps,correlated_identities_exact=True))
 save('symbolic_transport.json',ledger)

def audit_row(recs,row,variant,g,short,ground_only=False):
 beta=F(row['beta_initial']);order=row['order_before_transport'];ind=ratios(recs,beta,order,ground_only);saved=[F(row[k]) for k in ['J1','J2','C0']]
 assert all(0<x<=y<=1 for x,y in zip(saved,ind)),(variant,g,order,ground_only,list(zip(saved,ind)))
 v=first_steps(saved);out=dict(variant=variant,g=str(g),order=order,beta=str(beta),ground_only_numerator=ground_only,accepted=row['accepted'],independent_direct_trace_ratio_lower=list(map(str,ind)),saved_ratio_lower=list(map(str,saved)),saved_witnesses_conservative=True)
 if 'permuted_prefix' in row:
  assert not row['accepted'] and v==list(map(F,row['permuted_prefix'])) and min(v)<=0
  return dict(out,failure='first-cycle nonpositive',all_beta_exclusion=False)
 assert v==list(map(F,row['permuted_first_purities'])) and min(v)>0
 abc=move(v,order);assert abc==list(map(F,row['canonical_first_purities']))
 assert row['canonical_base']==dict(n=8,m=8,beta=str(2*beta));boot=row['bootstrap']
 assert boot['input']==dict(A_lower=str(abc[0]),B_lower=str(abc[1]),C_lower=str(abc[2]),n=8,m=8,beta=str(2*beta))
 defects=[up(1-x,10**18) for x in abc];states=[abc];n=8;temp=2*beta
 for j,step in enumerate(boot['updates']):
  assert max(defects)>F(1,500)
  defects=cycle(defects);assert defects is not None and defects==list(map(F,step['defects'])) and step['round']==j+1
  n*=2;temp*=2;states.append([1-x for x in defects])
 if not row['accepted']:
  assert boot['status']=='bound_left_purity_domain' and max(defects)>F(1,500) and cycle(defects) is None
  return dict(out,failure='recurrence left positivity',all_beta_exclusion=False)
 assert boot['status']=='accepted_analytic_scalar_certificate' and n==boot['n']==boot['m'] and temp==F(boot['beta'])
 assert len(boot['updates'])==boot['rounds'] and defects==list(map(F,boot['defects']))
 u=max(defects);assert u==F(boot['u']) and 0<u<=F(1,500)
 asym=F(boot['uniform_square_gap_lower']);assert asym>0 and exponential(temp*asym)[1]*32*u<1
 assert len(row['windows'])==len(states);windows=[]
 for j,(w,state) in enumerate(zip(row['windows'],states)):
  nn=8*2**j;tt=2*beta*2**j;p,detail=interpolate2(state)
  assert w['n']==nn and w['through']==2*nn and F(w['beta'])==tt and F(w['thermal_lower'])==p and w['details']==detail
  gap=F(w['gap_lower']);assert gap>0 and p>F(1,2) and exponential(tt*gap)[1]*(1-p)<p
  windows.append(dict(n=nn,through=2*nn,gap=str(gap),gap_display=float(gap),required=nn<n))
 # Explicit interval coverage: short sizes 2..7, adjacent overlapping finite windows,
 # followed by the independently checked small-defect theorem for every L>=n.
 cursor=8
 for w in windows:
  if w['required']:assert w['n']==cursor;cursor=w['through']
 assert cursor==n
 final=min([short,asym]+[F(w['gap']) for w in windows if w['required']])
 assert final==F(row['all_integer_L_ge2_gap']) and short==F(row['uniform_small_L2_through_L7_gap'])
 assert row['all_integer_gap_display']==float(final)
 return dict(out,canonical=list(map(str,abc)),onset=n,asymptotic_gap=str(asym),all_integer_L_ge2_gap=str(final),gap_display=float(final),finite_windows=windows,short_bound=str(short),complete_integer_cover=True)

def main():
 start=time.monotonic();count=verify_inputs();sealed=seals();short06,short10=short_sizes();symbolic();patches=[];accepted=[];failed=[];optional=[]
 for variant in ['combined','filter_only']:
  d=C/variant;summary=load(d/'summary.json');assert summary==[load(d/('combined_g'+z['g'].replace('/','d')+'.json')) for z in summary]
  assert len(summary)==7
  for data in summary:
   g=F(data['g']);short=short06 if g<=F(3,50) else short10
   paths=[d/f'patch_{nx}x{ny}_g{str(g).replace("/","d")}.json' for nx,ny in [(4,4),(8,4),(8,8)]];recs=[load(p) for p in paths]
   for p in paths:patches.append(audit_patch(p,sealed))
   assert [z['order_before_transport'] for z in data['results']]==['txy','xty','xyt']
   for row in data['results']:
    result=audit_row(recs,row,variant,g,short);(accepted if row['accepted'] else failed).append(result)
    if 'largest_ground_only_replay' in row:
     result0=audit_row(recs,row['largest_ground_only_replay'],variant,g,short,True);assert result0['accepted'] and F(result0['all_integer_L_ge2_gap'])<=F(result['all_integer_L_ge2_gap']);optional.append(result0)
    print('PASS',variant,g,row['order_before_transport'],result.get('gap_display',result.get('failure')),flush=True)
    save('accepted_certificates.json',accepted);save('selected_failures.json',failed);save('ground_only_certificates.json',optional)
   save('patch_review.json',patches)
 assert len(patches)==42 and len(accepted)==30 and len(failed)==12 and len(optional)==11
 verify_inputs();save('summary.json',dict(status='PASS independent combined scalar and all-size review',frozen_inputs=count,patches=42,selected_orders=42,accepted_full_band=30,selected_failures=12,accepted_ground_only=11,all_beta_exclusion=False,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,arithmetic='512-bit outward exponentials and exact rational scalars; direct physical shifted traces',cpu_affinity=list(os.sched_getaffinity(0)),address_space_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0]))
 print('ALL COMBINED CERTIFICATES PASS',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
