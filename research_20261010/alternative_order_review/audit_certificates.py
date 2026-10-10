"""Independent g=3/50 complete-band, order-transport and all-size acceptance.
Uses only independent reviewer helpers; no producer modules are imported.
"""
from audit_physical import *
# Reuse the already-loaded specialization rather than execute a second helper
# initialization that would try to raise the inherited 1-GiB hard limit.
sys.modules['audit_large']=sys.modules['audit_physical']
import audit_tail_trace as sealed
HERE=OUT; SRC=HERE/'snapshot'
exp_independent=sealed.exp_independent
floor_grid=sealed.floor_grid;ceil_grid=sealed.ceil_grid;log_lower=sealed.log_lower
trace=sealed.trace

def check_hashes():
 inherited=load(HERE/'PRIOR_REVIEW_SHA256.json')
 assert hashlib.sha256((PRIOR/'MANIFEST_SHA256.json').read_bytes()).hexdigest()==inherited['manifest_sha256']
 for name,h in inherited['files'].items():assert hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==h,name
 for name,h in load(HERE/'INPUT_SHA256.json').items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==h,name
 for name,h in load(SRC/'geometry_source_sha256.json').items():
  assert hashlib.sha256((RESEARCH/name).read_bytes()).hexdigest()==h,name
  shape=Path(name).stem.removeprefix('geometry_')
  a=load(RESEARCH/name);b=load(PRIOR/'results'/f'geometry_{shape}.json')
  assert all(a[k]==b[k] for k in ['F','S','V','W'])
 for name in ['ground_replay.json','translation_replay.json']:
  rows=load(HERE/'results'/name);assert len(rows)==3 and all(F(r['g'])==F(3,50) for r in rows)
 print('INHERITED AND NEW PHYSICAL HASHES PASS',flush=True)

def local_number():
 weights=[2,1,2,1];m=[[F(0)]*16 for _ in range(16)];creation=[]
 for j in range(16):
  qj=(j//4!=0)+(j%4!=0)
  for a,b,v in KERNEL[j]:
   i=4*a+b;qi=(a!=0)+(b!=0);assert abs(qi-qj) in [0,2]
   if qi==qj:m[i][j]+=v
   if qi==qj+2:
    sq=v*v*F(weights[a]*weights[b],weights[j//4]*weights[j%4]);assert sq==F(1,4);creation.append([i,j,str(sq)])
  m[j][j]+=F(qj,2)
 m=[[m[i][j]*weights[i//4]*weights[i%4] for j in range(16)] for i in range(16)]
 inert=inertia(m);assert inert==(0,5,11) and len(creation)==3
 return list(inert),sorted(creation)
LOCAL=local_number()

def occupied_bounds(nx,ny):
 n=nx*ny;assert nx>=2 and ny>=2;out=[]
 for q in range(n+1):
  h=min(q,n-q);root=math.isqrt(4*h);root+=root*root<4*h
  iso=2*q-min(root,nx,ny)
  if nx>=4 and ny>=4 and nx%2==ny%2==0:
   comp=n-q;iso=min(iso,2*q,q*q//4,4*q-2*n+min(2*comp,comp*comp//4))
  out.append(iso)
 return out,[2*n-4*q+e for q,e in enumerate(out)]

def audit_number(rec):
 nx,ny,n=rec['nx'],rec['ny'],rec['N'];g=F(rec['g']);assert n==nx*ny and g==F(3,50)
 occ,emp=occupied_bounds(nx,ny);assert occ==rec['graph_counts']['occupied_edge_max'] and emp==rec['graph_counts']['empty_edge_max']
 assert rec['graph_counts']['degrees']==[4]*n
 assert F(rec['energy_shift'])==-F(3*n,4)
 local=rec['local_certificate'];assert local['preserving_plus_half_number_inertia']==LOCAL[0] and sorted(local['creation_entries_abs_squared'])==LOCAL[1]
 diagonal=[(1-2*g)*q for q in range(n+1)];off=[F(3,4)*g*g*emp[q]*occ[q+2] for q in range(n-1)]
 assert list(map(F,rec['diagonal']))==diagonal and list(map(F,rec['offdiagonal_squared']))==off
 prev=None;index=1
 assert len(rec['bins'])==n+1
 for q,row in enumerate(rec['bins']):
  assert row['q']==q and row['first_ordered_index']==index
  mult=math.comb(n,q)*3**q;assert row['multiplicity']==mult;index+=mult
  starts=list(range(q,min(q+2,n+1)));assert len(row['parity_compressions'])==len(starts)
  lows=[]
  for start,part in zip(starts,row['parity_compressions']):
   ids=list(range(start,n+1,2));assert part['number_indices']==ids;l=F(part['lower']);piv=[]
   for j,i in enumerate(ids):
    v=diagonal[i]-l-(off[ids[j-1]]/piv[-1] if j else 0);assert v>0;piv.append(v)
   assert piv==list(map(F,part['ldl_positive_pivots']));lows.append(l)
  bound=min(lows);bound=max(bound,prev) if prev is not None else bound
  assert bound==F(row['lower']);prev=bound
 assert index==4**n+1
 return [F(r['lower']) for r in rec['bins'][:3]]

def patches():
 out=[]
 for nx,ny in [(4,4),(8,4),(8,8)]:
  rec=load(SRC/f'temple_{nx}x{ny}_g3d50.json');gr=load(SRC/f'block1_{nx}x{ny}_g3d50.json');fr=load(SRC/f'translated_{nx}x{ny}_g3d50_fourier.json');num=load(SRC/f'number_bins_{nx}x{ny}_g3d50.json')
  for name,h in rec['source_sha256'].items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==h
  assert rec['nx']==nx and rec['ny']==ny and rec['N']==nx*ny and F(rec['g'])==F(3,50)
  assert rec['number_sector_bins']==num
  a0,a1,a=audit_number(num);assert [a0,a1,a]==[F(rec[k]) for k in ['global_ground_lower','all_excited_global_lower','global_lambda_kplus1_lower']]
  rho=F(gr['exact_rayleigh'])-F(gr['E00']);rr=F(gr['exact_residual_squared']);assert rho<a1<a
  assert rec['relative_form_bound']==gr['relative_form_bound']
  bl=rec['blocks'][0];endpoint=rho-rr/(a-rho)
  assert bl['k']==bl['multiplicity']==1 and len(bl['eigen_lower'])==len(bl['eigen_upper'])==1
  assert F(bl['eigen_lower'][0])==endpoint and F(bl['eigen_upper'][0])==rho
  assert F(rec['ground_width'])==rho-endpoint
  trip=rec['blocks'][1];assert trip['k']==nx*ny and trip['multiplicity']==3
  assert len(trip['eigen_lower'])==len(trip['eigen_upper'])==len(trip['exact_Qsqrt2_Temple_endpoints'])==len(fr['modes'])==nx*ny
  for m,l,u,saved_endpoint in zip(fr['modes'],trip['eigen_lower'],trip['eigen_upper'],trip['exact_Qsqrt2_Temple_endpoints']):
   theta=qload(m['theta']);variance=qload(m['residual_squared']);distance=qs((a,F(0)),theta)
   assert qsign(distance)>0 and qsign(variance)>=0
   endpoint=qs(theta,qd(variance,distance));assert endpoint==qload(saved_endpoint)
   l=F(l);assert l<=F(u)<a and qsign(qs(endpoint,(l,F(0))))>=0
   assert qsign(qs(qm(distance,qs(theta,(l,F(0)))),variance))>=0
   assert u==m['theta_upper']
  assert rec['full_hilbert_dimension']==4**(nx*ny) and rec['retained_full_band_dimension']==1+3*nx*ny
  assert F(rec['energy_shift'])==-F(3*nx*ny,4)
  out.append(dict(shape=f'{nx}x{ny}',g='3/50',all_number_bins_and_full_count_verified=True,all_sector_Temple_endpoints_verified=True,complete_band=1+3*nx*ny,trial_linear_dimension=gr['trial_subspace_dimension'],full_dimension=str(4**(nx*ny)),cutoff=str(a)))
  print('NEW PHYSICAL PATCH PASS',nx,ny,flush=True)
 save('patch_review.json',out)


def sqrt_lower(x):
 x=F(x);den=10**40;num=math.isqrt(x.numerator*den*den//x.denominator);lo=F(num,den)
 assert lo*lo<=x<(lo+F(1,den))**2
 return lo

def ratio_replay():
 out=[];recs=[load(SRC/f'temple_{x}x{y}_g3d50.json') for x,y in [(4,4),(8,4),(8,8)]]
 e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
 for order in ['xty','txy']:
  row=load(SRC/f'transported_{order}_g006.json');beta=F(row['beta_initial']);assert row['order']==order
  for name,h in row['source_sha256'].items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==h
  q0=trace(recs[0],beta);q3=trace(recs[2],2*beta)
  i1,b1=(0,2*beta) if order=='txy' else (1,beta)
  i2,b2=1,2*beta
  q1=trace(recs[i1],b1);q2=trace(recs[i2],b2)
  j1=floor_grid(exp_independent(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,10**16)
  j2=floor_grid(exp_independent(-4*beta*e[2]+8*b1*e[i1])[0]*q3[0]**2/q1[1]**8,10**16)
  c0=floor_grid(exp_independent(-2*beta*e[2]+2*b2*e[i2])[0]*q3[0]/q2[1]**2,10**16)
  assert [j1,j2,c0]==[F(row[k]) for k in ['J1','J2','third_original_staircase_ratio']]
  def G(z):assert 0<z<=1;return 1-(1-z)**2/(2*z*z)
  a=floor_grid(G(j1),10**16);b=floor_grid(G(j2*a),10**16);c=floor_grid(G(c0**4*a*a*b),10**16)
  assert [a,b,c]==list(map(F,row['permuted_first_purities']))
  moved=[a,b*sqrt_lower(c),b*b*c] if order=='xty' else [a*sqrt_lower(b),a*a*b*sqrt_lower(c),a**4*b*b*c]
  abc=[floor_grid(x,10**18) for x in moved];assert abc==list(map(F,row['canonical_first_purities']))
  boot=row['bootstrap'];assert abc==[F(boot['input'][k+'_lower']) for k in ['A','B','C']]
  assert row['canonical_base']=={'n':8,'m':8,'beta':str(2*beta)}
  assert boot['input']['n']==boot['input']['m']==8 and F(boot['input']['beta'])==2*beta
  defects=[ceil_grid(1-v,10**18) for v in abc];n=8;temperature=2*beta
  for j,step in enumerate(boot['updates']):
   for _ in range(3):
    product=(1-defects[0])**4*(1-defects[1])**2*(1-defects[2]);assert 0<product<=1
    new=ceil_grid((1-product)**2/(2*product*product),10**18);assert 0<=new<1;defects=defects[1:]+[new]
   assert step['round']==j+1 and list(map(F,step['defects']))==defects;n*=2;temperature*=2
  assert n==boot['n']==boot['m'] and temperature==F(boot['beta']) and len(boot['updates'])==boot['rounds']
  assert defects==list(map(F,boot['defects']));u=max(defects);assert u==F(boot['u']) and 0<u<=F(1,500)
  gap=floor_grid(log_lower(1/(32*u))/temperature,10**12)
  assert gap==F(boot['uniform_square_gap_lower']) and exp_independent(temperature*gap)[1]*32*u<1
  out.append(dict(order=order,g='3/50',beta_initial=str(beta),all_trace_ratios_first_cycle_transport_and_recursion_equal=True,gap=str(gap),gap_display=float(gap),asymptotic_L_ge=n))
  print('TRANSPORTED TRACE PASS',order,float(gap),flush=True)
 save('trace_review.json',out)
 return out


def validate_step(S,T,witness):
 S,T=F(S),F(T);p=S*S*T;assert p>F(1,2) and p==F(witness['p'])
 w=F(witness['dominant_weight_lower']);assert F(1,2)<w<=1 and (2*w-1)**2<=2*p-1
 r=F(witness['tail_ratio_upper']);assert r==(1-w)/w and 0<=r<1
 d=F(witness['d_lower']);assert d==T/(1+r*r)
 lower=F(witness['purity_lower']);scaled=lower/(1-r)
 assert lower>0 and scaled<=d and (scaled/S)**2<=d
 return lower

def audit_bridges():
 results=[];numbers={}
 for side in range(2,8):
  name=f'small_sizes/number_bins_{side}x{side}_g3d50.json';rec=load(SRC/name);a0,a1,a2=audit_number(rec);assert a1>0;numbers[side]=a1
  # Additional exhaustive geometry check on the three smallest tori.
  if side<=4:
   ed,_,_=graph(side,side);n=side*side;occ,_=occupied_bounds(side,side);actual=[0]*(n+1)
   for mask in range(1<<n):
    count=sum(w for (i,j),w in ed.items() if mask>>i&1 and mask>>j&1);q=mask.bit_count();actual[q]=max(actual[q],count)
   assert all(x<=y for x,y in zip(actual,occ))
  print('SMALL NUMBER BRIDGE PASS',side,float(a1),flush=True)
 for row in load(SRC/'all_size_bridges.json'):
  order=row['order'];source=SRC/f'transported_{order}_g006.json';assert hashlib.sha256(source.read_bytes()).hexdigest()==row['source_sha256']
  seed=load(source);boot=seed['bootstrap'];target=F(boot['uniform_square_gap_lower'])
  states=[list(map(F,seed['canonical_first_purities']))]+[[1-F(x) for x in step['defects']] for step in boot['updates']]
  covered=set();windows=[]
  assert len(row['small_sizes'])==6 and len(row['windows'])==len(states)
  for small in row['small_sizes']:
   side=small['side'];assert F(small['gap_lower'])==numbers[side]>=target;covered.add(side)
  for j,(window,abc) in enumerate(zip(row['windows'],states)):
   n=8*2**j;beta=2*F(seed['beta_initial'])*2**j;A,B,C=abc
   assert window['n']==n and window['through']==2*n and F(window['beta'])==beta
   detail=window['details'];S=F(detail['spatial_lower']);assert 0<S<=1 and S*S<=A**4*(2*B-1)
   T=validate_step(B,C,detail['y']);assert T==F(detail['transverse_thermal_lower'])
   purity=validate_step(S,T,detail['x']);assert purity==F(window['thermal_lower'])>F(1,2)
   gap=F(window['gap_lower']);assert gap>=target and exp_independent(beta*gap)[1]*(1-purity)<purity
   covered.update(range(n,2*n+1));windows.append(dict(n=n,through=2*n,gap=str(gap),gap_display=float(gap)))
  assert all(L in covered for L in range(2,boot['n']))
  assert F(row['asymptotic_gap'])==F(row['all_integer_L_ge2_gap'])==target
  results.append(dict(order=order,g='3/50',all_integer_square_L_ge=2,gap=str(target),gap_display=float(target),small_size_min=str(min(numbers.values())),finite_windows=windows,asymptotic_onset=boot['n']))
  print('ALL INTEGER SIZE PASS',order,float(target),flush=True)
 save('all_size_review.json',results)
 return results

if __name__=='__main__':
 check_hashes();patches();ratio_replay();results=audit_bridges()
 (HERE/'REVIEW_STATUS.json').write_text(json.dumps(dict(status='PASS independent physical, exact arithmetic, order-transport, and all-integer-size review',updated_at_utc='2026-10-10T18:24:00Z',updated_at_local='2026-10-10T14:24:00-04:00',symbolic_paths=dict(six_orders=True,adjacent_swaps=12,sequential_rotations=18),model='ordinary spin-1/2 square bilayer; rung exchange 1; equal straight intralayer couplings g=3/50; no crossed exchange',boundary='Periodic positive-direction edge multiplicity, including parallel edges at side 2',accepted=results,prior_geometry_manifest_sha256=load(HERE/'PRIOR_REVIEW_SHA256.json')['manifest_sha256'],producer_freeze_sha256=hashlib.sha256((HERE/'PRODUCER_FREEZE_1818.json').read_bytes()).hexdigest(),new_physical_scope='Three g=3/50 ground and translated-band records, number bins and complete-band Temple endpoints rebuilt; sealed coupling-independent geometry inherited by exact hash',qualification='Unique finite-volume ground states; no arbitrary aspect-ratio or infinite-volume ground-state uniqueness conclusion; not proof-assistant verified'),indent=2)+'\n')
