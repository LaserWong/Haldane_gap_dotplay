# Independent review of the ordinary-bilayer interval

Updated 2026-10-10 14:58 EDT / 18:58 UTC.

The review accepted the following result. For every 0≤g≤0.07 and every integer square side L≥2, the ordinary periodic spin-1/2 square bilayer has a unique finite-volume ground state and gap at least 0.001945771244. The rung exchange is one, the straight intralayer exchange is g, and side-two periodic multiplicities are retained.

Read [REVIEW.md](REVIEW.md) for proof, provenance and limitations, or [results/SUMMARY.json](results/SUMMARY.json) for exact endpoints. Run `bash REPRODUCE.sh` for the independent exact replay. The replay uses no producer imports, eigensolver or new full-spectrum computation.

Three fixed vectors per interval use trial search dimensions 11/29/29. Each denominator retains one ground level. The largest numerator has rank one and uses G/K only. The largest physical Hilbert space is 2^128, not 29.

The 16 closed intervals, 48 vectors, 32 full residual polynomials, 46 finite windows, and 96 short-size rows are independently checked. Worst-interval asymptotic onset is L=1024. All preceding integer sizes are covered. The review changed local files only and performed no remote publication.
