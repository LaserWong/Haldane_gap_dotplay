# usage: python3 run_enclose.py L sz1 sz2 ...  ; writes enc/L{L}_{sz}_{k}.json per block (resume-safe)
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb
from indep_blocks import full_H, translation, flip, checks, sector_data, block
from cert_core import certify, up_float
L = int(sys.argv[1]); szs = [int(x) for x in sys.argv[2:]]
t0 = time.time()
H = full_H(L); T = translation(L); F = flip(L)
chk, Szv = checks(L, H, T, F)
print('L', L, 'nnz', H.nnz, 'checks', chk, flush=True)
assert all(v is True for v in chk.values() if isinstance(v, bool))
json.dump({k: v for k, v in chk.items()}, open(f'enc/checks_L{L}.json', 'w'))
for sz in szs:
    reps, per, coef, dim = sector_data(L, H, T, Szv, sz)
    for k in range(L // 2 + 1):
        fn = f'enc/L{L}_{sz}_{k}.json'
        if os.path.exists(fn): continue
        m, ent, Hf, real = block(L, k, reps, per, coef)
        rec = dict(L=L, sz=sz, k=k, m=m, sector_dim=dim, real=real)
        if m > 0:
            Lint, eta, delta = certify(Hf, ent, arb(2 * L))
            tr = sum((ent[(q, q)].real for q in range(m) if (q, q) in ent), arb(0))
            fr = sum((v.real * v.real + v.imag * v.imag for v in ent.values()), arb(0))
            rec.update(Lint=Lint, SL=30, eta_up=up_float(eta), delta_up=up_float(delta),
                       eta=eta.str(radius=True), delta=delta.str(radius=True),
                       trace=tr.str(20, radius=True), frob2=fr.str(20, radius=True))
        json.dump(rec, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
        print(L, sz, k, m, rec.get('eta_up'), rec.get('delta_up'), round(time.time() - t0), flush=True)
print('done', szs, round(time.time() - t0), flush=True)
