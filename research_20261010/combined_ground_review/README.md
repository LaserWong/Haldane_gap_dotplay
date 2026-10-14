# Combined ground endpoint review

Updated 2026-10-10 15:15 America/New_York (EDT, UTC−4) / 19:15 UTC.

The review checks the ordinary periodic spin-1/2 square bilayer with unit rung exchange. It independently verifies 42 patch recombinations, 42 selected orders, 30 successful full-band certificates, and 11 largest-ground-only certificates. Each successful result covers every integer square side L≥2.

The newly accepted g=0.08 bound is 0.023243965748 at initial β=197/20, using time–x–y followed by canonical transport. Its largest-ground-only numerator gives 0.023241913957. The latter still uses original second-moment data to certify the filter.

- `REVIEW.md`: physical scope, endpoint-combination theorem, dimensions, trace cancellation, order transport, and every finite-size bridge
- `REVIEW_STATUS.json`: terminal machine-readable verdict and strongest accepted results
- `results/accepted_certificates.json`: all 30 exact accepted records
- `results/ground_only_certificates.json`: all 11 exact numerator-only alternatives
- `results/selected_failures.json`: 12 selected failures, with no all-temperature claim
- `results/patch_review.json`: all 42 physical input and unchanged-tail checks
- `results/bounded_grid_review.json`: independent 21,042-sample diagnostic
- `INPUT_SHA256.json` and `PRIOR_REVIEW_SHA256.json`: exact consumed inputs and eight prerequisite independent seals
- `REPRODUCE.sh`: complete standard-library replay, ≤1 CPU and 1 GiB, outputs in a new temporary directory

Producer files are preserved unchanged. This review makes discrete-coupling claims, not a continuous-coupling theorem or a physical optimality claim. The extracted shared tree has no Git metadata.
