# Diagnose the ordinary bilayer g=.10 startup

2026-10-10 17:37 EDT / 21:37 UTC. Exact endpoint candidates and conditional diagnostics; independent review required. No g=.10 gap certificate.

## Actionable result

The 8x4 denominator ground interval is the dominant tested bottleneck. At beta=9.25, its upper trace at physical beta=18.5 contains ground factor 1.0512446515, odd-band contribution .00003103453, and counted tail .000000004368. In contrast, the 4x4 trace at physical beta=9.25 has ground excess .00315680, odd contribution .00809050, and tail .000903107. The joint txy ratios amplify ground error, especially in the later stages.

Conditional one-at-a-time tests on beta=5..20 by .05, at most ten cycles:

| Hypothetical change | Successful grid points | Best diagnostic asymptotic score |
|---|---:|---:|
| None | 0 | — |
| Small ground lowers set equal to saved trial uppers | 241 | .08733855 |
| Only odd lowers set equal to saved trial uppers | 0 | — |
| Only counted tails deleted | 0 | — |
| Only 4x4 ground interval completely closed | 0 | — |
| Only 8x4 ground interval 50% closed | 0 | — |
| Only 8x4 ground interval 75% closed | 99 | .03577912 |
| Largest numerator improved by .002 | 0 | — |
| Largest numerator improved by .003 | 75 | .02960285 |

These are conditional sensitivity diagnostics, NOT valid spectral replacements or rigorous gap bounds. In particular, a trial upper cannot simply become a lower, and an omitted tail cannot be dropped. No finite-grid failure is an all-temperature exclusion. Scores are floating asymptotic proposal scores, not replayed all-integer-size minima.

The saved 8x4 interval is [-.255370784663,-.2526694417167282...], width .00270134294627. Closing 75% conditionally corresponds to lower approximately -.2533447774533. Exact positive-definite replay shows the existing 43D numerator optimum is already within 10^-10 of its saved upper, so coefficient retuning alone cannot obtain the ~.003 hypothetical numerator improvement.

## New exact ground candidates

A rigorous U=N(1+g) spectral upper and the existing unique-ground even-sector count make a negative (U-H')(H'-a)(H'-ell) expectation a ground lower certificate. It uses only base M0..M5, not M6. Exact witnesses yield:

- 4x4: -.126993368814, gain .0000846906642
- 8x4: -.255086154800, gain .000284629863
- 8x8: -.517246809590, gain .0007066132366; ancillary only for this txy route

The two small improvements alone still give zero successful bounded startup proposals; best minimum defect drops .27240 to .22115. Exact positive-definite tests bracket the optimum of the endpoint-weighted affine-square class to 10^-10. More general M5 methods remain open. See PROOF.md for the sector-qualified theorem, full moment provenance, and restricted optimization statement.

## Files and reproduction

- diagnostics.json and followup_diagnostics.json: conditional scans and trace decomposition
- weighted_ground_*.json: rational coefficient vectors, exact quadratic moments, negative witnesses
- moments_*.json: exact old-space G/A/B/C and base integer M5
- patch_*.json: candidate denominator patches, unchanged odd bands and counts
- replay.py / replay_result.json: exact separate block-Hankel replay, no eigensolver
- weight_class_result.json: exact positive-definite class brackets
- numerator_floor.json: exact fixed-43D compression bracket
- INPUT_SHA256.json / INHERITED_SEALS.json: source pins and 810 checked inherited sealed files

Run `bash REPRODUCE.sh` from this directory. It verifies the freeze before writing replay results. Candidate generation, if desired, is `python weighted_ground.py`; floating scans are `python diagnose.py` and `python followup_scan.py`. All scripts disable bytecode, BLAS/OpenMP use one thread, CPU affinity prefers CPU5, and jobs cap address space at 1 GiB and CPU time at 300 seconds. Ground generation took roughly 2.2 seconds total; exact replays take seconds; no large contraction is run.

This extracted snapshot has no Git metadata. No root status, GitHub, or previous producer/review file was changed. Two development import-path mistakes and an early helper-loader recursion were corrected before successful replay; no scientific output from those failed attempts is used.

Next: independently review the new polynomial endpoints. Prioritize the 8x4 full residual/ground lower information if extending inputs, rather than additional odd-band or counted-tail effort for this particular route.
