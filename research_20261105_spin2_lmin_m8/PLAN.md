# Spin-2 minimal moment length — contract v1
2026-11-05, America/Chicago. DISCOVER; bounded deliverable, not full campaign. Local source packet only; no git changes.

## Definitions
beta=64; shift a=4.761248; Z_k=exp(-beta*a*k) Tr exp(-beta H_k); P_k uses the pi seam (flip the seam XY coupling). Structural class is exactly F1--F4 of MOMENT_NOGO.md: compact self-adjoint transfer spectrum, integer J/N weights, Z=J+3N, P=J-N, simple J PF atom dominating every modulus, Z_L,P_L>0 for ALL integer L>=4. No cross-beta, inverse-spectrum or extra SU(2) restrictions. D_M contains separate two-sided Z/P data at EVERY integer k=4,...,M. No rigorous spin-2 anchors are supplied. Target Phi_seed(n): S(n)=Z_2n/Z_n^2>1/sqrt(2), n in {256,300}. M_min is the least prefix length whose nonempty compatible class forces Phi_seed (infinity if none).

## Three candidate contracts
### A — one-sided budget application: PROVISIONAL
For every M<=25 and n in {256,300}, given a compatible spectrum sigma, positive non-PF J subset A with rho_M^+(A)>=1, and t<lambda0 satisfying the Thm1 moment and anchor inequalities, short-L P positivity and its EXPLICIT fixed-n S bound <=1/sqrt(2), no certificate from D_M^+ seeds at n. These side conditions cannot be suppressed: rho alone is asymptotic, not a fixed-n theorem.
Cheapest falsifier: check the fixed-n bound and positivity. Existing evidence: inherited Thm1 PROVED with caveats; spin-2 rho is only TESTED and includes all sectors, not positive J only. PROVED without new Z intervals? Abstract implication yes; spin-2 application no. Answers Xiao? No: wrong data class, and no through25 hypothesis verification.

### B — dataset-specific two-sided fake: BLOCKED (rigorous application)
At beta64, exhibit finite rational spectra compatible with actual rigorous spin-2 Z/P boxes for k4..8 and F1--F4, killing S(256) and S(300). Soundness gives M_min>8 separately for these n.
Cheapest falsifier/discriminator: adapt existing NNLS + integer-cluster position adjustment to float low-temperature ED estimates; test a near-PF unit J competitor plus bulk. Evidence: spin-1 exact fakes, no spin-2 Z/P intervals. PROVED without new rigorous Z intervals? No: numerical compatibility is TESTED only. Answers Xiao? An initial mechanism test only, NOT >=26.

### C — Xiao through25 target: BLOCKED
At beta64, for each n in {256,300}, a spectrum compatible with actual spin-2 two-sided D_25 and F1--F4 violates Phi_seed(n). Restricting this witness to every smaller prefix would imply M_min>=26. Any anchors must be explicitly added and checked; none are assumed here.
Cheapest falsifier: a sound certificate at any M<=25. First cheap mechanism test: B. Evidence: universality estimates m65--100 are TESTED, not a lower bound. PROVED without new rigorous Z intervals? Only if a new rigorous analytic moment enclosure/identity replaces them; none exists in packet. Answers Xiao? Yes, within this explicitly limited certificate class. xi alone does not specify a moment sequence and cannot supply this theorem without a bridge.

## Deterministic selection (before solving)
Pick B because it tests actual two-sided compensation with ED-length resources; A misses the critique and C lacks data11..25. This is a bounded permitted intermediate, not a weakened resolution of C.

## Experiment B-test-v1
beta64, k4..8, n256/300. ESTIMATED Z/P via eight Ritz eigenvalues in each Sz=0,...,4 block (weight1 at0,2 otherwise); omitted levels not rigorously bounded. Float input => TESTED only. Adapt moment_nogo/explore_fake.py NNLS and build.py integer-weight position adjustment, with high precision for odd cancellations. Fix PF1.00001, extra J.999, bulk |x|<=.95; deterministic grid and no randomness. Accept only separate Z/P relative residuals <=1e-8, integer weights, strict PF, all-L positivity by finite prefix + geometric tail, and both S<=1/sqrt2. Preconditioning may change without changing this contract; retain failures. Stop on accepted witness or bounded declared search-class failure. A failed solver is NOT a nonexistence theorem.
YES: approximate data admit an accepted fake, TESTED only. NO: no accepted fake in this search class, TESTED only. Neither proves nor disproves >=26. Current evidence has NO established rigorous path to the ED-impossible lower bound: missing rigorous spin-2 boxes plus through25 extension/uniform mechanism. Do not close the campaign.
