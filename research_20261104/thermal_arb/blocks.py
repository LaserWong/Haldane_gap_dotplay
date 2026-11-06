# Symmetry blocks of the periodic spin-1 Heisenberg ring, untwisted (I) and pi-twisted (P) seam.
#   H^I = sum_{j=0}^{L-1} S_j.S_{j+1}  (S_L = S_0)
#   H^P = same, but the closing bond (L-1,0) has S^x S^x + S^y S^y sign-flipped  (= U_0 h U_0^*, U_0 = exp(i pi S^z_0))
# Basis: digit d in {0,1,2} <-> m = +1,0,-1, site 0 most significant.  Integer matrix: S.S = SzSz + Sp(x)Sm + Sm(x)Sp,
# Sp = S^+/sqrt2 (entries 1).  Seam flip terms get -1 for P.
# Twisted translation T_g = U_0 T (U_0 = diag(-1,1,-1) on site 0, identity for g=I): signed permutation
#   T_g|x> = s(Tx)|Tx>.  Verified EXACTLY: T_g H^g T_g^-1 = H^g, T_g^L = (-1)^{Sz} (g=P) or I (g=I), F H^g F = H^g.
# Bloch vectors (orbit rep b, period p_b, T_g^{p_b} b = sigma_b b), lambda = exp(i pi q/L), lambda^L T_g^L = 1 on sector:
#   v_b = (sqrt(p_b)/L) sum_{s<L} lambda^s T_g^s|b>,  nonzero (and unit) iff lambda^{p_b} sigma_b = 1.
#   B_ab = <v_a|H|v_b> = (sqrt(p_a p_b)/L) sum_{t<L} lambda^t <a|H T_g^t|b>.
#   q runs over residues mod 2L with q = Sz (mod 2) for P, q even for I.  B_{2L-q} = conj(B_q) entrywise (integer
#   coefficients, sigma real), so q in [0,L] with multiplicity 2 for 0<q<L and 1 for q in {0,L}.
import numpy as np, scipy.sparse as sp, flint
from flint import arb, acb, fmpq
flint.ctx.prec = 128
def full_H(L, tw):
    Sz = sp.csr_matrix(np.diag([1, 0, -1]).astype(np.int64))
    Sp = sp.csr_matrix(np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], np.int64))
    Sm = Sp.T.tocsr()
    I = lambda n: sp.identity(3**n, dtype=np.int64, format='csr')
    H = sp.csr_matrix((3**L, 3**L), dtype=np.int64)
    for j in range(L - 1):
        for A, B in [(Sz, Sz), (Sp, Sm), (Sm, Sp)]:
            H = H + sp.kron(sp.kron(I(j), sp.kron(A, B)), I(L - 2 - j), format='csr')
    sgn = -1 if tw == 'P' else 1
    for A, B, c in [(Sz, Sz, 1), (Sp, Sm, sgn), (Sm, Sp, sgn)]:   # closing bond: A on site L-1, B on site 0
        H = H + c * sp.kron(sp.kron(B, I(L - 2)), A, format='csr')
    H.sum_duplicates(); H.eliminate_zeros(); return H.tocsr()
def digits(L):
    x = np.arange(3**L); return np.stack([(x // 3**(L - 1 - j)) % 3 for j in range(L)], 1)
def perm_index(L, D): return (D * (3**np.arange(L - 1, -1, -1))[None, :]).sum(1)
def twisted_translation(L, tw):
    D = digits(L); T = perm_index(L, np.roll(D, 1, axis=1))     # T|x> = |T[x]>, new digit at j+1 = old at j
    s = np.ones(3**L, np.int64)
    if tw == 'P': s = np.where(D[:, 0] != 1, -1, 1)              # s(y) = -1 iff m_0(y) != 0
    return T, s                                                  # T_g|x> = s[T[x]] |T[x]>
def flip(L): return perm_index(L, 2 - digits(L))
def same(A, B): return (A != B).nnz == 0
def checks(L, tw, H, T, s, F):
    out = {}; N = 3**L
    out['H_symmetric'] = same(H, H.T)
    P = sp.csr_matrix((s[T].astype(np.int64), (T, np.arange(N))), shape=(N, N))   # P e_x = s[Tx] e_{Tx}
    out['T_g H T_g^-1 = H'] = same(P @ H @ P.T, H)
    out['P orthogonal'] = same(P @ P.T, sp.identity(N, dtype=np.int64, format='csr'))
    Szv = (1 - digits(L)).sum(1)
    Q = sp.identity(N, dtype=np.int64, format='csr')
    for _ in range(L): Q = P @ Q
    want = sp.diags((((-1) ** (Szv % 2)) if tw == "P" else np.ones(N)).astype(np.int64), dtype=np.int64).tocsr()
    out['T_g^L = (-1)^Sz or I'] = same(Q, want)
    Fm = sp.csr_matrix((np.ones(N, np.int64), (F, np.arange(N))), shape=(N, N))
    out['F H F = H'] = same(Fm @ H @ Fm.T, H)
    r, c = H.nonzero(); out['H conserves Sz'] = bool((Szv[r] == Szv[c]).all())
    out['T conserves Sz'] = bool((Szv[T] == Szv).all()); out['F negates Sz'] = bool((Szv[F] == -Szv).all())
    return out, Szv
def sector_data(L, H, T, s, Szv, sz):
    sec = np.nonzero(Szv == sz)[0]
    orb = [sec]
    for _ in range(L - 1): orb.append(T[orb[-1]])
    reps = np.unique(np.array(orb).min(0))
    o = [reps]; sg = [np.ones(len(reps), np.int64)]
    for _ in range(L): o.append(T[o[-1]]); sg.append(sg[-1] * s[o[-1]])
    o = np.array(o); sg = np.array(sg)                 # T_g^u |b> = sg[u] |o[u]>
    per = np.array([next(u for u in range(1, L + 1) if o[u, j] == reps[j]) for j in range(len(reps))])
    sigma = sg[per, np.arange(len(reps))]
    assert (L % per == 0).all() and per.sum() == len(sec)
    Hrows = H[reps]; coef = {}
    for u in range(L):
        S = Hrows[:, o[u]].tocoo()
        for a, b, v in zip(S.row, S.col, S.data):
            if v == 0: continue
            key = (int(a), int(b))
            if key not in coef: coef[key] = np.zeros(L, np.int64)
            coef[key][u] += int(v) * int(sg[u, b])
    return dict(reps=reps, per=per, sigma=sigma, coef=coef, dim=len(sec))
def q_values(L, tw, sz):
    par = (sz % 2) if tw == 'P' else 0
    return [(q, 1 if q in (0, L) else 2) for q in range(L + 1) if q % 2 == par]
_wc = {}
def epi(L, j):   # exp(i pi j / L), exact ball
    if (L, j) not in _wc: _wc[(L, j)] = acb(arb(fmpq(j, L))).exp_pi_i()
    return _wc[(L, j)]
def block(L, q, sd):
    per, sigma = sd['per'], sd['sigma']
    # selection lambda^{p} sigma = 1  <=>  q p / L integer with parity (0 if sigma=1, 1 if sigma=-1)
    ok = ((q * per) % L == 0) & ((((q * per) // L) % 2) == ((1 - sigma) // 2))
    sel = np.nonzero(ok)[0]; m = len(sel)
    pos = -np.ones(len(per), int); pos[sel] = np.arange(m)
    real = q in (0, L)
    ent = {}; Hf = np.zeros((m, m), float if real else complex)
    cache = {}
    for (a, b), cv in sd['coef'].items():
        if pos[a] < 0 or pos[b] < 0: continue
        cz = np.zeros(2 * L, np.int64)
        for t in range(L):
            if cv[t]: cz[(q * t) % (2 * L)] += cv[t]
        pp = int(per[a] * per[b])
        key = (tuple(cz), pp)
        if key not in cache:
            if not cz.any(): cache[key] = None
            else:
                if real:
                    s_ = sum(int(cz[j]) * (1 if j == 0 else -1) for j in range(2 * L) if cz[j])
                    assert all(j in (0, L) for j in range(2 * L) if cz[j])
                    val = acb(arb(s_) * arb(pp).sqrt() / L)
                    fl = float(s_) * np.sqrt(pp) / L
                else:
                    val = sum((int(cz[j]) * epi(L, j) for j in range(2 * L) if cz[j]), acb(0)) * (arb(pp).sqrt() / L)
                    fl = complex(val.real.mid()) + 1j * float(val.imag.mid())
                cache[key] = (val, fl)
        if cache[key] is None: continue
        val, fl = cache[key]
        i, j = int(pos[a]), int(pos[b]); ent[(i, j)] = val; Hf[i, j] = fl
    for (i, j), v in ent.items():
        w = ent.get((j, i), acb(0)); assert (v - w.conjugate()).contains(0), 'non-Hermitian block'
    Hf = (Hf + Hf.conj().T) / 2
    return m, ent, Hf, real
