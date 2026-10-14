# Independent review of uniform-chain seed-size exclusions

Updated October 10, 2026, at 17:14 EDT / 21:14 UTC.

The exclusions for the fixed D = 26 single-Rayleigh method passed independent review at n = 6, 8, 10, and 12.
[REVIEW.md](REVIEW.md) gives the scope, physical reconstruction, exact all-temperature proof, and provenance.
These exclusions concern the certificate inputs.
They bound neither the physical purity nor the physical gap and do not establish an absolute minimum seed size.

Run `bash REPRODUCE.sh` in a disposable sibling copy to preserve sealed timing metadata.
The independent audit requires Python, C++, and GMP.
It uses one CPU and at most 1 GiB of address space, without an eigensolver.
