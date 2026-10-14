"""Small finite-matrix exact certificates and explicitly non-certified Ritz candidates.

Exact inputs are rational. Floats are rejected, never rounded into a proof.
The exact engine performs congruences and Schur elimination, not diagonalization.
It is cubic and intended for small validation matrices, not large spin ED.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import math
import time
import numpy as np
from scipy.sparse.linalg import LinearOperator


def rational(x):
    if isinstance(x, (float, np.floating, complex, np.complexfloating)):
        raise TypeError('Exact certificates require int, Fraction or rational string, not float')
    return F(int(x)) if isinstance(x, np.integer) else F(x)


def exact_matrix(H, max_dimension=64):
    if hasattr(H, 'toarray'):
        if H.shape[0] > max_dimension:
            raise ValueError('Exact dimension budget exceeded before densification')
        H = H.toarray()
    if isinstance(H, LinearOperator):
        raise TypeError('LinearOperator supports candidates only, not exact certificates')
    n = len(H)
    if not n or n > max_dimension or any(len(row) != n for row in H):
        raise ValueError('Nonempty square matrix within exact dimension budget required')
    M = [[rational(x) for x in row] for row in H]
    if any(M[i][j] != M[j][i] for i in range(n) for j in range(n)):
        raise ValueError('Exact real symmetry required')
    return M


@dataclass(frozen=True)
class Inertia:
    negative: int
    zero: int
    positive: int
    evidence: str = 'exact_rational_congruence'


def _inertia(M):
    """Congruence using nonzero scalar pivots or zero-diagonal 2x2 pivots."""
    M = [row[:] for row in M]
    neg = pos = zero = 0
    while M:
        n = len(M)
        pivot = next((i for i in range(n) if M[i][i]), None)
        if pivot is not None:
            order = [pivot] + [i for i in range(n) if i != pivot]
            M = [[M[i][j] for j in order] for i in order]
            d = M[0][0]
            neg += int(d < 0)
            pos += int(d > 0)
            M = [[M[i][j] - M[i][0]*M[0][j]/d for j in range(1,n)] for i in range(1,n)]
            continue
        pair = next(((i,j) for i in range(n) for j in range(i+1,n) if M[i][j]), None)
        if pair is None:
            zero += n
            break
        i,j = pair
        order = [i,j] + [k for k in range(n) if k not in pair]
        M = [[M[i][j] for j in order] for i in order]
        a = M[0][1]
        neg += 1
        pos += 1
        M = [[M[i][j] - (M[i][0]*M[1][j]+M[i][1]*M[0][j])/a
              for j in range(2,n)] for i in range(2,n)]
    return Inertia(neg, zero, pos)


def inertia(H, threshold=0, max_dimension=64):
    """Count full-matrix eigenvalues strictly below, at and above threshold."""
    M = exact_matrix(H, max_dimension)
    t = rational(threshold)
    for i in range(len(M)):
        M[i][i] -= t
    return _inertia(M)


def _inverse(M):
    n = len(M)
    A = [row[:] + [F(i == j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        p = next((i for i in range(j,n) if A[i][j]), None)
        if p is None:
            raise ValueError('Singular matrix')
        A[j],A[p] = A[p],A[j]
        d = A[j][j]
        A[j] = [v/d for v in A[j]]
        for i in range(n):
            if i != j:
                d = A[i][j]
                A[i] = [x-d*y for x,y in zip(A[i],A[j])]
    return [row[n:] for row in A]


def _split(M, trial_indices):
    idx = list(trial_indices)
    n = len(M)
    if not idx or len(idx) >= n or len(set(idx)) != len(idx) or any(i<0 or i>=n for i in idx):
        raise ValueError('Distinct trial coordinates required with 0 < k < n')
    other = [i for i in range(n) if i not in idx]
    return ([[M[i][j] for j in idx] for i in idx],
            [[M[i][j] for j in other] for i in idx],
            [[M[i][j] for j in other] for i in other])


def gershgorin_lower(M):
    return min(M[i][i]-sum(abs(x) for j,x in enumerate(M[i]) if i != j) for i in range(len(M)))


def schur_certificate(H, trial_indices, threshold, max_dimension=64):
    """Certify full spectrum at a threshold from a positive complement and small Schur block.

    Exact inversion of the complement is still cubic in its dimension. A large
    Hilbert space needs an independently proven structural complement bound.
    """
    M = exact_matrix(H, max_dimension)
    A,B,C = _split(M, trial_indices)
    t = rational(threshold)
    for i in range(len(C)):
        C[i][i] -= t
    ci = _inertia(C)
    if ci.negative or ci.zero:
        raise ValueError('Complement minus threshold is not positive definite')
    inv = _inverse(C)
    k = len(A)
    S = [[A[i][j] - (t if i == j else 0) -
          sum(B[i][a]*inv[a][b]*B[j][b] for a in range(len(C)) for b in range(len(C)))
          for j in range(k)] for i in range(k)]
    si = _inertia(S)
    return {'threshold':t, 'trial_dimension':k, 'full_dimension':len(M),
            'inertia':Inertia(si.negative,si.zero,si.positive+len(C)),
            'schur_matrix':S, 'evidence':'exact_rational_schur_congruence'}


def ritz_candidates(H, Q):
    """Floating diagnostic only. Q is orthonormalized, never certified complete."""
    Q = np.asarray(Q, dtype=float)
    if Q.ndim != 2 or Q.shape[0] != H.shape[0] or Q.shape[1] == 0 or Q.shape[1]>Q.shape[0]:
        raise ValueError('Trial array must have shape (n,k), 0 < k <= n')
    if np.linalg.matrix_rank(Q) != Q.shape[1]:
        raise ValueError('Linearly independent columns required')
    Q,_ = np.linalg.qr(Q,mode='reduced')
    HQ = H @ Q
    A = Q.T @ HQ
    if not np.allclose(A,A.T,rtol=1e-11,atol=1e-12):
        raise ValueError('Ritz compression is not real symmetric')
    e,U = np.linalg.eigh(A)
    V = Q @ U
    residual = HQ @ U - V*e
    return {'ritz_values':e, 'vectors':V, 'residual_norms':np.linalg.norm(residual,axis=0),
            'evidence':'floating_candidates_only', 'certifies_omitted_spectrum':False}


def _exp_negative_upper(x, terms):
    """Exact rational upper bound e^-x <= 1 / sum_{j=0}^terms x^j/j!."""
    if x < 0 or terms < 1:
        raise ValueError('Nonnegative exponent and positive Taylor degree required')
    term = total = F(1)
    for j in range(1,terms+1):
        term *= x/j
        total += term
    return 1/total


def thermal_tail_certificate(H, trial_indices, beta, target=None, young_parameter=1,
                             taylor_terms=32, max_dimension=64):
    """Bound sum_{j=k}^{n-1} exp(-beta*(lambda_j-E0)), zero-based indexing.

    Min-max gives lambda_k >= lambda_min(C) >= gamma without assuming the
    trial space contains ground states. E0 <= min diag(A). Residual coupling
    additionally certifies H >= diag((a-t)I,(gamma-||B||_F^2/t)I).
    This is a bound on a spectral-index tail, not Tr(Qperp exp(-beta H)).
    """
    M = exact_matrix(H,max_dimension)
    A,B,C = _split(M,trial_indices)
    beta,t = rational(beta),rational(young_parameter)
    if beta <= 0 or t <= 0:
        raise ValueError('beta and Young parameter must be positive')
    gamma,a = gershgorin_lower(C),gershgorin_lower(A)
    upper = min(A[i][i] for i in range(len(A)))
    r2 = sum(x*x for row in B for x in row)
    ground_lower = min(a-t,gamma-r2/t)
    x = beta*(gamma-upper)
    bound = len(C)*_exp_negative_upper(x,taylor_terms) if x >= 0 else None
    goal = None if target is None else rational(target)
    if goal is not None and goal < 0:
        raise ValueError('Target must be nonnegative')
    return {'full_dimension':len(M), 'trial_dimension':len(A),
            'complement_lower':gamma, 'tail_eigenvalue_lower':gamma,
            'ground_energy_upper':upper, 'ground_energy_lower':ground_lower,
            'residual_frobenius_squared':r2, 'young_parameter':t,
            'block_energy_lowers':(a-t,gamma-r2/t),
            'tail_upper_rational':bound, 'target':goal,
            'target_met':None if goal is None else bound is not None and bound <= goal,
            'evidence':'exact_rational_minmax_and_young',
            'scope':'finite input matrix only; spectral-index tail, not projected heat trace'}


def search_trial_dimension(H, beta, target, order=None, max_trial_dimension=None,
                           max_dimension=64, max_seconds=5, taylor_terms=32):
    """Find sufficient coordinate-trial dimension under explicit small-matrix budgets.

    Time is checked between trials. Individual exact arithmetic operations are
    not preempted. Failure means no certificate found, not physical gap closure.
    """
    start = time.monotonic()
    M = exact_matrix(H,max_dimension)
    n = len(M)
    order = list(range(n)) if order is None else list(order)
    if sorted(order) != list(range(n)):
        raise ValueError('order must be a permutation')
    cap = n-1 if max_trial_dimension is None else min(int(max_trial_dimension),n-1)
    records = []
    for k in range(1,cap+1):
        if time.monotonic()-start >= max_seconds:
            return {'status':'time_budget_exhausted','records':records,'sufficient_dimension':None}
        cert = thermal_tail_certificate(M,order[:k],beta,target,taylor_terms=taylor_terms,max_dimension=max_dimension)
        records.append(cert)
        if cert['target_met']:
            return {'status':'certified','records':records,'sufficient_dimension':k}
    return {'status':'no_certificate_within_dimension_budget','records':records,'sufficient_dimension':None}


def partial_ritz_candidates(H, k, tol=1e-10, maxiter=1000):
    """Iterative low Ritz states, explicitly uncertified even on solver convergence."""
    from scipy.sparse.linalg import eigsh
    n = H.shape[0]
    if not 0 < k < n:
        raise ValueError('Partial solve requires 0 < k < n')
    _, Q = eigsh(H,k=k,which='SA',tol=tol,maxiter=maxiter,
                 v0=np.linspace(1.0,2.0,n))
    return ritz_candidates(H,Q)


def _has_excited_space(M):
    """A finite real symmetric matrix has one energy iff it is scalar identity."""
    return any(M[i][j] != (M[0][0] if i == j else 0)
               for i in range(len(M)) for j in range(len(M)))


def spectral_gap_certificate(H, threshold, ground_upper=None, max_dimension=64):
    """Exact finite-matrix gap lower bound when exactly one eigenvalue is below t."""
    M = exact_matrix(H,max_dimension)
    t = rational(threshold)
    # A supplied upper bound is an explicit assumption, so disallow unsupported
    # tightening here. Coordinate Rayleigh quotients always justify this bound.
    upper = min(M[i][i] for i in range(len(M)))
    if ground_upper is not None and rational(ground_upper) < upper:
        raise ValueError('Tighter ground bound requires a separate exact Rayleigh certificate')
    if ground_upper is not None:
        upper = rational(ground_upper)
    counts = inertia(M,t,max_dimension)
    passed = _has_excited_space(M) and counts.negative == 1 and counts.zero == 0 and t > upper
    return {'inertia':counts,'threshold':t,'ground_energy_upper':upper,
            'status':'CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not _has_excited_space(M) else 'NOT_CERTIFIED'),
            'gap_lower':t-upper if passed else None,'certified':passed,
            'evidence':'exact_rational_full_matrix_inertia',
            'scope':'finite matrix only, no thermodynamic extrapolation'}


def certify_gap(H, ground_energy, gap_lower_bound, max_dimension=64):
    """Verify exact ground energy and gap above its entire eigenspace.

    Degenerate ground spaces are supported and reported, not called unique.
    Eigenvalues exactly at the upper threshold are allowed.
    """
    M = exact_matrix(H,max_dimension)
    e,g = rational(ground_energy),rational(gap_lower_bound)
    if g <= 0:
        raise ValueError('Requested gap lower bound must be positive')
    low,high = inertia(M,e,max_dimension),inertia(M,e+g,max_dimension)
    passed = low.negative == 0 and 0 < low.zero < len(M) and high.negative == low.zero
    return {'certified':passed,
            'status':'CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not _has_excited_space(M) else 'NOT_CERTIFIED'),
            'ground_energy':e,'gap_lower_bound':g,
            'ground_multiplicity':low.zero if low.negative == 0 else None,
            'ground_inertia':low,'gap_threshold_inertia':high,
            'full_dimension':len(M),'evidence':'exact_rational_full_matrix_inertia',
            'scope':'finite input matrix only, no thermodynamic extrapolation'}


def verify_gap_certificate(H, certificate, max_dimension=64):
    """Recompute from the input matrix. A replay, not an independent implementation."""
    fresh = certify_gap(H,certificate['ground_energy'],certificate['gap_lower_bound'],max_dimension)
    fields = ('certified','ground_energy','gap_lower_bound','ground_multiplicity','full_dimension')
    return fresh['certified'] and all(fresh[k] == certificate.get(k) for k in fields)


def certify_gap_from_vector(H, vector, threshold, max_dimension=64):
    """Exact Rayleigh upper plus full-matrix inertia, without exact eigenvector assumption.

    The vector may originate from explicitly rounded numerical trial data, but
    every component passed here must already be rational and is recorded.
    """
    M = exact_matrix(H,max_dimension)
    v = [rational(x) for x in vector]
    if len(v) != len(M):
        raise ValueError('Vector dimension must match matrix')
    norm2 = sum(x*x for x in v)
    if norm2 == 0:
        raise ValueError('Trial vector must be nonzero')
    t = rational(threshold)
    Hv = [sum(x*y for x,y in zip(row,v)) for row in M]
    upper = sum(x*y for x,y in zip(v,Hv))/norm2
    residual2 = sum((x-upper*y)**2 for x,y in zip(Hv,v))/norm2
    counts = inertia(M,t,max_dimension)
    passed = _has_excited_space(M) and counts.negative == 1 and t > upper
    return {'certified':passed,'trial_vector':v,'trial_norm_squared':norm2,
            'status':'CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not _has_excited_space(M) else 'NOT_CERTIFIED'),
            'ground_energy_upper':upper,'residual_squared':residual2,
            'threshold':t,'gap_lower_bound':t-upper if passed else None,
            'inertia':counts,'full_dimension':len(M),
            'evidence':'exact_rational_rayleigh_and_full_matrix_inertia',
            'scope':'finite input matrix only, no thermodynamic extrapolation'}


def _exact_pencil(A, Wdiag, max_dimension):
    M = exact_matrix(A,max_dimension)
    w = [rational(x) for x in Wdiag]
    if len(w) != len(M) or any(x <= 0 for x in w):
        raise ValueError('Positive diagonal metric of matching dimension required')
    return M,w


def _pencil_has_excited_space(M,w):
    e = M[0][0]/w[0]
    return any(M[i][j] != (e*w[i] if i == j else 0)
               for i in range(len(M)) for j in range(len(M)))


def pencil_inertia(A, Wdiag, threshold=0, max_dimension=64):
    """Exact inertia of A-tW for symmetric rational A and positive diagonal W.

    Sylvester congruence counts physical eigenvalues of W^-1/2 A W^-1/2.
    No square roots are evaluated or assumed rational.
    """
    M,w = _exact_pencil(A,Wdiag,max_dimension)
    t = rational(threshold)
    for i in range(len(M)):
        M[i][i] -= t*w[i]
    return _inertia(M)


def certify_pencil_gap(A, Wdiag, ground_energy, gap_lower_bound, max_dimension=64):
    """Exact generalized eigenvalue gap above the full ground eigenspace."""
    M,w = _exact_pencil(A,Wdiag,max_dimension)
    e,g = rational(ground_energy),rational(gap_lower_bound)
    if g <= 0:
        raise ValueError('Requested gap lower bound must be positive')
    low = pencil_inertia(M,w,e,max_dimension)
    high = pencil_inertia(M,w,e+g,max_dimension)
    passed = low.negative == 0 and 0 < low.zero < len(M) and high.negative == low.zero
    return {'certified':passed,
            'status':'CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not _pencil_has_excited_space(M,w) else 'NOT_CERTIFIED'),
            'ground_energy':e,'gap_lower_bound':g,
            'ground_multiplicity':low.zero if low.negative == 0 else None,
            'ground_inertia':low,'gap_threshold_inertia':high,
            'metric_diagonal':w,'full_dimension':len(M),
            'evidence':'exact_rational_generalized_pencil_inertia',
            'scope':'finite input pencil only, no thermodynamic extrapolation'}


def certify_pencil_gap_from_vector(A, Wdiag, vector, threshold, max_dimension=64):
    """Exact generalized Rayleigh quotient and full pencil inertia.

    v describes coordinates in the weighted basis, not orthonormal physical
    coordinates. A numerical physical vector q must first be transformed as
    v=W^-1/2 q and explicitly rationalized by the caller.
    """
    M,w = _exact_pencil(A,Wdiag,max_dimension)
    v = [rational(x) for x in vector]
    if len(v) != len(M):
        raise ValueError('Vector dimension must match pencil')
    norm2 = sum(wi*x*x for wi,x in zip(w,v))
    if norm2 == 0:
        raise ValueError('Trial vector must be nonzero')
    t = rational(threshold)
    Av = [sum(x*y for x,y in zip(row,v)) for row in M]
    upper = sum(x*y for x,y in zip(v,Av))/norm2
    residual2 = sum((ai-upper*wi*vi)**2/wi for ai,wi,vi in zip(Av,w,v))/norm2
    counts = pencil_inertia(M,w,t,max_dimension)
    passed = _pencil_has_excited_space(M,w) and counts.negative == 1 and t > upper
    return {'certified':passed,'trial_vector':v,'trial_norm_squared':norm2,
            'status':'CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not _pencil_has_excited_space(M,w) else 'NOT_CERTIFIED'),
            'ground_energy_upper':upper,'residual_squared':residual2,
            'threshold':t,'gap_lower_bound':t-upper if passed else None,
            'inertia':counts,'metric_diagonal':w,'full_dimension':len(M),
            'evidence':'exact_rational_generalized_rayleigh_and_pencil_inertia',
            'scope':'finite input pencil only, no thermodynamic extrapolation'}


def verify_pencil_gap_certificate(A,Wdiag,certificate,max_dimension=64):
    """Recompute the exact-ground generalized pencil certificate from its inputs."""
    fresh = certify_pencil_gap(A,Wdiag,certificate['ground_energy'],certificate['gap_lower_bound'],max_dimension)
    fields = ('certified','ground_energy','gap_lower_bound','ground_multiplicity','full_dimension')
    return fresh['certified'] and all(fresh[k] == certificate.get(k) for k in fields)
