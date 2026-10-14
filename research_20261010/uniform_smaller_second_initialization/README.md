# Smaller initializations with the second thermal-input set

2026-10-10 22:22 EDT / 2026-10-11 02:22 UTC. These exact producer certificates await independent review.

| Initialization | Gap lower bound | Integer length range | Fresh MPS anchor | Asymptotic entry |
| --- | --- | --- | --- | --- |
| n=34, beta=49/4 | 0.0248 | L≥34 | 68 | 17408 |
| n=32, beta=49/4 | 0.0245 | L≥32 | 64 | 16384 |
| n=30, beta=49/4 | 0.0179 | L≥30 | 60 | 30720 |

Each row includes a unique ground state, and every preceding integer window is certified separately. These are genuine smaller initializations, without a minimum-seed or optimal-gap claim. All 18 beta=49/4 thermal inputs inherit completed independent physical validation. The fresh MPS60/64/68 contractions and scalar extension require their own review.

`PROOF.md` and `certificate.json` give the evidence. Replay with `python certify_long.py` followed by `python certify.py`. No new thermal campaign, exact diagonalization, optimization, or remote change is involved.
