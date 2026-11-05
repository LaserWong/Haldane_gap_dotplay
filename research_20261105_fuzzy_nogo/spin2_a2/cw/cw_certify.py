"""Rigorous certification (python-flint arb, 128-bit) of the CW bound for a saved Jastrow solution.
theta, phi are rounded to exact dyadic rationals (these DEFINE the test vector; no approximation enters
the inequality). mu_cert = min over all edges of the arb lower endpoint of
   zz + phi[src]-phi[dst] - sum_flips exp(A theta)."""
import json,sys,numpy as np
from fractions import Fraction
from flint import arb, ctx
from cw_jastrow import build
ctx.prec=128
k=int(sys.argv[1]); r=json.load(open(f'jastrow_k{k}.json')); B=build(k)
q=lambda v: Fraction(v).limit_denominator(2**40)
th=[arb(q(t).numerator)/q(t).denominator for t in r['theta']]
ph=[arb(q(t).numerator)/q(t).denominator for t in r['phi']]
A=B['A'].tocsr(); F=B['F'].tocsc()
expo=[]
for f in range(A.shape[0]):
    s=arb(0)
    for j in range(A.indptr[f],A.indptr[f+1]): s+=int(A.data[j])*th[A.indices[j]]
    expo.append(s.exp())
Fc=B['F'].tocsr(); mu=None; arg=None
for e in range(len(B['zz'])):
    v=arb(int(B['zz'][e]))+ph[B['src'][e]]-ph[B['dst'][e]]
    for j in range(Fc.indptr[e],Fc.indptr[e+1]): v-=expo[Fc.indices[j]]
    lo=v.lower()
    if mu is None or lo<mu: mu=lo; arg=e
out=dict(k=k,mu_cert_lower=str(mu),mu_cert_float=float(mu.mid()),mu_float_solver=r['mu_float'],argmin_edge=int(arg))
print(json.dumps(out)); json.dump(out,open(f'cert_k{k}.json','w'))
