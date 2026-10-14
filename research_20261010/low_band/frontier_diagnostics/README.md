# Saved-input frontier sensitivity diagnostics

Updated 2026-10-10 14:57 EDT / 18:57 UTC.

## Status

These are **floating, hypothetical sensitivity screens**, not rigorous gap
certificates, physical realizability claims, or all-temperature exclusions.
No new trial vectors or physical moments were constructed. All original frozen
`.08` and `.10` endpoint files remain unchanged.

The screen uses the ordinary spin-1/2 bilayer with unit rung coupling, periodic
square/rectangular rung lattices, and the existing 4×4, 8×4, 8×8 seeds. It scans
the proved `txy` initial order followed by canonical transport, with
β = 5, 5.05, …, 30. The displayed score tests eventual small-defect scalar
acceptance. It does not rebuild finite-size windows for the hypothetical data.

## Main findings

- Setting both denominator ground lower endpoints equal to their Rayleigh
  uppers produced no scalar success at either coupling in this grid.
- Setting all denominator ground/triplet intervals to zero width and deleting
  both omitted tails also produced no scalar success in this grid.
- The 8×4 upper trace at twice the initial temperature is overwhelmingly
  controlled by its ground width. Its triplet and tail contributions are tiny.
- The largest Rayleigh energy also matters, although its residual and spectral
  cutoff are absent from the reduced-input `txy` proof. At the best baseline
  temperatures, the main contributions to −log(C0) are listed below.

| g | β | 2β(ρ64−2ρ32) | 4β × 8×4 ground width |
|---|---:|---:|---:|
| .08 | 9.15 | .04832245 | .04635818 |
| .10 | 8.70 | .15162882 | .17507385 |

Here `ρ` includes the physical ground-energy offset. These are contributions
to an enclosure loss, not estimates of the true finite-size energy curvature.
The two terms together equal the ground-only exponent
`2β(ρ64−2 lower32)`. Thus a lower Rayleigh upper bound for the largest numerator
and a higher ground lower bound for the middle denominator are complementary
ways to reduce this loss.

The initial half/full-width largest-Rayleigh ablations often make a raw ratio
exceed one, so their apparent large scores must not be interpreted as feasible
targets. The follow-up script rejects all such points. With unchanged
denominators, at g=.08 a hypothetical largest-Rayleigh improvement of about
.002199 at β=9.75 crosses scalar acceptance. An improvement of .002304 at β=9.55 reaches a
hypothetical score .01. All three raw ratios then remain below one. This
necessary consistency check is not sufficient to establish that a physical
trial vector can attain the improvement. At g=.10, no largest-only change
passes before a raw ratio reaches one, within the tested grid and score rule.

## Reproduction and files

From the repository root, run the following commands with one BLAS thread and a 1 GiB virtual-memory cap.

```sh
ulimit -v 1048576
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python research_20261010/low_band/frontier_diagnostics/optimistic_screens.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python research_20261010/low_band/frontier_diagnostics/rayleigh_gain_threshold.py
```

These commands overwrite only this diagnostic directory's JSON outputs.
`summary.json` contains all ablations and exact source-file hashes.
`rayleigh_gain_thresholds.json` contains the restricted hypothetical thresholds.
The original physical inputs are the frozen `frontier_g007_g010/g2d25` and
`frontier_g007_g010/g1d10` `temple_*` files. Code dependencies are the frozen
trace routine `correlated_low_band.py` and transport routine
`frontier_g006/transport_orders.py`, with their transitive imports.

At this checkpoint, the next proposed computations were being handled separately. They involved inverse-moment
ground lower bounds using the full existing ground trial family, and an
explicit variational filter to lower a Rayleigh numerator using certified
compression bounds. Neither result is assumed here.
