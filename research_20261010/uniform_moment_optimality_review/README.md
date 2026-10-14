# Optimality of the fixed-moment envelope

2026-10-10 18:54 EDT / 22:54 UTC. The independent review accepts the following scoped results.

- Exact sharpness of the relaxed Radau problem with fixed moments
- Explicit integer-count spectra satisfying all nine raw intervals and positive A4 seam traces at every integer L≥2
- Moment-only improvement ceilings below 7.1643e-5 at L26 and 3.0482e-5 at L100
- A strict trivial-L26 integer correction greater than 1.49e-14

These results establish no physical or cross-temperature realization, new gap, n50/n48 obstruction, or minimum-seed theorem. The auxiliary 96/100 contractions are not accepted as new anchors by this review.

See `REVIEW.md`. In a disposable copy, run `python independent_check.py > replay.log` and `python adversarial.py > adversarial.log`. The replay uses CPU5 with a 700 MiB ceiling and takes approximately .42 CPU seconds. It makes no producer, root, or remote changes.
