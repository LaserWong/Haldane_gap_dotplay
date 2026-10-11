# Actual-input scalar tests and conditional ground target

All new physical uses remain conditional on the complete8x4 matrix audit. No new unconditional gap or higher-coupling interval is claimed.

## Small actual-input set

Seven temperatures beta8,9.4,10,11,12,13,15 were tested at g=.11 and.12, using the actual exact16D/43D pencil lower endpoints, exact rational57D numerator upper, accepted fixed-z=.1 odd witnesses and full omitted-tail count. The odd lower endpoints are safely improved to their maximum with the unrestricted global r1 reference after unique even-ground identification. The independently accepted L2..7 short bridge through.15 gives gap .050426624396 and is not a bottleneck here.

No tested actual-input path yielded a certificate. These failed-path diagnostics use floating scalar evaluation and only describe the finite temperature set, not a theorem that every parameter choice fails. At beta10,.11 passes the first size8..16 window but fails the next size16..32 window, with interpolated purity .3986621685<=1/2. At beta9.4 its next-window purity is .4484721938. At .12,beta10 fails the first window, with no positive accepted interpolation lower. Minimum encountered canonical defect among this tested set is attained at beta10 for each coupling.

## Correctly normalized error contributions

Trace components are rebased to the best exact rational ground upper, rather than interpreting a poor old normalization pivot as physical uncertainty. Rebasing leaves every ratio unchanged. At beta10,g=.11:

-4x4 at beta: ground1.000208067, odd.005043208, tail.000536434.
-4x4 at2beta: ground1.000416177, odd.000001437, tail2.4e-10.
-8x4 at2beta: ground1.009315541, odd.000044359, tail2.0e-9.

At beta10,g=.12:

-4x4 at beta: ground1.000443147, odd.007180413, tail.001054564.
-4x4 at2beta: ground1.000886490, odd.000002906, tail9.2e-10.
-8x4 at2beta: ground1.019192525, odd.000368776, tail9.9e-9.

Thus8x4 ground uncertainty dominates its denominator excess. The4x4 hotter trace is dominated by actual low-band weight; deleting that weight entirely is an unphysical but informative upper-limit test of what odd-bound improvement could accomplish.

At .11,beta10, setting ONLY the8x4 ground uncertainty hypothetically to zero yields a small-defect candidate. Removing all odd contributions while leaving grounds unchanged does not; replacing the odd eigenlower endpoints by their Rayleigh uppers also does not. At .12, no single idealized replacement of ground16,ground32,both grounds,all odd contributions,odd Rayleigh endpoints or omitted tails gives a candidate at beta9.4 or10. These are sensitivity tests, not physical trace certificates.

## Actionable sufficient target and finite-basis limitation

At g=.11,beta9.4, a hypothetical8x4 ground interval width .0000289855, i.e. lower endpoint−.3079106277352142 relative to the exact best upper, suffices for an EXACT conditional all-size scalar path with gap .000255993196. All other inputs are unchanged. The necessary improvement over the current saved pencil lower FOR THIS SELECTED TARGET is .0004346354293. The actual current uncertainty is about.00046362093.

At beta10, width .0000187367 gives an exact conditional path with gap .000186385898. These are sufficient target examples, not necessary conditions for all possible bootstraps, and their hypothetical ground lower is not certified.

For both selected lower targets ell, target_limit.json saves43 strictly positive exact LDL pivots for J−(a+ell)K+a ell G at the fixed directed even-sector cutoff a=r2(.11). Consequently no current43D vector can supply a negative Temple-pencil witness at these targets, conditional on the complete physical matrix. This is a finite-space/fixed-cutoff limitation, not a no-bootstrap or physical-gap obstruction. It strengthens the case for additional8x4 ground directions over more coefficient tuning or an odd-only contraction campaign.

## Resources and provenance

No new physical contractions, no full ED and no broad parameter grid. CPU3,120CPU seconds/256MiB per bounded scalar/LDL batch. Source modules are read via selected AST definitions to avoid unnecessary heavyweight optimizer imports. Actual-input scans, exact conditional paths and exact LDL limitations are distinguished in the saved records. All predecessors remain unchanged.
