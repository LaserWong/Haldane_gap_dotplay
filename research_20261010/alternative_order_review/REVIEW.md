# Independent review of alternative-order bootstrap certificates at g = 0.06

Updated: 10 October 2026, 14:24 America/New_York (EDT) / 18:24 UTC.

## Verdict

The ordinary spin-1/2 square bilayer at g = 3/50 has the independently verified bound

\[
\boxed{\Delta_L \ge \frac{4977793417}{50000000000}=0.099555868340}
\]

for **every integer square side L >= 2**, with a unique finite-volume ground state. The strongest audited certificate starts with the time–x–y order, transports its lower bounds to the canonical x–y–time staircase, and only then applies canonical recursion and interpolation.

The separately accepted x–time–y route gives 0.082067113439 on the same all-integer square scope. The untransported floating scores near 0.115 and 0.156 are not these certificates and are not accepted as gap bounds by this review.

This is an exact-arithmetic and analytic audit, not formal proof-assistant verification. Neither arbitrary aspect ratios nor uniqueness of all infinite-volume ground states is asserted. These are sufficient lower bounds, not estimates of the actual physical gap or a claim of an optimal certified coupling.

## 1. Model, provenance and division of work

The Hamiltonian has unit vertical rung exchange, equal straight in-layer exchanges g = 3/50 in both square-lattice directions, and no crossed exchange. It retains one positive-direction neighbor term per site in each spatial direction and each layer. At side two, the parallel terms remain separate; no simple-graph deduplication is made.

For N rungs, let E00 = -3N/4 and K = H - E00. The full space has dimension 4^N. The physical patches are 4×4, 8×4, and 8×8 rungs, containing 32, 64, and 128 physical spins.

The immutable producer package contains 40 files. Its `FROZEN_MANIFEST_1818.json` SHA-256 is:

`2777dd7f93ae82ba2ab9fdc519f0fca2e279a3d54a25eb4c453e025ed6041081`.

The bytes of every file are preserved in `snapshot/`, with their original nested paths. `PRODUCER_FREEZE_1818.json` preserves the producer manifest. The review's `INPUT_SHA256.json` verifies every frozen input before computation. One initial snapshot was taken while the producer's bridge job was finishing; only `bridge.log` changed before the final freeze. All acceptance uses the final frozen bytes.

The prior independent physical review is `../large_seed_review/`. Its manifest SHA-256 is:

`058ded69771bffe4822090fc8f88175592e5170e932173962fd32d02bd1d056d`.

All 163 entries of that sealed manifest and all its frozen input hashes were verified. Its coupling-independent F/S/V/W geometry is reused rather than recomputed. Each new producer geometry hash must equal the prior frozen geometry hash, and its F/S/V/W arrays must equal the prior independently rebuilt arrays. The prior review is never modified by these programs.

The existing transfer hypotheses, purification inequalities and signed-transfer all-integer interpolation theorem are inherited from the independent general-dimensional and finite-window reviews. Everything dependent on the **new coupling** is checked here: ground moments, full translated residuals, full-space spectral bins, low-band completeness, sector Temple bounds, heat traces, alternative-order transport, recursion and short-size bridges.

The working directory is an extracted shared snapshot without local Git metadata; no commit or publication is inferred from a filesystem write.

## 2. Independent physical replay at the new coupling

`audit_physical.py` is a g = 3/50 specialization of the prior independent auditor. It imports no producer module.

### Ground trial

Using the independent physical four-spin kernel and sealed graph geometry, it reconstructs all M0 through M4 moments and all G/K/J matrices, including complete H-squared contributions in the reached four- and six-triplet sectors. Exact Schur elimination determines the independent trial columns. Every matrix and selected index agrees with the producer.

The stored integer coefficient vector is merely a proposal. Its norm, Rayleigh quotient and full residual square are recomputed exactly. The ground search spaces have dimensions 11, 29, and 29. Their complete Hilbert spaces have dimensions 2^32, 2^64, and 2^128. Those quantities must not be confused.

The older affine relative-form certificate is also checked. Its simple ground Temple separation is unavailable for the larger two patches at this coupling. This is not a failure of the present certificate: its accepted ground Temple cutoff comes from the stronger independently verified number-sector count below.

### Full translated triplet band

The independent local kernel is applied to the bare one-triplet state to reconstruct the first-order translated generator W, then applied once more to reconstruct the entire HW. Every nonzero coefficient agrees with the frozen compressed columns. Nothing outside a selected support is dropped.

The audit verifies every one-site basis digit under every translation, checks the exact highest-weight condition, and computes every displacement Gram/Hamiltonian/H-squared moment. Fourier symbols are evaluated with independent pair arithmetic in Q(sqrt(2)). Their exact values, positive Gram symbols, energy enclosures and residual-square bounds all agree.

| Patch | Ground search dimension | W support | HW support | Complete retained band |
|---|---:|---:|---:|---:|
| 4×4 rungs | 11 | 85 | 3,185 | 49 |
| 8×4 rungs | 29 | 181 | 15,466 | 97 |
| 8×8 rungs | 29 | 373 | 67,755 | 193 |

The last column is 1 + 3N: one ground state and the N triplet momentum states with spin multiplicity three. It is distinct from both the trial search dimension and the configuration supports. No maximum-patch full-spectrum diagonalization is performed, and no MPS bond dimension enters this calculation.

## 3. Global counting closes the omitted-state problem

Write Q for total rung-triplet number. The independently reconstructed two-rung kernel verifies

\[
V_{\rm preserving} \ge -(Q_i+Q_j)/2,
\]

and its three normalized pair-creation matrix entries have squared magnitude 1/4. Thus the q-number diagonal comparison is (1-2g)q, and the squared off-diagonal Jacobi bound is

\[
\frac{3g^2}{4} E_{\rm empty,upper}(q) E_{\rm occupied,upper}(q+2).
\]

The local positive semidefinite inertia is exactly (negative, zero, positive) = (0,5,11).

The geometric upper counts are justified for **all integer torus side lengths at least two**, including odd sides. If h = min(q,N-q), then the edge boundary obeys

\[
|\partial A|/2 \ge \min\{\lceil 2\sqrt h\rceil,n_x,n_y\}.
\]

For q <= N/2: with no full row or column, the numbers r,c of occupied rows and columns satisfy rc >= q, and each partial cycle contributes two boundary edges. With a full row but no full column, every column is partial; the transposed case is identical. With both a full row and full column, no row or column is empty, so the complement lies inside partial-row/partial-column intersections and rc >= N-q >= N/2. Hence r+c >= sqrt(2N) >= min(nx,ny). Complementation handles q > N/2. Length-two cycles still have two boundary edges because their multiplicities are retained.

Together with 4q = 2E_occupied + |boundary|, this proves the saved upper counts. The bipartite/simple-graph refinement is applied only when both side lengths are even and at least four. It is never applied to 3×3, 5×5 or 7×7. As extra diagnostics, this review independently enumerates every subset of the 2×2, 3×3 and 4×4 graphs and verifies that every actual edge count is below the proposed bound.

For each patch and each of the six small square sizes, `audit_certificates.py` checks every saved Jacobi diagonal, squared off-diagonal, parity-chain endpoint, strictly positive rational LDL pivot, and monotonicized spectral bin. It verifies the bin multiplicity binom(N,q)3^q, its first global ordered index, and the total sum 4^N. The min–max direction is important: a lower bound on the compression to Q >= q gives a lower bound on the global eigenvalue with index 1 + sum_{j<q} binom(N,j)3^j.

Let a0,a1,a2 be the first three global bins. The singlet trial has rho < a1, and lambda2(K) >= a1, so the unique full ground is in that singlet sector. Each triplet momentum trial has Ritz upper bound below a2. The 1+3N mutually orthogonal trial states therefore give that many eigenvalues below a2, while global counting gives lambda_(2+3N)(K) >= a2. Consequently the entire low band is counted, every represented invariant sector contains exactly one eigenvalue below a2, and every omitted eigenvalue is at least a2.

## 4. Exact rank-one Temple endpoints and heat traces

In each represented sector, with one eigenvalue lambda below a = a2 and all remaining eigenvalues at least a, a normalized trial has exact mean theta < a and full residual square r². Positivity of (H-lambda)(H-a) gives

\[
\lambda \ge \theta-\frac{r^2}{a-\theta}.
\]

The independent audit checks the positive denominator and nonnegative variance before applying this inequality. It recomputes the exact rational ground endpoint and every Q(sqrt(2)) triplet endpoint. Every outward rational lower endpoint is on the correct branch and satisfies the exact Temple margin. Ground and triplet multiplicities are checked explicitly.

Only after the full count is established may the omitted trace sum start at q = 2. With u0 the ground Rayleigh upper endpoint, the retained complete band gives both bounds on Tr exp[-beta(K-u0)], while the upper bound includes

\[
\sum_{q=2}^{N} \binom Nq 3^q e^{-\beta(a_q-u_0)}.
\]

No omitted positive term or interval subtraction is used. The physical energy shift E00+u0 is restored explicitly in every correlated partition-function ratio; extensivity of a trial shift is never assumed.

The independent exponential routine uses a 90-term exact Taylor series after reduction to absolute argument at most 1/8, a rigorous positive remainder bound, and directed 384-bit rounding and squaring. This is independent of the producer's 256-bit, 70-term implementation. Every saved 16-decimal ratio matches exactly. Gap acceptance additionally uses a direct rigorous exponential inequality, rather than trusting a floating logarithm.

## 5. Axis order and exact basepoints

Let v = (4,4,beta), and D_x,D_y,D_t double x, y, and inverse temperature respectively. Define

\[
P_i(v)=Z(D_i v)/Z(v)^2.
\]

At all staircase points under consideration the spatial lengths are even. Spatial self-adjoint-transfer and thermal Gibbs purities are therefore in (0,1]. This does not identify physical time with a spatial direction; it establishes that the same algebraic squaring bound applies to their respective normalized spectra.

For order (i,j,k), let v1=D_i v, v2=D_jD_i v, v3=D_kD_jD_i v and let q1,q2,q3 be its three staircase purities. Exact cancellation gives

\[
J_1=Z(v_3)/Z(v)^8=q_1^4q_2^2q_3,
\quad J_2=Z(v_3)^2/Z(v_1)^8=q_2^4q_3^2,
\quad C_0=Z(v_3)/Z(v_2)^2=q_3.
\]

Writing G(z)=1-(1-z)^2/(2z²), the sequential first-cycle lower bounds are

\[
a=G(J_1),\quad b=G(J_2a),\quad c=G(C_0^4a^2b),
\]

with downward rounding in the implementation. These bound the ordered (i,j,k) staircase **at the common post-cycle base v3=(8,8,2beta)**. The bounds are not canonical merely because the base is square.

The physical partition functions needed are:

| Order | v1 | v2 | v3 |
|---|---|---|---|
| x–time–y | (8,4,beta) | (8,4,2beta) | (8,8,2beta) |
| time–x–y | (4,4,2beta) | (8,4,2beta) | (8,8,2beta) |

Thus J1 is common, J2 uses the correct order-specific v1 denominator, and C0 uses (8,4,2beta) in both cases. There is no unlicensed exchange of a spatial length and temperature. Spatial x/y reflection of the isotropic square model, if used, preserves the same periodic multiplicity convention.

For an adjacent pair a=P_i(w), b=P_j(D_iw), the swapped entries are c=P_j(w), e=P_i(D_jw). Exact cancellation is

\[
e c^2 = b a^2.
\]

Since both c and e are at most one, valid lower bounds transform as

\[
(a,b)\longmapsto(a\sqrt b,a^2b).
\]

The prefix before the pair is unchanged. The endpoint after it is also unchanged because doublings commute, so all later edges retain their basepoints.

For x–time–y, swapping the final pair produces

\[
(A,B,C)=(a,b\sqrt c,b^2c).
\]

For time–x–y, first swap time with x, then time with y:

\[
(A,B,C)=(a\sqrt b,a^2b\sqrt c,a^4b^2c).
\]

Both are canonical x–y–time lower triples at (8,8,2beta). All square roots are enclosed by integer-square-root inequalities before downward rounding. `audit_paths.py` independently verifies formal partition-function monomial identities for every one of the six orders, all twelve adjacent-swap positions and all eighteen sequential rotations. Its output is a ledger of exact coordinate basepoints, not a finite numerical substitute for the analytic proof above.

## 6. Canonical recursion and all integer sizes

After transport, only the previously reviewed canonical three-step recursion is used. The independent program reproduces every directed 18-decimal defect update. At its accepted side n=16 the common defect is at most 1/500, so the established all-integer theorem gives

\[
\Delta \ge \log(1/(32u))/\beta_{\rm accepted}.
\]

The proposed rational endpoint d is independently checked by exp(beta_accepted d)32u < 1. The parameters are:

| Initial order | Initial beta | Accepted beta | Asymptotic onset | Audited gap |
|---|---:|---:|---:|---:|
| x–time–y | 221/20 | 221/5 | L >= 16 | 0.082067113439 |
| time–x–y | 203/20 | 203/5 | L >= 16 | 0.099555868340 |

The larger txy result uses the exact canonical starting triple

\[
A=499520977455059221/500000000000000000,
\quad B=498024228182534247/500000000000000000,
\quad C=198422505485447151/200000000000000000.
\]

At side eight and beta = 203/10, the independently reviewed signed-transfer finite-window lemma gives a uniform thermal-purity bound for **every integer rectangle in [8,16]²**, and hence every needed square. This review independently checks its dominant-weight square-root witnesses, tail ratios, both one-dimensional interpolation steps, and the direct exponential gap inequality. Its gap endpoint is 0.171374817102, strictly above the final target. The x–time–y window similarly gives 0.150159812136. Extra saved [16,32] windows are also verified but are not needed to close the first missing interval.

For L=2,...,7, the singlet-product trial has exact K-energy zero, so lambda1(K) <= 0. The independently replayed q>=1 compression gives lambda2(K) >= a1 > 0. Therefore gap >= a1, with the exact accepted endpoints:

| L | Gap lower endpoint |
|---|---:|
| 2 | 0.855787635559 |
| 3 | 0.816149240629 |
| 4 | 0.793364149067 |
| 5 | 0.737883348270 |
| 6 | 0.668066575973 |
| 7 | 0.583853380272 |

Every endpoint exceeds 0.099555868340. These local sizes, the side-eight finite window, and the canonical asymptotic theorem cover every integer L>=2 with no gap in the size range.

The more general geometric conclusion remains a union of common dyadic boxes. It is not all rectangles of arbitrary or merely bounded aspect ratio. The ground-state uniqueness established here is finite-volume uniqueness for the specified periodic Hamiltonians.

## 7. Reproduction and files

Run `REPRODUCE.sh` from any directory. It performs the new ground reconstruction, complete translation reconstruction, symbolic path checks, all number-bin and Temple tests, independent traces and scalar replay, and all-size bridge acceptance. It writes only this review directory and changes no remote state or producer input.

All substantial numerical scripts pin to one CPU and set every BLAS/OpenMP thread count to one. The inherited independent kernel reduces the hard address-space limit to 1 GiB, below the requested 1.5 GiB ceiling. The largest translated replay took about fifteen seconds in this environment; timing is diagnostic only. The whole-space counts and acceptance comparisons use exact integer, rational or Q(sqrt(2)) arithmetic.

- `REVIEW_STATUS.json`: accepted model, scope, gaps and provenance
- `results/ground_replay.json`: new exact ground moments and complete residuals
- `results/translation_replay.json`: complete new translated-band replay
- `results/patch_review.json`: complete count and all sector endpoints
- `results/trace_review.json`: independent traces, transport and canonical recursion
- `results/all_size_review.json`: every finite-size bridge and final coverage
- `results/path_ledger.json`: exact symbolic coordinate identities
- `PRIOR_REVIEW_SHA256.json`: sealed inherited review provenance
- `INPUT_SHA256.json`, `PRODUCER_FREEZE_1818.json`, `snapshot/`: immutable new inputs
- `MANIFEST_SHA256.json`: this review's completed package
