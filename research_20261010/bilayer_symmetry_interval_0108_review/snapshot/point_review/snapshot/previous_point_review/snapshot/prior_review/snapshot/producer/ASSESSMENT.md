# Stronger square-symmetry scalar pilot at g = .11

Updated 2026-10-11 00:35 UTC / 2026-10-10 20:35 EDT.

## Result

Using the existing accepted physical inputs and the newly proved square-symmetry window/recurrence, exact cached arithmetic gives:

- beta0=47/5: gap >= .066142574905 on every integer square L=8,...,16, and >= .020227124817 on L=16,...,32.
- beta0=10: corresponding bounds .063807423673 and .016865809130.

The accepted short-size theorem on 0<=g<=.15 gives a gap >.050426624396 for L=2,...,7. It therefore combines with the first pair to give the exact finite-size candidate **.020227124817 for every integer 2<=L<=32 at g=.11**, subject to the separately assigned independent numerical review. This is not an all-size certificate. The accepted all-size frontier .105 is unchanged.

The reported .4004802356 thermal-purity failure at the second beta0=10 window is repaired to .662539645986775 by symmetry. At beta0=9.4, the old .4499780537 becomes .681470938958503. Thus that particular earlier window failure was not an obstruction inherent in the physical inputs.

## What still fails

The actual compact recurrence leaves its useful domain before a positive third square window can be certified. The bounded 9x9x9 dyadic edge closure includes every adjacent exchange, same-axis squaring/monotonicity, and x/y reflection, with mixed dyadic temperature indices. None of the seven cached temperatures 8,9.4,10,11,12,13,15 supplies a standard small-defect starting state. At spatial side32, the best tested mixed-temperature uniform square window is only about .273235 (beta0=9.4), below one half.

These are bounded floating diagnostics, not an all-temperature, all-schedule or physical no-go. The closure is valid but not proved complete. The old all-six-order small-seed obstruction concerns 2x2/4x2/4x4 at g=.04/.05 and does not exclude this new square-symmetric method or these larger seeds.

## Quantified next target, explicitly hypothetical

Holding every other physical bound fixed, raising the current 8x4 shifted-ground lower endpoint by **.0002743** at beta0=9.4 is sufficient for the new recurrence. The exact hypothetical target is approximately -0.3080696165627645. A fully directed rational replay then passes all dyadic windows and the standard asymptotic theorem at side32768. The minimum scalar gap along this hypothetical route is .000137393606, below the accepted short bridge.

At beta0=10, a sufficient hypothetical ground-lower gain .0002847 gives an asymptotic onset16384 and minimum scalar gap .000212810132. The exact targets and every intermediate fraction are in exact_results.json. Neither improved ground lower has been physically proved. These are sufficient improvement budgets for this particular recipe, not necessary conditions, actual ground energies, or globally optimal target values. Previous fixed-pencil exclusions cannot automatically be extended to these different targets.

## Arithmetic and provenance

All three source seals specified by the parent were verified, including every file in each manifest: scalar161881ac..., complete57Dmatrix874c87f..., and endpointfc205510.... The current4x4 ground lower comes from the accepted16D point witness; the8x4 lower from the accepted57D point witness. The cached43/57D physical certificates retain49/97 low states in denominator traces and one upper-energy state in the largest numerator. Existing odd reference floors and complete omitted tails remain included. No new physical contraction, eigensolver, support, or trial-vector optimization was performed.

exact_pilot.py imports no producer module. It reconstructs the same physical scalar ratios from frozen cached spectral data, verifies agreement of its floating diagnostic with the previous sampled ratios, then uses independent384-bit directed exponential enclosures,60-decimal downward rational rounding and integer-square-root witnesses. Every finite-window and asymptotic gap is accepted by a rational exponential inequality. Snapshot inputs and independent proof/physical-review dependencies are hash-pinned.

All computational work used CPU2, one thread and256MiB caps. The main closure run used10.77CPU seconds, the mixed-index refinement .66CPU seconds, and exact actual/hypothetical replay22.98CPU seconds/12.3MiB. Including a tiny underflow-guard repair, this pilot used less than36CPU seconds of its120-second budget. A subsequent intermediate-coupling extension, if authorized, must be recorded separately rather than rewriting this .11 freeze.

Reproduce the exact calculation with `python exact_pilot.py`; it verifies the frozen input and dependency hashes first. Timings are diagnostic. No root-status, prior sealed result, or GitHub file was modified by this pilot.
