# Smaller uniform-chain seeds from cooled sector moments

2026-10-10 18:22 EDT / 22:22 UTC. Exact producer candidates; independent review pending.

## Three separate results

For the uniform periodic spin-one Heisenberg chain with unit bilinear coupling, the following producer certificates now pass exact replay:

1. Existing physical seed n=60, existing MPS120 anchor, beta=105/4: gap >= 51/5000 = 0.0102 for every integer L>=60. Small-defect entry is L=960. This strengthens the scalar bounds and adds earlier finite-window coverage; it does not reduce the physical seed. The historical audited bound 0.005908566393 for L>=1920 remains untouched.
2. Smaller physical seed n=56, new exact MPS112 anchor, beta=609/25: gap >= 17/2500 = 0.0068 for every integer L>=56. Small-defect entry is L=1792. This uses the original squared-sector-tail recipe with sharper moment caps, different base length28 and cooling ratio58/25.
3. Smaller physical seed n=54, new exact MPS108 anchor, beta=2373/100: gap >= 1/400 = 0.0025 for every integer L>=54. Small-defect entry is L=3456. This additionally uses the direct-sector-power lemma below, which allows the canonical seed length54 to differ from twice the base moment length28. Its cooling ratio is113/50.

No gap for L below the stated seed is claimed, and no minimal seed theorem is claimed. All three results await independent physical/scalar/analytic review. The exact seed purities, every finite integer window, asymptotic constants, and positive exponential margins are in certificates.json.

## Inherited physical inputs and conventions

Read the frozen sibling uniform_transfer_moment_assessment/ASSESSMENT.md for the complete identification. In short: beta0=21/2, shift a=700741/500000, nine physical traces at lengths6/8/10 with seam rotations0,pi,2pi/3; A4 sector multiplicity spaces I,O,N and full trace I+2O+3N. I/P/C are seams, not doubling directions. The sibling replay rigorously refines the three transfer support caps and bounds each even moment at beta0. Its manifest/result hash is checked here and its seal is unchanged.

For every even base length ell>=10, let A_ell,B_ell,C_ell denote the sibling's upper sector moments. Define

    z=A_ell+2B_ell+3C_ell,
    p=A_ell+2B_ell.

The untwisted trace is at most z. Every nonidentity tetrahedral seam has a physical trace at most p: the two possible character combinations are I+2O-N and I-O. All these physical partition functions are nonnegative. For any rational cooling ratio r>=1, ordinary Gibbs norm monotonicity separately for each physical seam gives total upper D=z^r and nonidentity upper E=p^r at beta=r beta0. No independently computed second-temperature trace is asserted.

The cooled trivial and trivial-plus-complex sector masses consequently satisfy

    I_ell(beta) <= tau=(D+11E)/12,
    I_ell(beta)+2O_ell(beta) <= tau0=(D+3E)/4,
    total <= D.

D,E are rounded upward, preserving these inequalities. The new numerical values satisfy D>=tau0>=tau>0. These equations parameterize the original proof's constants D=1.450,E=1.202,tau=1.225,tau0=1.264; they are no longer rounded to that coarse fixed set.

## Exact MPS anchors and resource gate

The archived physical D26 matrices and two-site Heisenberg insertion are the independently audited audit/mps/mps_blocks.txt. The copied contraction uses exact GMP integer arithmetic on their difference blocks. It returns H0_L=L*Tr(T^(L-2) O) and N0_L=Tr(T^L), so the total unshifted Rayleigh quotient is H0_L/N0_L. Its per-bond quantity would be smaller by L; these conventions are not mixed.

The copied engine is modified only to accept requested lengths, support enough binary powers, reject unreadable/wrong-count block input, and enforce700MiB/600CPU seconds. No matrix-building or multiplication rule changes. CPU affinity is one CPU0. An initial attempted path was absent; its zero-output result was discarded before validation, and explicit input rejection was added. The actual benchmark at48 consumed10.3954CPU seconds and32224KiB, matching both archived integers exactly. Only after that gate was the104/108/112/120 batch run; it consumed23.5523CPU seconds and38324KiB. The new120 integers also match the independently audited archived120 exactly, including H0_120=120*U120 and N0_120=V120. Physical interpretation of the block file remains an inherited audited premise, not an inference from numerical matching alone.

All new normalized trial states are nonzero. Their total shifted Rayleigh quotients are strictly negative by exact integer inequalities. Displays are approximately -1.0938916430e-5 at104, -1.1359094931e-5 at108, -1.1779556395e-5 at112, and -1.2620790579e-5 at120. The certificate uses only negativity, not those decimal values or a conjectured infinite-size energy.

At anchor length2n this supplies Z_(2n)(beta)>1 for every beta>0 and a ground Boltzmann weight greater than1. Uniqueness is not assumed at this stage. Each anchor is one physical D26 MPS trial state; D26 is neither the physical Hilbert dimension3^(2n) nor the thermal transfer rank.

## Sector tail lemma, including arbitrary powers

Fix an even base length ell. At cooled beta let nonnegative transfer weights be w_i=|lambda_i|^ell, with the full physical multiplicities1,2,3 included. Let their largest weight be t. For any p0>=1,

    sum w_i^p0 <= t^(p0-1) sum w_i <= t^(p0-1) D.

At anchor length2n with p0=2n/ell, the left side is the physical trace and is greater than1. Thus any t0 with D*t0^(p0-1)<1 is a strict lower bound on t. All selected cases use t0=4/5, and2t0>D. Therefore the leading atom is unique and lies in the trivial sector: any additional equal leading copy, or a complex/vector representation's required multiplicity, would exceed D. Since ell is even, this argument does not yet require a positive sign for lambda; the inherited all-integer interpolation supplies that sign when needed.

After removing this one trivial atom, write x for the remaining trivial mass, y for the combined complex mass, and zeta for the vector mass. Their constraints are

    0<=x<=tau-t,
    0<=x+y<=tau0-t,
    0<=x+y+zeta<=D-t.

For any exponent q>=1 their q-power tail obeys

    tail_q <= x^q + 2*(y/2)^q + 3*(zeta/3)^q.

The factors2,3 follow from identical copies in the relevant irreducible representations, and ordinary l^q convexity within each multiplicity list. No finite rank or fabricated count is assumed. Replace zeta by D-t-x-y, which increases the expression. The remaining function is convex in(x,y) on its polygon, so its maximum is attained at one of

    (0,0), (tau-t,0),
    (tau-t,tau0-tau), (0,tau0-t).

Call this maximum R_q(t). It is decreasing in t on0<=t<=tau: at each displayed vertex, every nonconstant nonnegative component decreases with t and the other components remain fixed. This proves the direct-sector-power lemma for every real q>=1, including the rational noninteger exponents used at n54. This is an analytic generalization of the original quadratic polygon bound, not a numerical extrapolation.

Given a known lower bound t0, Z_(2n)>1 and the lemma imply

    t^p0 > 1-R_p0(t0).

This tightens t by a directed lower p0-th root. Iterating preserves validity. In the original squared-tail mode, the weaker but originally proved bound tail_4 <= R_2(t0)^2 is used instead. n60 and n56 use this original mode, with p0=4. n54 uses the direct bound at p0=27/7. Every update in certificates.json includes a strict contradiction upper sum below1. The code never assumes a passing moment screen establishes realizability.

## Spatial and thermal seed purities

At canonical seed length n, put q=n/ell>=1. For the known leading mass bound t0,

    Z_n <= t^q + R_q(t0),
    Z_(2n) >= t^(2q),
    S(n,beta)=Z_(2n)/Z_n^2
       >= [1+R_q(t0)/t0^q]^(-2).

This remains valid for rational q. n60 and n56 have q=2; n54 has q=27/14. The leading-weight construction is at the common cooled beta, whereas the anchor length2n is fixed independently. This is why changing base length does not silently change temperature or canonical geometry.

At beta0 let Q be the certified untwisted upper trace at anchor length2n. Its ground Boltzmann weight w0 exceeds1 by the trial anchor. Remaining mass is at most Q-w0<Q-1. Cooling by r>=1 gives remaining-to-ground ratio at most(Q-1)^r. Therefore

    T(2n,beta) >= [1+(Q-1)^r]^(-2).

This is the ground-plus-tail cooling mechanism of the old proof, which is much sharper here than Z(2beta)<=Z(beta)^2. No separate2beta input or ground-state uniqueness premise is needed.

The selected seed bounds (display only) are:

- n60,beta26.25: S>=0.879366793876755, T>=0.882386452652102;
- n56,beta24.36: S>=0.871523270082368, T>=0.880888618271534;
- n54,beta23.73: S>=0.863373202575697, T>=0.883355350322216.

## Recurrence and every preceding integer window

The code performs the archived sequential canonical update with exact rational downward rounding:

    S_new=G(S^2 T),
    T_new=G(T^2 S_new),
    G(z)=1-(1-z)^2/(2z^2),
    n_new=2n, beta_new=2beta.

Every update has a positive legal argument and output. At common defect u=max(1-S,1-T)<=1/100, the inherited small-defect theorem gives the all-integer asymptotic gap provided exp(beta*gap)*5u<1. That strict inequality is checked by rational Taylor upper bounds; no floating logarithm certifies it.

Every state before asymptotic acceptance also has a separate finite-window proof using research_20261010/root_review/FINITE_WINDOW_INTERPOLATION.md. In its one-dimensional formula, put p=S^2T>1/2, w=(1+sqrt(2p-1))/2, rho=(1-w)/w, d=T/(1+rho^2), and

    C=(1-rho)*min(S*sqrt(d),d).

The supplied lower C bounds T(L,beta) for every integer n<=L<=2n, including odd L. A unique dominant transfer eigenvalue must be positive because all odd physical traces are positive; the signed-spectrum proof in the cited lemma applies to the same uniform chain history transfer. Directed lower roots give safe C. Every C>1/2, and exp(beta*gap)*(1-C)<C is checked exactly. This proves a unique ground state and the desired gap throughout that window.

The complete windows are:

- n60:60–120,120–240,240–480,480–960; asymptotic all L>=960.
- n56:56–112,112–224,224–448,448–896,896–1792; asymptotic all L>=1792.
- n54:54–108,108–216,216–432,432–864,864–1728,1728–3456; asymptotic all L>=3456.

The code also checks the first window inside the asymptotic region as an overlapping consistency check. No interval below the stated first endpoint is omitted from the claimed range. Sizes below54 remain outside every new claim.

## Scan scope and absence of minimum claims

scan_results.json is explicitly a floating proposal scan, not an exclusion proof. It tests even n40..60, even base ell16..40 with ell<=n, and cooling ratios1.50..3.20 in steps0.02, using only a ground Boltzmann anchor greater than1. It finds candidates beginning at n54 in that grid. In particular it finds none for n52, even though the new MPS104 anchor has negative shifted energy. A denser grid, different moment bound, exploiting the magnitude of negative trial energy, another temperature, or another initialization could succeed. The scan establishes no all-temperature failure and no minimality.

## Reproduction, exactness and seals

Run REPRODUCE.sh. The contraction stages have oneCPU/700MiB/600CPU-second limits per batch. The scalar replay takes about0.2CPU seconds and12MiB. It checks the sibling result seal, benchmark48 equality, archived120 equality, exact negative shifted Rayleigh signs, all dominant-atom updates, seed purities, all recurrence steps, all finite windows and final asymptotic margins. Rational powers are enclosed by integer-root bisection with explicit power checks. All physical long traces are inferred from the nine small archived heat inputs; no new thermal job or many-body eigensolver was run.

INPUT_SHA256.json identifies consumed files. MANIFEST_SHA256.json seals this new package. The original archive, previous assessment, all earlier seals, root state and GitHub remain untouched. For scientific acceptance a separate reviewer must independently reconstruct the new contractions and the scalar/analytic chain, especially the direct-sector-power variant at n54.
