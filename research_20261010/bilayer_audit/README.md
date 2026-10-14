# Optimized ordinary-bilayer audit

Completed 2026-10-10 13:21 EDT / 17:21 UTC.

## New verified conclusions

- The ordinary spin-1/2 square bilayer with unit rungs and both intralayer couplings g=0.01 has a gap of at least **0.168921021674 for every integer L≥2**.
- The same model at g=0.02 has a gap of at least **0.057308457817 for every integer L≥2**.
- The previous gap in size coverage below L=16 at g=0.02 is closed. A rational local comparison gives 0.4472 for L=2…7, and exact finite-scale interpolation gives 0.060761949098 for L=8…16.

These are rigorous lower bounds under the explicit periodic multigraph convention, not predictions of the actual gaps. The two-dimensional interpolation domain used in the bridge is now checked through common defect 1/200, using the already-established one-dimensional domain 1/40.

## Artifacts

- `PROOF.md`: complete physical assumptions, full-space completeness, optimized scalar audit, all-integer interpolation and finite-size bridge.
- `verify_optimized_bilayer.py`: standalone independent exact verifier. No generating-project imports, floating optimizer or eigensolver.
- `optimized_bilayer_audit.json`: six full-support ground checks, 24 per-node optimized tail checks, six scalar-path checks, exact bridges, input hashes and resource record.
- `replay.log`: successful replay output.

From the repository root, run the following commands.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python research_20261010/bilayer_audit/verify_optimized_bilayer.py
```

The checked baseline is the resumed main 6be889a archive supplied to this worker, whose 1,149 original file hashes were verified by the parent. This extracted local workspace has no .git metadata. No baseline files or GitHub state were modified by this worker.
