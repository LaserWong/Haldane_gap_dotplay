# Uniform all-integer gap .0248 by finite completion

2026-10-10 22:52 EDT / 2026-10-11 02:52 UTC. Exact producer certificate; independent review pending.

## Result and initialization distinction

For the uniform periodic spin-one Heisenberg chain with unit bilinear coupling and the prescribed periodic convention, the producer certificate proves a unique ground state and gap >= 31/1250 = .0248 for EVERY integer L >= 2.

This stronger global bound uses the already accepted n34 bootstrap tail at gap .0248. The smallest separately certified bootstrap initialization remains n30 at gap .0179. Finite coverage reaching L2 is not a bootstrap initialization at2, and the stronger .0248 result must not be attributed to an n30 .0248 startup. No minimum-size or optimal-gap theorem is claimed.

The proof covers disjoint pieces without gaps:

- L2 and L3: exact total-spin algebra, gaps2 and1, unique ground states;
- L4 through L25: previously frozen purity certificates, rechecked exactly at the larger target gap .0248;
- L26 through L33: fresh own-length D26 MPS numerators and existing exact trace upper bounds;
- every integer L >= 34: the independently accepted n34 gap .0248 theorem.

No new thermal campaign, ED, tensor optimization, larger MPS bond dimension or root/remote edit is used. All prior sealed packages remain unchanged.

## Read-only cached prefix check

Before launching new anchors, check_cached_prefix.py reads the frozen finite-prefix L4..23 results, isolated parity L24 result and direct thermal L25 result. Their manifests are checked. It keeps each exact lower purity C and rechecks

    C - upper_exp((49/4) * .0248) (1-C) > 0.

All22 lengths pass. The weakest cached purity is L24, C >= .6813771416499027, with positive margin approximately .2496437965. Thus none of these lengths is a new bottleneck at the requested target. Their original Hamiltonians, temperature and own-length trial provenance are retained; no older gap label is merely relabeled without a fresh inequality.

The L2/L3 checks are inherited from the explicitly normalized finite-completion proof: H2 = 2 S1 dot S2 has energies -4,-2,2, and H3 = (S_total squared - 6)/2 has energies -3,-2,0,3. The singlet is unique in both cases. These analytic arguments do not extend the transfer proposition below its original domain L >= 4.

## Fresh physical anchors 26,...,33

For each L = 26,...,33 the unchanged audited physical D26 tensor blocks give exact integer contractions

    N0_L = Tr(T^L) > 0,
    H0_L = L Tr(T^(L-2) O),
    R_L = H0_L/N0_L + L * 700741/500000.

These are total energies and own-length norms. The odd trial states use their own odd-length contractions; no doubled or neighboring even quotient is substituted. Some R_L are positive and some negative. All signs are retained in the directed exponential.

Jensen for each normalized physical trial yields

    Z_L(2 beta0) >= exp(-2 beta0 R_L), beta0 = 49/4.

This requires neither a negative shifted Rayleigh nor prior uniqueness. The physical Hilbert space has dimension3^L, the MPS bond dimension stays26, and each numerator uses one trial state.

## Denominator bounds and odd-length Cauchy–Schwarz

The accepted18-input beta49/4 physical data, signed J/N moment intervals and support filters provide the already certified even upper traces Q26,Q28,Q30,Q32,Q34. The helper takes the safe minimum of exact twelfth-moment packing and the previously verified signed polynomial majorants sector by sector, then forms J + 3N with its correct multiplicities.

For even L, Z_L(beta0)^2 <= Q_L^2. For odd L, the real self-adjoint transfer's absolutely convergent eigenvalue sequence gives

    |Tr X^L|^2 <= (Tr X^(L-1)) (Tr X^(L+1)),

by Cauchy–Schwarz on lambda^((L-1)/2) and lambda^((L+1)/2). Both neighboring exponents are even. Physical Z_L is strictly positive, so division by its square is legitimate. Consequently

    Z_L(beta0)^2 <= Q_(L-1) Q_(L+1).

This uses the same temperature and full physical multiplicities. It assumes neither positivity of all transfer eigenvalues nor finite transfer rank. No separate odd physical thermal input is invented.

## Eight exact direct inequalities

For each new length, the checker forms lower_exp(-2 beta0 R_L) divided by the corresponding upper squared-trace bound, rounding downward. It verifies the lower purity is <=1 as a consistency check, exceeds1/2, and has a positive exponential gap margin at .0248.

Approximate displays of the exact saved purity bounds:

- L26: .8692559860
- L27: .7567727545
- L28: .8737925526
- L29: .7949222602
- L30: .8779999921
- L31: .8228656865
- L32: .8813220598
- L33: .8428024167

Every row passes. The weakest new row is odd L27, with margin approximately .4272003162. The finite prefix's overall weakest retained purity remains L24. The new proof therefore has comfortable finite margins; the asymptotic .0248 tail is inherited from the accepted n34 route rather than optimized here.

All acceptance arithmetic is rational with directed integer-root/Taylor-exponential enclosures. Floating decimals are displays only. certificate.json records every exact trial quotient, trace input, numerator bound, purity and margin. cached_prefix.json records the read-only prefix recheck.

## Dependency pins and acceptance boundary

The n34 producer manifest is fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84 and its independent review manifest is54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f. The finite4..23 producer manifest is71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08. Isolated24 and direct25 manifests are ef04180cedde73a09aa627c3dc75c2730472c9f425fd29bcec376678fea00240 and abd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa.

This new package is a producer proof. Independent review must check the fresh26..33 physical contractions, exact direct inequalities and coverage composition before promotion. An earlier independent direct25 run had a separately documented unresolved resource anomaly; this new internally consistent guarded batch does not rewrite or excuse that history.

## Guarded one-shot resource accounting

The batch uses the same exact small-power matrix multiplication, with binary powers through16 shared across eight lengths. max(L-2) = 31 is representable using1,2,4,8,16. Source accepts only26..33. It does not truncate physical tensors or eigenvalues.

The authorized physical run is a single process on CPU4, hard/soft30CPU seconds,100MiB address space, and an independent25-second monotonic wall watchdog. Before launch a guard-only self-test checks the limits, sole-CPU affinity, default unblockedSIGXCPU, parent-deathSIGKILL and separate process group. After exec, C++ rechecks CPU/address-space limits, CPU4 affinity, default/unblockedSIGXCPU and the parent-death signal and logs them before contracting. The parent watchdog cleans the process group; the launcher does not automatically retry. Compilation is separate under CPU2/512MiB/30CPU-second caps.

Observed successful batch measurements:

- independent wait4 user CPU:7.176423 seconds;
- independent wait4 system CPU:.073837 seconds;
- wait4 total CPU:7.250260 seconds;
- program CPU timer:7.244510 seconds;
- external wall elapsed:11.677676471 seconds;
- peak RSS:15824KiB;
- exit0, watchdog did not fire.

The scheduler-related difference between wall and CPU is retained, not collapsed into a single measure. Every observed quantity is below its applicable cap. Cached prefix replay is about.011CPU seconds; complete exact scalar replay is about4.5CPU seconds/~11MiB, with CPU2/30CPU-second/256MiB limits. No extra anchors or automatic reruns occurred.

## Reproduction

Use a disposable copy preserving sibling pins. For cached scalar proof run python check_cached_prefix.py and python certify.py. Fresh physical reproduction requires a separately authorized build of contract_prefix.cpp, then run_guarded.py in a fresh output directory; preserve original guard_resources.json because the launcher deliberately refuses automatic repetition. INPUT_SHA256.json and PREFIX_INPUT_SHA256.json pin sources; MANIFEST_SHA256.json and SEAL.json freeze this package. Do not modify previous seals or replace the old .0023 result while this stronger result awaits review.
