"""Shared spin-1 Heisenberg (periodic) helpers for T1.  H = sum_i S_i.S_{i+1}, shifted by c*L, c = 700741/500000
(the spin-1 proof's shift a), so exp(-tau H') is O(1).  Basis: base-3 digits, site 0 most significant (as spin2/ed_small.py),
digit x <-> m = x-1.  For spin-1 every matrix element of S.S is an integer, so H is an exact integer matrix."""
import sys, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '..', 'spin2'))
from ed_small import sector, ham
from fractions import Fraction
C_SHIFT = Fraction(700741, 500000)
BETA = Fraction(49, 4); K = 6; TAU0 = BETA / 2**K          # ladder tau_k = TAU0*2^k, tau_6 = beta
d = 3
Sp = np.array([[0, 0, 0], [np.sqrt(2), 0, 0], [0, np.sqrt(2), 0]])   # basis m=-1,0,1 (digit 0,1,2): S+|m> -> |m+1>
Sz1 = np.diag([-1., 0, 1])
hbond = np.kron(Sz1, Sz1) + 0.5 * (np.kron(Sp, Sp.T) + np.kron(Sp.T, Sp))   # S.S on 9-dim, eigs {-2,-1,1}
def sectors(L):
    return {M: sector(1.0, L, M) for M in range(-L, L + 1)}
def Hblock_int(L, M):
    st = sector(1.0, L, M); H = ham(1.0, L, st).toarray() if len(st) > 0 else np.zeros((0, 0))
    Hi = np.round(H).astype(np.int64); assert np.abs(H - Hi).max() < 1e-12
    return st, Hi
def Hdense(L):
    n = d**L; H = np.zeros((n, n))
    for M in range(-L, L + 1):
        st, Hi = Hblock_int(L, M); H[np.ix_(st, st)] = Hi
    return H
def bonds(L): return [(i, (i + 1) % L) for i in range(L)]
