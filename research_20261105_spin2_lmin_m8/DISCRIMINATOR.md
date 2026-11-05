# Spin-2 moment discriminator — B-test-v1
2026-11-05, America/Chicago. **TESTED**. Bounded experiment completed; stronger theorem remains **BLOCKED**.

## Answer
**YES**: classical-ED-length (M=8) *estimated two-sided spin-2 data* admit an integer-multiplicity fake satisfying all structural premises F1--F4 and killing both proposed spatial seeds:

| beta | moment prefix | n | S_fake(n) | threshold |
|---|---|---|---|---|
|64|all integers4..8, separate Z and P|256|0.5082725203986761|1/sqrt(2)|
|64|all integers4..8, separate Z and P|300|0.5113138102625230|1/sqrt(2)|

**NO established path to M_min>=26 under current evidence.** This is NOT a disproof of that claim or a claim that no path exists. The two-sided compensation mechanism survives its first ED-length test, so proceed toward a rigorous M=8 result, not directly to a large production campaign. There is no logical extension from M=8 to25 in this experiment.

## Chosen statement and exact scope
Candidate B: a finite fake compatible with actual spin-2 D_8 and F1--F4 would exclude a seed certificate at n256/300. The present numerical intermediate substitutes explicitly ESTIMATED data, not rigorous boxes. No claim about real spin-2 M_min is PROVED. See PLAN.md for candidates A/B/C and the stronger through25 contract.

Data: beta64, shift4.761248. Periodic and pi-seam Hamiltonians are built in Sz blocks. The pi seam negates only XY off-diagonal terms on the final bond, leaving SzSz unchanged. Retain eight low Ritz levels in each Sz0..4; combine with weights1,2,2,2,2 for +/-Sz. Ritz residuals <1e-7; L4 periodic E0=-20 smoke check passes. This is NOT a complete heat trace. Omitted eigenvalues and |Sz|>=5 contributions are not rigorously bounded. Lanczos float error is not enclosed. Log values are subsequently reified as decimal constants and exponentiated at180 digits; these extra digits do not add input accuracy.

|k|log Z_k estimate|log P_k estimate|
|---|---|---|
|4|61.12051200000269|-38.14886918262867|
|5|-170.70309715387498|14.298441258828252|
|6|38.221132847990475|-23.576151099867072|
|7|-106.95145141288162|10.161523101688712|
|8|27.640648665687426|-16.76352863883695|

Odd-length cancellation is extreme. It was NOT dropped or tested only at relative sector tolerance: final verification tests each Z_k and P_k separately.

## Method and independently replayable checks
Adapted mechanism from moment_nogo/explore_fake.py and build.py: even-moment NNLS proposes three symmetric bulk pairs per sector; round each pair weight to a positive integer, then solve five moment equations by changing five of six positions using180-digit Newton. Fixed J atoms:1.00001 (simple PF) and0.999 (unit competitor). Final bulk moduli <0.005062; integer cluster weights reach about2.03e50. These large finite multiplicities are allowed by F1--F4; no physical tensor-network realization or finer SU(2) constraints are claimed.

candidate.json exports165-significant-digit decimal atom positions (exact rationals) and integer weights. check_integer.py parses with Fraction, embeds positions into common denominator10^180, then uses exact integer arithmetic. It separately checks:
- positive integer weights, simple dominating J PF atom, and declared bulk cap .95;
- all TEN separate Z/P constraints for k4..8, relative tolerance1e-8 against rationalized estimates;
- Z_L,P_L>0 for EVERY integer L>=4: exact finite prefix4..13, and from14 onward a geometric tail bound. The total absolute bulk contribution divided by PF^L is <1 at14 and decreases thereafter. The second positive J atom is harmless for both Z and P;
- 2 Z_2n^2 <= Z_n^4 at n256 and300, exactly equivalent to S<=1/sqrt(2) given positivity.

All checks pass. Largest separate relative residual is about5.22e-71 (Z5); this reflects synthetic fitting accuracy ONLY, not physical ED accuracy. Exact rational verification of a synthetic candidate does not promote the physical statement beyond TESTED. The checker is separate from the fitting algorithm, not a fresh-context mathematical review.

## What was retained, including abandoned attempts
- First shell launch used unavailable `python`; no files were written in that launch. Correct executable is /usr/bin/python3.
- Initial ED run used a symmetric all-ones Lanczos start. Replaced by a deterministic nonsymmetric sine/cosine vector to avoid a symmetry-restricted starting subspace. Original estimates/log retained as *_symmetric_start.*; final log is estimate_data.log.
- Initial .95-endpoint grid gave a candidate with a bulk atom exceeding .95 by ~1.45e-10; retained as candidate_grid095.json, fit_fake_grid095.log, NOT accepted under the declared cap. Use an initial .94 endpoint instead, unchanged final allowed cap .95. Final NNLS selected much smaller nodes and passed all checks. This is a representation/search proposal change, not a target change.
- The general Fraction-only checker on the initial candidate was stopped after~75s because common-denominator integer arithmetic is equivalent and much faster; its log is check_candidate.log. It yielded no accepted verdict. Final exact checker is check_integer.py, runtime <1s.

## Consequences for Xiao and next action
**TESTED:** the M=8 two-sided approximate-data route is viable, including odd lengths, sectors, integer weights, and all-length positivity. This is stronger evidence than a total rho estimate and avoids the DISPROVED general two-sided rho implication.

**BLOCKED:** a rigorous spin-2 D_8 no-go needs actual interval enclosures (both Z/P, every k4..8), or a rigorously quantified robust inverse-moment construction that covers certified physical data. Neither is supplied. No anchor family is present; adding anchors or cross-beta/SU(2) constraints requires a new contract and recheck.

**BLOCKED:** M_min>=26 requires a witness compatible through25 (or a genuinely uniform theorem) and nonvacuous data consistency. No k9..25 compatibility has been checked. The xi~49.5 rescaling is TESTED heuristic only, not a theorem-level bridge. beta64 does not cover every beta or every bootstrap window. ED feasibility boundaries themselves are engineering estimates, not complexity lower bounds.

Next step: **prove** the limited M=8 data-specific theorem by obtaining/certifying the missing short spin-2 traces and preserving strict witness margins. Keep the >=26 claim BLOCKED pending a separate analytical through25/finite-size-moment mechanism; do NOT weaken the advertised final target or launch exponential ED at25.

## Replay
From /workspace/runs/spin2_lmin:
```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 estimate_data.py > estimate_data.log 2>&1
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 fit_fake.py > fit_fake.log 2>&1
python3 check_integer.py > check_integer.log 2>&1
```
No randomness; deterministic nonsymmetric starting vectors. Environment: Python3.13.5, NumPy2.5.4, SciPy1.18.1, mpmath1.3.0. Final witness/check binding and source hashes: manifest.json. Full estimated eigenvalues and residuals: ed_estimates.json. Final exact-check output: check_integer_result.json. No git repository changes made.
