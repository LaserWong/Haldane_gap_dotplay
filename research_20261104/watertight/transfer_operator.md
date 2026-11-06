# Transfer-operator condition: statement, proof, sanity checks

Repo: LaserWong/Haldane_gap_dotplay @ a99fa21 (read-only clone; nothing modified).

## Claim used by the n=8 exclusion
For the periodic spin-1 Heisenberg chain H_L = sum_j S_j.S_{j+1} (L=2 counts both bonds) and
Z_L(beta) = Tr exp[-beta(H_L + aL)], a = 700741/500000
(heat_trace/audit_inputs/APPENDIX_A_BRIDGE.md:9), there is, for each beta > 0, ONE real symmetric
Hilbert-Schmidt operator X_beta with Z_L(beta) = Tr X_beta^L for every integer L >= 2
(stated without proof at APPENDIX_A_BRIDGE.md:23; also used at :33, :78).

Consequence used here: for even m <= M, Z_M(beta) <= Z_m(beta)^{M/m}. In particular
  W_8(b) = Z_16(2b)/Z_8(b)^4 <= Z_12(2b)^{4/3} / Z_8(b)^4.
(Any even m in [2,16] is valid; the n=8 certificate uses m = 12 = n+4, NOT n+2.)
W = S^2 T is the quantity of seed_size/proofs/DERIVATIONS.md:3-13,89; W <= 1/2 for all b means the
scalar G-iteration can never enter its contracting region. This is an impossibility statement about
THAT scalar method (DERIVATIONS.md:13 says the same), not about the physical gap.

## Proof  (status: PROVEN)
1. Real Cartesian spin-1: (A_alpha)_{beta gamma} = -eps_{alpha beta gamma}, S_alpha = i A_alpha.
   A_alpha real antisymmetric, ||A_alpha||_op = 1. Then S.S' = sum_alpha (iA_alpha)(x)(iA_alpha)
   = -sum_alpha A_alpha (x) A_alpha, so -beta(H_L + aL) = beta * sum_{b,alpha} V_{b,alpha} - beta a L,
   V_{b,alpha} = A_alpha^{(b)} A_alpha^{(b+1)}  (3L commuting-or-not terms, each norm 1).
2. Expand exp(beta sum_j V_j) = sum_m (beta^m/m!) (sum_j V_j)^m. Equivalently: a positive measure on
   finite sets of marked times {(t_i, b_i, alpha_i)} in [0,beta], the time-ordered product of the V's.
   The series converges absolutely in operator norm (sum_m (3L beta)^m/m!), so trace and sum commute.
   The measure is a product over bonds: mu = (x)_b mu_b, each mu_b (3 colours, unit rate on [0,beta])
   has finite mass e^{3 beta}.
3. Each V factorizes over sites, so the trace of a time-ordered product factorizes:
   Tr = prod_s f(omega_{s-1}, omega_s), f(omega,omega') = Tr_C3[ time-ordered product of A_alpha over
   the points of omega u omega' ] (ties have measure zero).
   Hence Z_L = int prod_s F(omega_{s-1},omega_s) prod_b dmu(omega_b), F = e^{-beta a} f,
   which is Tr X^L for the integral operator X with kernel F on L^2(Omega, mu_1).
4. F is REAL (A real), SYMMETRIC (f depends only on the union omega u omega', which is symmetric),
   and BOUNDED: |F| <= 3 e^{-beta a} (trace of a product of norm-1 3x3 matrices).
   With mu_1 finite, int int |F|^2 <= 9 e^{-2 beta a} e^{6 beta} < infinity: X is Hilbert-Schmidt and
   self-adjoint. For L >= 2, X^L = X * X^{L-1} is a product of two HS operators, hence trace class,
   and Tr X^L equals the cyclic iterated kernel integral (Fubini justified by boundedness + finite mass).
   So Z_L(beta) = sum_i lambda_i^L with real lambda_i (both signs allowed).
5. For even L, Z_L = sum |lambda_i|^L = ||lambda||_L^L. l^p norms decrease in p, so
   ||lambda||_16 <= ||lambda||_12, i.e. Z_16(2b) <= Z_12(2b)^{4/3}, using the SAME operator X_{2b}
   for both lengths (it does not depend on L). QED.

## Numerical sanity checks (NOT part of the proof)
Scripts: tm_check.py, tm_check_lib.py, mc2.py; logs tm_check.log, mc2_L{2,3,4}.log. beta = 0.5.
- Cartesian basis identities and ||A_alpha|| = 1 verified.
- Discretized kernel X_M (4^M states, symmetrized): Tr X_M^L increases toward ED; cubic Richardson
  in 1/M (M=2..5) matches ED within 0.12-0.38% for L=2..5. X_M has negative eigenvalues (min ~ -1.055),
  consistent with "spectrum can have either sign".
- Direct Monte Carlo of the bond-history integral, 1.5e6 samples:
  L=2: 17.3565 +- 0.035 vs ED 17.3833 (z -0.76); L=3: 40.312 +- 0.235 vs 40.508 (z -0.83);
  L=4: 164.43 +- 1.55 vs 163.484 (z +0.61).
