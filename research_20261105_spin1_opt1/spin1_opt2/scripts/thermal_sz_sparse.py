#!/usr/bin/env python3
"""Per-Sz sparse Lanczos Z. NUMERICAL. Skips symmetry checks for speed."""
import os, sys, json, time, argparse, math
os.environ['OPENBLAS_NUM_THREADS']='1'; os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from scipy.sparse.linalg import eigsh
sys.path.insert(0, '/workspace/haldane_chat_bundle/runs/thermal_arb')
import blocks as B
from pathlib import Path
CACHE = Path('/workspace/haldane_chat_bundle/runs/spin1_opt2/cache'); CACHE.mkdir(parents=True, exist_ok=True)
BETA0, A = 49/4, 700741/500000

def Z_sz(L, tw, k_per=100):
    t0=time.time()
    print(f'building H L={L} {tw}...', flush=True)
    H=B.full_H(L, tw)
    print(f'H done dim={H.shape[0]} nnz={H.nnz} {time.time()-t0:.1f}s', flush=True)
    # Sz from digits without full checks
    Szv = (1 - B.digits(L)).sum(1)
    Szv = np.asarray(Szv).ravel()
    print(f'Sz ready {time.time()-t0:.1f}s', flush=True)
    total=0.0; detail=[]
    for sz in range(0, L+1):
        idx=np.flatnonzero(Szv==sz)
        if len(idx)==0: continue
        print(f'  extracting sz={sz} m={len(idx)}...', flush=True)
        Hs=H[idx][:,idx].astype(np.float64).tocsr()
        m=Hs.shape[0]
        kk=min(k_per, max(1,m-2))
        t1=time.time()
        if m <= 900:
            ev=np.linalg.eigvalsh(Hs.toarray())
        else:
            ev=eigsh(Hs, k=kk, which='SA', return_eigenvectors=False, tol=1e-8,
                     maxiter=max(3*m, 3000))
            ev=np.sort(np.real(ev))
        spin_mult=1 if sz==0 else 2
        contrib=float(spin_mult*np.exp(-BETA0*(ev+A*L)).sum())
        e_cut=float(ev[-1]+A*L)
        n_rest=m-len(ev)
        tail=spin_mult*n_rest*math.exp(-BETA0*e_cut) if (n_rest>0 and e_cut>0) else (float('inf') if n_rest>0 else 0.0)
        total+=contrib
        detail.append(dict(sz=int(sz),m=int(m),k=int(len(ev)),contrib=contrib,tail_up=float(tail),
                           Emin=float(ev[0]),Ecut=float(ev[-1]),sec_s=time.time()-t1))
        print(f'  sz={sz} m={m} k={len(ev)} c={contrib:.10g} tail={tail:.3g} {time.time()-t0:.1f}s', flush=True)
        json.dump({'partial':total,'detail':detail}, open(CACHE/f'sz_L{L}_{tw}_partial.json','w'))
    out=dict(L=L,tw=tw,Z_partial=total,Z_tail_up=sum(d['tail_up'] for d in detail),
             Z_up=total+sum(d['tail_up'] for d in detail), detail=detail,
             seconds=time.time()-t0, label='NUMERICAL')
    print(f'DONE Z_partial={total:.12g} Z_up={out["Z_up"]:.12g} in {out["seconds"]:.1f}s', flush=True)
    json.dump(out, open(CACHE/f'sz_L{L}_{tw}.json','w'), indent=2)
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--L',type=int,required=True); ap.add_argument('--tw',default='I')
    ap.add_argument('--k',type=int,default=100)
    args=ap.parse_args(); Z_sz(args.L, args.tw, k_per=args.k)
