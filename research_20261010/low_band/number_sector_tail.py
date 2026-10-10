"""Whole-spectrum lower bins from number-sector Jacobi comparison.
Integer graph counts, rational local PSD, and rational tridiagonal LDL certify
all endpoints. Floating scalar Jacobi solves only propose the endpoints.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,time,argparse
from fractions import Fraction as F
from collections import defaultdict
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
from low_band_certificate import OUT,exact_inertia,lower_round,finish_block,exp_bounds,down
from dimer_subspace import dimer_local

def occupation_counts(nx,ny):
    assert nx>=2 and ny>=2
    N=nx*ny;edges=defaultdict(int);index=lambda x,y:(x%nx)*ny+y%ny
    for x in range(nx):
        for y in range(ny):
            i=index(x,y)
            for j in [index(x+1,y),index(x,y+1)]:edges[tuple(sorted((i,j)))]+=1
    assert sum(edges.values())==2*N
    degrees=[sum(w for (i,j),w in edges.items() if s in (i,j)) for s in range(N)]
    assert degrees==[4]*N
    emax=[0]*(N+1);witness=[0]*(N+1)
    for mask in range(1<<N):
        q=mask.bit_count();v=sum(w for (i,j),w in edges.items() if mask>>i&1 and mask>>j&1)
        if v>emax[q]:emax[q]=v;witness[q]=mask
    empty=[2*N-4*q+emax[q] for q in range(N+1)]
    assert all(v>=0 for v in empty)
    return dict(N=N,edges=[[i,j,w] for (i,j),w in sorted(edges.items())],degrees=degrees,
                occupied_edge_max=emax,empty_edge_max=empty,witness_masks=witness,
                enumeration_size=1<<N)

def local_check():
    labels,weights,kernels=dimer_local(F(1,2));nq=[int(x[0]!=0) for x in labels]
    J=np.array([weights[i]*weights[j] for i in range(4) for j in range(4)],dtype=object)
    q=[nq[i]+nq[j] for i in range(4) for j in range(4)]
    V=np.zeros((16,16),dtype=object)
    for col in range(16):
        for ab in [(0,0),(1,1)]:
            for i,j,v in kernels[ab][col]:V[4*i+j,col]+=v
    W=np.array([[V[i,j] if q[i]==q[j] else F(0) for j in range(16)] for i in range(16)],dtype=object)
    W+=np.diag([F(x,2) for x in q]);W=J[:,None]*W
    inert=exact_inertia(W);assert inert[0]==0
    creation=[]
    for i in range(16):
        for j in range(16):
            if q[i]==q[j]+2 and V[i,j]:
                normalized_abs2=F(V[i,j])**2*F(int(J[i]),int(J[j]));assert normalized_abs2==F(1,4)
                creation.append([i,j,str(normalized_abs2)])
    assert len(creation)==3
    assert all(not V[i,j] or abs(q[i]-q[j]) in [0,2] for i in range(16) for j in range(16))
    return dict(preserving_plus_half_number_inertia=inert,creation_entries_abs_squared=creation,
                local_convention='v=S_i,0.S_j,0+S_i,1.S_j,1, unit coupling')

def tridiagonal_lower(diag,off2):
    proposal=eigvalsh_tridiagonal(np.array(list(map(float,diag))),-np.sqrt(np.array(list(map(float,off2)))),select='i',select_range=(0,0))[0] if len(diag)>1 else float(diag[0])
    lo=lower_round(proposal,digits=12)
    def pivots(t):
        out=[]
        for i,d in enumerate(diag):
            p=d-t-(off2[i-1]/out[-1] if i else 0)
            if p<=0:return None
            out.append(p)
        return out
    while pivots(lo) is None:lo-=F(1,10**10)
    return lo,[str(x) for x in pivots(lo)]

def certify_bins(nx,ny,g):
    start=time.monotonic();g=F(g);assert 0<=g<F(1,2)
    counts=occupation_counts(nx,ny);N=counts['N'];diag=[(1-2*g)*q for q in range(N+1)]
    off2=[F(3,4)*g*g*counts['empty_edge_max'][q]*counts['occupied_edge_max'][q+2] for q in range(N-1)]
    bins=[]
    for q in range(N+1):
        parts=[]
        for startq in [q,q+1]:
            if startq>N:continue
            inds=list(range(startq,N+1,2));lo,piv=tridiagonal_lower([diag[j] for j in inds],[off2[j] for j in inds[:-1]])
            parts.append(dict(number_indices=inds,lower=str(lo),ldl_positive_pivots=piv))
        lo=min(F(p['lower']) for p in parts)
        if q:lo=max(lo,F(bins[-1]['lower']))
        bins.append(dict(q=q,lower=str(lo),multiplicity=math.comb(N,q)*3**q,
            first_ordered_index=1+sum(math.comb(N,j)*3**j for j in range(q)),parity_compressions=parts))
    rec=dict(status='exact_number_sector_jacobi_spectrum_bins_pending_independent_review',nx=nx,ny=ny,N=N,g=str(g),
        energy_shift=str(-F(3*N,4)),local_certificate=local_check(),graph_counts=counts,
        diagonal=list(map(str,diag)),offdiagonal_squared=list(map(str,off2)),bins=bins,seconds=time.monotonic()-start)
    (OUT/f'number_bins_{nx}x{ny}_g{g}.json'.replace('/','d')).write_text(json.dumps(rec,indent=2))
    print('NUMBER',nx,ny,'a0,1,2',[float(F(x['lower'])) for x in bins[:3]],'seconds',rec['seconds'],flush=True)
    return rec

def update_certificate(rec,number):
    rec=json.loads(json.dumps(rec));a=F(number['bins'][2]['lower']);L0=F(number['bins'][0]['lower'])
    r=F(rec['ritz_max_upper']);eps=F(rec['residual_squared_bound']);assert a>r
    s2=min(F(1),eps/(a-r)**2);b=a-(a-L0)*s2;assert b>r
    rec.update(global_lambda_kplus1_lower=str(a),global_ground_lower=str(L0),sin_angle_squared_upper=str(s2),orthogonal_complement_lower=str(b),number_sector_bins=number)
    rec['blocks']=[finish_block(block,b) for block in rec['blocks']]
    rec['status']='exact_full_low_band_and_number_sector_tail_pending_independent_review'
    return rec

def main():
    p=argparse.ArgumentParser();p.add_argument('--g',default='3/100');a=p.parse_args();g=F(a.g)
    for nx,ny in [(2,2),(4,2),(4,4)]:
        bins=certify_bins(nx,ny,g)
        path=OUT/f'bilayer_{nx}x{ny}_g{g}_low_band.json'.replace('/','d')
        rec=update_certificate(json.loads(path.read_text()),bins)
        (OUT/f'bilayer_{nx}x{ny}_g{g}_number_low_band.json'.replace('/','d')).write_text(json.dumps(rec,indent=2))
if __name__=='__main__':main()
