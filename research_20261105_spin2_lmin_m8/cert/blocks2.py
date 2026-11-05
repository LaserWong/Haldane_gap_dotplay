# Symmetry blocks of the periodic spin-2 Heisenberg ring, untwisted (Z) and pi-seam twisted (P).
# Ported from haldane_chat_bundle/runs/thermal_arb/blocks.py (spin-1).
#   H^Z = sum_{j<L} S_j.S_{j+1} (S_L=S_0);  H^P: closing bond (L-1,0) has S^xS^x+S^yS^y sign-flipped (= U_0 h U_0^*, U_0=exp(i pi S^z_0)).
# Basis digit d in {0..4} <-> m = 2-d, site 0 most significant (same as ed_helpers digit order up to m<->-m relabel; spectra identical).
# Exact representation H = A + sqrt(6) B with A,B INTEGER sparse matrices:
#   S.S = SzSz + (S+S- + S-S+)/2 ; (1/2)<m+1|S+|m><m'-1|S-|m'> in {2 (=2*2/2), sqrt6 (=2*sqrt6/2), 3 (=sqrt6*sqrt6/2)}.
# Twisted translation T_g = U_0 T, U_0 = diag((-1)^m) on site 0; checked EXACTLY on A and B separately:
#   T_g H T_g^-1 = H, T_g^L = (-1)^Sz (P) or I (Z), F H F = H (spin flip m->-m), Sz conserved.
# Bloch blocks as in the spin-1 file: B_ab = (sqrt(p_a p_b)/L) sum_t lambda^t <a|H T_g^t|b>, lambda = exp(i pi q/L).
import numpy as np, scipy.sparse as sp, flint
from flint import arb, acb, fmpq
flint.ctx.prec = 128
d = 5
MV = np.array([2, 1, 0, -1, -2])
def _ops():
    Sz = sp.csr_matrix(np.diag(MV).astype(np.int64))
    # raise: |m> -> |m+1> i.e. digit k -> k-1. coefficient c(m)=sqrt(6-m(m+1)): m=1:2, m=0:sqrt6, m=-1:sqrt6, m=-2:2
    # Encode each S+ entry as (int part, sqrt6-flag): 2 -> 'a', sqrt6 -> 'b'
    Pa = np.zeros((5, 5), np.int64); Pb = np.zeros((5, 5), np.int64)
    Pa[0, 1] = 1; Pb[1, 2] = 1; Pb[2, 3] = 1; Pa[3, 4] = 1   # S+ = 2*Pa + sqrt6*Pb
    return Sz, sp.csr_matrix(Pa), sp.csr_matrix(Pb)
def full_H(L, tw):
    """Return (A, B) integer sparse, H = A + sqrt6 B."""
    Sz, Pa, Pb = _ops()
    I = lambda n: sp.identity(d**n, dtype=np.int64, format='csr')
    N = d**L; A = sp.csr_matrix((N, N), dtype=np.int64); B = sp.csr_matrix((N, N), dtype=np.int64)
    # (S+ x S- + S- x S+)/2 with S+ = 2Pa + r Pb, r=sqrt6:
    #   S+xS- = 4 PaxPa^T + 2r (PaxPb^T + PbxPa^T) + 6 PbxPb^T ; /2 -> 2 PaPa + r(PaPb+PbPa) + 3 PbPb
    terms_A = lambda X, Y: [(Sz, Sz, 1), (Pa, Pa.T, 2), (Pa.T, Pa, 2), (Pb, Pb.T, 3), (Pb.T, Pb, 3)]
    terms_B = [(Pa, Pb.T, 1), (Pb, Pa.T, 1), (Pa.T, Pb, 1), (Pb.T, Pa, 1)]
    TA = [(Sz, Sz, 1, False), (Pa, Pa.T, 2, True), (Pa.T, Pa, 2, True), (Pb, Pb.T, 3, True), (Pb.T, Pb, 3, True)]
    TB = [(X, Y, c, True) for X, Y, c in terms_B]
    for j in range(L - 1):
        for X, Y, c, _ in TA: A = A + c * sp.kron(sp.kron(I(j), sp.kron(X, Y)), I(L - 2 - j), format='csr')
        for X, Y, c, _ in TB: B = B + c * sp.kron(sp.kron(I(j), sp.kron(X, Y)), I(L - 2 - j), format='csr')
    sgn = -1 if tw == 'P' else 1
    for X, Y, c, xy in TA:   # closing bond: X on site L-1, Y on site 0
        A = A + (sgn if xy else 1) * c * sp.kron(sp.kron(Y, I(L - 2)), X, format='csr')
    for X, Y, c, xy in TB:
        B = B + sgn * c * sp.kron(sp.kron(Y, I(L - 2)), X, format='csr')
    for M in (A, B): M.sum_duplicates(); M.eliminate_zeros()
    return A.tocsr(), B.tocsr()
def digits(L):
    x = np.arange(d**L); return np.stack([(x // d**(L - 1 - j)) % d for j in range(L)], 1)
def perm_index(L, D): return (D * (d**np.arange(L - 1, -1, -1))[None, :]).sum(1)
def twisted_translation(L, tw):
    D = digits(L); T = perm_index(L, np.roll(D, 1, axis=1))
    s = np.ones(d**L, np.int64)
    if tw == 'P': s = np.where(MV[D[:, 0]] % 2 != 0, -1, 1)     # s(y) = (-1)^{m_0(y)}
    return T, s
def flip(L): return perm_index(L, 4 - digits(L))
def same(X, Y): return (X != Y).nnz == 0
def checks(L, tw, AB, T, s, F):
    out = {}; N = d**L
    P = sp.csr_matrix((s[T].astype(np.int64), (T, np.arange(N))), shape=(N, N))
    Fm = sp.csr_matrix((np.ones(N, np.int64), (F, np.arange(N))), shape=(N, N))
    Szv = MV[digits(L)].sum(1)
    Q = sp.identity(N, dtype=np.int64, format='csr')
    for _ in range(L): Q = P @ Q
    want = sp.diags(((-1) ** (Szv % 2) if tw == "P" else np.ones(N, np.int64)).astype(np.int64), dtype=np.int64).tocsr()
    out['P orthogonal'] = same(P @ P.T, sp.identity(N, dtype=np.int64, format='csr'))
    out['T_g^L = (-1)^Sz or I'] = same(Q, want)
    for nm, H in zip('AB', AB):
        out[f'{nm} symmetric'] = same(H, H.T)
        out[f'T_g {nm} T_g^-1 = {nm}'] = same(P @ H @ P.T, H)
        out[f'F {nm} F = {nm}'] = same(Fm @ H @ Fm.T, H)
        r, c = H.nonzero(); out[f'{nm} conserves Sz'] = bool((Szv[r] == Szv[c]).all())
    out['T conserves Sz'] = bool((Szv[T] == Szv).all()); out['F negates Sz'] = bool((Szv[F] == -Szv).all())
    return out, Szv
def sector_data(L, AB, T, s, Szv, sz):
    sec = np.nonzero(Szv == sz)[0]
    orb = [sec]
    for _ in range(L - 1): orb.append(T[orb[-1]])
    reps = np.unique(np.array(orb).min(0))
    o = [reps]; sg = [np.ones(len(reps), np.int64)]
    for _ in range(L): o.append(T[o[-1]]); sg.append(sg[-1] * s[o[-1]])
    o = np.array(o); sg = np.array(sg)
    per = np.array([next(u for u in range(1, L + 1) if o[u, j] == reps[j]) for j in range(len(reps))])
    sigma = sg[per, np.arange(len(reps))]
    assert (L % per == 0).all() and per.sum() == len(sec)
    coef = {}
    for part, H in enumerate(AB):
        Hrows = H[reps]
        for u in range(L):
            S = Hrows[:, o[u]].tocoo()
            for a, b, v in zip(S.row, S.col, S.data):
                if v == 0: continue
                key = (int(a), int(b))
                if key not in coef: coef[key] = np.zeros((2, L), np.int64)
                coef[key][part, u] += int(v) * int(sg[u, b])
    return dict(reps=reps, per=per, sigma=sigma, coef=coef, dim=len(sec))
def q_values(L, tw, sz):
    par = (sz % 2) if tw == 'P' else 0
    return [(q, 1 if q in (0, L) else 2) for q in range(L + 1) if q % 2 == par]
_wc = {}
def epi(L, j):
    if (L, j) not in _wc: _wc[(L, j)] = acb(arb(fmpq(j, L))).exp_pi_i()
    return _wc[(L, j)]
R6 = arb(6).sqrt()
def block(L, q, sd):
    per, sigma = sd['per'], sd['sigma']
    ok = ((q * per) % L == 0) & ((((q * per) // L) % 2) == ((1 - sigma) // 2))
    sel = np.nonzero(ok)[0]; m = len(sel)
    pos = -np.ones(len(per), int); pos[sel] = np.arange(m)
    real = q in (0, L)
    ent = {}; Hf = np.zeros((m, m), float if real else complex)
    cache = {}
    for (a, b), cv in sd['coef'].items():
        if pos[a] < 0 or pos[b] < 0: continue
        cz = np.zeros((2, 2 * L), np.int64)
        for part in range(2):
            for t in range(L):
                if cv[part, t]: cz[part, (q * t) % (2 * L)] += cv[part, t]
        pp = int(per[a] * per[b])
        key = (cz.tobytes(), pp)
        if key not in cache:
            if not cz.any(): cache[key] = None
            else:
                val = acb(0)
                for part, fac in ((0, arb(1)), (1, R6)):
                    for j in range(2 * L):
                        if cz[part, j]: val += int(cz[part, j]) * fac * epi(L, j)
                val = val * (arb(pp).sqrt() / L)
                if real:
                    assert val.imag.contains(0) and all(j in (0, L) for p_ in range(2) for j in range(2 * L) if cz[p_, j])
                    val = acb(val.real)
                    fl = float(val.real.mid())
                else:
                    fl = float(val.real.mid()) + 1j * float(val.imag.mid())
                cache[key] = (val, fl)
        if cache[key] is None: continue
        val, fl = cache[key]
        i, j = int(pos[a]), int(pos[b]); ent[(i, j)] = val; Hf[i, j] = fl
    for (i, j), v in ent.items():
        w = ent.get((j, i), acb(0)); assert (v - w.conjugate()).contains(0), 'non-Hermitian block'
    Hf = (Hf + Hf.conj().T) / 2
    return m, ent, Hf, real
