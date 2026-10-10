"""Exact directed bins for the stable boson comparison, pending review."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'bosonic_tail'))
from bosonic_number_tail import bounds


def certify(nx,ny,g,digits=40):
    g=F(g);assert 0<=g<F(1,4)
    counts,edges,v,kappa2,_,_=bounds(nx,ny,g)
    alpha=1-2*g;x=1-4*g;scale=10**digits
    k=math.isqrt(x.numerator*scale*scale//x.denominator);delta=F(k,scale)
    assert 0<delta and delta*delta<=x<(delta+F(1,scale))**2
    eb=-v/(alpha+delta);n=nx*ny;d=3*n
    bins=[dict(q=q,lower=str(eb+q*delta),multiplicity=math.comb(d+q-1,q),
       first_ordered_index=1+sum(math.comb(d+p-1,p) for p in range(q))) for q in range(n+1)]
    assert sum(row['multiplicity'] for row in bins)>=4**n
    record=dict(status='quadratic_boson_spectrum_comparison_pending_independent_review',nx=nx,ny=ny,N=n,g=str(g),
       energy_shift=str(-F(3*n,4)),bosonic_modes=d,physical_hilbert_dimension=4**n,
       weighted_edges=[[i,j,w] for (i,j),w in sorted(edges.items())],alpha=str(alpha),
       vacuum_creation_norm_squared=str(v),creation_matrix_norm_squared_upper=str(kappa2),
       delta_squared=str(x),delta_lower=str(delta),delta_upper=str(delta+F(1,scale)),
       bosonic_ground_lower=str(eb),bins=bins,
       multiplicity_status='equal-frequency oscillator reference, finite q<=N overcount; not physical number multiplicities')
    path=HERE/f'quadratic_bins_{nx}x{ny}_g{g}.json'.replace('/','d')
    path.write_text(json.dumps(record,indent=2));print(nx,ny,g,[float(F(x['lower'])) for x in bins[:3]],flush=True)
    return record


if __name__=='__main__':
    for g in map(F,('3/100','1/25','1/20','3/50')):
        for nx,ny in ((4,4),(8,4),(8,8)):certify(nx,ny,g)
