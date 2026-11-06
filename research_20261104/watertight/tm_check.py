# Numerical SANITY checks (not proofs) of the transfer-operator representation Z_L = Tr X^L.
import numpy as np, itertools, sys
from indep_blocks import full_H
rng = np.random.default_rng(1)
# real antisymmetric A_a with S_a = i A_a  (Cartesian spin-1 basis: (S_a)_{bc} = -i eps_{abc})
eps = np.zeros((3, 3, 3))
for a, b, c in itertools.permutations(range(3)):
    eps[a, b, c] = np.linalg.det(np.eye(3)[[a, b, c]])
A = [-eps[a] for a in range(3)]          # S_a = -i eps_a = i A_a  with A_a = -eps_a (real antisym)
S = [1j * Aa for Aa in A]
assert all(np.allclose(S[a] @ S[b] - S[b] @ S[a], 1j * sum(eps[a, b, c] * S[c] for c in range(3))) for a in range(3) for b in range(3))
assert np.allclose(sum(s @ s for s in S), 2 * np.eye(3))
print('Cartesian basis: [S_a,S_b]=i eps S_c, S^2=2, S=iA with A real antisym: OK; ||A_a||_op =', [np.linalg.norm(a, 2) for a in A])
def Zed(L, beta):
    e = np.linalg.eigvalsh(full_H(L).toarray().astype(float)); return np.exp(-beta * e).sum()
# (1) discretised transfer matrix X_M (4^M states: per time slice the bond carries none or one of x,y,z)
def XM(M, beta):
    epsl = beta / M
    ops = [np.eye(3)] + A; w = np.array([1.0, epsl, epsl, epsl])
    states = list(itertools.product(range(4), repeat=M))
    n = len(states); F = np.zeros((n, n))
    for i, s in enumerate(states):
        for j, t in enumerate(states):
            P = np.eye(3)
            for q in range(M):
                P = 0.5 * (ops[s[q]] @ ops[t[q]] + ops[t[q]] @ ops[s[q]]) @ P
            F[i, j] = np.trace(P)
    d = np.sqrt(np.array([np.prod(w[list(s)]) for s in states]))
    X = d[:, None] * F * d[None, :]
    return X
beta = 0.5
print('\n(1) discretised X_M: Tr X_M^L vs Z_L(beta=0.5) (unshifted; H = sum S.S so -H = sum A(x)A)')
for L in [2, 3, 4, 5]:
    z = Zed(L, beta); row = []
    for M in [2, 3, 4, 5]:
        X = XM(M, beta); assert np.allclose(X, X.T); lam = np.linalg.eigvalsh(X)
        row.append((M, (lam**L).sum(), lam.min()))
    print(L, 'ED', z, ' TrX^L:', ' '.join(f'M={M}:{v:.6f}' for M, v, _ in row), ' min eig', f'{row[-1][2]:.3e}')
# (2) Monte-Carlo of the exact continuous history representation (Poisson events, rate 1 per bond per component)
print('\n(2) Monte Carlo of the continuum representation, beta=0.5, 4e5 samples')
def mc(L, beta, N=400000):
    tot = 0.0; tot2 = 0.0
    for _ in range(N):
        ev = []
        for b in range(L):
            n = rng.poisson(3 * beta); ts = rng.uniform(0, beta, n); al = rng.integers(0, 3, n)
            ev += [(t, b, a) for t, a in zip(ts, al)]
        ev.sort()
        val = 1.0
        mats = [np.eye(3) for _ in range(L)]
        for t, b, a in ev:
            mats[b] = A[a] @ mats[b]; mats[(b + 1) % L] = A[a] @ mats[(b + 1) % L]
        val = np.prod([np.trace(m) for m in mats]) * np.exp(3 * beta * L)
        tot += val; tot2 += val * val
    m = tot / N; return m, np.sqrt((tot2 / N - m * m) / N)
for L in [2, 3, 4]:
    m, se = mc(L, beta); z = Zed(L, beta)
    print(L, 'ED', round(z, 5), 'MC', round(m, 5), '+-', round(se, 5), 'z-score', round((m - z) / se, 2))
