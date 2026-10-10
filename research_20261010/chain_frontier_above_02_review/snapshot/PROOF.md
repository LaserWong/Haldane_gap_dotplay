# Alternating-chain frontier above 0.2

Updated 2026-10-10 17:21 America/New_York (EDT) / 21:21 UTC.

Status: producer exact candidates pending independent review. Read summary.json for the completed discrete couplings. No continuous interval, optimal frontier, physical transition, or infinite-volume uniqueness is asserted.

## Model and input boundary

H_M(g)=Σ_i S_(i,0)·S_(i,1)+g Σ_i S_(i−1,1)·S_(i,0), with spin one, strong exchange one, periodic cells, and all M oriented weak links retained (including both physical links at M=2). There are 2M physical sites and 9^M states.

The previous accepted thirteen-reference-vector certificate at g=.2 is limited by its [8,16] finite window rather than its final asymptotic estimate. Our bounded scan of the unchanged recipe at g=.21,.22,.225,.25, β=2,2.05,…,80 found no passing scalar path. This is not an all-temperature impossibility. Optimizing the same E<2 compression cutoff over the recorded rational local-coefficient grid did not remove this bounded failure.

The new physical input enlarges only the M=4 bare reference space. The largest seed M=8 is unchanged: a rational two-vector linear combination evaluated from sealed first-moment matrices supplies only a Rayleigh upper bound, with support 43,294 in physical dimension 43,046,721. No M=8 action, residual, lower energy, low band, or full spectrum is used. Its trial support and two-dimensional combination space are not MPS bond dimensions.

## Weighted reference space and complete counting

Set H'=H_4+8I=E+gV, with strong-dimer levels 0,1,3 and degeneracies 1,3,5. Let P project onto E<3. Its dimension is

1 + 4·3 + binomial(4,2)·3² = 67.

This consists of the bare vacuum, twelve single triplets, and fifty-four two-triplet states. All twenty single quintets have weighted energy 3 and remain in Q=I−P. No occupation parity or particle-number conservation is assumed. The full complement dimension is 6,494.

In the rational Clebsch–Gordan basis the exact Gram weights are (3,2,2,2,1,2,6,2,1). expanded_moments.json records every Gram entry, compressed first weak moment K, and full second weak moment J. Full physical action, including every leaked configuration, constructs J. Define

R_Gram = J − K G^−1 K.

Because E preserves P, the residual Gram of H' is g² R_Gram. It is not the square of a truncated compressed Hamiltonian.

The rational local certificate is

g V_local + a(h_i+h_j)+bI > 0.

All 81 local pivots are checked exactly. Summing over four edges yields H'≥αE−B, with α=1−2a>0 and B=4b. Thus QH'Q≥A Q, A=3α−B. Optimization proposes a; exact local positivity verifies b. The coefficients of (1+3x+5x³)^4 are the complete reference multiplicities. The omitted bins E≥3 contain exactly 6,494 states, including every quintet. Global min–max gives all their ordered lower endpoints αe−B.

## Partial spectrum through exact inertia, without band isolation

Write the physical block matrix H'=[[D,R*],[R,C]], with C≥A I. For any rational t<A the complement C−t is positive and the physical negative inertia below t is at most the negative inertia of

D−tI−R*R/(A−t).

In rational unnormalized P coordinates the congruent comparison is

F(t)=(A−t)(H_PP−tG)−g² R_Gram,

where H_PP is diag(E)G+gK. Multiplication by A−t>0 and congruence by the positive Gram metric preserve inertia. If F(t) has exactly k negative eigenvalues and no zero eigenvalue, then at most k full physical eigenvalues lie below t. Therefore λ_(k+1)(H')≥t. This statement uses the whole omitted complement and does not assume sixty-seven physical Ritz levels below A.

The floating spectrum of a 134-dimensional comparison matrix proposes rational thresholds only. Every accepted threshold is rounded down, lies strictly below A, and has its negative and zero counts verified by exact fraction-free symmetric elimination. Sorted thresholds with counts 0=k₀<k₁<… give ordered lower bins of multiplicities k_(j+1)−k_j; the final bin ends at rank 67 because global min–max controls λ_68≥A. The counts, rather than inferred spin labels or numerical degeneracies, justify the retained multiplicities.

The independently replayed M=4 rational ground vector has full action support, full residual and a Temple ground enclosure. Its lower endpoint replaces only the first comparison endpoint, after checking that it lies above the first comparison bound and below the second. It is not counted twice.

## Complete heat trace

With rho the M=4 Rayleigh upper endpoint and e_- its verified ground lower endpoint,

exp(β rho) Z_4(β) ≤ exp[β(rho−e_-)]
 + Σ_(retained bins except ground) m_j exp[−β(−8+t_j−rho)]
 + Σ_(e≥3) m_e exp[−β(−8+αe−B−rho)].

The β=0 count is exactly 1+66+6,494=6,561. Every exponential is rationally enclosed outwards. Complete omitted reference counts, rather than a sampled Ritz list, supply the final tail.

## Scalar paths and every integer cell count

The accepted joint-ratio recurrence and signed-transfer interpolation of joint_ratio_review are reused at the same spatial and thermal basepoints. Initial J=Z_8(2β)/Z_4(β)^4 has a lower endpoint from the largest Rayleigh term and the complete small trace upper bound. The corresponding C ratio uses the small trace at 2β. Each candidate records all time-first steps, canonical conversion, later canonical steps and every intermediate finite window. No early window is dropped when optimizing the eventual asymptotic bound.

The same initial joint endpoint gives S≥sqrt(J), T≥J, S²T≥J at (M=4,β), and therefore the full integer [4,8] window, including odd M=5,7. At M=2,3 the saved exact local comparison gives the direct singlet-product bridge gap≥1−2a−Mb. Later windows [8,16],[16,32],… meet the terminal all-integer small-defect theorem without a missing integer cell count. The reported uniform gap is the minimum of every short bridge, every finite window and the asymptotic bound. Strict exact exponential witnesses certify each positive gap.

## Reproduction and scope

All work runs on one allowed CPU, one BLAS thread and a one-GiB address-space ceiling. The M=4 sparse ground search computes one lowest trial eigenvector; exact action replay, not its floating eigenvalue, certifies the ground interval. The only other eigensolves are local/comparison matrices. No many-body full-spectrum diagonalization is performed.

The workspace has no Git metadata. Existing packages and root files are unchanged. FROZEN_MANIFEST.json seals this package, and EXTERNAL_INPUT_SHA256.json records inherited source and data hashes. Run REPRODUCE.sh for a clean sibling replay, which does not overwrite this freeze. This is an exact-arithmetic executable certificate pending external independent review, not proof-assistant formalization.
