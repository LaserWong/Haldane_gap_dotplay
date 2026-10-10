# Ordinary bilayer g=.07 independent frontier audit

Updated 2026-10-10 14:51 EDT / 18:51 UTC.

PASS: at g=.07, Δ_L≥0.024790852531 for every integer square side L≥2, with unique finite-volume ground state. The separately verified xty route gives .009272103501.

All nine new physical patches at g=.07,.08,.10 pass independent ground/full-residual/translated-band reconstruction and complete-spectrum counting. The .08/.10 scalar failures are bounded-grid diagnostics only, not all-temperature exclusions or physical gaplessness results.

- [Full review and proof details](REVIEW.md)
- [Machine-readable verdict](REVIEW_STATUS.json)
- [Accepted all-size certificates](results/accepted_certificates.json)
- [Complete physical patch checks](results/patch_review.json)
- [Uniform L=2,…,7 comparison](results/short_size_review.json)
- [Selected exact failures](results/selected_failures.json)
- [Bounded grid diagnostic](results/bounded_grid_diagnostic.json)

Run `bash REPRODUCE.sh`; no remote writes occur. The frozen producer manifest is SHA-256 55b0ddf8e317c6953d0487a26880b075231d7fcc37c5a91a475a83b5a71dcb47, with 70 files. Prior reviewed coupling-independent geometry is reused only by matching sealed hashes. New physical moments, residuals, counting, scalar endpoints, traces, transport, and all-size bridges are independently replayed.
