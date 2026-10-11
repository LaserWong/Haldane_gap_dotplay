# Saved-input seed error budget at g=.105 and .11

2026-10-10 22:51 UTC / 18:51 America/New_York. Producer study awaiting independent review. Conditional targets are not physical gap certificates.

## Scope and fixed reference startup

Use the accepted ordinary-bilayer physical polynomial identities and the newly reviewed frontier witnesses. All calculations keep the exact periodic normalization H'=Q+(g/2)A. Four inverse temperatures8,9.4,11,13 are examined; no all-temperature exclusion is claimed.

The reference sufficient startup is the exact J1,J2,C0 triple of the g=.102 point at beta9.4. Its three values are approximately .857848851705,.836701244369,.949331210921. If new certified inputs at the SAME beta dominate all three, monotonicity of G, transport, joint recurrences and direct finite windows carries the accepted reference path over. New-g short-size bounds remain separately necessary. Here the exact hypothetical path is also replayed afresh, with rational exponential witnesses.

Write the normalized denominator traces as

 U_N(b)=exp(b delta_N)+O_N(b)+R_N(b),

where delta_N=rho_N-ground_lower_N, O is the complete retained odd band and R is the counted omitted tail. Physical heat traces retain every state through the accepted oscillator counting comparison. For a largest-numerator Rayleigh improvement epsilon, J1 and C0 multiply by exp(2 beta epsilon), while J2 multiplies by exp(4 beta epsilon).

The exploration substitutes one component at a time: zero ground widths, odd Ritz endpoints in place of lower endpoints, complete odd-band removal, or omitted-tail removal. These are deliberately optimistic HYPOTHETICAL substitutions, generally not physically valid trace bounds. In particular zero ground width at a non-eigenstate Rayleigh mean may force a ratio above1, demonstrating an inconsistent hypothetical input. No such input is promoted to a certificate.

## Main numerical budgets

At beta9.4, the important twice-temperature normalized contributions are:

 g=.105: N16 ground1.04800310, odd2.9673e-6, tail7.91e-10;
          N32 ground1.02221261, odd5.5990e-5, tail5.47e-9.
 g=.11:  N16 ground1.09502251, odd3.9597e-6, tail1.49e-9;
          N32 ground1.07819230, odd2.8316e-4, tail1.15e-8.

The ground-width effects dominate these twice-temperature trace errors. At the original temperature, odd contributions are approximately .00779/.00879 for N16 and the tails .000977/.001344. Removing odd/tail contributions alone does not start the tested paths; neither idealizing one ground component alone does. These latter failures are bounded floating diagnostics, not exclusions of all methods or temperatures.

### Numerator-only sufficient targets

With the old denominators fixed, exact sufficient decreases of the saved N64 Rayleigh mean are

 g=.105: epsilon=.0026005306;
 g=.11:  epsilon=.010131571.

Each is the least multiple1e-10 accepted by the three fixed reference-ratio inequalities. The preceding grid point fails at least one inequality with an outward exponential enclosure. targets.json records these witnesses and hypothetical exact all-integer paths.

Reoptimizing the existing43D numerator basis gives real, exact rational Rayleigh improvements .0016235926345 and .0059086054849. Exact positive-LDL tests enclose the minimum of this entire saved43D generalized Rayleigh problem within1e-8 of the new trial values. Thus this43D space cannot attain the selected numerator-only sufficient targets. This does NOT prove that no43D bootstrap certificate exists, nor that the targets are necessary for all orders, temperatures, windows or denominator improvements.

### Joint sufficient targets after cheap reoptimization

Reoptimize only the existing11D N16 auxiliary Temple trial and43D N64 numerator, using their accepted exact matrices; no new physical contraction is required. To dominate the reference startup it suffices to obtain the following ground widths relative to these stored pivots:

 g=.105: delta16<=.001201, delta32<=.000976;
 g=.11:  delta16<=.001042, delta32<=.002732.

Both are explicit componentwise sufficient targets, not necessary budgets. Exact bisection brackets the largest width satisfying the assigned reference ratios; downward rounding to six decimal places gives the displayed simple caps. endpoint_ranges.json saves the current exact admissible intervals [ground_lower,rho] before and after the cheap reoptimization. All original odd bands/tails remain unchanged.

For any trial with mean R<a and full second moment B, its Temple lower exceeds a proposed lambda only if

 <H'^2>-(a+lambda)<H'>+a lambda<=0.

The exact compressed matrix B-(a+lambda)A+a lambda G is positive definite for both proposed N16 endpoints, as witnessed by11 positive rational LDL pivots. Therefore the WHOLE saved11D space cannot attain those selected endpoints using this fixed-cutoff Temple method. It does not exclude another scalar path or cutoff method. The already available16D third-moment trial space is the smallest saved enlargement beyond11D.

For an optimized43D N32 Rayleigh vector with mean R_new and target lower lambda32, the required COMPLETE variance is

 variance <= (R_new-lambda32)(r2-R_new).

At g=.105 this gives .00039663744641237324. The current fixed-vector complete variance is .0017074706303877541, but the optimized vector has a different mean and potentially different variance. Its coefficients and exact Rayleigh value are saved in joint_targets.json. The required target ground lower is approximately -.28003060136814.

At g=.11 the resulting variance budget is NEGATIVE, -.00013286490564076858. More directly, an exact physical trial mean -.30788032248132 lies BELOW the proposed ground lower -.30778705259964. Since E0<=that trial mean, the chosen joint target is incompatible with the physical inputs and is DISCARDED. It must not motivate a residual contraction. This only discards that sufficient target allocation, not the coupling or every possible certificate.

## Temperature/order/window versus trial dimension

The time-first path already uses the newly accepted stronger direct2D finite-window lemma. Reoptimization in the existing spaces still fails the bounded test at beta8,9.4,11,13. The alternative permitted xty startup, with correctly changed J2 denominator geometry/temperature, also fails the same four-temperature screen (order_comparison.json). This suggests physical input improvement is more useful than another tiny temperature adjustment, but is not an all-temperature or all-order obstruction.

## Full residual obligation and cost gate

The optimized43D N32 candidate is supported in q0,2,4,6. Its COMPLETE H' image includes q8. A projected residual or small q<=6 part cannot certify the target. The accepted exact hard-core commutator engine evaluates the full q8 norm as CM norm plus the signed q6 commutator expectation, retaining every negative/cross term and the nonzero image where M itself vanishes.

The existing matching8x4 run processed4,495 fixed-origin q4 supports and169,911 q6 supports in3.51709 seconds, peakRSS7,808KiB. The geometry and support remain identical for the new coefficients. A conservative approved re-evaluation budget is40CPU seconds and100MiB, with the same exact normalization and integer-overflow guards. No such contraction is part of this frozen error-budget study; it must be saved and audited separately.

The saved4x4 enlargement has16 columns, not43. The analogous fixed-origin q4/q6 support counts would be C(15,3)=455 and C(15,5)=3003, respectively, versus4,495/169,911 for8x4. This is a cost estimate, not a completed full-residual result. Any actual enlargement must retain its complete q8 obligation and verify the same structural identities.

## Reproduction and resources

All scripts write only in this directory. CPU3, one numerical-library thread,600CPU-second/700MiB per-job caps. Small11D/43D eigensolvers propose rational vectors; exact Rayleigh evaluations, LDL pivots and rational exponential witnesses carry the accepted algebra. No full ED or new large physical contraction was performed. Frozen source/data dependencies are hash pinned. Study conclusions remain pending independent review.
