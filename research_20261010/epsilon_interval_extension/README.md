# Continuum extension of the fully frustrated perturbation certificate

Updated 2026-10-10 13:53 EDT / 17:53 UTC.

Exact candidate coverage is now the entire interval 0<=epsilon<=0.00855 for every integer square side L>=2, with a common gap greater than 0.000768515509. The new part requires independent audit before promotion. Within 0<=epsilon<=0.0085 the selected candidates give the stronger common gap greater than 0.001703099464.

See PROOF.md for the model, continuum argument, full-spectrum completeness and size bridge. coverage_summary.json checks exact endpoint adjacency and identifies each selected input. The previously audited vacuum interval covers [0,0.00475]. Six new overlapping-at-endpoint intervals cover [0.00475,0.00855]. No statement is made for the unverified region above 0.00855.

The fixed q<=2 rational vectors are reused without changing their files. Full Hilbert dimensions are 256, 65,536 and 2^32, while the trial dimensions are 23, 93 and 377. Only one trial vector per seed is retained. The new calculation uses complete sparse residual polynomials, fixed local comparisons verified at both parameter endpoints, full occupancy-bin tails, correlated heat traces and all-integer finite windows. There were no new eigensolves.

Current status is ready for separate independent review. The initial unsplit construction and the refined frontier construction remain separate immutable records. REPRODUCE.sh rebuilds them using one CPU thread and roughly 100 MiB peak RSS. Raw measured times and memory are in the two cost files. No baseline files or GitHub state were changed.

Next step is independent reconstruction of polynomial contractions and interval heat bounds, followed by exact replay of the selected certificates. Further epsilon extension should first identify whether the limiting loss is the current heat-tail/spatial seed rather than simply increasing trial precision. Failed temperature-grid proposals are diagnostics and do not define a maximal coupling.
