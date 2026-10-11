import os,resource,time,json
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));st=time.process_time()
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent
C=json.loads((P.parent/'uniform_second_moment_optimization/certificate.json').read_text())
M={s:[[F(x) for x in row] for row in vals] for s,vals in C['moment_intervals'].items()}
import json,math,numpy as np
from scipy.optimize import minimize_scalar
L=json.loads((P/'long_candidates.json').read_text());out={}
def bernstein(poly,a,b):
 n=len(poly)-1
 power=[sum(poly[j]*math.comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,n+1)) for k in range(n+1)]
 return [sum(power[k]*F(math.comb(i,k),math.comb(n,k)) for k in range(i+1)) for i in range(n+1)]
def nonnegative(B,depth=0):
 if min(B)>=0:return 1,depth
 assert depth<30
 left=[B[0]];right=[B[-1]]
 while len(B)>1:
  B=[(a+b)/2 for a,b in zip(B[:-1],B[1:])];left.append(B[0]);right.append(B[-1])
 n1,d1=nonnegative(left,depth+1);n2,d2=nonnegative(right[::-1],depth+1);return n1+n2,max(d1,d2)
for key,v in L.items():
 s=key[0];k=int(key[1:]);a=-F(C['filters'][s+'-']['cap']);b=F(C['filters'][s+'+']['cap']);q=[F(round(x*10**14),10**14) for x in v['coeff']]
 f=lambda x:sum(float(z)*x**j for j,z in enumerate(q))-x**(k-4)
 grid=np.linspace(float(a),float(b),10001);vals=np.array([f(x) for x in grid]);mins=[vals[0],vals[-1]]
 for j in range(1,len(grid)-1):
  if vals[j]<vals[j-1] and vals[j]<vals[j+1]:mins.append(minimize_scalar(f,bounds=(grid[j-1],grid[j+1]),method='bounded',options={'xatol':1e-15}).fun)
 delta=F(math.ceil(max(0,-min(mins))*10**14)+1000,10**14);q[0]+=delta
 poly=q+[F(0)]*(k-4+1-len(q));poly[-1]-=1
 count,depth=nonnegative(bernstein(poly,a,b))
 bound=sum(c*(u if c>=0 else l) for c,(l,u) in zip(q,M[s]))
 out[key]={'coeff':list(map(str,q)),'bound':str(bound),'decimal':float(bound),'added_constant':str(delta),'bernstein_leaf_count':count,'bernstein_max_depth':depth}
 print(key,float(bound),count,depth,flush=True)
(P/'long_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS CPU',time.process_time()-st)
