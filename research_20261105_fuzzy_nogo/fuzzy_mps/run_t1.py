"""T1 driver.  usage: python3 run_t1.py tebd|ladder L chi     (chi = 0 means no truncation)
Writes results/<mode>_L<L>_chi<chi>.json.  Ladder: tau_k = TAU0*2^k, TAU0 = 49/256, k=0..6 (tau_5 = beta/2, tau_6 = beta,
beta = 49/4).  Z(2 tau_k) = ||E_k||_F^2.
eta_true: RIGOROUS (arb ladder + IEEE standard-model float Frobenius; see pipeline.py).
a-priori bounds: computed only from pipeline quantities (measured truncation errors eps, ||Y||_F, rounding) plus an
energy lower bound e0_lb (per site) used for ||E||_op <= exp(-tau L (e0_lb + c)).  Variants:
  'bond'  : e0_lb = -2 (bond-wise bound; = product of gate norms)            non-circular, trivially scalable
  'anders': e0_lb = best Anderson cluster bound with m <= L (FLOAT)          non-circular, scalable (local ED)
  'exact' : e0_lb = exact E0(L)/L (FLOAT)                                     ORACLE, circular at scale
  'fro'   : (ladder only) ||E||_op <= ||Y||_F + delta, ||Y||_op <= ||Y||_F    non-circular, no energy input"""
import sys, os, json, time, numpy as np
from pipeline import *
mode, L, chi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); chi = chi or None
n = 3**L; tau0 = float(TAU0); c = float(C_SHIFT); u = 2.0**-53; gam_n = n * u / (1 - n * u)
And = json.load(open(f'{D}/anderson.json'))
e0lb = {'bond': -2.0, 'anders': max(v['bound_per_site'] for m, v in And['open'].items() if int(m) <= L),
        'exact': And['ring'][str(L)] / L * (1 + 1e-9)}
opE = lambda tau, e: np.exp(-tau * L * (e + c))       # upper bound on ||exp(-tau(H+cL))||_op given e0 >= e*L
os.makedirs(f'{D}/results', exist_ok=True); out_fn = f'{D}/results/{mode}_L{L}_chi{chi or 0}.json'
t0 = time.time()
ucache = f'{D}/cache/U_L{L}.npy'
if os.path.exists(ucache): U = np.load(ucache)
else:
    U, _, _ = tebd(L, tau0 / 64, None, 1)          # one Strang step, dt = TAU0/64
    for _ in range(6): U = U @ U                     # U = (Strang step)^64 ~ exp(-TAU0 (H+cL))
    np.save(ucache, U)
etaU, _ = eta_true(U, L, 0); etaU += gam_n * fro(U)**2 * 6   # (rounding of the 6 float squarings, crude)
res = dict(L=L, chi=chi, mode=mode, tau0=tau0, e0lb=e0lb, etaU_trotter_chunk=etaU, rows=[])
def zrow(Y, k, deltas):
    eta, Zex = eta_true(Y, L, k); r = dict(k=k, tau=tau0 * 2**k, eta_true=eta, Z_exact=Zex.str(20))
    lo, hi, nY = Zbounds(Y, eta); r.update(normY=nY, Z_lo_true=lo, Z_hi_true=hi)
    for v, dlt in deltas.items():
        lo, hi, _ = Zbounds(Y, dlt); r[f'delta_{v}'] = dlt; r[f'Z_lo_{v}'] = lo; r[f'Z_hi_{v}'] = hi
    return r
if mode == 'tebd':
    # 64 chunks of TAU0; truncate after each chunk.  delta_j <= eps_j + nu delta_{j-1} + etaU ||E_{j-1}||_op
    Y = np.eye(n); dl = {v: 0.0 for v in e0lb}; eps_all = []
    NCH = int(os.environ.get('TEBD_CHUNKS', '64'))
    for j in range(1, NCH + 1):
        P = U @ Y; rnd = gam_n * fro(U) * fro(Y)
        if chi: Y, e = truncate(P, L, chi)
        else: Y, e = P, 0.0
        e += rnd; eps_all.append(e)
        for v, ev in e0lb.items():
            nu = min(opE(tau0, ev) + etaU, np.exp(tau0 * L * (2 - c)))
            dl[v] = e + nu * dl[v] + etaU * opE((j - 1) * tau0, ev)
        if j in (1, 2, 4, 8, 16, 32, 64) or j == NCH:
            k = int(np.log2(j)); r = zrow(Y, k, dict(dl)); r['eps_max'] = max(eps_all); res['rows'].append(r)
            print(json.dumps({a: (b if not isinstance(b, float) else float('%.4g' % b)) for a, b in r.items()}), '%.0fs' % (time.time() - t0), flush=True)
elif mode == 'ladder':
    # Y_0 = trunc(U) ~ E_0 ; Y_{k+1} = trunc(Y_k^2).  delta_{k+1} <= eps_{k+1} + rnd + (||Y_k||_op + ||E_k||_op) delta_k
    if chi: Y, e = truncate(U, L, chi)
    else: Y, e = U.copy(), 0.0
    d0, _ = eta_true(Y, L, 0)                      # certified first step vs EXACT exp(-TAU0 H) (A3a-type input)
    dl = {v: d0 for v in list(e0lb) + ['fro']}
    r = zrow(Y, 0, dict(dl)); r['eps'] = e; res['rows'].append(r); print(json.dumps(r), flush=True)
    for k in range(1, K + 1):
        nYF = fro(Y); P = Y @ Y; rnd = gam_n * nYF**2
        if chi: Yn, e = truncate(P, L, chi)
        else: Yn, e = P, 0.0
        new = {}
        for v in dl:
            if v == 'fro': fac = 2 * nYF + dl[v]
            else:
                oE = min(opE(tau0 * 2**(k - 1), e0lb[v]), nYF + dl[v]); fac = min(2 * oE + dl[v], 2 * nYF + dl[v])
            new[v] = e + rnd + fac * dl[v]
        dl = new; Y = Yn
        r = zrow(Y, k, dict(dl)); r['eps'] = e + rnd; res['rows'].append(r)
        print(json.dumps({a: (b if not isinstance(b, float) else float('%.4g' % b)) for a, b in r.items()}), '%.0fs' % (time.time() - t0), flush=True)
json.dump(res, open(out_fn, 'w'), indent=1)
