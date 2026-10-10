"""Exact combined old-span / two-image four-dimensional Rayleigh input."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import json,math,resource,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600));HERE=Path(__file__).resolve().parent;start=time.process_time()
W=[3,2,2,2,1,2,6,2,1]
def read(name,skip=0):
 out={}
 with (HERE/name).open() as f:
  for _ in range(skip):next(f)
  for line in f:
   k,v=map(int,line.split())
   if v:out[k]=v
 return out
def wt(k):return math.prod(W[(k>>(4*i))&15] for i in range(8))
psi=read('packed_input.txt',82);u=read('packed_old_direction.txt',82);phi=read('full_image.txt');chi=read('old_direction_image.txt');phi2=read('second_image.txt');weights={k:wt(k) for k in phi2}
def dot(a,b):
 if len(a)>len(b):a,b=b,a
 return sum(x*b[k]*(weights[k] if k in weights else wt(k)) for k,x in a.items() if k in b)
vs=[psi,u,phi,phi2];n=4;den=144;G=[[F(dot(a,b)) for b in vs] for a in vs];H=[[F(0)]*n for _ in range(n)]
for i,im in enumerate([phi,chi,phi2]):
 for j,v in enumerate(vs):H[i][j]=F(dot(im,v),den)
for i in range(3):H[3][i]=H[i][3]
m2=json.loads((HERE/'second.json').read_text());H[3][3]=F(int(m2['moment3_scaled']),den)
assert H==list(map(list,zip(*H)))
rec=json.loads((HERE.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(rec['large']['exact_rayleigh']);assert H[0][0]/G[0][0]==rho
# Exact Gram LDL provides a well-scaled rational orthogonal trial basis.
def ldl(M):
 d=[];L=[[F(i==j) for j in range(n)] for i in range(n)]
 for i in range(n):
  p=M[i][i]-sum(L[i][k]**2*d[k] for k in range(i));d.append(p)
  if p==0:return L,d
  for j in range(i+1,n):L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*d[k] for k in range(i)))/p
 return L,d
L,D=ldl(G);assert len(D)==n and min(D)>0
Li=[[F(0)]*n for _ in range(n)]
for j in range(n):
 for i in range(n):Li[i][j]=F(i==j)-sum(L[i][k]*Li[k][j] for k in range(i))
B=list(map(list,zip(*Li)));K=[[H[i][j]-rho*G[i][j] for j in range(n)] for i in range(n)]
KK=[[sum(B[i][a]*K[i][j]*B[j][b] for i in range(n) for j in range(n)) for b in range(n)] for a in range(n)];sc=np.sqrt([float(x) for x in D]);nf=np.array(KK,dtype=float)/np.outer(sc,sc);assert np.max(np.abs(nf-nf.T))<1e-12
es,v=eigh(nf);alpha=v[:,0]/sc;alpha/=max(abs(alpha));aa=[F(float(x)) for x in alpha];c=[sum(B[i][j]*aa[j] for j in range(n)) for i in range(n)]
bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));norm=bil(G);assert norm>0;new=bil(H)/norm;target=2*F(rec['small']['exact_rayleigh'])+F(19,1250);_,piv=ldl([[H[i][j]-target*G[i][j] for j in range(n)] for i in range(n)]);excluded=len(piv)==n and min(piv)>0
out=dict(status='EXACT_RAYLEIGH_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g='1/4',trial_dimension=4,trial_files=['packed_input.txt:psi','packed_old_direction.txt:u','full_image.txt:den*Hpsi','second_image.txt:den^2*H^2psi'],auxiliary_action_file='old_direction_image.txt:den*Hu',Gram=[[str(x) for x in r] for r in G],H=[[str(x) for x in r] for r in H],Gram_LDL_pivots=list(map(str,D)),coefficients=list(map(str,c)),exact_rayleigh=str(new),improvement=str(rho-new),improvement_display=float(rho-new),new_delta=str(new-2*F(rec['small']['exact_rayleigh'])),new_delta_display=float(new-2*F(rec['small']['exact_rayleigh'])),necessary_target_rayleigh=str(target),meets_necessary_target=new<target,span_exclusion=excluded,span_target_LDL_pivots=list(map(str,piv)),cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,contract='Four-dimensional numerator-only span containing both original saved trial directions and two Hamiltonian images of their best combination. No filtered residual or full physical spectral information is used.')
(HERE/'rayleigh_four.json').write_text(json.dumps(out,indent=2));print('FOUR GAIN',float(rho-new),'delta',out['new_delta_display'],'targetmet',new<target,'spanexcluded',excluded,'cpu',out['cpu_seconds'],'rss',out['peak_rss_kib'],flush=True)
