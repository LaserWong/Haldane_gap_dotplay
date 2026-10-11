# Independentg=.10825 point and scopedg=.1085 failure audit

## Accepted actual point

For the ordinary isotropic periodic bilayer, unit rung exchange andg=433/4000=.10825, every integer square sideL≥2 has a unique full-Hilbert ground and gap≥.001585809758. This is a point statement, not a continuous coupling extension.

Producer seald2ca461c0012053a6ea715cccd25c3d675c86f4c9839af600d36b878deb21039 is pinned. result.json contains exactly the.10825 successful point and.1085 failed diagnostic;g=.109 is untested. No floating optimizer or grid search is executed by the reviewer.

## New physical vectors and exact moments

For both saved couplings.10825 and.1085, both energy and pencil candidate vectors for each denominator are freshly contracted with the accepted21D4×4 and57D8×4 Gram, affine H′ and complete quadratic H′² matrices. Thus eight new ground candidates are checked. Every exact norm, mean, full second moment, complete variance, strict endpoint, reference cutoff and coupling-polynomial coefficient matches. Norms are positive, variance coefficient forms are PSD and point variances nonnegative.

For each strict endpointell and sector cutoffa=r2, the reviewer verifiesrho<r1<a, ell<rho−variance/(a−rho)<a, and <H′²>−(a+ell)rho+aell<0. Selection between energy/pencil candidates is compared using exact lower bounds. Floating eigenvalues and root brackets are proposals only. Complete H′² includes physicalq8 images and all cross terms; it is not projected H′ squared. The accepted basis preserves even-singlet symmetry.

Each new43D numerator vector is independently embedded throughU=R+M into the accepted split first-H geometry. Its norm and affine Rayleigh coefficients are rebuilt using the physical weighted8×8 pair graph and cached operator blocks. One numerator state is retained; no numerator residual is needed for an energy upper. The full physical Hilbert dimension is2^128.

## Counts, cutoffs and complete traces

At each coupling the reviewer freshly evaluatesr_q=(3N/8)(2g−1)+(3N/8+q)sqrt(1−4g). Positiver1−rho identifies the unique global ground. All fixedz=.1 odd-mode Grams, affine means and complete residual polynomials are reconstructed in exactQ(sqrt2). Positive Grams, variance signs and strict cutoff margins ensure all16/32 momentum directions, each with spin multiplicity3, lie belowr2. Together with the ground and full-Hilbert reference count, this bounds the second level of the full untruncated even-singlet sector byr2. It is not a full-Hilbertλ2≥r2 assertion.

The retained counts are49/97. Each odd lower ismax(r1,theta_lower−variance_upper/(r2−theta_upper)). All omittedq=2,…,N tails are retained with multiplicitybinomial(3N+q−1,q); total reference count covers at least4^N. Ground widths, odd energies and tails use the same verified energy-candidate trace pivot. The correlated combinations8e16−2u64,16e16−4u64,4e32−2u64 are rebuilt exactly.

## Successful scalar path

Atg=.10825,β0=19/2, the first square base is(8,8,19). The independent544-bit exponential engine reconstructs all three ratio seeds, which match the saved60-decimal lower bounds. Every raw/canonical state, common defect, window purity and gap is recomputed under the accepted square-isotropic recurrence with exact basepoint/temperature labels.

All eight finite dyadic windows from[8,16] through[1024,2048] passp>1/2 andexp(βγ)(1−p)<p. Odd integer sides are covered by the signed-transfer theorem. At terminal side2048,β=4864, the canonical defect satisfies0<u≤1/500 andexp(βγ)*32u<1 atγ=.001585809758. The accepted[0,.15] short bridge gives.050426624396 forL=2,…,7. The short, finite and asymptotic ranges therefore cover all integerL≥2 with no missing size.

## What theg=.1085 diagnostic proves

The reviewer reconstructs the physical bounds and exact ratio seeds for the savedg=217/2000=.1085 vectors atβ0=19/2, then replays every saved lower-bound state. Four windows pass their purity gate. At side128 the computed lower boundc is exactly the saved fraction, approximately.4352080278629311; its exact difference from1/2 is negative. The saved lower-bound finite-window gate therefore cannot certify the next window.

This is failure of this bound and this path. It does not prove the actual physical ratio is below1/2, does not disprove a gap, and is not a universal bootstrap obstruction. The producer reports no successful proposal on its finiteβ grid7…14 in steps.05; this floating grid was not independently rerun and is not elevated to an exact all-temperature exclusion. The reported best-path ranking is likewise not an optimization certificate. No result atg=.109 is claimed.

## Reproduction and resource scope

The source/matrix/physical proof chain is pinned through the accepted prior review. REPRODUCE.sh verifies all seals and reruns the exact vector, count, trace, successful path and selected failed path checks in a fresh directory. Observed runtime is under4CPU seconds and21MiB RSS onCPU4, within the120CPU-second/256MiB budget. No physical support contraction or work above the requested couplings occurs.
