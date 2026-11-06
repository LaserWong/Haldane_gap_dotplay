# thermal_arb — independent rigorous recomputation of the 18 thermal inputs

STATUS: **DONE. All 18 rigorous enclosures lie strictly inside the repo's `refined_rounded_interval`s** (and therefore inside the coarse windows, center ± 3e-5).
So every downstream inequality in `check_provenance.py` and `uniform_second_moment_optimization` holds independently of the producer's C++ integer kernel. Those checks use the J/N moment intervals built from the refined endpoints.

Z_L^g = Tr exp(-β0 (H_L^g + a L)), with β0 = 49/4 and a = 700741/500000, for L = 4..12 and g ∈ {I, P}.

## Conventions (checked exactly)
- Our sparse integer H^g (`blocks.full_H`) was rebuilt as the repo's per-weight byte streams D = (32-3n)I - 2H. These reproduce **every** SHA-256 in `uniform_second_thermal_full_review/matrix_L{4..12}.json`, for both I and P and all M ≥ 0 (`digest_check.py`, `digest_moments.json`). So the integer matrices are identical to the repo's.
- Exact integer moments Tr(H^g)^j are computed from the full sparse matrix: j ≤ 4 for L ≤ 10, j ≤ 3 for L = 11, 12. Each is contained in the enclosed power sums of the certified spectra (`moments_contain_exact` in `results.json`).
- Symmetries verified exactly as integer sparse matrices, for every L and g:
  - T_g H T_g^-1 = H, with T_P = U_0 T, U_0 = exp(iπS^z_0);
  - T_g^L = (-1)^{Sz} for P, and = I for I;
  - F H F = H;
  - Sz is conserved.
- Block dimensions times multiplicities sum to each sector dimension and to 3^L.

## Method (each enclosure is a theorem, given FLINT/arb and exact integer arithmetic)
1. **Blocks.** Exact Bloch blocks B_q (q ∈ [0, L], with B_{2L-q} = conj B_q) per Sz ≥ 0 (Sz < 0 by spin flip). Entries are acb balls at 128 bits.
2. **Weyl + Ostrowski.** For trial (V, Λ): η ≥ ‖V*V - I‖, r ≥ ‖BV - VΛ‖, and ‖B + L/2‖ ≤ 3L/2, because every bond, twisted or not, has spectrum {-2, -1, 1}. Then δ = (3L/2)η + r√(1+η), and the i-th eigenvalue lies in Λ_i ± (η|Λ_i + L/2| + δ), exactly m enclosures per block.
   - ‖dH‖_2 is bounded by the max absolute row sum of B - Hs, in arb.
   - See the header of `cert.py` for the proof sketch.
3. **Three modes for computing η and r:**
   - **hp** (m ≤ 40): mpmath 60-digit trial pair, scaled to 2^180. η and r are computed **exactly** with fmpz_mat. 333 blocks.
   - **exact** (40 < m ≤ 3000): LAPACK trial pair, scaled to 2^60 (V) and 2^56 (H, Λ). η and r are computed **exactly** with fmpz_mat. 359 blocks. This covers all of L = 7..11 beyond the hp blocks, and the L = 12 sectors with Sz ≥ 4.
   - **float** (m > 3000, L = 12 only, Sz = 0..3): 54 blocks.
     - The Gram matrix and residual are computed in IEEE binary64 BLAS / scipy sparse.
     - Bounds are a-priori, from Higham's standard model: |fl(xᵀy) - xᵀy| ≤ γ_n|x|ᵀ|y| + n·2^-1074, valid for any summation order and with or without FMA.
     - Sums of squares are bounded as fl/(1 - γ_N) + N·2^-1074. The diagonal subtraction is exact by Sterbenz (asserted).
     - **Labelled assumption:** correctly rounded IEEE-754 arithmetic, and no Strassen-type fast matmul in OpenBLAS 0.3.34 dgemm. Standard OpenBLAS does not use Strassen.
     - Cross-validation (`validate_modes.json`): on 4 blocks with m = 323..902, the float-mode enclosures intersect the exact-mode ones and are 500-2000x wider, as expected for a-priori bounds.
4. **Assembly.** `assemble.py` sums Z = Σ mult·exp(-β0(μ + aL)) over μ-balls in arb at 256 bits. Containment is checked with certain-ball comparisons against the exact rational repo endpoints.

Floats appear only as (a) trial data, whose rigor does not depend on accuracy, and (b) the labelled float-mode products in (3). Error bounds stored as floats are rounded outward: arb upper bound, then +2 ulps.

## Results (repo relative margins: (Z_lo - repo_lo)/repo_hi and (repo_hi - Z_hi)/repo_hi)
| case | repo refined interval | our rigorous enclosure | our rel. radius | margin lo / hi | contained | suffices downstream |
|---|---|---|---|---|---|---|
| L4_I | [124.8853798264238, 124.8853798268525] | [124.885379826638506, 124.885379826638506] | 8.4e-37 | 1.7e-12 / 1.7e-12 | yes | yes |
| L4_P | [0.06575703547748390, 0.06575703548732130] | [0.06575703548240392, 0.06575703548240392] | 9.2e-37 | 7.5e-11 / 7.5e-11 | yes | yes |
| L5_I | [0.002925182678780198, 0.002925182688159524] | [0.00292518268346975, 0.00292518268346975] | 2.1e-36 | 1.6e-09 / 1.6e-09 | yes | yes |
| L5_P | [2.960742995594862, 2.960742995893260] | [2.96074299574405557, 2.96074299574405557] | 2.1e-36 | 5.0e-11 / 5.0e-11 | yes | yes |
| L6_I | [12.87061404889128, 12.87061405228679] | [12.8706140505890111, 12.8706140505890111] | 3.4e-36 | 1.3e-10 / 1.3e-10 | yes | yes |
| L6_P | [0.2865996490525385, 0.2865996495592301] | [0.28659964930588783, 0.28659964930588783] | 3.7e-36 | 8.8e-10 / 8.8e-10 | yes | yes |
| L7_I | [0.05406952271997903, 0.05406952383788854] | [0.05406952327876386, 0.05406952327909726] | 3.1e-12 | 1.0e-08 / 1.0e-08 | yes | yes |
| L7_P | [1.920414791860990, 1.920414798523347] | [1.92041479518593435, 1.92041479519817387] | 3.2e-12 | 1.7e-09 / 1.7e-09 | yes | yes |
| L8_I | [4.639283417984037, 4.639283475100072] | [4.63928344651155430, 4.63928344657308013] | 6.6e-12 | 6.1e-09 / 6.1e-09 | yes | yes |
| L8_P | [0.5101407266224009, 0.5101407455622971] | [0.51014073608878410, 0.51014073609598714] | 7.1e-12 | 1.9e-08 / 1.9e-08 | yes | yes |
| L9_I | [0.1954550355787458, 0.1954550986348204] | [0.19545506710424221, 0.19545506710944440] | 1.3e-11 | 1.6e-07 / 1.6e-07 | yes | yes |
| L9_P | [1.514846900354352, 1.514847075899103] | [1.51484698810480648, 1.51484698814846758] | 1.4e-11 | 5.8e-08 / 5.8e-08 | yes | yes |
| L10_I | [2.654822445716474, 2.654823714326909] | [2.65482307994627326, 2.65482308009727472] | 2.8e-11 | 2.4e-07 / 2.4e-07 | yes | yes |
| L10_P | [0.6754193864435276, 0.6754200263217818] | [0.67541970636489511, 0.67541970640051203] | 2.6e-11 | 4.7e-07 / 4.7e-07 | yes | yes |
| L11_I | [0.3776280450198119, 0.3776306448351835] | [0.37762934490240360, 0.37762934495077063] | 6.4e-11 | 3.4e-06 / 3.4e-06 | yes | yes |
| L11_P | [1.314541759963492, 1.314546610583277] | [1.31454418518940770, 1.31454418535468830] | 6.3e-11 | 1.8e-06 / 1.8e-06 | yes | yes |
| L12_I | [1.900531549299379, 1.900563579253822] | [1.90054472271147625, 1.90055040440590852] | 1.5e-06 | 6.9e-06 / 6.9e-06 | yes | yes |
| L12_P | [0.7873950532568925, 0.7874156698136163] | [0.78740418547160484, 0.78740653657015269] | 1.5e-06 | 1.2e-05 / 1.2e-05 | yes | yes |

Tightest case: L12_I. Our relative radius is 1.5e-6 (float mode), against a margin of 6.9e-6 on each side.

## Still trusted
- FLINT/arb via python-flint 0.9.0 (ball arithmetic, fmpz_mat), CPython integers, and mpmath only for trial vectors (not trusted).
- numpy/scipy integer sparse construction of H. This is cross-checked bit-for-bit against the repo digests, so the residual trust is that sha256 collisions don't occur.
- `blocks.py` symmetry reduction: our code. Its algebra is checked by the exact symmetry identities, the dimension counts, the moment containment, and a float full-spectrum match at L = 4, 5.
- For the 54 L = 12 float-mode blocks: IEEE-754 correctness of OpenBLAS dgemm and scipy CSR matmul, under the standard model (no Strassen).
- The Weyl/Ostrowski theorem and the bond-spectrum bound (textbook).
- **No longer trusted:** the producer's C++ integer kernel and its outputs (W and endpoints). They are used only as the comparison targets.

## Runtime
- Wall time ≈ 1 h 25 min (10:50-12:15 CST, Nov 4, 2026), on 4-6 parallel single-threaded processes.
- Total CPU ≈ 4.7 h: ~3.1 h in the L = 12 complex eigensolver stage and ~1.6 h in block building and certification.
- Max single process: 448 s CPU (eigensolver stage, run separately from certification via `job.sh`). All processes were under 600 s.

## Files
- Code: `blocks.py`, `cert.py`, `run.py`, `job.sh`, `assemble.py`, `digest_check.py`, `validate_modes.py`.
- Outputs:
  - `enc/` (per-block certificates: trial eigenvalues as exact dyadics, err bounds, η, δ);
  - `results.json`, `digest_moments.json`, `validate_modes.json`;
  - logs.
- Re-assemble with `python3 assemble.py` (seconds). Re-run any block by deleting its `enc/*.json` and running `./job.sh TW L SZ Q`.
