"""Exact rational Collatz lower bounds for open spin-2 Heisenberg clusters.
Only eigsh proposes positive dyadic vectors. Certificate uses exact integer H2*v
and componentwise inequalities, independent of eigensolver accuracy/completeness.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='2';os.environ['OMP_NUM_THREADS']='2'
from pathlib import Path
from fractions import Fraction as F
import json,time,math,argparse
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
from threadpoolctl import threadpool_limits
threadpool_limits(2)
ROOT=Path(__file__).resolve().parent

def matrix(n,m):
 ids=np.arange(5**n,dtype=np.int32);z=ids.copy();tot=np.zeros(len(ids),np.int16)
 for _ in range(n):tot+=z%5-2;z//=5
 ids=ids[tot==m];d=len(ids);pw=5**np.arange(n,dtype=np.int64)
 dig=(ids[:,None]//pw)%5;w=dig-2
 diag=np.sum(w[:,:-1]*w[:,1:],axis=1)
 lookup=np.full(5**n,-1,dtype=np.int32);lookup[ids]=np.arange(d)
 rr=[np.arange(d)];cc=[np.arange(d)];asym2=[2*diag];sym=[diag.astype(float)]
 for j in range(n-1):
  l=j+1
  for ds in [-1,1]:
   good=(dig[:,j]+ds>=0)&(dig[:,j]+ds<=4)&(dig[:,l]-ds>=0)&(dig[:,l]-ds<=4)
   col=np.flatnonzero(good);r=dig[good,j];s=dig[good,l]
   row=lookup[ids[good]+ds*pw[j]-ds*pw[l]]
   aa=(4-r)*s if ds==1 else r*(4-s)
   bb=(r+1)*(5-s) if ds==1 else (5-r)*(s+1)
   rr.append(row);cc.append(col);asym2.append(-aa);sym.append(-np.sqrt(aa*bb)/2)
 ri=np.concatenate(rr);ci=np.concatenate(cc)
 A2=sp.csr_matrix((np.concatenate(asym2).astype(np.int64),(ri,ci)),shape=(d,d))
 B=sp.csr_matrix((np.concatenate(sym),(ri,ci)),shape=(d,d))
 D=np.sqrt(np.prod(np.array([1,4,6,4,1],dtype=np.int64)[dig],axis=1).astype(float))
 return A2,B,D

def certify(n,m):
 path=ROOT/f'open{n}_m{m}.json'
 if path.exists():return json.loads(path.read_text())
 t0=time.time();A2,B,D=matrix(n,m);d=B.shape[0]
 if d<=3:
  ev,V=eigh(B.toarray());e=ev[0];v=V[:,0]
 else:
  ev,V=eigsh(B,k=1,which='SA',tol=2e-13,v0=np.ones(d),maxiter=20000);e=ev[0];v=V[:,0]
 # Sign and exact positivity are checked after dyadic quantization.
 v=v*np.sign(v.sum())*D;v=v/v.max();v=np.maximum(v,np.finfo(float).tiny)
 # Nonnegative power smoothing repairs relative inaccuracies in tiny components.
 # This stage proposes vectors only; all accepted inequalities remain exact.
 P=sp.eye(d,format='csr')*(8*(n-1)+1)-A2
 assert np.min(P.data,initial=0)>=0
 for _ in range(500):
  v=P@v;v/=v.max()
 assert v.min()>0,(n,m,v.min())
 # float.as_integer_ratio keeps the proposal exact, then a common 80-bit scale.
 scale=2**80
 q=[]
 for x in v:
  a,b=float(x).as_integer_ratio();q.append((a*scale+b//2)//b)
 assert min(q)>0
 lo=None;hi=None
 for i in range(d):
  s=sum(int(A2.data[p])*q[int(A2.indices[p])] for p in range(A2.indptr[i],A2.indptr[i+1]))
  ratio=F(s,2*q[i]);lo=ratio if lo is None or ratio<lo else lo;hi=ratio if hi is None or ratio>hi else hi
 # round certificates outward to 1e-9 grid for short input
 unit=10**9;lb=F(lo.numerator*unit//lo.denominator,unit);ub=F(-((-hi.numerator*unit)//hi.denominator),unit)
 # Store vector as decimal integer list. A2 regenerates with exact integer rules.
 vpath=ROOT/f'open{n}_m{m}_vector.json';vpath.write_text(json.dumps(q,separators=(',',':')))
 obj={'n':n,'m':m,'dimension':d,'lower':str(lb),'upper':str(ub),'lower_display':float(lb),'upper_display':float(ub),'ritz_display':float(e),'min_vector_component':min(q),'max_vector_component':max(q),'vector_file':vpath.name,'seconds':time.time()-t0,'method':'Exact integer Collatz inequalities for irreducible stoquastic rational matrix similar to Hermitian H.'}
 path.write_text(json.dumps(obj,indent=2));print(json.dumps(obj),flush=True);return obj

def envelope(n,cluster_records,m):
 # H_n - h M >= n/(l-1) min_j [E_l(j)-h(l-1)j/l].
 l=cluster_records[0]['n'];pts=[(j,F(x['lower'])) for j,x in enumerate(cluster_records)]
 fields={F(0)}
 for j,e in pts:
  for k,f in pts:
   if j<k:
    h=(f-e)*l/F((l-1)*(k-j));
    if h>=0:fields.add(h)
 best=None;besth=None
 for h in fields:
  Emin=min(e-h*F(l-1,l)*j for j,e in pts)
  bound=h*m+F(n,l-1)*Emin
  if best is None or bound>best:best=bound;besth=h
 return best,besth

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--lengths',nargs='+',type=int,default=[4,6,8]);args=p.parse_args()
 allrec={}
 for l in args.lengths:allrec[l]=[certify(l,m) for m in range(2*l+1)]
 out={'method':'Overlapping open-cluster field lower bounds; valid for arbitrary z seam twist and n>=l.', 'clusters':args.lengths,'n10_sector_lower_bounds':{}}
 for m in range(21):
  cand=[(envelope(10,r,m),l) for l,r in allrec.items()];((bound,h),l)=max(cand,key=lambda x:x[0][0]);out['n10_sector_lower_bounds'][str(m)]={'lower':str(bound),'lower_display':float(bound),'cluster_length':l,'field':str(h)}
 (ROOT/'cluster_envelopes.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
