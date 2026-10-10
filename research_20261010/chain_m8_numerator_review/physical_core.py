"""Independent counted low-band audit. Exact proof checks, optional floating diagnostic."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[name]='1'
if hasattr(os,'sched_getaffinity'): os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import itertools,json,math,time,resource,hashlib
from fractions import Fraction as F
from collections import Counter,defaultdict
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
HERE=Path(__file__).resolve().parent
# Independently specified integer Clebsch-Gordan columns in |m_left,m_right>, m=-1,0,1.
CG=[[0,0,1,0,-1,0,1,0,0],[0,-1,0,1,0,0,0,0,0],[0,0,-1,0,0,0,1,0,0],[0,0,0,0,0,-1,0,1,0],[1,0,0,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0],[0,0,1,0,2,0,1,0,0],[0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,1]]
W=[sum(x*x for x in v) for v in CG]
EX=[0,1,1,1,3,3,3,3,3]; MAG=[0,-1,0,1,-2,-1,0,1,2]
assert W==[3,2,2,2,1,2,6,2,1]
assert all(sum(x*y for x,y in zip(CG[i],CG[j]))==(W[i] if i==j else 0) for i in range(9) for j in range(9))
def dimer_action(v):
 out=[0]*9
 for c,vv in enumerate(v):
  i,j=divmod(c,3);out[c]+=(i-1)*(j-1)*vv
  if i<2 and j>0:out[c+2]+=vv
  if i>0 and j<2:out[c-2]+=vv
 return out
assert all(dimer_action(v)==[(e-2)*x for x in v] for v,e in zip(CG,EX))
def op(site,kind):
 A=[[0]*9 for _ in range(9)]
 for c in range(9):
  x=list(divmod(c,3));m=x[site]
  if kind=='z':A[c][c]=m-1
  elif kind=='+' and m<2:x[site]+=1;A[3*x[0]+x[1]][c]=1
  elif kind=='-' and m>0:x[site]-=1;A[3*x[0]+x[1]][c]=1
 return [[F(sum(CG[r][i]*A[i][j]*CG[c][j] for i in range(9) for j in range(9)),W[r]) for c in range(9)] for r in range(9)]
O={(s,k):op(s,k) for s in [0,1] for k in ['z','+','-']}
K={}
for c,d in itertools.product(range(9),repeat=2):
 row=[]
 for r,s in itertools.product(range(9),repeat=2):
  z=O[1,'z'][r][c]*O[0,'z'][s][d]+O[1,'+'][r][c]*O[0,'-'][s][d]+O[1,'-'][r][c]*O[0,'+'][s][d]
  if z:row.append((r,s,z))
 K[c,d]=row
# Physical spin-one ladder sqrt(2) factors cancel the conventional 1/2.
def metric(st):return math.prod(W[i] for i in st)
def action(st):
 out=defaultdict(F)
 for j in range(4):
  i=(j-1)%4
  for a,b,v in K[st[i],st[j]]:
   s=list(st);s[i]=a;s[j]=b;out[tuple(s)]+=v
 return {s:v for s,v in out.items() if v}
def psd(A):
 A=[[F(x) for x in r] for r in A];n=len(A);p=[]
 assert all(A[i][j]==A[j][i] for i in range(n) for j in range(n))
 for k in range(n):
  x=A[k][k];assert x>=0,(k,x)
  p.append(x)
  if not x:assert all(A[j][k]==0 for j in range(k+1,n));continue
  for i in range(k+1,n):
   for j in range(i,n):A[i][j]=A[j][i]=A[i][j]-A[i][k]*A[j][k]/x
 return p

