# Candidate gap bound of .0248 at every periodic length

Recorded October 10, 2026, at 22:52 EDT / October 11, 2026, at 02:52 UTC.
The exact generated proof was awaiting independent review at this checkpoint.

The candidate establishes a unique ground state and gap >= .0248 for every integer periodic L >= 2 through four inputs.

- Analytic bounds at L = 2 and 3
- Cached purity bounds at L = 4..25, rechecked at .0248
- Fresh direct thermal certificates at each length L = 26..33
- The independently accepted tail initialized at n = 34

This stronger proof uses initialization 34.
The smallest separately certified initialization remains 30 at .0179.
Coverage beginning at length 2 does not imply initialization at 2.

The new batch used 7.25026 CPU seconds measured by wait4, 11.67768 elapsed seconds, and 15824 KiB.
All guarded limits were checked before and after exec.
It required no new thermal inputs, exact diagonalization, or tensor optimization.
See `PROOF.md` and `certificate.json`.
Replay the scalar calculations with `python check_cached_prefix.py` followed by `python certify.py`.
