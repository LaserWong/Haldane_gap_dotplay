"""Only lowest eigenpairs in the total-Sz=0 block for open higher-spin AKLT chains.
SU(2) symmetry puts every integer total-spin multiplet in this block.
These are floating-point diagnostics, not certified lower bounds.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import scipy.linalg as la
from scipy.sparse.linalg import eigsh,lobpcg
from threadpoolctl import threadpool_limits
from numerics import local,sectors,block
OUT=Path(__file__).resolve().parents[1]/'results'

def run(s,L):
    h=local(s,kind='aklt')
    bonds=np.ones(L)
    bonds[-1]=0
    rows=[]
    all_pos=[]
    nzero=0
    residual=0
    for M,ids,dig,pw in sectors(s,L):
        if M!=0:
            continue
        H=block(s,L,ids,dig,pw,h,bonds)
        k=min(H.shape[0],max(s-M+1,0)+3)
        if H.shape[0]<=max(400,k+2):
            e,v=la.eigh(H.toarray(),subset_by_index=[0,k-1],check_finite=False)
        else:
            X=np.random.default_rng(7+M).normal(size=(H.shape[0],k))
            e,v=lobpcg(H,X,largest=False,tol=2e-10,maxiter=1500)
            order=np.argsort(e)
            e,v=e[order],v[:,order]
        er=float(np.linalg.norm(H@v-v*e,axis=0).max())
        residual=max(residual,er)
        zeros=int(np.sum(abs(e)<1e-8))
        nzero+=zeros*(1 if M==0 else 2)
        assert zeros==max(s-M+1,0), (s,L,M,e)
        pos=e[e>1e-8]
        if len(pos):
            all_pos.append(float(pos[0]))
        rows.append(dict(M=M,block_dimension=H.shape[0],lowest_eigenvalues=e.tolist(),max_residual=er))
    assert nzero==s+1
    gap=min(all_pos)
    kn=1/(L-1)
    gm=6/(L*(L+1))
    row=dict(s=s,L=L,local_projectors=f'sum_(J={s+1})^{2*s} P_J',
             dimension=(2*s+1)**L,ground_space_dimension=(s+1)**2,M0_zero_count=nzero,gap=gap,
             knabe_threshold=kn,gosset_mozgunov_threshold=gm,
             passes_Knabe_float=gap>kn,passes_GM_float=gap>gm,
             max_residual=residual,blocks=rows,status='floating_low_spectrum_diagnostic')
    (OUT/f'aklt_s{s}_L{L}.json').write_text(json.dumps(row,indent=2))
    print({k:v for k,v in row.items() if k!='blocks'},flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('s',type=int)
    a.add_argument('lengths',type=int,nargs='+')
    args=a.parse_args()
    with threadpool_limits(limits=1):
        for L in args.lengths:
            run(args.s,L)
