# Ordinary bilayer g=.09 frontier check

Updated 2026-10-10 15:19 EDT / 19:19 UTC.

No scalar proposal succeeded on the tested finite temperature grid. The new exact physical inputs remained producer candidates awaiting independent point-specific replay. This finite-grid result does not exclude other temperatures or establish physical gaplessness.

All three seed patches, 4×4, 8×4, 8×8 rungs, pass ground identification and full
low-band separation. The largest omitted-band cutoff is 1.12 and the largest
triplet Ritz upper is .839832551909, leaving a margin of .280167448091. Thus the
current failure is at the scalar/finite-temperature stage, not the certified
band-count stage.

The input construction uses saved g-independent geometry and exact polynomial
evaluation of the existing affine translated-vector family. See
`POLYNOMIAL_INPUTS.md` for the explicit degree proof and the required removal of
the g-dependent integer normalization. No physical support or higher moments
are generated. Peak producer RSS was below 94 MiB. The scripts pin one CPU and
set a 1 GiB virtual-memory cap.

`joint_scan_g9d100.json` scans β=5,…,25 by .05 across the three distinct axis
orders. It checks ordinary conversion, up to six complete order-preserving
cycles before conversion, and up to ten coupled canonical/joint cycles. None
has a successful floating proposal. Selected strongest partial paths are
replayed with exact directed arithmetic. The new joint scalar lemma is frozen
separately in `../joint_trace_bootstrap` and is under independent review.

Full spaces are 4^16, 4^32, and 4^64. The original ground trial dimensions are 11,29,29.
The optional filtered ground vector lies in an implicit two-vector Krylov
span. Retained full low-band counts are 49,97,193. These are different notions
of dimension. None is a full-Hilbert diagonalization.

To reproduce the calculation from the repository root, run

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python research_20261010/low_band/frontier_g009/build_inputs.py
python research_20261010/low_band/frontier_g009/scan_joint.py
```

These overwrite only this producer directory. Do not rerun in place after the
freeze. The first development attempt had a harmless Python Fraction input
type error before any polynomial result. Its traceback is retained in
`first_attempt_type_error.log`. The corrected producer run completed all inputs.
