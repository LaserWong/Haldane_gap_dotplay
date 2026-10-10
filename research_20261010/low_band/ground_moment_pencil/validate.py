"""Synthetic exact checks; independent review still required."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
import json
import numpy as np
from certify import certify_pencil,HERE


def moments(e,W):
    H=np.diag(list(map(F,e)));W=np.array(W,dtype=object)
    return W.T@W,W.T@H@W,(H@W).T@(H@W)


def main():
    cases=[]
    # Nonorthogonal rectangular trials, m>k, exact cutoff eigenvalues included.
    for k in (1,2,3):
      for seed in range(8):
        rng=np.random.default_rng(173+seed)
        e=[F(i-k-1) for i in range(k)]+[F(0),F(2),F(4),F(7)]
        m=k+2;n=len(e)
        W=np.zeros((n,m),dtype=object)
        # All low eigenvectors are present, mixed nonorthogonally. High
        # directions contain a cutoff component but no pure cutoff vector.
        W[:k,:k]=np.eye(k,dtype=int)
        W[k,k:]=[1,2];W[k+1,k]=1;W[k+2,k+1]=1
        T=np.eye(m,dtype=object)
        for i in range(m):
          for j in range(i+1,m):T[i,j]=int(rng.integers(-2,3))
        W=W@T;G,A,B=moments(e,W);rec=certify_pencil(G,A,B,F(0),k)
        for endpoint in rec['endpoints']:
          idx=endpoint['sector_eigenvalue_index_one_based']-1
          assert F(endpoint['lower'])<e[idx]<=F(endpoint['optimal_pencil_endpoint_upper'])
        cases.append(dict(k=k,m=m,seed=seed,cutoff_eigenvalue_present=True,certificate=rec))
    # Nonzero leakage and subspace not containing the ground eigenvector.
    for seed in range(10):
        e=[F(-3),F(0),F(2),F(5),F(8)]
        W=[[1,0,0],[0,1,0],[F(seed+1,30),1,0],[0,0,1],[F(1,10),0,1]]
        G,A,B=moments(e,W);rec=certify_pencil(G,A,B,F(0),1)
        assert F(rec['endpoints'][0]['lower'])<e[0]
        cases.append(dict(k=1,m=3,nonzero_leakage=True,seed=seed,certificate=rec))
    # Correct generalized k theorem with only one negative trial Ritz:
    # bounds lambda_2, and cannot bound the unrepresented lambda_1.
    G,A,B=moments([-2,-1,1],[[0,0],[1,0],[0,1]])
    proper=certify_pencil(G,A,B,0,2)
    assert proper['endpoints'][0]['sector_eigenvalue_index_one_based']==2
    invalid=certify_pencil(G,A,B,0,1)
    assert F(invalid['endpoints'][0]['lower'])>F(-2)
    # A cutoff eigenvector in W makes S singular, which is rejected.
    singular_rejected=False
    try:
        certify_pencil(*moments([-1,0,2],[[1,0],[0,1],[0,0]]),0,1)
    except AssertionError:singular_rejected=True
    assert singular_rejected
    out=dict(status='all_synthetic_exact_tests_passed',case_count=len(cases),cases=cases,
      missing_external_count_counterexample=dict(H=[-2,-1,1],a=0,correct_count=2,trial=[[0,0],[1,0],[0,1]],
        valid_second_eigenvalue_certificate=proper,invalid_if_falsely_declared_one_low_state=invalid),
      singular_shifted_gram_rejected=singular_rejected)
    (HERE/'validation.json').write_text(json.dumps(out,indent=2));print('PASS',len(cases),'synthetic cases; count counterexample; cutoff singularity')

if __name__=='__main__':main()
