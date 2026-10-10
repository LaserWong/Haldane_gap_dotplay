"""Finite-sector exact tests of the bosonic commutator and physical norm bound."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,itertools,math
import numpy as np
from bosonic_number_tail import bounds
from translated_band import Model
from low_band_certificate import exact_inertia
HERE=Path(__file__).resolve().parent


def physical(nx,ny,q):
    m=Model(nx,ny,F(1,10));states=[]
    for positions in itertools.combinations(range(m.N),q):
        for colors in itertools.product((1,2,3),repeat=q):
            states.append(sum(c<<(2*i) for i,c in zip(positions,colors)))
    columns=[{s:c for s,c in m.apply({v:1}).items() if m.q(s)==q+2} for v in states]
    gram=np.diag([m.weight(s) for s in states]).astype(object)
    squares=np.array([[sum(c*columns[j].get(s,0)*m.weight(s) for s,c in columns[i].items())
                      for j in range(len(states))] for i in range(len(states))],dtype=object)
    _,_,v,kappa2,old,bos=bounds(nx,ny,m.g);t2=bos[q]
    inertia=exact_inertia(m.den*m.den*t2*gram-squares);assert inertia[0]==0
    if q==0:assert F(squares[0,0],m.den*m.den*gram[0,0])==v
    return dict(nx=nx,ny=ny,q=q,input_dimension=len(states),full_creation_bound=str(t2),
                bound_minus_exact_creation_gram_inertia=list(inertia),vacuum_exact=q==0)


def occupation(q):return [(i,q-i) for i in range(q+1)]
def metric(states):return np.diag([math.prod(math.factorial(n) for n in s) for s in states]).astype(object)


def creation(K,q):
    source=occupation(q);target=occupation(q+2);index={s:i for i,s in enumerate(target)}
    out=np.zeros((len(target),len(source)),dtype=object)
    for j,s in enumerate(source):
        for u in range(2):
            for v in range(2):
                t=list(s);t[u]+=1;t[v]+=1;out[index[tuple(t)],j]+=K[u,v]/2
    return out


def bosonic(q):
    K=np.array([[F(1),F(1,3)],[F(1,3),F(1,2)]],dtype=object);K2=K@K
    source=occupation(q);index={s:i for i,s in enumerate(source)};G=metric(source)
    B=creation(K,q);Gnext=metric(occupation(q+2));positive=B.T@Gnext@B
    negative=np.zeros_like(G)
    if q>=2:
        prev=creation(K,q-2);Gprev=metric(occupation(q-2))
        inverse=np.diag([F(1,x) for x in np.diag(Gprev)]).astype(object)
        negative=G@prev@inverse@prev.T@G
    second=np.zeros_like(G)
    for j,s in enumerate(source):
        for u in range(2):
            for v in range(2):
                if s[v]:
                    t=list(s);t[v]-=1;t[u]+=1;second[index[tuple(t)],j]+=K2[u,v]*s[v]
    vacuum=sum(K[u,v]**2 for u in range(2) for v in range(2))/2
    assert np.array_equal(positive-negative,G@second+vacuum*G)
    kappa2=F(16,9) # squared maximum absolute row sum
    bound=(q//2+1)*vacuum+kappa2*((q+1)**2//4)
    inertia=exact_inertia(bound*G-positive);assert inertia[0]==0
    return dict(q=q,dimension=len(source),K=[[str(x) for x in row] for row in K],
                exact_commutator_identity=True,creation_bound=str(bound),norm_bound_inertia=list(inertia))


def main():
    phys=[physical(2,2,q) for q in range(3)]+[physical(3,2,q) for q in range(2)]
    bos=[bosonic(q) for q in range(7)]
    result=dict(status='passed_internal_exact_finite_sector_tests_pending_independent_review',physical_cases=phys,bosonic_cases=bos)
    (HERE/'finite_q_validation.json').write_text(json.dumps(result,indent=2))
    print('PASSED',len(phys),'physical norm bounds and',len(bos),'bosonic commutator/norm checks')


if __name__=='__main__':main()
