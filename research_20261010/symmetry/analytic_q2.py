"""Analytic exact Gram/H/H^2 for symmetry-compressed q<=2 singlet trials.

The Q4 leakage is evaluated in the three pairings per four-rung set. Their
normalized Gram is diag(9), offdiag(3), checked against explicit rational states.
No four-triplet physical configurations are constructed by this module.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import math,json,time,itertools,resource,argparse
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy.linalg as la
from symmetric_ground import Model,OUT
from local_relative_bound import optimize_bound

def analytic_matrices(model):
    start=time.monotonic();_,orbits=model.q2_basis();d=1+len(orbits);N=model.N;p=model.g.numerator
    ids={pair:i+1 for i,orb in enumerate(orbits) for pair in orb}
    orbit=lambda i,j:ids[tuple(sorted((i,j)))]
    mult=[[0]*N for _ in range(N)]
    for a,b,m in model.edges:mult[a//2][b//2]=mult[b//2][a//2]=m
    diag=[1]+[3*len(orb) for orb in orbits]
    C=[[0]*d for _ in range(d)]
    for j,orb in enumerate(orbits,1):C[0][j]=6*p*sum(mult[a][b] for a,b in orb)
    for row,orb in enumerate(orbits,1):
        i,j=orb[0];C[row][0]=2*p*mult[i][j];C[row][row]=2*model.den-4*p*mult[i][j]
        for k in range(N):
            if k in (i,j):continue
            C[row][orbit(k,j)]+=2*p*mult[i][k]
            C[row][orbit(k,i)]+=2*p*mult[j][k]
    G=[[diag[i] if i==j else 0 for j in range(d)] for i in range(d)]
    K=[[diag[i]*C[i][j] for j in range(d)] for i in range(d)]
    assert K==list(map(list,zip(*K)))
    J=[[sum(C[k][i]*diag[k]*C[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
    leakage=[[0]*d for _ in range(d)];nonzero=0
    def add_outer(v,scale):
        for i,a in v.items():
            for j,b in v.items():leakage[i][j]+=scale*a*b
    for i,j,k,l in itertools.combinations(range(N),4):
        pairings=[((i,j),(k,l)),((i,k),(j,l)),((i,l),(j,k))]
        amps=[]
        for (a,b),(c,e) in pairings:
            amp={}
            if mult[a][b]:amp[ids[c,e]]=2*p*mult[a][b]
            if mult[c][e]:amp[ids[a,b]]=amp.get(ids[a,b],0)+2*p*mult[c][e]
            if amp:amps.append(amp)
        if not amps:continue
        nonzero+=1;total={}
        for amp in amps:
            add_outer(amp,6)
            for a,b in amp.items():total[a]=total.get(a,0)+b
        add_outer(total,3)
    J=[[J[i][j]+leakage[i][j] for j in range(d)] for i in range(d)]
    return G,K,J,orbits,dict(four_rung_subsets=math.comb(N,4),nonzero_four_rung_subsets=nonzero,analytic_build_seconds=time.monotonic()-start)

def bilinear(v,A,w=None):
    if w is None:w=v
    return sum(v[i]*A[i][j]*w[j] for i in range(len(v)) for j in range(len(w)))

def certify(nx,ny,g,bits=48,save=True):
    start=time.monotonic();model=Model(nx,ny,g);G,K,J,orbits,cost=analytic_matrices(model)
    d=len(G);sq=np.sqrt([G[i][i] for i in range(d)])
    H=np.array(K,dtype=float)/sq[:,None]/sq[None,:]/model.den
    vals,vecs=la.eigh(H);vraw=vecs[:,0]/sq;vraw/=max(abs(vraw));v=[int(round(x*2**bits)) for x in vraw]
    norm=bilinear(v,G);mean=F(bilinear(v,K),norm*model.den)
    ray=model.E00+mean;r2=F(bilinear(v,J),norm*model.den**2)-mean**2
    bound=optimize_bound(F(1,2),model.g,'bilayer',model.N)
    a=model.E00+F(bound['second_shift_lower']);assert ray<a
    lo=ray-r2/(a-ray)
    rec=dict(status='exact_rational_analytic_q2_symmetry_certificate',s='1/2',nx=nx,ny=ny,N_dimers=model.N,physical_sites=2*model.N,coupling=str(model.g),
        full_dimension=4**model.N,Sz0_full_dimension=math.comb(2*model.N,model.N),q2_Sz0_dimension=1+model.N+3*math.comb(model.N,2),
        q2_even_parity_Sz0_dimension=1+3*math.comb(model.N,2),q2_singlet_dimension=1+math.comb(model.N,2),trial_subspace_dimension=d,retained_states=1,
        pair_orbit_sizes=[len(orb) for orb in orbits],spatial_group_order=len(model.group()),
        gram_common_factor_removed=str(2**model.N),gram=[[str(x) for x in row] for row in G],
        shifted_hamiltonian_numerator=[[str(x) for x in row] for row in K],shifted_H2_numerator=[[str(x) for x in row] for row in J],
        integer_matrix_denominator=model.den,coefficients=[str(x) for x in v],bits=bits,
        E00=str(model.E00),second_eigenvalue_lower=str(a),ground_lower=str(lo),ground_upper=str(ray),exact_rayleigh=str(ray),exact_residual_squared=str(r2),
        ground_lower_display=float(lo),ground_upper_display=float(ray),ground_width_display=float(ray-lo),exact_residual_squared_display=float(r2),
        relative_form_bound=bound,total_seconds=time.monotonic()-start,peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        proof='SU2-singlet/translation/reflection q2 basis. Exact Q4 leakage contracted using three-pairing Gram diag9/off3; full-space relative-form comparison and Temple.')
    rec.update(cost)
    if save:(OUT/(f'analytic_{nx}x{ny}_g{g}.json'.replace('/','d'))).write_text(json.dumps(rec,indent=2))
    print(json.dumps({k:rec[k] for k in ['nx','ny','coupling','trial_subspace_dimension','ground_upper_display','ground_width_display','exact_residual_squared_display','four_rung_subsets','nonzero_four_rung_subsets','analytic_build_seconds','total_seconds','peak_process_rss_kib']}),flush=True)
    return rec

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--nx',type=int,default=4);a.add_argument('--ny',type=int,default=4);a.add_argument('--g',default='1/100');args=a.parse_args();certify(args.nx,args.ny,args.g)
