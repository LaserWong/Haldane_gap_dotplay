# Spin-2 BLBQ near the AKLT point

Status 2026-11-05: Spin-2 BLBQ KHH(α) near AKLT — heat-trace bootstrap reuse NO (ξ≲6 only for α≳0.92, where QTM has complex multiplets; NUMERICAL + PROVED construction failure); Knabe/Gosset–Mozgunov local gap for α<1 NO (frustrated, PROVED). Spin-1 Heisenberg bootstrap and spin-2 AKLT/VBS certificates unaffected.

This folder is the 2026-11-05 deposit for the periodic spin-2 bilinear-biquadratic chain KHH(α). Each bond is

h = x + α(2/9 x² + 1/63 x³ + 10/7), x = S_i·S_j,

with spin 2. α = 1 is the AKLT parent and α = 0 is the Heisenberg chain. The notes use America/Chicago timestamps. Evidence labels stay as written in those notes. PROVED marks the failed real-transfer construction and the frustration argument. NUMERICAL marks the floating-point iDMRG and quantum-transfer-matrix spectra. HEURISTIC marks the correlation-length crossing near α ≈ 0.92 and the unattempted stability window.

The files below are the extracted archive. This README is the only file added after extraction. No existing repository file is changed, and the spin-1 Heisenberg bootstrap and the spin-2 AKLT and VBS-parent certificates are not modified.

## Contents

- `NOGO.md` summarizes both negative results and the open stability question.
- `PLAN.md` maps the spin-1 heat-trace obligations onto KHH(α).
- `DISCRIMINATOR.md` compares iDMRG correlation lengths with the reality of the quantum-transfer-matrix spectrum.
- `LOCAL_GAP_PLAN.md` records the frustration obstruction to Knabe and Gosset–Mozgunov local-gap theorems for α < 1.
- `idmrg_xi.py` and `xi_0.6.log`, `xi_0.7.log`, `xi_0.8.log`, `xi_0.9.log`, and `xi_0.95.log` are the correlation-length runs.
- `ff_check.py` and `ff_check.log` check frustration of the bond ground space.
- `qtm/N2.log`, `qtm/N3.log`, and `qtm/a095.log` are the transfer-matrix spectra.
- `deps/ed.py`, `deps/qtm.py`, and `deps/README.txt` are copies of the scripts those runs expect under `../spin2_aklt`.

## SHA-256

| File | SHA-256 |
| --- | --- |
| `DISCRIMINATOR.md` | `0d22419c8bb20e9dc67c25246df5dbcc81e2ad31590e6e23ffd92dfa090b638e` |
| `LOCAL_GAP_PLAN.md` | `792f2f265fe1f877f418cadcdb52f32450d10c1c44d8ebc0f8bc9a2bc81f47e4` |
| `NOGO.md` | `f05af93e5e70a2aa25ca8e01ac3122cacd26c6b3d91f6a073e8eea16d07b36b4` |
| `PLAN.md` | `4ade3df4b1caeb06dd5edf069884b274ee21b707e7746d1943c6e8513f81d2cf` |
| `deps/README.txt` | `1479671065e827cdeeebe8745ed2e5c79ef19d1f37af6589d6813a9e018466de` |
| `deps/ed.py` | `579f2d8ac43d106f3351fbe421bc52993de62e2347747d4de318a0927c5d164c` |
| `deps/qtm.py` | `b3d20385b828352c2cf2f6d89db27d6cbc8bc9c72ed9da099213d1bca04eb268` |
| `ff_check.log` | `98350ba3c93fb4c04a4375d55aafa48598e4fbb94fad673a225a44a6f84745e9` |
| `ff_check.py` | `06114189b5e388a4cab400ce249ac2205f6b3fd8b362f3ac0336dcd71097301a` |
| `idmrg_xi.py` | `49d84c05025f19607bd543b3d55a7f5c0e4b9e8704f3ce992c5881284a7d1459` |
| `qtm/N2.log` | `2bf60d72e3c93cd1cf7f08bb9e0968bbea782fd190d9ae5ec482d87fc41d887a` |
| `qtm/N3.log` | `148ef7efa0bf9343f931889699aaeef95db61e2015922febd05b81fdc3107e4b` |
| `qtm/a095.log` | `585178584a00c462d5318d3119cc79d9a7ebbb306e83f4c643d92e323e327e7c` |
| `xi_0.6.log` | `c05dc1133569a36779aa62a5e5375abddefae5b1548c9b7905aa05710440a30d` |
| `xi_0.7.log` | `e604837417c4994f7b51c59685f9958efcc1cfca92e830c9fd471c84f9170235` |
| `xi_0.8.log` | `ad2c4ea78025ea9610f0099cc6abb08e4368afb767101eb5e40e604bbddb1b40` |
| `xi_0.9.log` | `a4d011c511cd1f3bf20efcd2868f46dcc8625bda16a811ccb27821c0475263ae` |
| `xi_0.95.log` | `5234482bb6a8ac1dc66ac1c48bd31c275f2d9a87d2f4e1204bd70a2a13ef2188` |
