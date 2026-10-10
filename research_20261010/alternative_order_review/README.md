# Alternative-order bootstrap audit at g = 0.06

Updated 2026-10-10 14:24 EDT / 18:24 UTC.

**PASS:** the ordinary spin-1/2 square bilayer at g = 3/50 has a unique finite-volume ground state and gap at least **0.099555868340 for every integer square L >= 2**. The x–time–y route separately gives 0.082067113439.

See [REVIEW.md](REVIEW.md) for the physical replay, exact basepoints, transport proof and complete finite-size coverage; [REVIEW_STATUS.json](REVIEW_STATUS.json) is machine-readable. New-coupling physical data are rebuilt, while coupling-independent geometry is inherited only from a hash-verified sealed independent audit. No producer module is imported by the audit.

Run `./REPRODUCE.sh`. Resource use is one CPU, single-thread BLAS and at most 1 GiB address space. Frozen inputs remain untouched. No arbitrary-aspect-ratio or infinite-volume uniqueness conclusion is made.
