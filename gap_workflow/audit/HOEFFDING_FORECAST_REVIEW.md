# Independent audit: Hoeffding seed obstruction and size forecasts

Review: 2026-10-14 19:38 UTC.

## Verdict

The stated permanent obstruction is valid for the archived, uncorrelated global-width Hoeffding lower-bound construction in the canonical x,y,beta order. It does not exclude the physical model, its actual purities, other coordinate orders, correlated joint bounds, or stronger tail/trace methods. The implementation and theory note preserve this distinction.

The forecast initially had a false scalar-success issue caused by float conversion; it was reported and fixed. The exact boundary regression now passes. No proved minimum or uniform gap is inferred by the current forecast output.

## Formula provenance and coefficient

Read the archived `two_d_theory/three_purity_certificate.py`, `analytic_seed`, lines 106–135, in the restored checkpoint. It uses b=4g,c=3 for the unit-rung bilayer and b=6g,c=2 for spin-one D=1. The seed exponents are E,4E,16E where E=(beta*b*N)^2/4. Its C denominator is `(1+c*exp(-beta))^(8N)` with an upper enclosure in the denominator; all numerator exponentials are lower enclosures.

Therefore canonical A^4 B^2 C has total Gaussian exponent 4E+2*4E+16E=28E=7(beta*b*N)^2. The new diagnostic's formula exactly matches the ideal unrounded archived estimate. Actual archived downward-rounded bounds are no larger.

## All-temperature proof audit

For fixed beta>0, g>=0 and N>=4, the ideal joint estimate is nonincreasing in g and N. Both the Gaussian term and thermal denominator have the required direction; increasing N makes the latter strictly smaller for finite beta. Consequently an all-beta upper bound at N=4 and g=g0 covers all larger N and g.

On beta<=B, exp(-beta)>=exp(-B), so dropping the Gaussian gives the stated thermal upper bound. On beta>=B, dropping the thermal factor and replacing beta by B gives the stated Gaussian upper bound. These intervals cover the entire positive axis and overlap at B. No sampling assumption is used.

At bilayer g=1/190, N=4, B=9/2, the Gaussian exponent is exactly 9072/9025>1. At large-D g=1/250, N=4, B=4, it is 16128/15625>1. The low-branch rational upper bounds are approximately 0.35026058 and 0.31624388, respectively. Both are below the rational lower enclosure of exp(-1). The Gaussian branch is <=exp(-1). Thus the ideal supremum is <=exp(-1)<2/5<sqrt(2)-1. The stored rational final upper enclosure is slightly greater than exp(-1), as outward rounding requires, but remains strictly below 2/5.

G(z)=1-(1-z)^2/(2z^2) is increasing on (0,1] and is negative for 0<z<sqrt(2)-1. A smaller positive archived input therefore fails the first update as well. If rounding yields zero, the positive-domain recurrence is unavailable; it is not a physical gaplessness claim.

## Exact arithmetic audit

The degree-128 positive Taylor polynomial is a lower bound on exp(x). The first omitted term has degree 129; all subsequent ratios are bounded by x/130<1 for x<=16. Summing that geometric majorant gives a valid upper remainder. Reciprocation swaps endpoints. `down` and `up=-down(-x)` round in the correct directions on the decimal rational grid.

The low-beta branch uses a lower enclosure for exp(-B), making its inverse denominator an upper bound. The Gaussian branch clips its exponent to min(x,1), which only weakens the upper bound. All final acceptance comparisons are exact rational comparisons.

## Independent numerical corroboration

`audit/check_hoeffding_independent.py` uses mpmath at 100 decimal digits, independently evaluating the analytic expression rather than the implementation's Taylor arithmetic. It checks:

- Both models, N in {4,8,16}, coupling at cutoff and twice cutoff: 12 cases.
- 1,000 beta samples per case on [0.05,50].
- The unique stationary maximum by 400 bisection steps on the derivative of log J. The derivative is strictly decreasing because its derivative is -14*b^2*N^2 - 8*N*c*exp(-beta)/(1+c*exp(-beta))^2 < 0.
- 161 exp enclosure points from 0 to 16.

All passed. Numerical stationary maxima at the smallest cutoffs and N=4 are approximately 0.1545094417536522551 for the bilayer and 0.1351898136124226841 for large-D. These are corroboration, not the all-beta proof. Full output: `audit/hoeffding_independent_results.json`.

## Forecast issue and resolution

Original reproducer:

    forecast_seed_size([
      {'linear_size':2,
       'defect_upper':Decimal('0.100000000000000000000001'),
       'evidence':'certified_bound'}], Decimal('0.1'))

The original function rounded both numbers to float 0.1 and incorrectly returned `TESTED_SUFFICIENT_SCALAR_SEED`. The corrected function preserves rational comparisons and returns `INSUFFICIENT_PILOT_DATA`, with no tested sufficient size.

Current scope is appropriately limited: successful input labels are caller-supplied certified scalar bounds, not independently reverified; physical transfer and finite-size bridge hypotheses remain unverified. Fits are explicitly heuristic and never establish true minimum size, uniform gap, or physical gaplessness. Comparing empirical defects from incomparable model/shape/optimization protocols remains a caller responsibility, documented as an assumption.

## Additional CLI checks

Added independent regressions that mutate checkpoint source provenance without editing code and require resume refusal, and that certify the 81-dimensional large-D example through complete Sz-sector coverage. Both pass. All 14 CLI tests pass; log: `audit/cli_regression_results.txt`.
