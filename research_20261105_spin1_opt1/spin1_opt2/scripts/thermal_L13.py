#!/usr/bin/env python3
"""Float Z for one (L,tw) via Sz+Bloch. NUMERICAL."""
import os, sys, json, time, argparse
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
sys.path.insert(0, '/workspace/haldane_chat_bundle/runs/thermal_arb')
import blocks as B
from pathlib import Path
CACHE = Path('/workspace/haldane_chat_bundle/runs/spin1_opt2/cache')
CACHE.mkdir(parents=True, exist_ok=True)
BETA0, A = 49/4, 700741/500000

def Z_L(L, tw, beta=BETA0, a=A):
    H = B.full_H(L, tw)
    T, s = B.twisted_translation(L, tw)
    F = B.flip(L)
    chk, Szv = B.checks(L, tw, H, T, s, F)
    assert chk['H_symmetric']
    total = 0.0
    detail = []
    for sz in range(0, L+1):
        t0 = time.time()
        sd = B.sector_data(L, H, T, s, Szv, sz)
        sec_sum = 0.0
        for q, mult_q in B.q_values(L, tw, sz):
            m, ent, Hf, real = B.block(L, q, sd)
            if m == 0:
                continue
            if real:
                Hf = np.real(Hf)
                Hf = 0.5 * (Hf + Hf.T)
                ev = np.linalg.eigvalsh(Hf)
            else:
                Hf = 0.5 * (Hf + Hf.conj().T)
                ev = np.linalg.eigh(Hf, UPLO='L')[0].real
            spin_mult = 1 if sz == 0 else 2
            contrib = float(spin_mult * mult_q * np.exp(-beta * (ev + a * L)).sum())
            sec_sum += contrib
            detail.append({'sz': int(sz), 'q': int(q), 'm': int(m), 'contrib': contrib})
        print(f'  sz={sz} dim={sd["dim"]} sum={sec_sum:.12g} {time.time()-t0:.1f}s', flush=True)
        total += sec_sum
        json.dump({'partial_Z': total, 'detail': detail}, open(CACHE/f'L{L}_{tw}_partial.json','w'))
    return total, detail

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', type=int, default=13)
    ap.add_argument('--tw', default='I')
    args = ap.parse_args()
    # validate L=10
    if args.L == 10:
        pass
    t0 = time.time()
    Z, detail = Z_L(args.L, args.tw)
    print(f'Z L={args.L} {args.tw} = {Z} in {time.time()-t0:.1f}s')
    json.dump({'Z': Z, 'detail': detail, 'seconds': time.time()-t0, 'label': 'NUMERICAL'},
              open(CACHE/f'thermal_L{args.L}_{args.tw}.json', 'w'), indent=2)
