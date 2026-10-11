"""Cached exact scalar replay only. No physical contractions or eigensolvers."""
import os,resource,json,math,hashlib,time,copy
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(100,100));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
HERE=Path(__file__).resolve().parent;RES=HERE/'snapshot';start=time.process_time();D=10**60;GRID=1<<384
load=lambda p:json.loads(p.read_text())
for name,h in load(HERE/'INPUT_SHA256.json').items():assert hashlib.sha256((RES/name).read_bytes()).hexdigest()==h,name
for name,h in load(HERE/'DEPENDENCY_SHA256.json').items():assert hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()==h,name
def down(x,d=D):return F(x.numerator*d//x.denominator,d)
def up(x,d=D):return -down(-x,d)
@lru_cache(None)
def exp(x):
 x=F(x);y=abs(x);k=0
 while y>F(1,8):y/=2;k+=1
 term=total=F(1)
 for j in range(1,91):term*=y/j;total+=term
 lo=down(total,GRID);hi=up(total+(term*y/91)/(1-y/92),GRID)
 for _ in range(k):lo=down(lo*lo,GRID);hi=up(hi*hi,GRID)
 return (lo,hi) if x>=0 else (down(1/hi,GRID),up(1/lo,GRID))
def sqrtlo(x):
 k=math.isqrt(x.numerator*D*D//x.denominator);r=F(k,D);assert r*r<=x<(r+F(1,D))**2;return r

def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
def raw(r,exact=True):
 rnd=down if exact else lambda x:x
 a=rnd(G(r['J1']))
 if a<=0:return None
 b=rnd(G(r['J2']*a))
 if b<=0:return None
 c=rnd(G(r['C0']**4*a*a*b));return [a,b,c] if c>0 else None

def advance(abc,exact=True):
 a,b,c=abc;rnd=down if exact else lambda x:x
 aa=rnd(G(a**4*b*b*c))
 if aa<=0:return None
 bb=rnd(G(aa*c*c))
 if bb<=0:return None
 cc=rnd(G(aa*aa*bb*c**4));return [aa,bb,cc] if cc>0 else None

def window(abc,exact=True):
 a,b,c=abc;rnd=down if exact else lambda x:x;sqrt=sqrtlo if exact else math.sqrt
 if min(b,c)<=F(1,2):return F(0)
 s=rnd(b*b*sqrt(2*c-1))
 return rnd(a**4*(2*b-1)*sqrt(2*s-1)) if s>F(1,2) else F(0)
def canonical(abc,exact=True):
 a,b,c=abc;rnd=down if exact else lambda x:x;sqrt=sqrtlo if exact else math.sqrt
 return [rnd(a*sqrt(b)),rnd(a*a*b*sqrt(c)),rnd(a**4*b*b*c)]

def float_path(r,beta):
 abc=raw(r,False)
 if abc is None:return False
 for j in range(16):
  u=max(1-x for x in canonical(abc,False))
  if 0<u<=.002:return True
  if window(abc,False)<=.5:return False
  abc=advance(abc,False)
  if abc is None:return False
 return False

src=load(RES/'bilayer_split_pencil_scalar/result.json')['results'][0];assert F(src['g'])==F(11,100)
d=next(x['data'] for x in load(RES/'bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100));g=F(11,100)
ph=src['physical'];splits=load(RES/'bilayer_split_basis_plan/reoptimization.json')['results'];upper64=F(next(x for x in splits if x['shape']==[8,8] and F(x['g'])==g)['split']['rayleigh'])
coeff=list(map(F,d['largest_base_trial']['rayleigh_coefficients']));old64=sum(v*g**i for i,v in enumerate(coeff));gain=old64-upper64
for p,physical in zip(d['denominator_patches'],ph):
 assert p['N']==physical['N']
 for m in p['odd_band']['modes']:m['eigen_lower_minus_ground_rayleigh_uniform_lower']=str(max(F(physical['odd_floor']),F(m['eigen_lower_minus_ground_rayleigh_uniform_lower'])))

def ratios(beta,delta=F(0),exact=True):
 exup=(lambda z:exp(z)[1]) if exact else (lambda z:math.exp(float(z)))
 exlo=(lambda z:exp(z)[0]) if exact else (lambda z:math.exp(float(z)))
 components=[]
 for ix,timefactor in [(0,1),(0,2),(1,2)]:
  p=d['denominator_patches'][ix];physical=ph[ix];b=beta*timefactor;N=p['N']
  width=F(physical['trace_pivot'])-F(physical['ground_lower'])-(delta if ix else 0)
  gr=exup(b*width);odd=sum(3*exup(-b*F(m['eigen_lower_minus_ground_rayleigh_uniform_lower'])) for m in p['odd_band']['modes'])
  tail=sum(math.comb(3*N+q-1,q)*exup(-b*F(en)) for q,en in enumerate(p['reference_minus_rayleigh_uniform_lowers'],1) if q>=2)
  components.append(dict(ground=gr,odd=odd,tail=tail,total=gr+odd+tail))
 e={k:F(v['uniform_lower'])+mult*gain for (k,v),mult in zip(d['correlated_energy_combinations'].items(),[2 if k!='J2' else 4 for k in d['correlated_energy_combinations']])}
 r={k:exlo(beta*e[k])/components[i]['total']**power for k,i,power in [('J1',0,8),('J2',1,8),('C0',2,2)]}
 if exact:r={k:down(v) for k,v in r.items()}
 return r,components

def gap_witness(p,beta):
 proposal=F(math.floor(math.log(float(p/(1-p)))/float(beta)*10**12)-1,10**12)
 while exp(beta*proposal)[1]*(1-p)>=p:proposal-=F(1,10**12)
 return proposal

def exact_path(beta,delta=F(0),allsize=False):
 r,comp=ratios(beta,delta);abc=raw(r);assert abc is not None;states=[]
 for j in range(16):
  can=canonical(abc);u=max(1-x for x in can);bb=2*beta*2**j;v=window(abc)
  row=dict(cycle=j,n=8*2**j,beta=str(bb),raw=list(map(str,abc)),canonical=list(map(str,can)),common_defect=str(u),symmetry_window_purity=str(v))
  if v>F(1,2):row['finite_window_gap']=str(gap_witness(v,bb))
  if 0<u<=F(1,500):
   prop=F(math.floor(math.log(float(1/(32*u)))/float(bb)*10**12)-1,10**12)
   while exp(bb*prop)[1]*32*u>=1:prop-=F(1,10**12)
   row['asymptotic_gap']=str(prop);states.append(row);break
  states.append(row)
  if v<=F(1,2):break
  abc=advance(abc)
  if abc is None:break
 if allsize:assert 'asymptotic_gap' in states[-1]
 return dict(beta_initial=str(beta),ground32_improvement_hypothetical=str(delta),exact_ratios={k:str(v) for k,v in r.items()},states=states,small_sizes_inherited_separately=True)

out=[]
for beta in [F(47,5),F(10)]:
 rf,_=ratios(beta,exact=False);saved=next(x for x in src['tests'] if F(x['beta'])==beta)
 assert max(abs(rf[k]-saved['ratios'][k]) for k in rf)<1e-13
 actual=exact_path(beta)
 width=F(ph[1]['ground_uncertainty']);lo=0.;hi=float(width)
 assert float_path(ratios(beta,F(hi),False)[0],float(beta))
 for _ in range(55):
  mid=(lo+hi)/2
  if float_path(ratios(beta,F(mid),False)[0],float(beta)):hi=mid
  else:lo=mid
 delta=F(math.ceil(hi*10**7)+1,10**7);assert delta<width
 hypothetical=exact_path(beta,delta,True)
 hypothetical.update(hypothetical_only=True,target_ground32_lower=str(F(ph[1]['ground_lower'])+delta),current_ground32_lower=ph[1]['ground_lower'],required_improvement=str(delta),float_success_threshold_bracket=[lo,hi])
 out.append(dict(actual=actual,hypothetical=hypothetical));print(beta,'actualwindows',[(s['n'],s.get('finite_window_gap')) for s in actual['states']],'targetdelta',float(delta),'terminal',hypothetical['states'][-1]['n'],flush=True)
result=dict(status='EXACT_SCALAR_ONLY_ACTUAL_FINITE_WINDOWS_AND_HYPOTHETICAL_ALL_SIZE_TARGETS',g='11/100',results=out,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,no_new_physical_contractions=True,no_actual_all_size_certificate=True)
(HERE/'exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
