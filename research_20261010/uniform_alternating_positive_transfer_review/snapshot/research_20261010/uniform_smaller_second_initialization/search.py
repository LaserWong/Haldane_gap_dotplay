import os,resource,time,json,sys
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent;OLD=P.parent/'uniform_second_moment_optimization';C=json.loads((OLD/'certificate.json').read_text());out={};start=time.process_time()
for sector in ['J','N']:
 a=-float(F(C['filters'][sector+'-']['cap']));b=float(F(C['filters'][sector+'+']['cap']));x=np.linspace(a,b,3001);A=x[:,None]**np.arange(9)
 ints=[[F(v) for v in row] for row in C['moment_intervals'][sector]];mid=np.array([float((l+u)/2) for l,u in ints]);err=np.array([float((u-l)/2) for l,u in ints])
 for k in list(range(16,37,2))+[64,68]:
  cost=np.r_[mid,err];Ab=np.c_[-A,np.zeros_like(A)];sg1=np.c_[np.eye(9),-np.eye(9)];sg2=np.c_[-np.eye(9),-np.eye(9)]
  res=linprog(cost,A_ub=np.r_[Ab,sg1,sg2],b_ub=np.r_[-x**(k-4),np.zeros(18)],bounds=[(None,None)]*9+[(0,None)]*9,method='highs',options={'threads':1});assert res.success
  out[f'{sector}{k}']={'coeff':res.x[:9].tolist(),'lp_bound':res.fun}
  print(sector,k,res.fun,flush=True)
(P/'long_candidates.json').write_text(json.dumps(out,indent=2));print('CPU',time.process_time()-start)
