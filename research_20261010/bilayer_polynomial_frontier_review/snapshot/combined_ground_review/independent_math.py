"""Fresh scalar implementation for the combined-endpoint review.
Only standard-library integer/rational operations; no producer/reviewer imports.
"""
import os,sys,resource,math
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
D=2**512

def down(x,d=D):x=F(x);return F(x.numerator*d//x.denominator,d)
def up(x,d=D):return -down(-F(x),d)

def sqrtlo(x):
 x=F(x);assert x>=0;d=10**40
 a=math.isqrt(x.numerator*d*d//x.denominator)
 assert F(a*a,d*d)<=x<F((a+1)**2,d*d)
 return F(a,d)

@lru_cache(maxsize=10000)
def exponential(x):
 x=F(x);y=abs(x);k=0
 while y>F(1,8):y/=2;k+=1
 # Directed rational term recurrence, 100 terms, geometric tail.
 lo=hi=tlo=thi=F(1)
 for j in range(1,101):
  tlo=down(tlo*y/j);thi=up(thi*y/j);lo+=tlo;hi+=thi
 hi+=up(thi*y/101/(1-y/102))
 for _ in range(k):lo=down(lo*lo);hi=up(hi*hi)
 return (lo,hi) if x>=0 else (down(1/hi),up(1/lo))

def trace(r,beta,ground_only=False):
 """Direct shifted physical trace Z'=Tr exp(-beta H'), no Rayleigh normalization.
 Ground-only changes LOWER numerator alone; full upper count is preserved.
 """
 lo=hi=F(0)
 for i,b in enumerate(r['blocks']):
  assert b['k']==len(b['eigen_lower'])==len(b['eigen_upper'])
  for l,u in zip(b['eigen_lower'],b['eigen_upper']):
   if not ground_only or i==0:lo+=b['multiplicity']*exponential(-beta*F(u))[0]
   hi+=b['multiplicity']*exponential(-beta*F(l))[1]
 tail=sum(z['multiplicity']*exponential(-beta*F(z['lower']))[1] for z in r['number_sector_bins']['bins'][2:])
 return lo,hi+tail

def ratios(recs,beta,order,ground_only=False):
 assert not ground_only or order=='txy'
 q0=trace(recs[0],beta);q3=trace(recs[2],2*beta,ground_only)
 i1,t1=(0,2*beta) if order[0]=='t' else (1,beta)
 i2,t2=(2,beta) if order[-1]=='t' else (1,2*beta)
 q1=trace(recs[i1],t1);q2=trace(recs[i2],t2)
 return [down(q3[0]/q0[1]**8,10**16),down(q3[0]**2/q1[1]**8,10**16),down(q3[0]/q2[1]**2,10**16)]

def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)

def first_steps(js):
 j1,j2,c0=js;v=[]
 for i in range(3):
  p=j1 if i==0 else j2*v[0] if i==1 else c0**4*v[0]**2*v[1]
  v.append(down(G(p),10**16))
  if v[-1]<=0:break
 return v

def move(v,order):
 a,b,c=v
 z=v if order=='xyt' else [a,b*sqrtlo(c),b*b*c] if order=='xty' else [a*sqrtlo(b),a*a*b*sqrtlo(c),a**4*b*b*c]
 return [down(x,10**18) for x in z]

def cycle(defects):
 d=list(defects)
 for i in range(3):
  p=(1-d[0])**4*(1-d[1])**2*(1-d[2]);assert 0<p<=1
  x=up((1-p)**2/(2*p*p),10**18)
  if x>=1:return None
  d=d[1:]+[x]
 return d

def interpolate1(s,t):
 assert 0<s<=1 and 0<t<=1;p=s*s*t;assert p>F(1,2)
 w=(1+sqrtlo(2*p-1))/2;r=(1-w)/w;d=t/(1+r*r)
 a=down((1-r)*min(s*sqrtlo(d),d),10**40)
 assert 0<a and a/(1-r)<=d and (a/(s*(1-r)))**2<=d
 return a,dict(p=str(p),dominant_weight_lower=str(w),tail_ratio_upper=str(r),d_lower=str(d),purity_lower=str(a))

def interpolate2(abc):
 a,b,c=abc;assert b>F(1,2)
 s=a*a*sqrtlo(2*b-1);t,y=interpolate1(b,c);ans,x=interpolate1(s,t)
 return ans,dict(spatial_lower=str(s),transverse_thermal_lower=str(t),y=y,x=x)

def edges(nx,ny):
 out=Counter()
 for x in range(nx):
  for y in range(ny):
   i=x*ny+y
   for j in [((x+1)%nx)*ny+y,x*ny+(y+1)%ny]:out[tuple(sorted([i,j]))]+=1
 return out
