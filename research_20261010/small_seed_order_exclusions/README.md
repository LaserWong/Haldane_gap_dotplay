# Small-seed exclusion for all six coordinate orders

Updated: 2026-10-10 14:31 America/New_York (EDT, UTC−4) / 18:31 UTC.
Status: complete. Separate independent analytic and exact scalar review passed.

## Result

For the ordinary isotropic square bilayer at **g=0.04 and g=0.05**, the fixed
**2×2 / 4×2 / 4×4 small-seed recurrence fails for every β≥0 in all six coordinate
orders**, even with exact physical partition functions. The intermediate
rectangle is rotated to 2×4 for the spatially exchanged orders.

- g=.04: xyt/yxt fail by update 4; xty/ytx/txy/tyx fail by update 3.
- g=.05: every order fails by update 2.

The four alternative orders fail before a positive first-cycle triple can be
transported into the canonical staircase. This turns the earlier bounded
temperature scan into an all-temperature method obstruction. It does not
imply a physical gap closes, and it leaves larger seeds, improved inequalities,
new trace injections, and adaptive order changes open.

## What is actually certified

1. **0≤β≤4:** common J1≤T_2×2(β)^4≤T_2×2(4)^4. Exact upper bounds T_2×2(4)<.674
   force a negative first update for every order. Only physical thermal purity
   is assumed monotone in β.
2. **4≤β≤20:** 320 consecutive closed rational boxes of width 1/20, separately
   checked for xyt, xty, and txy. This is exhaustive interval coverage, not a
   temperature grid inference.
3. **β≥20:** exact positive physical energy-curvature slopes and nonnegative
   relative spectral gaps give uniform upper bounds on the full unbounded ray.
4. **All six orders:** the unitary site relabeling (x,y,layer)↔(y,x,layer)
   preserves the periodic bond multiset and equal couplings, proving identical
   traces and complete paths for xyt↔yxt, xty↔ytx, and txy↔tyx.

Every failure witness is a strictly negative upper enclosure of an output of
the specified lower-bound recipe. It is not merely failure to reach a sufficient
small-defect basin. All prior-positive-domain checks are enforced.

## Evidence

- [Analytic proof, quotient identities, and exact scope](PROOF.md)
- [Reproducible rational construction](certify_orders.py)
- [All 1,920 order-specific middle-box checks plus hot/cold witnesses](results.json)
- [Original accepted physical reconstruction](../small_seed_exclusion_review/README.md)
- [Independent analytic review](independent_review/REVIEW.md)
- [Independent 320-bit exact replay](independent_review/results.json)
- [Joined acceptance and scope](ACCEPTANCE.json)

The 1,920 checks comprise 320 boxes × 3 representative orders × 2 couplings.
No new physical vector, full diagonalization, or physical-input reconstruction
was needed. The accepted physical audit is explicitly reused and its input
hashes rechecked. Construction used one CPU, one BLAS thread and a 1 GiB
address-space cap; it took about 81 seconds and 53 MiB peak RSS in this run.

The separate review imports no project implementation and uses a newly written
320-bit integer exponential enclosure with an 84-term reduced Taylor series.
It verifies every saved input and every rounded recurrence argument/output,
independently recomputes all interval and hot/cold bounds, and checks all six
symbolic quotient identities and full-spin bond-multiset exchange. Its replay
took about 15 seconds and 49 MiB peak RSS on its final pass. Both timings are environment-dependent.

## Reproduce

To independently replay the currently sealed producer result, from the
repository root:

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/small_seed_order_exclusions/independent_review/audit_orders.py

To regenerate the construction itself:

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/small_seed_order_exclusions/certify_orders.py

Both commands overwrite their own output JSON with fresh timing/RSS metadata.
For a byte-preserving verification, run them on a copy of the repository tree.
A producer rerun changes its result hash and requires a fresh producer freeze
and review; the independent replay deliberately rejects a stale seal. The
commands write this directory only and make no external write. The source
tree is an extracted checkpoint without local Git metadata; no commit or remote
publication is claimed. The producer result retains its historical
"awaiting independent review" field; the separate acceptance and review files
record the final passed status without mutating the reviewed scientific record.
