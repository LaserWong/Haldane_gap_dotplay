# Assemble rigorous arb enclosures  Z_L = sum_blocks mult * sum_i exp(-beta (mu_i + a L)),  mu_i in [lt_i -+ err_i]
# beta = 64, a = 4761248/10^6 (exact rationals).  key 'Z' = untwisted ring, 'P' = pi-seam ring.
# Checks: block dims*mult = 5^L and per-Sz sector dims; enclosed power sums contain exact Tr H and Tr H^2
# (exact: Tr A, Tr A^2 + 6 Tr B^2 + 2 sqrt6 Tr AB from the integer sparse matrices, H = A + sqrt6 B).
import sys, os, json, math, flint
from flint import arb, fmpq
flint.ctx.prec = 256
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from blocks2 import q_values, full_H
beta = arb(64); a = arb(fmpq(4761248, 10**6))
out = {}
fn = f'{D}/enclosures.json'; old = json.load(open(fn)) if os.path.exists(fn) else {}
for L in [int(x) for x in sys.argv[1:]]:
    for tw in 'ZP':
        need = [(sz, q) for sz in range(2 * L + 1) for q, _ in q_values(L, tw, sz)]
        recs = [json.load(open(f'{D}/enc/{tw}_L{L}_sz{sz}_q{q}.json')) for sz, q in need]
        Z = arb(0); dim = 0; P1 = arb(0); P2 = arb(0); modes = {}; maxerr = 0.0; secdim = {}
        for r in recs:
            assert all(r['checks'].values())
            mu = r['mult']; dim += mu * r['m']; secdim.setdefault(r['sz'], [r['sector_dim'], 0])
            secdim[r['sz']][1] += r['m'] * (mu // (2 if r['sz'] > 0 else 1))
            modes[r['mode']] = modes.get(r['mode'], 0) + 1
            for lt, e in zip(r['lt'], r['err_up']):
                x = (arb(int(lt)) * arb(2)**(-r['SH'])) if r['SH'] else arb(float.fromhex(lt))
                ball = arb(x, arb(e)); maxerr = max(maxerr, e)
                Z += mu * (-(beta * (ball + a * L))).exp(); P1 += mu * ball; P2 += mu * ball * ball
        assert dim == 5**L and all(v[0] == v[1] for v in secdim.values()), (L, tw, dim, secdim)
        A, B = full_H(L, tw)
        t1 = int(A.diagonal().sum()); assert B.diagonal().sum() == 0
        tAA = int(A.multiply(A).sum()); tBB = int(B.multiply(B).sum()); tAB = int(A.multiply(B).sum())   # Tr(XY)=sum X_ij Y_ji, X,Y symmetric
        t2 = arb(tAA + 6 * tBB) + 2 * arb(6).sqrt() * tAB
        mcheck = bool(P1.contains(t1) and P2.overlaps(t2))
        lo = Z.lower(); hi = Z.upper()
        # rational outward endpoints (25 significant digits, rounded outward)
        def rat(x, up):
            s = arb(x).mid(); e = int(math.floor(float(arb(x).log().mid()) / math.log(10))) - 30
            q = fmpq(10)**(-e) if e < 0 else fmpq(1, 10**e)
            n = (arb(x) * arb(q)); n = n.upper().ceil() if up else n.lower().floor()
            return fmpq(int(n.unique_fmpz()), 1) / q
        rlo = rat(lo, False); rhi = rat(hi, True)
        assert arb(rlo) <= lo and arb(rhi) >= hi and rlo > 0
        key = f'{tw}{L}'
        out[key] = dict(lo=str(rlo), hi=str(rhi), log_mid=float(Z.log().mid()), rel_radius=float((Z.rad() / Z.mid()).upper()),
                        moments_contain_exact=mcheck, TrH=t1, max_eig_err=maxerr, blocks_by_mode=modes, n_blocks=len(recs))
        print(key, 'log Z in', float(arb(rlo).log().mid()), float(arb(rhi).log().mid()), 'relrad %.2e' % out[key]['rel_radius'], 'mom', mcheck, modes, flush=True)
old.update(out); json.dump(old, open(fn, 'w'), indent=1)
