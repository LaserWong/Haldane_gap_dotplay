#!/usr/bin/env python3
"""Exact-rational replay of a three-purity 2D bootstrap.

All accept/reject comparisons and emitted gap lower bounds use rational
arithmetic. This checks scalar/analytic seed arithmetic, not a formal proof of
the transfer or interpolation theorems in THEORY.md. No diagonalization.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


def down(x, digits=18):
    s=10**digits
    return F(x.numerator*s//x.denominator,s)


def up(x, digits=18):
    s=10**digits
    return F(-((-x.numerator*s)//x.denominator),s)


def exp_positive(x, terms=160):
    x=F(x)
    if not 0<=x<terms+2:
        raise ValueError('Taylor remainder condition failed')
    term=F(1); total=term
    for k in range(1,terms+1):
        term*=x/k; total+=term
    first=term*x/(terms+1)
    return total,total+first/(1-x/(terms+2))


def exp_interval(x):
    x=F(x)
    if x>=0:
        return exp_positive(x,max(160,3*int(x)+40))
    a,b=exp_positive(-x,max(160,-3*int(x)+40))
    return 1/b,1/a


def log_lower(x,terms=80):
    x=F(x)
    assert x>1
    k=0
    while x>=2:
        x/=2; k+=1
    def unit(y):
        z=(y-1)/(y+1)
        return 2*sum((z**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    return k*unit(F(2))+unit(x)


def f(u):
    assert 0<=u<1
    return u*u/(2*(1-u)**2)


def advance(defects,digits=18):
    # The evolving list is a staircase path in (x,y,beta) doubling space.
    q=list(defects)
    for _ in range(3):
        a,b,c=q
        v=1-(1-a)**4*(1-b)**2*(1-c)
        if v>=1:
            return None
        new=up(f(v),digits)
        if new>=1:
            return None
        q=q[1:]+[new]
    return q


def replay(A,B,C,n=2,m=2,beta=F(12),rounds=32,digits=18):
    A,B,C,beta=map(F,(A,B,C,beta))
    assert n>=2 and m>=2 and n%2==m%2==0 and beta>0
    assert all(0<x<=1 for x in (A,B,C))
    q=[up(1-x,digits) for x in (A,B,C)]
    out={'input':{'A_lower':str(A),'B_lower':str(B),'C_lower':str(C),
                  'n':n,'m':m,'beta':str(beta)},'updates':[],
         'status':'not_accepted','formal_proof_assistant_verified':False}
    for j in range(rounds+1):
        u=max(q)
        # .002 ensures two successive applications of all-integer 1D
        # interpolation remain in its .01 region.
        if u<=F(1,500):
            out.update(status='accepted_analytic_scalar_certificate',rounds=j,
                       n=n,m=m,beta=str(beta),defects=list(map(str,q)),u=str(u))
            if u:
                gap=down(log_lower(1/(32*u))/beta,12)
                out['uniform_square_gap_lower']=str(gap)
                out['uniform_square_gap_lower_display']=float(gap)
            out['scope']='Every integer square side L >= n, when n=m and the two transfer hypotheses hold. For n != m, each dyadic rectangle [2^j n,2^(j+1)n] x [2^j m,2^(j+1)m].'
            return out
        if j==rounds:
            break
        nq=advance(q,digits)
        if nq is None:
            out['status']='bound_left_purity_domain';return out
        q=nq;n*=2;m*=2;beta*=2
        out['updates'].append({'round':j+1,'defects':list(map(str,q))})
    return out


def analytic_seed(model='bilayer_s_half',g=F(1,4000),beta=F(12),n=2,m=2):
    g,beta=F(g),F(beta)
    assert g>=0
    e=exp_interval(-beta)[1]
    if model=='bilayer_s_half':
        z=1+3*e
        b=4*g
        spins_per_cell=2
    elif model=='square_spin_one_large_D':
        # D=1. Each spin-one Heisenberg bond has spectral width 3.
        z=1+2*e
        b=6*g
        spins_per_cell=1
    else:
        raise ValueError(model)
    N=n*m
    exponents=[(beta*b*N)**2/4,(beta*b*2*N)**2/4,(beta*b*4*N)**2/4]
    A=down(exp_interval(-exponents[0])[0])
    B=down(exp_interval(-exponents[1])[0])
    C=down(exp_interval(-exponents[2])[0]/z**(8*N))
    out={'model':model,'g':str(g),'beta':str(beta),'onsite_gap':'1',
         'periodic_length_2_convention':'Two distinct directed-neighbor terms connect the same pair; no simple-graph deduplication.',
         'maximum_seed_spins':4*N*spins_per_cell,
         'trace_seed_method':'Gibbs variational lower + Golden-Thompson + centered Hoeffding upper',
         'perturbation_spectral_width_bound_per_cell':str(b),
         'seed_exponents':list(map(str,exponents)),
         'purity_lower_bounds':list(map(str,(A,B,C))),
         'purity_lower_bounds_display':list(map(float,(A,B,C))),
         'full_spectrum_used':False,
         'bootstrap':replay(A,B,C,n,m,beta)}
    return out


def checks():
    u=F(1,100)
    assert 49/(2*(1-7*u)**2)<32
    assert 32*u<=1
    # First axis-transfer interpolation and then strip interpolation.
    u=F(1,500)
    assert 5*u<=F(1,100)
    assert 20/(1-20*u)<=32
    # Exact polynomial check of (1-u)^3(1-2u)>=1-5u on [0,.01].
    # Difference is u^2(9-7u+2u^2)>0.
    assert (1-u)**3*(1-2*u)-(1-5*u)==u*u*(9-7*u+2*u*u)
    # Ground-state thermal tail -> gap.
    assert u/(1-u)<=32*u


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--model',default='bilayer_s_half',choices=['bilayer_s_half','square_spin_one_large_D'])
    p.add_argument('--g',default='1/4000')
    p.add_argument('--beta',default='12')
    p.add_argument('--output',type=Path)
    a=p.parse_args();checks()
    out=analytic_seed(a.model,F(a.g),F(a.beta))
    s=json.dumps(out,indent=2)
    if a.output:
        a.output.write_text(s+'\n')
    print(s)

if __name__=='__main__':
    main()
