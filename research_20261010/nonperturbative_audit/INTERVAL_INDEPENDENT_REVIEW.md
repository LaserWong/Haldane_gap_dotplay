# Independent review of the vacuum interval certificate

Reviewed: 2026-10-10 13:28 EDT / 17:28 UTC.

## Result

**PASS for the new uniform-interval argument and finite-size bridge.** No conceptual, multiplicity, normalization, or interval-extension gap was found. An independent exact replay of the saved records passed. This review uses the previously audited two-direction transfer and three-purity interpolation theorem; it is not a new independent derivation of that underlying theorem.

For unit rungs, straight exchanges `J + epsilon`, crossed exchanges `J`, and `J = 3/10`, the new certificate proves unique finite-volume ground states and

\[
\Delta_L\ge
\frac{2752980708324742958664216503824603161}
{340282366920938463463374607431768211456}
>0.008090283176
\]

uniformly for every `0 <= epsilon <= 19/4000` and every integer square side `L >= 2`, with the specified positive-direction periodic adjacency multiplicities. This is a square-volume statement; no arbitrary-aspect-ratio conclusion is added.

The smaller intervals also pass:

- `0 <= epsilon <= 1/250`: exact lower bound `8182689532058971559137629312639526707 / 340282366920938463463374607431768211456`, hence greater than `0.024046763298`.
- `0 <= epsilon <= 9/2000`: exact lower bound `307854805027554099529071281078899565 / 21267647932558653966460912964485513216`, hence greater than `0.014475263367`.

The saved vacuum scan has no successful seed for the interval through `1/200`. This is only a failure of the tested vacuum-bound/grid construction. It does not contradict the separately certified, improved-trial result at the single point `epsilon = 1/200`, nor prove that a uniform interval through that point is impossible.

## 1. Uniform local comparison and ordered spectrum

Fix a seed geometry and its saved rational `a,b`. The physical four-spin comparison matrix

\[
M(\epsilon)=\epsilon v+a(P_i+P_j)+bI
\]

is affine in epsilon. Exact positive-definite LDL checks at `0` and `epsilon_max` imply positive definiteness throughout the closed interval by convexity. Both endpoints were replayed directly in the physical-spin basis. The coefficients are fixed over the interval; no unjustified interpolation of separately optimized parameters is used.

Each rung has weighted degree four and the total edge weight is `2N`, including period-two directions. Summing therefore gives `H - E00 >= D_a - 2Nb`, with the occupancy-block value `f(A) - 4a|A|`. Exact enumeration independently reproduced every saved bin and its multiplicity, including total rank `4^N` and the rank-one vacuum block.

The saved nonvacuum cut

\[
d=\min_{A\ne\varnothing}(f(A)-4a|A|)-2Nb>0
\]

is independent of epsilon. It places the physical second eigenvalue at least `E00+d` by ordered min-max. The vacuum reference is the unique lowest reference block. This does not require the perturbed Hamiltonian to preserve triplet occupancy.

## 2. Full vacuum residual and Temple interval

For the normalized singlet product, `rho = E00 = -3N/4` at every epsilon. The reference interaction annihilates that state. For one distinct rung pair, direct action of the two straight physical exchanges gives zero expectation and squared norm `3/4`.

The output on that pair has a triplet on each endpoint and singlets elsewhere. Outputs belonging to different unordered rung pairs are orthogonal, even if the pairs share one endpoint, because at some rung one output has a singlet and the other a triplet. Parallel adjacency contributions must first be combined. Thus the full residual, including all states outside the one-dimensional trial space, is exactly

\[
r^2(\epsilon)=\frac34\epsilon^2\sum_{\{i,j\}}w_{ij}^2.
\]

The squared edge-weight sums are `16,24,32` for `2x2,4x2,4x4`. The reached dimensions for nonzero epsilon are `13,37,97`, respectively, while the linear trial dimension and retained-vector count are each one. The full Hilbert dimensions remain `256`, `65,536`, and `4,294,967,296`.

Because `rho < E00+d`, the second-eigenvalue cut proves ground-state uniqueness and Temple's inequality gives

\[
E00-\frac{r^2(\epsilon)}d\le E_0(\epsilon)\le E00.
\]

Replacing the numerator by `r^2(epsilon_max)` is valid throughout the interval. All saved rational interval endpoints and residuals were independently reproduced.

## 3. Thermal bounds and recurrence

The reference bins bound every ordered excited eigenvalue, not just a selected band. Their nonvacuum multiplicities total `4^N-1`. Separating the unique ground state gives the saved uniform partition-function bound

\[
e^{\beta E00} Z(\beta)\le
e^{\beta(E00-\ell)}+
\sum_{A\ne\varnothing}\operatorname{rank}(A)
e^{-\beta(f(A)-4a|A|-2Nb)},
\]

where `ell` is the uniform Temple lower endpoint. The variational numerator bound is uniform as well. The common upper energies are exactly `-3,-6,-12`; consequently all relevant extensive energy factors cancel exactly in the correlated first updates.

All four stored successful seeds were replayed with `audit_ff.seed_check`: independent 192-bit outward exponential bounds, exact 128-bit rounded sequential recurrence, accepted state, and final exponential test for the gap all passed. The relevant all-integer-square theorem continues to apply for every epsilon in these intervals: the layer-coupling eigenvalues are `2J+epsilon` and `epsilon`, both nonnegative, including the zero eigenvalue at epsilon zero. The real-structure and periodic-multiplicity conventions remain unchanged.

For the largest successful interval, the accepted seed uses initial `beta=57/2` and `n=m=32`; the thermal theorem covers all integer `L>=32`.

## 4. Triangle-free short-size bridge

For every square `L>=4`, the nearest-neighbor torus graph is simple, triangle-free, and degree four. Odd `L>=5` need not be bipartite, but are still triangle-free; bipartiteness is not used.

For an occupied set of size `q`, degree counting gives `E(A)<=2q`. The triangle-free bound `E(A)<=floor(q^2/4)` also holds: for each induced edge `uv`, its endpoints have disjoint neighbor sets, so `deg(u)+deg(v)<=q`. Summing over edges and using Cauchy gives `4E^2/q <= sum deg(v)^2 <= qE`, which yields the bound (the edgeless case is immediate).

All active edge weights are one, so `sum_i m_i(A)<=q`. The weighted-star comparison therefore yields

\[
f(A)\ge q-\frac3{10}\left(\min(2q,\lfloor q^2/4\rfloor)+q/2\right),
\]

with the sharper exact value `f=1` for `q=1`. The eight reference values in the implementation are exactly

`1, 7/5, 39/20, 11/5, 49/20, 12/5, 47/20, 2`.

For `q>=8`, the bound is `q/4`. Hence if `0<=a<1/16`, the expression `q/4-4aq` is increasing, and its minimum over `q>=8` occurs at `q=8`. Checking `q=1,...,8` is sufficient. This is an analytic cutoff, not a numerical truncation of the occupancy sectors.

After summing the local comparison, the second eigenvalue of the shifted physical Hamiltonian is at least

\[
c(a)-2L^2b,\qquad
c(a)=\min_{1\le q\le8}(f_q-4aq).
\]

The vacuum trial still has expectation zero, so the spectral gap is at least this same number. There is no missing factor of two from a perturbation-width estimate. All used `b` are positive, so among `4<=L<n` the worst such bound occurs at `L=n-1`. Endpoint PSD checks make this bound uniform in epsilon.

The exceptional sizes are properly treated separately: the bounds `2/5-12epsilon_max` for `L=2` and `1-27epsilon_max` for `L=3` follow from the unperturbed gaps and the lower spectral bound of the straight-exchange perturbation. No triangle-free claim is made for `L=3`.

For `epsilon_max=19/4000` and `n=32`, the saved bridge has `a=1/28`, `b=126412089/500000000000`, and `c=6/7`. It gives

- `L=2`: `343/1000`;
- `L=3`: `3487/4000`;
- every `4<=L<=31`: at least `649625877297/1750000000000`.

The full short-size minimum is `343/1000`, comfortably above the thermal bound. Every missing integer size is covered.

## 5. Replay and provenance

The independent replay imported only the already independent `audit_ff` verifier, not the candidate producer or optimizer. It recomputed the physical-pair residual, all three occupancy histograms, all twelve geometry records, both local PSD endpoints for every seed geometry and every bridge, all four successful bootstrap seeds, and the full finite-bridge arithmetic. As an additional arithmetic check, the occupancy lower expression was evaluated for every integer `1<=q<=(n-1)^2` for each bridge, confirming the analytic eight-level cutoff. The replay used one-thread BLAS/OMP/MKL settings and took approximately 3.4 seconds of measured checking time.

The certificate file was verified unchanged from the start to the end of the replay. Reviewed SHA-256 values:

- `BASELINE_PROOF.md`: `449a77131ab7b484478e8b3363756ba181c44b82e5a7394d0fe9c229cbbd4f7b`
- `audit_ff.py`: `5e09b3000f2cd52fd1151c8a78febf873368f570d1336373ce45884aa4b2242a`
- `certify_vacuum_interval.py`: `5655ed8eb522fab0ff2de5a08a67488a046a2cf4932463c4cfab2712d5b5905b`
- `trianglefree_bridge.py`: `1a04c2d89cdbf9b12c4fe9ff8a16ee66eed53cf0aed3ea09d6b880fdd6e54691`
- `vacuum_interval_certificates.json`: `bb94201ea6001464582f9d6effed3636aec9cb5fb1dabb9f106e61bcbf35977d`

Only this review file was written. No baseline, producer, verifier, certificate, or remote state was modified. The supplied working directory is a materialized file tree without Git metadata, so local branch and commit verification were unavailable; the README names source commit `6be889a30f642bde77fb89af75b3a7379615bed1`, but this review relies on the explicit content hashes above rather than asserting a verified checkout identity.
