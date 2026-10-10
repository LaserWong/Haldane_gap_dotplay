#!/usr/bin/env python3
"""Derive exact finite-n24 singlet symmetry; check normalized lowering fixtures."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
from pathlib import Path
import numpy as np
import itertools,json,time,hashlib
P=Path(__file__).resolve().parent;t0=time.process_time();base=P.parent
R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object)
assert np.array_equal(R@L-L@R,M) and np.array_equal(M@R-R@M,R)
assert np.array_equal(M@M+R@L+L@R,2*I)
h=np.kron(M,M)+np.kron(R,L)+np.kron(L,R)
Rt=np.kron(R,I)+np.kron(I,R);Lt=Rt.T;Mt=np.kron(M,I)+np.kron(I,M)
for X in [Rt,Lt,Mt]:assert not np.any(h@X-X@h)
tensors=json.loads((base/'local_tensors.json').read_text());A=[np.array(x,dtype=object) for x in tensors['A']];labels=tensors['labels']
for s,mat in zip([-1,0,1],A):
    for i in range(26):
        for j in range(26):assert not mat[i,j] or labels[j][1]-labels[i][1]==2*s
matrices=json.loads((base/'momentum_extension/exact_matrices_n24.json').read_text());C=list(map(int,matrices['C_displacements']));K=list(map(int,matrices['K_displacements']))
assert sum(C)==0 and sum(K)==0 and C[0]>0
old_fourier=json.loads((base/'momentum_extension/fourier_witness_data.json').read_text())
completed=json.loads((P/'fourier_witness_data.json').read_text())
assert completed['retained_denominator_span_dimension']==70
for row,old in zip(completed['rows'],old_fourier['rows']):
    assert row['k']==old['k'] and row['norm_eigenvalue_interval']==old['norm_eigenvalue_interval']
    if row['k']:
        assert row['Rayleigh_interval']==old['Rayleigh_interval'] and row['retained_spin_components']==3
for row,old in zip(completed['trace_groups'],old_fourier['trace_groups']):
    assert row['k_representative']==old['k_representative']
    assert row['multiplicity']==(6 if row['k_representative']<12 else 3)
    assert row['energy_difference_upper']==old['energy_difference_upper']
def clean(v):return {s:c for s,c in v.items() if c}
def local_raise(psi,r):
    out={}
    for s,c in psi.items():
        if s[r]<2:
            t=list(s);t[r]+=1;out[tuple(t)]=c
    return out
def total(v,sign):
    out={}
    for s,c in v.items():
        for j in range(len(s)):
            if 0<=s[j]+sign<3:
                t=list(s);t[j]+=sign;t=tuple(t);out[t]=out.get(t,0)+c
    return clean(out)
def H(v,n):
    out={}
    for s,c in v.items():
        for j in range(n):
            k=(j+1)%n;out[s]=out.get(s,0)+(s[j]-1)*(s[k]-1)*c
            for sign in [-1,1]:
                if 0<=s[j]+sign<3 and 0<=s[k]-sign<3:
                    t=list(s);t[j]+=sign;t[k]-=sign;t=tuple(t);out[t]=out.get(t,0)+c
    return clean(out)
fixtures=[]
for n in [2,4,6]:
    psi={}
    for s in itertools.product(range(3),repeat=n):
        if sum(s)!=n:continue
        product=np.eye(26,dtype=object)
        for x in s:product=product@A[x]
        value=int(sum(product[i,i] for i in range(26)))
        if value:psi[s]=value
    assert not total(psi,1) and not total(psi,-1)
    vs=[local_raise(psi,r) for r in range(n)];zs=[]
    for r,v in enumerate(vs):
        z=clean({s:(s[r]-1)*c for s,c in psi.items()})
        lowered=total(v,-1)
        assert lowered=={s:-c for s,c in z.items()}
        assert not total(v,1)
        assert total(lowered,1)==v
        zs.append(z)
    hv=[H(v,n) for v in vs];hz=[H(z,n) for z in zs]
    cplus=[sum(c*vs[r].get(s,0) for s,c in vs[0].items()) for r in range(n)]
    cz=[sum(c*zs[r].get(s,0) for s,c in zs[0].items()) for r in range(n)]
    kplus=[sum(c*hv[r].get(s,0) for s,c in vs[0].items()) for r in range(n)]
    kz=[sum(c*hz[r].get(s,0) for s,c in zs[0].items()) for r in range(n)]
    assert cplus==cz and kplus==kz
    fixtures.append({'n':n,'total_raising_psi_zero':True,'total_lowering_psi_zero':True,'local_lowering_equals_minus_longitudinal_at_every_site':True,'all_displacement_Gram_and_H_forms_equal':True,'C':list(map(str,cz)),'K':list(map(str,kz))})
out={'status':'PASS exact finite-n24 singlet and all-momentum spin1 completion','n':24,'exact_sum_C':'0','exact_total_raising_norm':'0','Sz_psi':'0 by checked local charge selection and cyclic trace','normalized_operator_algebra':'R=S+/sqrt2,L=S-/sqrt2; [R,L]=M=Sz; [H,R]=[H,L]=[H,M]=0','derivation':['R psi=0 from zero exact norm. M psi=0 implies norm(L psi)^2=<psi,(LR+M)psi>=0, hence L psi=0.','For v_j=R_j psi, R v_j=0 and M v_j=v_j, so RL v_j=v_j.','Thus <L v_i,L v_j>=<v_i,RL v_j>=<v_i,v_j>; with [H,L]=0, the full H forms agree too.','L v_j=[L,R_j]psi=-Sz_j psi. All normalized lowered Fourier states have bond<=52.','Distinct nonzero momenta and three Sz components give69 orthogonal tangent states. Add psi for70. No spin multiplet or MPS symmetry is assumed before this finite-n derivation.'],'local_integer_commutators_verified':True,'small_physical_fixtures':fixtures,'input_hashes':{str(f.relative_to(base)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [base/'local_tensors.json',base/'momentum_extension/exact_matrices_n24.json',base/'momentum_extension/fourier_witness_data.json']},'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'singlet_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
