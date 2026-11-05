"""RIGOROUS (arb) exact ladder E_k = exp(-tau_k (H + cL)), tau_k = TAU0*2^k, k=0..K, per Sz block.
E_0 by arb_mat.exp; E_{k+1} = E_k^2 in arb.  Saves per block: float64 midpoints and a rigorous entrywise bound
err >= |E_true - float(mid)| (rad + |mid - float(mid)|), plus arb strings of Z(2 tau_k) = ||E_k||_F^2 per block.
usage: python3 exact_arb.py L M   (M >= 0; M<0 obtained by the spin flip, which maps H_M to H_{-M} exactly)"""
import sys, os, json, time, numpy as np
from common import *
from flint import arb_mat, arb, ctx
ctx.prec = 192
L, M = int(sys.argv[1]), int(sys.argv[2])
out = f'{D}/cache/E_L{L}_M{M}.npz'
if os.path.exists(out): sys.exit()
os.makedirs(f'{D}/cache', exist_ok=True)
st, Hi = Hblock_int(L, M); m = len(st); t0 = time.time()
tau0 = arb(TAU0.numerator) / TAU0.denominator; c = arb(C_SHIFT.numerator) / C_SHIFT.denominator
A = arb_mat(Hi.tolist()) * (-tau0)
E = A.exp() * (-tau0 * c * L).exp()
mids, errs, Zs = [], [], []
for k in range(K + 1):
    if k: E = E * E
    mid = np.array([[float(E[i, j].mid()) for j in range(m)] for i in range(m)])
    # rigorous entrywise bound: rad + |mid - fl(mid)| <= rad + ulp(|fl(mid)|) ; take max over entries
    rad = max(float(E[i, j].rad()) for i in range(m) for j in range(m))
    err = rad * (1 + 1e-12) + np.spacing(np.abs(mid)).max() + 1e-300
    fro2 = arb(0)
    for i in range(m):
        for j in range(m): fro2 += E[i, j] ** 2
    mids.append(mid); errs.append(err); Zs.append(fro2.str(30, radius=True))
    print(L, M, k, m, 'maxrad %.2e' % rad, 'Zpart', fro2.str(12), '%.1fs' % (time.time() - t0), flush=True)
np.savez(out + '.tmp.npz', st=st, mids=np.array(mids), errs=np.array(errs), Zs=np.array(Zs))
os.replace(out + '.tmp.npz', out)
