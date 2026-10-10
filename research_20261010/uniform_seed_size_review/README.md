# Independent uniform-seed-size review

Updated 2026-10-10 17:14 EDT / 21:14 UTC.

**PASS for the fixed D26 one-Rayleigh recipe at tested n=6,8,10,12.** See [REVIEW.md](REVIEW.md) for scope, physical reconstruction, exact all-beta proof and provenance. These are certificate-input obstructions, not physical-purity or physical-gap bounds, and not an absolute minimum-seed theorem.

Run `bash REPRODUCE.sh` only in a disposable sibling copy if preserving the sealed timing metadata. The independent audit requires Python, C++ and GMP; it uses one CPU, at most 1 GiB address space, and no eigensolver.
