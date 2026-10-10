import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import json,math,resource
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import eigh
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600))
HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'full.json').read_text());m2=json.loads((HERE/'second.json').read_text());rec=json.loads((HERE.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0]
N=F(m['norm']);den=m['integer_denominator'];assert m2['norm']==m['moment2_scaled'] and m2['moment1_scaled']==m['moment3_scaled'] and m2['integer_denominator']==den
mom=[F(1)]+[F(m[f'moment{k}_scaled'])/(den**k*N) for k in range(1,4)]+[F(m2['moment2_scaled'])/(den**4*N),F(m2['moment3_scaled'])/(den**5*N)]
rho=mom[1];assert rho==F(rec['large']['exact_rayleigh']);cm=[sum(F(math.comb(k,j))*(-rho)**(k-j)*mom[j] for j in range(k+1)) for k in range(6)]
G=[[cm[i+j] for j in range(3)] for i in range(3)];K=[[cm[i+j+1] for j in range(3)] for i in range(3)];scale=np.sqrt([float(G[i][i]) for i in range(3)]);gf=np.array(G,dtype=float)/np.outer(scale,scale);kf=np.array(K,dtype=float)/np.outer(scale,scale);ev,v=eigh(kf,gf);x=v[:,0]/scale;x/=x[0];c=[int(round(y*10**12)) for y in x]
bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(3) for j in range(3));norm=bil(G);assert norm>0;new=rho+bil(K)/norm;target=2*F(rec['small']['exact_rayleigh'])+F(19,1250)
A=[[K[i][j]+(rho-target)*G[i][j] for j in range(3)] for i in range(3)];piv=[]
for k in range(3):
 p=A[k][k];piv.append(p)
 if not p:break
 for i in range(k+1,3):
  for j in range(k+1,3):A[i][j]-=A[i][k]*A[k][j]/p
excluded=len(piv)==3 and min(piv)>0
out=dict(status='EXACT_RAYLEIGH_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g='1/4',trial_dimension=3,max_image_support=m2['image_support'],full_dimension=43046721,base_rayleigh=str(rho),moments=list(map(str,mom)),centered_moments=list(map(str,cm)),Gram=[[str(x) for x in row] for row in G],centered_H=[[str(x) for x in row] for row in K],coefficients=list(map(str,c)),trial_formula='sum_i c_i*(H-rho)^i psi, i=0,1,2. Both full H images are saved; no full H^3 output or residual is used.',exact_rayleigh=str(new),improvement=str(rho-new),improvement_display=float(rho-new),new_delta=str(new-2*F(rec['small']['exact_rayleigh'])),new_delta_display=float(new-2*F(rec['small']['exact_rayleigh'])),necessary_target_rayleigh=str(target),meets_necessary_target=new<target,span_exclusion=excluded,span_target_LDL_pivots=list(map(str,piv)))
(HERE/'rayleigh_three.json').write_text(json.dumps(out,indent=2));print('THREE GAIN',float(rho-new),'delta',out['new_delta_display'],'targetmet',new<target,'spanexcluded',excluded,flush=True)
