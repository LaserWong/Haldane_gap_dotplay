import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import json,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import eigvalsh
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RES=BAND.parent

def paths(g,nx,ny):
    tag=f'{nx}x{ny}_g{g}'.replace('/','d')
    if g>=F(7,100):
        base=BAND/'frontier_g007_g010'/f'g{g}'.replace('/','d');ground=base;bins=base;old=base
    else:
        ground=BAND/'frontier_g006' if g==F(3,50) else RES/'large_seed_moments'
        bins=BAND/'quadratic_boson';old=BAND/'tail_comparison'/'quadratic'
    return ground/f'block1_{tag}.json',bins/f'quadratic_bins_{tag}.json',old/f'temple_{tag}.json'

if __name__=='__main__':
    rows=[]
    for g in map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')):
        for nx,ny in ((4,4),(8,4),(8,8)):
            gp,bp,op=paths(g,nx,ny);gr=json.loads(gp.read_text());br=json.loads(bp.read_text());old=json.loads(op.read_text())
            G,A,B=[np.array(gr[k],float) for k in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')];d=gr['integer_matrix_denominator'];A/=d;B/=d*d
            a=float(F(br['bins'][2]['lower']));rho=float(F(gr['exact_rayleigh'])-F(gr['E00']));ol=float(F(old['blocks'][0]['eigen_lower'][0]))
            scale=np.sqrt(np.diag(G));G=G/scale[:,None]/scale[None,:];A=A/scale[:,None]/scale[None,:];B=B/scale[:,None]/scale[None,:]
            K=A-a*G;S=B-2*a*A+a*a*G;mu=eigvalsh(K,S);lo=a+1/mu[0]
            row=dict(g=str(g),nx=nx,ny=ny,m=len(G),a=a,rho=rho,old_lower=ol,new_lower=lo,old_width=rho-ol,new_width=rho-lo,ratio=(rho-lo)/(rho-ol),negative_mu_count=int(sum(mu<0)))
            rows.append(row);print(json.dumps(row),flush=True)
    (HERE/'float_proposals.json').write_text(json.dumps(rows,indent=2))
