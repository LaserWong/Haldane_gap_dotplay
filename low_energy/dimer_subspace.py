"""Sparse-support dimer-basis Ritz/Temple certificates without a full Hilbert basis.
Exact residual includes ALL states reached outside the retained trial subspace.
Works for homogeneous spin 1/2 and spin 1 with rational local dimer eigenvectors.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']: os.environ[k]='1'
import sys,math,json,time,itertools,resource,argparse
from pathlib import Path
from fractions import Fraction as F
from functools import reduce
from collections import defaultdict
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import sympy as sy
from ground_tail import seed
OUT=Path(__file__).resolve().parent

def dimer_local(s):
 s=F(s);assert s in [F(1,2),F(1)], "Only spin 1/2 and spin 1 have been implemented";d=int(2*s+1)
 sz=sy.diag(*[sy.Rational(i)-sy.Rational(s.numerator,s.denominator) for i in range(d)])
 kp=sy.zeros(d)
 for i in range(d-1): kp[i+1,i]=1
 km=kp.T; ident=sy.eye(d)
 factor=sy.Rational(1,2) if s==F(1,2) else sy.Integer(1)
 h=sy.kronecker_product(sz,sz)+factor*(sy.kronecker_product(kp,km)+sy.kronecker_product(km,kp))
 # For spin1 kp=Splus/sqrt2; for spinhalf kp=Splus.
 cols=[];labels=[]
 for J in range(int(2*s)+1):
  E=F(J*(J+1),2)-s*(s+1)
  for M in range(-J,J+1):
   inds=[i*d+j for i in range(d) for j in range(d) if F(i+j)-2*s==M]
   block=h.extract(inds,inds)-sy.Rational(E.numerator,E.denominator)*sy.eye(len(inds))
   ns=block.nullspace(); assert len(ns)==1
   den=sy.ilcm(*[v.q for v in ns[0]]) if len(ns[0])>1 else ns[0][0].q
   vec=sy.zeros(d*d,1)
   for i,x in zip(inds,ns[0]): vec[i]=x*den
   cols.append(vec); labels.append((J,M,F(J*(J+1),2)))
 P=sy.Matrix.hstack(*cols);G=P.T*P;assert G.is_diagonal()
 weights=[int(G[i,i]) for i in range(d*d)]
 Pinv=G.inv()*P.T
 ops={}
 for a in range(2):
  for name,op in [('z',sz),('p',kp),('m',km)]:
   O=sy.kronecker_product(op,ident) if a==0 else sy.kronecker_product(ident,op)
   ops[a,name]=Pinv*O*P
 kernels={}
 for a in range(2):
  for b in range(2):
   K=sy.kronecker_product(ops[a,'z'],ops[b,'z'])+factor*(sy.kronecker_product(ops[a,'p'],ops[b,'m'])+sy.kronecker_product(ops[a,'m'],ops[b,'p']))
   n=d*d; trans=[]
   for p in range(n):
    for q in range(n):
     trans.append([(i//n,i%n,F(int(K[i,p*n+q].p),int(K[i,p*n+q].q))) for i in range(n*n) if K[i,p*n+q]])
   kernels[a,b]=trans
 return labels,weights,kernels

def bilayer_bonds(nx,ny,gx,gy):
 idx=lambda x,y:(x%nx)*ny+y%ny
 weak=[]
 for x in range(nx):
  for y in range(ny):
   for layer in range(2):
    weak.append((idx(x,y),layer,idx(x+1,y),layer,gx))
    weak.append((idx(x,y),layer,idx(x,y+1),layer,gy))
 return weak

def columnar_bonds(M,W,g,k):
 # Dimer i=(x,y) = [R(x,y),L(x+1,y)] in that order.
 idx=lambda x,y:(x%M)*W+y
 weak=[]
 for x in range(M):
  for y in range(W):
   if g: weak.append((idx(x-1,y),1,idx(x,y),0,g))
  for y in range(W-1):
   for a in range(2):
    if k: weak.append((idx(x,y),a,idx(x,y+1),a,k))
 return weak

def certify_sparse(s,N,weak,max_excited=2,bits=44,tag='sparse',relative_bound=None,support_depth=None,reference_certificate=None):
 t0=time.monotonic();s=F(s)
 labels,localw,kernels=dimer_local(s);dloc=len(labels)
 assert labels[0]==(0,0,F(0))
 basis=[(0,)*N]
 if support_depth is None:
  for nexc in range(1,max_excited+1):
   for sites in itertools.combinations(range(N),nexc):
    for vals in itertools.product(range(1,dloc),repeat=nexc):
     if sum(labels[v][1] for v in vals): continue
     state=[0]*N
     for i,v in zip(sites,vals): state[i]=v
     basis.append(tuple(state))
 else:
  seen=set(basis);frontier=set(basis)
  for depth in range(support_depth):
   nxt=set()
   for st in frontier:
    acc=defaultdict(F)
    for i,aa,j,bb,g in weak:
     for p,q,value in kernels[aa,bb][st[i]*dloc+st[j]]:
      out=list(st);out[i]=p;out[j]=q;acc[tuple(out)]+=g*value
    for out,value in acc.items():
     if value and out not in seen:nxt.add(out)
   seen.update(nxt);frontier=nxt
  basis=[(0,)*N]+sorted(seen-{(0,)*N})
 lookup={x:i for i,x in enumerate(basis)}
 w=lambda st:math.prod(localw[x] for x in st)
 weights=[w(st) for st in basis]
 E00=-N*s*(s+1)
 vmin=sum((-g*s*(s+1) if g>=0 else g*s*s) for _,_,_,_,g in weak)
 vmax=sum((g*s*s if g>=0 else -g*s*(s+1)) for _,_,_,_,g in weak)
 a=E00+1+vmin if relative_bound is None else E00+F(relative_bound['second_shift_lower'])
 if reference_certificate is not None:a=E00+F(reference_certificate['second_shift_lower'])
 # One exact common denominator for every local transition and diagonal.
 coeffs=[g*c for _,aa,_,bb,g in weak for row in kernels[aa,bb] for _,_,c in row]
 den=reduce(math.lcm,[x.denominator for x in coeffs]+[E00.denominator],1)
 intkernels={}
 for aa,bb,g in set((aa,bb,g) for _,aa,_,bb,g in weak):
  intkernels[aa,bb,g]=[[(p,q,int(c*g*den)) for p,q,c in row] for row in kernels[aa,bb]]
 # Cache the exact sparse rectangular map H: trial support -> entire reached support.
 output_index=dict(lookup);output_states=list(basis)
 rr=[];cc=[];vv=[]
 for c,st in enumerate(basis):
  acc=defaultdict(int); acc[st]+=int((E00+sum(labels[v][2] for v in st))*den)
  for i,aa,j,bb,g in weak:
   assert i!=j
   for p,q,value in intkernels[aa,bb,g][st[i]*dloc+st[j]]:
    out=list(st);out[i]=p;out[j]=q;acc[tuple(out)]+=value
  for out,value in acc.items():
   if not value: continue
   if out not in output_index: output_index[out]=len(output_states);output_states.append(out)
   rr.append(output_index[out]);cc.append(c);vv.append(value)
 Arect=sp.coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(len(output_states),len(basis))).tocsr();Arect.sum_duplicates()
 A=Arect[:len(basis)]
 # Similarity by sqrt(metric) produces the symmetric physical representation.
 sq=np.sqrt(np.array(weights,dtype=float));H=sp.diags(sq)@(A.astype(float)/den)@sp.diags(1/sq)
 assert np.max(np.abs((H-H.T).data),initial=0)<1e-11
 built=time.monotonic()
 if H.shape[0]==1: vals,vecs=np.array([H[0,0]]),np.ones((1,1))
 else: vals,vecs=eigsh(H,k=1,which='SA',tol=1e-13,v0=np.random.default_rng(781).normal(size=H.shape[0]))
 # Overall scale is irrelevant; choose weight relative to product ground to avoid tiny raw amplitudes.
 raw=vecs[:,0]*sq[0]/sq
 ints=[int(round(float(x)*2**bits)) for x in raw]
 norm=sum(w*x*x for w,x in zip(weights,ints))
 Av=[]
 for i in range(Arect.shape[0]):
  Av.append(sum(int(Arect.data[j])*ints[int(Arect.indices[j])] for j in range(Arect.indptr[i],Arect.indptr[i+1])))
 va=sum(w*x*y for w,x,y in zip(weights,ints,Av[:len(ints)]))
 outweights=[w(st) for st in output_states]
 aa=sum(w*x*x for w,x in zip(outweights,Av))
 rho=F(va,den*norm);r2=F(aa,den*den*norm)-rho*rho
 assert r2>=0 and rho<a, (float(rho),float(a),float(r2))
 elo=rho-r2/(a-rho);ehi=rho
 rec=dict(status='exact_rational_sparse_support_ground_certificate',s=str(s),N_dimers=N,physical_sites=2*N,
 full_dimension=int(2*s+1)**(2*N),retained_states=1,trial_subspace_dimension=len(basis),
 reached_support_dimension=len(output_states),trial_max_excited_dimers=max(sum(v!=0 for v in st) for st in basis),support_depth=support_depth,
 E00=str(E00),Vmin=str(vmin),Vmax=str(vmax),second_eigenvalue_lower=str(a),
 ground_lower=str(elo),ground_upper=str(ehi),ground_lower_display=float(elo),ground_upper_display=float(ehi),
 ground_width_display=float(ehi-elo),exact_rayleigh=str(rho),exact_residual_squared=str(r2),
 exact_residual_squared_display=float(r2),integer_matrix_denominator=den,sparse_nnz=Arect.nnz,
 build_seconds=built-t0,total_seconds=time.monotonic()-t0,peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 proof='Exact metric Rayleigh/residual includes all H-applied output states, including outside trial subspace. Ordered Weyl second-level bound and Temple give unique full-Hilbert ground enclosure.')
 # These exact vector and rational graph records suffice to reproduce residual independently.
 artifact=OUT/(tag+'_trial.npz');np.savez_compressed(artifact,vector=np.array(ints,dtype=np.int64),basis=np.array(basis,dtype=np.uint8),bits=bits)
 if relative_bound is not None: rec['relative_form_bound']=relative_bound
 if reference_certificate is not None: rec['reference_certificate']=reference_certificate
 rec['trial_artifact']=artifact.name
 rec['weak_bonds']=[[i,aa,j,bb,str(g)] for i,aa,j,bb,g in weak]
 (OUT/(tag+'_ground.json')).write_text(json.dumps(rec,indent=2))
 print('SPARSE',tag,{k:rec[k] for k in ['physical_sites','full_dimension','trial_subspace_dimension','reached_support_dimension','ground_lower_display','ground_upper_display','ground_width_display','total_seconds','peak_process_rss_kib']},flush=True)
 return rec

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',choices=['bilayer','columnar'],default='bilayer');ap.add_argument('--spin',default='1/2');ap.add_argument('--g',default='1/100');ap.add_argument('--k',default=None);ap.add_argument('--max-excited',type=int,default=2);ap.add_argument('--width',type=int,default=2);ap.add_argument('--nx',type=int,default=4);ap.add_argument('--ny',type=int,default=4);args=ap.parse_args()
 s=F(args.spin);g=F(args.g);k=F(args.k) if args.k else g
 if args.model=='bilayer':
  N=args.nx*args.ny;bonds=bilayer_bonds(args.nx,args.ny,g,k);tag=f'bilayer_s{s}_{args.nx}x{args.ny}_g{g}_k{k}_q{args.max_excited}'
 else:
  N=args.nx*args.width;bonds=columnar_bonds(args.nx,args.width,g,k);tag=f'columnar_s{s}_M{args.nx}_W{args.width}_g{g}_k{k}_q{args.max_excited}'
 certify_sparse(s,N,bonds,args.max_excited,tag=tag.replace('/','d'))
if __name__=='__main__':main()
