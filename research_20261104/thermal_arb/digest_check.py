# Convention check: rebuild the repo's per-weight matrix byte streams D = (32-3n)I - 2H from OUR sparse H^g
# (blocks.full_H) and compare SHA-256 with the repo's recorded digests (uniform_second_thermal_full_review/matrix_L*.json,
# which that review asserts equal the producer case digests). Equal digests => identical integer matrices.
# Also: exact integer moments Tr (H^g)^j from the full sparse matrix (used by assemble.py as a cross-check).
import sys, os, json, hashlib, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocks import full_H, digits, flip
REPO = os.environ.get('HALDANE_REPO', '/workspace/repos/Haldane_gap_dotplay')
R = f'{REPO}/research_20261010/uniform_second_thermal_full_review'
def moments(H, jmax):
    H = H.astype(np.int64); out = [int(H.diagonal().sum()), int((H.data.astype(object)**2).sum())]
    N = H.shape[0]; t3 = 0; t4 = 0
    for s in range(0, N, 20000):
        Hc = H[:, s:s+20000]; H2c = (H @ Hc).tocsc()          # columns of H^2
        t3 += int((H2c.multiply(Hc)).sum())                    # sum_ij (H^2)_ij H_ij = Tr H^3 (H symmetric)
        if jmax >= 4: t4 += int((H2c.data.astype(object)**2).sum())  # ||H^2||_F^2 = Tr H^4
    out.append(t3)
    if jmax >= 4: out.append(t4)
    return out
res = {}
for L in [int(x) for x in sys.argv[1:]]:
    want = json.load(open(f'{R}/matrix_L{L}.json'))['payload']
    D = digits(L); Szv = (1 - D).sum(1); code = flip(L)        # repo code = base-3 of e = w+1 = 2-d
    for tw in 'IP':
        H = full_H(L, tw).tocsr()
        ok = True
        for row in want:
            M = row['M']; xs = np.nonzero(Szv == M)[0]; xs = xs[np.argsort(code[xs])]
            pos = {int(x): i for i, x in enumerate(xs)}
            h = hashlib.sha256(f'MATRIX {L} {tw} {M} {len(xs)} {row["nnz"]}\n'.encode()); cnt = 0
            for i, x in enumerate(xs):
                st, en = H.indptr[x], H.indptr[x + 1]
                ent = {pos[int(c)]: int(v) for c, v in zip(H.indices[st:en], H.data[st:en])}
                ent.setdefault(i, 0)
                for j in sorted(ent):
                    a = (32 - 3 * L) * (i == j) - 2 * ent[j]
                    h.update(f'{i} {j} {a} 0\n'.encode()); cnt += 1
            good = (cnt == row['nnz'] and len(xs) == row['dimension'] and h.hexdigest() == row[f'{tw}_matrix_sha256'])
            ok &= good
        mo = moments(H, 4 if L <= 10 else 3)
        res[f'L{L}_{tw}'] = dict(repo_digests_match=bool(ok), exact_moments_TrH_j=[str(x) for x in mo])
        print(L, tw, 'digests match' if ok else 'DIGEST MISMATCH', 'Tr H^j', mo, flush=True)
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'digest_moments.json')
old = json.load(open(fn)) if os.path.exists(fn) else {}
old.update(res); json.dump(old, open(fn, 'w'), indent=1)
