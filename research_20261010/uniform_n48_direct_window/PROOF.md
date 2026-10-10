# Extend uniform-chain coverage to L48 with a direct finite window

2026-10-10 19:12 EDT / 23:12 UTC. Exact producer candidate; independent new review pending.

## Claim, and what has not changed

For the periodic uniform spin-one Heisenberg chain with bilinear coefficient one:

1. A new exact direct time-first window gives a unique ground state and gap>=53/10000=0.0053 for every integer48<=L<=96.
2. Combining this overlapping window with the independently accepted gap>=19/5000=0.0038 for every integerL>=52 gives that same0.0038 bound for every integerL>=48.

The bootstrap INITIALIZATION remains n52. Only all-integer COVERAGE starts at48. No successful n48 bootstrap initialization, result below48, minimum-seed theorem, or adaptive all-temperature exclusion is asserted. This is fully compatible with the separately reviewed failure of the particular n48 canonical initialization grammar.

The proof uses only independently accepted48/96 MPS anchors. The newly explored50-site anchor and all floating adaptive scans are absent from every dependency and computation in this folder.

## Physical conventions and accepted dependencies

Let H_L=sum S_j dot S_(j+1), unit spin-one bilinear coupling, and use Z_L(beta)=Tr exp[-beta(H_L+aL)], a=700741/500000. Put beta0=21/2. The accepted history transfer is real, self-adjoint and Hilbert-Schmidt and obeys Z_L(beta)=Tr X_beta^L for every integerL>=2. Positive physical partition functions at odd lengths are essential for the signed-spectrum direct-window theorem.

The nine thermal inputs remain lengths6/8/10, all at beta0, with seam rotations0,pi,2pi/3. Their A4 multiplicity-space moments and certified support caps are taken from the frozen, independently accepted uniform_transfer_moment_assessment. The Hermite majorant and signed endpoint directions are the construction independently accepted in uniform_seed_frontier_review. These are not temperature labels or new physical computations.

The48-site norm and total energy integers are read directly from mps_excited_seed_review/independent_ground.out and checked against that review's manifest. The96-site integers are read from the accepted uniform_anchor96_100_review/anchors.out and its acceptance is checked. Both normalized trial vectors have nonzero norm and negative shifted total Rayleigh quotient. The code uses H0_L/N0_L+aL, not a per-site quotient mistaken for a total energy.

The direct signed-window lemma is the separately accepted integer_window_refinement_review. The inherited large-size theorem is uniform_seed_frontier_review, whose accepted verdict explicitly gives gap19/5000 for all integerL>=52. Required files are hash-checked and their hashes are recorded. No provisional50-site input is read.

## Two different purity inputs at their correct basepoints

The direct lemma needs

    A=T(48,beta0)=Z48(2beta0)/Z48(beta0)^2,
    B=S(48,2beta0)=Z96(2beta0)/Z48(2beta0)^2.

It does NOT accept T(96,beta0) relabeled as A. The two inputs below are computed separately at these exact common basepoints.

### A: a direct48-site thermal certificate

The accepted48-site shifted total Rayleigh quotient R48 is negative. Let v48<=exp(-beta0*R48), with a rigorous rational lower endpoint. At least one physical ground Boltzmann weight w0 is at least v48. Let Q48>=Z48(beta0) be the fixed Hermite/packing upper moment envelope. Then

    A >= w0^2/Z48(beta0)^2 >= (v48/Q48)^2.

No ground-state uniqueness is assumed. This only uses one retained ground contribution plus a complete trace upper bound. Exact replay gives

    A >= 782159275175083593289269/10^24
      = approximately0.7821592751750835.

The Q48 upper uses all three A4 sector moment bounds, with physical multiplicities1,2,3 included once. It is not an MPS norm-transfer trace.

### B: a spatial certificate at beta21

Use even base moment length ell=26 at beta0. For the accepted sector upper envelopes A26,B26,C26, set z=A26+2B26+3C26 and e=A26+2B26. The untwisted trace is at most z, and every nonidentity tetrahedral seam has a physical trace at most e. Ordinary Gibbs cooling by factor2, separately for each seam Hamiltonian, gives at beta21

    D=z^2, E=e^2,
    tau=(D+11E)/12, tau0=(D+3E)/4.

Outward rounding only increases upper bounds. These cap the total, trivial and trivial-plus-complex transfer masses at the same cooled temperature.

The accepted96-site shifted Rayleigh quotient R96 gives W<=exp(-21*R96), so Z96(21)>=W>1. For nonnegative weights |lambda(X21)|^26, write the largest weight as t. Set p=96/26=48/13 and q=48/26=24/13. Total-power forcing gives a lower t0 from D*t0^(p-1)<W. The exact check2*t0>D proves uniqueness and trivial-sector membership of this leading transfer atom. It does not assume a preexisting physical ground-state uniqueness theorem.

With the leading atom removed, the reviewed residual polygon gives, for every exponent j>=1,

    R_j(t)=max[x^j+2(y/2)^j+3((D-t-x-y)/3)^j]

over(0,0),(tau-t,0),(tau-t,tau0-tau),(0,tau0-t). It decreases with t. Thus t^p>=W-R_p(t0), giving successive directed lower roots. Every strict inequality is checked against the fixed W. Fractional exponents are legitimate because weights are nonnegative and q,p>=1; no spatial/temperature interchange is made.

The spatial purity obeys

    B >= [1+R_q(t0)/t0^q]^-2
      >= 213232331787153576811891/(250000000000000000000000)
      = approximately0.8529293271486144.

Every endpoint, polynomial coefficient, mass bound and leading-atom update is stored in certificate.json. In particular, the base26 sector construction and the physical numerator length96 remain distinct.

## Direct all-integer window, including odd lengths

The accepted direct time-first lemma states that for an even n, valid a<=T(n,beta), b<=S(n,2beta) with b>1/2 imply

    T(L,beta) >= a^2 sqrt(2b-1), every integer n<=L<=2n.

Its proof normalizes the nonnegative spectrum of X_(2beta)^n. Purity b>1/2 singles out one largest-modulus eigenvalue. That eigenvalue must be positive, because otherwise sufficiently large odd physical traces would be negative. The signed remainder is bounded by its absolute mass, and Schatten power monotonicity controls the denominator. Thus no odd-base purity assumption or positivity of all transfer eigenvalues is needed.

With n48,beta=beta0,a=A_lower,b=B_lower, exact square-root rounding yields

    C = 256991805584988123566957/(500000000000000000000000)
      <= T(L,beta0), 48<=L<=96,

approximately0.5139836111699763, strictly greater than1/2. The exact Taylor upper bound satisfies

    exp(beta0*53/10000)*(1-C) < C,

with positive margin approximately0.000153676038362561. Therefore the physical ground state is unique and gap>=0.0053 at every integer length in that window. This is a positive finite-window certificate, not a sampled trend or a failure-to-find-candidate statement.

## Coverage composition

The new window covers all integers48..96. The existing independently accepted theorem covers all integersL>=52 with gap>=0.0038. Their overlap52..96 is nonempty and complete. Since0.0053>0.0038, their union proves the stated0.0038 lower bound and unique ground state for every integerL>=48.

No new asymptotic recursion is invoked at n48. The old n52 initialization, beta567/25, and asymptotic onset3328 remain the large-size mechanism. This coverage extension does not contradict any n48/n50 startup exclusion in a separately defined grammar.

## Reproduction, resources and preservation

Run python certify.py. The producer replay uses CPU0,100MiB address space and120CPU-second limits. Actual runtime is about0.49CPU seconds with10.6MiB resident memory. It performs no new physical contraction, eigensolver or heat trace. Exact rational power roots are verified by powers, and exponential bounds use a Taylor remainder and directed squaring.

INPUT_SHA256.json records all consumed accepted inputs. MANIFEST_SHA256.json seals this folder. All older producers/reviews, root state and GitHub remain unchanged. The new composition and scalar window are producer claims awaiting independent review; the supporting physical anchors and inherited theorems are already accepted.
