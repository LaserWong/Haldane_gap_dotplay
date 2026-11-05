"""PROVED-grade (exact integer/rational arithmetic): for the OPEN spin-2 chain of n sites with h = P3+P4,
the three Sz=0 VBS (Schwinger-boson) vectors  Psi_E = E(a1,b1) * prod_{i<n}(a_i b_{i+1} - b_i a_{i+1})^2 * F(a_n,b_n),
(E,F) in {(a^2,b^2),(ab,ab),(b^2,a^2)}, are exact zero modes of every bond term, and are linearly independent.
Coefficient vector c (monomial prod a_i^{k_i} b_i^{4-k_i}, k_i = basis index) satisfies  sum_q ht_pq c_q = 0  on each bond,
which is equivalent to h v = 0 for v_k = c_k * w_k (w = boson normalisation), since ht = W h W with W = diag(w) invertible.
Output: kernel_vectors_n{n}.json (integer coefficients, Sz=0 basis ordering = lexicographic base-5 index)."""
import json, sys, itertools
from fractions import Fraction as Fr
n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
B = json.load(open('bond_exact.json'))
ht = [[Fr(s) for s in row] for row in B['ht']]
L = 1
for row in ht:
    for v in row: L = L*v.denominator//__import__('math').gcd(L, v.denominator)
hti = [[int(v*L) for v in row] for row in ht]          # integer matrix L*ht
sq = {(2,0):1, (1,1):-2, (0,2):1}   # (a_i b_j - b_i a_j)^2 -> a-exponent added to (site i, site j)
edges = {'a2':2, 'ab':1, 'b2':0}
def vbs(Ename, Fname):
    # DP over sites: state = tuple of completed a-exponents, plus pending a-exponent for current site
    cur = {((), edges[Ename]): 1}
    for i in range(n-1):
        nxt = {}
        for (done, pend), c in cur.items():
            for (ei, ej), cc in sq.items():
                key = (done + (pend+ei,), ej)
                nxt[key] = nxt.get(key, 0) + c*cc
        cur = nxt
    out = {}
    for (done, pend), c in cur.items():
        k = done + (pend + edges[Fname],)
        if c: out[k] = out.get(k, 0) + c
    return {k: v for k, v in out.items() if v}
vecs = {f"{E}|{F}": vbs(E, F) for E, F in [('a2','b2'), ('ab','ab'), ('b2','a2')]}
res = {}
for name, vec in vecs.items():
    assert all(len(k) == n and all(0 <= e <= 4 for e in k) for k in vec)
    assert all(sum(e-2 for e in k) == 0 for k in vec), "not Sz=0"
    ok = True
    for i in range(n-1):
        # (sum_q ht_pq c_{..q..}) for every configuration of the other sites and every p
        acc = {}
        for k, c in vec.items():
            q = k[i]*5 + k[i+1]
            rest = k[:i] + k[i+2:]
            for p in range(25):
                hv = hti[p][q]
                if hv:
                    key = (rest, p); acc[key] = acc.get(key, 0) + hv*c
        if any(v != 0 for v in acc.values()): ok = False; break
    res[name] = dict(nnz=len(vec), annihilated_by_all_bonds=ok, maxabs=max(abs(v) for v in vec.values()))
# exact rank 3: find a nonzero 3x3 minor (Bareiss on the 3 x N matrix)
keys = sorted(set().union(*[set(v) for v in vecs.values()]))
Mx = [[Fr(vecs[nm].get(k, 0)) for k in keys] for nm in vecs]
r = 0; A = [row[:] for row in Mx]; cols = len(keys)
for c in range(cols):
    piv = next((i for i in range(r, 3) if A[i][c] != 0), None)
    if piv is None: continue
    A[r], A[piv] = A[piv], A[r]
    for i in range(3):
        if i != r and A[i][c] != 0:
            f = A[i][c]/A[r][c]; A[i] = [a - f*b for a, b in zip(A[i], A[r])]
    r += 1
    if r == 3: break
res['exact_rank'] = r
print(json.dumps(res, indent=1))
assert r == 3 and all(v['annihilated_by_all_bonds'] for k, v in res.items() if k != 'exact_rank')
json.dump({nm: [[list(k), v] for k, v in vec.items()] for nm, vec in vecs.items()}, open(f'kernel_vectors_n{n}.json', 'w'))
print("PROVED: dim ker(H_n) cap {Sz=0} >= 3 for n =", n)
