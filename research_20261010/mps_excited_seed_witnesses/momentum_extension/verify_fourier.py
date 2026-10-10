#!/usr/bin/env python3
"""Exact displacement matrices and certified Fourier Rayleigh intervals at n24."""
import os,resource,json,time
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
P=Path(__file__).resolve().parent;t0=time.process_time();GRID=1<<160
def raw(f):return {k:int(v) for k,v in (line.strip().split('=') for line in f.read_text().splitlines())}
fixtures=raw(P/'fixtures_plus.out')
for row in json.loads((P/'source_checks_plus.json').read_text())['fixtures']:
    n=row['n']
    for r in range(n):
        assert fixtures[f'C{n}_{r}']==int(row['C'][r])
        assert fixtures[f'K{n}_{r}']==int(row['K'][r])
data=raw(P/'benchmark_n24_plus.out');other=raw(P/'remaining_n24_plus.out')
assert not (data.keys()&other.keys());data.update(other)
n=24;C=[data[f'C24_{min(r,24-r)}'] for r in range(24)];K=[data[f'K24_{min(r,24-r)}'] for r in range(24)]
assert C[0]>0 and sum(C)==0 and sum(K)==0
prior=raw(P.parent/'contractions_n24.out')
assert n*sum((-1)**r*C[r] for r in range(n))==prior['N1_24']
assert n*sum((-1)**r*K[r] for r in range(n))==prior['H1_24']
Gmatrix=[[str(C[(j-i)%n]) for j in range(n)] for i in range(n)]
Hmatrix=[[str(K[(j-i)%n]) for j in range(n)] for i in range(n)]
matrix={'n':n,'basis':'v_j=(S_j^+/sqrt2) psi24, j=0,...,23; real vectors','C_displacements':list(map(str,C)),'K_displacements':list(map(str,K)),'Gram_matrix':Gmatrix,'H_quadratic_form_matrix':Hmatrix,'zero_mode':'Exact sum C(r)=sum K(r)=0. The total-raising vector is zero at this length, certified by its zero norm.','symmetry':'Reality, translation of psi and commutation of H with translation imply C(r)=C(n-r), K(r)=K(n-r), independently of reflection or SU2 invariance.'}
(P/'exact_matrices_n24.json').write_text(json.dumps(matrix,indent=2)+'\n')
def sqrt_i(x):
    a=isqrt(x*GRID*GRID);lo,hi=F(a,GRID),F(a+1,GRID)
    assert lo*lo<=x<=hi*hi
    return lo,hi
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def scale(a,c):return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
z=(F(0),F(0));one=(F(1),F(1));s2,s3,s6=[sqrt_i(k) for k in [2,3,6]]
positive=[one,scale(add(s6,s2),F(1,4)),scale(s3,F(1,2)),scale(s2,F(1,2)),(F(1,2),F(1,2)),scale(add(s6,neg(s2)),F(1,4)),z]
cosines=positive+[neg(positive[12-k]) for k in range(7,13)]
cosines+=cosines[11:0:-1]
assert len(cosines)==24
def fourier(values,k):
    out=z
    for r,v in enumerate(values):out=add(out,scale(cosines[(k*r)%n],v))
    return out
rows=[]
base=json.loads((P.parent/'exact_witness_data.json').read_text())['rows'][-1];alpha0=F(base['alpha0'])
for k in range(n):
    norm=fourier(C,k);energy=fourier(K,k)
    if k==0:
        assert norm==(F(0),F(0)) and energy==(F(0),F(0))
        rows.append({'k':0,'status':'zero vector; not retained','norm_eigenvalue_interval':['0','0']});continue
    assert norm[0]>0
    quotients=[e/x for e in energy for x in norm];lo,hi=min(quotients),max(quotients)
    assert hi-alpha0>0
    rows.append({'k':k,'momentum_over_pi':str(F(k,12)),'status':'positive norm; retained','norm_eigenvalue_interval':list(map(str,norm)),'H_eigenvalue_interval':list(map(str,energy)),'Rayleigh_interval':[str(lo),str(hi)],'Rayleigh_display':float((lo+hi)/2),'energy_difference_from_psi_upper':str(hi-alpha0),'energy_difference_display':float((lo+hi)/2-alpha0),'retained_with_spin_flip':2})
assert F(rows[12]['Rayleigh_interval'][0])==F(base['alpha1'])==F(rows[12]['Rayleigh_interval'][1])
for k in range(1,12):assert rows[k]['Rayleigh_interval']==rows[n-k]['Rayleigh_interval']
groups=[{'k_representative':k,'multiplicity':4 if k<12 else 3,'energy_difference_upper':rows[k]['energy_difference_from_psi_upper']} for k in range(1,13)]
out={'status':'PASS exact integer matrices and directed radical Fourier intervals; independent review pending','n':24,'ground_Rayleigh':base['alpha0'],'numerator_Rayleigh':base['R_2n'],'delta':base['delta'],'rows':rows,'trace_groups':groups,'retained_denominator_span_dimension':48,'span_description':'psi plus23 nonzero momentum vectors in Sz+1, their23 globally spin-flipped Sz-1 partners, and one longitudinal momentum-pi Sz0 vector. Orthogonality follows from distinct Sz and exact translation eigenvalues.','linear_search_dimension':'No energy optimization or eigensolver: fixed24 translation orbit; Fourier transform diagonalizes its circulant Gram and H forms algebraically.','maximum_single_state_MPS_bond_dimension':52,'full_Hilbert_dimension':3**24,'trigonometric_certificate':'At n24, cos(k*r*pi/12) is expressed by rational combinations of sqrt2,sqrt3,sqrt6. Each square root has160-bit rational endpoints checked by exact squaring.','cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'fourier_witness_data.json').write_text(json.dumps(out,indent=2)+'\n')
for k in range(1,13):print(k,rows[k]['Rayleigh_display'],rows[k]['energy_difference_display'])
print('Retained orthogonal states48; exact zero total-raising mode omitted')
