# Ordinary bilayer g=.09 frontier check

Updated 2026-10-10 15:19 EDT / 19:19 UTC.

**Result: no successful scalar proposal in the tested finite grid.**
This is not an all-temperature exclusion and says nothing about physical
gaplessness. New physical inputs are exact producer candidates awaiting an
independent point-specific replay.

All three seed patches, 4×4, 8×4, 8×8 rungs, pass ground identification and full
low-band separation. The largest omitted-band cutoff is 1.12 and the largest
triplet Ritz upper is .839832551909, leaving margin .280167448091. Thus the
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

Full spaces are 4^16,4^32,4^64; original ground trial dimensions are 11,29,29.
The optional filtered ground vector lies in an implicit two-vector Krylov
span. Retained full low-band counts are 49,97,193. These are different notions
of dimension; none is a full-Hilbert diagonalization.

Reproduction from the repository root:

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python research_20261010/low_band/frontier_g009/build_inputs.py
python research_20261010/low_band/frontier_g009/scan_joint.py
```

These overwrite only this producer directory. Do not rerun in place after the
freeze. The first development attempt had a harmless Python Fraction input
type error before any polynomial result; its traceback is retained in
`first_attempt_type_error.log`. The corrected producer run completed all inputs.
