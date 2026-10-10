# Stable g=0.03 checkpoint

2026-10-10 13:36 America/New_York / 17:36 UTC.

All existing g=0.03 certificate inputs and completed result files are now frozen. New coupling work is isolated in `frontier/`.

The complete low-band theorem, all three patch Gram/residual reconstructions, number-sector spectrum bins and the β=9.11 correlated exact replay have passed independent review. The independently reproduced gap is 0.004333053946. The parent’s finite-window bridge extends this to every integer square L≥2. The reviewer requested refreshing the root bridge’s source hash after the third temperature entry was written. This has been completed by the parent.

The stronger symmetry-ground variant gives an exact candidate gap of 0.009195338283 for L≥128 directly. Its immutable single-record input is `symmetric_correlated_beta909d100_FINAL.json`. The parent’s finite-window bridge also passes for all L≥2, saved as `../root_review/finite_window_symmetric_correlated_beta909d100_FINAL.json`. Independent review of the optional symmetry-ground source contraction and the final trace/bridge chain remains pending at this checkpoint.

The distinction between these two statuses matters. The second number must not be described as independently reviewed until that final review returns.

Independent audit entry points:

- `../low_band_review/REVIEW.md`
- `../low_band_review/NUMBER_AND_BRIDGE_REVIEW.md`
- `../low_band_review/reviewed_input_manifest.json`
- `../low_band_review/refined_correlated_results.json`
- `../root_review/FINITE_WINDOW_INTERPOLATION.md`

`STABLE_MANIFEST_1736.json` hashes all direct files in this directory at this checkpoint, excluding the manifest itself. It does not include the later `frontier/` work or certify any mathematical claim by itself.
