# Independent verifier: Z12(49/4) and sup_b Z12(2b)^(4/3)/Z8(b)^4 from enc/L{8,12}_*.json (my own blocks + cert_core).
# Enclosure per stored value lt=Lint/2^30 (exact dyadic): |mu - lt| <= eta_up*|lt| + delta_up.
import json, glob, sys, time
from pathlib import Path
from flint import arb, fmpq
import numpy as np, scipy.sparse as sp
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from indep_blocks import full_H
t0 = time.time()
a = fmpq(700741, 500000); b0 = fmpq(49, 4)
def mult(sz, k, L): return (1 if sz == 0 else 2) * (1 if k in (0, L // 2) else 2)
def load(L):
    recs = [json.load(open(f)) for f in glob.glob(str(HERE / 'enc' / f'L{L}_*_*.json'))]
    keys = {(r['sz'], r['k']) for r in recs}
    assert keys == {(s, k) for s in range(L + 1) for k in range(L // 2 + 1)}, ('missing', L)
    E = []  # (lo, hi, mult) as fmpq
    dim = 0; tr = arb(0); fr = arb(0)
    for r in recs:
        mu = mult(r['sz'], r['k'], L)
        if r['m'] == 0: continue
        lint = r['Lint']; assert len(lint) == r['m']
        eu = fmpq(*float(r['eta_up']).as_integer_ratio()); du = fmpq(*float(r['delta_up']).as_integer_ratio())
        # eta_up/delta_up = up_float(ball) in cert_core (rigorous); the decimal strings are display-only, cross-checked loosely
        assert arb(r['eta']).upper() <= arb(eu) * (1 + 1e-12) and arb(r['delta']).upper() <= arb(du) * (1 + 1e-12)
        assert eu < fmpq(1, 10**6) and du < fmpq(1, 10**5)
        for x in lint:
            lt = fmpq(int(x), 2**30); rad = eu * abs(lt) + du
            E.append((lt - rad, lt + rad, mu))
        dim += mu * r['m']; tr += mu * arb(r['trace']); fr += mu * arb(r['frob2'])
    assert dim == 3**L, (L, dim)
    return E, tr, fr
def exact_moments(L):
    H = full_H(L).astype(np.int64).tocsr()
    t1 = int(H.diagonal().sum()); t2 = int(H.multiply(H.T).sum())
    H2 = H @ H; t3 = int(H2.multiply(H.T).sum())
    return t1, t2, t3
def enc_moment(E, j):
    s = arb(0)
    for lo, hi, mu in E:   # flint x**j on a ball straddling 0 can give nan (seen before): multiply explicitly
        x = arb(lo).union(arb(hi)); p = arb(1)
        for _ in range(j): p = p * x
        s += mu * p
    assert s.is_finite()
    return s
res = {}
for L in (8, 12):
    E, tr, fr = load(L); ex = exact_moments(L)
    ms = [enc_moment(E, j) for j in (1, 2, 3)]
    ok = [m.contains(e) for m, e in zip(ms, ex)] + [tr.contains(ex[0]), fr.contains(ex[1])]
    print('L', L, 'n_enc', len(E), 'dim', 3**L, 'exact TrH^j', ex, 'enclosed', [m.str(8) for m in ms], 'contain', ok, flush=True)
    assert all(ok)
    res[L] = E
E12, E8 = res[12], res[8]
Z = sum((mu * (-arb(b0) * (arb(lo) + 12 * arb(a))).exp() for lo, hi, mu in E12), arb(0))
print('(1) Z12(49/4) <=', Z.upper().str(15), ' (old cert 1.90055706558595)')
# (2) sup_b: dyadic bins width 2^-9, outward
w = fmpq(1, 512)
def bins(E, L, low):
    d = {}
    for lo, hi, mu in E:
        u = (lo if low else hi) + L * a
        j = (u / w).floor() if low else (u / w).ceil()
        j = int(j); d[j] = d.get(j, 0) + mu
    return sorted(d.items())
X = bins(E12, 12, True); Y = bins(E8, 8, False)
def fup(b1, b2):
    B = arb(b1).union(arb(b2))
    num = sum((c * (-2 * B * arb(j * w)).exp() for j, c in X), arb(0))
    den = sum((c * (-B * arb(j * w)).exp() for j, c in Y), arb(0))
    dl = den.lower(); assert dl > 0
    return ((num.upper()).log() * fmpq(4, 3) - 4 * dl.log()).exp().upper()
BMAX = 80; todo = [(fmpq(i, 4), fmpq(i + 1, 4)) for i in range(4 * BMAX)]; worst = arb(0); wi = None; n = 0
while todo:
    b1, b2 = todo.pop(); f = fup(b1, b2); n += 1
    if f >= arb(fmpq(1, 10)) and b2 - b1 > fmpq(1, 4096): m = (b1 + b2) / 2; todo += [(b1, m), (m, b2)]; continue
    if f > worst: worst, wi = f, (b1, b2)
x0 = X[0][0] * w; y0 = Y[0][0] * w   # min shifted lower (L12), min shifted upper (L8) -> ground state bin
c = -fmpq(8, 3) * x0 + 4 * y0
tail = (arb(fmpq(4, 3)) * arb(3**12).log() + BMAX * arb(c)).exp()
print('(2) sup over b in [0,%d] <= %s at [%s,%s], %d intervals; tail slope c=%s, f(b>=%d) <= %s'
      % (BMAX, worst.str(8), wi[0], wi[1], n, float(c), BMAX, tail.str(4)))
assert c < 0 and tail < arb(fmpq(1, 2)) and worst < arb(fmpq(1, 2))
print('    => sup_{b>0} W8-bound <=', max(worst, tail, key=float).str(8), '< 1/2  (old cert 0.100397)', ' time %.0fs' % (time.time() - t0))
