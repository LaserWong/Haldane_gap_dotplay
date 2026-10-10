import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from explore import M,P,F
import numpy as np,json
from scipy.optimize import linprog
C=json.loads((P/'certificate.json').read_text());out={}
for sector in ['J','N']:
 a=-float(F(C['filters'][sector+'-']['cap']));b=float(F(C['filters'][sector+'+']['cap']));x=np.linspace(a,b,5001);A=x[:,None]**np.arange(9)
 mid=np.array([float((l+u)/2) for l,u in M[sector]]);err=np.array([float((u-l)/2) for l,u in M[sector]])
 for k in [24,36,48,72,120]:
  cost=np.r_[mid,err];Ab=np.c_[-A,np.zeros_like(A)];sg1=np.c_[np.eye(9),-np.eye(9)];sg2=np.c_[-np.eye(9),-np.eye(9)]
  res=linprog(cost,A_ub=np.r_[Ab,sg1,sg2],b_ub=np.r_[-x**(k-4),np.zeros(18)],bounds=[(None,None)]*9+[(0,None)]*9,method='highs')
  print(sector,k,res.success,res.fun,flush=True)
  out[f'{sector}{k}']={'coeff':res.x[:9].tolist(),'lp_bound':res.fun,'a':a,'b':b}
(P/'long_candidates.json').write_text(json.dumps(out,indent=2))
