# Nonperturbative robustness audit

Updated 2026-10-10 13:20 EDT / 17:20 UTC.

Completed independent audit of the saved J=0.3, epsilon=0.005 fully frustrated bilayer candidate. Straight exchanges are J+epsilon. Crossed exchanges are J. Rung exchanges are 1. Periodic directions of length 2 retain both adjacencies.

**The certified result is a unique finite-volume ground state and gap >= 0.038983227177 for every integer square side L >= 2.**

- `BASELINE_PROOF.md`: complete model, weighted-star argument, occupancy ranks, ordered min-max completeness, exact residual/Temple audit, thermal recursion, transfer hypotheses and newly completed short-size bridge
- `audit_ff.py`: independent verifier, no producer-module imports
- `ff_seed_J3d10_eps1d200_depth0_audit.json`: machine-readable exact verification and bridge
- `baseline_audit.log`: successful run (12.64 seconds, about 32 MiB peak RSS)

Reproduce from the repository root with the following command.

    python research_20261010/nonperturbative_audit/audit_ff.py --physical

The largest seed has 32 physical spins, full Hilbert dimension 4,294,967,296, a 377-dimensional linear trial space and 21,345 reached configurations. Exactly one Ritz vector is retained. Full residuals include leakage outside the trial space.

The fixed baseline result is separate from exploratory follow-on epsilon scans (`scan_epsilon.py`, `epsilon_scan/` and `epsilon_scan_summary.json`). A failed finite parameter/temperature grid is not a no-go theorem, a physical transition or a maximal threshold. A collection of certified points is not a continuum interval unless an interval argument is supplied explicitly.

## Separately completed extensions

`EPSILON_FRONTIER.md` supplies a new uniform one-product-trial theorem. Every 0 <= epsilon <= 0.00475 and every integer square L >= 2 has gap >= 0.008090283176. Its exact residual, affine endpoint-PSD argument and stronger triangle-free finite-size bridge are recorded explicitly.

Individually audited q<=2 Ritz certificates additionally give all-L gaps >= 0.028171615330 at epsilon=.006 and >=0.012626894873 at epsilon=.0075. Points .008 and .0085 have positive large-L certificates with smaller-size bridges still open. No maximal coupling claim is made.
