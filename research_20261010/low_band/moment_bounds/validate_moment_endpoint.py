"""Exact rational validation of the inverse-moment theorem and its scope.

The listed spectra are fixed by construction, not numerical diagonalization.
These are internal tests, not an independent audit of the theorem or physics.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json, random
import numpy as np
from moment_endpoint import certify, exact_inertia

HERE=Path(__file__).resolve().parent


def inv(matrix):
    a=np.asarray(matrix,dtype=object)
    n=len(a)
    rows=[[F(x) for x in a[i]]+[F(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot=next(j for j in range(i,n) if rows[j][i])
        rows[i],rows[pivot]=rows[pivot],rows[i]
        p=rows[i][i];rows[i]=[x/p for x in rows[i]]
        for j in range(n):
            if j!=i:
                p=rows[j][i]
                rows[j]=[x-p*y for x,y in zip(rows[j],rows[i])]
    return np.array([r[n:] for r in rows],dtype=object)


def main():
    rng=random.Random(20261010)
    cases=[]
    for k in (1,2,3):
        for cutoff_equality in (False,True):
            for repeat in range(12):
                n=k+4;a=F(2)
                spectrum=[F(i-k) for i in range(k)]+[a+int(not cutoff_equality),a+1,a+3,a+7]
                H=np.diag(spectrum).astype(object)
                W=np.array([[F(i==j) if i<k else F(rng.randint(-3,3),40)
                             for j in range(k)] for i in range(n)],dtype=object)
                transform=np.array([[F(i==j)+F(rng.randint(-1,1),8) for j in range(k)] for i in range(k)],dtype=object)
                W=W@transform
                G=W.T@W;A=W.T@H@W;B=(H@W).T@(H@W)
                rec=certify(G,A,B,a)
                for i,row in enumerate(rec['endpoints']):
                    assert F(row['lower'])<=spectrum[i]
                # Independently sweep strict moment-pencil tests and check every
                # accepted endpoint against the known exact ordered spectrum.
                checks=0
                for numerator in range(-32,8):
                    endpoint=F(numerator,4)
                    neg=exact_inertia(B-(a+endpoint)*A+a*endpoint*G)[0]
                    for i in range(k):
                        if neg>=k-i:
                            assert endpoint<=spectrum[i]
                            checks+=1
                if k==1:
                    rho=A[0,0]/G[0,0]
                    r2=B[0,0]/G[0,0]-rho*rho
                    temple=rho-r2/(a-rho)
                    assert F(rec['endpoints'][0]['lower'])<=temple
                    assert temple-F(rec['endpoints'][0]['lower'])<F(1,10**9)
                cases.append(dict(k=k,cutoff_equality=cutoff_equality,repeat=repeat,
                                  exact_spectrum=list(map(str,spectrum)),accepted_grid_checks=checks,
                                  certificate=rec))
    complement=[]
    for k in (1,2,3):
        n=k+4;a=F(2)
        H=np.diag([F(i-k) for i in range(k)]+[a,a+1,a+3,a+7]).astype(object)
        # Exact rational Householder matrix close to identity on the trial block.
        v=np.array([F(1,100)]*k+[F(1),F(0),F(0),F(0)],dtype=object)
        O=np.eye(n,dtype=object)-2*np.outer(v,v)/sum(x*x for x in v)
        assert np.array_equal(O.T@O,np.eye(n,dtype=object))
        Q,U=O[:,:k],O[:,k:]
        T=Q.T@H@Q;R=U.T@H@Q;C=U.T@H@U
        K=T-a*np.eye(k,dtype=object)
        assert exact_inertia(K)==(k,0,0)
        schur=C-a*np.eye(n-k,dtype=object)+R@inv(-K)@R.T
        assert exact_inertia(schur)[0]==0
        complement.append(dict(k=k,cutoff_equality=True,schur_inertia=list(exact_inertia(schur))))
    # The method cannot infer the external count from residuals or moments.
    invalid_count_example=certify([[F(1)]],[[F(0)]],[[F(0)]],F(2))
    assert F(invalid_count_example['endpoints'][0]['lower'])>F(-10)
    out=dict(status='passed_internal_exact_rational_tests_not_independent_review',
             moment_cases=cases,exact_direct_complement_cases=complement,
             missing_count_counterexample=dict(H_diagonal=['-10','0','2'],trial='second coordinate',
               residual_squared='0',true_ground='-10',
               invalid_claim='lambda_2 >= 2 is false; trial moments alone do not detect this',
               certificate_if_false_count_supplied=invalid_count_example))
    (HERE/'moment_validation.json').write_text(json.dumps(out,indent=2))
    print('PASSED',len(cases),'exact moment cases and',len(complement),'exact complement cases')


if __name__=='__main__':main()
