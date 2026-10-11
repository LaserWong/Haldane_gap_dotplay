# Independent completion of every periodic length

2026-10-11 02:51UTC /2026-10-10 22:51 America/New_York.

## Verdict and exact scope

ACCEPTED: for the uniform periodic spin-one Heisenberg chain with unit bilinear exchange, every integer L≥2 has a unique ground state and a spectral gap at least23/10000=.0023. The periodic two-site convention counts both terms in sum_j S_j·S_(j+1). The bootstrap initialization remains30. This review completes finite-size coverage; it does not initialize a bootstrap at2 or prove a minimum size.

The proof is a disjoint covering of all integers: analytic L2 and3, newly checked direct thermal certificates at every L4..23, and the previously independently accepted tail L≥24. Stronger accepted nested bounds remain .0179 forL≥28, .0245 forL≥32 and .0248 forL≥34. These are certified lower bounds, not claims about the actual or optimal gap.

Producer seal71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08 is fully verified. All40 new physical norm/total-energy integers and all20 finite gap inequalities independently match. Fourteen new whole-domain signed moment majorants pass. This batch's guarded resources are consistent and within limits. The distinct direct25 resource anomaly remains unresolved and is explicitly inherited, not overwritten.

## 1. Small volumes2 and3, without extending the transfer theorem

The model is H_L=sum_j S_j·S_(j+1), S_j²=2, with periodic indices. At2, both oriented periodic terms are present:

    H2=2 S1·S2=S_total²−4.

Coupling two spin-one representations yields total j0,1,2 once each. The energies are−4,−2,2, with physical degeneracies1,3,5. The unique singlet is the ground state and the gap is2.

At3 each pair appears once:

    H3=(S_total²−6)/2.

Successive exact angular-momentum coupling gives multiplicities m0=1,m1=3,m2=2,m3=1. Their full dimensions1+9+10+7=27 equal3³. Energies at j0,1,2,3 are−3,−2,0,3. The unique singlet ground state has gap1. In particular the singlet multiplicity is not the j1 multiplicity of three.

The independent checker reconstructs these multiplicities by the finite coupling rule j tensor1=|j−1|,...,j+1, checks physical dimensions and computes the exact energies. The normalization is explicitly pinned in audit/APPENDIX_A_BRIDGE.md. No numerical diagonalization, extrapolated trial quotient or transfer identity below its source-verified L≥4 range is used. Both gaps exceed.0023; an additive energy shift leaves them unchanged.

## 2. Fresh physical trial states at every own length4..23

The reviewer freshly reconstructs the fixed D26 site matrices entrywise from their physical representation labels and coefficients. It forms T=sum_s A_s tensor A_s and the exact two-site Heisenberg insertion O. Difference blocks follow the physical magnetization selection rule. The reconstructed block data matches the independently accepted original bytes. Direct physical amplitudes at2 and3 check both norms and TOTAL energies.

The inspected reviewer engine uses exact sequential GMP powers, independently of the producer's shared binary/small-power implementation. A single guarded run emits every pair

    N0_L=Tr(T^L), H0_L=L Tr(T^(L−2)O), L=4,...,23.

All40 integers match the producer exactly and every norm is strictly positive. Each row is its own physical length, including odd lengths. No neighboring even-size quotient is reused. The total shifted trial energy is R_L=H0_L/N0_L+L(700741/500000), with no missing or extra factor L. The physical trial has bond dimension26 and one-dimensional span inside a3^L-dimensional Hilbert space; neither26 nor676 is a thermal-rank cutoff.

For the normalized trial, the variational principle gives E0≤R_L, hence

    Z_L(2beta)≥exp(−2beta R_L).

Negative and positive R_L are both allowed. Several odd-length R_L are positive; the checker retains their exponential suppression and never substitutes a ground contribution of1. No ground uniqueness is presumed.

## 3. Untwisted physical inputs and new signed long traces

At L4..12, the denominator upper bound is selected explicitly from case Lk_I in the final physical thermal review792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94. The pi-seam P value is not a physical untwisted substitute. All nine identity entries are present and exactly matched to the refined outward intervals derived from the independently reproduced integer totals and error enclosures.

For longer lengths, the entire18-input physical-to-signed-moment mapping is checked against the accepted J,N moments4..12. The full physical trace is J+3N, including the multiplicity3. Odd moments retain their signs; x is a signed transfer eigenvalue, not its square.

The new orders are13,14,15,17,19,21,23 for both sectors. For each exact rational degree8 polynomial p, the reviewer proves p(x)−x^(k−4)≥0 over the entire closed signed support interval. It constructs full-degree Bernstein coefficients and independently subdivides by exact de Casteljau arithmetic until all leaf coefficients are nonnegative. Every leaf count and maximum depth matches. Multiplication by x^4 proves x^4 p(x)≥x^k, including x=0 and the negative half-line. The odd target is not replaced by |x|^k. The negative-N upper bounds at13,15,17,19,21,23 are specifically checked to remain negative.

Summation is valid for the countable spectrum: bounded support and finite fourth/twelfth absolute moments give absolute convergence of the required powers. Coefficients of either sign choose the corresponding conservative moment endpoint. Shared raw-trace correlations require no independent attainability assumption. No finite transfer rank or relaxation-to-physical realization is invoked.

Already accepted even majorants cover16,18,20,22,24. Absolute twelfth-moment packing gives an additional valid upper bound, including at odd orders where it can simply be weaker than a signed polynomial. The minimum of valid upper bounds remains valid. The final Q_L=J_upper+3N_upper is strictly positive even where N_upper<0. Optional Cauchy–Schwarz from adjacent even traces supplies another safe odd upper bound; each chosen method and denominator is independently checked. Every odd13..23 row selects the sharper signed polynomial in this package. Floating proposal searches are never executed or accepted as proof.

## 4. Exact direct finite gaps and union with the tail

At beta49/4 let Q_L be the certified physical upper trace. The normalized Gibbs purity obeys

    T_L(beta)=Z_L(2beta)/Z_L(beta)^2
             ≥exp(−2beta R_L)/Q_L².

The reviewer computes independent140-digit outward rational powers and exponential bounds. For positive exponential arguments it uses a lower truncated Taylor sum with downward squaring; for negative arguments it reciprocates a certified upper bound. Each saved numerator lower endpoint and denominator upper endpoint has the required direction. Every saved C_L is in(1/2,1], and the exact check

    C_L−exp[(49/4)(23/10000)](1−C_L)>0

passes for all twenty integers4..23. The smallest displayed purity is approximately.8604973284 at17. Integer data and rational margins, not these displays, establish the result.

Purity>1/2 forces a unique largest Gibbs weight and therefore a unique physical ground state. The ratio bound for the remaining weights gives the stated gap. The previously independent direct25 composition, seala70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9, gives the same gap for every integer≥24. Together with the exact2/3 argument there are no missing integers. No monotonicity in physical size or cooling temperature is used.

## 5. Guarded execution, timing and adversarial checks

The new reviewer physical batch was separately authorized for30CPU seconds/100MiB onCPU5 with an external25-second wall cutoff and no automatic retry. Its inspected launcher creates a separate process group, sets verified parent-death SIGKILL, restores/unblocks SIGXCPU, asserts resource limits and pins both the executable and freshly rebuilt block digest. A preflight guard-only self-test passes. The supervisor independently records monotonic wall time and wait4 user/system CPU and kills the entire group at the wall limit or on cleanup. Post-exec /proc observations verify CPU soft/hard30/30, address-space104857600/104857600, one thread and affinityCPU5 for the running sequential executable.

Observed successful batch: wall4.278608064s; wait4 user4.167127s and system.045742s, total4.212869s; program clock4.20801s; peak8260KiB; exit0; no wall kill. These are separate measurements and mutually consistent. The fresh reconstruction and guard-only self-test are separately logged. No claim is made that this consistent run explains or repairs the historical direct25 timer/limit anomaly. That earlier sealed review continues to mark15-second compliance unaccepted.

The independent scalar replay uses about5.24CPU seconds/14.4MiB under30CPU seconds/256MiB. Adversarial checks reject turning negative odd-N bounds unsigned, selecting each wrong pi seam in place of identity, the wrong two-site bond multiplicity, a spurious threefold singlet at3, calling coverage2 initialization2, and omitting23 from the union. No imported producer scientific code is executed.

All exact data, source pins, post-exec observations, wait4 records and proof outputs are sealed. Replay only in a disposable copy. The cheap audit is python audit.py. A fresh physical run requires the guarded launcher and a new authorized output directory; its one-shot record must not be deleted to bypass no-retry behavior. All prior producer/reviewer seals remain unchanged.
