# Independent chain frontier review above 0.2

Updated 2026-10-10 17:31 EDT (America/New_York) / 21:31 UTC.

## Accepted results at isolated couplings

For the periodic spin-one alternating chain with strong exchange one and all M weak links retained, the following rigorous bounds hold for every integer M≥2. Each finite volume has a unique ground state.

| g | Uniform gap lower bound | Initial β | Time/canonical cycles | Asymptotic onset M |
|---|---:|---:|---:|---:|
| .21 | .101607534008 | 8.3 | 3/0 | 64 |
| .22 | .065580452251 | 8.55 | 3/1 | 128 |
| .225 | .045509923956 | 8.7 | 4/1 | 256 |

The [8,16] finite window limits all three bounds. The results apply at the listed couplings and do not determine a continuous interval, an optimal certification threshold, the actual gap, a physical transition or infinite-volume uniqueness.

## Verification

- Reconstructed the physical spin-one matrices and nine orthogonal rational Clebsch–Gordan columns from their explicit physical coordinates.
- Enumerated the complete 67-dimensional reference projector E<3: one vacuum, twelve single triplets and fifty-four two-triplet states. All twenty single quintets have energy 3 and remain in the 6,494-dimensional complement.
- Reconstructed all 4,489 entries each of K, full J and residual Gram R, with the correct diagonal Gram normalization. R was computed directly from leaked physical configurations, then checked against J−KG⁻¹K.
- Full weak-action union: 786 configurations. Residual union: 719 configurations, including 556 containing quintets. The reference dimensions are unrelated to MPS bond dimensions.
- Independently verified local 81-dimensional rational positivity and all 17 counted Schur thresholds at each of .21, .22, .225 and .25. Rational symmetric congruence is independent of the producer's integer fraction-free inertia routine. No whole Ritz-band isolation, commuting-compression assumption or guessed spin multiplicity is used.
- Replayed each new M=4 ground vector's full physical action, residual and Temple interval using the sealed earlier independent physical verifier. Its trial dimension is 1,099 and full action support is 1,107.
- Evaluated only the sealed two-vector M=8 first-moment matrices for the largest seed Rayleigh bound: physical dimension 43,046,721 and trial support 43,294. No additional M=8 physical input was required.
- Replayed all 72 saved scalar paths with independent directed 384-bit exponential enclosures, including 378 finite-window checks and every M=2,3 bridge. Windows meet the terminal all-integer theorem without holes, including the initial odd sizes M=5,7.
- Ten deliberately corrupted inputs are rejected, and four singular/2×2-pivot cases test the inertia routine.

The trace bound is valid for every β≥0. The positive gap certificates select the displayed temperatures and their recorded paths. The complete trace accounts for exactly 1+66+6494=6561 ordered states.

## Files and reproduction

`PROOF.md` gives the counted Schur, complete-tail, thermal and all-integer arguments. `audit.py`, `physical_core.py` and `scalar_core.py` provide the independent executable verifier, with no producer mathematical imports. Physical and scalar helpers inherited from the earlier accepted independent review are copied transparently. New inertia elimination and expanded-projector logic are separately implemented.

`SUMMARY.json` and `review_g*.json` hold the exact all-size results and all saved path replays. `physical_endpoint_review.json` additionally verifies the .25 physical endpoints without claiming a positive gap there. `physical_premises.json` records complete counts and supports. `adversarial_tests.json` records rejection tests. `snapshot/` preserves producer input bytes. The producer freeze files and `PROVENANCE.json` record their seals and the preserved accepted predecessors.

Run `REPRODUCE.sh` from any directory. It verifies the seal, runs a clean temporary sibling replay and removes only that temporary directory. It does not alter producer or predecessor packages. One CPU (default CPU4), one BLAS thread, and a 1 GiB address-space cap are enforced. Initial full acceptance took 68.51 seconds and peaked at 28.89 MiB RSS. This is an exact-arithmetic executable mathematical certificate, not a proof-assistant formalization.

The review used an extracted tree without Git metadata and changed no root, producer or remote files. Publication was outside its scope.

## Separate accepted recipe obstruction at .25

`obstruction_review.json` and `audit_obstruction.py` independently verify a strictly recipe-scoped all-temperature failure. For the saved .25 inputs, 1,200 exact intervals cover β∈[0,12], followed by an analytic β≥12 tail. The largest interval bound on the second purification argument is .4970915063143724<1/2. The tail is below .472341. Therefore this particular route cannot certify its required first [8,16] window at any temperature. This is an upper bound on the certificate recipe's output, not on actual physical purity. Improved seed inputs, other inequalities and independent short bridges remain open.

The final producer manifest SHA-256 is f3e38ff6b3106078c1a4109db83722e1220e5214fc3e6b3c9aaea5920e1074bc. All 48 sealed producer files and all cited predecessor seals passed provenance verification.

The clean sibling replay completed successfully at 21:31 UTC, including exact .25 physical endpoint reconstruction and the separate all-temperature recipe obstruction. `ACCEPTANCE.json` is the final machine-readable acceptance.
