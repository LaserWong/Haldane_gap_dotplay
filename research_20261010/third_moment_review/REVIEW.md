# Independent exact-third-moment review

Updated 2026-10-10 17:18 America/New_York (EDT) / 21:18 UTC.

## Verdict

PASS: the new exact X/Y/Z contractions, original-trial third moment, rational two-vector filter, enlarged numerator Gram/Hamiltonian matrices, exact Gram ranks, base M5, and both separate g=.09 all-integer scalar certificates.

For the ordinary periodic spin-1/2 square bilayer, with unit rung exchange and straight intralayer exchange g=.09, every integer square side L≥2 has a unique ground state and gap at least **0.027330086079**. This uses the enlarged numerator search. The two-vector alternative independently gives **0.001111944974**.

The complete proof and assumptions are in `PROOF.md`; exact results are under `results/`.

## Dimensions and retained information

| Rung geometry | Physical spins | Full Hilbert dimension | Original search rank | Enlarged exact rank | Retained numerator states |
|---|---:|---:|---:|---:|---:|
| 4×4 | 32 | 2^32 | 11 | 16 | 1 |
| 8×4 | 64 | 2^64 | 29 | 43 | 1 |
| 8×8 | 128 | 2^128 | 29 | 43 | 1 |

The enlarged vectors have q≤6 support. The largest-seed Rayleigh upper bounds in H′=H+3N/4 units are −0.4062623288761818 for the two-vector state and −0.4067853483943845 for the enlarged state. These displayed decimals are not the certificates; the accepted values are exact fractions in `matrix_and_rayleigh_replay.json`.

The accepted scalar certificate uses the new 43-dimensional search only for the largest 8×8 numerator. The reused 4×4 and 8×4 denominator ground searches remain 11- and 29-dimensional; their retained low bands contain 49 and 97 states (one ground plus 48 and 96 odd triplet states), with unchanged bounds for all omitted states. The new 16- and 43-dimensional smaller-geometry Rayleigh searches are checked but are not substituted into those denominators.

The new numerator needs only its exact G/A matrices and a rational coefficient vector. No filtered-state residual, base M6, new denominator lower bound, or additional retained state is inferred. The smaller-seed denominator matrices, spectral intervals and complete tails remain unchanged.

## Independence and provenance

No producer Python module is imported or executed. A fresh C++ auditor uses direct local bond forms and exhaustive q=6 subset enumeration instead of the producer's edge-mask generation and second-image contraction. All old F/S/V/W and new X/Y/Z agree at every geometry, including all 7,028,847 fixed-origin q=6 supports at 8×8. Every small full-support contraction agrees with the fixed-origin result.

A separate rational block builder reproduces all old G/A/J and base M0–M4, new H³ and base M5, every exact Gram pivot and each rational Rayleigh quotient. Direct spin-derived sparse tests independently reproduce all geometry entries and full enlarged G/A at 2×2 and 4×2. Every q=4/q=6 matching metric and local recoupling rule is checked. Exhaustive small translation-orbit tests include stabilizers of size two and four.

The final exhaustive 8×8 replay took 111.653 seconds with 210,304 KiB peak RSS, within the stated cap.

Physical producer seal: `PHYSICAL_MANIFEST.json`, SHA-256 `7a6d8ea0cdd15323289934c6ca851c7c1ac5340ef938f757f3df55394b51d2ce`.

The separate scalar producer seal and all copied inputs are pinned in `INPUT_SHA256.json`. Existing independent physical and scalar-lemma dependencies are pinned in `PRIOR_REVIEW_SHA256.json`. Prior accepted reviews were checked in full before their needed files were snapshotted. The scalar replay reuses only unchanged, hash-checked independent exact-arithmetic functions. It rechecks both all-size certificates from their new numerator terms rather than inheriting the producer's success flag.

The active project is an extracted shared snapshot without Git metadata. This review writes only its own directory and changes no frozen input, root status, GitHub state or earlier review.

## Reproduction and limits

Run `bash REPRODUCE.sh`. It verifies the finished manifest before replay and all input hashes afterward. Reproduction is pinned to one CPU, sets BLAS/OpenMP thread counts to one and caps address space at 1 GiB. It rebuilds the C++ auditor from source and writes only this review directory. Timing fields and logs can change on reproduction, so the original review manifest is checked before they are overwritten.

This accepts a discrete g=.09 result, not a continuous-coupling extension. The g=.10 producer files are outside this review's scientific acceptance. No all-temperature exclusion, optimality, physical-gap value, infinite-volume uniqueness or maximum-patch full-spectrum calculation is claimed.
