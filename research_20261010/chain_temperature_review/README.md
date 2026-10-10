# Independently verified temperature-first chain certificates

Updated 10 October 2026, 14:46 America/New_York (EDT) / 18:46 UTC.

Passed all-integer M>=2 bounds for the periodic spin-one alternating chain, strong exchange 1:

- g=.1615: gap >= .039815121561
- g=.1625: gap >= .037716426713
- g=.175: gap >= .006791087005

Every row includes a unique finite-volume ground state, exact short-size bridges, and signed-transfer windows covering odd as well as even cell counts. The largest M=8 input is truly Rayleigh-only; its full dimension is 43,046,721 and its one trial vector has support dimension 43,294. The M=4 full residual and complete trace-tail premise remain necessary and were independently verified or reused by sealed hash.

[Full independent proof and provenance](REVIEW.md). Exact results are in [SUMMARY.json](SUMMARY.json). Run `REPRODUCE.sh` for a complete one-CPU, BLAS=1, 1 GiB replay without an eigensolver.

Previous space-first obstructions remain recipe-specific and valid. The g=.2 finite failed scan is not an all-beta obstruction or a physical gaplessness result. The shared snapshot has no Git metadata; no remote change was made.
