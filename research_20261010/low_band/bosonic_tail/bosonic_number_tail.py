"""Exact bosonic/occupancy comparison for whole-spectrum number bins."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,math,time
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'translation_band'))
import large_refined_pipeline as P
import number_sector_tail as NT


def bounds(nx,ny,g):
    g=F(g);assert nx>=2 and ny>=2 and 0<=g<F(1,2)
    n=nx*ny;edges=defaultdict(int);index=lambda x,y:(x%nx)*ny+y%ny
    for x in range(nx):
        for y in range(ny):
            i=index(x,y)
            for j in (index(x+1,y),index(x,y+1)):edges[tuple(sorted((i,j)))]+=1
    assert all(i!=j for i,j in edges)
    assert [sum(w for e,w in edges.items() if i in e) for i in range(n)]==[4]*n
    v=F(3,4)*g*g*sum(w*w for w in edges.values());kappa2=4*g*g
    old=P.iso_counts(nx,ny)
    occupancy=[F(3,4)*g*g*old['empty_edge_max'][q]*old['occupied_edge_max'][q+2] for q in range(n-1)]
    bosonic=[(q//2+1)*v+kappa2*((q+1)**2//4) for q in range(n-1)]
    return old,edges,v,kappa2,occupancy,bosonic


def certify(nx,ny,g):
    start=time.monotonic();g=F(g);n=nx*ny
    counts,edges,v,kappa2,occ,bos=bounds(nx,ny,g)
    diag=[(1-2*g)*q for q in range(n+1)];off2=[min(a,b) for a,b in zip(occ,bos)];bins=[]
    for q in range(n+1):
        parts=[]
        for startq in (q,q+1):
            if startq>n:continue
            inds=list(range(startq,n+1,2))
            lo,piv=NT.tridiagonal_lower([diag[j] for j in inds],[off2[j] for j in inds[:-1]])
            parts.append(dict(number_indices=inds,lower=str(lo),ldl_positive_pivots=piv))
        lo=min(F(p['lower']) for p in parts)
        if q:lo=max(lo,F(bins[-1]['lower']))
        bins.append(dict(q=q,lower=str(lo),multiplicity=math.comb(n,q)*3**q,
          first_ordered_index=1+sum(math.comb(n,j)*3**j for j in range(q)),parity_compressions=parts))
    record=dict(status='bosonic_number_tail_candidate_pending_independent_review',nx=nx,ny=ny,N=n,g=str(g),
      energy_shift=str(-F(3*n,4)),graph_counts=counts,weighted_edges=[[i,j,w] for (i,j),w in sorted(edges.items())],
      local_certificate=NT.local_check(),vacuum_creation_norm_squared=str(v),creation_matrix_norm_squared_upper=str(kappa2),
      diagonal=list(map(str,diag)),occupancy_offdiagonal_squared=list(map(str,occ)),
      bosonic_offdiagonal_squared=list(map(str,bos)),offdiagonal_squared=list(map(str,off2)),bins=bins,
      seconds=time.monotonic()-start)
    (HERE/f'bosonic_bins_{nx}x{ny}_g{g}.json'.replace('/','d')).write_text(json.dumps(record,indent=2))
    print(nx,ny,g,[float(F(x['lower'])) for x in bins[:3]],flush=True)
    return record


if __name__=='__main__':
    for g in map(F,('3/100','1/25','1/20','3/50')):
        for nx,ny in ((4,4),(8,4),(8,8)):certify(nx,ny,g)
