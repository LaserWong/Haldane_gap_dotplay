# Independent review of the alternative-order bootstrap at g = 0.06

Updated October 10, 2026, at 14:24 EDT / 18:24 UTC.

The ordinary spin-1/2 square bilayer at g = 3/50 has a unique finite-volume ground state and a gap of at least **0.099555868340 for every integer square side L >= 2**.
This result passed independent review.
The x–time–y order separately gives 0.082067113439.

[REVIEW.md](REVIEW.md) gives the physical replay, exact starting points, transport proof, and complete finite-size coverage.
[REVIEW_STATUS.json](REVIEW_STATUS.json) records the machine-readable result.
The review rebuilds the physical data at the new coupling and reuses coupling-independent geometry only after checking the hashes of the sealed independent audit.
It imports no certificate-generator module.

Run `./REPRODUCE.sh` with one CPU, single-thread BLAS, and at most 1 GiB of address space.
The frozen inputs remain unchanged.
The result does not establish arbitrary-aspect-ratio coverage or infinite-volume uniqueness.
