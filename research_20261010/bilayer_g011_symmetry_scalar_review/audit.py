import os,resource,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
from functools import lru_cache
import json,hashlib,itertools,math,time,copy
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;S=H/'snapshot';P0=S/'producer';DATA=P0/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=time.process_time()
# Import only the previously independently accepted physical proof library; limit calls are clamped.
real=resource.setrlimit
def clamp(which,limits):
 hard=resource.getrlimit(which)[1];real(which,tuple(min(v,hard) for v in limits))
resource.setrlimit=clamp;sys.path.insert(0,str(S/'physical_library'));import physical_library as P
resource.setrlimit=real
D=10**60
def floor(x):return F(x.numerator*D//x.denominator,D)
def root(x):
 assert x>=0;k=math.isqrt(x.numerator*D*D//x.denominator);assert F(k*k,D*D)<=x<F((k+1)**2,D*D);return F(k,D)
@lru_cache(None)
def ex(x):return P.exp(x)
def G(x):assert 0<x<=1;return floor(1-(1-x)**2/(2*x*x))
def bil(c,a):return sum(c[i]*a[i][j]*c[j] for i in range(len(c)) for j in range(len(c)))
def zero(n):return [[F(0)]*n for _ in range(n)]
def split_rayleigh(shape,geo,c,g):
 nx,ny=shape;N=nx*ny;e=Counter();orbs=[];classes={}
 for x,y in itertools.product(range(nx),range(ny)):
  a=x*ny+y
  for b in (((x+1)%nx)*ny+y,x*ny+(y+1)%ny):e[tuple(sorted((a,b)))]+=1
 for a,b in itertools.combinations(range(N),2):
  ax,ay=divmod(a,ny);bx,by=divmod(b,ny);dx=min((ax-bx)%nx,(bx-ax)%nx);dy=min((ay-by)%ny,(by-ay)%ny);key=tuple(sorted((dx,dy))) if nx==ny else(dx,dy)
  if key not in classes:classes[key]=len(orbs);orbs.append([])
  orbs[classes[key]].append((a,b))
 n=len(orbs);b=n+1;dim=4*n+1;assert n==geo['orbits'] and len(c)==dim;diag=[1]+[3*len(o) for o in orbs];gram=zero(dim);A=zero(dim)
 for i in range(b):gram[i][i]=diag[i]
 for j in range(b):
  pair=defaultdict(F);vac=F(0)
  if j==0:
   for ed,w in e.items():pair[ed]+=w
  else:
   for a,c0 in orbs[j-1]:
    w=e.get((a,c0),0);pair[a,c0]-=2*w;vac+=3*w
    for (u,v),w in e.items():
     if u in (a,c0) and v not in(a,c0):pair[tuple(sorted((v,c0 if u==a else a)))]+=w
     elif v in(a,c0) and u not in(a,c0):pair[tuple(sorted((u,c0 if v==a else a)))]+=w
  A[0][j]=vac
  for i,orb in enumerate(orbs,1):
   vals={pair[x] for x in orb};assert len(vals)==1;A[i][j]=diag[i]*vals.pop()
 for i in range(n):
  for j in range(n):
   f,s,v,w,x,y,z=[F(geo[k][i][j]) for k in ('F','S','V','W','X','Y','Z')];li,ri,mi=b+i,b+n+i,b+2*n+i;lj,rj,mj=b+j,b+n+j,b+2*n+j
   gram[li][lj]=f;gram[li][rj]=gram[rj][li]=s;gram[ri][rj]=v;gram[mi][mj]=w
   A[1+i][lj]=A[lj][1+i]=f;A[1+i][rj]=A[rj][1+i]=s;A[li][lj]=s;A[li][rj]=A[rj][li]=v;A[li][mj]=A[mj][li]=w;A[ri][rj]=x;A[ri][mj]=A[mj][ri]=y;A[mi][mj]=z
 assert all(A[i][j]==A[j][i] and gram[i][j]==gram[j][i] for i in range(dim) for j in range(dim))
 q=[0]+[2]*n+[4]*(2*n)+[6]*n;Q=[[gram[i][j]*q[j] for j in range(dim)] for i in range(dim)];norm=bil(c,gram);assert norm>0;coeff=[bil(c,Q)/norm,bil(c,A)/(2*norm)];return norm,coeff,coeff[0]+g*coeff[1]

def main():
 assert sha(P0/'MANIFEST_SHA256.json')=='11c4405ac1528973eebaecaa1d7c8d655f6b14aa4d240f0b491446239b46d45e'
 for f,h in load(P0/'MANIFEST_SHA256.json').items():assert sha(P0/f)==h
 assert sha(S/'physical_library/MANIFEST_SHA256.json')=='9c6a17ceb920c20f323ccd27751b2d863f264566b0b1c8d46d5db4f2ea50c053'
 for f,h in load(S/'physical_library/MANIFEST_SHA256.json').items():assert sha(S/'physical_library'/f)==h
 P.verify()
 for name,expected in [('bilayer_split_pencil_optimization_review','fc205510f91902c1c9da6ba9bbdedefe69900a0fb1505fbd541aefe312417381'),('bilayer_short_bridge_refinement_review','49bc11944d411a6342f18b3661173fab47c4298d4932a1ce750befe244bc2d7a'),('bilayer_square_symmetry_window_review','890e942c8a7e37cbefc5b8de52f40f8d61cbfefe76e03f8a71f9dec8d66648cc'),('bilayer_square_symmetry_recurrence_review','21577fcf285cc7e53c6c4acdbdfa1086f1b7dd88f6f30c4e87e0ebf5f0ac5e83')]:
  assert sha(S/name/'MANIFEST_SHA256.json')==expected
  mf=load(S/name/'MANIFEST_SHA256.json')
  for f in ('audit.json','ACCEPTANCE.json','PROOF.md'):
   if (S/name/f).exists():assert sha(S/name/f)==mf[f]
 tm=load(S/'third_moment_review/MANIFEST_SHA256.json');tm=tm.get('files',tm);assert sha(S/'third_moment_review/results/geometry_8x8.json')==tm['results/geometry_8x8.json']
 d=next(x['data'] for x in load(DATA/'bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100));g=F(11,100)
 old=[];patches=[]
 for i,t in enumerate(d['denominator_patches']+[d['largest_base_trial']]):
  rho,info=P.physical_trial(t,i,g,g);old.append(P.poly(rho,g));patches.append(info)
 # Reconstruct all split-space Rayleigh uppers from accepted cached geometry, including numerator57D.
 opts=load(DATA/'bilayer_split_basis_plan/reoptimization.json')['results'];uppers={};upper_proof=[]
 for shape in ((4,4),(8,4),(8,8)):
  row=next(x['split'] for x in opts if x['shape']==list(shape) and F(x['g'])==g)
  geo=load(S/'third_moment_review/results/geometry_8x8.json') if shape==(8,8) else load(P.S/('GEOMETRY_%dx%d.json'%shape))
  norm,co,rho=split_rayleigh(shape,geo,list(map(F,row['integer_coefficients'])),g)
  assert norm==F(row['norm']) and co==list(map(F,row['rayleigh_coefficients'])) and rho==F(row['rayleigh']);uppers[math.prod(shape)]=rho
  upper_proof.append(dict(shape=list(shape),dimension=len(row['integer_coefficients']),norm=str(norm),rayleigh=str(rho)))
 e4=next(x for x in load(S/'physical_library/audit.json')['physical_endpoints'] if x['shape']==[4,4] and F(x['g'])==g);e8=next(x for x in load(S/'bilayer_split_pencil_optimization_review/audit.json')['physical_endpoints'] if F(x['g'])==g)
 lowers=[F(e4['ground_lower']),F(e8['ground_lower'])];assert lowers[0]<uppers[16] and lowers[1]<uppers[32]
 src=load(DATA/'bilayer_split_pencil_scalar/result.json')['results'][0];assert F(src['g'])==g
 for i,phys in enumerate(src['physical']):
  N=phys['N'];assert F(phys['ground_lower'])==lowers[i] and F(phys['trace_pivot'])==old[i] and F(phys['best_upper'])==uppers[N]
  floorodd=P.reference(N,g,1)-old[i];assert floorodd==F(phys['odd_floor']);patches[i]['odd']=[max(floorodd,x) for x in patches[i]['odd']]
 energies={'J1':8*old[0]-2*uppers[64],'J2':16*old[0]-4*uppers[64],'C0':4*old[1]-2*uppers[64]}
 def seed(beta,delta):
  widths=[old[i]-lowers[i]-(delta if i==1 else 0) for i in range(2)];assert min(widths)>=0;totals=[]
  for i,factor in ((0,1),(0,2),(1,2)):
   b=beta*factor;p=patches[i];N=p['N'];ground=ex(b*widths[i])[1];odd=3*sum(ex(-b*x)[1] for x in p['odd']);tail=sum(math.comb(3*N+q-1,q)*ex(-b*p['lower'][q-1])[1] for q in range(2,N+1));totals.append(ground+odd+tail)
  return {k:floor(ex(beta*energies[k])[0]/totals[i]**power) for k,i,power in [('J1',0,8),('J2',1,8),('C0',2,2)]}
 def first(r):
  a=G(r['J1']);b=G(r['J2']*a);c=G(r['C0']**4*a*a*b);assert min(a,b,c)>0;return[a,b,c]
 def advance(v):
  a,b,c=v;aa=G(a**4*b*b*c)
  if aa<=0:return None
  bb=G(aa*c*c)
  if bb<=0:return None
  cc=G(c**4*aa*aa*bb);return[aa,bb,cc] if cc>0 else None
 def window(v):
  a,b,c=v
  if min(b,c)<=F(1,2):return F(0)
  s=floor(b*b*root(2*c-1))
  return floor(a**4*(2*b-1)*root(2*s-1)) if s>F(1,2) else F(0)
 def canonical(v):
  a,b,c=v;return[floor(a*root(b)),floor(a*a*b*root(c)),floor(a**4*b*b*c)]
 results=[]
 for pair in load(P0/'exact_results.json')['results']:
  for kind in ('actual','hypothetical'):
   rec=pair[kind];beta=F(rec['beta_initial']);delta=F(rec['ground32_improvement_hypothetical']);assert (delta==0)==(kind=='actual')
   if delta:assert delta==F(rec['required_improvement']) and F(rec['target_ground32_lower'])==lowers[1]+delta<uppers[32]
   r=seed(beta,delta)
   assert r=={k:F(v) for k,v in rec['exact_ratios'].items()}
   abc=first(r);checked=[]
   for j,row in enumerate(rec['states']):
    assert row['n']==8*2**j and F(row['beta'])==2*beta*2**j and list(map(F,row['raw']))==abc
    can=canonical(abc);u=max(1-x for x in can);v=window(abc);assert can==list(map(F,row['canonical'])) and u==F(row['common_defect']) and v==F(row['symmetry_window_purity'])
    if 'finite_window_gap' in row:
     gap=F(row['finite_window_gap']);assert v>F(1,2) and gap>0 and ex(F(row['beta'])*gap)[1]*(1-v)<v
    if 'asymptotic_gap' in row:
     assert kind=='hypothetical' and 0<u<=F(1,500);gap=F(row['asymptotic_gap']);assert gap>0 and ex(F(row['beta'])*gap)[1]*32*u<1
    checked.append(dict(n=row['n'],beta=row['beta'],window_purity=str(v),finite_gap=row.get('finite_window_gap'),asymptotic_gap=row.get('asymptotic_gap')))
    if j<len(rec['states'])-1:abc=advance(abc);assert abc is not None
   if kind=='actual':assert 'asymptotic_gap' not in rec['states'][-1] and (window(abc)<=F(1,2) or advance(abc) is None)
   else:assert 'asymptotic_gap' in rec['states'][-1] and all('finite_window_gap' in z for z in rec['states'][:-1])
   results.append(dict(kind=kind,beta_initial=str(beta),hypothetical_delta=str(delta),fresh_seed_ratios={k:str(v) for k,v in r.items()},states=checked))
 short=load(S/'bilayer_short_bridge_refinement_review/ACCEPTANCE.json')['continuous_positive_bounds'][0];assert list(map(F,short['coupling_interval']))==[F(0),F(3,20)] and g<=F(3,20)
 actual=next(x for x in results if x['kind']=='actual' and x['beta_initial']=='47/5');combined=min(F(short['gap_lower']),*(F(z['finite_gap']) for z in actual['states'] if z['finite_gap']));assert combined==F(20227124817,10**12)
 conditional=[]
 for x in results:
  if x['kind']=='hypothetical':
   gaps=[F(z['finite_gap']) for z in x['states'][:-1]]+[F(x['states'][-1]['asymptotic_gap']),F(short['gap_lower'])]
   conditional.append(dict(beta_initial=x['beta_initial'],required_ground32_improvement=x['hypothetical_delta'],conditional_only=True,unproved_ground_target=str(lowers[1]+F(x['hypothetical_delta'])),conditional_all_size_gap=str(min(gaps)),terminal_L=x['states'][-1]['n']))
 out=dict(conditional_targets=conditional,status='PASS_ACTUAL_G011_FINITE_WINDOWS_AND_CONDITIONAL_TARGET_REPLAY',g='11/100',actual_combined_L2_through32_gap=str(combined),unique_ground_actual_L2_through32=True,actual_all_size_claim=False,numerator_and_auxiliary_split_Rayleigh_checks=upper_proof,odd_band_fresh_checks=P.ns['ODD_REPORTS'],results=results,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
