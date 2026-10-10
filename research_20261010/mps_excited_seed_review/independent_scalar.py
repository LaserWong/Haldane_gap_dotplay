#!/usr/bin/env python3
"""Independent decimal-grid exact enclosures and scalar half-line covering."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,time,os,resource
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
P=Path(__file__).resolve().parent;t0=time.process_time();D=10**50

def floor(x):return F(x.numerator*D//x.denominator,D)
def ceil(x):return F(-(-x.numerator*D//x.denominator),D)
def exp_interval(x):
 x=F(x)
 if x<0:
  a,b=exp_interval(-x);return floor(1/b),ceil(1/a)
 k=0
 while x>F(1,2):x/=2;k+=1
 xl,xu=floor(x),ceil(x);tl=tu=lo=hi=F(1)
 for j in range(1,81):
  tl=floor(tl*xl/j);tu=ceil(tu*xu/j);lo+=tl;hi+=tu
 hi=ceil(hi+tu*xu/81/(1-xu/82));lo=floor(lo)
 for _ in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
 assert 0<lo<=hi
 return lo,hi

def G(x):
 assert 0<x<=1
 return ceil((x*x+2*x-1)/(2*x*x))
def root(x):
 r=F(isqrt(x.numerator*D*D//x.denominator)+1,D);assert r*r>x;return r

def canonical(a,b):
 s=ceil(a*root(b));t=ceil(a*a*b);joint=t
 for step in range(1,101):
  if min(s,t)>=F(99,100):return {'excluded':False,'reason':'optimistic target entrance','step':step}
  s=G(max(s*s*t,joint))
  if s<=0:return {'excluded':True,'reason':'spatial update','step':step,'negative_upper':str(s)}
  t=G(max(t,joint)**2*s);joint=F(0)
  if t<=0:return {'excluded':True,'reason':'thermal update','step':step,'negative_upper':str(t)}
 return {'excluded':False,'reason':'100-step safety stop'}

def test(j,c):
 a=G(j)
 if a<=0:return {'excluded':True,'reason':'initial first G','negative_upper':str(a)}
 b=G(c*c*a)
 if b<=0:return {'excluded':True,'reason':'initial second G','negative_upper':str(b)}
 history=[]
 for delay in range(100):
  if min(a,b)>=F(99,100):return {'excluded':False,'reason':'time-first target entrance','conversions':history}
  v=canonical(a,b);history.append({'delay':delay,**v})
  if not v['excluded']:return {'excluded':False,'reason':'canonical optimistic orbit survives','conversions':history}
  a=G(a*a*b)
  if a<=0:return {'excluded':True,'reason':'time-first first G','negative_upper':str(a),'conversions':history}
  b=G(b*b*a)
  if b<=0:return {'excluded':True,'reason':'time-first second G','negative_upper':str(b),'conversions':history}
 return {'excluded':False,'reason':'100-delay safety stop','conversions':history}

def values(name):return {k:int(v) for k,v in [s.split('=') for s in (P/name).read_text().splitlines()]}
p=values('independent_contractions.out');g=values('independent_ground.out')
producer={r['n']:r for r in json.loads((P/'inputs/scalar_results.json').read_text())['rows']}
rows=[]
for n in [14,16,20,24]:
 alpha=F(p[f'H0_{n}'],p[f'N0_{n}']);excited=F(p[f'H1_{n}'],p[f'N1_{n}']);R=F(g[f'H0_{2*n}'],g[f'N0_{2*n}']);delta=R-2*alpha;gap=excited-alpha
 assert R<0 and delta>0 and gap>0
 pr=producer[n];assert F(pr['delta_lower'])<=delta and F(pr['trial_energy_difference_upper'])>=gap and F(pr['R_lower'])<=R
 hot=ceil(exp_interval(-R)[1]/3**(4*n));cold=int(pr['cold_closed_interval'][0]);coldbound=exp_interval(-2*cold*delta)[1]
 assert max(hot,coldbound)<F(2,5) and G(F(2,5))<0
 boxes=[];unresolved=[]
 for i in range(2,4*cold):
  lo,hi=F(i,4),F(i+1,4);num=exp_interval(-2*lo*delta)[1]
  j=ceil(num/(1+2*exp_interval(-hi*gap)[0])**4)
  c=ceil(num/(1+2*exp_interval(-2*hi*gap)[0])**2)
  result=test(j,c)
  if not result['excluded']:unresolved.append((str(lo),str(hi)))
  # A producer exclusion must be independently demonstrated.
  pb=pr['warm_boxes'][i-2]
  assert pb['beta_lower']==str(lo) and pb['beta_upper']==str(hi)
  assert j<=F(pb['J_upper']) and c<=F(pb['C_upper'])
  if pb['replay']['outcome']=='excluded':assert result['excluded']
  boxes.append({'lo':str(lo),'hi':str(hi),'J_upper':str(j),'C_upper':str(c),**result})
 if n<24:assert not unresolved
 rows.append({'n':n,'alpha0':str(alpha),'alpha1':str(excited),'R':str(R),'delta':str(delta),'gap':str(gap),'hot_upper':str(hot),'cold_start':cold,'cold_upper':str(coldbound),'max_J_upper':str(max([hot,coldbound]+[F(b['J_upper']) for b in boxes])),'unresolved_boxes':unresolved,'boxes':boxes,'verdict':'PASS all-beta fixed-recipe exclusion' if not unresolved else 'Only bounded screen; no feasibility claim'})
 print(n,rows[-1]['verdict'],len(unresolved),flush=True)
result={'status':'PASS independently verified all producer exclusions','rows':rows,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_scalar.json').write_text(json.dumps(result,indent=2)+'\n')
