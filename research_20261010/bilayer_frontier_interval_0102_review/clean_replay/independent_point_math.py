"""Fresh independent scalar/geometry/signed-spectrum audit. No producer imports."""
import os,resource,json,math,time,hashlib,random,copy,itertools
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
os.sched_setaffinity(0,{4})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(600,600))
HERE=Path(__file__).resolve().parent;S=HERE/'snapshot';D=1<<544
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def down(x):return F(x.numerator*D//x.denominator,D)
def up(x):return -down(-x)
def root(x):
 assert x>=0
 k=math.isqrt(x.numerator*D*D//x.denominator)
 return F(k,D)
@lru_cache(None)
def exp(x):
 if x<0:
  l,h=exp(-x);return down(1/h),up(1/l)
 k=0
 while x>F(1,2):x/=2;k+=1
 lo=hi=tl=th=F(1)
 for j in range(1,151):
  tl=down(tl*x/j);th=up(th*x/j);lo+=tl;hi+=th
 lo=down(lo);hi=up(hi+(th*x/151)/(1-x/152))
 for _ in range(k):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi

def trace(rec,beta):
 v=F(0);count=0
 for block in rec['blocks']:
  assert block['k']==len(block['eigen_lower'])==len(block['eigen_upper'])
  v+=block['multiplicity']*sum(exp(-beta*F(x))[1] for x in block['eigen_lower']);count+=block['multiplicity']*block['k']
 assert count==rec['retained_full_band_dimension']
 for b in rec['number_sector_bins']['bins'][2:]:v+=b['multiplicity']*exp(-beta*F(b['lower']))[1];count+=b['multiplicity']
 assert count>=rec['full_hilbert_dimension']
 return up(v)
def G(x):
 assert 0<x<=1
 return down(1-(1-x)**2/(2*x*x))
def full(v):return v[0]**4*v[1]**2*v[2]
def valid(v):assert len(v)==3 and all(0<x<=1 for x in v)
def convert(v):
 valid(v);a,b,c=v
 return [down(a*root(b)),down(a*a*b*root(c)),down(full(v))]
def advance(v):
 valid(v);v=v[:]
 for _ in range(3):v=v[1:]+[G(full(v))];valid(v)
 return v
def advance_canonical(v,k):
 a,b,c=v;d=G(max(full(v),k));e=G(max(b**4*c*c,k*k)*d);f=G(max(c,k)**4*d*d*e)
 ans=[d,e,f];valid(ans);return ans

def direct(a,b,c,n=2,m=2):
 valid([a,b,c]);assert n>=2 and m>=2 and n%2==m%2==0 and c>F(1,2)
 d=down(b*root(c));s=down(b*b*root(2*c-1));assert min(d,s)>F(1,2)
 return down(a**4*(2*d-1)*root(2*s-1)),d,s

def gapcheck(p,beta,g):
 assert F(1,2)<p<1 and beta>0 and g>0
 assert exp(beta*g)[1]*(1-p)<p

def initial(recs,beta):
 u=F(recs[2]['blocks'][0]['eigen_upper'][0]);num=exp(-2*beta*u)[0]
 q0=trace(recs[0],beta);q1=trace(recs[0],2*beta);q2=trace(recs[1],2*beta)
 js=[down(num/q0**8),down(num*num/q1**8),down(num/q2**2)]
 a=G(js[0]);b=G(js[1]*a);c=G(js[2]**4*a*a*b)
 return [a,b,c],js

def shortcheck(r):
 assert F(r['g_max'])==F(1,10) and r['sides']==list(range(2,8))
 sums=[]
 for n in range(2,8):
  edges=Counter()
  for x in range(n):
   for y in range(n):
    for z,w in [((x+1)%n,y),(x,(y+1)%n)]:edges[tuple(sorted((x*n+y,z*n+w)))]+=1
  sums.append(sum(v*v for v in edges.values()))
 assert sums==r['weighted_edge_square_sums']==[16,18,32,50,72,98]
 alpha,delta,v=map(F,[r['alpha_lower'],r['delta_lower'],r['vacuum_creation_norm_squared_upper']])
 assert alpha==F(4,5) and 0<delta*delta<=F(3,5) and v==F(147,200)
 g=delta-v/(alpha+delta);assert g==F(r['gap_lower']);return g

def labels(n,tau,order):
 base=[n,n,tau];out=[]
 for axis in order:
  old=base[:];base['xyt'.index(axis)]*=2
  out.append(dict(axis=axis,base=[old[0],old[1],str(old[2])],endpoint=[base[0],base[1],str(base[2])]))
 return out

def pathcheck(p,recs,short):
 assert F(p['coupling'])==F(1,10)
 beta=F(p['beta_initial']);raw,js=initial(recs,beta);can=convert(raw);joint=full(raw)
 assert all(0<F(p['initial'][k])<=z for k,z in zip(('J1','J2','C0'),js))
 assert all(0<F(x)<=y for x,y in zip(p['initial']['permuted_prefix'],raw))
 assert len(p['states'])==p['terminal_cycle']+1
 final=F(p['all_integer_gap']);assert 0<final<=short==F(p['short_L2_through_L7'])
 rows=[];saved_gaps=[]
 for i,row in enumerate(p['states']):
  n=8*2**i;tau=2*beta*2**i
  assert row['n']==n and F(row['beta'])==tau
  assert row['physical_base']==[n,n,str(tau)]
  assert row['raw_edge_labels']==labels(n,tau,'txy') and row['canonical_edge_labels']==labels(n,tau,'xyt')
  can=list(map(max,can,convert(raw)));joint=max(joint,full(can),full(raw));u=max(1-x for x in can)
  assert all(0<F(x)<=y for x,y in zip(row['raw'],raw))
  assert all(0<F(x)<=y for x,y in zip(row['canonical'],can))
  assert 0<F(row['joint'])<=joint and u<=F(row['defect'])
  if i==p['terminal_cycle']:
   su=F(row['defect']);assert 0<u<=su<=F(1,500)
   g=F(row['asymptotic_gap']);assert g>=final
   assert exp(tau*g)[1]*32*su<1
   saved_gaps.append(g);rows.append(dict(n=n,beta=str(tau),type='asymptotic',gap=str(g)))
  else:
   assert row['window']==[n,2*n]
   # Check saved endpoints against their own saved raw data, not only tighter independent states.
   bound,d,s=direct(*map(F,row['raw']),n,n)
   assert F(row['thermal_lower'])<=bound
   assert F(row['detail']['transverse_spatial_lower'])<=d and F(row['detail']['interpolated_spatial_lower'])<=s
   g=F(row['gap']);assert g>=final
   gapcheck(F(row['thermal_lower']),tau,g)
   saved_gaps.append(g);rows.append(dict(n=n,through=2*n,beta=str(tau),type='integer_window',gap=str(g),purity=str(row['thermal_lower'])))
   can=advance_canonical(can,joint);raw=advance(raw);joint=full(can)
 assert final==min([short]+saved_gaps)
 return dict(beta_initial=str(beta),terminal_cycle=p['terminal_cycle'],gap=str(final),gap_display=float(final),onset=p['states'][-1]['n'],windows=rows)

def ledger():
 checks=0
 for n,m in ((2,4),(4,4),(8,6)):
  for order in itertools.permutations('xyt'):
   base=[n,m,F(7,3)];start=tuple(base);poly=Counter()
   for j,axis in enumerate(order):
    old=tuple(base);base['xyt'.index(axis)]*=2;new=tuple(base);poly[new]+=2**(2-j);poly[old]-=2**(3-j)
   assert {k:v for k,v in poly.items() if v}=={tuple(base):1,start:-8};checks+=1
 return checks

def toys():
 rng=random.Random(812093);checks=odd_both=signed=0
 # Separable lattice partition functions have exact self-adjoint tensor transfers
 # in both directions. Positive leaders and signed subleaders test the odd case.
 for trial in range(120):
  rx,ry=[F(rng.choice((-1,1))*rng.randint(1,3),20) for _ in range(2)]
  sx,sy=rx/2,ry/2
  z=lambda L,W,r,s:(1+r**L)**W*(1+s**W)**L
  for n,m in ((2,2),(2,4),(4,2),(4,4)):
   a=z(n,m,sx,sy)/z(n,m,rx,ry)**2;b=z(2*n,m,sx,sy)/z(n,m,sx,sy)**2;c=z(2*n,2*m,sx,sy)/z(2*n,m,sx,sy)**2
   bound,_,_=direct(a,b,c,n,m)
   for L in range(n,2*n+1):
    for W in range(m,2*m+1):
     actual=z(L,W,sx,sy)/z(L,W,rx,ry)**2
     assert bound<=actual
     checks+=1;odd_both+=L%2==W%2==1;signed+=rx<0 or ry<0
 return dict(exact_rectangle_checks=checks,both_odd_checks=odd_both,signed_subleader_checks=signed,negative_leader_counterexample='[-10,1] has positive even traces but negative odd traces; excluded by all-integer physical positivity')

def main():
 start=time.monotonic()
 for rel,h in load(HERE/'INPUT_SHA256.json').items():assert sha(S/rel)==h
 physical_manifest=load(S/'PHYSICAL_REVIEW_MANIFEST.json');physical_manifest=physical_manifest.get('files',physical_manifest)
 for shape in ('4x4','8x4','8x8'):assert sha(S/f'input_{shape}.json')==physical_manifest[f'snapshot_scalar/scalar/input_{shape}.json']
 assert load(S/'PHYSICAL_REVIEW_STATUS.json')['status']=='PASS'
 recs=[load(S/f'input_{shape}.json') for shape in ('4x4','8x4','8x8')]
 short=shortcheck(load(S/'short_sizes.json'));p=load(S/'replay.json')['results'];results=[pathcheck(x,recs,short) for x in p]
 candidate=load(S/'candidate.json');assert candidate in p and candidate['all_integer_gap']==max(p,key=lambda x:F(x['all_integer_gap']))['all_integer_gap']
 bad=[]
 for label,mutate in [('wrong_beta',lambda x:x['states'][1].update(beta='1')),('wrong_labels',lambda x:x['states'][0]['raw_edge_labels'][1]['base'].__setitem__(2,'1')),('wrong_base',lambda x:x['states'][1].update(n=12)),('missing_window',lambda x:x['states'].pop(1)),('oversized_gap',lambda x:x.update(all_integer_gap='1')),('optimistic_window',lambda x:x['states'][0].update(thermal_lower='1')),('bad_terminal_defect',lambda x:x['states'][-1].update(defect='1/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))]:
  r=copy.deepcopy(p[0]);mutate(r)
  try:pathcheck(r,recs,short)
  except AssertionError:bad.append(label)
  else:raise AssertionError('corruption accepted '+label)
 for label,args in [('odd_x',(F(9,10),F(9,10),F(9,10),3,4)),('odd_y',(F(9,10),F(9,10),F(9,10),4,3)),('c_half',(F(9,10),F(9,10),F(1,2))),('outer_gate',(F(9,10),F(3,4),F(3,4))),('a_above_one',(F(11,10),F(9,10),F(9,10)))]:
  try:direct(*args)
  except AssertionError:bad.append(label)
  else:raise AssertionError('invalid domain accepted '+label)
 out=dict(status='PASS_INDEPENDENT_2D_DIRECT_WINDOW_AND_ALL_INTEGER_PATHS',results=results,geometry_identity_checks=ledger(),toy_tests=toys(),adversarial_rejections=bad,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
