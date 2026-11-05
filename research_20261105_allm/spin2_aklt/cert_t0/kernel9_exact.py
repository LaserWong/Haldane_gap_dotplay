"""PROVED-grade (exact integers): all 9 VBS vectors E(a1,b1) prod (a_i b_{i+1}-b_i a_{i+1})^2 F(a_n,b_n), E,F in {a^2,ab,b^2},
are annihilated by every bond of the open n-chain (h = P3+P4) and are linearly independent (exact rank 9).
Combined with the Sz=0 count (=3, certified) this gives dim ker H_n = 9 exactly (see CERT_T0.md)."""
import sys, json, itertools, sympy as sp
sys.argv = sys.argv[:2]
src = open('kernel_exact.py').read().split("vecs = {")[0]
exec(src)
vecs = {f"{E}|{F}": vbs(E, F) for E in edges for F in edges}
ok = {}
for name, vec in vecs.items():
    good = True
    for i in range(n-1):
        acc = {}
        for k, c in vec.items():
            q = k[i]*5 + k[i+1]; rest = k[:i] + k[i+2:]
            for p in range(25):
                hv = hti[p][q]
                if hv: acc[(rest, p)] = acc.get((rest, p), 0) + hv*c
        if any(v for v in acc.values()): good = False; break
    ok[name] = good
keys = sorted(set().union(*[set(v) for v in vecs.values()]))
M = sp.Matrix([[vecs[nm].get(k, 0) for k in keys] for nm in vecs])
# rank via exact integer arithmetic on a selected set of columns (vectors live in different Sz sectors -> block structure)
rank = M.rank(iszerofunc=lambda x: x == 0) if len(keys) < 3000 else None
if rank is None:
    rank = 0
    for Sz in range(-2, 3):
        rows = [nm for nm in vecs if (edges[nm.split('|')[0]] - 2 + edges[nm.split('|')[1]] - 2 + 0) == -Sz or True]
    # group by total Sz of the vector
    groups = {}
    for nm, vec in vecs.items():
        s = sum(e-2 for e in next(iter(vec))); groups.setdefault(s, []).append(nm)
    for s, nms in groups.items():
        ks = sorted(set().union(*[set(vecs[x]) for x in nms]))
        rank += sp.Matrix([[vecs[x].get(k, 0) for k in ks] for x in nms]).rank()
print(json.dumps(dict(n=n, all_annihilated=all(ok.values()), per_vector=ok, exact_rank=rank)))
assert all(ok.values()) and rank == 9
