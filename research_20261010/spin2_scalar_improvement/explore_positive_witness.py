import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np,json
from scipy.optimize import linprog,least_squares
from pathlib import Path
P=Path(__file__).resolve().parent
rs=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())
out=[]
for row in rs[1:2]:
 for sec in ['J','N']:
  target=np.array([row['moments'][sec][str(k)] for k in range(4,11)])
  fixed=np.array([1.03] if sec=='J' else [1.02])
  ks=np.arange(4,11)
  want=target-(fixed[:,None]**ks).sum(axis=0)
  nodes=np.r_[np.linspace(-.95,-.02,200),np.linspace(.02,.95,200)]
  A=nodes[None,:]**ks[:,None]
  scale=np.maximum(abs(target),1)
  # Use a mild count objective to select positive integer-count prototypes.
  lp=linprog(np.ones(len(nodes)),A_eq=A/scale[:,None],b_eq=want/scale,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9,'threads':1})
  print(row['beta'],sec,'lp',lp.success,flush=True)
  if not lp.success:continue
  ix=np.flatnonzero(lp.x>1e-5)
  x=nodes[ix];n=np.maximum(1,np.round(1.1*lp.x[ix])).astype(int)
  # Split each count over two nearby groups; creates enough free nodes for nonlinear correction.
  xx=[];nn=[]
  for xx0,nn0 in zip(x,n):
   if nn0>1:xx.extend([xx0-.001,xx0+.001]);nn.extend([nn0//2,nn0-nn0//2])
   else:xx.append(xx0);nn.append(nn0)
  x=np.array(xx);n=np.array(nn)
  def fun(x):return ((n[:,None]*x[:,None]**ks).sum(axis=0)-want)/scale
  def jac(x):return (n[:,None]*ks*x[:,None]**(ks-1)).T/scale[:,None]
  opt=least_squares(fun,x,jac=jac,bounds=(-.99,.99),max_nfev=400,ftol=1e-13,gtol=1e-13,xtol=1e-13)
  err=float(max(abs(fun(opt.x)*scale)))
  out.append({'beta':row['beta'],'sector':sec,'counts':[1]+n.tolist(),'nodes':[str(fixed[0])]+[format(x,'.15f') for x in opt.x],'max_numerical_moment_error':err,'nfev':opt.nfev})
  print(row['beta'],sec,'max_abs_error',err,'nfev',opt.nfev,flush=True)
(P/'positive_witnesses.json').write_text(json.dumps(out,indent=2)+'\n')
