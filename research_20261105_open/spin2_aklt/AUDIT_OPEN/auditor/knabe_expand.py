"""Independently verify Knabe expansion coefficients on artificial ring with wrap-around.
Uses small random PSD projectors (not necessarily FF) to check the ALGEBRAIC identity
of Sigma B^2 coefficients; then tests operator inequality direction under C_M hyp.
"""
import numpy as np
from itertools import combinations

rng = np.random.default_rng(0)

def random_projector(d, rank, rng):
    A = rng.normal(size=(d, rank))
    Q, _ = np.linalg.qr(A)
    return Q @ Q.T  # d x d projector

def embed_bond(h, i, M, d):
    """Embed 2-site op h on sites (i, i+1) of M-site chain, sites 0..M-1."""
    ops = []
    for s in range(M):
        if s == i % M:
            # left factor of h: reshape h as (d,d,d,d)
            pass
    # Build via kron
    # h acts on sites i, i+1 mod M
    left = i % M
    right = (i + 1) % M
    # order sites 0..M-1
    if left < right:
        # standard
        before = left
        after = M - right - 1
        mid_gap = right - left - 1  # 0
        H = np.eye(1)
        for s in range(M):
            if s == left:
                # absorb both via reshaping later
                break
        # simpler: reshape
        h4 = h.reshape(d, d, d, d)
        dim = d ** M
        out = np.zeros((dim, dim))
        # enumerate basis
        # too slow for large; use kron carefully
    # Use iterative kron with swap for wrap
    if left < right:
        mats = []
        for s in range(M):
            if s == left:
                continue  # handle as pair
            elif s == right:
                continue
            else:
                mats.append(('I', s))
        # Build: I^{left} ⊗ h ⊗ I^{M-right-1} but h is on 2 sites
        eye_before = np.eye(d ** left)
        eye_after = np.eye(d ** (M - right - 1))
        return np.kron(np.kron(eye_before, h), eye_after)
    else:
        # wrap-around bond between M-1 and 0
        assert left == M - 1 and right == 0
        # h_{M-1,0}: need to permute
        # Use: apply as partial
        # State reshape (d^{M-1}, d) for last site, etc.
        # Implement via explicit basis for small M
        dim = d ** M
        out = np.zeros((dim, dim))
        h4 = h.reshape(d, d, d, d)  # a,b,a',b' with a=site left=M-1, b=site 0
        for ket in range(dim):
            coords = [(ket // d**(M-1-s)) % d for s in range(M)]
            for bra in range(dim):
                bcoords = [(bra // d**(M-1-s)) % d for s in range(M)]
                # other sites must match
                ok = True
                for s in range(1, M-1):
                    if coords[s] != bcoords[s]:
                        ok = False
                        break
                if not ok:
                    continue
                a, b = coords[M-1], coords[0]
                ap, bp = bcoords[M-1], bcoords[0]
                out[bra, ket] = h4[a, b, ap, bp]
        return out

def embed_bond_general(h, i, M, d):
    left = i % M
    right = (i + 1) % M
    if left < right:
        eye_before = np.eye(d ** left)
        eye_after = np.eye(d ** (M - right - 1))
        return np.kron(np.kron(eye_before, h), eye_after)
    else:
        return embed_bond(h, i, M, d)  # wrap path

# Test embed: M=3,d=2
d=2; M=3
h = random_projector(d*d, 1, rng)
H01 = embed_bond_general(h, 0, M, d)
H12 = embed_bond_general(h, 1, M, d)
H20 = embed_bond_general(h, 2, M, d)
assert H01.shape == (8,8)
# hermiticity
assert np.allclose(H01, H01.T)
print("embed ok")

def knabe_coeffs_count(n, M, cs):
    """Count coefficient of each unordered pair {i,i'} in Sigma_l B_l^2
    by combinatorial window counting (algebraic, exact).
    Returns dict: ('diag', i) -> sum c^2 contributions per bond
                   ('adj', i) -> anticommutator coeff for bonds i,i+1
                   ('far', e, i) -> coeff for hi hi_{i+e} (directed then symmetrized)
    """
    # B_l = sum_{j=0}^{n-2} c_j h_{l+j}
    # B_l^2 = sum_j c_j^2 h_{l+j} + sum_{j<k} c_j c_k {h_{l+j}, h_{l+k}}
    #        (for projectors h^2=h; for general PSD use h_j^2 terms separately)
    # For projectors: {h_a,h_b} = 2 h_a h_b when they commute (d>=2), else anticommutator.
    n_w = n - 1  # number of bonds in window
    assert len(cs) == n_w
    diag = np.zeros(M)
    # coeff of {h_i, h_k} for each ordered pair with ring directed distance
    # store coeff of product term in expansion before using h^2=h
    # We'll accumulate coefficient multiplying the operator X_{i,k} where
    # for i=k: h_i (after using h^2=h, contrib c^2)
    # for i!=k: c_a c_b for the anticommutator term / 2 each way... 
    # From (A.1): B^2 = sum c^2 h + sum_{adj in window} c c' {h,h'} + sum_{far} c c' {h,h'}
    # Actually (A.1) uses {hj,hj'} for all j'>=j+2 and also for adjacent.
    pair = np.zeros((M, M))  # pair[i,k] = coefficient of {h_i, h_k}/2? Let's use coeff of {hi,hk} for i<k, and coeff of hi for diagonal
    for l in range(M):
        for j in range(n_w):
            bj = (l + j) % M
            diag[bj] += cs[j]**2
        for j in range(n_w):
            for jp in range(j+1, n_w):
                bj = (l + j) % M
                bjp = (l + jp) % M
                # contributes cs[j]*cs[jp] * {h_bj, h_bjp}
                a, b = min(bj, bjp), max(bj, bjp)
                pair[a, b] += cs[j] * cs[jp]
    return diag, pair

def q_of(cs, x):
    if x <= 0 or x >= len(cs):
        return 0.0
    return sum(cs[j]*cs[j+x] for j in range(len(cs)-x))

def predicted_pair_coeff(cs, M, i, k):
    """Predicted coefficient of {hi,hk} in Sigma B^2 from C_M theory."""
    e = min((k - i) % M, (i - k) % M)
    if e == 0:
        return None
    # On ring, directed contributions: window relative offsets
    # C_M(e) = q(e)+q(M-e); this is the coeff of {hi, h_{i+e}}? 
    # In (A.2) for non-wrap case, coeff of hi hi' (not anticommutator!) for d>=2 is q(d).
    # Careful: (A.1) uses anticommutator {hj,hj'}=hj hj'+hj' hj.
    # For d>=2 commuting projectors, {h,h'}=2hh', and (A.2) writes hi hi' with coeff = sum c c = q(d).
    # Wait - (A.2) says hi hi' * (sum c_j c_{j+d}). So they use product not anticommutator for the far terms,
    # meaning the coeff of hi hi' is 2 * (window co-occurrence of ordered?). 
    # Looking at (A.1): + sum sum c c {hj, hj'} for j'>=j+2.
    # When summing over windows and converting {h,h'}=hh'+h'h to for unordered, 
    # for each unordered pair, the total coeff of {hi,hk} equals q(d) where d=dist,
    # and then they write it as coeff of hi hi' equal to that same q(d) by using hh'=h'h and absorbing?
    # Actually if {h,h'} has coeff q, then since hh'=h'h, {h,h'}=2hh' so hh' has coeff q.
    # No: if expansion has q * {h,h'} = q*(hh'+h'h) = 2q hh', then writing q * hi hi' would be wrong by factor 2.
    # Look at (A.2) again carefully from the paper text:
    # Σ B^2 = (Σc²)H + (Σ c_j c_{j+1}) Q + Σ_{d=2..n-2} hi hi' (Σ_{j=0}^{n-2-d} c_j c_{j+d})
    # And Q := Σ {hi, hi+1}, F := Σ_{d≥2} hi hi'
    # So adjacent: coeff of {hi,hi+1} is q(1)
    # Far: coeff of hi hi' (product) is q(d)
    # Consistency of (A.1)->(A.2): from (A.1) far terms are c c {h,h'} = c c (hh'+h'h).
    # When collecting coeff of unordered product hi hi' for i < i', both orderings in the double sum
    # within a window contribute... Actually within one window, each unordered pair appears once
    # as {h,h'} with coeff c_j c_j'. Summing windows, total coeff of {hi,hk} is q(d).
    # Then {hi,hk}=2 hi hk, so coeff of hi hk would be 2 q(d). But (A.2) says q(d) for hi hi'!
    # CONTRADICTION unless (A.2) means something else.
    #
    # Alternative reading: In (A.2) the sum is over 1≤i,i'≤M+1 with 2≤d≤n-2, which is ORDERED pairs (both (i,i') and (i',i)).
    # So each unordered pair appears twice, each with coeff q(d), total 2q(d) for hi hi' + h'i hi = { } contribution matching.
    # YES - the sum is over ordered pairs i,i', so hi hi' for (i,i') and (i',i) each get q(d), totaling 2q = coeff of products matching { } with coeff q.
    return q_of(cs, e) + q_of(cs, M - e)

# Compare combinatorial to prediction for various n, M
results = []
for n, M in [(4, 8), (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (8, 9), (8, 10), (8, 16), (8, 17)]:
    n_w = n - 1
    # equal weights for clarity
    cs = [1.0] * n_w
    # also LM-like increasing then decreasing
    cs2 = [float(j+1) for j in range((n_w+1)//2)]
    cs2 = cs2 + cs2[:n_w//2][::-1]
    if len(cs2) > n_w:
        cs2 = cs2[:n_w]
    while len(cs2) < n_w:
        cs2.append(cs2[-1])
    for label, cs in [("eq", [1.0]*n_w), ("sym", None)]:
        if label == "sym":
            # Ass 4.1 style
            mid = (n_w - 1) / 2
            cs = [1.0 + 0.3 * (mid - abs(j - mid)) for j in range(n_w)]
        diag, pair = knabe_coeffs_count(n, M, cs)
        # predicted diag: each bond appears in n_w windows with each relative slot once... 
        # on ring size M, each bond gets sum_j c_j^2
        pred_diag = sum(c*c for c in cs)
        diag_ok = np.allclose(diag, pred_diag)
        # check all pairs
        pair_ok = True
        details = []
        for i in range(M):
            for k in range(i+1, M):
                e = min(k - i, M - (k - i))
                got = pair[i, k]  # coeff of {hi,hk}
                pred = predicted_pair_coeff(cs, M, i, k)
                # Our knabe_coeffs_count accumulates cs[j]*cs[jp] for each window co-occurrence
                # which is exactly the coeff of {hi,hk}. Predicted C_M(e)=q(e)+q(M-e) should match.
                if abs(got - pred) > 1e-9:
                    pair_ok = False
                    details.append((i, k, e, got, pred))
        results.append(dict(n=n, M=M, label=label, diag_ok=diag_ok, pair_ok=pair_ok, nfail=len(details), sample=details[:3],
                            pred_diag=pred_diag, got_diag=float(diag[0]), q1=q_of(cs,1)))
        if not pair_ok or not diag_ok:
            print("FAIL", results[-1])
        else:
            print("OK", n, M, label, "q1", q_of(cs,1), "maxC/q1", max((predicted_pair_coeff(cs,M,0,e)/q_of(cs,1) if q_of(cs,1) else 0) for e in range(2, M//2+1)))

print("SUMMARY fails", sum(1 for r in results if not r['pair_ok'] or not r['diag_ok']), "of", len(results))
