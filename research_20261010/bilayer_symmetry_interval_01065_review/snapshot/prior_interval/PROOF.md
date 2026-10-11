# Independent closed [.105,.106] all-size extension

## Accepted scopes

For the ordinary isotropic bilayer, unit rung coupling and positive-neighbor periodic multiedges, every real coupling21/200≤g≤53/500 and every integer square sideL≥2 has a unique full-Hilbert ground and gap≥.020881493369.

The earlier independently accepted closed cover[0,21/200] has80 pieces and uniform gap .004499695659. The new single closed piece starts exactly at21/200; hence their union has81 pieces, covers everyg∈[0,53/500]=[0,.106], and preserves the uniform lower .004499695659. No coupling point is omitted, and no gap-monotonicity assumption is used.

## Fixed physical data

The producer interval seal235a0c6e2012657bd2bf0c84c863c07b4caf47eadd992bd29fed496a3f230bb6 is pinned. The accepted point review3cc26510… supplies the independently reconstructed complete matrix and physical-library provenance. The checker nevertheless recontracts the fixed.10516D/43D denominator vectors with the accepted21D/57D Gram, affine H′ and complete quadratic H′² matrices, recovering their entire mean and variance polynomials. These are the same physical vectors embedded through U=R+M; no new search, matrix support contraction or projected-H² approximation is made.

The43D numerator's affine Rayleigh coefficients are independently reconstructed from the accepted8×8 physical pair graph/orbit action and cached first-H geometry after its exact57D embedding. Only one numerator state is retained. The selected denominator search dimensions are16/43, numerator43; ambient matrix dimensions21/57 are not new selected-vector search dimensions. Full denominator trace retained counts remain49/97, and largest physical Hilbert dimension remains2^128.

## Uniform ground and tail inequalities

For a fixed trial, rho(g) is affine and v(g)=<H′²>−rho(g)² is a globally nonnegative quadratic. Exact rational checks establish v0≥0,v2≥0 and4v0v2−v1²≥0. In particular v is convex, so its maximum on the closed interval is at an endpoint.

The full-Hilbert comparison reference

r_q(g)=(3N/8)(2g−1)+(3N/8+q)sqrt(1−4g)

is concave for g<1/4; subtracting affine rho leaves a concave function. Both ground-identification r1−rho and even-sector denominator r2−rho therefore have minima at endpoints. Directed lower square roots at the endpoints provide safe endpoint lower bounds and hence safe bounds throughout the interval, without pretending the rounded square-root function itself is concave.

Let d=min_endpoint(r2−rho)>0 and V=max_endpoint v. The full untruncated even-singlet Temple bound gives E0(g)≥rho(g)−V/d uniformly. The positive r1−rho margin separately identifies the unique global ground. The normalized trace uses that same coupling-dependent affine rho; its ground contribution is at most exp(βV/d).

For every omitted q≥2, r_q−rho is concave and bounded below by its two endpoint lower bounds. The audit checks every saved relative tail value forq=2,…,N and retains multiplicity binomial(3N+q−1,q). Their total includingq0/1 covers at least4^N states. The complete omitted tail is not truncated to the trial space.

## Uniform odd family and counting

For fixedz=.1, each momentum Gram is independent of physicalg and strictly positive. The checker reconstructs all48 modes acrossN=16,32 from the accepted operator polynomials, in exact Q(sqrt2), rather than copying endpoint energy claims. Their mean theta(g) is affine. Complete residual squared is a quadratic with a positive-semidefinite coefficient form, checked by exact field signs, and is convex. Its endpoint upper maximum Vodd controls the entire interval.

The cutoff difference r2−theta is concave; positive lower endpoint margins give a uniform Temple denominator dodd. The relative affine difference theta−rho has a lower bound from its endpoints. Thus the odd energy lower relative to rho is at least

max(min_endpoint(r1−rho), min_endpoint(theta−rho)−Vodd/dodd).

All these quantities, coefficient PSD witnesses, both endpoint enclosures and cutoff margins are checked exactly. The N distinct momentum modes each carry spin multiplicity3. Their uniformly positive cutoff margins prove all3N odd directions stay belowr2. Together with the unique ground and full-Hilbert reference count, this supplies the full even-singlet sector's second-level lower r2. It does not identify r2 with the full-Hilbert second eigenvalue.

## Correlated traces and scalar path

The fixed-vector correlated combinations8rho16−2rho64,16rho16−4rho64,4rho32−2rho64 are affine. The checker reconstructs both coefficients and endpoint values, then takes the endpoint minimum. Combining these uniform numerator exponential lower bounds with the uniform ground/odd/complete-tail upper bounds produces simultaneous J1,J2,C0 lower bounds for every coupling in the same closed interval.

At β0=189/20, the first square base is(8,8,189/10). All saved60-decimal seeds are independently reconstructed using the reviewer's544-bit directed exponential implementation. Every trace component is checked against its independently computed upper bound. The first-cycle map, stronger square-preserving recurrence and square finite-window factor are exactly those independently proved and pinned in the point review's dependency chain. No ratio is relabeled from the wrong rectangular base or temperature.

Every raw/canonical state, common defect, finite-window purity and displayed gap is recomputed. The four closed size windows[8,16],[16,32],[32,64],[64,128] cover every integer side from8 through128, including odd sides. For each p>1/2 and gapγ, exp(βγ)(1−p)<p is verified rationally. At side128 andβ=1512/5, the canonical common defect obeys0<u≤1/500 and exp(βγ)*32u<1, withγ=.020881493369. The accepted short theorem on[0,.15] suppliesgap≥.050426624396 forL=2,…,7, uniformly covering the entire new coupling interval. These facts prove the stated all-size bound.

The old closed cover is pinned by review seal0c19177fdb91be54ba1892e5e3960e18a90e0ace9f11018018445368333eea9d. Its accepted endpoint, model, integer-size scope and uniqueness agree exactly with the new piece, permitting the81-piece union.

## Reproduction and exclusions

REPRODUCE.sh checks all seals and repeats the fresh matrix-polynomial, endpoint/interior-control, odd-count, complete-tail and scalar audit in a fresh directory. Observed runtime is under3CPU seconds and21MiB RSS onCPU4, within the120CPU-second/256MiB bound. No physical support computation or floating search is performed. This does not certify any coupling above.106, claim optimality, or turn sampled failures elsewhere into impossibility results.
