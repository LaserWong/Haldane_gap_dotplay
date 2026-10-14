# Bounded ordinary-bilayer frontier at g=.07, .08 and .10

2026-10-10 14:45 America/New_York / 18:45 UTC.

All outputs in this directory are new candidates pending independent physical
and scalar replay. The underlying geometry-contraction, translated-band,
quadratic-boson comparison, sector-Temple, order-transport and interpolation
theorems are independently reviewed upstream. Existing frozen results are not
changed.

## Candidate bounds

The ordinary spin-1/2 periodic square bilayer has unit rung coupling and equal
straight in-layer couplings g. All nine new 4x4,8x4,8x8 patch records pass the
exact complete-band cutoff and residual checks.

At g=.07, the time,x,y route, explicitly transported to the canonical staircase,
gives an exact candidate gap 0.024790852531 for every integer square side L>=2.
Its initial beta is 49/5. Canonical asymptotic acceptance begins at L>=64. The
intermediate windows give .087252183109 on 8–16, .054169796249 on 16–32, and
.040154192241 on 32–64. A common quadratic-boson short-size comparison gives
at least .307810466553 on L=2,...,7. The x,time,y route also succeeds, giving
.009272103501 after its own transport and bridges.

At g=.08 and .10, no successful scalar certificate was found on the bounded grid
beta=5,...,30 with step .05 in any of the three inequivalent order placements.
Selected best-stage failures were replayed exactly. This is not an all-beta
exclusion, a claim of physical gaplessness, or an obstruction to other trial
families or seed geometries. Every physical low-band cutoff still passes, despite failure of the scalar
certificate tests.

| g | 8x8 counted cutoff minus max Ritz | 8x8 ground Temple width |
|---|---:|---:|
| .07 | .499548323198 | .004576037661 |
| .08 | .397097935597 | .010044491525 |
| .10 | .145965013182 | .036961220218 |

The largest patch has 128 physical spins and full Hilbert dimension 4^64. Its
retained full low band has 193 states, with a 29-dimensional symmetry/Krylov
ground trial and 64 translated spin-one directions with exact multiplicity 3.
No larger Krylov support or new geometry contraction was used.

## Input generation and exact checks

`prepare_frontier.py` reuses the same previously audited geometry files and
creates new coupling-specific integer G/K/J and translated G/A/B moments. It
records all source geometry hashes. Every H-applied leaked configuration is
retained in the residual, and the existing 4x4/8x4/8x8 sparse support sizes are
unchanged. The new quadratic reference endpoints use directed rational square
roots and bosonic reference multiplicities, not physical shell multiplicities.

`scan_frontier.py` first requires ground identification and complete-band
separation at all three sizes. It then reuses the reviewed exact arithmetic
helper with an explicit local-only source resolver. Every recorded source hash
refers to the actual coupling-specific file. It clips each ground lower bound
by the known global ground floor and each triplet lower bound by the certified
lambda2 floor. This is valid because the unique ground lies in the even singlet
sector and all triplet trials belong to orthogonal invariant sectors. Original
unclipped endpoints are retained in the records.

For every L=2,...,7 and 0<=g<=.10, alpha>=.8, ||K||<=.2 and
v=(3g^2/4)sum w_e^2<=.735. The short-size comparison therefore uses the uniform
lower endpoint delta-.735/(.8+delta), with a directed delta<=sqrt(.6). The edge
square sums 16,18,32,50,72,98 are recorded explicitly. The singlet product has
shifted energy zero, giving the stated gap. This does not assume monotonicity of
the physical gap.

## Reproduction and scope

From the repository root:

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/frontier_g007_g010/prepare_frontier.py
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/frontier_g007_g010/scan_frontier.py

These commands overwrite files only in this directory. Use a separate copy to
preserve the frozen records for audit and publication. Continuous-coupling interval work has not begun. No 8x8 H²W
second-order-band construction has been launched.
