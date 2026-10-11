import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import resource,ast,json,time,hashlib,itertools,math
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import numpy as np
from scipy.linalg import eigh
p=Path(__file__).resolve().parent;s=p.parent/'third_moment_review';start=time.time()
ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools)
a=ast.parse((s/'audit_matrices.py').read_text());names={'mat','zero','graph','rebuild'};nodes=[x for x in a.body if isinstance(x,ast.FunctionDef) and x.name in names];exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_rebuild','exec'),ns)
def bil(c,A):return sum(F(c[i])*F(A[i,j])*c[j] for i in range(len(c)) for j in range(len(c)))
def optimize(G,H):
 scale=1/np.sqrt(np.array(G.diagonal(),dtype=float));ss=np.outer(scale,scale)
 val,vec=eigh(np.array(H,dtype=float)*ss,np.array(G,dtype=float)*ss,subset_by_index=[0,0]);v=vec[:,0]*scale;v/=v[0];c=[int(round(x*2**48)) for x in v];norm=bil(c,G);rho=bil(c,H)/norm
 return dict(integer_coefficients=c,norm=str(norm),rayleigh=str(rho),rayleigh_display=float(rho),float_ritz_proposal=float(val[0]),dimension=len(c))
out=[]
for shape in ((4,4),(8,4),(8,8)):
 geo=json.loads((s/'results'/('geometry_%dx%d.json'%shape)).read_text());n=geo['orbits'];b=n+1;D=4*n+1;z=ns['rebuild'](*shape,F(0),geo);o=ns['rebuild'](*shape,F(1),geo)
 G=np.zeros((D,D),dtype=object);A=G.copy();G[:b,:b]=z['G'][:b,:b];A[:b,:b]=2*(o['A']-z['A'])[:b,:b]
 for i in range(n):
  for j in range(n):
   f,ss,v,w,x,y,zz=[F(geo[k][i][j]) for k in ('F','S','V','W','X','Y','Z')];li,ri,mi=b+i,b+n+i,b+2*n+i;lj,rj,mj=b+j,b+n+j,b+2*n+j
   G[li,lj]=f;G[li,rj]=G[rj,li]=ss;G[ri,rj]=v;G[mi,mj]=w
   A[1+i,lj]=A[lj,1+i]=f;A[1+i,rj]=A[rj,1+i]=ss;A[li,lj]=ss;A[li,rj]=A[rj,li]=v;A[li,mj]=A[mj,li]=w;A[ri,rj]=x;A[ri,mj]=A[mj,ri]=y;A[mi,mj]=zz
 assert np.array_equal(A,A.T) and np.array_equal(G,G.T)
 q=[0]+[2]*n+[4]*(2*n)+[6]*n;Q=np.array([[G[i,j]*q[j] for j in range(D)] for i in range(D)],dtype=object)
 for g in (F(11,100),F(3,25)):
  H=Q+g*A/2;old=ns['rebuild'](*shape,g,geo);new=optimize(G,H);prev=optimize(old['G'],old['A']);c=new['integer_coefficients'];new['rayleigh_coefficients']=[str(bil(c,Q)/F(new['norm'])),str(bil(c,A)/(2*F(new['norm'])))];assert sum(F(x)*g**i for i,x in enumerate(new['rayleigh_coefficients']))==F(new['rayleigh'])
  out.append(dict(shape=shape,g=str(g),split=new,old=prev,exact_gain=str(F(prev['rayleigh'])-F(new['rayleigh'])),gain_display=float(F(prev['rayleigh'])-F(new['rayleigh']))))
  print(shape,g,'gain',out[-1]['gain_display'],'rho',new['rayleigh_display'],flush=True)
(p/'reoptimization.json').write_text(json.dumps(dict(status='EXACT_RATIONAL_RAYLEIGH_UPPERS_ONLY_NO_RESIDUALS',results=out,seconds=time.time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
