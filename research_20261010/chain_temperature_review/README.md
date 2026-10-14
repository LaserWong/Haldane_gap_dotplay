# Independently verified temperature-first chain certificates

Updated October 10, 2026, at 14:46 America/New_York (EDT) / 18:46 UTC.

The periodic spin-1 alternating chain with strong exchange 1 has the following independently verified gap bounds for every integer cell count M >= 2.

- At g = .1615, the gap is at least .039815121561.
- At g = .1625, the gap is at least .037716426713.
- At g = .175, the gap is at least .006791087005.

Each result includes a unique finite-volume ground state, exact short-size bounds, and signed-transfer windows covering both odd and even cell counts.
The largest input, at M = 8, uses only a Rayleigh quotient.
Its full Hilbert-space dimension is 43,046,721, and its single trial vector has support dimension 43,294.
The M = 4 full residual and complete trace-tail bound remain necessary.
They were checked independently or reused after verification against sealed hashes.

[REVIEW.md](REVIEW.md) gives the independent proof and provenance.
[SUMMARY.json](SUMMARY.json) records the exact results.
Run `REPRODUCE.sh` for the complete replay with one CPU, BLAS=1, and 1 GiB of address space.
No eigensolver is required.

The earlier space-first exclusions remain valid for their specified method.
The unsuccessful finite scan at g = .2 excludes neither all temperatures nor a physical gap.
The shared snapshot has no Git metadata, and no remote change was made.
