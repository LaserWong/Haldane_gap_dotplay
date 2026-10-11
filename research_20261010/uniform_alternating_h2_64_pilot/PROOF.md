# Exact physical64 H² and variance-refined fidelity

2026-10-11 04:46 UTC. Producer physical/scalar result requiring independent review. No new interval or physical32 H² calculation. All previously accepted packages remain immutable.

## 1. Observable and exact input identity

Use the accepted periodic spin-one uniform unit-exchange Hamiltonian H0=sum_j h_j and the same single periodic D26 MPS at L=64. The trial span is one-dimensional, MPS bond dimension26, full physical Hilbert dimension3^64. No full physical Hilbert vector is constructed.

The frozen local insertion file contains T,O=E_h,U=E_(h²),V=E_(h01h12+h12h01), with SHA2561e63ba284062733ec459fd0f2125874b561b407ef7d722897f1923336ff58581. The shared fixture.cpp matrix kernel, hashafaf61d76e1de0dceae377b0c61923bf3d2facf11f85a3915888a19707ad5214, is included unchanged; its renamed main is never executed. Independent observable review8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee verifies the local blocks and full physical L4/L6 H²/B² fixtures, including periodic closing bonds and both block-power signs.

This wrapper uses structured LENGTH=64, CONVOLUTION_POWER=LENGTH−3=61 and CONVOLUTION_SIGN=+1. Let

    Kplus=[[T,O],[0,T]], P61=(Kplus^61)_upper-diagonal,
    R61=(Kplus^61)_upper-right, P62=P61*T.

For every difference-charge block,

    N=Tr(P62*T²), H=64Tr(P62*O),
    H2=64[Tr(P62*U)+Tr(P61*V)+Tr(R61*O)].               (1)

Both the adjacent term and disjoint convolution have positive signs. Equation(1) is distinct from B²=64[same−adjacent+alternating-disjoint]. It is already tested at physical4/6 by the accepted fixture.

The11 block sides remain1,8,32,80,136,162,136,80,32,8,1. Every block recomputes and exactly matches N,H,same-bond and adjacent scalar contributions against the accepted64 B² checkpoints before its H² contribution is accepted. The expected64.txt table is produced from those frozen JSON records after verifying their manifest and every member, and is itself pinned.

The final sums N0_64 and total H0_64 match uniform_smaller_second_initialization_review/anchors.out, hash217e4ba47ad3544f4f8ce384970cdc501c77a5916a7f5883a86cadeb42df1af2. The scalar checker independently sums all11 checkpoints and rechecks every old-field identity. The total H² is nonnegative and at most(2L)²N, and H2*N−H² is nonnegative.

## 2. Exact variance result and normalization

Define the total energy variance of the normalized trial by

    sigma²=H2/N−(H/N)²=(H2*N−H²)/N².

Its exact rational is in scalar_result.json and its defining integers are in pilot.out. The display is

    sigma²=.0004964120744254386... .

This is a variance, not its square root and not a per-site value. It is unchanged under the energy shift aL. H/N is already total energy; no additional64 factor is applied. Exact GMP subtraction avoids floating cancellation between the two large terms.

## 3. Existing thermal data sharpen weight and finite gap

All thermal inputs are the already accepted ones at beta0=49/4, with shift a=700741/500000 per physical site. Let Q64 be the accepted shifted partition-function upper bound, mu=H/N+64a the exact total shifted trial mean, and q=<B64²>/96²=.007521781460785803... from the independently accepted B² contraction.

Variational E0'<=mu gives the actual Gibbs ground weight lower bound

    w>=lower_exp(−beta0*mu)/Q64≈.9176574240821238.

The checker independently verifies

    lower_exp(−beta0*E_lo)>Q64, E_lo=−702409/100000000,
    w−upper_exp(beta0*delta)(1−w)>0, delta=19681/100000.

Thus E0'>=E_lo, and the finite64 Hamiltonian has unique ground and gap>=.19681. These are finite-volume fidelity premises, not an all-size.19681 claim. The old purity-only.19 finite premise is not silently reused at a stronger value: the new directed weight inequality is checked from original Q and mu.

Put e=mu−E_lo. The energy-only trial infidelity satisfies

    epsilon0=e/delta≈.03564252859864026<1/2.

This identifies the ground-overlap branch before variance is used.

## 4. Pairwise variance controls ground overlap

Let F be the trial probability in the unique ground state, epsilon=1−F. The spectral variance identity and the finite gap give

    sigma²=sum_(i<j) p_i p_j(E_i−E_j)²
          >=F(1−F)delta².

The energy bound has already shown F>=1−epsilon0>1/2, so epsilon lies on the increasing branch of epsilon(1−epsilon). If4sigma²<=delta²,

    epsilon<=[1−sqrt(1−4sigma²/delta²)]/2.              (2)

Otherwise retain epsilon0. The checker uses the smaller of epsilon0 and an upward endpoint for(2). Here it obtains

    epsilon<=.012984463954072514...,
    F>=.9870155360459275... .

The threshold for a strict improvement over energy-only fidelity is sigma²<delta² epsilon0(1−epsilon0), approximately.0013313764754208206. The observed variance is well below it. No uncontrolled residual assumption or guess for E0 is used.

## 5. Fidelity to the staggered effect and Gibbs kappa

For O=B64²/96², 0<=O<=I. The trial expectation q is exact. If the actual ground expectation is alpha, Cauchy applied separately to sqrt(O) and sqrt(I−O) yields

    sqrt(F)<=sqrt(q alpha)+sqrt((1−q)(1−alpha)).

For a lower fidelity f>q this implies

    alpha<=[sqrt(fq)+sqrt((1−f)(1−q))]².

Use f=1−epsilon from(2), upward root endpoints and the actual Gibbs weight lower w. All excited-state effect expectations are bounded by1, so

    kappa64=Tr(rho0 B64²)/96²
       <=1−w+w alpha
       <=.11893272968811675...<119/1000=.119.             (3)

The exact rational alpha and kappa upper endpoints are saved. The result is an upper bound for the actual untwisted uniform Gibbs state at beta49/4, not merely the MPS expectation. Applying it to new alternating-chain intervals requires a separately verified seed/finite-bridge/bootstrap composition; none is claimed here.

## 6. Scalar arithmetic correction and preserved failed attempt

The first postproduction scalar script had a self-imposed one-second CPU limit. Its exact Rayleigh denominator propagated through140 Taylor terms, and the process was killed with exit137 before any scalar_result.json was produced. Physical H² outputs were already complete and unaffected. No independent wait4 record exists for this initial scalar-only call; its tool wall observation was2.787669337seconds. Because it was single-CPU, a conservative3CPU-second charge is preserved in scalar_attempt_FAILURE.json rather than claiming an unmeasured precise CPU cost.

Root authorized one specific scalar correction under3 child+1 parent CPU seconds. certify_scalar.py remains the failed historical source. The new certify_scalar_retry1.py first encloses every exponential argument between adjacent dyadics of denominator2^128, then evaluates the lower endpoint downward and upper endpoint upward. Monotonicity of exp preserves rigor and avoids propagating the original huge denominator through the Taylor sum. The exact huge variance fraction is retained without approximation.

The corrected arithmetic uses a120-decimal output grid, exact integer-root brackets,140 positive Taylor terms after argument reduction below1/16, a geometric remainder, reciprocal endpoints for negative arguments and outward repeated squaring. The dyadic argument width is explicitly enclosed; a120-place output grid does not falsely claim120-digit accuracy of that argument. Its width is far below every required strict scalar margin here.

The independent scalar launcher records wait4 .488720CPU seconds, parent.014570354CPU seconds, peak10496KiB,24 active polls, wall.513521029seconds, exit0, no watchdog. No further numerical retry occurred.

## 7. Physical and compilation controls

The sole physical pilot was authorized for40 aggregate CPU seconds, with39 child+1 parent,256MiB, sole CPU4 and120-second external wall timeout. After exec, the wrapper verifies hard CPU/address-space limits, exact affinity, default/unblocked SIGXCPU and parent-death SIGKILL. The independent parent actively polls process CPU, kills above38seconds, uses wait4, and saves complete per-block checkpoints. It refuses an existing attempt or checkpoint.

Physical run:18.231025 user+.216389 system=18.447414CPU seconds; parent.415477456CPU seconds; peak35652KiB; wall18.901852876seconds;443 active polls; exit0 and no watchdog. No physical retry or32 execution occurred.

Compilation was separately authorized for30CPU seconds/512MiB. Its child cap is29 plus a one-second parent reserve; parent hard memory is lowered only after fork, so the compiler can inherit512MiB. Observed compiler-tree wait4 cost6.973980CPU seconds and parent.155911665, peak205628KiB, total7.129891665. The active process poll observes the compiler driver; the retained wait4 total includes its compilation descendants. No compiler retry occurred.

Physical/scalar cumulative accounting is

    18.447414+.415477456+3+.488720+.014570354
      =22.366181810CPU seconds of40.

The3 term is the preserved conservative failed-scalar charge. Charging full one-second reserves for both measured numerical parents gives23.936134CPU seconds, still below40. Compilation remains separate. The new gate does not reset or consume unrecorded earlier scalar/physical budgets.

All source/input pins, logs, rejected scalar history, guarded resource records and final exact outputs are retained. Root documents and every prior sealed package remain unchanged. This package is producer-only until independently reconstructed and reviewed.
