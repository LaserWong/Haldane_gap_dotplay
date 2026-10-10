#!/usr/bin/env python3
"""Exact one-trial-state nonperturbative 2D bilayer certificate.

H=sum_r P_triplet(r)+J sum_edges T_r.T_s, J=3/10.
No matrix diagonalization or perturbation expansion is used here.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path
from three_purity_certificate import exp_interval, down, replay


def cert(J=F(3,10),n=2,beta=F(120)):
    J,beta=F(J),F(beta)
    assert 0<=J<F(1,3) and n>=2 and n%2==0
    # The plaquette inequality works including all length-two multibonds.
    gamma=1-3*J if n==2 else 1-F(5,2)*J
    N=n*n
    z=1+3*exp_interval(-beta*gamma)[1]
    purities=[down(z**(-k*N)) for k in (2,4,8)]
    boot=replay(*purities,n=n,m=n,beta=beta)
    L2gap=min(F(1),2-4*J,3-6*J,4-12*J)
    out={'model':'fully_frustrated_spin_half_bilayer',
         'hamiltonian':'sum P_triplet + J sum_square_edges (S1+S2)_r dot (S1+S2)_s',
         'J':str(J),'rung_gap':'1','straight_coupling':str(J),'cross_coupling':str(J),
         'ground_trial_dimension':1,'ground_trial_state':'product of rung singlets',
         'ground_energy':'0','residual_norm_squared':'0',
         'global_hilbert_dimension_at_largest_seed':str(4**(4*N)),
         'max_seed_rungs':4*N,'max_seed_physical_spins':8*N,
         'tail_bound':'Z_N <= (1+3 exp(-beta*gamma))^N; all omitted states are included',
         'gamma_for_seeds':str(gamma),'beta':str(beta),
         'purity_lower_bounds':list(map(str,purities)),
         'purity_lower_bounds_display':list(map(float,purities)),
         'bootstrap':boot,'gap_L2_exact':str(L2gap),
         'gap_L_ge_3_star_lower':str(1-F(5,2)*J),
         'no_perturbative_expansion':True,'complete_spectrum_used':False}
    if J<=F(3,10):
        # q>=4 uses E_q >= q/4, q=2,3 use elementary bond bounds.
        assert 1-F(5,2)*J>=F(1,4)
        assert 2-2*J>=1 and 3-6*J>=1
        out['gap_L_ge_3_exact']='1'
        out['gap_all_square_L_ge_2_exact_infimum']=str(min(F(1),L2gap))
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--J',default='3/10')
    p.add_argument('--n',type=int,default=2)
    p.add_argument('--beta',default='120')
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    out=cert(F(a.J),a.n,F(a.beta))
    s=json.dumps(out,indent=2)
    if a.output:a.output.write_text(s+'\n')
    print(s)

if __name__=='__main__':main()
