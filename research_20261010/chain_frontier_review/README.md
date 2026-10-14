# Independent chain frontier review

Updated 10 October 2026, 13:47 EDT / 17:47 UTC.

## Result

The following spin-one alternating-chain certificates have passed independent exact-arithmetic audit, with a unique ground state and the stated gap for every integer two-spin cell count M>=2.

| Weak coupling g | Gap lower bound |
|---|---:|
| .16 | .004358246531 |
| .161 | .001952374069 |
| .16125 | .001075806295 |

The specified ground-only numerator plus independent-dimer-bin-tail plus G-recursion family is independently excluded for every beta>0 and every valid local comparison parameter at g=.1615 (depth-five ground intervals), .1625, and .175. This remains true with arbitrarily sharp ground refinements within the audited intervals. These exclusions are method-specific. They neither establish physical gaplessness nor prove a maximal coupling threshold.

See [FRONTIER_PROOF.md](FRONTIER_PROOF.md) for model normalization, the cancelled-first-step derivation, complete-spectrum justification, finite integer windows, M7 bridge, and the all-temperature obstruction proof.

## Files

- `verify_frontier.py`: new independent cancelled-step, window, affine-ceiling, and interval-coverage checker. It imports no producer mathematical code.
- `independent_core.py`: explicitly preserved previous independent physical-spin kernel, exact full residual, local rational LDL, Temple, full reference bins, and exponential enclosure.
- `independent_core_changes.patch`: exact changes from the earlier independent verifier, with changes to the input directory and 1 GiB cap only.
- `*_independent_review.json`: complete exact acceptance records, including LDL pivots, seed and replay tests, window enclosures, and obstruction trajectories.
- `summary.json`, `audit_final.log`: final clean combined replay and resource measurements.
- `INPUT_SHA256SUMS.json`: input records and integer trial artifacts actually read by the clean combined replay.
- `PRODUCER_FINALIZED_SHA256.json`: finalized hashes explicitly supplied by the producer, checked when reading those records.
- `PROVENANCE.json`: prior independent sources and integrity checks.
- `SHA256SUMS.json`: review artifacts, excluding this manifest itself.
- `audit.log`, `summary_deeper.json`, `audit_deeper.log`, `INPUT_SHA256SUMS_deeper.json`: earlier completed initial and depth-five replay diagnostics. Final acceptance uses the clean combined replay.

## Reproduce

From the repository root, on Linux:

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    taskset -c $(python -c 'import os; print(min(os.sched_getaffinity(0)))') \
    python research_20261010/chain_frontier_review/verify_frontier.py --include-new --include-deeper

The checker requires a one-CPU affinity and limits address space to 1 GiB. It does not call an eigensolver. Expect several minutes for the complete replay. Each stage prints its completion. A failure aborts instead of creating a new successful summary. Only files in this review directory are written. Source and producer files are preserved.

The full Hilbert dimension at M=8 is 43,046,721. The positive depth-four certificates have trial/full-residual supports 43,294/245,870. The depth-five .1615 obstruction inputs have supports 245,870/939,326. These are linear support dimensions, not MPS bond dimensions. Independent verification of the latter used 283.7 MiB peak RSS in its standalone replay. Producer cost is not the verification cost.

The final clean combined replay passed in 187.25 seconds, with peak RSS 303.3 MiB, one-CPU affinity, BLAS threads one, and a 1 GiB address-space cap. All nine explicitly finalized producer record hashes matched.

This is an executable exact-arithmetic certificate and independent proof review, not a proof-assistant formalization.
