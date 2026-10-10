"""Independent integer/rational arithmetic, without imports from producer code."""
import os,resource,sys
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
sys.dont_write_bytecode=True
import math,json,hashlib
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
from collections import Counter
GRID=1<<384

def floor(x,grid=GRID):x=F(x);return F(x.numerator*grid//x.denominator,grid)
def ceil(x,grid=GRID):return -floor(-F(x),grid)
def ceildiv(a,b):return -(-a//b)

@lru_cache(maxsize=8192)
def exp_bounds(x):
 # Directed integer Taylor recurrence at |x|/2^k <= 1/16.
 # Unlike the producer, each term is rounded with exact integer arithmetic.
 x=F(x);y=abs(x);k=0
 while y>F(1,16):y/=2;k+=1
 yl=y.numerator*GRID//y.denominator;yu=ceildiv(y.numerator*GRID,y.denominator)
 tl=tu=sl=su=GRID
 for j in range(1,81):
  tl=tl*yl//(GRID*j);tu=ceildiv(tu*yu,GRID*j);sl+=tl;su+=tu
 # After degree 80, ratio of successive omitted terms is <= y/82.
 su+=ceildiv(tu*yu*82,81*(82*GRID-yu))
 for _ in range(k):sl=sl*sl//GRID;su=ceildiv(su*su,GRID)
 if x<0:sl,su=GRID*GRID//su,ceildiv(GRID*GRID,sl)
 return F(sl,GRID),F(su,GRID)

def log_lower(x):
 x=F(x);assert x>1;k=0
 while x>=2:x/=2;k+=1
 def atom(t):
  z=(t-1)/(t+1);return 2*sum((z**(2*j+1)/F(2*j+1) for j in range(100)),F(0))
 return k*atom(F(2))+atom(x)

def sqrt_lower(x):
 x=F(x);D=10**40;assert x>=0
 n=math.isqrt(x.numerator*D*D//x.denominator);z=F(n,D)
 assert z*z<=x<(z+F(1,D))**2;return z

def qa(x,y):return x[0]+y[0],x[1]+y[1]
def qs(x,y):return x[0]-y[0],x[1]-y[1]
def qm(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def qd(x,y):
 d=y[0]**2-2*y[1]**2;assert d;return qm(x,(y[0]/d,-y[1]/d))
def qsign(x):
 a,b=x
 if not a:return (b>0)-(b<0)
 if not b:return (a>0)-(a<0)
 if (a>0)==(b>0):return 1 if a>0 else -1
 z=(a*a>2*b*b)-(a*a<2*b*b);return z if a>0 else -z

def qload(x):return tuple(map(F,x))
def graph(nx,ny):
 ed=Counter()
 for x in range(nx):
  for y in range(ny):
   i=x*ny+y
   for j in [((x+1)%nx)*ny+y,x*ny+(y+1)%ny]:ed[tuple(sorted((i,j)))]+=1
 return ed

def occupied_bounds(nx,ny):
 n=nx*ny;out=[]
 for q in range(n+1):
  h=min(q,n-q);root=math.isqrt(4*h);root+=root*root<4*h
  z=2*q-min(root,nx,ny)
  if nx>=4 and ny>=4 and nx%2==ny%2==0:
   c=n-q;z=min(z,2*q,q*q//4,4*q-2*n+min(2*c,c*c//4))
  out.append(z)
 return out,[2*n-4*q+z for q,z in enumerate(out)]

def trace(rec,beta):
 shift=F(rec['blocks'][0]['eigen_upper'][0]);lo=hi=F(0)
 for block in rec['blocks']:
  assert len(block['eigen_lower'])==len(block['eigen_upper'])==block['k']
  for l,u in zip(block['eigen_lower'],block['eigen_upper']):
   lo+=block['multiplicity']*exp_bounds(-beta*(F(u)-shift))[0]
   hi+=block['multiplicity']*exp_bounds(-beta*(F(l)-shift))[1]
 # The saved shell multiplicities are deliberately left separate by variant.
 tail=sum(row['multiplicity']*exp_bounds(-beta*(F(row['lower'])-shift))[1] for row in rec['number_sector_bins']['bins'][2:])
 return lo,hi+tail,tail

def G(x):
 assert 0<x<=1;return 1-(1-x)**2/(2*x*x)

def interpolate_1d(S,T):
 assert 0<S<=1 and 0<T<=1
 p=S*S*T;assert p>F(1,2)
 w=(1+sqrt_lower(2*p-1))/2;r=(1-w)/w;d=T/(1+r*r)
 ans=floor((1-r)*min(S*sqrt_lower(d),d),10**40)
 assert F(1,2)<w<=1 and (2*w-1)**2<=2*p-1
 assert ans>0 and ans/(1-r)<=d and (ans/((1-r)*S))**2<=d
 return ans,dict(p=str(p),dominant_weight_lower=str(w),tail_ratio_upper=str(r),d_lower=str(d),purity_lower=str(ans))

def interpolate_2d(A,B,C):
 assert all(0<z<=1 for z in (A,B,C)) and B>F(1,2)
 S=A*A*sqrt_lower(2*B-1);T,y=interpolate_1d(B,C);z,x=interpolate_1d(S,T)
 return z,dict(spatial_lower=str(S),transverse_thermal_lower=str(T),y=y,x=x)
