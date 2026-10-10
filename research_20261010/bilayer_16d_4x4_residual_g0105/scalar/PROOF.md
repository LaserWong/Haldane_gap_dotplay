# Actual-input g=.105 all-integer point candidate

2026-10-10 23:00 UTC / 19:00 America/New_York. Exact producer candidate pending independent physical and scalar review.

The ordinary periodic spin-half bilayer at g=21/200 has the candidate all-integer square gap

 gap >= 31673112867/10^12 = .031673112867,

with a unique finite-volume ground for every integer L>=2. This is a discrete-coupling claim only. No hypothetical error-budget target is used.

## Physical inputs and trace normalization

Take the actual complete-residual ground lower from the new16D4x4 package and the actual complete-residual ground lower from the new43D8x4 package. The16D trial has complete q0,...,q8 image variance2.2505420524742475e-5; the43D trial has complete variance.0005240758184406096. The latter misses an earlier sufficient target, but its ACTUAL lower endpoint is used here.

Keep all48/96 existing odd-mode lower endpoints, with fixed trial parameterz=.1, their exact cutoff/count conditions and the entire omitted bosonic tail. Denominator retained counts remain49/97; denominator ground search dimensions are now16/43 and total ground-plus-odd trial dimensions64/139. The largest8x8 numerator is one exact rational Rayleigh state reoptimized in the existing43D space. Its physical Hilbert space remains2^128, and no largest-patch residual or full ED is required.

The exact trace pivots remain the old accepted/reoptimized trial means for convenient normalization. Changing only the ground lower is legitimate: replace exp(beta*(rho_pivot-old_lower)) by exp(beta*(rho_pivot-new_lower)). Odd and tail exponents stay relative to the same rho_pivot. Their unchanged values therefore still represent the same absolute-energy bounds. Every denominator record explicitly describes this override and identifies the actual complete-residual source and actual search dimension. Old variance metadata in a pivot record is not used to claim the new lower endpoint.

The correlated affine energy combinations in J1,J2,C0 are evaluated with these same pivots. Exact trace upper/lower arithmetic recomputes all three ratios. This is not an unchecked transplant of a target purity or a coupling extrapolation.

## Scalar and integer coverage

Best initial beta=47/5. The first full time-first state is at common square base n8 and physical beta94/5. Retain joint ratios, use valid order transport and exact raw/canonical recurrence. The new signed direct2D finite-window lemma covers eight windows:

 [8,16], [16,32], [32,64], [64,128], [128,256],
 [256,512], [512,1024], [1024,2048].

Their gap bounds are respectively .086476244644, .054648852724, .041340676866, .036043840688, .033995258132, .033172275743, .032773827535, .032533381801. The terminal canonical base is L2048 at beta24064/5, with0<u<=1/500 and an exact exp(beta*gap)*32u<1 witness. Its all-integer asymptotic gap is the final minimum .031673112867.

At the actual g=.105, the accepted short-size comparison is freshly evaluated for L2,...,7. The smallest short gap exceeds.239. Thus no integers are missing and no g<=.10 short certificate is reused outside its scope.

All square roots and exponentials are outward rational enclosures; recurrences are rounded downward. Four specific temperatures9.4,9.5,10,11 were proposed and all passed exact replay, with best result as above. There is no assertion of global temperature or method optimality.

## Reproduction

SCALAR_INPUT_SHA256.json pins all physical packages, saved reoptimized matrix trials, scalar implementations and predecessor dependencies. REPRODUCE.sh checks the scalar seal and dependencies, replays four paths to candidate_check.json, and compares every exact result. Each physical package has its own separate replay/seal. CPU3, one thread,600CPU-second/700MiB scalar budget. No new contractions occur in scalar replay.
