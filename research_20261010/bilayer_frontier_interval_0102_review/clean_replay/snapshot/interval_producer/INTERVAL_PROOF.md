# Closed ordinary-bilayer extension from .10 to .102

2026-10-10 22:35 UTC / 18:35 America/New_York. Producer candidate pending independent new-coupling physical and scalar review. This extension has a separate seal from the immutable five-point package.

Eight adjoining closed intervals of width1/4000 cover every real g in[1/10,51/500]. They certify, subject to review, unique finite-volume ground states and

 gap >= 13574634391/10^12 = .013574634391

for every periodic integer square side L>=2 throughout that interval. Joining the separately accepted66-interval direct-window continuation would give

 gap >= 4499695659/10^12 = .004499695659

for every real0<=g<=51/500 and every integer square L>=2. This is a genuine closed coupling extension, not an inference of monotonicity from point certificates.

## Fixed witnesses, exact parameter control

Reuse precisely the fixed physical polynomial witnesses described in POINT_PROOF.md. Both odd trial families have z=1/10, independent of g or interval midpoint. All extension records explicitly label odd_band.fixed_center as1/10. The original point package had a stale inherited metadata label; its separate METADATA_ERRATUM.json explains that its numerical polynomials already used z1/10. The point seal is unchanged.

For each new closed interval[a,b], the trial vectors are identical, the normalized ground means and each odd-mode mean are affine in g, and the complete variances are convex quadratic forms. The stable bosonic reference r_q(g) is concave on[0,1/4). Therefore endpoint lower bounds on r_q-rho or r2-theta_k are uniform lower bounds, and maximum endpoint variance is a uniform variance upper bound. Exact rational/Q(sqrt2) arithmetic and outward root enclosures implement these statements. Both separate ground conditions and ALL odd-mode Temple/counting cutoffs are positive. Reconstruct all ground and odd lower energies relative to the current fixed-ground Rayleigh mean.

The complete upper trace has one ground,3N odd levels and all omitted reference shells q2,...,N with oscillator multiplicities binom(3N+q-1,q). The numerator is one8x8 saved43D-search trial contribution. All correlated energy combinations for J1,J2,C0 are affine and are lower-bounded at interval endpoints before exponentiation. No spectral state is dropped because its residual is small.

Each short L2,...,7 bound is recalculated at the interval's upper endpoint. Its expression C(2g-1)+(C+1)sqrt(1-4g) is strictly decreasing in the domain, since its derivative is2C-2(C+1)/sqrt(1-4g)<0. Thus this endpoint choice is rigorous on every new closed interval.

The saved ground witness coefficients, full moments and odd polynomial identities are inherited from the accepted complete-residual/interval-input packages. No new large physical contraction, vector optimization, eigensolver or ED is performed. New physical inequalities atg>.10 are explicitly checked; validity is not borrowed from the old point or old interval conclusions.

## Scalar and all-integer coverage

Every interval supplies exact initial trace-ratio bounds and txy purities at n8 and physical beta twice its recorded beta_initial. The accepted direct2D-window lemma, valid canonical transport, retained joint ratio and exact recurrences cover each integer finite window. The canonical terminal has0<u<=1/500 and an exact exp(beta*gap)*32u<1 witness. Take the minimum with all required early windows and six short-size bounds.

extension_summary.json verifies exact closed-interval adjacency and the endpoint coverage[1/10,51/500]. Each full extension/interval_NNN.json stores parameter endpoints, all physical inequalities, normalized traces, scalar states, edge basepoints and final coverage. The extension minimum is attained on[407/4000,51/500]=[.10175,.102].

## Bounded unsuccessful diagnostics

The separate startup_diagnostic.json is floating evidence only, beta5..20 step.05 and at most12 coupled cycles. It finds zero accepted small-defect starts at.1025,.105,.11. At.1025,251 temperatures complete the first cycle and121 pass the initial direct-window half-purity gate, but none enters the contracting terminal regime. At.105,162 complete the first cycle and none passes that direct-window gate. At.11 no tested temperature completes the first cycle. These are bounded method diagnostics, not all-temperature exclusions or physical transition claims.

## Resources and replay

CPU3, one thread,600CPU-second/700MiB caps. The eight-interval run takes about8 seconds. REPRODUCE.sh verifies both immutable point and interval seals plus all imported sources, reconstructs five point certificates and all eight closed intervals, and compares exact results; outputs go to separate check files/directories. Neither prior seals nor remote files are changed.
