#!/usr/bin/env python3
"""Small floating diagnostics for two exact analytic obstructions.
These values are NOT proof inputs to the three-purity certificate.
Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1.
"""
import json
import math
from pathlib import Path
import numpy as np


def hard_core_dirichlet_laplacian(L,W):
    N=L*W
    H=np.zeros((1<<N,1<<N))
    bonds=[]
    # L>=3 here. Each positive x edge counted once.
    for x in range(L):
        for y in range(W):
            i=x*W+y
            bonds.append((i,((x+1)%L)*W+y))
            if y+1<W:
                bonds.append((i,i+1))
    for mask in range(1<<N):
        H[mask,mask]=4*mask.bit_count()
        for i,j in bonds:
            if ((mask>>i)&1)!=((mask>>j)&1):
                H[mask,mask^(1<<i)^(1<<j)]-=1
    return H


def main():
    out={'status':'floating_diagnostics_only','analytic_proofs':'THEORY.md Section 7',
         'strip_gap_counterexample':[],'width_purity_obstruction':[]}
    for W in (1,2,3):
        L=3
        vals=np.linalg.eigvalsh(hard_core_dirichlet_laplacian(L,W))
        expected=2-2*math.cos(math.pi/(W+1))
        assert abs(vals[0])<1e-12 and abs(vals[1]-expected)<1e-11
        out['strip_gap_counterexample'].append({'L':L,'W':W,
            'matrix_dimension':2**(L*W),'computed_gap':float(vals[1]),
            'analytic_gap':expected,'ground_degeneracy_diagnostic':int(np.sum(abs(vals)<1e-10))})
    # A commuting, gapped chain with unique all-up ground state.
    # H=sum (1-z_i)/2 + J*(1-z_i*z_{i+1})/2, J>0.
    beta=1.25;J=.4;n=2
    spins=(1,-1)
    T=np.array([[math.exp(-beta*((1-a)/4+(1-b)/4+J*(1-a*b)/2))
                 for b in spins] for a in spins])
    ev=np.linalg.eigvalsh(T)
    s=sum(ev**(2*n))/sum(ev**n)**2
    assert 0<s<1
    for W in (1,2,4,8,16,32,64,128):
        out['width_purity_obstruction'].append({'W':W,'S_x':float(s**W),
                'one_row_S':float(s),'beta':beta,'n':n,'J':J})
    p=Path(__file__).with_name('toy_checks.json')
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
