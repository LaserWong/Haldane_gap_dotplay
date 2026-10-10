# Independent second-initialization scalar review

## Verdict and inherited premises

CONDITIONALLY ACCEPTED: gap at least23/5000=.0046 and a unique ground state for every integer L≥36, for the uniform periodic spin-one Heisenberg chain with unit bilinear coupling. The condition is validity of all18 published physical I/P thermal trace intervals atβ49/4, lengths4 through12, error30·10^-6. This scalar review does not claim a full local physical rerun of those18 traces. The β21/2 nine-input certification does not discharge these distinct premises. The accepted kernel/tiny fixtures are separate evidence, not full thermal validation.

The 72-site D26 variational anchor is the existing independently reconstructed contraction in audit/mps/contraction.out, with provenance in audit/APPENDIX_A_BRIDGE.md. Positive norm and −700741V72−500000U72>0 are checked exactly. U72 is a per-bond insertion, and the total shifted Rayleigh value is72(U72/V72+a), a=700741/500000. This supplies Z72(b)>1 at every positive b without any uniqueness assumption. No new contraction or imported source execution occurs here.

Producer manifest2ee9120d69863ab73babbcc9c07036cabcd787f9d8ad6b61f9f485656ccb1a59 is fully verified. INPUT_SHA256.json records all consumed dependencies. The source transfer identity is inherited only for integer lengths≥4; all claimed lengths≥36 satisfy it.

## Original signed-moment calculation

The inputs are same-temperature identity and π-seam physical traces, not separate temperature axes. Character inversion gives J_n=(Z_n+3Z_n(P))/4, N_n=(Z_n−Z_n(P))/4, Z_n=J_n+3N_n. J is the full D2-invariant list, containing I+2O; N is one of three identical lists. Each transformed moment error is conservatively bounded by30·10^-6. These are signed λ moments; odd moments cannot be silently replaced by |λ| powers or squared-variable moments.

The filters F_J=x⁴(7+17x−280x²−185x³+1000x⁴)² and F_N=x⁴(12−394x²+1000x⁴)² are nonnegative on the entire real axis. The summed upper bound is the signed center combination plus εΣ|coefficient|, equivalently selecting the adverse interval endpoint for every signed coefficient. Independent polynomial convolution reproduces B_J=318604.54848175 and B_N=48169.880699 exactly. Absolute convergence of the countable transfer spectrum legitimizes summing these degree4–12 terms; no trace of a lower power is required.

Support caps are |λ|<U=1.00139 in J and |λ|<V=.872 in N. Endpoint inequalities alone would be insufficient. The reviewer verifies the exact global ray identities Q(1+y)=559+2902y+5165y²+3815y³+1000y⁴ and Q(−1−y)=895+3978y+6275y²+4185y³+1000y⁴. Positive coefficients imply positivity and monotonicity for y≥0, covering both exterior rays because U>1. For N the even inner polynomial is positive atV and has derivative4r(1000r²−197)>0 for r≥V. The x⁴ factor is increasing in modulus. Consequently each filter exceeds its summed upper bound on both whole excluded rays. This proof retains odd coefficients and signs.

The twelfth-moment endpoints are mJ=1.0657205 and mN=.2783155. For nonnegative unit atoms bounded by h, the convex packing bound C(m,h,r)=floor(m/h)h^r+(m−floor(m/h)h)^r holds for r≥1, including countable lists by finite-subfamily limits. With ℓ=.999, set B(k)=3C(mN,V^12,k/12) and R(k)=B(k)+(mJ−ℓ^12)^(k/12), k36,72. The exact inequality C(mJ,ℓ^12,6)+B(72)<1 has margin>.0693. Since Z72(49/4)>1, at least one J eigenvalue has modulus>ℓ. Removing that one unit atom leaves the stated residual twelfth-moment mass. No fractional multiplicity or Hamiltonian realization claim is introduced.

The canonical seed is S(36,49/4)≥[1+R(36)/ℓ^36]^-2 and T(72,49/4)≥[U^72+R(72)]^-2. For S retain the leading λ^72 numerator; for T use Z72(49/2)>1 and the β49/4 denominator upper bound. This is correctly staggered S36/T72. Seed purities are approximately .9520842289937825 and .8184798319671879.

## Printed totals and original theorem replay

All18 integer W values parsed as literal data from published_scalar_enclosures.py match the official thermal72.tex table exactly. No imported Python code is executed. For each entry the reviewer reconstructs the integer-square-root enclosure and rational positive Taylor degree100 exponential bounds. Every interval is strictly inside its center±30·10^-6 by more than13·10^-6. This verifies the scalar conversion of published totals, conditional on those totals being valid outputs of the physical algorithm; it is not recomputation of physical columns.

The original six upward10^-7 defect updates are reproduced exactly. They use the newly rounded spatial defect in the thermal update and reach S2304/T4608 atβ784. Terminal defects84513/10^7 and27493/(5·10^6) are both<.01. The original published eventual theorem is log20/784 for even L≥2304. Its numerical value/scope should not be confused with this new conditional .0046 all-integer theorem or later archived reproductions.

## Optimized scalar continuation and finite windows

No new moment optimization is claimed. The producer uses finer downward purity rounding and continues the same canonical seed. At state(n,β), S means S(n,β), T means T(2n,β). Set K=S²T and update Snew=G(K), Tnew=G(T²Snew), G(z)=1−(1−z)²/(2z²), then double n and β. G is increasing on0<z≤1. Every saved result is bounded above by its independent exact unrounded expression, and every argument/result is positive. The review does not replace T(2n) with T(n) or use the old spatial value in the second update.

For each state K>1/2 gives a dominant normalized n-th spatial weight in X_(2β) at least w=(1+sqrt(2K−1))/2. The unique largest-modulus eigenvalue is positive: otherwise, compactness plus a finite even moment makes sufficiently large odd transfer traces negative. The official all-integer untwisted physical trace identity and physical positivity exclude that possibility. This is a leading-sign statement only; subleading eigenvalues may be negative.

Let ρ=(1−w)/w and d=T/(1+ρ²). For n≤L≤2n, a=L/(2n), the absolute tail at2n is at mostρ² and atL at mostρ. Hence Z_L(2β)≥[Z_2n(2β)/(1+ρ²)]^a(1−ρ). Absolute spectral Hölder independently gives Z_L(β)≤Z_n(β)^(2−2a)Z_2n(β)^(2a−1). Dividing and simplifying yields T(L,β)≥(1−ρ)S^(2−2a)d^a. Its logarithm is affine in a, so uniformly
C=(1−ρ)min(S sqrt(d),d).
A lower square root for sqrt(2K−1) produces an upperρ and lowerd,C. These directions are explicitly verified.

Every one of11 dyadic windows[36·2^j,72·2^j], j0..10, passes exp(β·23/5000)(1−C)<C with positive directed margin. Purity C>1/2 forces a largest Gibbs weight≥C, thus a unique ground state, and the next-to-ground ratio≤(1−C)/C proves the gap. This argument includes every odd integer in each window without assuming size-monotone thermal purity.

## Infinite closure

After ten updates, n=36864, β=12544 and common defect u≈7.23115·10^-27. For0<u≤.01 the inherited exact sequential recurrence gives both new defects≤5u²; the finite-window bound gives purity≥1−4u and excited-to-ground ratio≤5u. The rational endpoint inequalities and monotonic coefficients are checked independently. The strict inequality5u exp(12544·23/5000)<1 proves the same gap throughout all later dyadic windows because u_j≤(5u)^(2^j)/5 and β_j=2^jβ. No persistent numerical rounding floor is used in this analytical continuation. Earlier windows share endpoints and cover every integer36..36864, completing the all-L≥36 conditional result.

## Source provenance, corrections and tests

The review preserves exact unchanged official initialization.tex, thermal72.tex and trials.tex snapshots with Git blob pins a9a4604db87448b4e7d211ef483518b57862f097, b9f3c87a4fcfa96a82cdb5d4daf30b6088428037 and14be92f2308bc6758f3aac628e337a363caead77. URLs/hashes are in SOURCE_PROVENANCE.json. Apache2.0 LICENSE, attribution and prior relevant NOTICE checks accompany them. Producer official TeX copies each contain one additional trailing newline; this harmless discrepancy means their literal file bytes are not the stated Git blobs. We explicitly check this exact difference and preserve the producer seal rather than silently editing it. Producer certify.py also retains a stale n48 docstring; it is not the certificate scope.

Independent optimized_check.py uses110-decimal rational grids, integer-isqrt bounds and a separate140-term fixed-point Taylor enclosure, versus producer80-digit/120-term exact-Taylor machinery. It checks all saved purities, coordinates, windows, asymptotic values, anchor signs and dependency seals. Original scalar reconstruction took about.035CPU seconds, optimized review about.044, under256MiB onCPU5. Ten adversarial checks reject missing windows, wrong coordinates/temperature, inflated purities/gap labels and premature closure, and retain signed-odd and leading-sign safeguards. No minimum initialization size or below36 claim is made. Full thermal validation remains a separate outstanding task.
