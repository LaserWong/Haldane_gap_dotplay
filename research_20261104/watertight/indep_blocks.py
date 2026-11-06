# Independent construction of the (Sz, k) blocks of the periodic spin-1 Heisenberg ring H_L = sum_j S_j.S_{j+1}.
# Different from b_n8_rigorous_arb/enclose12.py: H is built by Kronecker products of 3x3 integer matrices
# (site 0 = most significant factor), translation T is a separate permutation verified EXACTLY to commute with H,
# and block entries come from the direct formula
#     B_ab(k) = sqrt(p_a p_b)/L * sum_{u=0}^{L-1} w^{k u} <a|H|T^u b>,   w = exp(2 pi i / L),
# i.e. B = Phi^* H Phi for the orthonormal Bloch vectors v_b = (sqrt(p_b)/L) sum_s w^{k s} T^s |b>.
# (proof in WATERTIGHT_STATUS.md / sector_proof section).  No orbit-representative bookkeeping of H|r>.
import numpy as np, scipy.sparse as sp
from flint import arb, acb, fmpq
def full_H(L):
    Sz = sp.csr_matrix(np.diag([1, 0, -1]).astype(np.int64))      # basis d=0,1,2 <-> m=+1,0,-1
    Sp = sp.csr_matrix(np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], np.int64))   # S^+ / sqrt2
    Sm = Sp.T.tocsr()
    # S.S = SzSz + (S+S- + S-S+)/2 = SzSz + Sp(x)Sm + Sm(x)Sp   (since S+ = sqrt2 Sp)
    terms = [(Sz, Sz), (Sp, Sm), (Sm, Sp)]
    I = lambda n: sp.identity(3**n, dtype=np.int64, format='csr')
    H = sp.csr_matrix((3**L, 3**L), dtype=np.int64)
    for j in range(L - 1):
        for A, B in terms:
            H = H + sp.kron(sp.kron(I(j), sp.kron(A, B)), I(L - 2 - j), format='csr')
    for A, B in terms:            # wrap bond (L-1, 0): operator A on site L-1 (least significant), B on site 0
        if L == 2: H = H + sp.kron(B, A, format='csr')
        else: H = H + sp.kron(sp.kron(B, I(L - 2)), A, format='csr')
    H.sum_duplicates(); H.eliminate_zeros(); return H.tocsr()
def digits(L):
    N = 3**L; x = np.arange(N); return np.stack([(x // 3**(L - 1 - j)) % 3 for j in range(L)], 1)
def perm_index(L, D):
    return (D * (3**np.arange(L - 1, -1, -1))[None, :]).sum(1)
def translation(L):
    D = digits(L); Dn = np.roll(D, 1, axis=1)   # new digit at j+1 = old digit at j
    return perm_index(L, Dn)                     # T|x> = |Tidx[x]>
def flip(L):
    return perm_index(L, 2 - digits(L))
def same(A, B): return (A != B).nnz == 0
def checks(L, H, T, F):
    out = {}
    out['H_symmetric'] = same(H, H.T)
    out['THT^-1=H'] = same(H[T][:, T], H)
    out['FHF=H'] = same(H[F][:, F], H)
    Tk = np.arange(3**L)
    for _ in range(L): Tk = T[Tk]
    out['T^L=I'] = bool((Tk == np.arange(3**L)).all())
    Szv = (1 - digits(L)).sum(1); r, c = H.nonzero()
    out['H_conserves_Sz'] = bool((Szv[r] == Szv[c]).all())
    out['T_conserves_Sz'] = bool((Szv[T] == Szv).all()); out['F_negates_Sz'] = bool((Szv[F] == -Szv).all())
    out['FT=TF'] = bool((F[T] == T[F]).all())
    out['norm_bound'] = 'sum of bond norms = 2L (||S.S||=2 for spin 1)'
    return out, Szv
def sector_data(L, H, T, Szv, sz):
    sec = np.nonzero(Szv == sz)[0]
    orb = [sec]
    for _ in range(L - 1): orb.append(T[orb[-1]])
    orb = np.array(orb)
    reps = np.unique(orb.min(0))
    # period: smallest u>0 with T^u b = b
    o = [reps]
    for _ in range(L): o.append(T[o[-1]])
    o = np.array(o)                              # o[u] = T^u reps, u = 0..L
    per = np.array([next(u for u in range(1, L + 1) if o[u, j] == reps[j]) for j in range(len(reps))])
    assert (L % per == 0).all()
    assert per.sum() == len(sec)                 # orbits partition the sector
    Hrows = H[reps]
    S = [Hrows[:, o[u]].tocoo() for u in range(L)]   # S[u][a,b] = <a|H|T^u b>
    coef = {}
    for u in range(L):
        for a, b, v in zip(S[u].row, S[u].col, S[u].data):
            if v == 0: continue
            key = (int(a), int(b))
            if key not in coef: coef[key] = np.zeros(L, np.int64)
            coef[key][u] += int(v)
    return reps, per, coef, len(sec)
_wcache = {}
def wpow(L, j):
    if (L, j) not in _wcache: _wcache[(L, j)] = acb(arb(fmpq(2 * j, L))).exp_pi_i()
    return _wcache[(L, j)]
def block(L, k, reps, per, coef):
    sel = np.nonzero((per * k) % L == 0)[0]; m = len(sel)
    pos = -np.ones(len(reps), int); pos[sel] = np.arange(m)
    real = (k == 0 or 2 * k == L)
    ent = {}; Hf = np.zeros((m, m), float if real else complex)
    wnum = np.exp(2j * np.pi * k * np.arange(L) / L)
    cache = {}
    for (a, b), nvec in coef.items():
        if pos[a] < 0 or pos[b] < 0: continue
        cz = np.zeros(L, np.int64)
        for u in range(L):
            if nvec[u]: cz[(k * u) % L] += nvec[u]
        key = (tuple(cz), int(per[a] * per[b]))
        if key not in cache:
            s = sum((int(cz[j]) * wpow(L, j) for j in range(L) if cz[j]), acb(0))
            val = s * (arb(key[1]).sqrt() / L)
            if real:
                assert val.imag.contains(0); val = acb(sum((int(cz[j]) * (1 if j == 0 else -1) for j in range(L) if cz[j]), 0) * (arb(key[1]).sqrt() / L))
            cache[key] = val
        v = cache[key]
        if v.contains(0) and all(c == 0 for c in cz): continue
        i, j = int(pos[a]), int(pos[b]); ent[(i, j)] = v
        z = complex(np.sqrt(per[a] * per[b]) / L * (nvec * wnum).sum())
        Hf[i, j] = z.real if real else z
    for (i, j), v in ent.items():
        w = ent.get((j, i)); assert w is not None and (v - w.conjugate()).contains(0), 'non-Hermitian block'
    if not real: Hf = (Hf + Hf.conj().T) / 2
    else: Hf = (Hf + Hf.T) / 2
    return m, ent, Hf, real
