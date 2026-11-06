# Open chat claims: verification status (Task A)

Source of the claims: https://chatgpt.com/share/6aeaa621-8684-8332-85da-3c869dad9cd2 (2nd answer, section 3, and the plaquette section).
Labels: **EXACT** = exact integers/rationals (fmpz / Fraction) or arb ball arithmetic with directed endpoints. **NUMERICAL** = floating point, not a proof.

| # | Claim (as stated in chat) | Verdict | Evidence |
|---|---|---|---|
| 1a | Tensor variant diag[0]=-289 (original): R68=-8.32218e-6, all-L>=2 bound 0.025068 | **CONFIRMED** (EXACT) | `tensor_R68.log`: R68=-8.322178606774621e-06; the exact contraction equals repo `anchors.out` (asserted). `tensor_gap_W10.log`: 6267/250000=0.025068 passes, 0.025069 fails (W=10, grid 1e-600) |
| 1b | -288: R68=+6.62092e-5, bound 0.023176 | **CONFIRMED** (EXACT) | R68=6.620915480134449e-05; W=10 gives 2897/125000=0.023176. (More windows give more: W=11 0.023249, W=12 0.023286) |
| 1c | -287: R68=+6.07160e-4, bound 0.003025 | **PARTIALLY TRUE** (EXACT) | R68=6.071603422304583e-04 matches. But **with the chat's W=10 the certified value is 1449/500000=0.002898, not 0.003025**. 0.003025 (=121/40000) is reproduced only at W=13 (`tensor_gap_W13_extra.log`). W=8/9/11/12/14/15 give 0.002607/0.002772/0.00297/0.003007/0.003034/0.003039. So the number is valid as a bound, but it depends on a window count the chat does not state |
| 1d | -285: R68=+3.14927e-3, "did not start" | **CONFIRMED** (EXACT) | R68=3.1492687597611075e-03; the leader ell is admissible, but the first window 68->136 fails even at gap 0 |
| 2a | Plaquette: W_box = -15/32 g^4 + O(g^5) | **CONFIRMED** (EXACT) | `plaquette.log`: exact Rayleigh-Schroedinger inclusion-exclusion. Coefficients of g^1, g^2 and g^3 are 0 and the g^4 coefficient is -15/32; single-edge E2=-3/8, E4=-3/128 |
| 2b | Table W/g^4 = -0.47571, -0.48252, -0.49562, -0.51917 at g=0.0125, 0.025, 0.05, 0.1 | **CONFIRMED** (NUMERICAL) | 60-digit mpmath diagonalisation (Sz=0 block): -0.475712349656, -0.482524747793, -0.495624287926, -0.519165518161 |
| 2c | Periodic 3x3 bilayer gaps 0.915256 (gx=gy=0.1) and 0.958627 (gy=0) | **CONFIRMED** (NUMERICAL) | `bilayer3x3.log`: float64 eigsh in the Sz=0 block (dim 48620) gives 0.915256 and 0.958627 |
| 3 | TFI J=1, h=5, n=2, beta=1/2, purification MPS with 32 steps: chi=6, 9, 16 -> 1.492020, 1.714857, 1.931304 (ideal 1.973380) | **PARTIALLY CONFIRMED** (bounds EXACT given Y; the MPS itself is float64) | Ideal reproduced: 1.9733807294 (`ising_mps_W8.log`). With 2nd-order Strang (half field / ZZ / half field) and SVD truncation once per step (`ising_mps_variants.log`, `ising_mps_chi9.log`): chi=6 -> **1.4920200** (exact match) and chi=16 -> **1.9313050** (claim 1.931304 is 1e-6 lower, so still valid). chi=9 depends on the convention: 1.7041-1.7347 across 12 truncation/bond-order variants, and none gives 1.714857. The chat's code is not in the bundle or repo, so chi=9 cannot be pinned down. Other Trotter splittings move all three values (e.g. bond-split 2nd order gives 1.494139 / 1.726473 / 1.962222) |

## How claim 3 is made rigorous here
- The MPS purification Y is computed in float64. Every Y entry is converted exactly into arb, so the method is not "float error modelling".
- eta = ||Y - e^{-beta H/2}||_F is computed in arb, with e^{-beta H/2} from `arb_mat.exp()` at 600 bits.
- Then max(0, ||Y|| - eta)^2 <= Z <= (||Y|| + eta)^2. S and T lower bounds and the window recursion (`runs/d_ising/win.py` logic) are evaluated in arb, using lower endpoints.
- So each printed gap is a rigorous lower bound **for the gap of the L=2,4 seed recursion**, relative to the repo's window theory.
- Bisection is to about 1e-10 and floors toward the passing side.

## Caveats / not done
- Claim 1: all L<34 rely on the repo's small-length certificate. Per the watertight all-sizes audit, that certificate is valid at least up to 0.025179.
- Claim 3: I did not reproduce the chat's chi=9 digit-for-digit (unknown implementation details). The alternating-chain table (chi=3,4,9,27) and the Monte Carlo rows were not requested and not checked.

## Files
- `tensor_R68.py/.log/.json`, `tensor_gap.py`, `tensor_gap_W*.log/.json`
- `plaquette.py/.log/.json`, `bilayer3x3.py/.log`
- `ising_mps.py`, `ising_mps_W8.log/.json`, `ising_mps_variants.py/.log`, `ising_mps_chi9.py/.log`

Runtimes: tensor R68 about 7 s; tensor gaps under 1 min each; plaquette 35 s; bilayer 1.7 s; MPS scans 1 s each.
