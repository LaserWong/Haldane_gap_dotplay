"""Independent local identities, Jacobi bins, sector endpoints, and trace replay.
Imports only independent reviewer code, never producer modules.
"""
from audit_large import *
from functools import lru_cache

def matching_list(vertices):
 if not vertices:yield ();return
 a=vertices[0]
 for b in vertices[1:]:
  for rem in matching_list(tuple(v for v in vertices if v not in (a,b))):yield ((a,b),)+rem

def canonical(pairs):return tuple(sorted(tuple(sorted(p)) for p in pairs))
def expand_matching(pairs):
 v={0:1}
 for i,j in pairs:
  v={s|(a<<(2*i))|(b<<(2*j)):c*t for s,c in v.items() for a,b,t in [(1,3,-2),(2,2,1),(3,1,-2)]}
 return v

def audit_local():
 n=6;nx,ny=3,2;g=F(3,100);den=400;ed,_,_=graph(nx,ny);count=0
 for q in [0,2,4,6]:
  for verts in itertools.combinations(range(n),q):
   for pairs in matching_list(verts):
    pairs=canonical(pairs);p={i:j for a,b in pairs for i,j in [(a,b),(b,a)]};symbolic=defaultdict(int);symbolic[pairs]+=den*q
    for (a,b),mul in ed.items():
     h=6*mul
     if a not in p and b not in p:symbolic[canonical(pairs+((a,b),))]+=h
     elif a in p and b in p:
      if p[a]==b:
       symbolic[pairs]-=2*h;symbolic[canonical(t for t in pairs if a not in t)]+=3*h
      else:
       rest=tuple(t for t in pairs if a not in t and b not in t);x,y=p[a],p[b]
       symbolic[canonical(rest+((a,y),(b,x)))]+=h
       symbolic[canonical(rest+((a,b),(x,y)))]-=h
       symbolic[canonical(rest+((x,y),))]+=h
     else:
      old,new=(a,b) if a in p else (b,a)
      symbolic[canonical(tuple(new if k==old else k for k in t) for t in pairs)]+=h
    expanded=defaultdict(int)
    for matching,c in symbolic.items():
     for state,v in expand_matching(matching).items():expanded[state]+=c*v
    expanded={s:c for s,c in expanded.items() if c}
    assert expanded==apply(expand_matching(pairs),nx,ny,g);count+=1
 all6=list(matching_list(tuple(range(6))));mask=sum(1<<(2*i) for i in range(6))
 for a in all6:
  for b in all6:
   v=expand_matching(a);w=expand_matching(b);ip=sum(c*w.get(s,0)*(1<<(6-(s&mask).bit_count())) for s,c in v.items())
   unseen=set(range(6));loops=0
   while unseen:
    reached={next(iter(unseen))}
    while True:
     new=reached|{j for pair in a+b for i,j in [pair,pair[::-1]] if i in reached}
     if new==reached:break
     reached=new
    unseen-=reached;loops+=1
   assert ip==2**6*3**loops
 w=[2,1,2,1];pres=[[F(0) for _ in range(16)] for _ in range(16)];creation=[]
 for j in range(16):
  qj=(j//4!=0)+(j%4!=0)
  for a,b,v in KERNEL[j]:
   i=4*a+b;qi=(a!=0)+(b!=0)
   assert abs(qi-qj) in [0,2]
   if qi==qj:pres[i][j]+=v
   if qi==qj+2:
    r=v*v*F(w[a]*w[b],w[j//4]*w[j%4]);assert r==F(1,4);creation.append(r)
  pres[j][j]+=F(qj,2)
 weighted=[[pres[i][j]*w[i//4]*w[i%4] for j in range(16)] for i in range(16)]
 assert inertia(weighted)[0]==0 and len(creation)==3
 result=dict(matching_actions_checked=count,all_225_q6_Gram_entries_checked=True,local_number_preserving_PSD_inertia=inertia(weighted),three_creation_entry_squares=list(map(str,creation)),source='Independent physical four-spin kernel from frozen low_band_review, no producer kernel imported')
 save('local_identities.json',result);print('LOCAL IDENTITIES PASS',flush=True)

def uppercounts(nx,ny):
 n=nx*ny;out=[]
 for q in range(n+1):
  h=min(q,n-q);ceil=math.isqrt(4*h);ceil+=ceil*ceil<4*h
  iso=2*q-min(ceil,nx,ny)
  assert nx%2==ny%2==0 and nx>=4 and ny>=4
  direct=min(2*q,q*q//4);cq=n-q;complement=4*q-2*n+min(2*cq,cq*cq//4)
  out.append(min(iso,direct,complement))
 return out,[2*n-4*q+z for q,z in enumerate(out)]

def audit_number(rec):
 nx,ny,n=rec['nx'],rec['ny'],rec['N'];g=F(rec['g']);assert nx*ny==n
 occ,emp=uppercounts(nx,ny);assert rec['graph_counts']['occupied_edge_max']==occ and rec['graph_counts']['empty_edge_max']==emp
 assert rec['graph_counts']['degrees']==[4]*n
 diagonal=[(1-2*g)*q for q in range(n+1)];off=[F(3,4)*g*g*emp[q]*occ[q+2] for q in range(n-1)]
 assert list(map(F,rec['diagonal']))==diagonal and list(map(F,rec['offdiagonal_squared']))==off
 prev=None;index=1
 for q,row in enumerate(rec['bins']):
  assert row['q']==q and row['first_ordered_index']==index
  mult=math.comb(n,q)*3**q;assert row['multiplicity']==mult;index+=mult
  lows=[]
  for start,part in zip(range(q,min(q+2,n+1)),row['parity_compressions']):
   ids=list(range(start,n+1,2));assert part['number_indices']==ids;l=F(part['lower']);ps=[]
   for j,i in enumerate(ids):
    pivot=diagonal[i]-l-(off[ids[j-1]]/ps[-1] if j else 0);assert pivot>0;ps.append(pivot)
   assert ps==list(map(F,part['ldl_positive_pivots']));lows.append(l)
  lower=min(lows);lower=max(lower,prev) if prev is not None else lower
  assert F(row['lower'])==lower;prev=lower
 assert index==4**n+1 and len(rec['bins'])==n+1
 return [F(row['lower']) for row in rec['bins'][:3]]

def audit_patches():
 results=[]
 for nx,ny in [(4,4),(8,4),(8,8)]:
  for g in map(F,['3/100','1/25','1/20']):
   tag=f'translated_{nx}x{ny}_g{g}'.replace('/','d');rec=load(REF/f'{tag}_block1_low_band.json');num=load(REF/(f'number_bins_{nx}x{ny}_g{g}.json'.replace('/','d')))
   assert rec['number_sector_bins']==num;a0,a1,a2=audit_number(num)
   ground=RESEARCH/rec['ground_source'];fourier=BAND/rec['fourier_source'];gr=load(ground);fr=load(fourier)
   assert hashlib.sha256(ground.read_bytes()).hexdigest()==rec['ground_source_sha256'];assert hashlib.sha256(fourier.read_bytes()).hexdigest()==rec['fourier_source_sha256']
   rho=F(gr['exact_rayleigh'])-F(gr['E00']);rr=F(gr['exact_residual_squared']);assert rho<a1<a2
   angle=rr/(a2-rho)**2;assert 0<=angle<1;bg=a2-(a2-a0)*angle
   assert bg==F(rec['ground_complement_lower']);bs=[];angles=[]
   for mode in fr['modes']:
    th=F(mode['theta_upper']);r2=F(mode['residual_squared_upper']);assert th<a2
    a=r2/(a2-th)**2;assert 0<=a<1;angles.append(a);bs.append(a2-(a2-a1)*a)
   assert angles==list(map(F,rec['triplet_angle_squared_upper'])) and bs==list(map(F,rec['triplet_sector_complement_lowers']))
   b=min(bg,*bs);assert b==F(rec['orthogonal_complement_lower']) and b>max(rho,*[F(m['theta_upper']) for m in fr['modes']])
   assert a0==F(rec['global_ground_lower']) and a1==F(rec['all_excited_global_lower']) and a2==F(rec['global_lambda_kplus1_lower'])
   bl=rec['blocks'][0];l=F(bl['eigen_lower'][0]);assert l<=rho and l<b and (b-l)*(rho-l)>=rr
   assert F(bl['eigen_upper'][0])==rho and bl['multiplicity']==bl['k']==1
   assert bl['trial_dimension']==gr['trial_subspace_dimension']
   trip=rec['blocks'][1];assert trip['k']==nx*ny and trip['multiplicity']==3
   for mode,l,u,margin in zip(fr['modes'],trip['eigen_lower'],trip['eigen_upper'],trip['schur_Qsqrt2_margins']):
    th=qload(mode['theta']);r2=qload(mode['residual_squared']);l=F(l);assert l<b and qsign(qs(th,(l,F(0))))>=0
    diff=qs(qm((b-l,F(0)),qs(th,(l,F(0)))),r2);assert qsign(diff)>=0 and diff==qload(margin)
    assert u==mode['theta_upper']
   assert rec['full_hilbert_dimension']==4**(nx*ny) and rec['retained_full_band_dimension']==1+3*nx*ny
   assert len(trip['eigen_lower'])==len(trip['eigen_upper'])==len(trip['schur_Qsqrt2_margins'])==nx*ny
   assert F(rec['energy_shift'])==-F(3*nx*ny,4)
   results.append(dict(shape=f'{nx}x{ny}',g=str(g),every_number_bin_and_LDL_pivot_replayed=True,full_Hilbert_count=4**(nx*ny),retained_band=1+3*nx*ny,all_sector_angles_and_Schur_endpoints_verified=True,ground_complement=str(bg),global_complement=str(b),ground_width=str(rho-F(bl['eigen_lower'][0]))))
   print('PATCH PASS',nx,ny,g,flush=True)
 save('patch_replay.json',results)

BITS=384;GRID=1<<BITS
def floor_grid(x,grid=GRID):return F(x.numerator*grid//x.denominator,grid)
def ceil_grid(x,grid=GRID):return -floor_grid(-x,grid)
@lru_cache(None)
def exp_independent(x):
 # Different order and reduction from producer: exact series at <=1/8,
 # followed by a single 384-bit enclosure and directed squares.
 x=F(x);y=abs(x);k=0
 while y>F(1,8):y/=2;k+=1
 term=total=F(1)
 for j in range(1,91):term*=y/j;total+=term
 lo=floor_grid(total);hi=ceil_grid(total+(term*y/91)/(1-y/92))
 for _ in range(k):lo=floor_grid(lo*lo);hi=ceil_grid(hi*hi)
 return (lo,hi) if x>=0 else (floor_grid(1/hi),ceil_grid(1/lo))

def trace(rec,beta):
 shift=F(rec['blocks'][0]['eigen_upper'][0]);lo=hi=F(0)
 for block in rec['blocks']:
  for l,u in zip(block['eigen_lower'],block['eigen_upper']):
   lo+=block['multiplicity']*exp_independent(-beta*(F(u)-shift))[0]
   hi+=block['multiplicity']*exp_independent(-beta*(F(l)-shift))[1]
 tail=sum(row['multiplicity']*exp_independent(-beta*(F(row['lower'])-shift))[1] for row in rec['number_sector_bins']['bins'][2:])
 return lo,hi+tail,tail

def log_lower(x):
 assert x>1;k=0
 while x>=2:x/=2;k+=1
 def atom(t):
  z=(t-1)/(t+1);return 2*sum((z**(2*j+1)/F(2*j+1) for j in range(100)),F(0))
 return k*atom(F(2))+atom(x)

def audit_traces():
 result=[]
 for g in map(F,['3/100','1/25','1/20']):
  saved=load(REF/(f'large_seed_g{g}.json'.replace('/','d')));row=saved['exact'];beta=F(row['beta_initial']);assert row['order']=='xyt'
  recs=[load(REF/(f'translated_{nx}x{ny}_g{g}_block1_low_band.json'.replace('/','d'))) for nx,ny in [(4,4),(8,4),(8,8)]]
  e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
  q0,q1,q2=[trace(r,beta) for r in recs];q3=trace(recs[-1],2*beta)
  J1=floor_grid(exp_independent(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,10**16)
  J2=floor_grid(exp_independent(-4*beta*e[2]+8*beta*e[1])[0]*q3[0]**2/q1[1]**8,10**16)
  C=floor_grid(q3[0]/q2[1]**2,10**16)
  assert [J1,J2,C]==[F(row[k]) for k in ['J1','J2','C']]
  def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
  A1=floor_grid(G(J1),10**16);B1=floor_grid(G(J2*A1),10**16);C1=floor_grid(G(C**4*A1*A1*B1),10**16)
  assert [A1,B1,C1]==list(map(F,row['first_purities']))
  boot=row['bootstrap'];assert boot['input']['n']==boot['input']['m']==8 and F(boot['input']['beta'])==2*beta
  defect=[ceil_grid(1-v,10**18) for v in [A1,B1,C1]];n=8;b=2*beta
  for i,step in enumerate(boot['updates']):
   for _ in range(3):
    product=(1-defect[0])**4*(1-defect[1])**2*(1-defect[2]);assert 0<product<=1
    new=ceil_grid((1-product)**2/(2*product**2),10**18);assert 0<=new<1;defect=defect[1:]+[new]
   assert step['round']==i+1 and list(map(F,step['defects']))==defect;n*=2;b*=2
  assert n==boot['n']==boot['m'] and b==F(boot['beta']) and len(boot['updates'])==boot['rounds']
  assert defect==list(map(F,boot['defects']));u=max(defect);assert u==F(boot['u']) and 0<u<=F(1,500)
  gap=floor_grid(log_lower(1/(32*u))/b,10**12);assert gap==F(boot['uniform_square_gap_lower'])
  assert exp_independent(b*gap)[1]*32*u<1
  result.append(dict(g=str(g),beta_initial=str(beta),independent_384bit_trace_replay=True,J1=str(J1),J2=str(J2),C=str(C),all_first_cycle_and_bootstrap_fractions_equal=True,all_integer_square_scope_L_ge=n,gap=str(gap),gap_display=float(gap)))
  print('TRACE PASS',g,n,float(gap),flush=True);save('trace_replay.json',result)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--part',choices=['local','patch','trace'],required=True);args=p.parse_args()
 {'local':audit_local,'patch':audit_patches,'trace':audit_traces}[args.part]()
