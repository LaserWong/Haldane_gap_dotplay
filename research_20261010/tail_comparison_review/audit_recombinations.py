"""Independent frozen full-spectrum/trace/transport/all-size recombination audit.
No producer or previous reviewer module is executed. Prior accepted physical
moments are reused by exact sealed hashes; all new scalar consequences are rebuilt.
"""
from independent_math import *
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SRC=HERE/'snapshot';COMP=SRC/'low_band/tail_comparison';RESULT=HERE/'results'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(name,obj):(RESULT/name).write_text(json.dumps(obj,indent=2)+'\n')
VARIANTS=['original','jacobi','quadratic'];GVALUES=list(map(F,['3/100','1/25','1/20','3/50']));SHAPES=[(4,4),(8,4),(8,8)]

def check_hashes():
 for name,h in load(HERE/'INPUT_SHA256.json').items():assert sha(SRC/name)==h,name
 for name,prior in load(HERE/'PRIOR_REVIEW_SHA256.json').items():
  p=ROOT/name;assert sha(p/'MANIFEST_SHA256.json')==prior['manifest_sha256']
  for k,h in prior['files'].items():assert sha(p/k)==h,(name,k)
  for k,h in load(p/'INPUT_SHA256.json').items():assert sha(p/'snapshot'/k)==h,(name,k)
 freeze=load(COMP/'FROZEN_MANIFEST_1834.json')
 print('Producer manifest shape',list(freeze)[:6],flush=True)
 entries=freeze.get('files',freeze)
 for name,h in entries.items():
  if isinstance(h,dict):h=h['sha256']
  assert sha(COMP/name)==h,name
 assert sha(COMP/'FROZEN_MANIFEST_1834.json')=='ca267779b17e27a109cfc964c3ca6aaf6a5be9ba8cbc84b368e0c3fc0fc082dd'
 print('HASHED PHYSICAL AND TAIL PREREQUISITES PASS',flush=True)


def number_bins(rec,variant):
 nx,ny,n=rec['nx'],rec['ny'],rec['N'];g=F(rec['g']);assert n==nx*ny and F(rec['energy_shift'])==-F(3*n,4)
 ed=graph(nx,ny);degree=[0]*n
 for (i,j),w in ed.items():degree[i]+=w;degree[j]+=w
 assert degree==[4]*n;v=F(3,4)*g*g*sum(w*w for w in ed.values());kap=4*g*g
 if variant=='quadratic':
  assert rec['weighted_edges']==[[i,j,w] for (i,j),w in sorted(ed.items())]
  assert rec['bosonic_modes']==3*n and rec['physical_hilbert_dimension']==4**n
  assert F(rec['alpha'])==1-2*g and F(rec['vacuum_creation_norm_squared'])==v and F(rec['creation_matrix_norm_squared_upper'])==kap
  dl,du=F(rec['delta_lower']),F(rec['delta_upper']);assert 0<dl<du and dl*dl<=1-4*g<du*du
  assert F(rec['delta_squared'])==1-4*g
  el=-v/(1-2*g+dl);assert el==F(rec['bosonic_ground_lower'])
  index=1;assert len(rec['bins'])==n+1
  for q,row in enumerate(rec['bins']):
   m=math.comb(3*n+q-1,q);assert row['q']==q and row['multiplicity']==m and row['first_ordered_index']==index
   assert F(row['lower'])==el+q*dl;index+=m
  assert index-1==math.comb(4*n,n)>=4**n
  return [F(z['lower']) for z in rec['bins'][:3]],dict(reference_count=index-1,physical_count=4**n,overcount=True,pivots=0)
 occ,emp=occupied_bounds(nx,ny);assert rec['graph_counts']['occupied_edge_max']==occ and rec['graph_counts']['empty_edge_max']==emp and rec['graph_counts']['degrees']==degree
 diagonal=[(1-2*g)*q for q in range(n+1)];old=[F(3,4)*g*g*emp[q]*occ[q+2] for q in range(n-1)]
 if variant=='jacobi':
  assert rec['weighted_edges']==[[i,j,w] for (i,j),w in sorted(ed.items())]
  assert F(rec['vacuum_creation_norm_squared'])==v and F(rec['creation_matrix_norm_squared_upper'])==kap
  boson=[(q//2+1)*v+kap*((q+1)**2//4) for q in range(n-1)]
  assert list(map(F,rec['occupancy_offdiagonal_squared']))==old and list(map(F,rec['bosonic_offdiagonal_squared']))==boson
  off=[min(a,b) for a,b in zip(old,boson)]
 else:off=old
 assert list(map(F,rec['diagonal']))==diagonal and list(map(F,rec['offdiagonal_squared']))==off
 prev=None;index=1;pivots=0;assert len(rec['bins'])==n+1
 for q,row in enumerate(rec['bins']):
  assert row['q']==q and row['first_ordered_index']==index
  m=math.comb(n,q)*3**q;assert row['multiplicity']==m;index+=m
  starts=list(range(q,min(q+2,n+1)));assert len(row['parity_compressions'])==len(starts);low=[]
  for start,part in zip(starts,row['parity_compressions']):
   ids=list(range(start,n+1,2));assert part['number_indices']==ids;l=F(part['lower']);ps=[]
   for j,i in enumerate(ids):
    p=diagonal[i]-l-(off[ids[j-1]]/ps[-1] if j else 0);assert p>0;ps.append(p);pivots+=1
   assert ps==list(map(F,part['ldl_positive_pivots']));low.append(l)
  bound=min(low);bound=max(bound,prev) if prev is not None else bound
  assert bound==F(row['lower']);prev=bound
 assert index==4**n+1
 return [F(z['lower']) for z in rec['bins'][:3]],dict(physical_count=4**n,reference_count=4**n,overcount=False,pivots=pivots)


def audit_patch(rec):
 v=rec['tail_variant'];nx,ny,n,g=rec['nx'],rec['ny'],rec['N'],F(rec['g']);assert n==nx*ny and (nx,ny) in SHAPES and g in GVALUES
 paths=rec['source_sha256'];assert len(paths)==3
 for p,h in paths.items():assert sha(SRC/p)==h
 gr=load(SRC/next(p for p in paths if Path(p).name.startswith('block1_')))
 fr=load(SRC/next(p for p in paths if Path(p).name.startswith('translated_')))
 number=load(SRC/next(p for p in paths if 'bins_' in p));assert rec['number_sector_bins']==number
 a0,a1,a2=number_bins(number,v)[0];assert [a0,a1,a2]==[F(rec[k]) for k in ['global_ground_lower','all_excited_global_lower','global_lambda_kplus1_lower']]
 c=list(map(int,gr['coefficients']));den=gr['integer_matrix_denominator']
 def quad(k):return sum(c[i]*int(gr[k][i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
 norm,mean,second=[quad(k) for k in ['gram','shifted_hamiltonian_numerator','shifted_H2_numerator']]
 assert norm>0;rho=F(mean,den*norm);variance=F(second,den*den*norm)-rho*rho
 assert rho==F(gr['exact_rayleigh'])-F(gr['E00']) and variance==F(gr['exact_residual_squared'])>=0
 assert rho<a1<a2 and F(fr['ritz_max_upper'])<a2
 assert rec['relative_form_bound']==gr['relative_form_bound'];assert F(gr['E00'])==F(rec['energy_shift'])==-F(3*n,4)
 assert len(rec['blocks'])==2;ground,trip=rec['blocks'];endpoint=rho-variance/(a2-rho)
 assert ground['k']==ground['multiplicity']==1 and len(ground['eigen_lower'])==len(ground['eigen_upper'])==1
 assert F(ground['eigen_lower'][0])==endpoint and F(ground['eigen_upper'][0])==rho and F(rec['ground_width'])==rho-endpoint
 assert trip['k']==n and trip['multiplicity']==3
 assert len(trip['eigen_lower'])==len(trip['eigen_upper'])==len(trip['exact_Qsqrt2_Temple_endpoints'])==len(fr['modes'])==n
 for mode,l,u,st in zip(fr['modes'],trip['eigen_lower'],trip['eigen_upper'],trip['exact_Qsqrt2_Temple_endpoints']):
  theta,rr=qload(mode['theta']),qload(mode['residual_squared']);distance=qs((a2,F(0)),theta)
  assert qsign(distance)>0 and qsign(rr)>=0
  e=qs(theta,qd(rr,distance));assert e==qload(st)
  lower=F(l);assert lower<=F(u)<a2 and u==mode['theta_upper']
  assert qsign(qs(e,(lower,F(0))))>=0 and qsign(qs(qm(distance,qs(theta,(lower,F(0)))),rr))>=0
  # Lower endpoints use a 14-decimal grid and sit within one cell of the exact endpoint.
  assert (lower*10**14).denominator==1 and qsign(qs((lower+F(1,10**14),F(0)),e))>0
 assert rec['full_hilbert_dimension']==4**n and rec['retained_full_band_dimension']==1+3*n
 # Both number schemes agree only for the first 1+3N ordered levels.
 assert number['bins'][2]['first_ordered_index']==2+3*n
 return dict(variant=v,g=str(g),shape=f'{nx}x{ny}',cutoff=str(a2),cutoff_display=float(a2),ground_width=str(rho-endpoint),retained_full_band_dimension=1+3*n,full_hilbert_dimension=4**n,linear_ground_trial_dimension=len(c),all_full_band_endpoints_recomputed=True,counting=number_bins(number,v)[1])


def symbolic_paths():
 def mon(point,power):return Counter({point:power})
 def product(*terms):
  out=Counter()
  for t in terms:
   for p,k in t.items():out[p]+=k
  return {p:k for p,k in out.items() if k}
 def purity(p,axis):
  q=list(p);q[axis]+=1;q=tuple(q);return product(mon(q,1),mon(p,-2)),q
 out=[]
 for order in ['xyt','xty','txy']:
  axes=['xyt'.index(c) for c in order];points=[(0,0,0)];qs_=[]
  for axis in axes:
   q,p=purity(points[-1],axis);qs_.append(q);points.append(p)
  def power(d,k):return {p:v*k for p,v in d.items()}
  assert product(power(qs_[0],4),power(qs_[1],2),qs_[2])==product(mon(points[3],1),mon(points[0],-8))
  assert product(power(qs_[1],4),power(qs_[2],2))==product(mon(points[3],2),mon(points[1],-8))
  assert qs_[2]==product(mon(points[3],1),mon(points[2],-2))
  # Identity at arbitrary formal base, for each adjacent pair needed in transport.
  pairs=[] if order=='xyt' else [('t','y')] if order=='xty' else [('t','x'),('t','y')]
  for i,j in pairs:
   a,di=purity((2,3,4),'xyt'.index(i));b,_=purity(di,'xyt'.index(j));c,dj=purity((2,3,4),'xyt'.index(j));e,_=purity(dj,'xyt'.index(i))
   assert product(e,power(c,2))==product(b,power(a,2))
  out.append(dict(order=order,dyadic_coordinate_path=points,adjacent_swaps=pairs,identities_verified=True))
 save('path_ledger.json',out)


def audit_seed(recs,row,variant,g,short):
 order=row['order_before_transport'];beta=F(row['beta_initial']);assert row['accepted']
 e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
 q0=trace(recs[0],beta);q3=trace(recs[2],2*beta)
 i1,b1=(0,2*beta) if order[0]=='t' else (1,beta)
 i2,b2=(2,beta) if order[-1]=='t' else (1,2*beta)
 q1=trace(recs[i1],b1);q2=trace(recs[i2],b2)
 j1=floor(exp_bounds(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,10**16)
 j2=floor(exp_bounds(-4*beta*e[2]+8*b1*e[i1])[0]*q3[0]**2/q1[1]**8,10**16)
 c0=floor(exp_bounds(-2*beta*e[2]+2*b2*e[i2])[0]*q3[0]/q2[1]**2,10**16)
 independent_ratios=[j1,j2,c0];saved_ratios=[F(row[k]) for k in ['J1','J2','C0']]
 assert all(0<stored<=certified<=1 for stored,certified in zip(saved_ratios,independent_ratios)), (variant,str(g),order,[(str(x),str(y)) for x,y in zip(independent_ratios,saved_ratios)])
 # Producer 256-bit tail overcounts may be less sharp than our 384-bit enclosure.
 # Its saved lower witnesses remain valid and are used to replay its certificate.
 j1,j2,c0=saved_ratios
 a=floor(G(j1),10**16);b=floor(G(j2*a),10**16);c=floor(G(c0**4*a*a*b),10**16)
 assert [a,b,c]==list(map(F,row['permuted_first_purities']))
 moved=[a,b,c] if order=='xyt' else [a,b*sqrt_lower(c),b*b*c] if order=='xty' else [a*sqrt_lower(b),a*a*b*sqrt_lower(c),a**4*b*b*c]
 abc=[floor(z,10**18) for z in moved];assert abc==list(map(F,row['canonical_first_purities']))
 assert row['canonical_base']==dict(n=8,m=8,beta=str(2*beta))
 boot=row['bootstrap'];assert boot['status']=='accepted_analytic_scalar_certificate'
 assert abc==[F(boot['input'][k+'_lower']) for k in ['A','B','C']]
 assert boot['input']['n']==boot['input']['m']==8 and F(boot['input']['beta'])==2*beta
 defects=[ceil(1-z,10**18) for z in abc];n=8;temp=2*beta;states=[abc]
 for j,step in enumerate(boot['updates']):
  for _ in range(3):
   p=(1-defects[0])**4*(1-defects[1])**2*(1-defects[2]);assert 0<p<=1
   new=ceil((1-p)**2/(2*p*p),10**18);assert 0<=new<1;defects=defects[1:]+[new]
  assert step['round']==j+1 and list(map(F,step['defects']))==defects;n*=2;temp*=2;states.append([1-z for z in defects])
 assert n==boot['n']==boot['m'] and temp==F(boot['beta']) and len(boot['updates'])==boot['rounds']
 assert defects==list(map(F,boot['defects']));u=max(defects);assert u==F(boot['u']) and 0<u<=F(1,500)
 gap=floor(log_lower(1/(32*u))/temp,10**12)
 assert gap==F(boot['uniform_square_gap_lower']) and exp_bounds(temp*gap)[1]*32*u<1
 assert len(row['windows'])==len(states);windows=[];covered=set(range(2,8))
 for j,(w,state) in enumerate(zip(row['windows'],states)):
  nn=8*2**j;temperature=2*beta*2**j;purity,detail=interpolate_2d(*state)
  assert w['n']==nn and w['through']==2*nn and F(w['beta'])==temperature
  assert detail==w['details'] and purity==F(w['thermal_lower'])>F(1,2)
  gg=F(w['gap_lower']);assert gg>0 and exp_bounds(temperature*gg)[1]*(1-purity)<purity
  # Floating window proposal is accepted solely through the exact exponential witness.
  covered.update(range(nn,2*nn+1));windows.append(dict(n=nn,through=2*nn,gap=str(gg),required=nn<n))
 assert all(k in covered for k in range(2,n))
 target=min([gap,short]+[F(w['gap']) for w in windows if w['required']])
 assert target==F(row['all_integer_L_ge2_gap']) and short==F(row['uniform_small_L2_through_L7_gap'])
 return dict(variant=variant,g=str(g),order=order,beta_initial=str(beta),J1=str(j1),J2=str(j2),C0=str(c0),canonical_first_purities=list(map(str,abc)),accepted_beta=str(temp),asymptotic_onset=n,asymptotic_gap=str(gap),all_integer_L_ge2_gap=str(target),gap_display=float(target),windows=windows,small_L2_through_L7_gap=str(short),shifted_trace_bounds={name:list(map(str,q)) for name,q in [('q0',q0),('q1',q1),('q2',q2),('q3',q3)]},independent_exact_arithmetic=True,independent_ratio_floors=list(map(str,independent_ratios)),saved_ratios_are_conservative=True,ratio_rounding_differences=list(map(str,[x-y for x,y in zip(independent_ratios,saved_ratios)])))


def small_sizes():
 rows=[]
 for side in range(2,8):
  r=load(SRC/f'low_band/frontier_g006/small_sizes/number_bins_{side}x{side}_g3d50.json');a=number_bins(r,'original')[0][1];assert a>0
  # For every 0<=g<=.06, this very same real nonnegative comparison vector
  # has larger diagonals and no larger negative off-diagonal magnitudes.
  assert F(r['g'])==F(3,50)
  rows.append(dict(side=side,gap=str(a),valid_coupling_interval=['0','3/50'],comparison_form_uniformity=True))
 short=min(F(r['gap']) for r in rows)
 bridges=load(SRC/'low_band/frontier_g006/all_size_bridges.json')
 for row in bridges:
  assert len(row['small_sizes'])==6
  assert [(z['side'],F(z['gap_lower'])) for z in row['small_sizes']]==[(z['side'],F(z['gap'])) for z in rows]
 save('small_sizes.json',rows);return short


def main():
 started=time.monotonic();check_hashes();symbolic_paths();short=small_sizes();patches=[];accepted=[];comparisons=[]
 for variant in VARIANTS:
  summaries=load(COMP/variant/'summary.json');assert len(summaries)==4
  for g,summary in zip(GVALUES,summaries):
   tag=str(g).replace('/','d');recs=[load(COMP/variant/f'temple_{x}x{y}_g{tag}.json') for x,y in SHAPES]
   for rec in recs:patches.append(audit_patch(rec))
   assert summary==load(COMP/variant/f'recombined_g{tag}.json') and F(summary['g'])==g and summary['tail_variant']==variant
   assert sha(SRC/summary['shared_short_size_source'])==summary['shared_short_size_source_sha256']
   assert [r['order_before_transport'] for r in summary['results']]==['xyt','xty','txy']
   for row in summary['results']:
    if row.get('status')=='no_successful_float_proposal':
     assert variant=='original' and g==F(3,50) and row['order_before_transport']=='xyt'
     comparisons.append(dict(variant=variant,g=str(g),order='xyt',status='No accepted proposal on producer grid; not an all-beta exclusion'))
     continue
    result=audit_seed(recs,row,variant,g,short);accepted.append(result)
    comparisons.append({k:result[k] for k in ['variant','g','order','beta_initial','all_integer_L_ge2_gap','gap_display','asymptotic_onset']})
    print('EXACT ALL-SIZE PASS',variant,g,result['order'],result['gap_display'],flush=True)
    save('accepted_certificates.json',accepted)
   save('patch_review.json',patches)
 save('same_order_comparison.json',comparisons)
 gains=[]
 for g in GVALUES:
  values={v:next(r for r in accepted if r['g']==str(g) and r['variant']==v and r['order']=='txy') for v in VARIANTS}
  assert len({r['beta_initial'] for r in values.values()})==1
  d={v:F(r['all_integer_L_ge2_gap']) for v,r in values.items()}
  gains.append(dict(g=str(g),order='txy',common_beta=values['original']['beta_initial'],original=str(d['original']),jacobi=str(d['jacobi']),quadratic=str(d['quadratic']),jacobi_tail_gain=str(d['jacobi']-d['original']),quadratic_tail_gain=str(d['quadratic']-d['original']),quadratic_over_jacobi=str(d['quadratic']-d['jacobi'])))
 save('fixed_order_fixed_beta_gains.json',gains)
 # Re-read every frozen byte and every prerequisite manifest after calculations.
 check_hashes();save('summary.json',dict(status='PASS independent exact recombination audit',patches=len(patches),accepted_certificates=len(accepted),three_orders=True,prior_physical_moments_hash_reused=True,independent_band_trace_transport_recurrence_and_all_size_bridges=True,physical_and_oscillator_counts_never_pointwise_merged=True,best=[max((r for r in comparisons if r['g']==str(g) and 'gap_display' in r),key=lambda r:F(r['all_integer_L_ge2_gap'])) for g in GVALUES]))
 print('ALL RECOMBINATIONS PASS',len(patches),len(accepted),time.monotonic()-started,'seconds; maximum RSS KiB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)

if __name__=='__main__':main()
