"""PROVED-grade (exact integer arithmetic): the periodic spin-2 VBS vector
Psi = prod_{j in Z_m} (a_j b_{j+1} - b_j a_{j+1})^2  is a nonzero exact zero mode of every bond (j, j+1 mod m)
of h = P3+P4 on the ring of m sites (same rescaled-integer test as cert_t0/kernel_exact.py).
Output: ring_kernel_m{m}.json (Sz=0 basis, integer coefficients of monomials prod a^k b^(4-k))."""
import json, sys, math
from fractions import Fraction as Fr
m = int(sys.argv[1])
B = json.load(open('bond_exact.json'))
ht = [[Fr(s) for s in row] for row in B['ht']]
L = 1
for row in ht:
    for v in row: L = L*v.denominator//math.gcd(L, v.denominator)
hti = [[int(v*L) for v in row] for row in ht]
sq = {(2, 0): 1, (1, 1): -2, (0, 2): 1}
cur = {tuple([0]*m): 1}
for j in range(m):
    nxt = {}
    jj = (j+1) % m
    for k, c in cur.items():
        for (ei, ej), cc in sq.items():
            kk = list(k); kk[j] += ei; kk[jj] += ej; kk = tuple(kk)
            nxt[kk] = nxt.get(kk, 0) + c*cc
    cur = {k: v for k, v in nxt.items() if v}
vec = cur
assert vec, "VBS vanished"
assert all(all(0 <= e <= 4 for e in k) and sum(e-2 for e in k) == 0 for k in vec)
ok = True
for i in range(m):
    j = (i+1) % m; acc = {}
    for k, c in vec.items():
        q = k[i]*5 + k[j]
        rest = tuple(k[s] for s in range(m) if s not in (i, j))
        for p in range(25):
            hv = hti[p][q]
            if hv: acc[(rest, p)] = acc.get((rest, p), 0) + hv*c
    if any(v != 0 for v in acc.values()): ok = False; break
print(json.dumps(dict(m=m, nnz=len(vec), annihilated_by_all_bonds=ok, maxabs=max(abs(v) for v in vec.values()))))
assert ok
json.dump({'VBS': [[list(k), v] for k, v in vec.items()]}, open(f'ring_kernel_m{m}.json', 'w'))
