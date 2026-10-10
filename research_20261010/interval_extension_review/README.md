# Accepted continuous ordinary-bilayer extension

Updated 2026-10-10 15:16 America/New_York (EDT, UTC−4) / 19:16 UTC.

Independent exact replay accepts the full interval 0≤g≤0.078 with unique finite-volume ground state and gap ≥0.001945771244 for every integer square side L≥2. The fifteen new pieces covering .07≤g≤.078 separately have gap ≥0.002006633957. Together with the older sixteen pieces, the exact union has thirty-one closed intervals.

- [Independent proof, assumptions, provenance and limits](REVIEW.md)
- [Exact per-interval results and accepted union](results/SUMMARY.json)
- [Machine-readable status](REVIEW_STATUS.json)
- [Producer freeze](PRODUCER_FREEZE.json)
- [Physical polynomial reconstruction](results/matrix_reconstruction.json)
- [All auxiliary vector checks](results/auxiliary_exports.json)
- [Corruption guards](results/rejection_guards.json)

One ground contribution per patch, no excited trial family. Original trial dimensions 11/29/29; largest augmented dimension at most 30, q≤6. Largest physical space 2^128. Existing full second moments are required at the largest patch; no higher moments are used.

Reproduce with `bash REPRODUCE.sh`. Verify the completed seal first using `python verify_manifest.py`. One CPU, 1 GiB address-space cap. Older packages and producer files are untouched. This is a local independent review; it does not imply a remote publication.
