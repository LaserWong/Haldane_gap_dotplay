import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import resource
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
import json,math,time,ast,itertools
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import numpy as np
from scipy.linalg import eigh
p=Path(__file__).resolve().parent;r=p.parent;s=r/'third_moment_review';start=time.time();ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools)
names={'mat','zero','graph','rebuild'};nodes=[x for x in ast.parse((s/'audit_matrices.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name in names];exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_rebuild','exec'),ns)
def mat(x):return np.array([[F(t) for t in row] for row in x],dtype=object)
def bil(c,M):return F(np.array(c,dtype=object)@M@np.array(c,dtype=object))
def ref(N,g,q):
 x=1-4*g;den=10**60;root=F(math.isqrt(x.numerator*den*den//x.denominator),den);assert root*root<=x<(root+F(1,den))**2;C=F(3*N,8);return C*(2*g-1)+(C+q)*root
energy=json.loads((r/'bilayer_split_basis_plan/reoptimization.json').read_text())['results'];out=[]
for shape,source in [((8,4),'bilayer_complete_split_H2_8x4')]:
 tag='%dx%d'%shape;geo=json.loads((s/'results'/f'geometry_{tag}.json').read_text());data=json.loads((r/source/f'complete_H2_polynomial_{tag}.json').read_text());Jcs=list(map(mat,data['H2_coefficients']));G=mat(data['gram']);scale=1/np.sqrt(np.array(G.diagonal(),dtype=float));ss=np.outer(scale,scale);GF=np.array(G,dtype=float)*ss
 for g in (F(11,100),F(3,25)):
  K=sum(g**i*mat(M) for i,M in enumerate(data['H_coefficients']));J=sum(g**i*M for i,M in enumerate(Jcs));N=math.prod(shape);a=ref(N,g,2);r1=ref(N,g,1);prev=next(t for t in energy if tuple(t['shape'])==shape and F(t['g'])==g)['split'];c0=prev['integer_coefficients'];norm0=bil(c0,G);rho0=bil(c0,K)/norm0;var0=bil(c0,J)/norm0-rho0*rho0;lower0=rho0-var0/(a-rho0)
  HF=np.array(K,dtype=float)*ss;JF=np.array(J,dtype=float)*ss;af=float(a)
  def eig(ell):return eigh(JF-(af+ell)*HF+af*ell*GF,GF,subset_by_index=[0,0])
  lo=float(lower0)-.001;hi=float(rho0);assert eig(lo)[0][0]<0 and eig(hi)[0][0]>=0
  for _ in range(45):
   mid=(lo+hi)/2
   if eig(mid)[0][0]<0:lo=mid
   else:hi=mid
  ell=F(math.floor(lo*10**10)-1,10**10);v=eig(float(ell))[1][:,0]*scale;v/=v[0];c=[int(round(x*2**48)) for x in v];norm=bil(c,G);rho=bil(c,K)/norm;var=bil(c,J)/norm-rho*rho;witness=bil(c,J-(a+ell)*K+a*ell*G)/norm
  assert var>=0 and rho<r1 and ell<a and witness<0
  lower=rho-var/(a-rho);assert lower>ell
  rec=dict(shape=shape,g=str(g),dimension=len(c),cutoff=str(a),global_r1=str(r1),integer_coefficients=c,norm=str(norm),rayleigh=str(rho),variance=str(var),strict_pencil_endpoint=str(ell),normalized_pencil_witness=str(witness),Temple_lower=str(lower),Temple_lower_display=float(lower),energy_optimized_lower=str(lower0),energy_optimized_variance=str(var0),endpoint_improvement=str(lower-lower0),endpoint_improvement_display=float(lower-lower0),float_root_bracket=[lo,hi],scope='Exact rational witness conditional on producer complete matrix; independent review required before physical promotion')
  prior=next(x for x in json.loads((r/'bilayer_residual_pencil_optimization/result.json').read_text())['results'] if x['shape']==list(shape) and F(x['g'])==g);rec['previous43D_pencil_lower']=prior['Temple_lower'];rec['gain_over43D_pencil']=str(lower-F(prior['Temple_lower']));out.append(rec);print(shape,g,'lower',float(lower),'gain',float(lower-lower0),'variance',float(var),flush=True)
  (p/'checkpoint.json').write_text(json.dumps(out,indent=2)+'\n')
(p/'result.json').write_text(json.dumps(dict(status='EXPLORATORY_ENDPOINT_WITNESSES_PENDING_COMPLETE_MATRIX_REVIEW',results=out,seconds=time.time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
