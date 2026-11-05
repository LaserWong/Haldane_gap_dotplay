# spin1_opt1 — Close trusted base to arb-only (Option 1)

STATUS: **DONE** (2026-11-05 ~05:39 America/Chicago)

Trusted base for the spin-1 thermal L=12 blocks is now **arb-only**: the 54 former IEEE float-mode blocks were re-certified with `exact_chunked` (exact fmpz Gram/residual + arb dH / Weyl–Ostrowski). `assemble12.py` asserts **no `mode=='float'` remains**.

## (a) L=12 re-cert — DONE

- Enc files: 54/54 under `l12/enc/` (`l12/DONE` stamped 05:38).
- Assemble: `assemble12.py 12` exit 0; overrides n=54; max |new−old| eig 6.94e-18; old(float) maxerr ~4.23e-07 → new(exact_chunked) maxerr ~2.26e-11; non-intersecting pairs **0**.
- Cross-checks (both L12_I and L12_P): `moments_contain_exact=True`, `digests_match=True`, `inside_refined=True`, `inside_coarse_window=True`.

| case | Z enclosure (arb) | rel radius | blocks_by_mode |
|---|---|---|---|
| L12_I | [1.900547563954856529282874, 1.900547564527809249273346] | 1.51e-10 | {'exact_chunked': 28, 'exact': 35, 'hp': 22, 'empty': 6} |
| L12_P | [0.7874053613805283708642947, 0.7874053616217252892050861] | 1.53e-10 | {'exact_chunked': 26, 'exact': 33, 'hp': 20, 'empty': 6} |

Method: same theorem as `thermal_arb/cert.py` mode `exact`, split across processes under the ~600 s/process box limit (`exact_chunked`). Trial eigenvectors from LAPACK (untrusted); η, r from exact fmpz / int64-limb sparse products.

## (b) Headline dual-checked bound — DONE

| gap | logic | checkers | label |
|---|---|---|---|
| **63033/2500000 = 0.0252132** | FULL, W=17 | (1) patched repo FULL checker `push_bound/certs/full_W17`; (2) `indep_chain.py` FULL W=17 DIGITS=20000 ACCEPTED (factor 0.9577); next grid 31517/1250000 REJECTED | **PROVED, dual-checked** |
| 25177/1000000 = 0.025177 | FULL, W=12 | repo + `a_uniform/cert12.py` | PROVED, dual-checked (conservative floor) |
| 2497/100000 = 0.02497 | Z>1, W=12 | repo + cert12 | PROVED, dual-checked |
| 250057/10000000 = 0.0250057 | ORIGINAL/Z1, W=17 | repo (CPU cap 590) + indep_chain Z1 | PROVED, dual-checked |

Headline chosen: **63033/2500000**. See `notes/headline_b.md`.

## (c) Seals / direct-25 — SUMMARIZED (no seal fights)

- HEAD MANIFEST_SHA256 AssertionError is post-seal `.md` edits only (code identical).
- Restoring 253 sealed `.md` blobs → direct25 / n24 / gap-0.0248 audits exit 0.
- `limited_run.py` L=25 under RLIMIT_CPU 15 s / AS 100 MiB: exit 0, cpu_seconds=2.5792, stdout byte-identical to sealed `anchor25.out`. Prior “26 s vs 15 s cap” anomaly **not reproduced**.
See `notes/direct25_c.md`.

## Related (not this deposit’s claim)

- Option 2 (`../spin1_opt2/PILOT.md`): seed-strength float pilot max γ ≈ 0.027 ≈ 1.07× current bound — **do not certify**.
- Open spin-1 chains and 16c uniqueness remain **not** claimed here.

## Artifacts

- `results.json`, `assemble12.py`, `l12/` (enc + logs + scripts; work/ optional), `indep_chain/`, `direct25/`, `notes/`.
