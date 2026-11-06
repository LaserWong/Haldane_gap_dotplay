# WATERTIGHT_STATUS  (2026-11-04, America/Chicago)
Repo clone /workspace/repos/Haldane_gap_dotplay @ a99fa21: untouched, nothing pushed. All work in runs/watertight/.

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | Transfer operator: Z_L(beta)=Tr X_beta^L, X real symmetric Hilbert-Schmidt, all L>=2 (APPENDIX_A_BRIDGE.md:23) | PROVEN | transfer_operator.md (bond-history expansion; kernel real, symmetric, bounded by 3e^{-beta a}, finite measure) |
| 1a | Z16(2b) <= Z12(2b)^{4/3} (same X_{2b}, even powers, l^p monotonicity) | PROVEN | transfer_operator.md section 5. Any even m<=16 works; certificate uses m=12=n+4 (not n+2) |
| 1b | Numerical sanity check of 1 | CONSISTENT (not proof) | discretized-kernel Richardson within 0.12-0.38% of ED for L=2..5; MC 1.5e6: z = -0.76, -0.83, +0.61 for L=2,3,4 |
| 2 | n=8 exclusion: sup_{b>0} Z12(2b)^{4/3}/Z8(b)^4 <= 0.0999792 < 1/2 | PROVEN (computer-assisted) | verify_indep.py / verify_indep.log; independent rebuild (old cert 0.100397 agrees) |
| 2a | Scope of the exclusion | method only | W<=1/2 means the scalar G-iteration cannot be started at n=8 (DERIVATIONS.md:3-13,89). It says nothing about the physical gap |
| 3 | Z12(49/4) <= 1.90055706747399 < 1.900577 | PROVEN (computer-assisted) | verify_indep.log (old: 1.90055706558595; both are upper bounds) |
| 4 | Independent Z12 symmetry-block code | PROVEN by independent rebuild | indep_blocks.py: exact sparse checks (H sym, THT^-1=H, FHF=H, T^L=I, Sz conserved, F negates Sz, FT=TF); 176571 enclosures with total multiplicity 3^12; enclosed sum of lambda^j contains exact integer Tr H^j for j=1,2,3 (0, 8503056, -4251528) at L=12 and (0, 69984, -34992) at L=8; L=8 matches dense ED to 4.7e-10; max delta 4.06e-7 |
| 4a | Old certificate's int64 limb recombination | GAP FOUND, now CLOSED | the old cert recombined limbs mod 2^64 with no check against wraparound. cert_core.py adds a float64 guard (|F-c|<=2^61 means the exact value is c). The new guarded run reproduces every trial eigenvalue (max diff 0 at the 2^-30 grid), so the old numbers stand |
| 5 | Gap 2497/100000, ORIGINAL audit logic | PROVEN (machine-checked) | run_orig_logic.py runs git-HEAD audit_scalar.py/audit.py with count-asserted substitutions only: file names, CPU affinity, gap literal, and the rounding grid B=10^140 -> 10^700 (precision only; down/up stay directed). Both scalar and all-sizes (L>=2) runs ACCEPTED. At B=10^140 it fails because depth-11 defects (~1e-273) fall below the grid |
| 5b | NEW: gap 1/40 = 0.025, ORIGINAL logic | PROVEN (machine-checked) | Z1 recipe, W=15, B=10^2500: scalar ACCEPTED (n=34, asymptotic_from 557056); all-sizes ACCEPTED for all L>=2 (auditor/orig_scan_F0_2500.log, orig_allsizes_scan_F0.log) |
| 6 | Gap 25177/1000000 | PROVEN with PATCHED checker only | needs FULL mode: Z_{2n}>1 replaced by the Jensen/Peierls-Bogoliubov bound Tr e^{-bH} >= e^{-b<H>_ray}. I reviewed it and the math is valid, but it is new checker code. The diff also re-pins the review seal 54401c... -> 56a4f066... (manifest regenerated), raises resource limits, takes file names and gap from env, and changes strongtail from a string compare to a Fraction compare |
| 7 | Claim "0.025179 fails" | REFUTED | true only at W=12. With W=13 (700 digits) the patched scalar checker ACCEPTS 25179/1000000, and the original all-sizes audit.py on that output ACCEPTS all L>=2 (auditor/orig_allsizes_patchedfull25179.log) |
| 8 | Ceiling of each recipe as W grows | ESTIMATE (float, not proof) | per-window rate -ln(1-C)/beta_w -> about 0.025007 (Z1/original) and 0.025214 (FULL). 0.02521 fails at W=15 (asym); W=16 fails at window 15 with 4000 digits (grid limit; defects square every window) |
| 9 | Chat claims (tensor -288/-287/-285, plaquette -15/32, MPS chi=6,9,16) | OPEN | not attempted (optional) |

Trusted base for 2-4: python-flint 0.9.0 arb; IEEE float64 BLAS with no fast-math, checked by the wrap guard; the Bloch-block and multiplicity derivation (mathematical; multiplicities are cross-checked by the dimension and moment checks).
