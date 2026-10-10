import os,sys,resource,json,math,hashlib
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;RES=HERE.parent;BAND=RES/'low_band'
sys.path.insert(0,str(BAND/'third_moment_exact'))
from enlarged_numerator import build
sys.path.insert(0,str(RES/'symmetry'))
from symmetric_ground import independent_indices
out=[]
for shape in ['4x4','8x4']:
 gp=BAND/'frontier_g007_g010/g1d10'/f'block1_{shape}_g1d10.json';geompath=BAND/'third_moment_exact'/f'geometry_{shape}_origin.json';pp=BAND/'combined_ground_bounds/combined'/f'patch_{shape}_g1d10.json'
 gr,geom,p=[json.loads(q.read_text()) for q in [gp,geompath,pp]]
 G,K,_=build(gr,geom);ids=independent_indices(G.tolist());G=G[np.ix_(ids,ids)];A=K[np.ix_(ids,ids)]*F(1,gr['integer_matrix_denominator'])
 sc=np.sqrt(np.array(np.diag(G),float));vv,vc=eigh(np.array(A,float)/sc[:,None]/sc[None,:],np.array(G,float)/sc[:,None]/sc[None,:]);v=vc[:,0]/sc;v/=max(abs(v));c=np.array([int(round(x*2**56)) for x in v],dtype=object)
 norm=F(c@G@c);rho=F(c@A@c)/norm;a=F(p['global_lambda_kplus1_lower']);old=F(p['blocks'][0]['eigen_lower'][0]);up=F(p['blocks'][0]['eigen_upper'][0]);target=old+F(3,4)*(up-old)
 # This is ONLY a budget for an as-yet uncomputed full residual of this
 # rational enlarged state. Nothing here asserts that the budget is met.
 budget=(rho-target)*(a-rho)
 r=dict(shape=shape,rank=len(ids),selected_basis_indices=ids,coefficients=list(map(int,c)),norm=str(norm),rayleigh=str(rho),rayleigh_display=float(rho),cutoff=str(a),conditional_target_ground_lower=str(target),conditional_target_ground_lower_display=float(target),residual_squared_budget=str(budget),residual_squared_budget_display=float(budget),residual_budget_interpretation='If the complete exact variance v of THIS rational vector satisfies v < budget, Temple proves ground > target. Variance is not computed or assumed.',old_ground_lower=str(old),old_upper=str(up),available_endpoint_headroom=float(rho-old),ideal_zero_variance_gain=float(rho-old),source_sha256={str(q.relative_to(RES)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [gp,geompath,pp]})
 out.append(r);print(shape,float(rho),'target',float(target),'allowed var',float(budget),flush=True)
(HERE/'residual_budgets.json').write_text(json.dumps(out,indent=2)+'\n')
