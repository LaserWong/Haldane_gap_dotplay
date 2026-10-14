# Direct Cartesian rules and indexed q6 sample

2026-10-11 02:22 UTC / 2026-10-10 22:22 EDT. The producer checks are complete. Independent review is pending.

The direct Cartesian edge operator, exact 15-probe extraction, both 4×2/5×2 physical fixtures, and 512 dispersed origin-containing q6 targets for each N/F/L passed the implemented checks. The source is the analytic m=M cM from the accepted 57D g=.11 witness. The checks do not cover the full q6 cache or the full 8×4 moment and establish no new gap.

N/F/L have 6,824 / 263,791 / 34,618 matrix-unit records. Indexed sample actions took 0.787 / 4.810 / 2.590 CPU seconds per 512 targets. Scaling these observed means to 169,911 origin-containing targets gives 2,716.66 CPU seconds. A 10× margin gives 27,166.62 seconds, before additional moment work. Thus this implementation fails the proposed 180-second gate. The estimate is empirical. It neither proves fundamental infeasibility nor establishes a runtime bound or permission to expand the budget.

The single computation run used 22.8854 CPU seconds and 26,128 KiB peak RSS. Bounded postprocessing used 0.172426 CPU seconds. Builds were separately capped at 512 MiB. Runtime used CPU6, one thread, 256 MiB address space and 60 CPU seconds. No hardening replay or production run was performed.

PROOF.md describes conventions, indexing and limitations. Results are in run/summary.json and run/analysis.json. NEXT_PROPOSAL.md describes the unexecuted invariant-diagram compiler and cache analysis. REPRODUCE.sh requires a fresh authorized budget and a fresh output directory. All predecessor seals remain immutable.
