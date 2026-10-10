"""Independent rational audit; imports no producer code. CPU8, <=1GiB."""
import os,resource,json,hashlib,math,random,time,copy
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
os.sched_setaffinity(0,{8});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
HERE=Path(__file__).resolve().parent; ROOT=HERE/'snapshot'; PROD=ROOT/'integer_window_refinement'; SCALE=1<<176

def floor(x):return Q(x.numerator*SCALE//x.denominator,SCALE)
def ceil(x):return -floor(-x)
@lru_cache(None)
def exp(x):
 if x<0:
  l,h=exp(-x);return floor(1/h),ceil(1/l)
 k=0
 while x>Q(1,2):x/=2;k+=1
 term=total=Q(1)
 for j in range(1,101):term=term*x/j;total+=term
 nxt=term*x/101
 lo=floor(total);hi=ceil(total+nxt/(1-x/102))
 for i in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
 return lo,hi

def rootpow(x,m=1,n=2):
 assert x>=0 and m>=1 and n>=1
 z=x**m;v=z.numerator*SCALE**n//z.denominator
 if n==2:k=math.isqrt(v)
 else:
  low=0;high=1<<((v.bit_length()+n-1)//n)
  while high-low>1:
   mid=(low+high)//2
   if mid**n<=v:low=mid
   else:high=mid
  k=high if high**n<=v else low
 return Q(k,SCALE),Q(k+1,SCALE)
def G(x):
 assert 0<x<=1
 return floor(1-(1-x)**2/(2*x*x))
def direct(a,b,M,n):
 assert 0<a<=1 and Q(1,2)<b<=1 and n>=2 and n%2==0 and n<=M<=2*n
 w=(1+rootpow(2*b-1)[0])/2
 f=rootpow(w,M,n)[0]
 if M%2:f-=rootpow(1-w,M,n)[1]
 assert f>=0
 return floor(rootpow(a,M,n)[0]*f)
def uniform(a,b):
 assert 0<a<=1 and Q(1,2)<b<=1
 return floor(a*a*rootpow(2*b-1)[0])
def old(s,t,k):
 z=max(s*s*t,k)
 assert Q(1,2)<z<=1
 w=(1+rootpow(2*z-1)[0])/2;r=(1-w)/w;d=t/(1+r*r)
 return floor((1-r)*min(s*rootpow(d)[0],d))
def heat(s,b):
 band=s['expanded_band'];rho=Q(s['exact_rayleigh']);alpha=Q(band['alpha']);B=Q(band['B'])
 terms=[(1,rho-Q(s['ground_lower']))]
 terms.extend((r['multiplicity'],rho+8-Q(r['lower'])) for r in band['comparison_endpoints'][1:])
 terms.extend((m,rho+8-alpha*e+B) for e,m in band['complete_reference_bins'] if e>=band['omitted_reference_excitation'])
 assert sum(m for m,e in terms)==6561
 return ceil(sum(m*exp(b*e)[1] for m,e in terms))
def initial(rec,beta):
 delta=Q(rec['large']['exact_rayleigh'])-2*Q(rec['small']['exact_rayleigh'])
 e=exp(-2*beta*delta)[0];j=floor(e/heat(rec['small'],beta)**4);c=floor(e/heat(rec['small'],2*beta)**2)
 return j,c,G(j),G(floor(c*c*G(j)))
def gapcheck(p,beta,d):
 assert Q(1,2)<p<1 and beta>0 and d>0
 assert exp(beta*d)[1]<p/(1-p)
def pathcheck(saved,rec):
 assert saved['g']==rec['g'] and saved['canonical_steps']==0
 beta=Q(saved['beta']);d=Q(saved['gap_lower']);j,c,a,b=initial(rec,beta)
 lc=rec['small']['relative_form_bound']['local_certificate'];short=[1-2*Q(lc['a'])-m*Q(lc['b']) for m in (2,3)]
 assert min(short)>d and list(map(Q,saved['short_M2_M3']))==short
 bound=max(uniform(rootpow(j)[0],c),old(rootpow(j)[0],j,j))
 n=4;be=beta; windows=saved['windows'];assert len(windows)==saved['time_steps']+1
 for idx,row in enumerate(windows):
  assert row['n']==n and Q(row['beta'])==be
  if idx:
   assert 0<a<=1 and Q(1,2)<b<=1
   p=floor(a*a*b);bound=max(uniform(a,b),old(rootpow(p)[0],p,p))
   assert Q(row['a'])<=a and Q(row['b'])<=b
  assert Q(row['purity_lower'])<=bound
  gapcheck(Q(row['purity_lower']),be,d)
  if idx:a=G(p);b=G(floor(b*b*a))
  n*=2;be*=2
 p=floor(a*a*b);u=max(1-rootpow(p)[0],1-p)
 assert n==saved['asymptotic_onset'] and be==Q(saved['asymptotic_beta'])
 assert 0<u<=Q(saved['u'])<=Q(1,100)
 assert exp(be*d)[1]<1/(5*Q(saved['u']))
 return dict(g=rec['g'],gap=str(d),onset=n,windows=len(windows),status='PASS')
def toys():
 rng=random.Random(57231);checks=0;signed=0
 for i in range(600):
  # Arbitrary finite real spectra with a positive, unique modulus leader.
  X=[Q(20)]+[Q(rng.randint(-16,16)) for _ in range(rng.randint(1,7))]
  Y=[Q(10)]+[Q(rng.randint(-6,6)) for _ in range(rng.randint(1,7))]
  for n in (2,4,8):
   zx=lambda m:sum(v**m for v in X);zy=lambda m:sum(v**m for v in Y)
   a=zy(n)/zx(n)**2;b=zy(2*n)/zy(n)**2
   if not(Q(1,2)<b<=1):continue
   for m in range(n,2*n+1):
    if zx(m)<=0 or zy(m)<=0:continue
    target=zy(m)/zx(m)**2
    assert direct(a,b,m,n)<=target and uniform(a,b)<=target
    checks+=1;signed+=any(v<0 for v in Y)
 # Negative dominant eigenvalue satisfies even purity but invalidates odd conclusion.
 y=[Q(-10),Q(1)];assert sum(v**3 for v in y)<0
 return dict(checks=checks,signed_checks=signed,negative_dominant_counterexample='[-10,1] has negative odd traces')
def main():
 start=time.monotonic();saved=json.loads((PROD/'replay_paths.json').read_text());recs=json.loads((ROOT/'chain_frontier_above_02/expanded_inputs.json').read_text());by={r['g']:r for r in recs}
 paths=[pathcheck(p,by[p['g']]) for p in saved['results']]
 r25=json.loads((ROOT/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];s25=json.loads((PROD/'replay.json').read_text());beta=Q(s25['initial_beta']);j,c,a,b=initial(r25,beta);p=floor(a*a*b)
 assert Q(s25['a'])<=a and Q(s25['b'])<=b and Q(s25['P'])<=p and Q(s25['window_beta'])==2*beta
 for row in s25['rows']:
  m=row['M'];bound=direct(a,b,m,8)
  if m==8:bound=max(bound,a)
  if m==16:bound=max(bound,p)
  assert Q(row['purity_lower'])<=bound;gapcheck(Q(row['purity_lower']),2*beta,Q(row['gap_lower']))
 assert len(s25['rows'])==9 and {r['M'] for r in s25['rows']}==set(range(8,17))
 assert Q(s25['uniform_window_lower'])<=uniform(a,b)
 initial_bound=uniform(rootpow(j)[0],c)
 assert Q(s25['initial_M4_M8_lower'])<=initial_bound
 gapcheck(Q(s25['initial_M4_M8_lower']),beta,Q(1,100))
 lc=r25['small']['relative_form_bound']['local_certificate']
 short=[1-2*Q(lc['a'])-m*Q(lc['b']) for m in (2,3)]
 assert min(short)>Q(1,100) and list(map(Q,s25['short_M2_M3']))==short
 ap=G(p);arg=floor(b*b*ap);bp=G(arg);assert bp<0
 bad=[]
 for label,mutate in [('oversized_gap',lambda p:p.update(gap_lower='1')),('wrong_temperature',lambda p:p['windows'][1].update(beta='1')),('wrong_base',lambda p:p['windows'][1].update(n=16)),('missing_window',lambda p:p['windows'].pop(1)),('optimistic_endpoint',lambda p:p['windows'][1].update(purity_lower='999999/1000000')),('wrong_onset',lambda p:p.update(asymptotic_onset=64)),('bad_terminal_u',lambda p:p.update(u='1/1000000000000000000000000000000000000000000000000000000000000000'))]:
  q=copy.deepcopy(saved['results'][0]);mutate(q)
  try:pathcheck(q,by[q['g']])
  except AssertionError:bad.append(label)
  else:raise AssertionError('corruption accepted '+label)
 for label,args in [('odd_base',(Q(3,4),Q(3,4),4,3)),('b_half',(Q(3,4),Q(1,2),3,2)),('b_above_one',(Q(3,4),Q(11,10),3,2)),('a_above_one',(Q(11,10),Q(3,4),3,2)),('outside_window',(Q(3,4),Q(3,4),5,2))]:
  try:direct(*args)
  except AssertionError:bad.append(label)
  else:raise AssertionError('invalid domain accepted '+label)
 out=dict(status='PASS_INDEPENDENT_LEMMA_AND_COMPLETE_PATHS',paths=paths,g025=dict(status='FINITE_M2_THROUGH_M16_ONLY',gap='1/100',beta=str(2*beta),next_argument=float(arg),next_b=float(bp)),toy_tests=toys(),adversarial_rejections=bad,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
