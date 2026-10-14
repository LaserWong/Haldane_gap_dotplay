# Independently verified large ordinary-bilayer seeds

Updated 2026-10-10 14:07 EDT / 18:07 UTC.

The angle-based frozen larger-seed certificates and all integer-size bridges passed independent physical, exact-arithmetic and analytic review, giving the following bounds.

- At g=.03, gap >= .281837226184 for every integer L>=2
- At g=.04, gap >= .179380190534 for every integer L>=2
- At g=.05, gap >= .093620600631 for every integer L>=2

See `REVIEW.md` for the Hamiltonian, normalization, complete-state count, all-sector tails, inherited transfer hypotheses, finite-size bridge, and limitations. These are rigorous sufficient bounds, not actual-gap estimates. The new direct Schur/inverse-moment lemmas are valid but are not used by these particular numbers.

`results/` contains independent exact replay records. `snapshot/` preserves the producer inputs. `INPUT_SHA256.json` records their provenance. No producer source was edited. `REPRODUCE.sh` rebuilds and rechecks the frozen package with one CPU and at most 1.5 GiB address space.
