#!/usr/bin/env python3
"""Re-optimize n, a (and report beta0 needs new thermal). NUMERICAL/HEURISTIC."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_core import (
    load_repo_moments, load_long, load_R68, hankel_caps, seed_from_moments,
    chain_max_gamma, window_C, BETA0, A_SHIFT, CUR_GAMMA, TARGET, pack
)

CACHE = Path('/workspace/haldane_chat_bundle/runs/spin1_opt2/cache')
CACHE.mkdir(parents=True, exist_ok=True)

def eval_cfg(mj, mn, U, V, Mdeg, n, a, beta0, R, longB, full=True, label=''):
    # seed_from_moments does not take `a` — a enters only via R68 and moments
    # (moments already include e^{-beta(E+aL)}). Changing `a` without new moments
    # is INVALID for S,T from thermal. We still sweep `a` only as HEURISTIC note
    # that recipe a is locked to the moment definition.
    sd = seed_from_moments(mj, mn, U, V, Mdeg, n, beta0, R, longB, full=full)
    if sd is None:
        return dict(label=label, n=n, a=a, beta0=beta0, gamma=0.0, C0=0.0, ok=False)
    g, C0 = chain_max_gamma(sd['S'], sd['T'], n=n, beta0=beta0, W=24)
    return dict(label=label, n=n, a=a, beta0=beta0, S=sd['S'], T=sd['T'],
                K=sd['K'], ell=sd['ell'], rem=sd['rem'], gamma=g, C0=C0,
                ratio=g/CUR_GAMMA, ok=True)

def main():
    M, caps_repo, Crow = load_repo_moments()
    longB = load_long()
    R = load_R68()
    mj = M['J'][-1][1]; mn = M['N'][-1][1]
    mj_mid = 0.5*(M['J'][-1][0]+M['J'][-1][1])
    mn_mid = 0.5*(M['N'][-1][0]+M['N'][-1][1])
    U = max(caps_repo['J+'], caps_repo['J-'])
    V = max(caps_repo['N+'], caps_repo['N-'])
    mids = {s: [0.5*(lo+hi) for lo,hi in rows] for s,rows in M.items()}
    errs0 = {s: [0.0]*len(rows) for s,rows in M.items()}
    ideal_caps = hankel_caps(mids, errs0)
    Ui = max(ideal_caps['J+']['cap'], ideal_caps['J-']['cap'])
    Vi = max(ideal_caps['N+']['cap'], ideal_caps['N-']['cap'])
    print(f'repo U={U} V={V}; ideal U={Ui} V={Vi}; R={R}', flush=True)

    results = []
    # Baseline
    r = eval_cfg(mj, mn, U, V, 12, 34, A_SHIFT, BETA0, R, longB, label='baseline')
    results.append(r); print('baseline', r['gamma'], r['C0'], flush=True)

    # Ideal L<=12
    r = eval_cfg(mj_mid, mn_mid, Ui, Vi, 12, 34, A_SHIFT, BETA0, R, longB, label='ideal_L12')
    results.append(r); print('ideal_L12', r['gamma'], r['C0'], flush=True)

    # Ideal without long_bounds (pure packing)
    r = eval_cfg(mj_mid, mn_mid, Ui, Vi, 12, 34, A_SHIFT, BETA0, R, None, label='ideal_L12_no_long')
    results.append(r); print('ideal_no_long', r['gamma'], flush=True)

    # n sweep with repo caps
    for n in range(24, 56, 2):
        r = eval_cfg(mj, mn, U, V, 12, n, A_SHIFT, BETA0, R, longB, label=f'n{n}_repo')
        results.append(r)
        print(f'n={n} repo g={r["gamma"]:.8f} C0={r["C0"]:.5f} S={r.get("S",0):.5f} T={r.get("T",0):.5f}', flush=True)

    # n sweep ideal
    for n in range(24, 56, 2):
        r = eval_cfg(mj_mid, mn_mid, Ui, Vi, 12, n, A_SHIFT, BETA0, R, longB, label=f'n{n}_ideal')
        results.append(r)

    # Mdeg variation: pretend we have moments only up to M (truncate)
    # Using midpoints of available moments length M as mj = J[M-1]
    for Mdeg in [6, 8, 10, 12]:
        mjM = 0.5*(M['J'][Mdeg-1][0]+M['J'][Mdeg-1][1])
        mnM = 0.5*(M['N'][Mdeg-1][0]+M['N'][Mdeg-1][1])
        # recompute caps on truncated moments
        midsM = {s: mids[s][:Mdeg] for s in mids}
        errsM = {s: [0.0]*Mdeg for s in mids}
        capsM = hankel_caps(midsM, errsM, degree=min(5, (Mdeg+1)//2))
        UM = max(capsM['J+']['cap'], capsM['J-']['cap'])
        VM = max(capsM['N+']['cap'], capsM['N-']['cap'])
        r = eval_cfg(mjM, mnM, UM, VM, Mdeg, 34, A_SHIFT, BETA0, R, longB, label=f'Mdeg{Mdeg}_ideal')
        results.append(r)
        print(f'Mdeg={Mdeg} U={UM:.6f} V={VM:.6f} g={r["gamma"]:.8f}', flush=True)

    # Synthetic L=13,14: extrapolate J_L, N_L from ratio of last terms
    # J_L ~ (Z_L + 3 P_L)/4. From mids, L=4..12.
    JL = [0.5*(lo+hi) for lo,hi in M['J']]
    NL = [0.5*(lo+hi) for lo,hi in M['N']]
    # Ls corresponding: certificate moments are for L=4..12? Check length
    # Actually moment_intervals J has 9 entries for L=4..12
    print('len J moments', len(JL), 'values', JL, flush=True)
    # Fit log|J_L| ~ c - L/xi or just ratio
    # Use geometric extension: J_{L+1}/J_L ≈ J_L/J_{L-1}
    def extend(seq, n_extra):
        s = list(seq)
        for _ in range(n_extra):
            if len(s) < 2 or s[-2] == 0:
                s.append(s[-1])
            else:
                ratio = s[-1]/s[-2]
                # damp toward asymptotic |ratio|->e^{-something}; clamp
                ratio = max(0.3, min(2.5, ratio))
                s.append(s[-1]*ratio)
        return s

    # Also try transfer: in Haldane phase free energy f, Z~ e^{-beta (e0+a) L} * ...
    # J_L should approach something related to transfer eigenvalue.
    # HEURISTIC synthetic M=14 moments
    J14 = extend(JL, 2)
    N14 = extend(NL, 2)
    print('synth J14', J14[-3:], 'N14', N14[-3:], flush=True)
    mids14 = {'J': J14, 'N': N14}
    errs14 = {'J': [0.0]*14, 'N': [0.0]*14}
    # For Mdeg=14 need 14 moments (indices 0..13 = L=4..17? WAIT
    # Looking at certificate: moment_intervals J rows are for powers/L?
    # In improve.py / explore: moments[k] is for length related to filter degree.
    # Check certificate structure
    print('moment note: using extended midpoints as if L=4..15', flush=True)
    caps14 = hankel_caps(mids14, errs14, degree=5)
    U14 = max(caps14['J+']['cap'], caps14['J-']['cap'])
    V14 = max(caps14['N+']['cap'], caps14['N-']['cap'])
    mj14, mn14 = J14[-1], N14[-1]
    r = eval_cfg(mj14, mn14, U14, V14, 14, 34, A_SHIFT, BETA0, R, longB, label='synth_M14_n34')
    results.append(r)
    print(f'synth M14 n34 U={U14:.6f} g={r["gamma"]:.8f}', flush=True)
    for n in range(28, 52, 2):
        r = eval_cfg(mj14, mn14, U14, V14, 14, n, A_SHIFT, BETA0, R, longB, label=f'synth_M14_n{n}')
        results.append(r)

    # Optimistic: perfect U=1.0, V=0.87, mj=1.0+eps (almost pure), mn small
    for mj_o, U_o, lab in [
        (1.001, 1.0001, 'opt_U1.0001'),
        (1.0001, 1.00001, 'opt_U1.00001'),
        (1.05, 1.001, 'opt_mild'),
        (mj_mid, 1.0, 'opt_U1_real_mj'),
    ]:
        r = eval_cfg(mj_o, mn_mid, U_o, Vi, 12, 34, A_SHIFT, BETA0, R, longB, label=lab)
        results.append(r)
        print(f'{lab} g={r["gamma"]:.8f} S={r.get("S")} T={r.get("T")}', flush=True)

    # beta0 sweep HEURISTIC with FIXED moments (invalid physically but shows chain sensitivity)
    for b in [8., 10., 12., 12.25, 14., 16., 20.]:
        r = eval_cfg(mj, mn, U, V, 12, 34, A_SHIFT, b, R, longB, label=f'beta0_{b}_HEURISTIC')
        results.append(r)
        print(f'beta0={b} (moments@12.25) g={r["gamma"]:.8f}', flush=True)

    ok = [x for x in results if x.get('ok')]
    top = sorted(ok, key=lambda x: -x['gamma'])[:20]
    summary = {
        'label': 'NUMERICAL/HEURISTIC',
        'certified_gamma': CUR_GAMMA,
        'target_1p5x': TARGET,
        'best': top[0],
        'top20': top,
        'warrant_cert': bool(top[0]['gamma'] >= TARGET),
        'n_results': len(results),
        'note_a': 'a is locked into thermal definition; sweeping a without new Z is invalid — not done as primary',
        'note_beta0': 'beta0 sweep with frozen moments is HEURISTIC only; real reopt needs new thermal at each beta0',
    }
    json.dump(summary, open(CACHE/'reopt.json','w'), indent=2)
    json.dump(results, open(CACHE/'reopt_all.json','w'))
    print('\n=== SUMMARY ===')
    print(json.dumps({k: summary[k] for k in ['best','warrant_cert','target_1p5x']}, indent=2, default=str))

if __name__ == '__main__':
    main()
