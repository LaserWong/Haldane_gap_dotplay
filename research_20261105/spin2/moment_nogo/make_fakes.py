# Step 1 (exploration, mp floats): build fake spectra and save positions as exact rationals. Verification is in verify.py.
from build import *
LAM = F(100001, 100000)
SPEC = {  # dataset M : (J big atoms, N big atoms)
    6: ([LAM, F(999,1000)], []),
    7: ([LAM, F(999,1000)], []),
    8: ([LAM, F(89,100)], [F(17,20), F(-93,100)]),
    10: ([LAM], [F(-9,10)]),
}
def bulk(M, T, big):
    ks = list(range(4, M+1)); r = {k: T[k] - sum(b**k for b in big) for k in ks}
    for c in [0.9, 0.95, 0.99, 0.97, 0.85, 0.8, 0.75, 0.7, 0.6]:
        for ng in [801, 1201, 1601, 2001]:
            try:
                prop, res = propose(r, ks, c=c, ngrid=ng)
                if prop is None: continue
                nodes, wts = prop
                while len(nodes) < len(ks):
                    i = max(range(len(nodes)), key=lambda i: wts[i]); w = wts[i]; nodes.append(nodes[i]*0.97); wts.append(w//2); wts[i] = w-w//2
                pos = solve(r, ks, nodes, wts)
                if all(abs(p) < 0.995 for p in pos): return pos, wts
            except Exception: pass
    raise RuntimeError('no bulk')
def rat(p): return F(int(mp.nint(p*mp.mpf(10)**42)), 10**42)
out = {}
for M, (bJ, bN) in SPEC.items():
    J, N = targets(M)
    pJ, wJ = bulk(M, J, bJ); pN, wN = bulk(M, N, bN)
    out[M] = {'J': [[str(b), 1] for b in bJ] + [[str(rat(p)), w] for p, w in zip(pJ, wJ)],
              'N': [[str(b), 1] for b in bN] + [[str(rat(p)), w] for p, w in zip(pN, wN)]}
    print(M, 'J', [(mp.nstr(p,6), w) for p, w in zip(pJ, wJ)], 'N', [(mp.nstr(p,6), w) for p, w in zip(pN, wN)])
json.dump(out, open('fakes.json', 'w'), indent=1)
