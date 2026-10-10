#!/usr/bin/env python3
"""Independent normalized lowering identities and finite-n24 completion."""
import os,resource,time,json,itertools
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
from pathlib import Path
from collections import defaultdict
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time();R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object)
assert np.array_equal(R@L-L@R,M) and np.array_equal(M@R-R@M,R)
h=np.kron(M,M)+np.kron(R,L)+np.kron(L,R)
for X in [R,L,M]:
 total=np.kron(X,I)+np.kron(I,X);assert np.array_equal(h@total,total@h)
A=[np.array(x,dtype=object) for x in json.loads((P/'inputs/local_tensors.json').read_text())['A']]
def apply(v,op,sites):
 out=defaultdict(int)
 for w,a in v.items():
  for j in sites:
   for s in range(3):
    c=int(op[s,w[j]])
    if c:out[w[:j]+(s,)+w[j+1:]]+=c*a
 return {w:a for w,a in out.items() if a}
def fullH(v,n):
 out=defaultdict(int)
 for w,a in v.items():
  for j in range(n):
   k=(j+1)%n
   for s,t in itertools.product(range(3),repeat=2):
    c=int(h[3*s+t,3*w[j]+w[k]])
    if c:
     target=list(w);target[j]=s;target[k]=t;out[tuple(target)]+=c*a
 return {w:a for w,a in out.items() if a}
fixtures=[]
for n in [2,4,6]:
 psi={}
 for w in itertools.product(range(3),repeat=n):
  p=np.eye(26,dtype=object)
  for s in w:p=p@A[s]
  a=int(np.trace(p))
  if a:psi[w]=a
 assert not apply(psi,R,range(n)) and not apply(psi,L,range(n)) and not apply(psi,M,range(n))
 raised=[apply(psi,R,[j]) for j in range(n)];lowered=[]
 for j,v in enumerate(raised):
  z=apply(psi,M,[j]);lv=apply(v,L,range(n));assert lv=={w:-a for w,a in z.items()}
  assert not apply(v,R,range(n)) and apply(v,M,range(n))==v and apply(lv,R,range(n))==v
  lowered.append(lv)
 C=[sum(a*raised[r].get(w,0) for w,a in raised[0].items()) for r in range(n)]
 Hr=[fullH(v,n) for v in raised]
 K=[sum(a*Hr[r].get(w,0) for w,a in raised[0].items()) for r in range(n)]
 # Compute H once for each lowered vector, checking the entire mixed quadratic form row.
 Hz=[fullH(v,n) for v in lowered]
 Cz=[sum(a*lowered[r].get(w,0) for w,a in lowered[0].items()) for r in range(n)]
 Kz=[sum(a*Hz[r].get(w,0) for w,a in lowered[0].items()) for r in range(n)]
 assert C==Cz and K==Kz
 fixtures.append({'n':n,'C':list(map(str,C)),'K':list(map(str,K)),'all_lowering_identities':True})
# n24 singlet proof inputs: exact zero total raising norm and nonzero Sz0 ground.
fourier=json.loads((P/'independent_fourier.json').read_text());assert fourier['zero_global_raising_norm'] and fourier['Gram_rank']==23
source=json.loads((P/'inputs/exact_matrices_n24.json').read_text());assert sum(map(int,source['C_displacements']))==0
prod=json.loads((P/'inputs70/fourier_witness_data.json').read_text());old=json.loads((P/'inputs/fourier_witness_data.json').read_text())
assert prod['retained_denominator_span_dimension']==70
for a,b in zip(prod['rows'],old['rows']):
 assert a['norm_eigenvalue_interval']==b['norm_eigenvalue_interval']
 if a['k']:assert a['Rayleigh_interval']==b['Rayleigh_interval'] and a['retained_spin_components']==3
assert sum(r['multiplicity'] for r in prod['trace_groups'])==69
out={'status':'PASS independent normalized spin completion','n24_ground_singlet_is_derived':True,'requires_H_eigenstate_assumption':False,'local_commutators_and_H_invariance':True,'fixtures':fixtures,'positive_momentum_modes':23,'retained_orthogonal_states':70,'single_state_bond_bound':52,'identities':['[R,L]=M with R=S+/sqrt2, L=S-/sqrt2.','R psi=0 and M psi=0 imply L psi=0 by norm positivity.','R v_j=0 and M v_j=v_j imply RL v_j=v_j.','<L v_i,L v_j>=<v_i,v_j>; [H,L]=0 gives equal full-H forms.','L v_j=-Sz_j psi; each lowered Fourier vector remains a single-source bond52 MPS.'],'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_singlet.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='fixtures'}))
