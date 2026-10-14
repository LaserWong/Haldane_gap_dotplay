# Permanent limits of the global-width Hoeffding seeds

The conservative analytic seeds in `two_d_theory/three_purity_certificate.py` cannot be rescued by increasing their cell count once the scalar obstruction below applies. This is a theorem about one particular lower-bound construction. It is not an upper bound on the physical purities, a proof of physical gaplessness, or an obstruction to stronger trace and tail estimates.

Exact rational certificates establish the following sufficient regimes.

| Model and normalization | Coupling regime | Temperature split | Seed sizes covered |
|---|---|---|---|
| Ordinary spin-half bilayer with unit rung coupling | g≥1/190 | B=9/2 | Every cell count N≥4 |
| Square spin-one large-D model with D=1 | g≥1/250 | B=4 | Every cell count N≥4 |

At every positive inverse temperature in either regime, the canonical first updated purity from this analytic seed family is nonpositive. All allowed even-by-even seed rectangles have N≥4. The cutoffs are sufficient and are not claimed to be optimal.

The positive reference cases g=1/4000 for the bilayer and g=1/6000 for the large-D model are not rejected by this diagnostic. The scalar regression tests reproduce their accepted historical bounds separately.

## The seed depends monotonically on cell count

Write N=nm for the initial number of cells and set

\[
E=(\beta bN)^2/4,\qquad z_0(\beta)=1+c e^{-\beta}.
\]

For the ordinary bilayer, b=4g and c=3. For the large-D model, b=6g and c=2. Before outward rounding, the original analytic seed estimates are

\[
A_N=e^{-E},\qquad B_N=e^{-4E},\qquad
C_N=e^{-16E}z_0(\beta)^{-8N}.
\]

For fixed beta>0 and g≥0, each estimate is nonincreasing in N. The first two are strictly decreasing when g>0. The third is strictly decreasing for finite beta because c>0. Downward-rounded lower estimates cannot exceed these ideal analytic estimates.

This has a stronger consequence than failure at a sampled seed size. The ideal joint input for the first canonical update is

\[
J_N(\beta,g)=A_N^4B_N^2C_N
=\exp[-7(\beta bN)^2]\bigl(1+c e^{-\beta}\bigr)^{-8N}.
\]

It is nonincreasing in N and g at fixed beta. Therefore a uniform upper bound on J at N=4 and one coupling also bounds J at every larger N and every larger coupling. Optimizing beta at larger N cannot defeat an obstruction proved uniformly over all beta at N=4.

This monotonicity concerns the uncorrelated canonical analytic seed formulas. It does not exclude a different coordinate order, a stronger numerator contribution, a correlated joint-ratio certificate, a local relative comparison, or an improved omitted-spectrum estimate. Those constructions must be assessed on their own formulas.

## A rational temperature split covers the entire positive axis

Fix B>0. On 0<beta≤B, discard the Gaussian factor and use monotonicity of the exponential to obtain

\[
J_N(\beta,g)\le\bigl(1+c e^{-B}\bigr)^{-8N}=:U_{\rm low}.
\]

On beta≥B, discard the thermal factor to obtain

\[
J_N(\beta,g)\le\exp[-7(BbN)^2]=:U_{\rm high}.
\]

Thus

\[
\sup_{\beta>0}J_N(\beta,g)\le\max\{U_{\rm low},U_{\rm high}\}.
\]

No temperature grid, fit, asymptotic extrapolation, or numerical optimization enters this bound. The two closed ranges overlap at B and cover all positive beta.

The implemented acceptance threshold is the rational number 2/5. The exact inequality

\[
(1+2/5)^2=49/25<2
\]

proves 2/5<sqrt(2)−1. For a positive scalar argument J, the purification map is

\[
G(J)=1-\frac{(1-J)^2}{2J^2}.
\]

Consequently J≤2/5 implies G(J)<0. Since G is increasing on (0,1], the smaller outward-rounded input produced by the archived seed construction also cannot yield a positive first update.

For the bilayer at g=1/190, N=4, B=9/2, the Gaussian exponent is

\[
7(BbN)^2=9072/9025>1.
\]

For the large-D model at g=1/250, N=4, B=4, it is

\[
7(BbN)^2=16128/15625>1.
\]

In both cases, the upper branch is at most e^(-1). The rational certificates also verify that the lower branch is no greater than the outward upper enclosure of e^(-1), which is strictly below 2/5. This proves the displayed coupling regimes. The simpler common split B=4 also certifies the weaker cutoffs 1/160 and 1/240, respectively.

## Exact exponential enclosures

For 0≤x≤16, the implementation sums the positive Taylor polynomial through degree 128,

\[
S_{128}(x)=\sum_{j=0}^{128}\frac{x^j}{j!}.
\]

Every ratio of consecutive omitted terms is at most x/130<1 after the first omitted term. Therefore

\[
S_{128}(x)\le e^x\le S_{128}(x)+
\frac{x^{129}/129!}{1-x/130}.
\]

Reciprocation gives a lower and upper bound for e^(-x). The code rounds these bounds outward to rational numbers with denominator 10^40. The low-temperature-branch denominator uses the lower enclosure of e^(-B), and its reciprocal is rounded upward. The Gaussian branch may replace its exponent x by min(x,1), which weakens the bound safely and bounds computational cost.

All acceptance comparisons use rational values. The decimal 0.36787944117144233 is only a display approximation and is not a proof input.

## Executable diagnostic and evidence

`gapflow/seed_obstruction.py` provides three public operations.

- `split_bound(model,coupling,split_beta,minimum_cells=4)` returns one rational split certificate.
- `diagnose_hoeffding_seed(model,coupling,minimum_cells=4,split_betas=None)` tests at most 64 supplied split points. Its default finite list is 1/2,1,...,10.
- `verify_obstruction(record)` recomputes the saved split certificate and ignores its saved acceptance flag. It shares the enclosure implementation and is a reproducibility check, not an independent implementation of the mathematics.

A successful diagnostic returns `CERTIFIED_CRITERION_OBSTRUCTION`, with `physical_gaplessness` and `physical_seed_exclusion` both false. A failed search returns `INCONCLUSIVE`. Failure to find a split does not prove that a successful seed exists or that a sharper obstruction is unavailable.

Exact outputs for the two stated regimes are saved in `benchmarks/hoeffding_seed_obstructions.json`. Nine tests in `tests/test_seed_obstruction.py` pass, covering the rational threshold, coarse and improved cutoff regimes, larger sizes and couplings, both known positive baselines, zero coupling, exponential enclosures, tamper rejection, and malformed inputs.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_seed_obstruction.py -v
```

## Consequence for resource planning

Run this diagnostic before enlarging the seed for the same global-width Hoeffding construction. A certified obstruction supplies a mathematically justified stopping condition for that branch. More memory, a larger rectangle, or a denser temperature scan cannot repair that particular failed branch.

Record the input model, coupling, minimum cell count, split certificate, and the exact scope of the exclusion. Then change the proof input rather than repeat the same lower-bound construction. Candidate changes include certified low-energy contributions with complete tails, a sharper local relative bound, or a separately justified joint-ratio estimate. If none is available within the authorized resource budget, report the criterion-specific obstruction and the next missing mathematical ingredient.

An inconclusive diagnostic leaves seed exploration open. It does not authorize rejecting a model or bypassing actual seed and tail verification.
