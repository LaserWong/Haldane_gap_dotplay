#!/usr/bin/env python3
"""Exact local current tensors and tiny two-vector Rayleigh diagnostics only."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import numpy as np
import itertools,json,time,hashlib
P=Path(__file__).resolve().parent;t0=time.process_time();BASE=P.parent/'mps_excited_seed_witnesses'
data=json.loads((BASE/'local_tensors.json').read_text());A=[np.array(x,dtype=object) for x in data['A']]
B=[np.zeros((26,26),dtype=object),A[0],A[1]]
R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object)
h=np.kron(M,M)+np.kron(R,L)+np.kron(L,R);J=np.kron(R,M)-np.kron(M,R)
assert np.array_equal(h@np.kron(R,I)-np.kron(R,I)@h,J)
assert np.array_equal(h@np.kron(I,R)-np.kron(I,R)@h,-J)
assert not np.any(h@(np.kron(R,I)+np.kron(I,R))-(np.kron(R,I)+np.kron(I,R))@h)
words=[A[s]@A[t] for s,t in itertools.product(range(3),repeat=2)]
current=[]
for s,t in itertools.product(range(3),repeat=2):
    direct=sum((J[3*s+t,x]*words[x] for x in range(9)),np.zeros((26,26),dtype=object))
    tensor=(t-1)*B[s]@A[t]-(s-1)*A[s]@B[t]
    assert np.array_equal(direct,tensor)
    current.append(tensor.tolist())
(P/'current_two_site_tensors.json').write_text(json.dumps({'physical_order':[-1,0,1],'J_operator':'R_i M_j-M_i R_j, with R=S+/sqrt2','word_tensors':current,'commutator_pi_factor':2},indent=2)+'\n')
def clean(v):return {s:c for s,c in v.items() if c}
def add(a,b,scale=1):
    z=dict(a)
    for s,c in b.items():z[s]=z.get(s,0)+scale*c
    return clean(z)
def applyH(v,n):
    out={}
    for s,c in v.items():
        for j in range(n):
            k=(j+1)%n;out[s]=out.get(s,0)+(s[j]-1)*(s[k]-1)*c
            for d in [-1,1]:
                if 0<=s[j]+d<3 and 0<=s[k]-d<3:
                    w=list(s);w[j]+=d;w[k]-=d;w=tuple(w);out[w]=out.get(w,0)+c
    return clean(out)
def raise_sum(v,n,stagger=True):
    out={}
    for s,c in v.items():
        for j in range(n):
            if s[j]<2:
                w=list(s);w[j]+=1;w=tuple(w);out[w]=out.get(w,0)+((-1)**j if stagger else 1)*c
    return clean(out)
def current_sum(v,n):
    out={}
    for s,c in v.items():
        for j in range(n):
            k=(j+1)%n
            for r,coefficient in [(j,s[k]-1),(k,-(s[j]-1))]:
                if s[r]<2:
                    w=list(s);w[r]+=1;w=tuple(w);out[w]=out.get(w,0)+2*(-1)**j*coefficient*c
    return clean(out)
def inner(a,b):return sum(c*b.get(s,0) for s,c in a.items())
rows=[];GRID=1<<160
for n in [2,4,6]:
    psi={}
    for s in itertools.product(range(3),repeat=n):
        if sum(s)!=n:continue
        mat=np.eye(26,dtype=object)
        for x in s:mat=mat@A[x]
        value=int(sum(mat[i,i] for i in range(26)))
        if value:psi[s]=value
    assert not raise_sum(psi,n,False)
    v=raise_sum(psi,n);Hpsi=applyH(psi,n);Hv=applyH(v,n)
    w=add(Hv,raise_sum(Hpsi,n),-1);assert w==current_sum(psi,n)
    assert not raise_sum(w,n,False)
    for state,c in w.items():assert sum(state)==n+1 and w.get(state[1:]+state[:1],0)==-c
    Hw=applyH(w,n);G=[[inner(x,y) for y in [v,w]] for x in [v,w]];H=[[inner(x,y) for y in [Hv,Hw]] for x in [v,w]]
    assert G[0][1]==G[1][0] and H[0][1]==H[1][0]
    detG=G[0][0]*G[1][1]-G[0][1]**2;assert detG>=0
    initial=F(H[0][0],G[0][0]);psiE=F(inner(psi,Hpsi),inner(psi,psi))
    row={'n':n,'Gram':[[str(x) for x in a] for a in G],'H_form':[[str(x) for x in a] for a in H],'Gram_determinant':str(detG),'psi_Rayleigh':str(psiE),'initial_Rayleigh':str(initial),'initial_energy_difference_display':float(initial-psiE),'phi_support':len(v),'commutator_support':len(w),'commutator_H_action_support':len(Hw),'commutator_equals_current_direct':True}
    if detG==0:
        row.update({'retained_span_dimension':1,'verdict':'Current vector is exactly dependent; no two-vector improvement.'})
    else:
        coeff=H[0][0]*G[1][1]+H[1][1]*G[0][0]-2*H[0][1]*G[0][1]
        detH=H[0][0]*H[1][1]-H[0][1]**2;disc=coeff*coeff-4*detG*detH;assert disc>=0
        sq=isqrt(disc*GRID*GRID);slo,shi=F(sq,GRID),F(sq+1,GRID);assert slo*slo<=disc<=shi*shi
        lo,hi=(coeff-shi)/(2*detG),(coeff-slo)/(2*detG)
        mid=(lo+hi)/2;t=-(H[0][0]-mid*G[0][0])/(H[0][1]-mid*G[0][1]);scale=10**9;t=F(round(t*scale),scale)
        ray=(H[0][0]+2*t*H[0][1]+t*t*H[1][1])/(G[0][0]+2*t*G[0][1]+t*t*G[1][1]);assert lo<=ray<=initial and ray-hi<F(1,10**12)
        row.update({'retained_span_dimension':2,'generalized_minimum_interval':list(map(str,[lo,hi])),'fixed_rational_mixing_t':str(t),'mixed_Rayleigh':str(ray),'mixed_energy_difference_display':float(ray-psiE),'improvement_display':float(initial-ray),'verdict':'Exact rational two-vector combination improves this small-size trial Rayleigh.'})
    rows.append(row)
out={'status':'PASS exact local tensors and tiny fixtures only; no n24 run','rows':rows,'MPS_bond_dimension_safe_explicit_bound':156,'bound_explanation':'Open-chain nearest-neighbor sum has a four-channel D104 MPS; two explicit wrapping product terms add2D, giving a simple periodic direct-sum bound6D=156. Better compression may exist but is not asserted.','cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'source_tensor_sha256':hashlib.sha256((BASE/'local_tensors.json').read_bytes()).hexdigest()}
(P/'tiny_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
